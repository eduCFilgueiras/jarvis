import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.tools import TodoTool


class TodoToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_adds_and_lists_todos(self) -> None:
        with TemporaryDirectory() as directory:
            tool = TodoTool(Path(directory) / "todos.json")

            add_response = await tool.execute("criar tarefa pagar conta")
            list_response = await tool.execute("listar tarefas")

        self.assertEqual(add_response, "Tarefa criada: pagar conta")
        self.assertEqual(list_response, "Tarefas:\n1. [ ] pagar conta")

    async def test_completes_todo(self) -> None:
        with TemporaryDirectory() as directory:
            tool = TodoTool(Path(directory) / "todos.json")

            await tool.execute("criar tarefa pagar conta")
            complete_response = await tool.execute("concluir tarefa 1")
            list_response = await tool.execute("listar tarefas")

        self.assertEqual(complete_response, "Tarefa concluida: pagar conta")
        self.assertEqual(list_response, "Tarefas:\n1. [x] pagar conta")

    async def test_clears_todos(self) -> None:
        with TemporaryDirectory() as directory:
            tool = TodoTool(Path(directory) / "todos.json")

            await tool.execute("criar tarefa pagar conta")
            clear_response = await tool.execute("limpar tarefas")
            list_response = await tool.execute("listar tarefas")

        self.assertEqual(clear_response, "Tarefas apagadas.")
        self.assertEqual(list_response, "Nenhuma tarefa salva.")

    async def test_rejects_empty_task(self) -> None:
        with TemporaryDirectory() as directory:
            tool = TodoTool(Path(directory) / "todos.json")

            with self.assertRaises(ValueError):
                await tool.execute("criar tarefa")
