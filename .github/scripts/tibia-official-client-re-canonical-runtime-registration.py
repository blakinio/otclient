#!/usr/bin/env python3
"""Read-only Track A canonical runtime candidate registration probe.

The probe inspects X11 window metadata, /proc executable/process-start identity,
Linux boot identity and sanitized noVNC/RFB metadata. It never sends X11/VNC
input, reads process environments/credentials/cmdlines, attaches with ptrace, or
exports framebuffer contents.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import socket
import struct
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51_965_216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
TRACK_DISPLAY = ":98"
WEB_PORT = 6082
TIMEOUT = 4.0


class ProbeError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProcessIdentity:
    pid: int
    process_start_ticks: int
    boot_id_sha256: str
    exact_executable: bool
    executable_size: int
    executable_sha256: str | None


@dataclass(frozen=True)
class WindowCandidate:
    window_id: int
    visible: bool
    pid: int | None
    width: int | None
    height: int | None
    exact_executable: bool
    executable_size: int | None
    executable_sha256: str | None
    process_start_ticks: int | None
    boot_id_sha256: str | None


@dataclass(frozen=True)
class RfbMetadata:
    reachable: bool
    protocol_version: str | None
    width: int | None
    height: int | None
    security_types_hex: str | None
    desktop_name_sha256: str | None
    desktop_name_references_display_98: bool | None
    error_class: str | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_process_start_ticks(pid: int) -> int:
    text = Path(f"/proc/{pid}/stat").read_text(encoding="ascii", errors="strict")
    rparen = text.rfind(")")
    if rparen < 0:
        raise ProbeError("invalid /proc stat format")
    fields_after_comm = text[rparen + 2 :].split()
    # fields_after_comm[0] is Linux /proc stat field 3; field 22 is index 19.
    if len(fields_after_comm) <= 19:
        raise ProbeError("truncated /proc stat")
    return int(fields_after_comm[19])


def boot_id_digest() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9a-fA-F-]{32,64}", raw):
        raise ProbeError("invalid boot id format")
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def inspect_pid(pid: int, boot_digest: str, digest_cache: dict[tuple[int, int, int], str]) -> ProcessIdentity | None:
    try:
        exe = Path(f"/proc/{pid}/exe").resolve(strict=True)
        st = exe.stat()
        size = int(st.st_size)
        if size != EXPECTED_SIZE:
            return None
        cache_key = (int(st.st_dev), int(st.st_ino), size)
        digest = digest_cache.get(cache_key)
        if digest is None:
            digest = sha256_file(exe)
            digest_cache[cache_key] = digest
        if digest != EXPECTED_SHA256:
            return None
        start_ticks = read_process_start_ticks(pid)
        return ProcessIdentity(
            pid=pid,
            process_start_ticks=start_ticks,
            boot_id_sha256=boot_digest,
            exact_executable=True,
            executable_size=size,
            executable_sha256=digest,
        )
    except (FileNotFoundError, PermissionError, ProcessLookupError, OSError, ProbeError, ValueError):
        return None


def enumerate_exact_processes(boot_digest: str) -> list[ProcessIdentity]:
    digest_cache: dict[tuple[int, int, int], str] = {}
    identities: list[ProcessIdentity] = []
    for proc_dir in Path("/proc").iterdir():
        if not proc_dir.name.isdigit():
            continue
        identity = inspect_pid(int(proc_dir.name), boot_digest, digest_cache)
        if identity is not None:
            identities.append(identity)
    return sorted(identities, key=lambda item: (item.pid, item.process_start_ticks))


def toolroot_from_state() -> Path:
    canonical = Path("/home/runner/_work/_otclient_tibia_re_state")
    legacy = Path("/work/_otclient_tibia_re_state")
    for state in (canonical, legacy):
        if (state / "toolroot").is_dir():
            return state / "toolroot"
    raise ProbeError("Track A toolroot unavailable")


def xdotool_env(toolroot: Path) -> dict[str, str]:
    return {
        "DISPLAY": TRACK_DISPLAY,
        "PATH": f"{toolroot}/usr/bin:{toolroot}/usr/sbin:/usr/bin:/bin",
        "LD_LIBRARY_PATH": f"{toolroot}/usr/lib/x86_64-linux-gnu:{toolroot}/lib/x86_64-linux-gnu",
        "LC_ALL": "C",
    }


def run_xdotool(toolroot: Path, *args: str, check: bool = True) -> str:
    binary = toolroot / "usr/bin/xdotool"
    if not binary.is_file():
        raise ProbeError("xdotool unavailable")
    completed = subprocess.run(
        [str(binary), *args],
        env=xdotool_env(toolroot),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
        check=False,
    )
    if check and completed.returncode != 0:
        raise ProbeError(f"xdotool failed rc={completed.returncode}")
    return completed.stdout


def parse_window_ids(text: str) -> set[int]:
    values: set[int] = set()
    for line in text.splitlines():
        value = line.strip()
        if value.isdigit() and int(value) > 0:
            values.add(int(value))
    return values


def parse_geometry(text: str) -> tuple[int | None, int | None]:
    width = None
    height = None
    for line in text.splitlines():
        if line.startswith("WIDTH="):
            width = int(line.split("=", 1)[1])
        elif line.startswith("HEIGHT="):
            height = int(line.split("=", 1)[1])
    return width, height


def inspect_window(
    toolroot: Path,
    window_id: int,
    visible: bool,
    exact_process_by_pid: dict[int, ProcessIdentity],
) -> WindowCandidate:
    pid: int | None = None
    raw_pid = run_xdotool(toolroot, "getwindowpid", str(window_id), check=False).strip()
    if raw_pid.isdigit() and int(raw_pid) > 0:
        pid = int(raw_pid)

    width: int | None = None
    height: int | None = None
    try:
        width, height = parse_geometry(
            run_xdotool(toolroot, "getwindowgeometry", "--shell", str(window_id))
        )
    except ProbeError:
        pass

    identity = exact_process_by_pid.get(pid) if pid is not None else None
    return WindowCandidate(
        window_id=window_id,
        visible=visible,
        pid=pid,
        width=width,
        height=height,
        exact_executable=identity is not None,
        executable_size=identity.executable_size if identity else None,
        executable_sha256=identity.executable_sha256 if identity else None,
        process_start_ticks=identity.process_start_ticks if identity else None,
        boot_id_sha256=identity.boot_id_sha256 if identity else None,
    )


def list_x11_socket_displays() -> list[int]:
    root = Path("/tmp/.X11-unix")
    if not root.is_dir():
        return []
    values: list[int] = []
    for entry in root.iterdir():
        match = re.fullmatch(r"X(\d+)", entry.name)
        if match:
            values.append(int(match.group(1)))
    return sorted(set(values))


def default_ipv4_gateway() -> str | None:
    try:
        lines = Path("/proc/net/route").read_text(encoding="ascii").splitlines()[1:]
    except OSError:
        return None
    for row in lines:
        fields = row.split()
        if len(fields) < 4 or fields[1] != "00000000":
            continue
        try:
            flags = int(fields[3], 16)
            raw = int(fields[2], 16)
        except ValueError:
            continue
        if (flags & 0x2) and raw:
            return socket.inet_ntoa(struct.pack("<I", raw))
    return None


def recv_exact(sock: socket.socket, count: int) -> bytes:
    out = bytearray()
    while len(out) < count:
        chunk = sock.recv(count - len(out))
        if not chunk:
            raise EOFError("socket closed")
        out.extend(chunk)
    return bytes(out)


def websocket_send(sock: socket.socket, payload: bytes) -> None:
    mask = os.urandom(4)
    length = len(payload)
    frame = bytearray([0x82])
    if length < 126:
        frame.append(0x80 | length)
    elif length <= 0xFFFF:
        frame.append(0x80 | 126)
        frame.extend(struct.pack("!H", length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack("!Q", length))
    frame.extend(mask)
    frame.extend(bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload)))
    sock.sendall(frame)


def websocket_recv(sock: socket.socket) -> bytes:
    while True:
        head = recv_exact(sock, 2)
        opcode = head[0] & 0x0F
        length = head[1] & 0x7F
        masked = bool(head[1] & 0x80)
        if length == 126:
            length = struct.unpack("!H", recv_exact(sock, 2))[0]
        elif length == 127:
            length = struct.unpack("!Q", recv_exact(sock, 8))[0]
        mask = recv_exact(sock, 4) if masked else None
        payload = bytearray(recv_exact(sock, length))
        if mask:
            for i in range(len(payload)):
                payload[i] ^= mask[i % 4]
        if opcode == 8:
            raise EOFError("websocket closed")
        if opcode == 9:
            pong_mask = os.urandom(4)
            frame = bytearray([0x8A, 0x80 | len(payload)])
            frame.extend(pong_mask)
            frame.extend(bytes(byte ^ pong_mask[i % 4] for i, byte in enumerate(payload)))
            sock.sendall(frame)
            continue
        if opcode == 1:
            return base64.b64decode(bytes(payload), validate=True)
        if opcode == 2:
            return bytes(payload)


class WebsocketRfbStream:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.buf = bytearray()

    def read(self, count: int) -> bytes:
        while len(self.buf) < count:
            self.buf.extend(websocket_recv(self.sock))
        out = bytes(self.buf[:count])
        del self.buf[:count]
        return out

    def write(self, payload: bytes) -> None:
        websocket_send(self.sock, payload)


def rfb_server_metadata(stream: WebsocketRfbStream) -> tuple[str, int, int, str, bytes]:
    banner = stream.read(12)
    if not re.fullmatch(rb"RFB \d{3}\.\d{3}\n", banner):
        raise ProbeError("invalid RFB banner")
    stream.write(banner)
    count = stream.read(1)[0]
    if count == 0 or count > 32:
        raise ProbeError("invalid RFB security type count")
    security = stream.read(count)
    if 1 not in security:
        raise ProbeError("RFB no-auth metadata handshake unavailable")
    stream.write(b"\x01")
    if stream.read(4) != b"\x00\x00\x00\x00":
        raise ProbeError("RFB security negotiation failed")
    stream.write(b"\x01")
    server_init = stream.read(24)
    width, height = struct.unpack("!HH", server_init[:4])
    name_len = struct.unpack("!I", server_init[20:24])[0]
    if name_len > 4096:
        raise ProbeError("RFB desktop name too long")
    name = stream.read(name_len)
    return banner.decode("ascii").strip().split(" ", 1)[1], width, height, security.hex(), name


def inspect_rfb() -> RfbMetadata:
    gateway = default_ipv4_gateway()
    if not gateway:
        return RfbMetadata(False, None, None, None, None, None, None, "GatewayUnavailable")
    sock: socket.socket | None = None
    try:
        sock = socket.create_connection((gateway, WEB_PORT), timeout=TIMEOUT)
        sock.settimeout(TIMEOUT)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request = (
            "GET /websockify HTTP/1.1\r\n"
            f"Host: synology:{WEB_PORT}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Sec-WebSocket-Protocol: binary\r\n"
            f"Origin: http://synology:{WEB_PORT}\r\n\r\n"
        ).encode("ascii")
        sock.sendall(request)
        header = bytearray()
        while b"\r\n\r\n" not in header and len(header) < 16_384:
            chunk = sock.recv(4096)
            if not chunk:
                raise EOFError("websocket HTTP response closed")
            header.extend(chunk)
        if b" 101 " not in bytes(header).split(b"\r\n", 1)[0]:
            raise ProbeError("websocket upgrade rejected")
        protocol, width, height, security, name = rfb_server_metadata(WebsocketRfbStream(sock))
        name_text = name.decode("utf-8", errors="replace")
        references_98 = bool(
            re.search(r"(?i)(?:display\s*:?\s*98|:98(?:\D|$)|x98(?:\D|$))", name_text)
        )
        return RfbMetadata(
            True,
            protocol,
            width,
            height,
            security,
            hashlib.sha256(name).hexdigest(),
            references_98,
            None,
        )
    except Exception as exc:
        return RfbMetadata(False, None, None, None, None, None, None, type(exc).__name__)
    finally:
        if sock is not None:
            sock.close()


def classify(
    candidates: list[WindowCandidate],
    global_exact_processes: list[ProcessIdentity],
    display_present: bool,
) -> str:
    if any(candidate.exact_executable for candidate in candidates):
        return "EXACT_LIVE_RUNTIME_CANDIDATE_PROVEN"
    if candidates:
        return "LIVE_CLIENT_IDENTITY_MISMATCH"
    if global_exact_processes:
        return "INCONCLUSIVE_EXACT_CLIENT_PROCESS_UNBOUND"
    if display_present:
        return "PERSISTENT_DISPLAY_NO_LIVE_CLIENT"
    return "INCONCLUSIVE"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if os.environ.get("GITHUB_REPOSITORY") != "blakinio/otclient":
        raise ProbeError("wrong repository")
    if os.environ.get("RUNNER_NAME") != "synology-otclient-01":
        raise ProbeError("wrong runner")

    displays = list_x11_socket_displays()
    display_present = 98 in displays
    toolroot = toolroot_from_state()
    boot_digest = boot_id_digest()
    global_exact_processes = enumerate_exact_processes(boot_digest)
    exact_process_by_pid = {identity.pid: identity for identity in global_exact_processes}

    all_window_ids: set[int] = set()
    visible_window_ids: set[int] = set()
    if display_present:
        all_window_ids = parse_window_ids(
            run_xdotool(toolroot, "search", "--name", "^Tibia$", check=False)
        )
        visible_window_ids = parse_window_ids(
            run_xdotool(toolroot, "search", "--onlyvisible", "--name", "^Tibia$", check=False)
        )

    candidates = [
        inspect_window(toolroot, window_id, window_id in visible_window_ids, exact_process_by_pid)
        for window_id in sorted(all_window_ids)
    ]
    rfb = inspect_rfb()
    semantic_result = classify(candidates, global_exact_processes, display_present)

    result: dict[str, Any] = {
        "schema_version": 2,
        "track": "official-client-re",
        "runtime_class": "canonical_live_candidate",
        "display": TRACK_DISPLAY,
        "persistent_x11_displays": [f":{value}" for value in displays],
        "display_98_present": display_present,
        "tibia_window_count_all": len(all_window_ids),
        "tibia_window_count_visible": len(visible_window_ids),
        "candidates": [asdict(candidate) for candidate in candidates],
        "global_exact_client_processes": [asdict(identity) for identity in global_exact_processes],
        "exact_client_fence": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "rfb_6082": asdict(rfb),
        "rfb_desktop_name_supports_display_98_mapping": rfb.desktop_name_references_display_98,
        "exact_6082_backend_display": "UNKNOWN",
        "semantic_result": semantic_result,
        "display_98_is_canonical": False,
        "read_only": True,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    print("TRACK_A_CANONICAL_REGISTRATION_COMPLETE=true")
    print(f"TRACK_A_CANONICAL_REGISTRATION_RESULT={semantic_result}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_X11_DISPLAYS={','.join(result['persistent_x11_displays']) or 'none'}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_DISPLAY98_PRESENT={str(display_present).lower()}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_TIBIA_WINDOWS_ALL={len(all_window_ids)}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_TIBIA_WINDOWS_VISIBLE={len(visible_window_ids)}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_EXACT_PROCESSES_GLOBAL={len(global_exact_processes)}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_EXACT_WINDOW_CANDIDATES={sum(1 for c in candidates if c.exact_executable)}")
    print(f"TRACK_A_CANONICAL_REGISTRATION_RFB_REACHABLE={str(rfb.reachable).lower()}")
    print(
        "TRACK_A_CANONICAL_REGISTRATION_RFB_NAME_SUPPORTS_DISPLAY98="
        + ("unknown" if rfb.desktop_name_references_display_98 is None else str(rfb.desktop_name_references_display_98).lower())
    )
    print("TRACK_A_CANONICAL_REGISTRATION_6082_BACKEND_DISPLAY=UNKNOWN")
    print("TRACK_A_CANONICAL_REGISTRATION_FRAMEBUFFER_EXPORTED=false")
    print("TRACK_A_CANONICAL_REGISTRATION_PROCESS_ENV_READ=false")
    print("TRACK_A_CANONICAL_REGISTRATION_PROCESS_CMDLINE_READ=false")
    print("TRACK_A_CANONICAL_REGISTRATION_PTRACE_USED=false")
    print("TRACK_A_CANONICAL_REGISTRATION_INPUT_SENT=false")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeError as exc:
        print(f"TRACK_A_CANONICAL_REGISTRATION_ERROR={type(exc).__name__}", file=sys.stderr)
        raise SystemExit(2)
