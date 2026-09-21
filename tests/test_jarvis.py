import unittest
from unittest.mock import patch

from src.core import JarvisConfig
from src.core.jarvis import Jarvis, process_message


class JarvisTests(unittest.IsolatedAsyncioTestCase):
    async def test_process_message_routes_to_general_agent(self) -> None:
        with patch("builtins.print"):
            response = await process_message("bom dia")

        self.assertEqual(response, '[MODELO MOCK] Recebi: "bom dia"')

    async def test_process_message_routes_to_dev_agent(self) -> None:
        with patch("builtins.print"):
            response = await process_message("tem um bug no projeto")

        self.assertIn('[DEV] Tarefa: "tem um bug no projeto"', response)

    async def test_process_message_records_history(self) -> None:
        jarvis = Jarvis()

        with patch("builtins.print"):
            response = await jarvis.process_message("bom dia")

        messages = jarvis.context.history.all()
        self.assertEqual(response, '[MODELO MOCK] Recebi: "bom dia"')
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].content, "bom dia")
        self.assertEqual(messages[1].role, "assistant")
        self.assertEqual(messages[1].content, response)

    async def test_process_message_prints_route_when_debug_is_enabled(self) -> None:
        jarvis = Jarvis(config=JarvisConfig(debug=True))

        with patch("builtins.print") as print_mock:
            await jarvis.process_message("bom dia")

        print_mock.assert_called_once_with("Rota escolhida: general")

    async def test_process_message_does_not_print_route_when_debug_is_disabled(self) -> None:
        jarvis = Jarvis(config=JarvisConfig(debug=False))

        with patch("builtins.print") as print_mock:
            await jarvis.process_message("bom dia")

        print_mock.assert_not_called()
