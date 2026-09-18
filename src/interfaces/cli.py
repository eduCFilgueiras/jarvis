from collections.abc import Awaitable, Callable

from src.interfaces.commands import EXIT_COMMANDS, CliSession, CommandRouter

MessageProcessor = Callable[[str], Awaitable[str]]


async def run_cli(
    process_message: MessageProcessor,
    session: CliSession | None = None,
) -> None:
    command_router = CommandRouter(session) if session is not None else None

    while True:
        message = input("Voce: ").strip()

        if not message:
            continue

        if message.lower() in EXIT_COMMANDS:
            print("Jarvis: Ate logo.")
            break

        if command_router is not None and command_router.can_handle(message):
            response, should_exit = command_router.handle(message)
            print(response)
            if should_exit:
                break
            continue

        response = await process_message(message)
        print(f"Jarvis: {response}")
