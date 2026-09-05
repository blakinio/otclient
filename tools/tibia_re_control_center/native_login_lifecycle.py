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

    def status(self) -> dict[str, object]:
        return {
            "state": "UNBOUND",
            "bound": False,
            "current": False,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_RUNTIME_NOT_BOUND",
        }

    def start(self) -> dict[str, object]:
        raise NativeLoginLifecycleError(
            "NATIVE_LOGIN_UNBOUND",
            "native login runtime is not bound",
        )


__all__ = ("NativeLoginLifecycle", "NativeLoginLifecycleError")
