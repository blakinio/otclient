#!/usr/bin/env python3
"""Kasm adoption probe scoped to the canonical Track A container."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import time
from types import ModuleType
from typing import Any, Callable, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-existing-runtime-probe.py")
RETRYABLE_READINESS = {
    "official_client_candidate_count:0",
    "main_window_count:0",
    "window_pid_missing",
    "window_pid_mismatch",
}
SAFE_ERROR_RE = re.compile(r"^[A-Za-z0-9_:-]{1,120}$")


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_kasm_existing_probe_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("existing_probe_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
_original_candidate_rows = _base.candidate_rows


def collect(runner: Callable[[Sequence[str]], str] = _base.run) -> dict[str, Any]:
    containers = _base.docker_containers(runner)
    target = [(container_id, name) for container_id, name in containers if name == _base.TARGET_CONTAINER]
    if len(target) != 1:
        raise _base.ProbeError(f"target_container_count:{len(target)}")
    target_id = target[0][0]
    original = _base.candidate_rows

    def scoped_candidate_rows(container_id: str, inner_runner: Callable[[Sequence[str]], str] = runner):
        if container_id != target_id:
            return []
        return _original_candidate_rows(container_id, inner_runner)

    _base.candidate_rows = scoped_candidate_rows
    try:
        payload = _base.collect(runner)
    finally:
        _base.candidate_rows = original
    payload["inventory_scope"] = "canonical_kasm_container"
    payload["inventory_complete"] = True
    return payload


def _safe_error(exc: BaseException) -> str:
    code = str(exc)
    return code if SAFE_ERROR_RE.fullmatch(code) else type(exc).__name__


def collect_when_ready(
    runner: Callable[[Sequence[str]], str] = _base.run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 48,
) -> dict[str, Any]:
    """Retry only transient process/window readiness states; fail hard errors immediately."""
    last: _base.ProbeError | None = None
    for index in range(max(1, attempts)):
        try:
            return collect(runner)
        except _base.ProbeError as exc:
            code = _safe_error(exc)
            if code not in RETRYABLE_READINESS or index + 1 >= max(1, attempts):
                raise
            last = exc
            sleeper(0.25)
    assert last is not None
    raise last


ProbeError = _base.ProbeError
VER = _base.VER
SIZE = _base.SIZE
SHA = _base.SHA
PROOF_KIND = _base.PROOF_KIND


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 2 or argv[0] != "probe":
        print("TRACK_A_KASM_EXISTING_RUNTIME_PROBE_ERROR=usage", file=sys.stderr)
        return 2
    output = Path(argv[1])
    try:
        payload = collect_when_ready()
        output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        output.chmod(0o600)
        print("TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS")
        return 0
    except ProbeError as exc:
        print(f"TRACK_A_KASM_EXISTING_RUNTIME_PROBE_ERROR={_safe_error(exc)}", file=sys.stderr)
        return 2
    except OSError:
        print("TRACK_A_KASM_EXISTING_RUNTIME_PROBE_ERROR=OSError", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
