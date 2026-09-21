from dataclasses import dataclass, replace

from src.agents import AgentContext, AgentRegistry
from src.router.router import route


@dataclass(frozen=True)
class OrchestrationResult:
    destination: str
    response: str


class Orchestrator:
    def __init__(self, agents: AgentRegistry, context: AgentContext) -> None:
        self._agents = agents
        self._context = context

    async def execute(self, message: str) -> OrchestrationResult:
        destination = route(message)
        agent = self._agents.get(destination)
        context = self._context
        provider_for = getattr(context.model_provider, "provider_for", None)
        if provider_for is not None:
            context = replace(context, model_provider=provider_for(destination))
        response = await agent.execute(message, context)
        return OrchestrationResult(destination, response)
