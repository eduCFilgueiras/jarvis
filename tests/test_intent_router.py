import unittest

from src.router.intent_router import Intent, IntentRule, IntentRouter


class IntentRouterTests(unittest.TestCase):
    def test_intent_rule_matches_trigger(self) -> None:
        rule = IntentRule(
            intent=Intent(name="default"),
            triggers=("ola",),
        )

        self.assertTrue(rule.matches("ola mundo"))

    def test_routes_datetime_intent(self) -> None:
        intent = IntentRouter().route("que horas sao?")

        self.assertEqual(intent.name, "tool")
        self.assertEqual(intent.tool_name, "datetime")

    def test_routes_calculator_intent(self) -> None:
        intent = IntentRouter().route("calcule 2 + 2")

        self.assertEqual(intent.name, "tool")
        self.assertEqual(intent.tool_name, "calculator")

    def test_routes_history_intent(self) -> None:
        intent = IntentRouter().route("o que eu perguntei antes?")

        self.assertEqual(intent.name, "history")
        self.assertIsNone(intent.tool_name)

    def test_routes_notes_intent(self) -> None:
        intent = IntentRouter().route("anote comprar cafe")

        self.assertEqual(intent.name, "tool")
        self.assertEqual(intent.tool_name, "notes")

    def test_routes_files_intent(self) -> None:
        intent = IntentRouter().route("listar arquivos")

        self.assertEqual(intent.name, "tool")
        self.assertEqual(intent.tool_name, "files")

    def test_routes_todo_intent(self) -> None:
        intent = IntentRouter().route("criar tarefa pagar conta")

        self.assertEqual(intent.name, "tool")
        self.assertEqual(intent.tool_name, "todo")

    def test_routes_default_intent(self) -> None:
        intent = IntentRouter().route("bom dia")

        self.assertEqual(intent.name, "default")
        self.assertIsNone(intent.tool_name)
