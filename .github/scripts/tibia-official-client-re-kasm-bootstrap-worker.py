#!/usr/bin/env python3
"""Fail-closed KasmVNC create-new worker for Track A canonical bootstrap."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
_CURRENT_FENCE_MODULE = importlib.import_module(
    "tools.tibia_re_control_center.current_client_fence"
)
_CURRENT_CLIENT_FENCE = _CURRENT_FENCE_MODULE.current_client_fence()

TARGET_CONTAINER = 'otclient-track-a-kasmvnc'
TARGET_USER = 'kasm-user'
TARGET_DISPLAY = ':1'
HOME_DIR = '/home/kasm-user'
PACKAGE_DIR = '/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia'
CLIENT_PATH = PACKAGE_DIR + '/bin/client'
VER = _CURRENT_CLIENT_FENCE.version
SIZE = _CURRENT_CLIENT_FENCE.size
SHA = _CURRENT_CLIENT_FENCE.sha256
PREFLIGHT_SCHEMA = 'otclient.track-a.kasm-bootstrap.preflight.v1'
LAUNCH_SCHEMA = 'otclient.track-a.kasm-bootstrap.launch.v1'
LAUNCH_METHOD = 'docker_exec_detached_direct_env'
FULL_ID_RE = re.compile(r'^[0-9a-f]{64}$')
WINDOW_RE = re.compile(r'^\s*(0x[0-9a-fA-F]+)\s+"Tibia(?: - .+)?":')

PACKAGE_IDENTITY_SCRIPT = r'''
import hashlib,json,os,stat,sys
path=sys.argv[1]
try:
    st=os.lstat(path)
    symlink=stat.S_ISLNK(st.st_mode)
    regular=stat.S_ISREG(st.st_mode)
    executable=os.access(path,os.X_OK)
    size=st.st_size
    digest=''
    if regular and not symlink:
        h=hashlib.sha256()
        with open(path,'rb',buffering=0) as f:
            for block in iter(lambda:f.read(1<<20),b''): h.update(block)
        digest=h.hexdigest()
    print(json.dumps({'path':path,'regular':regular,'symlink':symlink,'executable':executable,'size':size,'sha256':digest},sort_keys=True,separators=(',',':')))
except OSError:
    print(json.dumps({'path':path,'regular':False,'symlink':False,'executable':False,'size':-1,'sha256':''},sort_keys=True,separators=(',',':')))
'''

CANDIDATE_SCRIPT = r'''
import hashlib,json,os,pathlib,sys
expected_size=int(sys.argv[1])
rows=[]
for entry in pathlib.Path('/proc').iterdir():
    if not entry.name.isdigit(): continue
    pid=int(entry.name)
    try:
        comm=(entry/'comm').read_text(errors='replace').strip()
    except OSError:
        comm=''
    try:
        exe=os.readlink(entry/'exe')
    except OSError:
        if comm=='client' or comm.startswith('Tibia'):
            rows.append({'readable':False,'pid':pid,'official_hint':True})
        continue
    hint=('CipSoft GmbH/Tibia/packages/Tibia' in exe or '/Tibia/packages/Tibia/' in exe or comm=='client' or comm.startswith('Tibia'))
    try:
        st=os.stat(entry/'exe')
    except OSError:
        if hint: rows.append({'readable':False,'pid':pid,'official_hint':True})
        continue
    if not hint and st.st_size!=expected_size: continue
    try:
        h=hashlib.sha256()
        with open(entry/'exe','rb',buffering=0) as f:
            for block in iter(lambda:f.read(1<<20),b''): h.update(block)
        raw=(entry/'stat').read_text()
        close=raw.rfind(')')
        fields=raw[close+2:].split()
        if close<0 or len(fields)<20: raise ValueError('stat')
        start=int(fields[19])
    except (OSError,ValueError):
        if hint: rows.append({'readable':False,'pid':pid,'official_hint':True})
        continue
    rows.append({'readable':True,'pid':pid,'exe':exe,'size':st.st_size,'sha256':h.hexdigest(),'start_ticks':start,'official_hint':hint})
print(json.dumps(rows,sort_keys=True,separators=(',',':')))
'''

BOOT_ID_SCRIPT = r'''
import hashlib,json,pathlib,uuid
path=pathlib.Path('/proc/sys/kernel/random/boot_id')
try:
    raw=path.read_bytes()
    uuid.UUID(raw.decode('ascii').strip())
    digest=hashlib.sha256(raw).hexdigest()
    print(json.dumps({'boot_id_sha256':digest},sort_keys=True,separators=(',',':')))
except (OSError,UnicodeDecodeError,ValueError):
    print(json.dumps({'boot_id_sha256':''},sort_keys=True,separators=(',',':')))
'''

PROCESS_IDENTITY_SCRIPT = r'''
import hashlib,json,os,pathlib,sys
pid=int(sys.argv[1]); root=pathlib.Path('/proc')/str(pid)
if not root.exists():
    print(json.dumps({'present':False},sort_keys=True,separators=(',',':'))); raise SystemExit(0)
try:
    exe=os.readlink(root/'exe'); st=os.stat(root/'exe')
    h=hashlib.sha256()
    with open(root/'exe','rb',buffering=0) as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    raw=(root/'stat').read_text(); close=raw.rfind(')'); fields=raw[close+2:].split()
    if close<0 or len(fields)<20: raise ValueError('stat')
    print(json.dumps({'present':True,'pid':pid,'exe':exe,'size':st.st_size,'sha256':h.hexdigest(),'start_ticks':int(fields[19])},sort_keys=True,separators=(',',':')))
except (OSError,ValueError):
    print(json.dumps({'present':True,'pid':pid,'unverifiable':True},sort_keys=True,separators=(',',':')))
'''


class WorkerError(RuntimeError):
    pass


def run(command: Sequence[str]) -> str:
    try:
        completed = subprocess.run(
            list(command), check=False, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkerError(f'command_failed:{command[0]}') from exc
    if completed.returncode:
        raise WorkerError(f'command_failed:{command[0]}:{completed.returncode}')
    return completed.stdout


def _json(output: str, code: str) -> Any:
    try:
        return json.loads(output.strip())
    except (json.JSONDecodeError, AttributeError) as exc:
        raise WorkerError(code) from exc


def write_record(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(path, flags, 0o600)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, sort_keys=True, separators=(',', ':'))
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def read_record(path: Path, expected_schema: str) -> dict[str, Any]:
    try:
        st = path.lstat()
        if not stat.S_ISREG(st.st_mode) or path.is_symlink() or stat.S_IMODE(st.st_mode) != 0o600:
            raise WorkerError('record_file_unsafe')
        data = json.loads(path.read_text(encoding='utf-8'))
    except WorkerError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkerError('record_invalid') from exc
    if not isinstance(data, dict) or data.get('schema') != expected_schema:
        raise WorkerError('record_schema_invalid')
    return data


def docker_containers(runner: Callable[[Sequence[str]], str] = run) -> list[tuple[str, str]]:
    output = runner(['docker', 'ps', '--no-trunc', '--format', '{{.ID}}\t{{.Names}}'])
    rows: list[tuple[str, str]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split('\t', 1)
        if len(parts) != 2:
            raise WorkerError('docker_inventory_malformed')
        rows.append((parts[0].strip().lower(), parts[1].strip()))
    return rows


def _target(containers: list[tuple[str, str]]) -> str:
    matches = [cid for cid, name in containers if name == TARGET_CONTAINER]
    if len(matches) != 1:
        raise WorkerError(f'target_container_count:{len(matches)}')
    container_id = matches[0]
    if not FULL_ID_RE.fullmatch(container_id):
        raise WorkerError('target_container_id_invalid')
    return container_id


def package_identity(container_id: str, runner: Callable[[Sequence[str]], str] = run) -> dict[str, Any]:
    data = _json(
        runner(['docker', 'exec', container_id, 'python3', '-c', PACKAGE_IDENTITY_SCRIPT, CLIENT_PATH]),
        'client_identity_invalid',
    )
    if not isinstance(data, dict) or data.get('path') != CLIENT_PATH:
        raise WorkerError('client_identity_invalid')
    if data.get('regular') is not True:
        raise WorkerError('client_not_regular')
    if data.get('symlink') is not False:
        raise WorkerError('client_symlinked')
    if data.get('executable') is not True:
        raise WorkerError('client_not_executable')
    if data.get('size') != SIZE:
        raise WorkerError('client_size_mismatch')
    if data.get('sha256') != SHA:
        raise WorkerError('client_sha256_mismatch')
    return data


def boot_identity(container_id: str, runner: Callable[[Sequence[str]], str] = run) -> str:
    try:
        output = runner(['docker', 'exec', container_id, 'python3', '-c', BOOT_ID_SCRIPT])
    except WorkerError as exc:
        raise WorkerError('boot_identity_unavailable') from exc
    data = _json(output, 'boot_identity_invalid')
    if not isinstance(data, dict):
        raise WorkerError('boot_identity_invalid')
    value = data.get('boot_id_sha256')
    if not isinstance(value, str) or not FULL_ID_RE.fullmatch(value):
        raise WorkerError('boot_identity_invalid')
    return value


def candidate_rows(container_id: str, runner: Callable[[Sequence[str]], str] = run) -> list[dict[str, Any]]:
    data = _json(
        runner(['docker', 'exec', container_id, 'python3', '-c', CANDIDATE_SCRIPT, str(SIZE)]),
        'candidate_inventory_invalid',
    )
    if not isinstance(data, list):
        raise WorkerError('candidate_inventory_invalid')
    rows: list[dict[str, Any]] = []
    for raw in data:
        if not isinstance(raw, dict) or not isinstance(raw.get('pid'), int) or raw['pid'] < 2:
            raise WorkerError('candidate_inventory_invalid')
        row = dict(raw)
        row['container_id'] = container_id
        if row.get('readable') is not True:
            if row.get('official_hint') is True:
                raise WorkerError('official_client_candidate_unverifiable')
            continue
        if not isinstance(row.get('size'), int) or not isinstance(row.get('sha256'), str) or not isinstance(row.get('start_ticks'), int):
            raise WorkerError('candidate_inventory_invalid')
        exact = row['size'] == SIZE and row['sha256'] == SHA
        if row.get('official_hint') is True and not exact:
            raise WorkerError('conflicting_official_client_candidate')
        if exact:
            rows.append(row)
    return rows


def exact_candidates(containers: list[tuple[str, str]], runner: Callable[[Sequence[str]], str] = run) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for container_id, _name in containers:
        found.extend(candidate_rows(container_id, runner))
    return found


def _window_count(container_id: str, runner: Callable[[Sequence[str]], str] = run) -> int:
    output = runner([
        'docker', 'exec', '-u', TARGET_USER, '-e', f'DISPLAY={TARGET_DISPLAY}',
        container_id, 'xwininfo', '-root', '-tree',
    ])
    return sum(1 for line in output.splitlines() if WINDOW_RE.match(line))


def _fingerprint(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(encoded).hexdigest()


def collect_preflight(runner: Callable[[Sequence[str]], str] = run) -> dict[str, Any]:
    containers = docker_containers(runner)
    container_id = _target(containers)
    try:
        runner([
            'docker', 'exec', '-u', TARGET_USER, '-e', f'DISPLAY={TARGET_DISPLAY}',
            container_id, 'xdpyinfo',
        ])
    except WorkerError as exc:
        raise WorkerError('display_unavailable') from exc
    package_identity(container_id, runner)
    current_boot = boot_identity(container_id, runner)
    candidates = exact_candidates(containers, runner)
    if candidates:
        raise WorkerError(f'official_client_candidate_count:{len(candidates)}')
    windows = _window_count(container_id, runner)
    if windows:
        raise WorkerError(f'main_window_count:{windows}')
    payload: dict[str, Any] = {
        'schema': PREFLIGHT_SCHEMA,
        'container_name': TARGET_CONTAINER,
        'container_id': container_id,
        'display': TARGET_DISPLAY,
        'package_dir': PACKAGE_DIR,
        'client_path': CLIENT_PATH,
        'client_size': SIZE,
        'client_sha256': SHA,
        'boot_id_sha256': current_boot,
        'candidate_count': 0,
        'main_window_count': 0,
    }
    payload['preflight_fingerprint'] = _fingerprint(payload)
    return payload


def _validate_preflight(data: dict[str, Any]) -> None:
    required = {
        'schema': PREFLIGHT_SCHEMA, 'container_name': TARGET_CONTAINER,
        'display': TARGET_DISPLAY, 'package_dir': PACKAGE_DIR,
        'client_path': CLIENT_PATH, 'client_size': SIZE, 'client_sha256': SHA,
        'candidate_count': 0, 'main_window_count': 0,
    }
    for key, expected in required.items():
        if data.get(key) != expected:
            raise WorkerError('preflight_record_invalid')
    if not FULL_ID_RE.fullmatch(str(data.get('container_id', ''))):
        raise WorkerError('preflight_record_invalid')
    if not FULL_ID_RE.fullmatch(str(data.get('boot_id_sha256', ''))):
        raise WorkerError('preflight_record_invalid')
    fingerprint = data.get('preflight_fingerprint')
    unsigned = dict(data)
    unsigned.pop('preflight_fingerprint', None)
    if not isinstance(fingerprint, str) or fingerprint != _fingerprint(unsigned):
        raise WorkerError('preflight_record_invalid')


def launch_from_preflight(
    path: Path,
    runner: Callable[[Sequence[str]], str] = run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 40,
) -> dict[str, Any]:
    saved = read_record(path, PREFLIGHT_SCHEMA)
    _validate_preflight(saved)
    fresh = collect_preflight(runner)
    if fresh != saved:
        raise WorkerError('preflight_drift')
    container_id = saved['container_id']
    runner([
        'docker', 'exec', '-d', '-u', TARGET_USER, '-w', PACKAGE_DIR,
        '-e', f'HOME={HOME_DIR}', '-e', f'DISPLAY={TARGET_DISPLAY}', container_id,
        '/usr/bin/env', '-u', 'RUNNER_TRACKING_ID', '-u', 'TIBIA_TEST_EMAIL',
        '-u', 'TIBIA_TEST_PASSWORD', '-u', 'TRACK_A_CANONICAL_LEASE_TOKEN',
        '-u', 'TRACK_A_CANONICAL_LEASE_TOKEN_FILE', CLIENT_PATH,
    ])
    candidate: dict[str, Any] | None = None
    for _ in range(max(1, attempts)):
        containers = docker_containers(runner)
        try:
            current_target = _target(containers)
        except WorkerError as exc:
            raise WorkerError('postlaunch_target_not_unique') from exc
        found = exact_candidates(containers, runner)
        if len(found) > 1:
            raise WorkerError('postlaunch_target_not_unique')
        if len(found) == 1:
            candidate = found[0]
            if candidate.get('container_id') != container_id or current_target != container_id:
                raise WorkerError('postlaunch_target_not_unique')
            break
        sleeper(0.25)
    if candidate is None:
        raise WorkerError('postlaunch_target_not_unique')
    if candidate.get('exe') != CLIENT_PATH or candidate.get('size') != SIZE or candidate.get('sha256') != SHA:
        raise WorkerError('postlaunch_identity_mismatch')
    pid = candidate.get('pid')
    start = candidate.get('start_ticks')
    if not isinstance(pid, int) or pid < 2 or not isinstance(start, int) or start < 1:
        raise WorkerError('postlaunch_identity_mismatch')
    launch = {
        'schema': LAUNCH_SCHEMA,
        'preflight_fingerprint': saved['preflight_fingerprint'],
        'container_name': TARGET_CONTAINER,
        'container_id': container_id,
        'display': TARGET_DISPLAY,
        'package_dir': PACKAGE_DIR,
        'client_path': CLIENT_PATH,
        'client_size': SIZE,
        'client_sha256': SHA,
        'pid': pid,
        'process_start_ticks': start,
        'launch_method': LAUNCH_METHOD,
        'bootstrap_helper_residue': False,
    }
    write_record(path, launch)
    return launch


def _validate_launch(data: dict[str, Any]) -> None:
    required = {
        'schema': LAUNCH_SCHEMA, 'container_name': TARGET_CONTAINER,
        'display': TARGET_DISPLAY, 'package_dir': PACKAGE_DIR,
        'client_path': CLIENT_PATH, 'client_size': SIZE, 'client_sha256': SHA,
        'launch_method': LAUNCH_METHOD, 'bootstrap_helper_residue': False,
    }
    for key, expected in required.items():
        if data.get(key) != expected:
            raise WorkerError('launch_record_invalid')
    if not FULL_ID_RE.fullmatch(str(data.get('container_id', ''))):
        raise WorkerError('launch_record_invalid')
    if not isinstance(data.get('preflight_fingerprint'), str) or not FULL_ID_RE.fullmatch(data['preflight_fingerprint']):
        raise WorkerError('launch_record_invalid')
    for key in ('pid', 'process_start_ticks'):
        if not isinstance(data.get(key), int) or data[key] < 1:
            raise WorkerError('launch_record_invalid')


def process_identity(container_id: str, pid: int, runner: Callable[[Sequence[str]], str] = run) -> dict[str, Any]:
    data = _json(
        runner(['docker', 'exec', container_id, 'python3', '-c', PROCESS_IDENTITY_SCRIPT, str(pid)]),
        'rollback_identity_unverifiable',
    )
    if not isinstance(data, dict) or not isinstance(data.get('present'), bool):
        raise WorkerError('rollback_identity_unverifiable')
    return data


def _require_same_identity(launch: dict[str, Any], current: dict[str, Any]) -> None:
    if current.get('unverifiable') is True:
        raise WorkerError('rollback_identity_drift')
    expected = {
        'pid': launch['pid'], 'exe': launch['client_path'], 'size': launch['client_size'],
        'sha256': launch['client_sha256'], 'start_ticks': launch['process_start_ticks'],
    }
    if any(current.get(key) != value for key, value in expected.items()):
        raise WorkerError('rollback_identity_drift')


def rollback_launch(
    path: Path,
    runner: Callable[[Sequence[str]], str] = run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 16,
) -> None:
    launch = read_record(path, LAUNCH_SCHEMA)
    _validate_launch(launch)
    containers = docker_containers(runner)
    try:
        current_id = _target(containers)
    except WorkerError as exc:
        raise WorkerError('rollback_container_drift') from exc
    if current_id != launch['container_id']:
        raise WorkerError('rollback_container_drift')
    current = process_identity(current_id, launch['pid'], runner)
    if current.get('present') is False:
        return
    _require_same_identity(launch, current)
    runner(['docker', 'exec', current_id, '/bin/kill', '-TERM', str(launch['pid'])])
    for _ in range(max(1, attempts)):
        current = process_identity(current_id, launch['pid'], runner)
        if current.get('present') is False:
            return
        _require_same_identity(launch, current)
        sleeper(0.25)
    current = process_identity(current_id, launch['pid'], runner)
    if current.get('present') is False:
        return
    _require_same_identity(launch, current)
    runner(['docker', 'exec', current_id, '/bin/kill', '-KILL', str(launch['pid'])])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['preflight', 'launch', 'rollback'])
    parser.add_argument('record', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == 'preflight':
            write_record(args.record, collect_preflight())
        elif args.operation == 'launch':
            launch_from_preflight(args.record)
        else:
            rollback_launch(args.record)
        print(f'TRACK_A_KASM_BOOTSTRAP_{args.operation.upper()}=PASS')
        return 0
    except (WorkerError, OSError) as exc:
        print(f'TRACK_A_KASM_BOOTSTRAP_ERROR={type(exc).__name__}', file=sys.stderr if 'sys' in globals() else None)
        return 2


if __name__ == '__main__':
    import sys
    raise SystemExit(main())
