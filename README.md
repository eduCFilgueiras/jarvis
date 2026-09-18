# Jarvis

Jarvis is a modular personal assistant prototype.

The current Python implementation keeps the architecture split into:

- `core`: orchestration
- `router`: message routing
- `agents`: specialized execution units
- `tools`: local tool registry
- `models`: model provider abstraction
- `memory`: in-session conversation history
- `interfaces`: CLI and internal commands
- `security`: permission policy primitives

## Run

```bash
python3 main.py
```

## Optional OpenAI Setup

Jarvis runs with the mock model by default. To enable the optional OpenAI
provider:

```bash
pip install -e ".[openai]"
export OPENAI_API_KEY="your_api_key_here"
python3 main.py
```

Inside the CLI:

```text
/model openai
```

Use `.env.example` as a reference for required environment variables. The app
does not load `.env` automatically yet; export variables in your shell.

## Test

```bash
python3 -m unittest discover
```

## Current Flow

```text
main.py
  -> src/interfaces/cli.py
  -> src/core/jarvis.py
      -> src/memory/conversation_history.py
      -> src/router/router.py
      -> src/router/intent_router.py
      -> src/agents/registry.py
      -> src/agents/dev.py or src/agents/general.py
      -> src/tools/registry.py
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Commands](docs/COMMANDS.md)
- [Environments](docs/ENVIRONMENTS.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Current Tools

- `calculator`: answers simple arithmetic questions.
- `datetime`: answers simple date and time questions.
- `files`: lists and reads files inside the project directory.
- `notes`: saves, lists, and clears local notes in `data/notes.json`.
- `todo`: creates, lists, completes, and clears local tasks in `data/todos.json`.

## Current Memory

Jarvis keeps an in-memory history during the current CLI session. You can ask
questions like `o que eu perguntei antes?` to recall previous user messages.

## Exit Commands

Use `sair`, `exit`, `quit`, or `q` to close the CLI.

## CLI Commands

- `/ajuda`: show available commands.
- `/historico`: show the current session history.
- `/limpar`: clear the current session history.
- `/status`: show runtime status.
- `/tools`: list registered tools.
- `/agents`: list registered agents.
- `/config`: show current configuration.
- `/version`: show the project version.
- `/diagnostico`: show a detailed runtime diagnostic.
- `/exportar`: export a Markdown snapshot of the current session to `data/session.md`.
- `/model`: show active and available model providers.
- `/model mock`: switch to the mock model provider.
- `/model openai`: switch to the optional OpenAI model provider.
- `/debug on`: enable route debug output.
- `/debug off`: disable route debug output.
- `/salvar`: save the current history to `data/history.json`.
- `/carregar`: load history from `data/history.json`.
