import os

from src.memory import ConversationMessage

from .provider import ModelProvider


class OpenAIModelProvider(ModelProvider):
    name = "openai"

    def __init__(self, model: str = "gpt-5") -> None:
        self._model = model

    @property
    def configured(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    async def generate(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> str:
        if not os.environ.get("OPENAI_API_KEY"):
            return "OpenAI nao esta configurado. Defina OPENAI_API_KEY para usar este modelo."

        try:
            from openai import AsyncOpenAI
        except ImportError:
            return "SDK da OpenAI nao esta instalado. Instale a dependencia openai para usar este modelo."

        client = AsyncOpenAI()
        response = await client.responses.create(
            model=self._model,
            input=self._format_input(message, history),
        )
        return response.output_text

    def _format_input(
        self,
        message: str,
        history: list[ConversationMessage],
    ) -> list[dict[str, str]]:
        previous_messages = [
            {"role": item.role, "content": item.content}
            for item in history[-10:]
            if item.role in {"user", "assistant"}
        ]

        if not previous_messages or previous_messages[-1]["content"] != message:
            previous_messages.append({"role": "user", "content": message})

        return [
            {
                "role": "system",
                "content": (
                    "Voce e o Jarvis, um assistente pessoal. Responda sempre em portugues do Brasil. "
                    "Se o usuario estiver falando por voz, responda em no maximo duas frases curtas. "
                    "Se a pergunta for simples, responda diretamente e nao explique o fluxo interno."
                ),
            },
            *previous_messages,
        ]
