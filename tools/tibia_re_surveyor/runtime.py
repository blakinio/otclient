from __future__ import annotations

from dataclasses import dataclass
import json
import re
import subprocess
import time
from typing import List, Mapping, Optional, Sequence

EXPECTED_CLIENT_VERSION = "15.32"
EXPECTED_CLIENT_SIZE = 52_109_920
EXPECTED_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
CANONICAL_STATE_ROOT = "/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime"


class RuntimeProbeError(RuntimeError):
    pass


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str = ""


class CommandRunner:
    def run(self, args: Sequence[str], timeout: float = 15.0) -> CommandResult:
        try:
            completed = subprocess.run(
                list(args), check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, timeout=timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeProbeError(f"command failed: {exc}") from exc
        return CommandResult(completed.returncode, completed.stdout, completed.stderr)


class DockerRuntimeProbe:
    def __init__(self, target_container: str = "otclient-track-a-kasmvnc", display: str = ":1", control_container: str = "otclient-synology-runner", runner: Optional[CommandRunner] = None, now_fn=time.time):
        for name in (target_container, control_container):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
                raise ValueError(f"invalid container name: {name!r}")
        if not re.fullmatch(r":\d+", display):
            raise ValueError("display must look like :N")
        self.target_container = target_container
        self.control_container = control_container
        self.display = display
        self.runner = runner or CommandRunner()
        self.now_fn = now_fn

    def _run(self, args: Sequence[str], *, required: bool = True, timeout: float = 15.0) -> str:
        result = self.runner.run(args, timeout=timeout)
        if required and result.returncode != 0:
            raise RuntimeProbeError(f"command rc={result.returncode}: {result.stderr.strip()[:240]}")
        return result.stdout

    def _docker_exec(self, container: str, args: Sequence[str], *, user: Optional[str] = None, env: Optional[Mapping[str, str]] = None, required: bool = True, timeout: float = 15.0) -> str:
        command: List[str] = ["docker", "exec"]
        if user:
            command += ["-u", user]
        for key, value in sorted((env or {}).items()):
            command += ["-e", f"{key}={value}"]
        command += [container, *args]
        return self._run(command, required=required, timeout=timeout)

    @staticmethod
    def _start_ticks(proc_stat: str) -> int:
        if ")" not in proc_stat:
            raise RuntimeProbeError("malformed /proc stat")
        rest = proc_stat.rsplit(")", 1)[1].strip().split()
        if len(rest) <= 19:
            raise RuntimeProbeError("truncated /proc stat")
        return int(rest[19])

    def _process_identity(self, pid: int) -> dict:
        proc = f"/proc/{pid}"
        exe = self._docker_exec(self.target_container, ["readlink", "-f", f"{proc}/exe"]).strip()
        size = int(self._docker_exec(self.target_container, ["stat", "-Lc", "%s", f"{proc}/exe"]).strip())
        sha = self._docker_exec(self.target_container, ["sha256sum", f"{proc}/exe"], timeout=30.0).split()[0]
        stat_text = self._docker_exec(self.target_container, ["cat", f"{proc}/stat"])
        return {"pid": pid, "process_start_ticks": self._start_ticks(stat_text), "exe_basename": exe.rsplit("/", 1)[-1] if exe else None, "client_size": size, "client_sha256": sha, "exact_fence_match": size == EXPECTED_CLIENT_SIZE and sha == EXPECTED_CLIENT_SHA256}

    def _visible_tibia_windows(self) -> List[dict]:
        raw = self._docker_exec(self.target_container, ["xdotool", "search", "--onlyvisible", "--name", "^Tibia"], user="kasm-user", env={"DISPLAY": self.display}, required=False)
        windows: List[dict] = []
        for token in raw.split():
            if not token.isdigit():
                continue
            xid = int(token)
            pid_raw = self._docker_exec(self.target_container, ["xprop", "-id", str(xid), "_NET_WM_PID"], user="kasm-user", env={"DISPLAY": self.display}, required=False)
            pid_match = re.search(r"=\s*(\d+)", pid_raw)
            name_raw = self._docker_exec(self.target_container, ["xprop", "-id", str(xid), "WM_NAME"], user="kasm-user", env={"DISPLAY": self.display}, required=False)
            windows.append({"xid": xid, "pid": int(pid_match.group(1)) if pid_match else None, "title_class": "CHARACTER_CONTEXT" if "Tibia - " in name_raw else "TIBIA_WINDOW"})
        return windows

    def _candidate_containers(self) -> dict:
        names = self._run(["docker", "ps", "--format", "{{.Names}}"])
        candidates: List[dict] = []
        unresolved_count = 0
        for name in sorted(filter(None, (line.strip() for line in names.splitlines()))):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
                continue
            try:
                result = self.runner.run(["docker", "exec", name, "pgrep", "-x", "client"], timeout=5.0)
            except RuntimeProbeError:
                if name == self.target_container:
                    raise
                unresolved_count += 1
                continue
            if result.returncode not in (0, 1):
                if name == self.target_container:
                    raise RuntimeProbeError(
                        f"target container client census failed with rc={result.returncode}"
                    )
                unresolved_count += 1
                continue
            pids = [int(value) for value in result.stdout.split() if value.isdigit()]
            if pids:
                candidates.append({"container": name, "pids": pids, "count": len(pids)})
        return {"candidates": candidates, "unresolved_count": unresolved_count}

    def _safe_json_file(self, path: str, fields: Sequence[str]) -> Optional[dict]:
        script = "import json,pathlib,sys; p=pathlib.Path(sys.argv[1]); d=json.loads(p.read_text()) if p.is_file() else None; print(json.dumps(None if d is None else {k:d.get(k) for k in sys.argv[2:]},sort_keys=True))"
        raw = self._docker_exec(self.control_container, ["python3", "-c", script, path, *fields], required=False).strip()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def snapshot(self) -> dict:
        now = int(self.now_fn())
        running = self._run(["docker", "inspect", "-f", "{{.State.Running}}", self.target_container], required=False).strip() == "true"
        if not running:
            return {"observed_at_epoch": now, "target_container": self.target_container, "display": self.display, "target_running": False, "target_uniqueness": "NOT_PROVEN", "runtime_access": "READ_ONLY_UNAVAILABLE"}
        pid_raw = self._docker_exec(self.target_container, ["pgrep", "-x", "client"], required=False)
        pids = [int(value) for value in pid_raw.split() if value.isdigit()]
        processes = [self._process_identity(pid) for pid in pids]
        windows = self._visible_tibia_windows()
        candidate_probe = self._candidate_containers()
        candidates = candidate_probe["candidates"]
        unresolved_count = int(candidate_probe["unresolved_count"])
        total_candidates = sum(item["count"] for item in candidates)
        target_pid = pids[0] if len(pids) == 1 else None
        target_window = next((w for w in windows if w.get("pid") == target_pid), None)
        unique = (
            unresolved_count == 0
            and len(pids) == 1
            and total_candidates == 1
            and len(candidates) == 1
            and candidates[0]["container"] == self.target_container
            and target_window is not None
        )
        registration = self._safe_json_file(f"{CANONICAL_STATE_ROOT}/runtime-registration.json", ("schema_version", "runtime_id", "registration_generation", "lease_generation", "boot_id_sha256", "pid", "process_start_ticks", "client_version", "client_size", "client_sha256", "display", "remote_view_mapping", "state", "source_task", "source_run"))
        lease = self._safe_json_file(f"{CANONICAL_STATE_ROOT}/lease.json", ("schema_version", "runtime_id", "status", "generation", "controller_task", "acquired_at", "renewed_at", "expires_at", "takeover_from"))
        lease_expired = True
        if lease and isinstance(lease.get("expires_at"), (int, float)):
            lease_expired = int(lease["expires_at"]) <= now
        fence_match = len(processes) == 1 and bool(processes[0]["exact_fence_match"])
        return {"observed_at_epoch": now, "target_container": self.target_container, "display": self.display, "target_running": True, "processes": processes, "visible_tibia_windows": windows, "candidate_containers": candidates, "candidate_process_count": total_candidates, "candidate_probe_unresolved_count": unresolved_count, "target_uniqueness": "PROVEN" if unique else "NOT_PROVEN", "exact_current_fence": {"version": EXPECTED_CLIENT_VERSION, "size": EXPECTED_CLIENT_SIZE, "sha256": EXPECTED_CLIENT_SHA256, "match": fence_match}, "canonical_control": {"registration_present": registration is not None, "registration": registration, "lease_present": lease is not None, "lease": lease, "lease_expired": lease_expired}, "runtime_access": "READ_ONLY_ADMITTED" if unique and fence_match else "READ_ONLY_NOT_ADMITTED"}
