from __future__ import annotations

"""Fail-closed composition seam for the native official-client login lifecycle."""


class NativeLoginLifecycleError(RuntimeError):
    def __init__(self, code: str, safe_message: str, *, physical_effect: bool = False) -> None:
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message
        self.physical_effect = physical_effect


class NativeLoginLifecycle:
    """Authority-free default lifecycle until trusted runtime composition binds it."""

    def __init__(self, *, executor: object | None = None) -> None:
        self._executor = executor

    def status(self) -> dict[str, object]:
        if self._executor is not None:
            return dict(self._executor.status())
        return {
            "state": "UNBOUND",
            "bound": False,
            "current": False,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_RUNTIME_NOT_BOUND",
        }

    def start(self, operation_id: str | None = None) -> dict[str, object]:
        if self._executor is None:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_UNBOUND",
                "native login runtime is not bound",
            )
        if operation_id is None:
            raise NativeLoginLifecycleError(
                "NATIVE_LOGIN_OPERATION_ID_REQUIRED",
                "native login operation identity is required",
            )
        return dict(self._executor.start(operation_id))


__all__ = ("NativeLoginLifecycle", "NativeLoginLifecycleError")
