from src.memory import ConversationMessage

from .provider import ModelProvider


class MockModelProvider(ModelProvider):
    name = "mock"

    async def generate(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> str:
        return f'[MODELO MOCK] Recebi: "{message}"'
