import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.tools import FilesTool


class FilesToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_lists_files(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "b.txt").write_text("b", encoding="utf-8")
            tool = FilesTool(root)

            response = await tool.execute("listar arquivos")

        self.assertEqual(response, "Arquivos:\na.txt\nb.txt")

    async def test_reads_file(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.txt").write_text("ola", encoding="utf-8")
            tool = FilesTool(root)

            response = await tool.execute("ler arquivo a.txt")

        self.assertEqual(response, "Conteudo de a.txt:\nola")

    async def test_blocks_paths_outside_root(self) -> None:
        with TemporaryDirectory() as directory:
            tool = FilesTool(Path(directory))

            with self.assertRaises(ValueError):
                await tool.execute("ler arquivo ../fora.txt")

    async def test_truncates_large_file(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.txt").write_text("abcdef", encoding="utf-8")
            tool = FilesTool(root, max_chars=3)

            response = await tool.execute("ler arquivo a.txt")

        self.assertEqual(response, "Conteudo de a.txt:\nabc\n...[truncado]")
