#!/usr/bin/env python3
"""Kasm bootstrap entrypoint scoped to the canonical Track A container."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import shlex
import sys
import time
from types import ModuleType
from typing import Any, Callable, Sequence

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-kasm-bootstrap-worker.py")
CANONICAL_CONTAINER = "otclient-track-a-kasmvnc"
LAUNCH_METHOD = "docker_exec_detached_official_linux_entrypoint"


def _load_base() -> ModuleType:
    spec = importlib.util.spec_from_file_location("track_a_kasm_bootstrap_worker_scoped_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("bootstrap_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
if _base.TARGET_CONTAINER != CANONICAL_CONTAINER:
    raise RuntimeError("canonical_container_contract_mismatch")
_original_candidate_rows = _base.candidate_rows
_original_collect_preflight = _base.collect_preflight
_original_rollback_launch = _base.rollback_launch
CLIENT_DIR = str(Path(_base.CLIENT_PATH).parent)
_base.LAUNCH_METHOD = LAUNCH_METHOD

LAUNCHER_DISCOVERY_SCRIPT = r'''
import hashlib,json,os,pathlib,shlex,stat,sys
home=pathlib.Path(sys.argv[1])
package=pathlib.Path(sys.argv[2])
skip={'.cache','.config','.local','.npm','.cargo','.rustup','node_modules'}
rows=[]
seen=set()
def digest(path):
    h=hashlib.sha256()
    with path.open('rb',buffering=0) as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()
def consider(path):
    try:
        lst=path.lstat(); resolved=path.resolve(strict=True)
    except OSError:
        return
    if path.is_symlink() or not stat.S_ISREG(lst.st_mode) or not os.access(path,os.X_OK):
        return
    if resolved.name!='Tibia' or package in resolved.parents:
        return
    parent=resolved.parent
    support=sum((parent/'qt.conf').is_file(), (parent/'lib').is_dir(), (parent/'plugins').is_dir())
    if support < 2:
        return
    key=str(resolved)
    if key in seen:
        return
    seen.add(key)
    try:
        st=resolved.stat(); sha=digest(resolved)
    except OSError:
        return
    rows.append({'path':key,'dir':str(parent),'size':st.st_size,'sha256':sha,'desktop_ref':False})
for current,dirs,files in os.walk(home):
    current_path=pathlib.Path(current)
    try:
        depth=len(current_path.relative_to(home).parts)
    except ValueError:
        continue
    if depth >= 5:
        dirs[:] = []
    else:
        dirs[:] = [name for name in dirs if name not in skip]
    if 'Tibia' in files:
        consider(current_path/'Tibia')
consider(pathlib.Path('/opt/Tibia/Tibia'))
by_path={row['path']:row for row in rows}
for directory in (home/'.local/share/applications', home/'Desktop', pathlib.Path('/usr/share/applications')):
    try:
        entries=list(directory.glob('*.desktop'))
    except OSError:
        continue
    for entry in entries:
        try:
            lines=entry.read_text(encoding='utf-8',errors='replace').splitlines()
        except OSError:
            continue
        for line in lines:
            if not line.startswith('Exec='):
                continue
            try:
                tokens=shlex.split(line[5:])
            except ValueError:
                continue
            if not tokens:
                continue
            token=tokens[0]
            if token.startswith('/'):
                try:
                    resolved=str(pathlib.Path(token).resolve(strict=True))
                except OSError:
                    continue
                if resolved in by_path:
                    by_path[resolved]['desktop_ref']=True
preferred=[row for row in rows if row['desktop_ref']]
selected=preferred if len(preferred)==1 else rows if not preferred and len(rows)==1 else []
print(json.dumps({'candidate_count':len(rows),'desktop_candidate_count':len(preferred),'selected':selected},sort_keys=True,separators=(',',':')))
'''

LAUNCHER_PROCESS_SCRIPT = r'''
import hashlib,json,os,pathlib,sys
expected_path=sys.argv[1]; expected_size=int(sys.argv[2]); expected_sha=sys.argv[3]
rows=[]
for entry in pathlib.Path('/proc').iterdir():
    if not entry.name.isdigit(): continue
    pid=int(entry.name)
    try:
        exe=os.readlink(entry/'exe')
    except OSError:
        continue
    if exe != expected_path:
        continue
    try:
        st=os.stat(entry/'exe')
        h=hashlib.sha256()
        with open(entry/'exe','rb',buffering=0) as f:
            for block in iter(lambda:f.read(1<<20),b''): h.update(block)
        raw=(entry/'stat').read_text(); close=raw.rfind(')'); fields=raw[close+2:].split()
        if close<0 or len(fields)<20: raise ValueError('stat')
        rows.append({'pid':pid,'start_ticks':int(fields[19]),'size':st.st_size,'sha256':h.hexdigest(),'exact':st.st_size==expected_size and h.hexdigest()==expected_sha})
    except (OSError,ValueError):
        rows.append({'pid':pid,'unverifiable':True})
print(json.dumps(rows,sort_keys=True,separators=(',',':')))
'''


def exact_candidates(
    containers: list[tuple[str, str]],
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> list[dict[str, Any]]:
    """Deep-scan only the one canonical Kasm container."""
    target = [(container_id, name) for container_id, name in containers if name == CANONICAL_CONTAINER]
    if len(target) != 1:
        raise _base.WorkerError(f"target_container_count:{len(target)}")
    return _original_candidate_rows(target[0][0], runner)


_base.exact_candidates = exact_candidates


def launcher_identity(
    container_id: str,
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> dict[str, Any]:
    data = _base._json(
        runner([
            "docker", "exec", "-u", _base.TARGET_USER, container_id,
            "python3", "-c", LAUNCHER_DISCOVERY_SCRIPT, _base.HOME_DIR, _base.PACKAGE_DIR,
        ]),
        "launcher_identity_invalid",
    )
    if not isinstance(data, dict):
        raise _base.WorkerError("launcher_identity_invalid")
    rows = data.get("selected")
    candidate_count = data.get("candidate_count")
    desktop_count = data.get("desktop_candidate_count")
    if not isinstance(rows, list) or not isinstance(candidate_count, int) or not isinstance(desktop_count, int):
        raise _base.WorkerError("launcher_identity_invalid")
    if len(rows) != 1:
        raise _base.WorkerError(f"launcher_candidate_count:{candidate_count}")
    row = rows[0]
    if not isinstance(row, dict):
        raise _base.WorkerError("launcher_identity_invalid")
    path = row.get("path")
    directory = row.get("dir")
    size = row.get("size")
    sha = row.get("sha256")
    if not isinstance(path, str) or not isinstance(directory, str) or not isinstance(size, int) or size < 1:
        raise _base.WorkerError("launcher_identity_invalid")
    if not isinstance(sha, str) or not _base.FULL_ID_RE.fullmatch(sha):
        raise _base.WorkerError("launcher_identity_invalid")
    parsed = Path(path)
    if not parsed.is_absolute() or parsed.name != "Tibia" or str(parsed.parent) != directory:
        raise _base.WorkerError("launcher_identity_invalid")
    package = Path(_base.PACKAGE_DIR)
    if parsed == package or package in parsed.parents:
        raise _base.WorkerError("launcher_identity_invalid")
    return {
        "launcher_path": path,
        "launcher_dir": directory,
        "launcher_size": size,
        "launcher_sha256": sha,
        "launcher_selection": "desktop" if desktop_count == 1 else "unique",
    }


def collect_preflight(
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> dict[str, Any]:
    payload = _original_collect_preflight(runner)
    launcher = launcher_identity(str(payload["container_id"]), runner)
    payload.pop("preflight_fingerprint", None)
    payload.update(launcher)
    payload["preflight_fingerprint"] = _base._fingerprint(payload)
    return payload


def _validate_launcher_fields(data: dict[str, Any]) -> None:
    path = data.get("launcher_path")
    directory = data.get("launcher_dir")
    size = data.get("launcher_size")
    sha = data.get("launcher_sha256")
    selection = data.get("launcher_selection")
    if not isinstance(path, str) or not isinstance(directory, str):
        raise _base.WorkerError("launcher_record_invalid")
    parsed = Path(path)
    package = Path(_base.PACKAGE_DIR)
    if not parsed.is_absolute() or parsed.name != "Tibia" or str(parsed.parent) != directory:
        raise _base.WorkerError("launcher_record_invalid")
    if parsed == package or package in parsed.parents:
        raise _base.WorkerError("launcher_record_invalid")
    if not isinstance(size, int) or size < 1:
        raise _base.WorkerError("launcher_record_invalid")
    if not isinstance(sha, str) or not _base.FULL_ID_RE.fullmatch(sha):
        raise _base.WorkerError("launcher_record_invalid")
    if selection not in {"desktop", "unique"}:
        raise _base.WorkerError("launcher_record_invalid")


def _launch_command(container_id: str, launcher_dir: str) -> list[str]:
    """Launch the current official Linux entrypoint from its own extracted directory."""
    launch_script = f"cd {shlex.quote(launcher_dir)} && exec ./Tibia"
    return [
        "docker", "exec", "-d", "-u", _base.TARGET_USER, "-w", launcher_dir,
        "-e", f"HOME={_base.HOME_DIR}",
        "-e", f"DISPLAY={_base.TARGET_DISPLAY}",
        "-e", f"XAUTHORITY={_base.HOME_DIR}/.Xauthority",
        container_id,
        "/usr/bin/env",
        "-u", "RUNNER_TRACKING_ID",
        "-u", "TIBIA_TEST_EMAIL",
        "-u", "TIBIA_TEST_PASSWORD",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE",
        "-u", "LD_PRELOAD",
        "-u", "LD_LIBRARY_PATH",
        "-u", "OTCLIENT_TIBIA_RE_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_AUTH_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
        "-u", "OTCLIENT_TIBIA_RE_BINARY_SHA256",
        "-u", "OTCLIENT_TIBIA_RE_CLIENT_VERSION",
        "-u", "OTCLIENT_TIBIA_RE_TARGETS",
        "sh", "-lc", launch_script,
    ]


def launcher_process_rows(
    record: dict[str, Any],
    runner: Callable[[Sequence[str]], str] = _base.run,
) -> list[dict[str, Any]]:
    _validate_launcher_fields(record)
    container_id = str(record.get("container_id", ""))
    if not _base.FULL_ID_RE.fullmatch(container_id):
        raise _base.WorkerError("launcher_process_identity_invalid")
    data = _base._json(
        runner([
            "docker", "exec", container_id, "python3", "-c", LAUNCHER_PROCESS_SCRIPT,
            str(record["launcher_path"]), str(record["launcher_size"]), str(record["launcher_sha256"]),
        ]),
        "launcher_process_identity_invalid",
    )
    if not isinstance(data, list):
        raise _base.WorkerError("launcher_process_identity_invalid")
    for row in data:
        if not isinstance(row, dict) or not isinstance(row.get("pid"), int) or row["pid"] < 2:
            raise _base.WorkerError("launcher_process_identity_invalid")
        if row.get("unverifiable") is True or row.get("exact") is not True:
            raise _base.WorkerError("launcher_process_identity_invalid")
        if not isinstance(row.get("start_ticks"), int) or row["start_ticks"] < 1:
            raise _base.WorkerError("launcher_process_identity_invalid")
    return data


def _wait_launcher_exit(
    record: dict[str, Any],
    runner: Callable[[Sequence[str]], str],
    sleeper: Callable[[float], None],
    attempts: int,
) -> None:
    for _ in range(max(1, attempts)):
        rows = launcher_process_rows(record, runner)
        if not rows:
            return
        if len(rows) > 1:
            raise _base.WorkerError("launcher_process_not_unique")
        sleeper(0.25)
    raise _base.WorkerError("launcher_residue")


def launch_from_preflight(
    path: Path,
    runner: Callable[[Sequence[str]], str] = _base.run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 80,
) -> dict[str, Any]:
    """Launch through the official Linux entrypoint and prove one exact game client."""
    saved = _base.read_record(path, _base.PREFLIGHT_SCHEMA)
    _base._validate_preflight(saved)
    _validate_launcher_fields(saved)
    fresh = collect_preflight(runner)
    if fresh != saved:
        raise _base.WorkerError("preflight_drift")
    container_id = str(saved["container_id"])
    runner(_launch_command(container_id, str(saved["launcher_dir"])))

    candidate: dict[str, Any] | None = None
    for _ in range(max(1, attempts)):
        containers = _base.docker_containers(runner)
        try:
            current_target = _base._target(containers)
        except _base.WorkerError as exc:
            raise _base.WorkerError("postlaunch_target_not_unique") from exc
        found = exact_candidates(containers, runner)
        if len(found) > 1:
            raise _base.WorkerError("postlaunch_target_not_unique")
        if len(found) == 1:
            candidate = found[0]
            if candidate.get("container_id") != container_id or current_target != container_id:
                raise _base.WorkerError("postlaunch_target_not_unique")
            break
        sleeper(0.25)
    if candidate is None:
        raise _base.WorkerError("postlaunch_target_not_unique")
    if candidate.get("exe") != _base.CLIENT_PATH or candidate.get("size") != _base.SIZE or candidate.get("sha256") != _base.SHA:
        raise _base.WorkerError("postlaunch_identity_mismatch")
    pid = candidate.get("pid")
    start = candidate.get("start_ticks")
    if not isinstance(pid, int) or pid < 2 or not isinstance(start, int) or start < 1:
        raise _base.WorkerError("postlaunch_identity_mismatch")

    launch = {
        "schema": _base.LAUNCH_SCHEMA,
        "preflight_fingerprint": saved["preflight_fingerprint"],
        "container_name": _base.TARGET_CONTAINER,
        "container_id": container_id,
        "display": _base.TARGET_DISPLAY,
        "package_dir": _base.PACKAGE_DIR,
        "client_path": _base.CLIENT_PATH,
        "client_size": _base.SIZE,
        "client_sha256": _base.SHA,
        "pid": pid,
        "process_start_ticks": start,
        "launch_method": LAUNCH_METHOD,
        "bootstrap_helper_residue": False,
        "client_dir": CLIENT_DIR,
        "launcher_path": saved["launcher_path"],
        "launcher_dir": saved["launcher_dir"],
        "launcher_size": saved["launcher_size"],
        "launcher_sha256": saved["launcher_sha256"],
        "launcher_selection": saved["launcher_selection"],
    }
    _base.write_record(path, launch)

    _wait_launcher_exit(launch, runner, sleeper, attempts)
    for _ in range(max(1, attempts)):
        current = _base.process_identity(container_id, pid, runner)
        if current.get("present") is not True or current.get("unverifiable") is True:
            raise _base.WorkerError("postlaunch_identity_drift")
        expected = {
            "pid": pid,
            "exe": _base.CLIENT_PATH,
            "size": _base.SIZE,
            "sha256": _base.SHA,
            "start_ticks": start,
        }
        if any(current.get(key) != value for key, value in expected.items()):
            raise _base.WorkerError("postlaunch_identity_drift")
        windows = _base._window_count(container_id, runner)
        if windows > 1:
            raise _base.WorkerError(f"main_window_count:{windows}")
        if windows == 1:
            return launch
        sleeper(0.25)
    raise _base.WorkerError("postlaunch_window_not_ready")


def _kill_launcher_residue(
    record: dict[str, Any],
    runner: Callable[[Sequence[str]], str],
    sleeper: Callable[[float], None],
    attempts: int,
) -> None:
    rows = launcher_process_rows(record, runner)
    if not rows:
        return
    if len(rows) != 1:
        raise _base.WorkerError("rollback_launcher_not_unique")
    pid = rows[0]["pid"]
    start = rows[0]["start_ticks"]
    runner(["docker", "exec", str(record["container_id"]), "/bin/kill", "-TERM", str(pid)])
    for _ in range(max(1, attempts)):
        current = launcher_process_rows(record, runner)
        if not current:
            return
        if len(current) != 1 or current[0].get("pid") != pid or current[0].get("start_ticks") != start:
            raise _base.WorkerError("rollback_launcher_identity_drift")
        sleeper(0.25)
    current = launcher_process_rows(record, runner)
    if not current:
        return
    if len(current) != 1 or current[0].get("pid") != pid or current[0].get("start_ticks") != start:
        raise _base.WorkerError("rollback_launcher_identity_drift")
    runner(["docker", "exec", str(record["container_id"]), "/bin/kill", "-KILL", str(pid)])


def _kill_late_exact_client(
    saved: dict[str, Any],
    runner: Callable[[Sequence[str]], str],
    sleeper: Callable[[float], None],
    attempts: int,
) -> None:
    containers = _base.docker_containers(runner)
    current_target = _base._target(containers)
    if current_target != saved["container_id"]:
        raise _base.WorkerError("rollback_container_drift")
    found = exact_candidates(containers, runner)
    if not found:
        return
    if len(found) != 1:
        raise _base.WorkerError("rollback_late_client_not_unique")
    row = found[0]
    launch = {
        "pid": row["pid"],
        "client_path": _base.CLIENT_PATH,
        "client_size": _base.SIZE,
        "client_sha256": _base.SHA,
        "process_start_ticks": row["start_ticks"],
    }
    current = _base.process_identity(current_target, row["pid"], runner)
    _base._require_same_identity(launch, current)
    runner(["docker", "exec", current_target, "/bin/kill", "-TERM", str(row["pid"])])
    for _ in range(max(1, attempts)):
        current = _base.process_identity(current_target, row["pid"], runner)
        if current.get("present") is False:
            return
        _base._require_same_identity(launch, current)
        sleeper(0.25)
    current = _base.process_identity(current_target, row["pid"], runner)
    if current.get("present") is False:
        return
    _base._require_same_identity(launch, current)
    runner(["docker", "exec", current_target, "/bin/kill", "-KILL", str(row["pid"])])


def _wait_clean_preflight(
    expected_fingerprint: str,
    runner: Callable[[Sequence[str]], str],
    sleeper: Callable[[float], None],
    attempts: int,
) -> None:
    last: BaseException | None = None
    for _ in range(max(1, attempts)):
        try:
            fresh = collect_preflight(runner)
        except _base.WorkerError as exc:
            last = exc
            sleeper(0.25)
            continue
        if fresh.get("preflight_fingerprint") != expected_fingerprint:
            raise _base.WorkerError("rollback_prelaunch_zero_state_unproven")
        return
    raise _base.WorkerError("rollback_prelaunch_zero_state_unproven") from last


def rollback_launch(
    path: Path,
    runner: Callable[[Sequence[str]], str] = _base.run,
    sleeper: Callable[[float], None] = time.sleep,
    attempts: int = 16,
) -> None:
    """Rollback exact game/launcher identities and re-prove the original zero state."""
    try:
        launch = _base.read_record(path, _base.LAUNCH_SCHEMA)
    except _base.WorkerError:
        launch = None
    if launch is not None:
        _base._validate_launch(launch)
        _validate_launcher_fields(launch)
        _original_rollback_launch(path, runner=runner, sleeper=sleeper, attempts=attempts)
        _kill_launcher_residue(launch, runner, sleeper, attempts)
        _wait_clean_preflight(str(launch["preflight_fingerprint"]), runner, sleeper, attempts)
        return

    saved = _base.read_record(path, _base.PREFLIGHT_SCHEMA)
    _base._validate_preflight(saved)
    _validate_launcher_fields(saved)
    _kill_launcher_residue(saved, runner, sleeper, attempts)
    _kill_late_exact_client(saved, runner, sleeper, attempts)
    _wait_clean_preflight(str(saved["preflight_fingerprint"]), runner, sleeper, attempts)


_base.collect_preflight = collect_preflight
_base.launch_from_preflight = launch_from_preflight
_base.rollback_launch = rollback_launch

WorkerError = _base.WorkerError
VER = _base.VER
SIZE = _base.SIZE
SHA = _base.SHA
process_identity = _base.process_identity


def main(argv: Sequence[str] | None = None) -> int:
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
