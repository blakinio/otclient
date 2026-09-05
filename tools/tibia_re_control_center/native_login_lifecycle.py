from __future__ import annotations

"""Fail-closed composition seam for the native official-client login lifecycle."""


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


__all__ = ("NativeLoginLifecycle",)
