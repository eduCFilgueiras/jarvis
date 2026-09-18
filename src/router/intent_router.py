from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    name: str
    tool_name: str | None = None


@dataclass(frozen=True)
class IntentRule:
    intent: Intent
    triggers: tuple[str, ...]

    def matches(self, input_text: str) -> bool:
        return any(trigger in input_text for trigger in self.triggers)


class IntentRouter:
    def __init__(self) -> None:
        self._rules = (
            IntentRule(
                intent=Intent(name="history"),
                triggers=(
                    "o que eu perguntei",
                    "perguntei antes",
                    "historico",
                    "histórico",
                    "resuma esta conversa",
                    "resumo da conversa",
                    "nossa conversa",
                ),
            ),
            IntentRule(
                intent=Intent(name="tool", tool_name="calculator"),
                triggers=(
                    "calcule",
                    "calcular",
                    "quanto e",
                    "quanto é",
                    "resultado de",
                ),
            ),
            IntentRule(
                intent=Intent(name="tool", tool_name="datetime"),
                triggers=(
                    "que hora",
                    "horas sao",
                    "horas são",
                    "qual a hora",
                    "data",
                    "hoje e",
                    "hoje é",
                    "dia de hoje",
                ),
            ),
            IntentRule(
                intent=Intent(name="tool", tool_name="files"),
                triggers=(
                    "listar arquivos",
                    "ler arquivo",
                ),
            ),
            IntentRule(
                intent=Intent(name="tool", tool_name="notes"),
                triggers=(
                    "anote",
                    "nota",
                    "crie uma nota",
                    "listar notas",
                    "liste notas",
                    "limpar notas",
                ),
            ),
            IntentRule(
                intent=Intent(name="tool", tool_name="todo"),
                triggers=(
                    "criar tarefa",
                    "crie uma tarefa",
                    "tarefa",
                    "listar tarefas",
                    "liste tarefas",
                    "concluir tarefa",
                    "limpar tarefas",
                ),
            ),
        )

    def route(self, message: str) -> Intent:
        input_text = message.lower()

        for rule in self._rules:
            if rule.matches(input_text):
                return rule.intent

        return Intent(name="default")
