import unittest

from src.memory import ConversationHistory, ConversationMessage


class ConversationHistoryTests(unittest.TestCase):
    def test_records_messages_in_order(self) -> None:
        history = ConversationHistory()

        history.add_user_message("oi")
        history.add_assistant_message("ola")

        messages = history.all()
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].content, "oi")
        self.assertEqual(messages[1].role, "assistant")
        self.assertEqual(messages[1].content, "ola")

    def test_returns_last_messages(self) -> None:
        history = ConversationHistory()
        history.add_user_message("1")
        history.add_assistant_message("2")
        history.add_user_message("3")

        self.assertEqual([message.content for message in history.last(2)], ["2", "3"])

    def test_clear_removes_messages(self) -> None:
        history = ConversationHistory()
        history.add_user_message("oi")

        history.clear()

        self.assertEqual(history.all(), [])

    def test_replace_swaps_messages(self) -> None:
        history = ConversationHistory()
        history.add_user_message("oi")

        history.replace([ConversationMessage(role="assistant", content="ola")])

        messages = history.all()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].role, "assistant")
        self.assertEqual(messages[0].content, "ola")
