import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.memory import ConversationHistory, HistoryStorage


class HistoryStorageTests(unittest.TestCase):
    def test_saves_and_loads_history(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            history = ConversationHistory()
            history.add_user_message("oi")
            history.add_assistant_message("ola")

            storage = HistoryStorage(path)
            storage.save(history)
            messages = storage.load()

        self.assertEqual([message.role for message in messages], ["user", "assistant"])
        self.assertEqual([message.content for message in messages], ["oi", "ola"])

    def test_load_missing_file_returns_empty_list(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            messages = HistoryStorage(path).load()

        self.assertEqual(messages, [])
