import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents import create_default_agent_registry
from src.core import JarvisConfig
from src.interfaces import CliSession, CommandRouter, CommandRule
from src.memory import ConversationHistory, MemoryCategory, PersistentMemory
from src.models import create_default_model_registry
from src.tools import create_default_tool_registry


def create_session(config: JarvisConfig | None = None) -> CliSession:
    return CliSession(
        agents=create_default_agent_registry(),
        tools=create_default_tool_registry(),
        history=ConversationHistory(),
        model_provider=create_default_model_registry(),
        config=config or JarvisConfig(),
    )


class CommandRouterTests(unittest.TestCase):
    def test_command_rule_stores_aliases(self) -> None:
        def handler() -> tuple[str, bool]:
            return "ok", False

        rule = CommandRule(aliases=("/ok",), handler=handler)

        self.assertEqual(rule.aliases, ("/ok",))
        self.assertEqual(rule.handler(), ("ok", False))

    def test_can_handle_known_command(self) -> None:
        router = CommandRouter(create_session())

        self.assertTrue(router.can_handle("/status"))

    def test_cannot_handle_unknown_command(self) -> None:
        router = CommandRouter(create_session())

        self.assertFalse(router.can_handle("/desconhecido"))

    def test_handles_tools_command(self) -> None:
        router = CommandRouter(create_session())

        response, should_exit = router.handle("/tools")

        self.assertEqual(
            response,
            "Jarvis: Ferramentas disponiveis: calculator, datetime, files, notes, todo.",
        )
        self.assertFalse(should_exit)

    def test_handles_memory_command(self) -> None:
        session = create_session()
        session = CliSession(
            agents=session.agents,
            tools=session.tools,
            history=session.history,
            model_provider=session.model_provider,
            config=session.config,
            memory=PersistentMemory(Path("/tmp/jarvis-test-memory.json")),
        )
        session.memory.add(MemoryCategory.PROJECT, "Jarvis")

        response, should_exit = CommandRouter(session).handle("/memoria")

        self.assertIn("[project] Jarvis", response)
        self.assertFalse(should_exit)

    def test_handles_debug_command(self) -> None:
        session = create_session()
        router = CommandRouter(session)

        response, should_exit = router.handle("/debug off")

        self.assertEqual(response, "Jarvis: Debug desativado.")
        self.assertFalse(session.config.debug)
        self.assertFalse(should_exit)

    def test_handles_version_command(self) -> None:
        router = CommandRouter(create_session())

        response, should_exit = router.handle("/version")

        self.assertEqual(response, "Jarvis: Versao 0.1.0.")
        self.assertFalse(should_exit)

    def test_handles_model_command(self) -> None:
        router = CommandRouter(create_session())

        response, should_exit = router.handle("/model")

        self.assertEqual(
            response,
            "Jarvis: Modelo ativo: mock. Disponiveis: mock, openai.",
        )
        self.assertFalse(should_exit)

    def test_handles_model_switch_command(self) -> None:
        session = create_session()
        router = CommandRouter(session)

        response, should_exit = router.handle("/model openai")

        self.assertEqual(response, "Jarvis: Modelo ativo alterado para openai.")
        self.assertEqual(session.model_provider.name, "openai")
        self.assertFalse(should_exit)

    def test_handles_unknown_model_switch_command(self) -> None:
        router = CommandRouter(create_session())

        response, should_exit = router.handle("/model local")

        self.assertEqual(
            response,
            "Jarvis: Modelo desconhecido: local. Disponiveis: mock, openai.",
        )
        self.assertFalse(should_exit)

    def test_handles_save_and_load_commands(self) -> None:
        with TemporaryDirectory() as directory:
            config = JarvisConfig(history_path=Path(directory) / "history.json")
            session = create_session(config)
            session.history.add_user_message("oi")
            router = CommandRouter(session)

            save_response, save_should_exit = router.handle("/salvar")
            session.history.clear()
            load_response, load_should_exit = router.handle("/carregar")

        self.assertEqual(
            save_response,
            f"Jarvis: Historico salvo em {config.history_path}.",
        )
        self.assertEqual(
            load_response,
            f"Jarvis: Historico carregado com 1 mensagens de {config.history_path}.",
        )
        self.assertEqual(session.history.all()[0].content, "oi")
        self.assertFalse(save_should_exit)
        self.assertFalse(load_should_exit)

    def test_handles_diagnostics_command(self) -> None:
        session = create_session()
        session.history.add_user_message("oi")
        router = CommandRouter(session)

        response, should_exit = router.handle("/diagnostico")

        self.assertIn("Jarvis: Diagnostico:", response)
        self.assertIn("- version: 0.1.0", response)
        self.assertIn("- environment: local", response)
        self.assertIn("- agents: dev, general", response)
        self.assertIn("- tools: calculator, datetime, files, notes, todo", response)
        self.assertIn("- model_active: mock", response)
        self.assertIn("- messages: 1", response)
        self.assertFalse(should_exit)

    def test_handles_export_command(self) -> None:
        with TemporaryDirectory() as directory:
            config = JarvisConfig(export_path=Path(directory) / "session.md")
            session = create_session(config)
            session.history.add_user_message("oi")
            router = CommandRouter(session)

            response, should_exit = router.handle("/exportar")
            content = config.export_path.read_text(encoding="utf-8")

        self.assertEqual(response, f"Jarvis: Sessao exportada em {config.export_path}.")
        self.assertIn("# Jarvis Session Export", content)
        self.assertIn("**User:** oi", content)
        self.assertFalse(should_exit)
