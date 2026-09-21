from dataclasses import dataclass
from enum import StrEnum

from collections.abc import Awaitable, Callable


ToolHandler = Callable[[str], Awaitable[str]]


class ToolRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    handler: ToolHandler
    risk: ToolRisk = ToolRisk.LOW

