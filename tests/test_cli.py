import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents import create_default_agent_registry
from src.core import JarvisConfig
from src.interfaces import CliSession
from src.interfaces.cli import run_cli
from src.memory import ConversationHistory
from src.models import create_default_model_registry
from src.tools import create_default_tool_registry


async def fake_process_message(message: str) -> str:
    return f"processado: {message}"


def create_test_session(history: ConversationHistory | None = None) -> CliSession:
    return CliSession(
        agents=create_default_agent_registry(),
        tools=create_default_tool_registry(),
        history=history or ConversationHistory(),
        model_provider=create_default_model_registry(),
        config=JarvisConfig(),
    )


class CliTests(unittest.IsolatedAsyncioTestCase):
    async def test_processes_messages_until_exit(self) -> None:
        inputs = iter(["oi", "calcule 2 + 2", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call("Jarvis: processado: oi")
        print_mock.assert_any_call("Jarvis: processado: calcule 2 + 2")
        print_mock.assert_any_call("Jarvis: Ate logo.")

    async def test_ignores_empty_messages(self) -> None:
        inputs = iter(["", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_called_once_with("Jarvis: Ate logo.")

    async def test_help_command_prints_available_commands(self) -> None:
        inputs = iter(["/ajuda", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call(
            "Jarvis: Comandos disponiveis: /ajuda, /historico, /limpar, "
            "/status, /tools, /memoria, /agents, /config, /version, /model, /debug on, /debug off, "
            "/salvar, /carregar, /exportar, /diagnostico, sair, exit, quit, q."
        )

    async def test_history_command_prints_session_history(self) -> None:
        history = ConversationHistory()
        history.add_user_message("oi")
        history.add_assistant_message("ola")
        inputs = iter(["/historico", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session(history))

        print_mock.assert_any_call("Jarvis: Historico da sessao:\nVoce: oi\nJarvis: ola")

    async def test_clear_command_clears_session_history(self) -> None:
        history = ConversationHistory()
        history.add_user_message("oi")
        inputs = iter(["/limpar", "/historico", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session(history))

        self.assertEqual(history.all(), [])
        print_mock.assert_any_call("Jarvis: Historico limpo.")
        print_mock.assert_any_call("Jarvis: Ainda nao ha historico nesta sessao.")

    async def test_tools_command_prints_registered_tools(self) -> None:
        inputs = iter(["/tools", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call(
            "Jarvis: Ferramentas disponiveis: calculator, datetime, files, notes, todo."
        )

    async def test_agents_command_prints_registered_agents(self) -> None:
        inputs = iter(["/agents", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call("Jarvis: Agentes disponiveis: dev, general.")

    async def test_status_command_prints_session_status(self) -> None:
        history = ConversationHistory()
        history.add_user_message("oi")
        inputs = iter(["/status", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session(history))

        print_mock.assert_any_call(
            "Jarvis: Status: agents=2, tools=5, model=mock, mensagens=1, debug=True."
        )

    async def test_config_command_prints_current_config(self) -> None:
        inputs = iter(["/config", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call(
            "Jarvis: Config: assistant_name=Jarvis, version=0.1.0, "
            "environment=local, language=pt-BR, debug=True, timezone=local, history_limit=5, "
            "history_path=data/history.json, export_path=data/session.md."
        )

    async def test_debug_command_updates_config(self) -> None:
        session = create_test_session()
        inputs = iter(["/debug off", "/config", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=session)

        self.assertFalse(session.config.debug)
        print_mock.assert_any_call("Jarvis: Debug desativado.")
        print_mock.assert_any_call(
            "Jarvis: Config: assistant_name=Jarvis, version=0.1.0, "
            "environment=local, language=pt-BR, debug=False, timezone=local, history_limit=5, "
            "history_path=data/history.json, export_path=data/session.md."
        )

    async def test_version_command_prints_project_version(self) -> None:
        inputs = iter(["/version", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call("Jarvis: Versao 0.1.0.")

    async def test_save_and_load_commands_use_session_history_path(self) -> None:
        with TemporaryDirectory() as directory:
            history = ConversationHistory()
            history.add_user_message("oi")
            session = create_test_session(history)
            session.config.history_path = Path(directory) / "history.json"
            inputs = iter(["/salvar", "/limpar", "/carregar", "/historico", "sair"])

            with (
                patch("builtins.input", side_effect=lambda _: next(inputs)),
                patch("builtins.print") as print_mock,
            ):
                await run_cli(fake_process_message, session=session)

            print_mock.assert_any_call(
                f"Jarvis: Historico salvo em {session.config.history_path}."
            )
            print_mock.assert_any_call(
                "Jarvis: Historico da sessao:\nVoce: oi"
            )

    async def test_model_command_prints_active_model_provider(self) -> None:
        inputs = iter(["/model", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        print_mock.assert_any_call(
            "Jarvis: Modelo ativo: mock. Disponiveis: mock, openai."
        )

    async def test_model_command_switches_active_model_provider(self) -> None:
        session = create_test_session()
        inputs = iter(["/model openai", "/model", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=session)

        self.assertEqual(session.model_provider.name, "openai")
        print_mock.assert_any_call("Jarvis: Modelo ativo alterado para openai.")
        print_mock.assert_any_call(
            "Jarvis: Modelo ativo: openai. Disponiveis: mock, openai."
        )

    async def test_diagnostics_command_prints_runtime_details(self) -> None:
        inputs = iter(["/diagnostico", "sair"])

        with (
            patch("builtins.input", side_effect=lambda _: next(inputs)),
            patch("builtins.print") as print_mock,
        ):
            await run_cli(fake_process_message, session=create_test_session())

        printed = "\n".join(str(call.args[0]) for call in print_mock.call_args_list)
        self.assertIn("Jarvis: Diagnostico:", printed)
        self.assertIn("- agents: dev, general", printed)

    async def test_export_command_writes_session_file(self) -> None:
        with TemporaryDirectory() as directory:
            history = ConversationHistory()
            history.add_user_message("oi")
            session = create_test_session(history)
            session.config.export_path = Path(directory) / "session.md"
            inputs = iter(["/exportar", "sair"])

            with (
                patch("builtins.input", side_effect=lambda _: next(inputs)),
                patch("builtins.print") as print_mock,
            ):
                await run_cli(fake_process_message, session=session)

            content = session.config.export_path.read_text(encoding="utf-8")

        print_mock.assert_any_call(
            f"Jarvis: Sessao exportada em {session.config.export_path}."
        )
        self.assertIn("**User:** oi", content)
