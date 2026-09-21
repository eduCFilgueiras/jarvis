import unittest

from src.interfaces.web import ControlState


class WebControlTests(unittest.TestCase):
    def test_state_snapshot_contains_observability_fields(self) -> None:
        state = ControlState()
        state.update("processing", "teste")
        snapshot = state.snapshot()

        self.assertEqual(snapshot["status"], "processing")
        self.assertEqual(snapshot["events"], ["teste"])
        self.assertIn("transcript", snapshot)
        self.assertIn("response", snapshot)

    def test_state_tracks_and_clears_conversation(self) -> None:
        state = ControlState()
        state.add_turn("user", "ola")
        state.add_turn("assistant", "ola, como posso ajudar?")

        self.assertEqual(len(state.snapshot()["history"]), 2)
        state.clear()
        self.assertEqual(state.snapshot()["history"], [])
