import unittest

from src.agents import AgentContext, create_default_agent_registry
from src.core.orchestrator import Orchestrator
from src.memory import ConversationHistory
from src.models import create_default_model_registry
from src.security import PermissionPolicy
from src.tools import create_default_tool_registry


class OrchestratorTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_destination_and_agent_response(self) -> None:
        context = AgentContext(
            tools=create_default_tool_registry(),
            history=ConversationHistory(),
            model_provider=create_default_model_registry(),
            permissions=PermissionPolicy(),
        )

        result = await Orchestrator(
            create_default_agent_registry(), context
        ).execute("tem um bug no projeto")

        self.assertEqual(result.destination, "dev")
        self.assertIn("Plano inicial", result.response)

    async def test_resolves_provider_for_destination(self) -> None:
        models = create_default_model_registry()
        models.set_route("dev", "openai")
        context = AgentContext(
            tools=create_default_tool_registry(),
            history=ConversationHistory(),
            model_provider=models,
            permissions=PermissionPolicy(),
        )

        result = await Orchestrator(
            create_default_agent_registry(), context
        ).execute("tem um bug no projeto")

        self.assertEqual(result.destination, "dev")
        self.assertIn("Plano inicial", result.response)
