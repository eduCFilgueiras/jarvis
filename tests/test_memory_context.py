import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents import AgentContext, GeneralAgent
from src.memory import ConversationHistory, MemoryCategory, PersistentMemory
from src.models import MockModelProvider
from src.security import PermissionPolicy
from src.tools import ToolRegistry


class MemoryContextTests(unittest.IsolatedAsyncioTestCase):
    async def test_general_agent_includes_limited_memory_context(self) -> None:
        with TemporaryDirectory() as directory:
            memory = PersistentMemory(Path(directory) / "memory.json")
            memory.add(MemoryCategory.PREFERENCE, "Prefere respostas curtas")
            context = AgentContext(
                tools=ToolRegistry(),
                history=ConversationHistory(),
                model_provider=MockModelProvider(),
                permissions=PermissionPolicy(),
                memory=memory,
            )

            response = await GeneralAgent().execute("bom dia", context)

        self.assertIn("Prefere respostas curtas", response)
