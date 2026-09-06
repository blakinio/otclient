from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .game_window_state_rebind import augment_rebind_output
    from .native_login_rebind_core import main as rebind_main
except ImportError:  # pragma: no cover - direct script execution
    from game_window_state_rebind import augment_rebind_output
    from native_login_rebind_core import main as rebind_main


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--client", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args, _ = parser.parse_known_args()
    result = rebind_main()
    if result != 0:
        return result
    augment_rebind_output(args.client, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
