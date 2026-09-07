#!/usr/bin/env python3
"""Kasm bootstrap entrypoint scoped to the canonical Track A container."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Callable, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_kasm_bootstrap_worker_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("bootstrap_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
_original_candidate_rows = _base.candidate_rows


def exact_candidates(
    containers: list[tuple[str, str]],
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> list[dict[str, Any]]:
    """Deep-scan only the one canonical Kasm container.

    Track A runtime uniqueness is intentionally scoped to
    ``otclient-track-a-kasmvnc``. Other Synology containers are outside this
    runtime namespace and are not queried or executed inside.
    """
    target = [(container_id, name) for container_id, name in containers if name == _base.TARGET_CONTAINER]
    if len(target) != 1:
        raise _base.WorkerError(f"target_container_count:{len(target)}")
    return _original_candidate_rows(target[0][0], runner)


_base.exact_candidates = exact_candidates

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
