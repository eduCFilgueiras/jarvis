from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class PermissionRequest:
    tool_name: str
    action: str
    resource: str


class PermissionStatus(StrEnum):
    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    reason: str
    status: PermissionStatus = PermissionStatus.DENY


class PermissionPolicy:
    def __init__(self, auto_allow_read_only: bool = True) -> None:
        self._auto_allow_read_only = auto_allow_read_only
        self._read_only_actions = {"list", "read"}
        self._pending_request: PermissionRequest | None = None
        self._granted_requests: set[PermissionRequest] = set()

    def check(self, request: PermissionRequest) -> PermissionDecision:
        if request in self._granted_requests:
            self._granted_requests.remove(request)
            return PermissionDecision(True, "permission granted for this request", PermissionStatus.ALLOW)

        if self._auto_allow_read_only and request.action in self._read_only_actions:
            return PermissionDecision(True, "read-only action allowed", PermissionStatus.ALLOW)

        if request.action == "delete":
            self._pending_request = None
            return PermissionDecision(False, "acao destrutiva bloqueada", PermissionStatus.DENY)

        self._pending_request = request
        return PermissionDecision(
            False,
            (
                f"Permissao necessaria para {request.tool_name}."
                f"{request.action} em {request.resource}."
            ),
            PermissionStatus.ASK,
        )

    @property
    def pending_request(self) -> PermissionRequest | None:
        return self._pending_request

    def grant_pending(self) -> bool:
        if self._pending_request is None:
            return False
        self._granted_requests.add(self._pending_request)
        self._pending_request = None
        return True

    def deny_pending(self) -> None:
        self._pending_request = None
