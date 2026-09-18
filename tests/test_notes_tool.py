import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.tools import NotesTool


class NotesToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_adds_and_lists_notes(self) -> None:
        with TemporaryDirectory() as directory:
            tool = NotesTool(Path(directory) / "notes.json")

            add_response = await tool.execute("anote comprar cafe")
            list_response = await tool.execute("listar notas")

        self.assertEqual(add_response, "Nota salva: comprar cafe")
        self.assertEqual(list_response, "Notas salvas:\n1. comprar cafe")

    async def test_clears_notes(self) -> None:
        with TemporaryDirectory() as directory:
            tool = NotesTool(Path(directory) / "notes.json")

            await tool.execute("anote comprar cafe")
            clear_response = await tool.execute("limpar notas")
            list_response = await tool.execute("listar notas")

        self.assertEqual(clear_response, "Notas apagadas.")
        self.assertEqual(list_response, "Nenhuma nota salva.")

    async def test_rejects_empty_note(self) -> None:
        with TemporaryDirectory() as directory:
            tool = NotesTool(Path(directory) / "notes.json")

            with self.assertRaises(ValueError):
                await tool.execute("anote")
