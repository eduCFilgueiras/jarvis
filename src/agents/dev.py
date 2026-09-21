from .base import AgentContext, BaseAgent
from .dev_planner import DevPlanner
from src.security import PermissionRequest


class DevAgent(BaseAgent):
    async def execute(self, message: str, context: AgentContext) -> str:
        plan = DevPlanner(context.project_root).create_plan(message)
        decision = context.permissions.check(
            PermissionRequest("dev", "write", plan.task)
        )
        if not decision.allowed:
            return f"{plan.render()} Permissao pendente: {decision.reason}"
        return f"{plan.render()} Autorizacao recebida; execucao ainda nao iniciada."
