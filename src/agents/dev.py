from .base import AgentContext, BaseAgent


class DevAgent(BaseAgent):
    async def execute(self, message: str, context: AgentContext) -> str:
        return (
            f'[DEV] Plano inicial para: "{message}". '
            "Vou analisar o contexto, propor as alteracoes e pedir autorizacao "
            "antes de executar qualquer escrita."
        )
