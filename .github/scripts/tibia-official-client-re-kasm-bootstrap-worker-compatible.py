#!/usr/bin/env python3
"""Compatibility entrypoint for Kasm bootstrap with daemon-side candidate prefilter."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tibia_re_control_center.docker_official_candidate_prefilter import (  # noqa: E402
    ProcessCensusError,
    container_requires_deep_scan,
)

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_kasm_bootstrap_worker_compat_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("bootstrap_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
_original_candidate_rows = _base.candidate_rows


def candidate_rows(
    container_id: str,
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> list[dict[str, Any]]:
    try:
        required = container_requires_deep_scan(container_id, runner)
    except ProcessCensusError as exc:
        raise _base.WorkerError(str(exc)) from exc
    if not required:
        return []
    return _original_candidate_rows(container_id, runner)


# exact_candidates resolves candidate_rows from the base module globals at call
# time, so one bounded substitution preserves every existing deep proof and all
# launch/rollback behavior while changing only harmless-container discovery.
_base.candidate_rows = candidate_rows

# Export the contract consumed by the same-boot invalidator.
WorkerError = _base.WorkerError
VER = _base.VER
SIZE = _base.SIZE
SHA = _base.SHA
collect_preflight = _base.collect_preflight
process_identity = _base.process_identity


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
