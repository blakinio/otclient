#!/usr/bin/env python3
"""Fail-closed metadata reconciliation for one approved canonical client-fence advance."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Sequence

STATE = Path('/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime')
REG = STATE / 'runtime-registration.json'
LEASE = STATE / 'lease.json'
LOCK = STATE / 'coordination.lock'
RID = 'track-a-canonical-live'
SOURCE_FENCE = (
    '15.32',
    52109920,
    'ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8',
)
CURRENT_FENCE = (
    '15.32.75d4a0',
    52105824,
    'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a',
)
ADOPTION_PROOF = 'existing_runtime_adoption_v1'
FAIL_CLOSED_EVIDENCE = {
    'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN',
    'NO_STRUCTURAL_BRIDGE',
}
TRANSITION_PATH = Path(__file__).with_name(
    'tibia-official-client-re-canonical-live-transition.py'
)
APPROVED_PROBE = Path(__file__).with_name(
    'tibia-official-client-re-kasm-existing-runtime-probe.py'
)


class ReconcileError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _transition() -> Any:
    spec = importlib.util.spec_from_file_location(
        'track_a_client_fence_reconcile_transition', TRANSITION_PATH
    )
    if spec is None or spec.loader is None:
        raise ReconcileError('current_transition_unavailable')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if (module.VER, module.SIZE, module.SHA) != CURRENT_FENCE:
        raise ReconcileError('current_transition_fence_mismatch')
    return module


def _is_private_regular(path: Path) -> bool:
    try:
        st = path.lstat()
    except OSError:
        return False
    owner = not hasattr(os, 'getuid') or st.st_uid == os.getuid()
    return bool(
        stat.S_ISREG(st.st_mode)
        and not path.is_symlink()
        and stat.S_IMODE(st.st_mode) == 0o600
        and owner
    )


def _hex64(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(c in '0123456789abcdef' for c in value.lower())
    )


def _fingerprint(document: dict[str, Any]) -> str:
    payload = (
        f"{document['runtime_locator']}:{document['pid']}:"
        f"{document['process_start_ticks']}:{document['client_size']}:"
        f"{document['client_sha256']}"
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _namespace(locator: Any) -> str:
    if not isinstance(locator, str):
        raise ReconcileError('runtime_namespace_invalid')
    parts = locator.split(':', 2)
    if len(parts) != 3 or parts[0] != 'docker' or not parts[1] or not parts[2]:
        raise ReconcileError('runtime_namespace_invalid')
    return parts[1]


def _load_json(path: Path, unsafe_code: str, invalid_code: str) -> dict[str, Any]:
    if not _is_private_regular(path):
        raise ReconcileError(unsafe_code)
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReconcileError(invalid_code) from exc
    if not isinstance(data, dict):
        raise ReconcileError(invalid_code)
    return data


def _base_registration(data: dict[str, Any]) -> None:
    required = {
        'schema_version', 'runtime_id', 'registration_generation', 'lease_generation',
        'registered_at', 'boot_id_sha256', 'pid', 'process_start_ticks',
        'client_version', 'client_size', 'client_sha256', 'display',
        'window_identity', 'remote_view_endpoint', 'remote_view_mapping', 'state',
        'source_task', 'source_run', 'proof_kind', 'runtime_locator',
        'inventory_scope', 'inventory_complete', 'candidate_count',
        'candidate_fingerprint', 'state_evidence',
    }
    if not required.issubset(data):
        raise ReconcileError('source_registration_schema_invalid')
    if data.get('schema_version') != 1 or data.get('runtime_id') != RID:
        raise ReconcileError('source_registration_schema_invalid')
    for field in ('registration_generation', 'lease_generation', 'pid', 'process_start_ticks'):
        if not isinstance(data.get(field), int) or int(data[field]) < 1:
            raise ReconcileError('source_registration_schema_invalid')
    if not _hex64(data.get('boot_id_sha256')):
        raise ReconcileError('source_registration_schema_invalid')
    if data.get('proof_kind') != ADOPTION_PROOF:
        raise ReconcileError('source_registration_not_adoption')
    if data.get('state') != 'UNKNOWN' or data.get('state_evidence') not in FAIL_CLOSED_EVIDENCE:
        raise ReconcileError('source_registration_not_fail_closed')
    if data.get('inventory_scope') != 'all_running_docker_containers':
        raise ReconcileError('source_registration_inventory_invalid')
    if data.get('inventory_complete') is not True or data.get('candidate_count') != 1:
        raise ReconcileError('source_registration_inventory_invalid')
    if not isinstance(data.get('display'), str) or not str(data['display']).startswith(':'):
        raise ReconcileError('source_registration_display_invalid')
    if data.get('remote_view_mapping') != 'PROVEN':
        raise ReconcileError('source_registration_remote_mapping_invalid')
    _namespace(data.get('runtime_locator'))
    expected_window_pid = f":pid:{data['pid']}:class:client/Tibia:"
    if expected_window_pid not in str(data.get('window_identity', '')):
        raise ReconcileError('source_registration_window_pid_mismatch')
    if not _hex64(data.get('candidate_fingerprint')):
        raise ReconcileError('source_registration_fingerprint_invalid')
    if data.get('candidate_fingerprint') != _fingerprint(data):
        raise ReconcileError('source_registration_fingerprint_invalid')


def _read_source() -> dict[str, Any]:
    data = _load_json(REG, 'source_registration_file_unsafe', 'source_registration_invalid_json')
    _base_registration(data)
    fence = (data.get('client_version'), data.get('client_size'), data.get('client_sha256'))
    if fence != SOURCE_FENCE:
        raise ReconcileError('source_fence_not_approved')
    return data


def _read_current() -> dict[str, Any]:
    data = _load_json(REG, 'current_registration_file_unsafe', 'current_registration_invalid_json')
    _base_registration(data)
    fence = (data.get('client_version'), data.get('client_size'), data.get('client_sha256'))
    if fence != CURRENT_FENCE:
        raise ReconcileError('current_fence_not_exact')
    return data


def _lease_generation(args: argparse.Namespace) -> int:
    data = _load_json(LEASE, 'lease_file_unsafe', 'lease_invalid_json')
    if (
        data.get('schema_version') != 1
        or data.get('runtime_id') != RID
        or data.get('status') != 'active'
        or data.get('controller_task') != args.task_id
        or data.get('controller_session') != args.session_id
        or not isinstance(data.get('generation'), int)
        or int(data['generation']) < 1
    ):
        raise ReconcileError('lease_identity_invalid')
    return int(data['generation'])


def _require_external_guard() -> None:
    if os.environ.get('TRACK_A_CANONICAL_FENCE_RECONCILE_GUARDED') != '1':
        raise ReconcileError('canonical_guard_required')
    try:
        fd = os.open(LOCK, os.O_RDONLY | os.O_CLOEXEC)
    except OSError as exc:
        raise ReconcileError('canonical_guard_required') from exc
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
    raise ReconcileError('canonical_guard_required')


def _clean_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        upper = key.upper()
        if (
            'CAPABILITY' in upper
            or 'LEASE_TOKEN' in upper
            or upper.startswith('TIBIA_TEST_')
            or key == 'TRACK_A_CANONICAL_WORKER_CONTRACT_TEST'
        ):
            env.pop(key, None)
    return env


def _probe(probe: Path) -> dict[str, Any]:
    if probe.resolve() != APPROVED_PROBE.resolve():
        raise ReconcileError('probe_not_approved')
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, raw = tempfile.mkstemp(prefix='.client-fence-probe.', dir=STATE)
    os.close(fd)
    path = Path(raw)
    path.unlink(missing_ok=True)
    try:
        completed = subprocess.run(
            [sys.executable, str(probe), 'probe', str(path)],
            env=_clean_env(),
            close_fds=True,
            check=False,
        )
        if completed.returncode != 0:
            raise ReconcileError('current_probe_failed')
        return _transition()._manifest(path)
    finally:
        path.unlink(missing_ok=True)


def _validate_fresh(old: dict[str, Any], fresh: dict[str, Any]) -> None:
    fence = (fresh.get('client_version'), fresh.get('client_size'), fresh.get('client_sha256'))
    if fence != CURRENT_FENCE:
        raise ReconcileError('current_probe_fence_invalid')
    if fresh.get('proof_kind') != ADOPTION_PROOF:
        raise ReconcileError('current_probe_not_adoption')
    if fresh.get('state') != 'UNKNOWN' or fresh.get('state_evidence') not in FAIL_CLOSED_EVIDENCE:
        raise ReconcileError('current_probe_not_fail_closed')
    if fresh.get('inventory_scope') != 'all_running_docker_containers':
        raise ReconcileError('current_probe_inventory_invalid')
    if fresh.get('inventory_complete') is not True or fresh.get('candidate_count') != 1:
        raise ReconcileError('current_probe_inventory_invalid')
    if not isinstance(fresh.get('pid'), int) or int(fresh['pid']) < 2:
        raise ReconcileError('current_probe_identity_invalid')
    if not isinstance(fresh.get('process_start_ticks'), int) or int(fresh['process_start_ticks']) < 1:
        raise ReconcileError('current_probe_identity_invalid')
    if not _hex64(fresh.get('boot_id_sha256')):
        raise ReconcileError('current_probe_identity_invalid')
    if _namespace(fresh.get('runtime_locator')) != _namespace(old.get('runtime_locator')):
        raise ReconcileError('runtime_namespace_changed')
    if fresh.get('display') != old.get('display'):
        raise ReconcileError('display_changed')
    if fresh.get('remote_view_endpoint') != old.get('remote_view_endpoint'):
        raise ReconcileError('remote_view_endpoint_changed')
    if fresh.get('remote_view_mapping') != old.get('remote_view_mapping'):
        raise ReconcileError('remote_view_mapping_changed')
    expected_window_pid = f":pid:{fresh['pid']}:class:client/Tibia:"
    if expected_window_pid not in str(fresh.get('window_identity', '')):
        raise ReconcileError('current_probe_window_pid_mismatch')
    if not _hex64(fresh.get('candidate_fingerprint')):
        raise ReconcileError('current_probe_fingerprint_invalid')
    if fresh.get('candidate_fingerprint') != _fingerprint(fresh):
        raise ReconcileError('current_probe_fingerprint_invalid')


def _signature(document: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(
        document.get(key)
        for key in (
            'proof_kind', 'boot_id_sha256', 'pid', 'process_start_ticks',
            'client_version', 'client_size', 'client_sha256', 'display',
            'window_identity', 'remote_view_endpoint', 'remote_view_mapping',
            'state', 'state_evidence', 'runtime_locator', 'inventory_scope',
            'inventory_complete', 'candidate_count', 'candidate_fingerprint',
        )
    )


def _candidate(old: dict[str, Any], fresh: dict[str, Any], generation: int, args: argparse.Namespace) -> dict[str, Any]:
    return {
        'schema_version': 1,
        'runtime_id': RID,
        'registration_generation': int(old['registration_generation']) + 1,
        'lease_generation': generation,
        'registered_at': int(time.time()),
        'boot_id_sha256': fresh['boot_id_sha256'],
        'pid': fresh['pid'],
        'process_start_ticks': fresh['process_start_ticks'],
        'client_version': CURRENT_FENCE[0],
        'client_size': CURRENT_FENCE[1],
        'client_sha256': CURRENT_FENCE[2],
        'display': fresh['display'],
        'window_identity': fresh['window_identity'],
        'remote_view_endpoint': fresh['remote_view_endpoint'],
        'remote_view_mapping': fresh['remote_view_mapping'],
        'state': 'UNKNOWN',
        'source_task': args.task_id,
        'source_run': os.environ.get('GITHUB_RUN_ID') or 'manual-unknown',
        'proof_kind': ADOPTION_PROOF,
        'runtime_locator': fresh['runtime_locator'],
        'inventory_scope': fresh['inventory_scope'],
        'inventory_complete': True,
        'candidate_count': 1,
        'candidate_fingerprint': fresh['candidate_fingerprint'],
        'state_evidence': fresh['state_evidence'],
    }


def _atomic_write(data: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(STATE, 0o700)
    fd, raw = tempfile.mkstemp(prefix='.runtime-registration.', dir=STATE)
    path = Path(raw)
    try:
        os.fchmod(fd, 0o600)
        payload = json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n'
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(path, REG)
        os.chmod(REG, 0o600)
        dir_fd = os.open(STATE, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        path.unlink(missing_ok=True)
        raise
    finally:
        path.unlink(missing_ok=True)


def _rollback(old: dict[str, Any], committed: dict[str, Any]) -> None:
    try:
        current = _read_current()
    except ReconcileError as exc:
        raise ReconcileError('rollback_current_registration_unverifiable') from exc
    if current != committed:
        raise ReconcileError('rollback_registration_conflict')
    _atomic_write(old)
    if _read_source() != old:
        raise ReconcileError('rollback_verification_failed')


def reconcile(args: argparse.Namespace) -> None:
    _require_external_guard()
    old = _read_source()
    generation = _lease_generation(args)
    if generation <= int(old['lease_generation']):
        raise ReconcileError('controller_generation_not_newer')

    first = _probe(args.probe)
    _validate_fresh(old, first)
    signature = _signature(first)
    committed = _candidate(old, first, generation, args)

    second = _probe(args.probe)
    _validate_fresh(old, second)
    if _signature(second) != signature:
        raise ReconcileError('fresh_identity_changed_before_commit')
    if _read_source() != old:
        raise ReconcileError('source_registration_changed_before_commit')
    if _lease_generation(args) != generation:
        raise ReconcileError('controller_generation_changed_before_commit')

    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_RUNTIME_ACCESS=canonical_recovery')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_RECOVERY_MODE=client_fence_reconciliation_v1')
    print(f'TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION={generation}')
    print(f"TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION={old['lease_generation']}")
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_TARGET_UNIQUENESS=PROVEN')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_MUTATION_AUTHORIZED=false')

    _atomic_write(committed)
    try:
        if _read_current() != committed:
            raise ReconcileError('committed_registration_mismatch')
        third = _probe(args.probe)
        _validate_fresh(old, third)
        if _signature(third) != signature:
            raise ReconcileError('fresh_identity_changed_after_commit')
        if _read_current() != committed:
            raise ReconcileError('committed_registration_changed_after_commit')
        if _lease_generation(args) != generation:
            raise ReconcileError('controller_generation_changed_after_commit')
    except BaseException:
        _rollback(old, committed)
        raise

    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION=PASS')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_STATE=UNKNOWN')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CLIENT_PROCESS_MUTATION=false')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PROCESS_MEMORY_OBSERVATION=false')
    print('TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_SEMANTIC_PROMOTION=false')


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--session-id', required=True)
    parser.add_argument('--probe', required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        reconcile(args)
        return 0
    except ReconcileError as exc:
        print(
            f'TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_ERROR={exc.code}',
            file=sys.stderr,
        )
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
