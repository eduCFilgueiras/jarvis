from .base import AgentContext, BaseAgent


class DevAgent(BaseAgent):
    async def execute(self, message: str, context: AgentContext) -> str:
        return f'[DEV] Recebi a tarefa: "{message}"'
