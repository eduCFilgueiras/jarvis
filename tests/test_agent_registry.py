import unittest

from src.agents.dev import DevAgent
from src.agents.general import GeneralAgent
from src.agents.registry import AgentRegistry, create_default_agent_registry


class AgentRegistryTests(unittest.TestCase):
    def test_default_registry_contains_builtin_agents(self) -> None:
        registry = create_default_agent_registry()

        self.assertEqual(registry.names(), ["dev", "general"])
        self.assertIsInstance(registry.get("dev"), DevAgent)
        self.assertIsInstance(registry.get("general"), GeneralAgent)

    def test_unknown_agent_uses_fallback(self) -> None:
        registry = create_default_agent_registry()

        self.assertIsInstance(registry.get("unknown"), GeneralAgent)

    def test_register_adds_agent(self) -> None:
        registry = AgentRegistry()
        registry.register("general", GeneralAgent())
        registry.register("dev", DevAgent())

        self.assertEqual(registry.names(), ["dev", "general"])
