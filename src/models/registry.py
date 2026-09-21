from src.memory import ConversationMessage

from .mock_provider import MockModelProvider
from .openai_provider import OpenAIModelProvider
from .provider import ModelProvider


class ModelRegistry(ModelProvider):
    def __init__(self, active: str = "mock", routes: dict[str, str] | None = None) -> None:
        self._providers: dict[str, ModelProvider] = {}
        self._active = active
        self._routes = routes or {}

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

    def set_route(self, destination: str, provider_name: str) -> bool:
        if provider_name not in self._providers:
            return False
        self._routes[destination] = provider_name
        return True

    def provider_for(self, destination: str) -> ModelProvider:
        provider_name = self._routes.get(destination, self._active)
        return self._providers[provider_name]

    async def generate(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> str:
        return await self.provider_for("default").generate(message, history)


def create_default_model_registry() -> ModelRegistry:
    registry = ModelRegistry()
    registry.register(MockModelProvider())
    registry.register(OpenAIModelProvider())
    return registry
