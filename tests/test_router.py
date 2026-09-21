import unittest

from src.router.router import route


class RouterTests(unittest.TestCase):
    def test_routes_dev_keywords_to_dev(self) -> None:
        self.assertEqual(route("Preciso corrigir um bug"), "dev")
        self.assertEqual(route("Ajuda com programação"), "dev")
        self.assertEqual(route("Analise este codigo"), "dev")

    def test_routes_general_project_question_to_general(self) -> None:
        self.assertEqual(route("qual o objetivo do projeto"), "general")

    def test_routes_other_messages_to_general(self) -> None:
        self.assertEqual(route("Bom dia"), "general")
