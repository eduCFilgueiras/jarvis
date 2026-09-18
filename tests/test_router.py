import unittest

from src.router.router import route


class RouterTests(unittest.TestCase):
    def test_routes_dev_keywords_to_dev(self) -> None:
        self.assertEqual(route("Preciso corrigir um bug"), "dev")
        self.assertEqual(route("Ajuda com programação"), "dev")
        self.assertEqual(route("Analise este projeto"), "dev")

    def test_routes_other_messages_to_general(self) -> None:
        self.assertEqual(route("Bom dia"), "general")
