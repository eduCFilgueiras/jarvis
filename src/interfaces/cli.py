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
            if session is not None and session.permissions is not None:
                request = session.permissions.pending_request
                if request is not None:
                    answer = input(
                        f"Jarvis: Permitir {request.tool_name}.{request.action} em "
                        f"{request.resource}? [s/N] "
                    ).strip().lower()
                    if answer in {"s", "sim", "y", "yes"}:
                        confirmed = command_router.confirm_pending()
                        if confirmed is not None:
                            print(confirmed)
                    else:
                        command_router.cancel_pending()
            if should_exit:
                break
            continue

        response = await process_message(message)
        print(f"Jarvis: {response}")

        if session is None or session.permissions is None:
            continue

        request = session.permissions.pending_request
        if request is None:
            continue

        answer = input(
            f"Jarvis: Permitir {request.tool_name}.{request.action} em "
            f"{request.resource}? [s/N] "
        ).strip().lower()

        if answer in {"s", "sim", "y", "yes"}:
            session.permissions.grant_pending()
            response = await process_message(message)
            print(f"Jarvis: {response}")
        else:
            session.permissions.deny_pending()
