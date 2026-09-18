from .base import BaseAgent
from .dev import DevAgent
from .general import GeneralAgent


class AgentRegistry:
    def __init__(self, fallback: str = "general") -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._fallback = fallback

    def register(self, name: str, agent: BaseAgent) -> None:
        self._agents[name] = agent

    def get(self, name: str) -> BaseAgent:
        return self._agents.get(name, self._agents[self._fallback])

    def names(self) -> list[str]:
        return sorted(self._agents)


def create_default_agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register("dev", DevAgent())
    registry.register("general", GeneralAgent())
    return registry
