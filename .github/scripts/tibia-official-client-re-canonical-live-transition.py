#!/usr/bin/env python3
"""Cancellation-safe Track A canonical bootstrap, rebind and Gate B."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Sequence

STATE = Path('/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime')
REG = STATE / 'runtime-registration.json'
GUARD_PATH = Path(__file__).with_name('tibia-official-client-re-canonical-live-guard.py')
INPUT_LOCK_PATH = Path(__file__).with_name('tibia-official-client-re-input-lock.py')
RID = 'track-a-canonical-live'
VER = '15.32'
SIZE = 52109920
SHA = 'ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8'
STATES = {'LOGIN', 'CHARACTER_SELECT', 'IN_GAME', 'DISCONNECTED', 'UNKNOWN'}
FIELDS = {
    'schema_version', 'runtime_id', 'registration_generation', 'lease_generation',
    'registered_at', 'boot_id_sha256', 'pid', 'process_start_ticks',
    'client_version', 'client_size', 'client_sha256', 'display',
    'window_identity', 'remote_view_endpoint', 'remote_view_mapping', 'state',
    'source_task', 'source_run',
}
TRACKED_ROLES = {'client', 'xvfb', 'vnc', 'wireproxy'}
ADOPTION_PROOF_KIND = 'existing_runtime_adoption_v1'
ADOPTION_STATE_EVIDENCE = {'BRIDGE_3_OF_3', 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN', 'NO_STRUCTURAL_BRIDGE'}


class E(RuntimeError):
    def __init__(self, code: str, msg: str = '') -> None:
        super().__init__(msg or code)
        self.code = code


def _guard() -> Any:
    spec = importlib.util.spec_from_file_location('track_a_bootstrap_guard', GUARD_PATH)
    if spec is None or spec.loader is None:
        raise E('guard_unavailable')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _input_lock_module() -> Any:
    spec = importlib.util.spec_from_file_location('track_a_input_lock', INPUT_LOCK_PATH)
    if spec is None or spec.loader is None:
        raise E('input_lock_unavailable')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except OSError as exc:
        raise E('input_lock_unavailable', str(exc)) from exc
    return module


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb', buffering=0) as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def _boot() -> str:
    boot_id = Path('/proc/sys/kernel/random/boot_id').read_text().strip().encode()
    return hashlib.sha256(boot_id).hexdigest()


def _proc_snapshot(pid: int) -> tuple[str, int, int] | None:
    """Return process state, pgrp and uid, or None if the process vanished."""
    try:
        raw_stat = Path(f'/proc/{pid}/stat').read_text()
        close = raw_stat.rfind(')')
        fields = raw_stat[close + 2:].split()
        if close < 0 or len(fields) < 3:
            raise E('proc_stat_invalid')
        state = fields[0]
        pgrp = int(fields[2])
        uid_line = next(
            line for line in Path(f'/proc/{pid}/status').read_text().splitlines()
            if line.startswith('Uid:')
        )
        uid = int(uid_line.split()[1])
        return state, pgrp, uid
    except FileNotFoundError:
        return None
    except (OSError, StopIteration, ValueError) as exc:
        raise E('process_inventory_incomplete', str(exc)) from exc


def _start(pid: int) -> int:
    snapshot = _proc_snapshot(pid)
    if snapshot is None:
        raise E('proc_stat_missing')
    raw = Path(f'/proc/{pid}/stat').read_text()
    close = raw.rfind(')')
    fields = raw[close + 2:].split()
    if close < 0 or len(fields) < 20:
        raise E('proc_stat_invalid')
    return int(fields[19])


def _exe(pid: int) -> Path:
    try:
        return Path(os.readlink(f'/proc/{pid}/exe'))
    except OSError as exc:
        raise E('client_exe_unreadable', str(exc)) from exc


def _cmdline(pid: int) -> str:
    try:
        return Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0', b' ').decode(
            'utf-8', errors='replace'
        )
    except FileNotFoundError:
        return ''
    except OSError as exc:
        raise E('process_inventory_incomplete', str(exc)) from exc


def _ident(pid: int) -> dict[str, Any]:
    path = _exe(pid)
    stat_result = path.stat()
    return {
        'boot_id_sha256': _boot(),
        'pid': pid,
        'process_start_ticks': _start(pid),
        'client_size': stat_result.st_size,
        'client_sha256': _sha(path),
    }


def _exact(identity: dict[str, Any]) -> None:
    if identity['client_size'] != SIZE:
        raise E('client_size_mismatch')
    if identity['client_sha256'] != SHA:
        raise E('client_sha256_mismatch')


def _looks_official(text: str) -> bool:
    return 'CipSoft GmbH/Tibia/packages/Tibia' in text or '/Tibia/packages/Tibia/' in text


def _candidates() -> list[int]:
    """Fail closed if local process inventory cannot exclude an official client."""
    found: list[int] = []
    current_uid = os.getuid() if hasattr(os, 'getuid') else None
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        snapshot = _proc_snapshot(pid)
        if snapshot is None or snapshot[0] == 'Z':
            continue
        _, _, uid = snapshot
        cmdline = _cmdline(pid)
        hinted = _looks_official(cmdline)
        try:
            path = _exe(pid)
            stat_result = path.stat()
        except E as exc:
            if hinted or current_uid is None or uid == current_uid:
                raise E('process_inventory_incomplete', str(exc)) from exc
            continue
        except OSError as exc:
            if hinted or current_uid is None or uid == current_uid:
                raise E('process_inventory_incomplete', str(exc)) from exc
            continue
        plausible = _looks_official(str(path)) or hinted
        if not plausible and stat_result.st_size != SIZE:
            continue
        try:
            digest = _sha(path)
        except OSError as exc:
            if plausible:
                raise E('official_client_candidate_unverifiable', str(exc)) from exc
            continue
        if plausible or (stat_result.st_size == SIZE and digest == SHA):
            found.append(pid)
    return sorted(set(found))


def _group_members(pgid: int) -> set[int]:
    members: set[int] = set()
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        snapshot = _proc_snapshot(pid)
        if snapshot is None or snapshot[0] == 'Z':
            continue
        if snapshot[1] == pgid:
            members.add(pid)
    return members


def _assert_group_tracked(manifest: dict[str, Any]) -> None:
    pgid = manifest.get('process_group_id')
    tracked = manifest.get('tracked_processes')
    if not isinstance(pgid, int) or pgid < 2:
        raise E('probe_process_group_invalid')
    if not isinstance(tracked, dict) or set(tracked) != TRACKED_ROLES:
        raise E('probe_tracked_processes_invalid')
    if not all(isinstance(pid, int) and pid >= 2 for pid in tracked.values()):
        raise E('probe_tracked_pid_invalid')
    if len(set(tracked.values())) != len(TRACKED_ROLES):
        raise E('probe_tracked_pid_not_unique')
    if tracked.get('client') != manifest.get('pid'):
        raise E('probe_client_not_tracked')
    actual = _group_members(pgid)
    expected = set(tracked.values())
    if actual != expected:
        raise E('bootstrap_process_group_untracked')


def _read() -> dict[str, Any] | None:
    if not REG.exists():
        return None
    st = REG.lstat()
    owner = not hasattr(os, 'getuid') or st.st_uid == os.getuid()
    if not REG.is_file() or REG.is_symlink() or (st.st_mode & 0o777) != 0o600 or not owner:
        raise E('registration_file_unsafe')
    try:
        data = json.loads(REG.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise E('registration_invalid_json', str(exc)) from exc
    if not isinstance(data, dict) or not FIELDS.issubset(data):
        raise E('registration_schema_invalid')
    if data.get('schema_version') != 1 or data.get('runtime_id') != RID:
        raise E('registration_schema_invalid')
    if (data.get('client_version'), data.get('client_size'), data.get('client_sha256')) != (VER, SIZE, SHA):
        raise E('registration_client_fence_invalid')
    if data.get('state') not in STATES or data.get('remote_view_mapping') not in {'PROVEN', 'UNKNOWN'}:
        raise E('registration_state_invalid')
    if not isinstance(data.get('registration_generation'), int) or data['registration_generation'] < 1:
        raise E('registration_generation_invalid')
    if not isinstance(data.get('lease_generation'), int) or data['lease_generation'] < 1:
        raise E('registration_lease_generation_invalid')
    if data.get('proof_kind') == ADOPTION_PROOF_KIND:
        required = {
            'runtime_locator', 'inventory_scope', 'inventory_complete', 'candidate_count',
            'candidate_fingerprint', 'state_evidence',
        }
        if not required.issubset(data):
            raise E('adoption_registration_schema_invalid')
        if data['inventory_scope'] != 'all_running_docker_containers' or data['inventory_complete'] is not True:
            raise E('adoption_registration_inventory_invalid')
        if data['candidate_count'] != 1:
            raise E('adoption_registration_candidate_count_invalid')
        if not isinstance(data['runtime_locator'], str) or not data['runtime_locator'].startswith('docker:'):
            raise E('adoption_registration_runtime_locator_invalid')
        fingerprint = data['candidate_fingerprint']
        if not isinstance(fingerprint, str) or len(fingerprint) != 64 or any(c not in '0123456789abcdef' for c in fingerprint.lower()):
            raise E('adoption_registration_candidate_fingerprint_invalid')
        if data['state_evidence'] not in ADOPTION_STATE_EVIDENCE:
            raise E('adoption_registration_state_evidence_invalid')
    return data


def _stage(data: dict[str, Any]) -> Path:
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix='.runtime-registration.', dir=STATE)
    path = Path(name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'wb') as handle:
            payload = json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n'
            handle.write(payload.encode())
            handle.flush()
            os.fsync(handle.fileno())
        return path
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        path.unlink(missing_ok=True)
        raise


def _commit(path: Path) -> None:
    os.replace(path, REG)
    fd = os.open(STATE, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write(data: dict[str, Any]) -> None:
    path = _stage(data)
    try:
        _commit(path)
    finally:
        path.unlink(missing_ok=True)


def _remove(expected: dict[str, Any]) -> None:
    if _read() != expected:
        raise E('registration_cleanup_mismatch')
    REG.unlink()
    fd = os.open(STATE, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    if REG.exists():
        raise E('registration_cleanup_failed')


def _manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise E('probe_manifest_invalid', str(exc)) from exc
    common = {
        'pid', 'display', 'window_identity', 'remote_view_endpoint',
        'remote_view_mapping', 'state',
    }
    if not isinstance(data, dict) or not common.issubset(data):
        raise E('probe_manifest_missing_fields')
    if not isinstance(data['pid'], int) or data['pid'] < 2:
        raise E('probe_pid_invalid')
    if not isinstance(data['display'], str) or not data['display'].startswith(':'):
        raise E('probe_display_invalid')
    if not isinstance(data['window_identity'], str) or not data['window_identity']:
        raise E('probe_window_invalid')
    if data['remote_view_mapping'] not in {'PROVEN', 'UNKNOWN'} or data['state'] not in STATES:
        raise E('probe_state_invalid')

    if data.get('proof_kind') == ADOPTION_PROOF_KIND:
        required = {
            'boot_id_sha256', 'process_start_ticks', 'client_version', 'client_size',
            'client_sha256', 'runtime_locator', 'inventory_scope', 'inventory_complete',
            'candidate_count', 'candidate_fingerprint', 'state_evidence',
        }
        if not required.issubset(data):
            raise E('adoption_manifest_missing_fields')
        if data['inventory_complete'] is not True or data['inventory_scope'] != 'all_running_docker_containers':
            raise E('adoption_inventory_incomplete')
        if data['candidate_count'] != 1:
            raise E('adoption_target_not_unique')
        if data['client_version'] != VER or data['client_size'] != SIZE or data['client_sha256'] != SHA:
            raise E('adoption_client_fence_invalid')
        if not isinstance(data['process_start_ticks'], int) or data['process_start_ticks'] < 1:
            raise E('adoption_start_ticks_invalid')
        for field in ('boot_id_sha256', 'candidate_fingerprint'):
            value = data[field]
            if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value.lower()):
                raise E(f'adoption_{field}_invalid')
        if not isinstance(data['runtime_locator'], str) or not data['runtime_locator'].startswith('docker:'):
            raise E('adoption_runtime_locator_invalid')
        if data['state_evidence'] not in ADOPTION_STATE_EVIDENCE:
            raise E('adoption_state_evidence_invalid')
        if data['state'] == 'IN_GAME':
            raise E('adoption_ingame_semantics_unproven')
        return data

    legacy = {'process_group_id', 'tracked_processes'}
    if not legacy.issubset(data):
        raise E('probe_manifest_missing_fields')
    return data


def _is_adoption_manifest(manifest: dict[str, Any]) -> bool:
    return manifest.get('proof_kind') == ADOPTION_PROOF_KIND


def _adoption_semantics_stale(registration: dict[str, Any]) -> bool:
    return bool(
        registration.get('proof_kind') == ADOPTION_PROOF_KIND
        and registration.get('state') == 'IN_GAME'
        and registration.get('state_evidence') == 'BRIDGE_3_OF_3'
    )


def _stable_adoption_identity(document: dict[str, Any]) -> tuple[Any, ...]:
    window = str(document.get('window_identity', ''))
    window_base = window.split(':title_sha256:', 1)[0]
    return tuple(document.get(key) for key in (
        'boot_id_sha256', 'pid', 'process_start_ticks', 'client_version', 'client_size',
        'client_sha256', 'display', 'runtime_locator', 'inventory_scope',
        'inventory_complete', 'candidate_count', 'candidate_fingerprint',
    )) + (window_base,)


def _adoption_signature(manifest: dict[str, Any]) -> tuple[Any, ...]:
    if not _is_adoption_manifest(manifest):
        raise E('adoption_manifest_required')
    return tuple(manifest[key] for key in (
        'boot_id_sha256', 'pid', 'process_start_ticks', 'client_version', 'client_size',
        'client_sha256', 'display', 'window_identity', 'remote_view_endpoint',
        'remote_view_mapping', 'state', 'state_evidence', 'runtime_locator', 'inventory_scope',
        'candidate_count', 'candidate_fingerprint',
    ))


def _match(manifest: dict[str, Any], registration: dict[str, Any]) -> None:
    for key in ('pid', 'display', 'window_identity', 'remote_view_endpoint', 'remote_view_mapping', 'state'):
        if manifest.get(key) != registration.get(key):
            raise E(f'probe_registration_{key}_mismatch')
    if _is_adoption_manifest(manifest):
        for key in (
            'boot_id_sha256', 'pid', 'process_start_ticks', 'client_version', 'client_size',
            'client_sha256', 'proof_kind', 'runtime_locator', 'inventory_scope',
            'inventory_complete', 'candidate_count', 'candidate_fingerprint', 'state_evidence',
        ):
            if manifest.get(key) != registration.get(key):
                raise E(f'registered_identity_{key}_mismatch')
        return
    identity = _ident(int(registration['pid']))
    _exact(identity)
    for key in ('boot_id_sha256', 'pid', 'process_start_ticks'):
        if identity[key] != registration.get(key):
            raise E(f'registered_identity_{key}_mismatch')

def _match_rebind_probe(manifest: dict[str, Any], registration: dict[str, Any]) -> None:
    evidence_refresh = bool(
        _is_adoption_manifest(manifest)
        and registration.get('proof_kind') == ADOPTION_PROOF_KIND
        and registration.get('state') == 'UNKNOWN'
        and manifest.get('state') == 'UNKNOWN'
        and registration.get('state_evidence') == 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN'
        and manifest.get('state_evidence') == 'NO_STRUCTURAL_BRIDGE'
    )
    if not evidence_refresh:
        _match(manifest, registration)
        return
    normalized = dict(manifest)
    normalized['state_evidence'] = registration['state_evidence']
    _match(normalized, registration)

def _env() -> dict[str, str]:
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


def _worker(worker: Path, operation: str, argument: str) -> None:
    completed = subprocess.run(
        [str(worker), operation, argument], env=_env(), close_fds=True, check=False
    )
    if completed.returncode:
        raise E(f'{operation}_worker_failed')


def _probe(worker: Path, path: Path) -> dict[str, Any]:
    path.unlink(missing_ok=True)
    _worker(worker, 'probe', str(path))
    return _manifest(path)


def _kill(pgid: int) -> None:
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return
    end = time.monotonic() + 4
    while time.monotonic() < end:
        try:
            os.killpg(pgid, 0)
        except ProcessLookupError:
            return
        try:
            while os.waitpid(-1, os.WNOHANG)[0] > 0:
                pass
        except ChildProcessError:
            pass
        time.sleep(0.1)
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return
    try:
        while os.waitpid(-1, os.WNOHANG)[0] > 0:
            pass
    except ChildProcessError:
        pass


def _lease(manager: Any, lease: Any, identity: Any, token: Path, generation: int | None = None) -> int:
    secret = lease._read_private_token(token)
    state = manager._load_state_unlocked()
    manager._require_current_unlocked(state, identity, secret, lease._now_epoch(None))
    if state is None:
        raise E('lease_absent')
    current = int(state['generation'])
    if generation is not None and current != generation:
        raise E('lease_generation_changed')
    return current


def _cancel(guard: Any) -> None:
    if guard._supervisor_cancel_signal is not None:
        raise E('supervisor_cancelled')


def _runid() -> str:
    return os.environ.get('GITHUB_RUN_ID') or 'manual-unknown'


def _probe_reg(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
    old: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    registration = _read()
    if registration is None:
        raise E('registration_absent')
    if _adoption_semantics_stale(registration):
        raise E('adoption_registration_semantics_stale')
    registered_generation = int(registration['lease_generation'])
    if old and registered_generation >= generation:
        raise E('rebind_generation_not_older')
    if not old and registered_generation != generation:
        raise E('registration_generation_mismatch')
    path = STATE / '.gate-b-manifest.json'
    try:
        manifest = _probe(args.probe, path)
        if _is_adoption_manifest(manifest):
            if old:
                _match_rebind_probe(manifest, registration)
            else:
                _match(manifest, registration)
        else:
            _assert_group_tracked(manifest)
            _match(manifest, registration)
            if _candidates() != [int(registration['pid'])]:
                raise E('registered_target_not_unique')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        return registration, manifest
    finally:
        path.unlink(missing_ok=True)


def _adopt_existing(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    if _read() is not None:
        raise E('registration_already_present')
    path = STATE / '.adopt-existing-manifest.json'
    staged: Path | None = None
    committed: dict[str, Any] | None = None
    try:
        STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
        first = _probe(args.probe, path)
        if not _is_adoption_manifest(first):
            raise E('adoption_manifest_required')
        signature = _adoption_signature(first)
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        if _read() is not None:
            raise E('adoption_registration_race')
        registration = {
            'schema_version': 1,
            'runtime_id': RID,
            'registration_generation': 1,
            'lease_generation': generation,
            'registered_at': int(time.time()),
            'boot_id_sha256': first['boot_id_sha256'],
            'pid': first['pid'],
            'process_start_ticks': first['process_start_ticks'],
            'client_version': VER,
            'client_size': SIZE,
            'client_sha256': SHA,
            'display': first['display'],
            'window_identity': first['window_identity'],
            'remote_view_endpoint': first['remote_view_endpoint'],
            'remote_view_mapping': first['remote_view_mapping'],
            'state': first['state'],
            'proof_kind': first['proof_kind'],
            'runtime_locator': first['runtime_locator'],
            'inventory_scope': first['inventory_scope'],
            'inventory_complete': first['inventory_complete'],
            'candidate_count': first['candidate_count'],
            'candidate_fingerprint': first['candidate_fingerprint'],
            'state_evidence': first['state_evidence'],
            'source_task': args.task_id,
            'source_run': _runid(),
        }
        staged = _stage(registration)
        second = _probe(args.probe, path)
        if _adoption_signature(second) != signature:
            raise E('adoption_identity_changed_before_commit')
        if _read() is not None:
            raise E('adoption_registration_race')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        try:
            _commit(staged)
        except BaseException:
            current = _read()
            if current == registration:
                committed = registration
            elif current is not None:
                raise E('adoption_registration_commit_conflict')
            raise
        else:
            staged = None
            committed = registration
        if _read() != registration:
            raise E('adoption_registration_revalidation_failed')
        third = _probe(args.probe, path)
        if _adoption_signature(third) != signature:
            raise E('adoption_identity_changed_after_commit')
        _match(third, registration)
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
    except BaseException as exc:
        if committed is not None:
            current = _read()
            if current == committed:
                _remove(committed)
            elif current is not None:
                raise E('adoption_rollback_registration_conflict') from exc
        raise
    finally:
        path.unlink(missing_ok=True)
        if staged is not None:
            staged.unlink(missing_ok=True)

def _semantic_downgrade(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    old = _read()
    if old is None:
        raise E('registration_absent')
    if not _adoption_semantics_stale(old):
        raise E('semantic_downgrade_not_required')
    path = STATE / '.semantic-downgrade-manifest.json'
    staged: Path | None = None
    committed = False
    try:
        first = _probe(args.probe, path)
        if not _is_adoption_manifest(first):
            raise E('semantic_downgrade_adoption_manifest_required')
        if first.get('state') != 'UNKNOWN' or first.get('state_evidence') != 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN':
            raise E('semantic_downgrade_probe_not_fail_closed')
        if _stable_adoption_identity(first) != _stable_adoption_identity(old):
            raise E('semantic_downgrade_identity_mismatch')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        new = dict(old)
        new.update(
            registration_generation=int(old['registration_generation']) + 1,
            lease_generation=generation,
            registered_at=int(time.time()),
            display=first['display'],
            window_identity=first['window_identity'],
            remote_view_endpoint=first['remote_view_endpoint'],
            remote_view_mapping=first['remote_view_mapping'],
            state='UNKNOWN',
            state_evidence='BRIDGE_3_OF_3_SEMANTICS_UNPROVEN',
            source_task=args.task_id,
            source_run=_runid(),
        )
        staged = _stage(new)
        second = _probe(args.probe, path)
        if _stable_adoption_identity(second) != _stable_adoption_identity(first):
            raise E('semantic_downgrade_identity_changed_before_commit')
        if second.get('state') != 'UNKNOWN' or second.get('state_evidence') != 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN':
            raise E('semantic_downgrade_state_changed_before_commit')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        committed = True
        _commit(staged)
        staged = None
        if _read() != new:
            raise E('semantic_downgrade_revalidation_failed')
        third = _probe(args.probe, path)
        _match(third, new)
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
    except BaseException as exc:
        if committed:
            try:
                _write(old)
            except BaseException as rollback_exc:
                raise E('semantic_downgrade_rollback_failed', str(rollback_exc)) from exc
            if _read() != old:
                raise E('semantic_downgrade_rollback_revalidation_failed') from exc
        raise
    finally:
        path.unlink(missing_ok=True)
        if staged is not None:
            staged.unlink(missing_ok=True)


def _bootstrap(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    if _read() is not None:
        raise E('registration_already_present')
    if _candidates():
        raise E('official_client_candidate_present')
    manifest_path = STATE / '.bootstrap-manifest.json'
    post_path = STATE / '.bootstrap-post-manifest.json'
    staged: Path | None = None
    child: subprocess.Popen[Any] | None = None
    committed: dict[str, Any] | None = None
    success = False
    try:
        STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
        manifest_path.unlink(missing_ok=True)
        post_path.unlink(missing_ok=True)
        child = subprocess.Popen(
            [str(args.worker), 'bootstrap', str(manifest_path)],
            env=_env(), close_fds=True, start_new_session=True,
        )
        if child.wait(timeout=args.worker_timeout):
            raise E('bootstrap_worker_failed')
        _cancel(guard)
        manifest = _manifest(manifest_path)
        if manifest.get('process_group_id') != child.pid:
            raise E('bootstrap_process_group_invalid')
        _assert_group_tracked(manifest)
        current_identity = _ident(int(manifest['pid']))
        _exact(current_identity)
        if _candidates() != [int(manifest['pid'])]:
            raise E('bootstrap_target_not_unique')
        _lease(manager, lease, identity, args.token_file, generation)
        registration = {
            'schema_version': 1,
            'runtime_id': RID,
            'registration_generation': 1,
            'lease_generation': generation,
            'registered_at': int(time.time()),
            'boot_id_sha256': current_identity['boot_id_sha256'],
            'pid': current_identity['pid'],
            'process_start_ticks': current_identity['process_start_ticks'],
            'client_version': VER,
            'client_size': SIZE,
            'client_sha256': SHA,
            'display': manifest['display'],
            'window_identity': manifest['window_identity'],
            'remote_view_endpoint': manifest['remote_view_endpoint'],
            'remote_view_mapping': manifest['remote_view_mapping'],
            'state': manifest['state'],
            'source_task': args.task_id,
            'source_run': _runid(),
        }
        staged = _stage(registration)
        post = _probe(args.worker, post_path)
        _assert_group_tracked(post)
        _match(post, registration)
        if _candidates() != [int(registration['pid'])]:
            raise E('bootstrap_uniqueness_changed_before_commit')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        try:
            _commit(staged)
        except BaseException:
            try:
                current = _read()
                committed = registration if current == registration else None
                if current is not None and current != registration:
                    raise E('registration_commit_conflict')
            finally:
                if not staged.exists():
                    staged = None
            raise
        else:
            staged = None
            committed = registration
        if _read() != registration:
            raise E('registration_revalidation_failed')
        post = _probe(args.worker, post_path)
        _assert_group_tracked(post)
        _match(post, registration)
        if _candidates() != [int(registration['pid'])]:
            raise E('bootstrap_uniqueness_changed_before_detach')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        success = True
    finally:
        manifest_path.unlink(missing_ok=True)
        post_path.unlink(missing_ok=True)
        if staged is not None:
            staged.unlink(missing_ok=True)
        if not success and child is not None:
            _kill(child.pid)
            try:
                _worker(args.worker, 'rollback', str(child.pid))
            except BaseException as exc:
                if committed is not None:
                    _remove(committed)
                raise E('bootstrap_rollback_failed', str(exc))
        if not success and committed is not None:
            _remove(committed)


def _rebind(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    old, manifest = _probe_reg(args, guard, lease, manager, identity, generation, True)
    new = dict(old)
    new.update(
        registration_generation=int(old['registration_generation']) + 1,
        lease_generation=generation,
        source_task=args.task_id,
        source_run=_runid(),
    )
    for key in ('display', 'window_identity', 'remote_view_endpoint', 'remote_view_mapping', 'state'):
        new[key] = manifest[key]
    if _is_adoption_manifest(manifest):
        new['state_evidence'] = manifest['state_evidence']
    staged = _stage(new)
    committed = False
    try:
        _probe_reg(args, guard, lease, manager, identity, generation, True)
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        committed = True
        _commit(staged)
        if _read() != new:
            raise E('rebind_revalidation_failed')
        final, _ = _probe_reg(args, guard, lease, manager, identity, generation, False)
        if final != new:
            raise E('rebind_final_registration_changed')
    except BaseException as exc:
        if committed:
            try:
                _write(old)
            except BaseException as rollback_exc:
                raise E('rebind_rollback_failed', str(rollback_exc)) from exc
            if _read() != old:
                raise E('rebind_rollback_revalidation_failed') from exc
        raise
    finally:
        if not committed:
            staged.unlink(missing_ok=True)


def _gateb(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> None:
    _probe_reg(args, guard, lease, manager, identity, generation, False)


def _read_guarded_request(path: Path) -> dict[str, Any]:
    try:
        st = path.lstat()
    except OSError as exc:
        raise E('guarded_dispatch_request_unavailable', str(exc)) from exc
    owner_ok = not hasattr(os, 'getuid') or st.st_uid == os.getuid()
    if not path.is_file() or path.is_symlink() or not owner_ok:
        raise E('guarded_dispatch_request_unsafe')
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise E('guarded_dispatch_request_invalid', str(exc)) from exc
    action_hash = data.get('action_hash') if isinstance(data, dict) else None
    if data.get('schema_version') != 1 or not isinstance(action_hash, str):
        raise E('guarded_dispatch_request_invalid')
    if len(action_hash) != 64 or any(c not in '0123456789abcdef' for c in action_hash.lower()):
        raise E('guarded_dispatch_request_invalid')
    forbidden = {'key', 'keys', 'coordinate', 'coordinates', 'opcode', 'address', 'pointer',
                 'pid', 'window_id', 'display', 'credential', 'password', 'token', 'lease_token'}

    def reject_raw(value: Any) -> None:
        if isinstance(value, dict):
            if forbidden.intersection(str(key).lower() for key in value):
                raise E('guarded_dispatch_request_raw_field_forbidden')
            for nested in value.values():
                reject_raw(nested)
        elif isinstance(value, list):
            for nested in value:
                reject_raw(nested)

    reject_raw(data)
    return data


def _guarded_fence_digest(registration: dict[str, Any], manifest: dict[str, Any]) -> str:
    fields = {
        'runtime_id': registration.get('runtime_id'),
        'registration_generation': registration.get('registration_generation'),
        'lease_generation': registration.get('lease_generation'),
        'boot_id_sha256': registration.get('boot_id_sha256'),
        'process_start_ticks': registration.get('process_start_ticks'),
        'client_sha256': registration.get('client_sha256'),
        'runtime_locator': registration.get('runtime_locator'),
        'candidate_fingerprint': registration.get('candidate_fingerprint'),
        'manifest_state': manifest.get('state'),
        'manifest_window_identity': manifest.get('window_identity'),
    }
    payload = json.dumps(fields, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(payload).hexdigest()


def _acquire_input_lock(args: argparse.Namespace, guard: Any):
    module = _input_lock_module()
    timeout = float(getattr(args, 'input_lock_timeout', 10.0))
    return module.InputLock(STATE).acquire(
        timeout_seconds=timeout,
        cancelled=lambda: guard._supervisor_cancel_signal is not None,
    )


def _emit_guarded_ready(request: dict[str, Any], fence_digest: str) -> None:
    payload = {
        'protocol': 'track-a-guarded-dispatch-v1',
        'status': 'READY',
        'action_hash': request['action_hash'],
        'fence_digest': fence_digest,
    }
    print('TRACK_A_GUARDED_DISPATCH_READY=' + json.dumps(payload, sort_keys=True, separators=(',', ':')), flush=True)


def _read_guarded_decision(stream: Any = None) -> str:
    source = sys.stdin if stream is None else stream
    raw = source.readline()
    if raw not in {'COMMIT\n', 'ABORT\n'}:
        raise E('guarded_dispatch_decision_invalid')
    return raw.rstrip('\n')


def _run_guarded_worker(args: argparse.Namespace, request: dict[str, Any]) -> dict[str, Any]:
    result_path = STATE / '.guarded-dispatch-result.json'
    result_path.unlink(missing_ok=True)
    try:
        completed = subprocess.run(
            [str(args.worker), 'guarded-dispatch', str(args.request_file), str(result_path)],
            env=_env(), close_fds=True, check=False, timeout=args.worker_timeout,
        )
        if completed.returncode:
            raise E('guarded_dispatch_worker_failed')
        try:
            result = json.loads(result_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise E('guarded_dispatch_worker_result_invalid', str(exc)) from exc
        allowed_keys = {'status', 'effect_count', 'action_hash', 'reason_code'}
        if not isinstance(result, dict) or not set(result).issubset(allowed_keys):
            raise E('guarded_dispatch_worker_result_invalid')
        if result.get('action_hash') != request['action_hash']:
            raise E('guarded_dispatch_worker_action_hash_mismatch')
        if result.get('effect_count') not in {0, 1}:
            raise E('guarded_dispatch_worker_effect_count_invalid')
        if result.get('status') not in {'CONFIRMED', 'AMBIGUOUS', 'REFUSED'}:
            raise E('guarded_dispatch_worker_result_invalid')
        reason = result.get('reason_code')
        if reason is not None and (not isinstance(reason, str) or not reason or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_' for c in reason)):
            raise E('guarded_dispatch_worker_result_invalid')
        return result
    finally:
        result_path.unlink(missing_ok=True)


def _guarded_dispatch(
    args: argparse.Namespace,
    guard: Any,
    lease: Any,
    manager: Any,
    identity: Any,
    generation: int,
) -> dict[str, Any]:
    request = _read_guarded_request(args.request_file)
    first_registration, first_manifest = _probe_reg(
        args, guard, lease, manager, identity, generation, False
    )
    first_fence = _guarded_fence_digest(first_registration, first_manifest)
    with _acquire_input_lock(args, guard):
        second_registration, second_manifest = _probe_reg(
            args, guard, lease, manager, identity, generation, False
        )
        second_fence = _guarded_fence_digest(second_registration, second_manifest)
        if second_fence != first_fence:
            raise E('guarded_dispatch_fence_changed_before_ready')
        _emit_guarded_ready(request, second_fence)
        decision = _read_guarded_decision()
        if decision == 'ABORT':
            result = {'status': 'ABORTED', 'effect_count': 0, 'action_hash': request['action_hash']}
            print('TRACK_A_GUARDED_DISPATCH_RESULT=' + json.dumps(result, sort_keys=True, separators=(',', ':')), flush=True)
            return result
        third_registration, third_manifest = _probe_reg(
            args, guard, lease, manager, identity, generation, False
        )
        third_fence = _guarded_fence_digest(third_registration, third_manifest)
        if third_fence != second_fence:
            raise E('guarded_dispatch_fence_changed_before_effect')
        _lease(manager, lease, identity, args.token_file, generation)
        _cancel(guard)
        result = _run_guarded_worker(args, request)
        print('TRACK_A_GUARDED_DISPATCH_RESULT=' + json.dumps(result, sort_keys=True, separators=(',', ':')), flush=True)
        return result


def _child(args: argparse.Namespace, guard: Any, lock_fd: int, previous_mask: set[signal.Signals]) -> None:
    rc = 2
    try:
        guard._supervisor_cancel_signal = None
        guard._install_supervisor_signal_handlers(previous_mask)
        guard._become_child_subreaper()
        lease = guard.lease
        manager = lease.LeaseManager(STATE)
        identity = lease.LeaseIdentity(args.task_id, args.session_id)
        generation = _lease(manager, lease, identity, args.token_file)
        _cancel(guard)
        {'bootstrap': _bootstrap, 'adopt-existing': _adopt_existing, 'semantic-downgrade': _semantic_downgrade, 'rebind': _rebind, 'gate-b': _gateb, 'guarded-dispatch': _guarded_dispatch}[args.operation](
            args, guard, lease, manager, identity, generation
        )
        label = args.operation.upper().replace('-', '_')
        print(f'TRACK_A_CANONICAL_{label}=PASS', flush=True)
        print(f'TRACK_A_CANONICAL_LEASE_GENERATION={generation}', flush=True)
        rc = 0
    except (E, guard.lease.LeaseError) as exc:
        print(
            f'TRACK_A_CANONICAL_TRANSITION_ERROR={getattr(exc, "code", "lease_error")}',
            file=sys.stderr, flush=True,
        )
    except subprocess.TimeoutExpired:
        print('TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout', file=sys.stderr, flush=True)
    except BaseException:
        print('TRACK_A_CANONICAL_TRANSITION_ERROR=supervisor_failure', file=sys.stderr, flush=True)
    finally:
        try:
            os.close(lock_fd)
        except OSError:
            pass
    os._exit(rc)


def _supervise(args: argparse.Namespace) -> int:
    guard = _guard()
    lease = guard.lease
    identity = lease.LeaseIdentity(
        lease._validate_identity(args.task_id, 'task-id'),
        lease._validate_identity(args.session_id, 'session-id'),
    )
    manager = lease.LeaseManager(STATE)
    token = lease._read_private_token(args.token_file)
    manager._prepare()
    lock_fd = os.open(manager.lock_path, os.O_RDWR)
    previous_mask: set[signal.Signals] | None = None
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        state = manager._load_state_unlocked()
        manager._require_current_unlocked(state, identity, token, lease._now_epoch(None))
        previous_mask = signal.pthread_sigmask(
            signal.SIG_BLOCK, guard.SUPERVISOR_CANCELLATION_SIGNALS
        )
        supervisor_pid = os.fork()
        if supervisor_pid == 0:
            _child(args, guard, lock_fd, previous_mask)
        pending = signal.sigpending()
        for signum in guard.SUPERVISOR_CANCELLATION_SIGNALS:
            if signum in pending:
                try:
                    os.kill(supervisor_pid, signum)
                except ProcessLookupError:
                    pass
                break
        signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
        previous_mask = None
        os.close(lock_fd)
        lock_fd = -1
        _, wait_status = os.waitpid(supervisor_pid, 0)
        return os.waitstatus_to_exitcode(wait_status)
    finally:
        if previous_mask is not None:
            try:
                signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            except OSError:
                pass
        if lock_fd >= 0:
            try:
                os.close(lock_fd)
            except OSError:
                pass


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest='operation', required=True)
    for name in ('bootstrap', 'adopt-existing', 'semantic-downgrade', 'rebind', 'gate-b', 'guarded-dispatch'):
        command = sub.add_parser(name)
        command.add_argument('--task-id', required=True)
        command.add_argument('--session-id', required=True)
        command.add_argument('--token-file', required=True, type=Path)
        if name == 'bootstrap':
            command.add_argument('--worker', required=True, type=Path)
            command.add_argument('--worker-timeout', type=int, default=180)
        elif name == 'guarded-dispatch':
            command.add_argument('--probe', required=True, type=Path)
            command.add_argument('--worker', required=True, type=Path)
            command.add_argument('--request-file', required=True, type=Path)
            command.add_argument('--worker-timeout', type=int, default=30)
            command.add_argument('--input-lock-timeout', type=float, default=10.0)
        else:
            command.add_argument('--probe', required=True, type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return _supervise(parser().parse_args(argv))
    except Exception as exc:
        print(
            f'TRACK_A_CANONICAL_TRANSITION_ERROR={getattr(exc, "code", "controller_failure")}',
            file=sys.stderr,
        )
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
