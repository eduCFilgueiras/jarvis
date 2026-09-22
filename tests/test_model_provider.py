import unittest
from unittest.mock import patch

from src.models import MockModelProvider, OpenAIModelProvider, create_default_model_registry


class MockModelProviderTests(unittest.IsolatedAsyncioTestCase):
    async def test_generates_mock_response(self) -> None:
        response = await MockModelProvider().generate("ola", [])

        self.assertEqual(response, '[MODELO MOCK] Recebi: "ola"')

    async def test_openai_provider_reports_missing_api_key(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            response = await OpenAIModelProvider().generate("ola", [])

        self.assertEqual(
            response,
            "OpenAI nao esta configurado. Defina OPENAI_API_KEY para usar este modelo.",
        )

    async def test_default_registry_delegates_to_active_provider(self) -> None:
        registry = create_default_model_registry()

        response = await registry.generate("ola", [])

        self.assertEqual(registry.names(), ["mock", "openai"])
        self.assertEqual(response, '[MODELO MOCK] Recebi: "ola"')

    def test_default_registry_switches_active_provider(self) -> None:
        registry = create_default_model_registry()

        switched = registry.set_active("openai")

        self.assertTrue(switched)
        self.assertEqual(registry.name, "openai")

    def test_registry_falls_back_to_mock_without_openai_key(self) -> None:
        with patch.dict("os.environ", {"JARVIS_MODEL_PROVIDER": "openai"}, clear=True):
            registry = create_default_model_registry()
        self.assertEqual(registry.name, "mock")

    def test_registry_routes_provider_by_destination(self) -> None:
        registry = create_default_model_registry()

        self.assertTrue(registry.set_route("dev", "openai"))
        self.assertEqual(registry.provider_for("dev").name, "openai")
        self.assertEqual(registry.provider_for("general").name, "mock")

    def test_openai_input_sets_portuguese_concise_persona(self) -> None:
        prompt = OpenAIModelProvider()._format_input("ola", [])

        self.assertEqual(prompt[0]["role"], "user")
        self.assertEqual(prompt[0]["content"], "ola")
