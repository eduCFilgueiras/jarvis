from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.agents import AgentRegistry
from src.core.config import JarvisConfig
from src.memory import ConversationHistory, HistoryStorage, MemoryCategory, PersistentMemory
from src.models import ModelProvider
from src.security import PermissionPolicy, PermissionRequest
from src.tools import ToolRegistry

EXIT_COMMANDS = {"sair", "exit", "quit", "q"}
CommandHandler = Callable[[], tuple[str, bool]]


@dataclass(frozen=True)
class CliSession:
    agents: AgentRegistry
    tools: ToolRegistry
    history: ConversationHistory
    model_provider: ModelProvider
    config: JarvisConfig
    permissions: PermissionPolicy | None = None
    memory: PersistentMemory | None = None


@dataclass(frozen=True)
class CommandRule:
    aliases: tuple[str, ...]
    handler: CommandHandler


class CommandRouter:
    def __init__(self, session: CliSession) -> None:
        self._session = session
        self._handlers = self._create_handlers()
        self._pending_action: Callable[[], str] | None = None

    def can_handle(self, message: str) -> bool:
        return (
            message.lower() in self._handlers
            or self._is_debug_command(message)
            or self._is_model_command(message)
            or self._is_memory_write_command(message)
        )

    def handle(self, message: str) -> tuple[str, bool]:
        if self._is_memory_write_command(message):
            return self._memory_write(message)
        if self._is_debug_command(message):
            return self._debug(message)

        if self._is_model_command(message):
            return self._model(message)

        handler = self._handlers[message.lower()]
        return handler()

    def _create_handlers(self) -> dict[str, CommandHandler]:
        rules = (
            CommandRule(aliases=("/ajuda", "/help"), handler=self._help),
            CommandRule(
                aliases=("/historico", "/histórico", "/history"),
                handler=self._history,
            ),
            CommandRule(aliases=("/limpar", "/clear"), handler=self._clear),
            CommandRule(aliases=("/status",), handler=self._status),
            CommandRule(aliases=("/tools", "/ferramentas"), handler=self._tools),
            CommandRule(aliases=("/memoria", "/memória", "/memory"), handler=self._memory),
            CommandRule(aliases=("/agents", "/agentes"), handler=self._agents),
            CommandRule(aliases=("/config",), handler=self._config),
            CommandRule(aliases=("/version", "/versao", "/versão"), handler=self._version),
            CommandRule(
                aliases=("/diagnostico", "/diagnóstico", "/diagnostics"),
                handler=self._diagnostics,
            ),
            CommandRule(aliases=("/exportar", "/export"), handler=self._export),
            CommandRule(aliases=("/salvar", "/save"), handler=self._save),
            CommandRule(aliases=("/carregar", "/load"), handler=self._load),
        )

        handlers: dict[str, CommandHandler] = {}

        for rule in rules:
            for alias in rule.aliases:
                handlers[alias] = rule.handler

        return handlers

    def _help(self) -> tuple[str, bool]:
        return (
            "Jarvis: Comandos disponiveis: /ajuda, /historico, /limpar, "
            "/status, /tools, /memoria, /lembrar, /esquecer, /agents, /config, /version, /model, /debug on, /debug off, "
            "/salvar, /carregar, /exportar, /diagnostico, sair, exit, quit, q.",
            False,
        )

    def _history(self) -> tuple[str, bool]:
        if not self._session.history.all():
            return "Jarvis: Ainda nao ha historico nesta sessao.", False

        lines = ["Jarvis: Historico da sessao:"]

        for message in self._session.history.all():
            label = "Voce" if message.role == "user" else "Jarvis"
            lines.append(f"{label}: {message.content}")

        return "\n".join(lines), False

    def _clear(self) -> tuple[str, bool]:
        self._session.history.clear()
        return "Jarvis: Historico limpo.", False

    def _status(self) -> tuple[str, bool]:
        message_count = len(self._session.history.all())
        return (
            "Jarvis: Status: "
            f"agents={len(self._session.agents.names())}, "
            f"tools={len(self._session.tools.names())}, "
            f"model={self._session.model_provider.name}, "
            f"mensagens={message_count}, "
            f"debug={self._session.config.debug}.",
            False,
        )

    def _tools(self) -> tuple[str, bool]:
        names = ", ".join(self._session.tools.names())
        return f"Jarvis: Ferramentas disponiveis: {names}.", False

    def _memory(self) -> tuple[str, bool]:
        if self._session.memory is None:
            return "Jarvis: Memoria persistente indisponivel nesta sessao.", False
        items = self._session.memory.all()
        if not items:
            return "Jarvis: Nenhuma memoria persistente registrada.", False
        lines = ["Jarvis: Memoria persistente:"]
        lines.extend(f"- [{item.category.value}] {item.content}" for item in items)
        return "\n".join(lines), False

    def _memory_write(self, message: str) -> tuple[str, bool]:
        if self._session.memory is None or self._session.permissions is None:
            return "Jarvis: Memoria ou permissoes indisponiveis nesta sessao.", False
        if message.lower().startswith("/esquecer "):
            query = message.split(maxsplit=1)[1].strip()
            if not query:
                return "Jarvis: Informe o texto da memoria a remover.", False
            request = PermissionRequest("memory", "forget", query)
            decision = self._session.permissions.check(request)
            if decision.allowed:
                return self._forget_memory(query), False
            self._pending_action = lambda: self._forget_memory(query)
            return f"Jarvis: Permissao necessaria: {decision.reason}", False

        parts = message.split(maxsplit=2)
        if len(parts) < 3:
            return "Jarvis: Use /lembrar <preferencia|fato|projeto> <texto>.", False
        category_map = {
            "preferencia": MemoryCategory.PREFERENCE,
            "preference": MemoryCategory.PREFERENCE,
            "fato": MemoryCategory.FACT,
            "fact": MemoryCategory.FACT,
            "projeto": MemoryCategory.PROJECT,
            "project": MemoryCategory.PROJECT,
        }
        category = category_map.get(parts[1].lower())
        content = parts[2].strip()
        if category is None or not content:
            return "Jarvis: Categoria ou texto invalido.", False
        request = PermissionRequest("memory", "write", f"{category.value}: {content}")
        decision = self._session.permissions.check(request)
        if decision.allowed:
            return self._save_memory(category, content), False
        self._pending_action = lambda: self._save_memory(category, content)
        return f"Jarvis: Permissao necessaria: {decision.reason}", False

    def confirm_pending(self) -> str | None:
        if self._pending_action is None or self._session.permissions is None:
            return None
        self._session.permissions.grant_pending()
        action = self._pending_action
        self._pending_action = None
        return action()

    def cancel_pending(self) -> None:
        self._pending_action = None
        if self._session.permissions is not None:
            self._session.permissions.deny_pending()

    def _save_memory(self, category: MemoryCategory, content: str) -> str:
        self._session.memory.add(category, content)
        return f"Jarvis: Memoria salva em {category.value}."

    def _forget_memory(self, query: str) -> str:
        removed = self._session.memory.remove(query)
        return f"Jarvis: {removed} memoria(s) removida(s)."

    def _is_memory_write_command(self, message: str) -> bool:
        return message.lower().startswith(("/lembrar ", "/esquecer "))

    def _agents(self) -> tuple[str, bool]:
        names = ", ".join(self._session.agents.names())
        return f"Jarvis: Agentes disponiveis: {names}.", False

    def _config(self) -> tuple[str, bool]:
        config = self._session.config
        return (
            "Jarvis: Config: "
            f"assistant_name={config.assistant_name}, "
            f"version={config.version}, "
            f"environment={config.environment}, "
            f"language={config.language}, "
            f"debug={config.debug}, "
            f"timezone={config.timezone}, "
            f"history_limit={config.history_limit}, "
            f"history_path={config.history_path}, "
            f"export_path={config.export_path}.",
            False,
        )

    def _version(self) -> tuple[str, bool]:
        return f"Jarvis: Versao {self._session.config.version}.", False

    def _diagnostics(self) -> tuple[str, bool]:
        model_names = self._model_names()
        return (
            "Jarvis: Diagnostico:\n"
            f"- version: {self._session.config.version}\n"
            f"- environment: {self._session.config.environment}\n"
            f"- agents: {', '.join(self._session.agents.names())}\n"
            f"- tools: {', '.join(self._session.tools.names())}\n"
            f"- model_active: {self._session.model_provider.name}\n"
            f"- models_available: {model_names}\n"
            f"- messages: {len(self._session.history.all())}\n"
            f"- debug: {self._session.config.debug}\n"
            f"- history_path: {self._session.config.history_path}\n"
            f"- export_path: {self._session.config.export_path}",
            False,
        )

    def _export(self) -> tuple[str, bool]:
        path = self._session.config.export_path
        self._write_export(path)
        return f"Jarvis: Sessao exportada em {path}.", False

    def _model(self, message: str) -> tuple[str, bool]:
        parts = message.split(maxsplit=1)

        if len(parts) == 1:
            names = self._model_names()
            return (
                "Jarvis: Modelo ativo: "
                f"{self._session.model_provider.name}. Disponiveis: {names}.",
                False,
            )

        target = parts[1].strip().lower()
        set_active = getattr(self._session.model_provider, "set_active", None)

        if set_active is None or not set_active(target):
            names = self._model_names()
            return f"Jarvis: Modelo desconhecido: {target}. Disponiveis: {names}.", False

        return f"Jarvis: Modelo ativo alterado para {target}.", False

    def _save(self) -> tuple[str, bool]:
        storage = HistoryStorage(self._session.config.history_path)
        storage.save(self._session.history)
        return f"Jarvis: Historico salvo em {self._session.config.history_path}.", False

    def _load(self) -> tuple[str, bool]:
        storage = HistoryStorage(self._session.config.history_path)
        messages = storage.load()
        self._session.history.replace(messages)
        return (
            "Jarvis: Historico carregado "
            f"com {len(messages)} mensagens de {self._session.config.history_path}.",
            False,
        )

    def _write_export(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Jarvis Session Export",
            "",
            "## Status",
            "",
            f"- Agents: {', '.join(self._session.agents.names())}",
            f"- Tools: {', '.join(self._session.tools.names())}",
            f"- Model: {self._session.model_provider.name}",
            f"- Debug: {self._session.config.debug}",
            "",
            "## History",
            "",
        ]

        if not self._session.history.all():
            lines.append("_No messages in this session._")
        else:
            for message in self._session.history.all():
                label = "User" if message.role == "user" else "Jarvis"
                lines.append(f"**{label}:** {message.content}")

        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _is_debug_command(self, message: str) -> bool:
        return message.lower() in {"/debug on", "/debug off"}

    def _debug(self, message: str) -> tuple[str, bool]:
        enabled = message.lower() == "/debug on"
        self._session.config.debug = enabled
        state = "ativado" if enabled else "desativado"
        return f"Jarvis: Debug {state}.", False

    def _is_model_command(self, message: str) -> bool:
        return message.lower() == "/model" or message.lower().startswith("/model ")

    def _model_names(self) -> str:
        names = getattr(self._session.model_provider, "names", None)

        if names is None:
            return self._session.model_provider.name

        return ", ".join(names())
