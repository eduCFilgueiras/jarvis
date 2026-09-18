import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.core.config import JarvisConfig
from src.core.env import load_env


class EnvTests(unittest.TestCase):
    def test_load_env_reads_key_values(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text(
                "JARVIS_ENV=hml\nJARVIS_DEBUG=false\nQUOTED='value with spaces'\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {}, clear=True):
                loaded = load_env(path)

                self.assertEqual(loaded["JARVIS_ENV"], "hml")
                self.assertEqual(os.environ["JARVIS_DEBUG"], "false")
                self.assertEqual(os.environ["QUOTED"], "value with spaces")

    def test_load_env_does_not_override_existing_values(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / ".env"
            path.write_text("JARVIS_ENV=prd\n", encoding="utf-8")

            with patch.dict(os.environ, {"JARVIS_ENV": "local"}, clear=True):
                loaded = load_env(path)

                self.assertEqual(loaded, {})
                self.assertEqual(os.environ["JARVIS_ENV"], "local")

    def test_config_reads_environment_values_at_instantiation(self) -> None:
        with patch.dict(
            os.environ,
            {
                "JARVIS_ENV": "hml",
                "JARVIS_DEBUG": "false",
                "JARVIS_HISTORY_LIMIT": "12",
            },
            clear=True,
        ):
            config = JarvisConfig()

        self.assertEqual(config.environment, "hml")
        self.assertFalse(config.debug)
        self.assertEqual(config.history_limit, 12)
