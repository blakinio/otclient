#!/usr/bin/env python3
"""Stage-labeled read-only diagnostic for the approved Track A Kasm preflight."""
from __future__ import annotations

import fcntl
import importlib.util
import os
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Any, Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tibia_re_control_center.current_client_fence import current_client_fence  # noqa: E402

APPROVED_WORKER = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")
STATE_DIR = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
LOCK_PATH = STATE_DIR / "coordination.lock"
GUARD_ENV = "TRACK_A_ZERO_CLIENT_STAGE_DIAGNOSTIC_GUARDED"
SAFE_CODE_RE = re.compile(r"^[a-z0-9_]+(?::[A-Za-z0-9_.-]+){0,2}$")
SAFE_STAGE_RE = re.compile(r"^[a-z0-9_]+$")


class DiagnosticError(RuntimeError):
    pass


def _load_worker(path: Path = APPROVED_WORKER) -> ModuleType:
    try:
        if path.resolve(strict=True) != APPROVED_WORKER.resolve(strict=True):
            raise DiagnosticError("worker_not_approved")
    except OSError as exc:
        raise DiagnosticError("worker_unavailable") from exc
    spec = importlib.util.spec_from_file_location("track_a_zero_client_stage_worker", path)
    if spec is None or spec.loader is None:
        raise DiagnosticError("worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise DiagnosticError("worker_import_failed") from exc
    required_callables = (
        "run",
        "docker_containers",
        "_target",
        "package_identity",
        "boot_identity",
        "candidate_rows",
        "_window_count",
    )
    if any(not callable(getattr(module, name, None)) for name in required_callables):
        raise DiagnosticError("worker_contract_invalid")
    if not isinstance(getattr(module, "WorkerError", None), type):
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


def _sanitize_code(value: object) -> str:
    code = str(value)
    if not SAFE_CODE_RE.fullmatch(code):
        raise DiagnosticError("worker_error_code_invalid")
    return code


def _sanitize_stage(value: str) -> str:
    if not SAFE_STAGE_RE.fullmatch(value):
        raise DiagnosticError("stage_label_invalid")
    return value


def _failure(stage: str, value: object) -> dict[str, str]:
    return {"stage": _sanitize_stage(stage), "code": _sanitize_code(value)}


def _run_stage(
    errors: list[dict[str, str]],
    stage: str,
    worker_error: type[BaseException],
    call: Callable[[], Any],
) -> Any | None:
    try:
        return call()
    except worker_error as exc:
        errors.append(_failure(stage, exc))
        return None


def _boot_stage(worker: ModuleType, container_id: str, errors: list[dict[str, str]]) -> str | None:
    underlying: list[BaseException] = []

    def capture(command: Sequence[str]) -> str:
        try:
            return worker.run(command)
        except worker.WorkerError as exc:
            underlying.append(exc)
            raise

    try:
        return worker.boot_identity(container_id, capture)
    except worker.WorkerError as exc:
        errors.append(_failure("boot_identity", underlying[0] if underlying else exc))
        return None


def diagnose(worker: ModuleType) -> tuple[list[dict[str, str]], dict[str, int]]:
    errors: list[dict[str, str]] = []
    metadata = {
        "running_container_count": 0,
        "non_target_container_count": 0,
        "exact_candidate_count": 0,
        "main_window_count": 0,
    }

    containers = _run_stage(
        errors,
        "docker_inventory",
        worker.WorkerError,
        lambda: worker.docker_containers(),
    )
    if containers is None:
        return errors, metadata
    if not isinstance(containers, list):
        raise DiagnosticError("docker_inventory_contract_invalid")
    metadata["running_container_count"] = len(containers)

    target = _run_stage(
        errors,
        "target_resolution",
        worker.WorkerError,
        lambda: worker._target(containers),
    )
    if target is None:
        return errors, metadata
    if not isinstance(target, str):
        raise DiagnosticError("target_resolution_contract_invalid")

    _run_stage(
        errors,
        "display",
        worker.WorkerError,
        lambda: worker.run([
            "docker", "exec", "-u", worker.TARGET_USER,
            "-e", f"DISPLAY={worker.TARGET_DISPLAY}",
            target, "xdpyinfo",
        ]),
    )

    _run_stage(
        errors,
        "package_identity",
        worker.WorkerError,
        lambda: worker.package_identity(target),
    )

    _boot_stage(worker, target, errors)

    exact_candidates: list[dict[str, Any]] = []
    non_target_ordinal = 0
    for container_id, _name in containers:
        if container_id == target:
            stage = "candidate_inventory_target"
        else:
            stage = f"candidate_inventory_non_target_{non_target_ordinal}"
            non_target_ordinal += 1
        rows = _run_stage(
            errors,
            stage,
            worker.WorkerError,
            lambda cid=container_id: worker.candidate_rows(cid),
        )
        if rows is not None:
            if not isinstance(rows, list):
                raise DiagnosticError("candidate_inventory_contract_invalid")
            exact_candidates.extend(rows)
    metadata["non_target_container_count"] = non_target_ordinal
    metadata["exact_candidate_count"] = len(exact_candidates)
    if exact_candidates:
        errors.append(_failure(
            "candidate_aggregate",
            f"official_client_candidate_count:{len(exact_candidates)}",
        ))

    windows = _run_stage(
        errors,
        "window_inventory",
        worker.WorkerError,
        lambda: worker._window_count(target),
    )
    if windows is not None:
        if not isinstance(windows, int) or windows < 0:
            raise DiagnosticError("window_inventory_contract_invalid")
        metadata["main_window_count"] = windows
        if windows:
            errors.append(_failure("window_aggregate", f"main_window_count:{windows}"))

    return errors, metadata


def _print_result(errors: list[dict[str, str]], metadata: dict[str, int]) -> int:
    print(f"RUNNING_CONTAINER_COUNT={metadata['running_container_count']}")
    print(f"NON_TARGET_CONTAINER_COUNT={metadata['non_target_container_count']}")
    print(f"EXACT_CANDIDATE_COUNT={metadata['exact_candidate_count']}")
    print(f"MAIN_WINDOW_COUNT={metadata['main_window_count']}")
    print("CREDENTIAL_ACCESS=false")
    print("RUNTIME_MUTATION=false")
    if not errors:
        print("TRACK_A_KASM_ZERO_CLIENT_STAGE_DIAGNOSTIC=PASS")
        return 0
    for item in errors:
        print(
            f"TRACK_A_KASM_ZERO_CLIENT_STAGE_DIAGNOSTIC_ERROR={item['stage']}:{item['code']}",
            file=sys.stderr,
        )
    return 2


def main(argv: Sequence[str] | None = None) -> int:
    if argv not in (None, [], ()):
        print("TRACK_A_KASM_ZERO_CLIENT_STAGE_DIAGNOSTIC_FATAL=usage", file=sys.stderr)
        return 64
    try:
        _require_external_guard()
        worker = _load_worker()
        errors, metadata = diagnose(worker)
        return _print_result(errors, metadata)
    except (DiagnosticError, OSError, ValueError) as exc:
        code = _sanitize_code(exc.args[0] if exc.args else "diagnostic_failure")
        print(f"TRACK_A_KASM_ZERO_CLIENT_STAGE_DIAGNOSTIC_FATAL={code}", file=sys.stderr)
        print("CREDENTIAL_ACCESS=false")
        print("RUNTIME_MUTATION=false")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
