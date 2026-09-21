from .base import AgentContext, BaseAgent
from src.router import IntentRouter
from src.security import PermissionRequest


class GeneralAgent(BaseAgent):
    def __init__(self, intent_router: IntentRouter | None = None) -> None:
        self._intent_router = intent_router or IntentRouter()

    async def execute(self, message: str, context: AgentContext) -> str:
        intent = self._intent_router.route(message)

        if intent.name == "history":
            return self._format_history(context)

        if intent.name == "tool" and intent.tool_name is not None:
            permission_response = self._check_tool_permission(
                intent.tool_name,
                message,
                context,
            )

            if permission_response is not None:
                return permission_response

            tool = context.tools.get(intent.tool_name)

            if tool is not None:
                try:
                    return await tool(message)
                except ValueError as error:
                    return f"Erro na ferramenta {intent.tool_name}: {error}"

        return await context.model_provider.generate(
            self._with_memory_context(message, context),
            context.history.all(),
        )

    def _with_memory_context(self, message: str, context: AgentContext) -> str:
        if context.memory is None:
            return message
        memories = context.memory.all()[:5]
        if not memories:
            return message
        context_lines = "\n".join(
            f"- {item.category.value}: {item.content}" for item in memories
        )
        return f"{message}\n\nMemorias relevantes locais:\n{context_lines}"

    def _check_tool_permission(
        self,
        tool_name: str,
        message: str,
        context: AgentContext,
    ) -> str | None:
        action = self._tool_action(tool_name, message)
        request = PermissionRequest(
            tool_name=tool_name,
            action=action,
            resource=message,
        )
        decision = context.permissions.check(request)

        if decision.allowed:
            return None

        return f"Permissao negada: {decision.reason}"

    def _tool_action(self, tool_name: str, message: str) -> str:
        input_text = message.lower().strip()
        if tool_name == "files":
            return "read" if input_text.startswith("ler arquivo") else "list"
        if tool_name == "notes":
            return "delete" if input_text.startswith("limpar notas") else (
                "write" if input_text.startswith(("anote", "nota", "crie uma nota")) else "read"
            )
        if tool_name == "todo":
            return "delete" if input_text.startswith("limpar tarefas") else (
                "write" if input_text.startswith(("criar tarefa", "crie uma tarefa", "tarefa", "concluir tarefa")) else "read"
            )
        return "read"

    def _format_history(self, context: AgentContext) -> str:
        previous_user_messages = [
            message.content
            for message in context.history.all()[:-1]
            if message.role == "user"
        ]

        if not previous_user_messages:
            return "Ainda nao tenho mensagens anteriores nesta conversa."

        summary = "; ".join(previous_user_messages[-5:])
        return f"Voce perguntou antes: {summary}."
