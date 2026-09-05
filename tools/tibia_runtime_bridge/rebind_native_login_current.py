from __future__ import annotations

try:
    from .native_login_rebind_core import main
except ImportError:  # pragma: no cover - direct script execution
    from native_login_rebind_core import main


if __name__ == "__main__":
    raise SystemExit(main())
