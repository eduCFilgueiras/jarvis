from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from src.memory import ConversationHistory, PersistentMemory
from src.models import ModelProvider
from src.security import PermissionPolicy
from src.tools import ToolRegistry


@dataclass(frozen=True)
class AgentContext:
    tools: ToolRegistry
    history: ConversationHistory
    model_provider: ModelProvider
    permissions: PermissionPolicy
    project_root: Path = Path(".")
    memory: PersistentMemory | None = None


class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, message: str, context: AgentContext) -> str:
        raise NotImplementedError
