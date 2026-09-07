#!/usr/bin/env python3
"""Same-boot zero-client invalidation using the canonical-Kasm scoped worker."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType
from typing import Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-same-boot-zero-client-invalidate.py")
SCOPED_WORKER = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker-compatible.py")


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_same_boot_invalidator_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("same_boot_invalidator_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
# Preserve every registration/lease/boot/identity/tombstone rule from the
# reviewed invalidator. Rebind only the approved worker path so its zero-client
# proof is scoped to otclient-track-a-kasmvnc.
_base.APPROVED_WORKER = SCOPED_WORKER


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
