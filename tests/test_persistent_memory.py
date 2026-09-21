import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.memory import MemoryCategory, PersistentMemory


class PersistentMemoryTests(unittest.TestCase):
    def test_saves_loads_filters_and_searches_memory(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            memory = PersistentMemory(path)
            memory.add(MemoryCategory.PREFERENCE, "Prefere respostas curtas")
            memory.add(MemoryCategory.PROJECT, "Projeto Jarvis")

            reloaded = PersistentMemory(path)

            self.assertEqual(len(reloaded.all(MemoryCategory.PROJECT)), 1)
            self.assertEqual(len(reloaded.search("jarvis")), 1)

    def test_clears_one_category(self) -> None:
        with TemporaryDirectory() as directory:
            memory = PersistentMemory(Path(directory) / "memory.json")
            memory.add(MemoryCategory.FACT, "Fato")
            memory.add(MemoryCategory.PROJECT, "Projeto")

            memory.clear(MemoryCategory.FACT)

            self.assertEqual(len(memory.all()), 1)
            self.assertEqual(memory.all()[0].category, MemoryCategory.PROJECT)
