from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionRequest:
    tool_name: str
    action: str
    resource: str


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    reason: str


class PermissionPolicy:
    def __init__(self, auto_allow_read_only: bool = True) -> None:
        self._auto_allow_read_only = auto_allow_read_only
        self._read_only_actions = {"list", "read"}

    def check(self, request: PermissionRequest) -> PermissionDecision:
        if self._auto_allow_read_only and request.action in self._read_only_actions:
            return PermissionDecision(allowed=True, reason="read-only action allowed")

        return PermissionDecision(
            allowed=False,
            reason=(
                f"Permissao necessaria para {request.tool_name}."
                f"{request.action} em {request.resource}."
            ),
        )
