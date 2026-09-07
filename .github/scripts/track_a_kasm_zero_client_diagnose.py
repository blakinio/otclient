#!/usr/bin/env python3
"""Read-only diagnostic for the approved Track A Kasm zero-client preflight."""
from __future__ import annotations

import fcntl
import importlib.util
import os
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tibia_re_control_center.current_client_fence import current_client_fence  # noqa: E402

APPROVED_WORKER = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")
STATE_DIR = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
LOCK_PATH = STATE_DIR / "coordination.lock"
GUARD_ENV = "TRACK_A_ZERO_CLIENT_DIAGNOSTIC_GUARDED"
SAFE_CODE_RE = re.compile(r"^[a-z0-9_]+(?::[A-Za-z0-9_.-]+){0,2}$")


class DiagnosticError(RuntimeError):
    pass


def _load_worker(path: Path = APPROVED_WORKER) -> ModuleType:
    try:
        if path.resolve(strict=True) != APPROVED_WORKER.resolve(strict=True):
            raise DiagnosticError("worker_not_approved")
    except OSError as exc:
        raise DiagnosticError("worker_unavailable") from exc
    spec = importlib.util.spec_from_file_location("track_a_zero_client_diagnostic_worker", path)
    if spec is None or spec.loader is None:
        raise DiagnosticError("worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise DiagnosticError("worker_import_failed") from exc
    if not callable(getattr(module, "collect_preflight", None)) or not isinstance(
        getattr(module, "WorkerError", None), type
    ):
        raise DiagnosticError("worker_contract_invalid")
    current = current_client_fence().as_tuple()
    if (getattr(module, "VER", None), getattr(module, "SIZE", None), getattr(module, "SHA", None)) != current:
        raise DiagnosticError("worker_current_fence_mismatch")
    return module


def _require_external_guard() -> None:
    if os.environ.get(GUARD_ENV) != "1":
        raise DiagnosticError("canonical_guard_required")
    try:
        fd = os.open(LOCK_PATH, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
    except OSError as exc:
        raise DiagnosticError("canonical_guard_required") from exc
    acquired = False
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except BlockingIOError:
            return
    finally:
        if acquired:
            fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
    raise DiagnosticError("canonical_guard_required")


def _sanitize_worker_code(value: object) -> str:
    code = str(value)
    if not SAFE_CODE_RE.fullmatch(code):
        raise DiagnosticError("worker_error_code_invalid")
    return code


def diagnose(worker: ModuleType) -> tuple[bool, str]:
    try:
        preflight = worker.collect_preflight()
    except worker.WorkerError as exc:  # type: ignore[misc]
        return False, _sanitize_worker_code(exc)
    if not isinstance(preflight, dict):
        raise DiagnosticError("worker_preflight_invalid")
    required = {
        "candidate_count": 0,
        "main_window_count": 0,
        "client_size": current_client_fence().size,
        "client_sha256": current_client_fence().sha256,
    }
    if any(preflight.get(key) != expected for key, expected in required.items()):
        raise DiagnosticError("worker_preflight_invalid")
    return True, "preflight_pass"


def main(argv: Sequence[str] | None = None) -> int:
    if argv not in (None, [], ()):
        print("TRACK_A_KASM_ZERO_CLIENT_DIAGNOSTIC_ERROR=usage", file=sys.stderr)
        return 64
    try:
        _require_external_guard()
        worker = _load_worker()
        ok, code = diagnose(worker)
        if not ok:
            print(f"TRACK_A_KASM_ZERO_CLIENT_DIAGNOSTIC_ERROR={code}", file=sys.stderr)
            print("CREDENTIAL_ACCESS=false")
            print("RUNTIME_MUTATION=false")
            return 2
        print("TRACK_A_KASM_ZERO_CLIENT_DIAGNOSTIC=PASS")
        print("CANDIDATE_COUNT=0")
        print("MAIN_WINDOW_COUNT=0")
        print("CREDENTIAL_ACCESS=false")
        print("RUNTIME_MUTATION=false")
        return 0
    except (DiagnosticError, OSError, ValueError) as exc:
        code = _sanitize_worker_code(exc.args[0] if exc.args else "diagnostic_failure")
        print(f"TRACK_A_KASM_ZERO_CLIENT_DIAGNOSTIC_ERROR={code}", file=sys.stderr)
        print("CREDENTIAL_ACCESS=false")
        print("RUNTIME_MUTATION=false")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
