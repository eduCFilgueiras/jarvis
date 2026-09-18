from collections.abc import Callable
from datetime import datetime

Clock = Callable[[], datetime]


class DateTimeTool:
    def __init__(self, clock: Clock | None = None) -> None:
        self._clock = clock or datetime.now

    async def execute(self, message: str) -> str:
        now = self._clock()
        input_text = message.lower()

        if "hora" in input_text:
            return f"Agora sao {now:%H:%M}."

        return f"Hoje e {now:%d/%m/%Y}."
