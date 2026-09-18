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

        return await context.model_provider.generate(message, context.history.all())

    def _check_tool_permission(
        self,
        tool_name: str,
        message: str,
        context: AgentContext,
    ) -> str | None:
        if tool_name != "files":
            return None

        action = "read" if message.lower().strip().startswith("ler arquivo") else "list"
        request = PermissionRequest(
            tool_name=tool_name,
            action=action,
            resource=message,
        )
        decision = context.permissions.check(request)

        if decision.allowed:
            return None

        return f"Permissao negada: {decision.reason}"

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
