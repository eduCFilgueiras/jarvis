# Commands

## Session

- `/ajuda`, `/help`: show available commands.
- `/historico`, `/histórico`, `/history`: show current session history.
- `/limpar`, `/clear`: clear current session history.
- `/salvar`, `/save`: save history to `data/history.json`.
- `/carregar`, `/load`: load history from `data/history.json`.
- `/exportar`, `/export`: export a Markdown snapshot to `data/session.md`.

## Inspection

- `/status`: show runtime counts and active model.
- `/tools`, `/ferramentas`: list registered tools.
- `/agents`, `/agentes`: list registered agents.
- `/config`: show current configuration.
- `/version`, `/versao`, `/versão`: show project version.
- `/diagnostico`, `/diagnóstico`, `/diagnostics`: show detailed diagnostics.

## Models

- `/model`: show active and available providers.
- `/model mock`: switch to the mock provider.
- `/model openai`: switch to the optional OpenAI provider.

## Debug

- `/debug on`: enable route debug output.
- `/debug off`: disable route debug output.

## Exit

- `sair`
- `exit`
- `quit`
- `q`

## Natural-Language Tool Examples

```text
que horas sao?
calcule 2 + 3 * 4
anote comprar cafe
listar notas
limpar notas
criar tarefa pagar conta
listar tarefas
concluir tarefa 1
limpar tarefas
listar arquivos
ler arquivo README.md
o que eu perguntei antes?
```
