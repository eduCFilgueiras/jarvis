from src.memory import ConversationMessage

from .mock_provider import MockModelProvider
from .openai_provider import OpenAIModelProvider
from .provider import ModelProvider


class ModelRegistry(ModelProvider):
    def __init__(self, active: str = "mock") -> None:
        self._providers: dict[str, ModelProvider] = {}
        self._active = active

    @property
    def name(self) -> str:
        return self._active

    def register(self, provider: ModelProvider) -> None:
        self._providers[provider.name] = provider

    def names(self) -> list[str]:
        return sorted(self._providers)

    def get(self, name: str) -> ModelProvider | None:
        return self._providers.get(name)

    def set_active(self, name: str) -> bool:
        if name not in self._providers:
            return False

        self._active = name
        return True

    async def generate(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> str:
        return await self._providers[self._active].generate(message, history)


def create_default_model_registry() -> ModelRegistry:
    registry = ModelRegistry()
    registry.register(MockModelProvider())
    registry.register(OpenAIModelProvider())
    return registry
