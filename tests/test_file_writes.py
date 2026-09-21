import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.tools import FilesTool


class FilesWriteTests(unittest.IsolatedAsyncioTestCase):
    async def test_writes_file_inside_root(self) -> None:
        with TemporaryDirectory() as directory:
            tool = FilesTool(Path(directory))
            response = await tool.execute("escrever arquivo notes.txt: ola")
            self.assertIn("Arquivo escrito", response)
            self.assertEqual((Path(directory) / "notes.txt").read_text(), "ola")

    async def test_blocks_write_outside_root(self) -> None:
        with TemporaryDirectory() as directory:
            tool = FilesTool(Path(directory))
            with self.assertRaises(ValueError):
                await tool.execute("escrever arquivo ../outside.txt: bloqueado")
