from abc import ABC, abstractmethod

from src.memory import ConversationMessage


class ModelProvider(ABC):
    name: str

    @abstractmethod
    async def generate(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> str:
        raise NotImplementedError
