from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from .model import Capability, Freshness, GameSnapshot, RuntimeStatus, ValidationError

PINNED_PRODUCER_COMMIT = "1affb3a094a06f2a250140e8173501b3a6938164"
AGENT_BUNDLE_SCHEMA = "otclient.tibia-re-surveyor.agent-bundle.v1"
COVERAGE_SCHEMA = "otclient.tibia-re-surveyor.coverage.v1"
ALIAS_SCHEMA = "otclient.tibia-re-surveyor.alias-view.v2"
TELEMETRY_SCHEMA = "otclient.tibia-re-surveyor.telemetry.v2"
MISSING_SCHEMA = "otclient.tibia-re-surveyor.missing-readers.v2"
PRIVACY_SCHEMA = "otclient.tibia-re-surveyor.privacy-scan.v1"
PINNED_CLIENT_VERSION = "15.32"
PINNED_CLIENT_SIZE = 52_109_920
PINNED_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
PINNED_TARGET_CONTAINER = "otclient-track-a-kasmvnc"
PINNED_CONTROL_CONTAINER = "otclient-synology-runner"
PINNED_RUNTIME_ID = "track-a-canonical-live"
PINNED_AUTH_LAYOUT_EVIDENCE = {
    "source_object": "tibia::client::TGameClient",
    "auth_controller_object": "tibia::authentication::TAuthenticationProcessController",
    "game_client_vptr_offset": "0x30adce8",
    "game_client_typeinfo_offset": "0x30a7778",
    "auth_controller_vptr_offset": "0x30b5290",
    "auth_controller_typeinfo_offset": "0x30b4410",
    "auth_controller_member_offset": "0x8d0",
    "qstate_private_offset": "0x8",
    "qstate_state_offset": "0xf0",
    "qstate_running_value": 2,
    "representation": "qt_qstatemachine_isRunning_equivalent",
    "semantic_state": "TYPED_AUTH_LIFECYCLE_ONLY",
    "in_game_claimed": False,
    "credentials_retained": False,
    "session_secrets_retained": False,
}
PINNED_PLAYER_LAYOUT_EVIDENCE = {
    "source_object": "tibia::cyclopedia::TCyclopediaMapStorage",
    "source_handler": "onPlayerPositionWasUpdated",
    "source_signal": "playerPositionChanged",
    "cyclopedia_vptr_offset": "0x30c2738",
    "cyclopedia_typeinfo_offset": "0x30c0aa0",
    "qt_metacast_offset": "0xd1eef0",
    "position_handler_offset": "0xd19ef0",
    "position_primary_offsets": ["0x2f0", "0x2f4", "0x2f8"],
    "position_mirror_offsets": ["0x408", "0x40c", "0x410"],
    "representation": "signed_i32_x3_mirrored",
    "semantic_state": "CANDIDATE_PENDING_CAUSAL_E2E",
}
PINNED_ACTION_LAYOUT_EVIDENCE = {
    "type_name": "tibia::game::TPlayerProtocolMessageHandler",
    "mangled_name": "N5tibia4game29TPlayerProtocolMessageHandlerE",
    "vptr_offset": "0x30bf620",
    "typeinfo_offset": "0x30bf298",
    "representation": "exact_rtti_primary_vptr_object_identity",
}
PINNED_ACTION_LAYOUT_EVIDENCE_KEYS = frozenset({
    "type_name", "mangled_name", "vptr_offset", "typeinfo_offset", "representation",
})
PINNED_QT_STATE_MACHINE_FENCE = {
    "library": "libQt6StateMachine.so.6",
    "size": 394_824,
    "sha256": "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8",
}
PINNED_UI_STATIC_EVIDENCE_KEYS = frozenset({
    "state", "type_name", "type_string_count", "clientoptions_literal_count",
})
PINNED_AGENT_GUARDRAILS = {
    "collect_all_runtime_mutation_allowed": False,
    "collector_has_input_path": False,
    "evidence_mentions_are_semantic_proof": False,
    "surveyor_can_promote_canonical_status": False,
}
PINNED_TELEMETRY_GUARDRAILS = {
    "chat_message_contents_retained": False,
    "credentials_retained": False,
    "packet_payloads_retained": False,
    "read_only": True,
    "runtime_mutation_requested": False,
    "semantic_promotion_allowed": False,
    "window_title_values_retained": False,
}
_ALLOWED_REGISTRATION_STATES = frozenset({"LOGIN", "CHARACTER_SELECT", "IN_GAME", "DISCONNECTED", "UNKNOWN"})
_ALLOWED_REMOTE_VIEW_MAPPING = frozenset({"PROVEN", "UNKNOWN"})

MAX_MANIFEST_BYTES = 64 * 1024
MAX_MANIFEST_FILES = 64
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024
MAX_JSON_DEPTH = 128
MAX_JSON_NODES = 100_000
MAX_JSON_INTEGER_DIGITS = 64
_MANIFEST_RE = re.compile(r"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_GENERATED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{6})?\+00:00$")
_SENSITIVE_KEYS = {"password", "passwd", "token", "credential", "secret", "authorization", "cookie", "otp", "2fa"}
_EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}")
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
_SECRET_VALUE_RE = re.compile(
    r'(?i)"(?:password|passwd|secret|token|cookie|credential|otp|2fa)"\s*:\s*"(?!<redacted>|<not-retained>)[^"\s][^"]*"'
)
_ALLOWED_RUNTIME_ACCESS = frozenset({"READ_ONLY_ADMITTED", "READ_ONLY_NOT_ADMITTED", "READ_ONLY_UNAVAILABLE"})

EXPECTED_INTERFACE_FILES = frozenset({
    'aliases/TIBIA-RE-ACTION-PROTOCOL.json',
    'aliases/TIBIA-RE-AUTH-SESSION.json',
    'aliases/TIBIA-RE-CHAT-SOCIAL.json',
    'aliases/TIBIA-RE-COORDINATOR.json',
    'aliases/TIBIA-RE-CREATURE-COMBAT.json',
    'aliases/TIBIA-RE-ECONOMY-PANELS.json',
    'aliases/TIBIA-RE-FEATURES.json',
    'aliases/TIBIA-RE-INVENTORY-CONTAINERS.json',
    'aliases/TIBIA-RE-ITEM-LOOT.json',
    'aliases/TIBIA-RE-PLAYER-STATE.json',
    'aliases/TIBIA-RE-UI-SETTINGS.json',
    'aliases/TIBIA-RE-WORLD-MINIMAP.json',
    'missing-readers.json',
    'privacy-scan.json',
    'summary.md',
    'surveyor/agent_bundle.json',
    'surveyor/coverage.json',
    'surveyor/runtime.json',
    'surveyor/summary.md',
    'telemetry/action-protocol.json',
    'telemetry/auth-session.json',
    'telemetry/chat-social.json',
    'telemetry/creature-combat.json',
    'telemetry/economy-panels.json',
    'telemetry/features.json',
    'telemetry/inventory-containers.json',
    'telemetry/item-loot.json',
    'telemetry/player-state.json',
    'telemetry/ui-settings.json',
    'telemetry/world-minimap.json',
})

PINNED_TELEMETRY_CONTRACTS = {
    "telemetry/action-protocol.json": ("TIBIA-RE-ACTION-PROTOCOL", "action_protocol_typed_reader"),
    "telemetry/auth-session.json": ("TIBIA-RE-AUTH-SESSION", "auth_session_typed_reader"),
    "telemetry/chat-social.json": ("TIBIA-RE-CHAT-SOCIAL", "chat_social_typed_reader"),
    "telemetry/creature-combat.json": ("TIBIA-RE-CREATURE-COMBAT", "creature_combat_typed_reader"),
    "telemetry/economy-panels.json": ("TIBIA-RE-ECONOMY-PANELS", "economy_panels_typed_reader"),
    "telemetry/features.json": ("TIBIA-RE-FEATURES", "features_typed_reader"),
    "telemetry/inventory-containers.json": ("TIBIA-RE-INVENTORY-CONTAINERS", "inventory_containers_typed_reader"),
    "telemetry/item-loot.json": ("TIBIA-RE-ITEM-LOOT", "item_loot_typed_reader"),
    "telemetry/player-state.json": ("TIBIA-RE-PLAYER-STATE", "player_state_typed_reader"),
    "telemetry/ui-settings.json": ("TIBIA-RE-UI-SETTINGS", "ui_settings_typed_reader"),
    "telemetry/world-minimap.json": ("TIBIA-RE-WORLD-MINIMAP", "world_minimap_typed_reader"),
}
PINNED_IMPLEMENTED_TYPED_READERS = frozenset({
    "action_protocol_typed_reader", "auth_session_typed_reader",
    "player_state_typed_reader", "ui_settings_typed_reader",
})

PINNED_ALIAS_CONTRACTS = {
    f"aliases/{alias}.json": (alias, telemetry_path, reader_id)
    for telemetry_path, (alias, reader_id) in PINNED_TELEMETRY_CONTRACTS.items()
}
PINNED_ALIAS_CONTRACTS["aliases/TIBIA-RE-COORDINATOR.json"] = ("TIBIA-RE-COORDINATOR", None, None)

@dataclass(frozen=True)
class SurveyorReadModel:
    runtime_status: RuntimeStatus
    snapshot: GameSnapshot
    capabilities: tuple[Capability, ...]
    readiness: Mapping[str, str]
    provenance: Mapping[str, Any]


def _fail(code: str, message: str) -> None:
    raise ValidationError(code, message)


def _is_plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_producer_visible_window(value: Any) -> bool:
    if not isinstance(value, dict) or set(value) != {"xid", "pid", "title_class"}:
        return False
    xid = value.get("xid")
    pid = value.get("pid")
    return (
        _is_plain_int(xid) and xid > 0
        and (pid is None or (_is_plain_int(pid) and pid > 0))
        and value.get("title_class") in {"CHARACTER_CONTEXT", "TIBIA_WINDOW"}
    )


def _reject_json_constant(_value: str) -> None:
    _fail("SURVEYOR_JSON_INVALID", "Surveyor JSON contains a nonstandard numeric constant")


def _parse_json_int(value: str) -> int:
    if len(value.lstrip("-")) > MAX_JSON_INTEGER_DIGITS:
        _fail("SURVEYOR_JSON_INVALID", "Surveyor JSON integer exceeds the accepted bound")
    try:
        return int(value)
    except ValueError:
        _fail("SURVEYOR_JSON_INVALID", "Surveyor JSON integer is invalid")


def _safe_relative(path_text: str) -> PurePosixPath:
    path = PurePosixPath(path_text)
    if path.is_absolute() or ".." in path.parts or any(part in {"", "."} for part in path.parts):
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor manifest contains an unsafe path")
    return path


def _is_reparse_point(info: os.stat_result) -> bool:
    marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(marker and getattr(info, "st_file_attributes", 0) & marker)


class _WindowsNative:
    FILE_ATTRIBUTE_DIRECTORY = 0x10
    FILE_ATTRIBUTE_REPARSE_POINT = 0x400
    _FILE_INFO_RESTART = 11
    _FILE_INFO_CONTINUE = 10
    _ERROR_NO_MORE_FILES = 18

    def __init__(self) -> None:
        import ctypes
        from ctypes import wintypes

        self.ctypes = ctypes
        self.wintypes = wintypes
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.ntdll = ctypes.WinDLL("ntdll")
        self._configure_structures()
        self._configure_functions()

    def _configure_functions(self) -> None:
        c = self.ctypes
        w = self.wintypes
        self.create_file = self.kernel32.CreateFileW
        self.create_file.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, w.LPVOID,
                                     w.DWORD, w.DWORD, w.HANDLE]
        self.create_file.restype = w.HANDLE
        self.close_handle = self.kernel32.CloseHandle
        self.close_handle.argtypes = [w.HANDLE]
        self.close_handle.restype = w.BOOL
        self.duplicate_handle = self.kernel32.DuplicateHandle
        self.duplicate_handle.argtypes = [w.HANDLE, w.HANDLE, w.HANDLE, c.POINTER(w.HANDLE),
                                          w.DWORD, w.BOOL, w.DWORD]
        self.duplicate_handle.restype = w.BOOL
        self.current_process = self.kernel32.GetCurrentProcess
        self.current_process.restype = w.HANDLE
        self.get_dir_info = self.kernel32.GetFileInformationByHandleEx
        self.get_dir_info.argtypes = [w.HANDLE, c.c_int, w.LPVOID, w.DWORD]
        self.get_dir_info.restype = w.BOOL
        self.nt_create_file = self.ntdll.NtCreateFile
        self.nt_create_file.argtypes = [c.POINTER(w.HANDLE), w.DWORD, c.POINTER(self.ObjectAttributes),
                                        c.POINTER(self.IoStatusBlock), w.LPVOID, w.DWORD, w.DWORD,
                                        w.ULONG, w.ULONG, w.LPVOID, w.ULONG]
        self.nt_create_file.restype = c.c_long

    def _configure_structures(self) -> None:
        c = self.ctypes
        w = self.wintypes

        class UnicodeString(c.Structure):
            _fields_ = [("Length", w.USHORT), ("MaximumLength", w.USHORT), ("Buffer", w.LPWSTR)]  # noqa: RUF012

        class ObjectAttributes(c.Structure):
            _fields_ = [("Length", w.ULONG), ("RootDirectory", w.HANDLE),  # noqa: RUF012
                        ("ObjectName", c.POINTER(UnicodeString)), ("Attributes", w.ULONG),
                        ("SecurityDescriptor", w.LPVOID), ("SecurityQualityOfService", w.LPVOID)]
        class IoStatusUnion(c.Union):
            _fields_ = [("Status", c.c_long), ("Pointer", w.LPVOID)]  # noqa: RUF012

        class IoStatusBlock(c.Structure):
            _fields_ = [("u", IoStatusUnion), ("Information", c.c_size_t)]  # noqa: RUF012

        class DirectoryEntryHeader(c.Structure):
            _fields_ = [("NextEntryOffset", w.DWORD), ("FileIndex", w.DWORD)]  # noqa: RUF012
            _fields_ += [(name, c.c_longlong) for name in
                         ("CreationTime", "LastAccessTime", "LastWriteTime", "ChangeTime",
                          "EndOfFile", "AllocationSize")]
            _fields_ += [("FileAttributes", w.DWORD), ("FileNameLength", w.DWORD),
                         ("EaSize", w.DWORD), ("ShortNameLength", c.c_byte),
                         ("ShortName", c.c_wchar * 12), ("FileId", c.c_longlong)]

        self.UnicodeString = UnicodeString
        self.ObjectAttributes = ObjectAttributes
        self.IoStatusBlock = IoStatusBlock
        self.DirectoryEntryHeader = DirectoryEntryHeader

    def close(self, handle: int) -> None:
        if handle:
            self.close_handle(handle)
    def _fstat(self, handle: int) -> os.stat_result:
        import msvcrt

        c = self.ctypes
        w = self.wintypes
        duplicate = w.HANDLE()
        process = self.current_process()
        if not self.duplicate_handle(process, handle, process, c.byref(duplicate), 0, False, 2):
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows handle could not be duplicated")
        try:
            fd = msvcrt.open_osfhandle(int(duplicate.value), os.O_RDONLY)
        except OSError:
            self.close(int(duplicate.value))
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows handle could not be inspected")
        try:
            return os.fstat(fd)
        finally:
            os.close(fd)

    def open_root(self, path: Path) -> int:
        desired = 0x0001 | 0x0080 | 0x00100000
        flags = 0x02000000 | 0x00200000
        handle = self.create_file(str(path), desired, 0x7, None, 3, flags, None)
        if int(handle) == self.ctypes.c_void_p(-1).value:
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root could not be opened safely")
        return int(handle)
    def open_relative(self, parent: int, name: str, *, directory: bool) -> int:
        c = self.ctypes
        w = self.wintypes
        encoded_length = len(name.encode("utf-16-le"))
        buffer = c.create_unicode_buffer(name)
        unicode_name = self.UnicodeString(encoded_length, encoded_length + 2, c.cast(buffer, w.LPWSTR))
        attrs = self.ObjectAttributes(c.sizeof(self.ObjectAttributes), parent, c.pointer(unicode_name),
                                      0x40, None, None)
        io_status = self.IoStatusBlock()
        handle = w.HANDLE()
        desired = 0x0001 | 0x0080 | 0x00100000
        options = (0x00000001 if directory else 0x00000040) | 0x00000020 | 0x00200000
        status = self.nt_create_file(c.byref(handle), desired, c.byref(attrs), c.byref(io_status),
                                     None, 0, 0x7, 1, options, None, 0)
        unsigned = c.c_ulong(status).value
        if status < 0:
            if unsigned in {0xC000000F, 0xC0000034, 0xC000003A}:
                raise FileNotFoundError(name)
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows path could not be opened safely")
        value = int(handle.value)
        try:
            info = self._fstat(value)
        except Exception:
            self.close(value)
            raise
        if _is_reparse_point(info) or (directory and not stat.S_ISDIR(info.st_mode)):
            self.close(value)
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle path traverses an unsafe directory")
        if not directory and not stat.S_ISREG(info.st_mode):
            self.close(value)
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle path is not a regular file")
        return value

    def read_file(self, handle: int, *, max_bytes: int,
                  too_large_code: str, too_large_message: str) -> bytes:
        import msvcrt

        c = self.ctypes
        w = self.wintypes
        duplicate = w.HANDLE()
        process = self.current_process()
        if not self.duplicate_handle(process, handle, process, c.byref(duplicate), 0, False, 2):
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows file handle could not be duplicated")
        try:
            fd = msvcrt.open_osfhandle(int(duplicate.value), os.O_RDONLY | getattr(os, "O_BINARY", 0))
        except OSError:
            self.close(int(duplicate.value))
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows file handle could not be inspected")
        try:
            opened = os.fstat(fd)
            if _is_reparse_point(opened) or not stat.S_ISREG(opened.st_mode):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle path is not a regular file")
            if opened.st_size > max_bytes:
                _fail(too_large_code, too_large_message)
            chunks: list[bytes] = []
            remaining = max_bytes + 1
            while remaining:
                chunk = os.read(fd, min(64 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if len(data) > max_bytes:
                _fail(too_large_code, too_large_message)
            return data
        finally:
            os.close(fd)

    def list_directory(self, handle: int) -> list[tuple[str, int]]:
        c = self.ctypes
        results: list[tuple[str, int]] = []
        info_class = self._FILE_INFO_RESTART
        max_entries = MAX_MANIFEST_FILES * 2
        page_count = 0
        while True:
            page_count += 1
            if page_count > 4:
                _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor Windows directory enumeration exceeds the accepted bound")
            buffer = c.create_string_buffer(64 * 1024)
            c.set_last_error(0)
            ok = self.get_dir_info(handle, info_class, buffer, len(buffer))
            if not ok:
                if c.get_last_error() == self._ERROR_NO_MORE_FILES:
                    return results
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory could not be enumerated safely")
            self._parse_directory_buffer(buffer.raw, results, max_entries)
            info_class = self._FILE_INFO_CONTINUE
    def _parse_directory_buffer(self, raw: bytes, results: list[tuple[str, int]], max_entries: int) -> None:
        c = self.ctypes
        header_size = c.sizeof(self.DirectoryEntryHeader)
        offset = 0
        while True:
            if offset + header_size > len(raw):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory entry is malformed")
            header = self.DirectoryEntryHeader.from_buffer_copy(raw[offset:offset + header_size])
            if header.FileNameLength % 2 or offset + header_size + header.FileNameLength > len(raw):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory name is malformed")
            start = offset + header_size
            try:
                name = raw[start:start + header.FileNameLength].decode("utf-16-le", "strict")
            except UnicodeDecodeError:
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory name is invalid")
            if name not in {".", ".."}:
                if not name or "/" in name or "\\" in name:
                    _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory name is unsafe")
                results.append((name, int(header.FileAttributes)))
                if len(results) > max_entries:
                    _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor bundle contains too many entries")
            if not header.NextEntryOffset:
                return
            if header.NextEntryOffset < header_size or offset + header.NextEntryOffset >= len(raw):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows directory entry offset is invalid")
            offset += header.NextEntryOffset


_WINDOWS_NATIVE = _WindowsNative() if os.name == "nt" else None


@dataclass(frozen=True)
class _BundleRoot:
    path: Path
    identity: tuple[int, int]
    fd: int | None
    win_handle: int | None = None


def _open_bundle_root(path: Path) -> _BundleRoot:
    if path.is_symlink():
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root cannot be a symlink")
    try:
        before = path.stat(follow_symlinks=False)
    except FileNotFoundError:
        _fail("SURVEYOR_BUNDLE_MISSING", "Surveyor bundle root is missing")
    except OSError:
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root cannot be safely inspected")
    if _is_reparse_point(before):
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root cannot be a reparse point")
    if not stat.S_ISDIR(before.st_mode):
        _fail("SURVEYOR_BUNDLE_MISSING", "Surveyor bundle root is missing")
    identity = (before.st_dev, before.st_ino)
    if os.name == "nt":
        if _WINDOWS_NATIVE is None:
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor Windows anchored traversal is unavailable")
        handle = _WINDOWS_NATIVE.open_root(path)
        try:
            opened = _WINDOWS_NATIVE._fstat(handle)
        except Exception:
            _WINDOWS_NATIVE.close(handle)
            raise
        if _is_reparse_point(opened) or not stat.S_ISDIR(opened.st_mode) or (opened.st_dev, opened.st_ino) != identity:
            _WINDOWS_NATIVE.close(handle)
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root changed during validation")
        return _BundleRoot(path=path, identity=identity, fd=None, win_handle=handle)
    if not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor anchored traversal is unavailable")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root could not be opened safely")
    opened = os.fstat(fd)
    if not stat.S_ISDIR(opened.st_mode) or (opened.st_dev, opened.st_ino) != identity:
        os.close(fd)
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle root changed during validation")
    return _BundleRoot(path=path, identity=identity, fd=fd)


def _close_bundle_root(root: _BundleRoot) -> None:
    if root.fd is not None:
        os.close(root.fd)
    if root.win_handle is not None:
        assert _WINDOWS_NATIVE is not None
        _WINDOWS_NATIVE.close(root.win_handle)


def _read_bounded_bundle_file(
    root: _BundleRoot,
    relative: str,
    *,
    max_bytes: int,
    missing_code: str,
    missing_message: str,
    too_large_code: str,
    too_large_message: str,
) -> bytes:
    relative_path = _safe_relative(relative)
    parts = relative_path.parts
    if root.win_handle is not None:
        assert _WINDOWS_NATIVE is not None
        opened_parents: list[int] = []
        current_handle = root.win_handle
        try:
            for part in parts[:-1]:
                try:
                    current_handle = _WINDOWS_NATIVE.open_relative(current_handle, part, directory=True)
                except FileNotFoundError:
                    _fail(missing_code, missing_message)
                opened_parents.append(current_handle)
            try:
                leaf = _WINDOWS_NATIVE.open_relative(current_handle, parts[-1], directory=False)
            except FileNotFoundError:
                _fail(missing_code, missing_message)
            try:
                return _WINDOWS_NATIVE.read_file(leaf, max_bytes=max_bytes,
                                                 too_large_code=too_large_code,
                                                 too_large_message=too_large_message)
            finally:
                _WINDOWS_NATIVE.close(leaf)
        finally:
            for handle in reversed(opened_parents):
                _WINDOWS_NATIVE.close(handle)
    if root.fd is None:
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor anchored traversal is unavailable")
    current = os.dup(root.fd)
    try:
        dir_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        for part in parts[:-1]:
            try:
                next_fd = os.open(part, dir_flags, dir_fd=current)
            except FileNotFoundError:
                _fail(missing_code, missing_message)
            except OSError:
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle path could not be opened safely")
            os.close(current)
            current = next_fd
        flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NONBLOCK", 0)
        try:
            fd = os.open(parts[-1], flags, dir_fd=current)
        except FileNotFoundError:
            _fail(missing_code, missing_message)
        except OSError:
            _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle file could not be opened safely")
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle path is not a regular file")
            if opened.st_size > max_bytes:
                _fail(too_large_code, too_large_message)
            chunks: list[bytes] = []
            remaining = max_bytes + 1
            while remaining:
                chunk = os.read(fd, min(64 * 1024, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if len(data) > max_bytes:
                _fail(too_large_code, too_large_message)
            return data
        finally:
            os.close(fd)
    finally:
        os.close(current)


def _parse_manifest(root: _BundleRoot) -> dict[str, str]:
    raw = _read_bounded_bundle_file(
        root,
        "manifest.sha256",
        max_bytes=MAX_MANIFEST_BYTES,
        missing_code="SURVEYOR_MANIFEST_MISSING_FILE",
        missing_message="Surveyor manifest is missing",
        too_large_code="SURVEYOR_MANIFEST_TOO_LARGE",
        too_large_message="Surveyor manifest exceeds the accepted bound",
    )
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError:
        _fail("SURVEYOR_MANIFEST_INVALID", "Surveyor manifest is not valid UTF-8")
    if len(lines) > MAX_MANIFEST_FILES:
        _fail("SURVEYOR_MANIFEST_TOO_LARGE", "Surveyor manifest contains too many files")
    entries: dict[str, str] = {}
    for line in lines:
        match = _MANIFEST_RE.fullmatch(line)
        if match is None:
            candidate = line.split("  ", 1)[-1] if "  " in line else ""
            if candidate and (candidate.startswith("/") or ".." in PurePosixPath(candidate).parts):
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor manifest contains an unsafe path")
            _fail("SURVEYOR_MANIFEST_INVALID", "Surveyor manifest has an invalid entry")
        digest, relative = match.groups()
        _safe_relative(relative)
        if relative in entries:
            _fail("SURVEYOR_MANIFEST_DUPLICATE_PATH", "Surveyor manifest repeats a path")
        entries[relative] = digest
    return entries


def _verify_files(root: _BundleRoot, entries: Mapping[str, str]) -> dict[str, bytes]:
    expected = set(entries)
    expected_dirs = {parent.as_posix() for relative in expected for parent in PurePosixPath(relative).parents if parent.as_posix() != "."}
    if root.win_handle is not None:
        assert _WINDOWS_NATIVE is not None

        def verify_windows(directory_handle: int, prefix: str = "") -> None:
            for name, attributes in _WINDOWS_NATIVE.list_directory(directory_handle):
                relative = f"{prefix}/{name}" if prefix else name
                is_reparse = bool(attributes & _WINDOWS_NATIVE.FILE_ATTRIBUTE_REPARSE_POINT)
                is_directory = bool(attributes & _WINDOWS_NATIVE.FILE_ATTRIBUTE_DIRECTORY)
                if relative == "manifest.sha256":
                    if is_reparse or is_directory:
                        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor manifest path is unsafe")
                    continue
                if is_reparse:
                    _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle contains a reparse point")
                if is_directory:
                    if relative not in expected_dirs:
                        _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor bundle contains an unmanifested directory")
                    try:
                        child = _WINDOWS_NATIVE.open_relative(directory_handle, name, directory=True)
                    except FileNotFoundError:
                        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle directory changed during validation")
                    try:
                        verify_windows(child, relative)
                    finally:
                        _WINDOWS_NATIVE.close(child)
                elif relative not in expected:
                    _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor bundle contains an unmanifested file")

        verify_windows(root.win_handle)
    elif root.fd is None:
        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor anchored traversal is unavailable")
    else:
        dir_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        def verify_fd(directory_fd: int, prefix: str = "") -> None:
            try:
                names = os.listdir(directory_fd)
            except OSError:
                _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle directory could not be listed safely")
            for name in names:
                relative = f"{prefix}/{name}" if prefix else name
                if relative == "manifest.sha256":
                    continue
                try:
                    info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                except OSError:
                    _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle entry could not be inspected safely")
                if stat.S_ISLNK(info.st_mode):
                    _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle contains a symlink")
                if stat.S_ISDIR(info.st_mode):
                    if relative not in expected_dirs:
                        _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor bundle contains an unmanifested directory")
                    try:
                        child_fd = os.open(name, dir_flags, dir_fd=directory_fd)
                    except OSError:
                        _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle directory could not be opened safely")
                    try:
                        verify_fd(child_fd, relative)
                    finally:
                        os.close(child_fd)
                elif stat.S_ISREG(info.st_mode):
                    if relative not in expected:
                        _fail("SURVEYOR_MANIFEST_FILE_SET_MISMATCH", "Surveyor bundle contains an unmanifested file")
                else:
                    _fail("SURVEYOR_MANIFEST_UNSAFE_PATH", "Surveyor bundle contains an unsupported filesystem entry")
        verify_fd(root.fd)
    total = 0
    payloads: dict[str, bytes] = {}
    for relative, digest in entries.items():
        data = _read_bounded_bundle_file(
            root, relative,
            max_bytes=MAX_FILE_BYTES,
            missing_code="SURVEYOR_MANIFEST_MISSING_FILE",
            missing_message="Surveyor manifest references a missing file",
            too_large_code="SURVEYOR_FILE_TOO_LARGE",
            too_large_message="Surveyor bundle file exceeds the accepted bound",
        )
        total += len(data)
        if total > MAX_TOTAL_BYTES:
            _fail("SURVEYOR_BUNDLE_TOO_LARGE", "Surveyor bundle exceeds the accepted total bound")
        if hashlib.sha256(data).hexdigest() != digest:
            _fail("SURVEYOR_MANIFEST_DIGEST_MISMATCH", "Surveyor bundle digest verification failed")
        payloads[relative] = data
    return payloads

def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _fail("SURVEYOR_JSON_DUPLICATE_KEY", "Surveyor JSON contains a duplicate key")
        result[key] = value
    return result

def _scan_text_payload_privacy(payloads: Mapping[str, bytes]) -> None:
    for relative, data in payloads.items():
        if Path(relative).suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        text = data.decode("utf-8", "replace")
        if (
            _EMAIL_RE.search(text)
            or _BEARER_RE.search(text)
            or _JWT_RE.search(text)
            or _SECRET_VALUE_RE.search(text)
        ):
            _fail("SURVEYOR_PRIVACY_RISK", "Surveyor text payload contains sensitive material")


def _load_json_documents(payloads: Mapping[str, bytes]) -> dict[str, Any]:
    docs: dict[str, Any] = {}
    for relative, data in payloads.items():
        if not relative.endswith(".json"):
            continue
        try:
            docs[relative] = json.loads(
                data.decode("utf-8", "strict"),
                object_pairs_hook=_object_pairs,
                parse_constant=_reject_json_constant,
                parse_int=_parse_json_int,
            )
        except ValidationError:
            raise
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError):
            _fail("SURVEYOR_JSON_INVALID", "Surveyor JSON is malformed")
    return docs


def _walk_json(value: Any):
    stack: list[tuple[Any, int]] = [(value, 0)]
    seen = 0
    while stack:
        node, depth = stack.pop()
        seen += 1
        if depth > MAX_JSON_DEPTH or seen > MAX_JSON_NODES:
            _fail("SURVEYOR_JSON_INVALID", "Surveyor JSON structure exceeds the accepted bound")
        yield node
        if isinstance(node, dict):
            stack.extend((child, depth + 1) for child in node.values())
        elif isinstance(node, list):
            stack.extend((child, depth + 1) for child in node)


def _contains_sensitive_key(value: Any) -> bool:
    for node in _walk_json(value):
        if isinstance(node, dict) and any(str(key).lower() in _SENSITIVE_KEYS for key in node):
            return True
    return False


def _contains_sensitive_value(value: Any) -> bool:
    for node in _walk_json(value):
        if isinstance(node, str) and (
            _EMAIL_RE.search(node)
            or _BEARER_RE.search(node)
            or _JWT_RE.search(node)
            or _SECRET_VALUE_RE.search(node)
        ):
            return True
    return False


def _contains_invalid_semantic_promotion(value: Any) -> bool:
    for node in _walk_json(value):
        if isinstance(node, dict) and "semantic_promotion_allowed" in node and node["semantic_promotion_allowed"] is not False:
            return True
    return False

def _require_schema(doc: Any, expected: str) -> None:
    if not isinstance(doc, dict) or doc.get("schema") != expected:
        _fail("SURVEYOR_SCHEMA_INCOMPATIBLE", "Surveyor schema is not the accepted version")

def _validate_documents(docs: Mapping[str, Any]) -> None:
    _require_schema(docs.get("surveyor/agent_bundle.json"), AGENT_BUNDLE_SCHEMA)
    _require_schema(docs.get("surveyor/coverage.json"), COVERAGE_SCHEMA)
    _require_schema(docs.get("missing-readers.json"), MISSING_SCHEMA)
    privacy = docs.get("privacy-scan.json")
    _require_schema(privacy, PRIVACY_SCHEMA)
    if privacy.get("result") != "PASS" or privacy.get("findings"):
        _fail("SURVEYOR_PRIVACY_RISK", "Surveyor privacy scan did not pass")
    agent = docs.get("surveyor/agent_bundle.json")
    if not isinstance(agent, dict) or agent.get("guardrails") != PINNED_AGENT_GUARDRAILS:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor producer guardrails do not match the pinned contract")
    for relative, doc in docs.items():
        if relative.startswith("aliases/"):
            _require_schema(doc, ALIAS_SCHEMA)
        elif relative.startswith("telemetry/"):
            _require_schema(doc, TELEMETRY_SCHEMA)
            if not isinstance(doc, dict) or doc.get("guardrails") != PINNED_TELEMETRY_GUARDRAILS:
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor telemetry guardrails do not match the pinned contract")
    for relative, (alias, telemetry_path, reader_id) in PINNED_ALIAS_CONTRACTS.items():
        doc = docs.get(relative)
        expected_missing = None if reader_id in PINNED_IMPLEMENTED_TYPED_READERS else reader_id
        if (
            not isinstance(doc, dict)
            or doc.get("alias") != alias
            or doc.get("telemetry_file") != telemetry_path
            or doc.get("missing_reader") != expected_missing
        ):
            _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor alias view does not match the pinned producer contract")
    for relative, (alias, reader_id) in PINNED_TELEMETRY_CONTRACTS.items():
        doc = docs.get(relative)
        states = doc.get("source_states") if isinstance(doc, dict) and isinstance(doc.get("source_states"), dict) else {}
        typed = states.get("subsystem_typed_reader") if isinstance(states.get("subsystem_typed_reader"), dict) else None
        if not isinstance(doc, dict) or doc.get("alias") != alias or typed is None or typed.get("source") != reader_id:
            _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor telemetry does not match the pinned producer contract")
        if reader_id not in PINNED_IMPLEMENTED_TYPED_READERS:
            expected_unavailable = {
                "state": "UNAVAILABLE", "evidence_level": "UNKNOWN",
                "source": reader_id, "reason": "NO_TYPED_READER_IMPLEMENTED",
            }
            if typed != expected_unavailable:
                _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor telemetry advertises an unimplemented typed reader")
    if any(_contains_sensitive_key(doc) or _contains_sensitive_value(doc) for doc in docs.values()):
        _fail("SURVEYOR_PRIVACY_RISK", "Surveyor bundle contains sensitive material")
    if any(_contains_invalid_semantic_promotion(doc) for doc in docs.values()):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor semantic promotion evidence is not exactly false")


def _expected_runtime_provenance(agent: Mapping[str, Any]) -> dict[str, Any]:
    runtime = agent.get("runtime")
    if not isinstance(runtime, dict):
        return {"client_sha256": None, "runtime_id": None, "registration_generation": None, "lease_generation": None}
    processes = runtime.get("processes")
    process = processes[0] if isinstance(processes, list) and len(processes) == 1 and isinstance(processes[0], dict) else {}
    control = runtime.get("canonical_control") if isinstance(runtime.get("canonical_control"), dict) else {}
    registration = control.get("registration") if isinstance(control.get("registration"), dict) else {}
    lease = control.get("lease") if isinstance(control.get("lease"), dict) else {}
    return {
        "client_sha256": process.get("client_sha256"),
        "runtime_id": registration.get("runtime_id"),
        "registration_generation": registration.get("registration_generation"),
        "lease_generation": lease.get("generation"),
    }




def _project_pinned_runtime_identity(runtime: Any) -> dict[str, Any]:
    if not isinstance(runtime, dict):
        return {"state": "UNKNOWN", "evidence_level": "UNKNOWN", "value": None, "source": "surveyor.runtime"}
    processes = runtime.get("processes") if isinstance(runtime.get("processes"), list) else []
    process = processes[0] if len(processes) == 1 and isinstance(processes[0], dict) else {}
    control = runtime.get("canonical_control") if isinstance(runtime.get("canonical_control"), dict) else {}
    registration = control.get("registration") if isinstance(control.get("registration"), dict) else {}
    lease = control.get("lease") if isinstance(control.get("lease"), dict) else {}
    fence = runtime.get("exact_current_fence") if isinstance(runtime.get("exact_current_fence"), dict) else {}
    value = {
        "observed_at_epoch": runtime.get("observed_at_epoch"),
        "target_container": runtime.get("target_container"),
        "control_container": runtime.get("control_container"),
        "display": runtime.get("display"),
        "target_running": runtime.get("target_running"),
        "runtime_namespace_scope": runtime.get("runtime_namespace_scope"),
        "external_containers_scanned": runtime.get("external_containers_scanned"),
        "target_process_count": runtime.get("target_process_count"),
        "target_uniqueness_scope": runtime.get("target_uniqueness_scope"),
        "target_uniqueness": runtime.get("target_uniqueness"),
        "runtime_access": runtime.get("runtime_access"),
        "exact_current_fence": {
            "version": fence.get("version"), "size": fence.get("size"),
            "sha256": fence.get("sha256"), "match": fence.get("match"),
        },
        "process": {
            "pid": process.get("pid"), "process_start_ticks": process.get("process_start_ticks"),
            "exe_basename": process.get("exe_basename"), "client_size": process.get("client_size"),
            "client_sha256": process.get("client_sha256"), "exact_fence_match": process.get("exact_fence_match"),
        },
        "canonical_control": {
            "registration_present": control.get("registration_present"),
            "registration_generation": registration.get("registration_generation"),
            "runtime_id": registration.get("runtime_id"),
            "registered_state": registration.get("state"),
            "lease_present": control.get("lease_present"),
            "lease_generation": lease.get("generation"),
            "lease_status": lease.get("status"),
            "lease_expired": control.get("lease_expired"),
        },
        "visible_tibia_window_count": len(runtime.get("visible_tibia_windows") or []),
        "window_title_values_retained": False,
    }
    return {
        "state": "AVAILABLE" if runtime.get("runtime_access") == "READ_ONLY_ADMITTED" else "OBSERVED_NOT_ADMITTED",
        "evidence_level": "PROVEN", "value": value, "source": "surveyor.runtime",
    }


def _validate_admitted_runtime_contract(runtime: Any) -> None:
    if not isinstance(runtime, dict) or runtime.get("runtime_access") != "READ_ONLY_ADMITTED":
        return
    processes = runtime.get("processes") if isinstance(runtime.get("processes"), list) else []
    if len(processes) != 1 or not isinstance(processes[0], dict):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted runtime does not contain one process")
    process = processes[0]
    fence = runtime.get("exact_current_fence") if isinstance(runtime.get("exact_current_fence"), dict) else {}
    control = runtime.get("canonical_control") if isinstance(runtime.get("canonical_control"), dict) else {}
    registration = control.get("registration") if isinstance(control.get("registration"), dict) else {}
    lease = control.get("lease") if isinstance(control.get("lease"), dict) else {}
    windows = runtime.get("visible_tibia_windows") if isinstance(runtime.get("visible_tibia_windows"), list) else []
    observed_at = runtime.get("observed_at_epoch")
    if runtime.get("target_container") != PINNED_TARGET_CONTAINER or runtime.get("control_container") != PINNED_CONTROL_CONTAINER:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted runtime container identity is not pinned")
    if (
        runtime.get("target_running") is not True
        or control.get("registration_present") is not True
        or control.get("lease_present") is not True
        or runtime.get("runtime_namespace_scope") != "DECLARED_TARGET_ONLY"
        or runtime.get("external_containers_scanned") is not False
        or not _is_plain_int(runtime.get("target_process_count"))
        or runtime.get("target_process_count") != 1
        or runtime.get("target_uniqueness_scope") != "DECLARED_RUNTIME_NAMESPACE"
        or runtime.get("target_uniqueness") != "PROVEN"
        or not _is_plain_int(observed_at)
        or observed_at < 0
    ):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted runtime scope or uniqueness evidence is inconsistent")
    if (
        fence.get("version") != PINNED_CLIENT_VERSION
        or fence.get("size") != PINNED_CLIENT_SIZE
        or fence.get("sha256") != PINNED_CLIENT_SHA256
        or fence.get("match") is not True
    ):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor executable fence is not the pinned accepted client")
    pid = process.get("pid")
    start_ticks = process.get("process_start_ticks")
    if (
        process.get("exe_basename") != "client"
        or process.get("client_size") != PINNED_CLIENT_SIZE
        or process.get("client_sha256") != PINNED_CLIENT_SHA256
        or process.get("exact_fence_match") is not True
        or not _is_plain_int(pid) or pid <= 0
        or not _is_plain_int(start_ticks) or start_ticks <= 0
    ):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor observed process is not the pinned accepted client")
    if (
        not windows
        or any(not _is_producer_visible_window(window) for window in windows)
        or not any(window.get("pid") == pid for window in windows)
    ):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted runtime lacks complete matching visible window evidence")
    boot_id = registration.get("boot_id_sha256")
    registration_generation = registration.get("registration_generation")
    lease_generation = registration.get("lease_generation")
    display = runtime.get("display")
    registration_matches = (
        registration.get("schema_version") == 1
        and registration.get("runtime_id") == PINNED_RUNTIME_ID
        and _is_plain_int(registration_generation) and registration_generation > 0
        and _is_plain_int(lease_generation) and lease_generation > 0
        and registration.get("pid") == pid
        and registration.get("process_start_ticks") == start_ticks
        and registration.get("client_version") == PINNED_CLIENT_VERSION
        and registration.get("client_size") == PINNED_CLIENT_SIZE
        and registration.get("client_sha256") == PINNED_CLIENT_SHA256
        and isinstance(display, str) and re.fullmatch(r":\d+", display) is not None
        and registration.get("display") == display
        and isinstance(boot_id, str) and re.fullmatch(r"[0-9a-f]{64}", boot_id) is not None
        and registration.get("remote_view_mapping") in _ALLOWED_REMOTE_VIEW_MAPPING
        and registration.get("state") in _ALLOWED_REGISTRATION_STATES
    )
    if not registration_matches:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor registration does not match the observed pinned runtime")
    lease_generation_current = lease.get("generation")
    acquired_at = lease.get("acquired_at")
    renewed_at = lease.get("renewed_at")
    expires_at = lease.get("expires_at")
    if (
        lease.get("schema_version") != 1
        or lease.get("runtime_id") != PINNED_RUNTIME_ID
        or lease.get("status") != "active"
        or not _is_plain_int(lease_generation_current)
        or lease_generation_current <= 0
        or lease_generation != lease_generation_current
        or not _is_plain_int(acquired_at)
        or acquired_at < 0
        or not _is_plain_int(renewed_at)
        or renewed_at < acquired_at
        or not _is_plain_int(expires_at)
        or expires_at <= renewed_at
        or expires_at <= observed_at
        or control.get("lease_expired") is not False
    ):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor registration and lease identity are not current")


def _validate_available_typed_reader(reader_id: str, value: Any) -> None:
    if not isinstance(value, dict) or value.get("state") != "AVAILABLE" or value.get("reader_id") != reader_id:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor typed-reader payload is not AVAILABLE for its pinned reader")
    if value.get("semantic_promotion_allowed") is not False:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor typed-reader semantic promotion is not disabled")
    if reader_id == "player_state_typed_reader":
        expected_keys = {
            "state", "reader_id", "position", "object_count", "position_mirror_consistent",
            "process_memory_access", "semantic_state", "layout_evidence",
            "semantic_promotion_allowed",
        }
        position = value.get("position") if isinstance(value.get("position"), dict) else {}
        x, y, z = position.get("x"), position.get("y"), position.get("z")
        if (
            set(value) != expected_keys or set(position) != {"x", "y", "z"}
            or not _is_plain_int(x) or not 1 <= x <= 65535
            or not _is_plain_int(y) or not 1 <= y <= 65535
            or not _is_plain_int(z) or not 0 <= z <= 15
            or value.get("object_count") != 1 or isinstance(value.get("object_count"), bool)
            or value.get("position_mirror_consistent") is not True
            or value.get("process_memory_access") != "read_only"
            or value.get("semantic_state") != "CANDIDATE_PENDING_CAUSAL_E2E"
            or value.get("layout_evidence") != PINNED_PLAYER_LAYOUT_EVIDENCE
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor player-state payload violates the pinned reader contract")
        return
    if reader_id == "action_protocol_typed_reader":
        expected_keys = {
            "state", "reader_id", "type_name", "object_count", "typed_object_identity",
            "process_memory_access", "layout_evidence", "semantic_state",
            "protocol_message_handler_present", "action_to_protocol_connection_claimed",
            "serialized_message_semantics_claimed", "protocol_opcodes_claimed",
            "packet_payloads_retained", "in_game_claimed", "credentials_retained",
            "session_secrets_retained", "semantic_promotion_allowed",
        }
        layout = value.get("layout_evidence")
        if (
            set(value) != expected_keys
            or value.get("type_name") != "tibia::game::TPlayerProtocolMessageHandler"
            or value.get("object_count") != 1 or isinstance(value.get("object_count"), bool)
            or value.get("typed_object_identity") != "PROVEN"
            or value.get("process_memory_access") != "read_only"
            or value.get("semantic_state") != "TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY"
            or value.get("protocol_message_handler_present") is not True
            or value.get("action_to_protocol_connection_claimed") is not False
            or value.get("serialized_message_semantics_claimed") is not False
            or value.get("protocol_opcodes_claimed") is not False
            or value.get("packet_payloads_retained") is not False
            or value.get("in_game_claimed") is not False
            or value.get("credentials_retained") is not False
            or value.get("session_secrets_retained") is not False
            or not isinstance(layout, dict)
            or set(layout) != PINNED_ACTION_LAYOUT_EVIDENCE_KEYS
            or any(layout.get(key) != expected for key, expected in PINNED_ACTION_LAYOUT_EVIDENCE.items())
            or re.fullmatch(r"0x[0-9a-f]+", str(layout.get("vptr_offset"))) is None
            or re.fullmatch(r"0x[0-9a-f]+", str(layout.get("typeinfo_offset"))) is None
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor action-protocol payload violates the pinned reader contract")
        return
    if reader_id == "auth_session_typed_reader":
        expected_keys = {
            "state", "reader_id", "game_client_object_count",
            "authentication_process_object_count", "authentication_state_machine_running",
            "process_memory_access", "semantic_state", "in_game_claimed",
            "credentials_retained", "session_secrets_retained", "layout_evidence",
            "qt_state_machine_fence", "semantic_promotion_allowed",
        }
        if (
            set(value) != expected_keys
            or value.get("game_client_object_count") != 1
            or isinstance(value.get("game_client_object_count"), bool)
            or value.get("authentication_process_object_count") != 1
            or isinstance(value.get("authentication_process_object_count"), bool)
            or not isinstance(value.get("authentication_state_machine_running"), bool)
            or value.get("process_memory_access") != "read_only"
            or value.get("semantic_state") != "TYPED_AUTH_LIFECYCLE_ONLY"
            or value.get("in_game_claimed") is not False
            or value.get("credentials_retained") is not False
            or value.get("session_secrets_retained") is not False
            or value.get("layout_evidence") != PINNED_AUTH_LAYOUT_EVIDENCE
            or value.get("qt_state_machine_fence") != PINNED_QT_STATE_MACHINE_FENCE
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor auth-session payload violates the pinned reader contract")
        return
    if reader_id == "ui_settings_typed_reader":
        expected_keys = {
            "state", "reader_id", "master_volume", "master_volume_old",
            "persistence_relative_path", "filesystem_access", "process_memory_access",
            "semantic_state", "settings_model_type", "settings_model_type_present",
            "persistence_fields", "master_volume_persistence_field_semantics",
            "live_ui_application_state_claimed", "all_settings_model_claimed",
            "qsettings_linkage_claimed", "client_options_to_file_linkage_claimed",
            "credentials_retained", "session_secrets_retained", "semantic_promotion_allowed",
            "static_evidence",
        }
        master = value.get("master_volume")
        master_old = value.get("master_volume_old")
        static = value.get("static_evidence")
        if (
            set(value) != expected_keys
            or not _is_plain_int(master) or not 0 <= master <= 100
            or not _is_plain_int(master_old) or not 0 <= master_old <= 100
            or value.get("persistence_relative_path") != "conf/clientoptions.json"
            or value.get("filesystem_access") != "read_only"
            or value.get("process_memory_access") != "not_used"
            or value.get("semantic_state") != "TYPED_UI_SETTINGS_MASTER_VOLUME_FILE_READ_ONLY"
            or value.get("settings_model_type") != "tibia::config::TClientOptions"
            or value.get("settings_model_type_present") is not True
            or value.get("persistence_fields") != [
                "options.soundMasterVolume", "options.soundMasterVolumeOld",
            ]
            or value.get("master_volume_persistence_field_semantics")
            != "PROVEN_ON_EXACT_BUILD_BY_PRIOR_REVERSIBLE_CAUSAL_EVIDENCE"
            or value.get("live_ui_application_state_claimed") is not False
            or value.get("all_settings_model_claimed") is not False
            or value.get("qsettings_linkage_claimed") is not False
            or value.get("client_options_to_file_linkage_claimed") is not False
            or value.get("credentials_retained") is not False
            or value.get("session_secrets_retained") is not False
            or not isinstance(static, dict)
            or set(static) != PINNED_UI_STATIC_EVIDENCE_KEYS
            or static.get("state") != "AVAILABLE"
            or static.get("type_name") != "tibia::config::TClientOptions"
            or not _is_plain_int(static.get("type_string_count"))
            or static["type_string_count"] < 1
            or static.get("clientoptions_literal_count") != 1
            or isinstance(static.get("clientoptions_literal_count"), bool)
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor UI-settings payload violates the pinned reader contract")
        return
    _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor typed-reader ID is not in the pinned implemented set")

def _validate_provenance(docs: Mapping[str, Any]) -> None:
    agent = docs["surveyor/agent_bundle.json"]
    generated_at = agent.get("generated_at")
    if not isinstance(generated_at, str) or not _GENERATED_AT_RE.fullmatch(generated_at):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor generated_at provenance is not the pinned UTC isoformat")
    try:
        datetime.fromisoformat(generated_at)
    except ValueError:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor generated_at provenance is not a valid timestamp")
    for relative, doc in docs.items():
        has_producer_timestamp = (
            relative in {"surveyor/coverage.json", "missing-readers.json"}
            or relative.startswith(("aliases/", "telemetry/"))
        )
        if has_producer_timestamp and (
            not isinstance(doc, dict) or doc.get("generated_at") != generated_at
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor document generated_at provenance is inconsistent")
    runtime_doc = docs.get("surveyor/runtime.json")
    agent_runtime = agent.get("runtime")
    if runtime_doc != agent_runtime:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor runtime artifact disagrees with agent bundle")
    if isinstance(agent_runtime, dict) and agent_runtime.get("runtime_access") not in _ALLOWED_RUNTIME_ACCESS:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor runtime access state is outside the pinned producer contract")
    if isinstance(agent_runtime, dict):
        runtime_access = agent_runtime.get("runtime_access")
        windows_present = "visible_tibia_windows" in agent_runtime
        if (
            (runtime_access != "READ_ONLY_UNAVAILABLE" or windows_present)
            and not isinstance(agent_runtime.get("visible_tibia_windows"), list)
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor visible-window collection is outside the pinned producer contract")
    _validate_admitted_runtime_contract(agent_runtime)
    if isinstance(agent_runtime, dict):
        control = agent_runtime.get("canonical_control") if isinstance(agent_runtime.get("canonical_control"), dict) else {}
        registration = control.get("registration") if isinstance(control.get("registration"), dict) else {}
        lease = control.get("lease") if isinstance(control.get("lease"), dict) else {}
        if (
            control.get("registration_present") is True
            and control.get("lease_present") is True
            and (
                registration.get("lease_generation") != lease.get("generation")
                or registration.get("runtime_id") != lease.get("runtime_id")
            )
        ):
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor registration is not bound to the current lease")
    expected = _expected_runtime_provenance(agent)
    expected_with_time = {"generated_at": generated_at, **expected}
    expected_runtime_identity = _project_pinned_runtime_identity(agent_runtime)
    raw_typed_readers = agent.get("typed_readers")
    if not isinstance(raw_typed_readers, dict):
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor typed-reader registry is malformed")
    agent_typed_readers = raw_typed_readers
    runtime_admitted = isinstance(agent_runtime, dict) and agent_runtime.get("runtime_access") == "READ_ONLY_ADMITTED"
    if runtime_admitted:
        if set(agent_typed_readers) != PINNED_IMPLEMENTED_TYPED_READERS:
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted runtime typed-reader set is incomplete or unexpected")
    elif agent_typed_readers:
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor typed readers exist without an admitted runtime")
    for relative, doc in docs.items():
        if relative.startswith(("aliases/", "telemetry/")):
            provenance = doc.get("run_provenance") if isinstance(doc, dict) else None
            if not isinstance(provenance, dict):
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor bundle provenance is missing")
            for key, value in expected_with_time.items():
                if provenance.get(key) != value:
                    _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor bundle provenance is inconsistent")
        if not relative.startswith("telemetry/") or not isinstance(doc, dict):
            continue
        states = doc.get("source_states") if isinstance(doc.get("source_states"), dict) else {}
        if states.get("runtime_identity") != expected_runtime_identity:
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor runtime identity disagrees with agent runtime")
        expected_alias, expected_reader_id = PINNED_TELEMETRY_CONTRACTS[relative]
        typed = states.get("subsystem_typed_reader") if isinstance(states.get("subsystem_typed_reader"), dict) else {}
        if doc.get("alias") != expected_alias or typed.get("source") != expected_reader_id:
            _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor telemetry selected an unexpected typed reader")
        if expected_reader_id not in PINNED_IMPLEMENTED_TYPED_READERS:
            continue
        if not runtime_admitted:
            expected_unavailable = {
                "state": "UNAVAILABLE", "evidence_level": "UNKNOWN", "source": expected_reader_id,
                "value": None, "reason": "RUNTIME_INPUT_UNAVAILABLE_THIS_RUN",
            }
            if typed != expected_unavailable:
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor reader evidence exists without an admitted runtime")
            continue
        expected_typed = agent_typed_readers[expected_reader_id]
        if not isinstance(expected_typed, dict) or expected_typed.get("reader_id") != expected_reader_id:
            _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted typed-reader payload is malformed")
        if expected_typed.get("state") == "AVAILABLE":
            _validate_available_typed_reader(expected_reader_id, expected_typed)
            expected_telemetry = {
                "state": "AVAILABLE", "evidence_level": "PROVEN", "source": expected_reader_id,
                "value": expected_typed, "reason": None,
            }
            if typed != expected_telemetry:
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor AVAILABLE reader evidence disagrees with agent bundle")
            continue
        if expected_typed.get("state") == "UNAVAILABLE":
            if (
                expected_typed.get("semantic_promotion_allowed") is not False
                or not isinstance(expected_typed.get("reason"), str)
                or not expected_typed.get("reason")
            ):
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor unavailable reader payload is malformed")
            expected_telemetry = {
                "state": "UNAVAILABLE", "evidence_level": "UNKNOWN", "source": expected_reader_id,
                "value": expected_typed, "reason": "RUNTIME_INPUT_UNAVAILABLE_THIS_RUN",
            }
            if typed != expected_telemetry:
                _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor unavailable reader evidence disagrees with agent bundle")
            continue
        _fail("SURVEYOR_PROVENANCE_MISMATCH", "Surveyor admitted reader has an unsupported state")


def _runtime_projection(docs: Mapping[str, Any], ingested_monotonic_ns: int) -> tuple[RuntimeStatus, dict[str, str], dict[str, Any]]:
    auth = docs.get("telemetry/auth-session.json") or {}
    states = auth.get("source_states") if isinstance(auth, dict) else {}
    runtime = states.get("runtime_identity") if isinstance(states, dict) else {}
    runtime_state = runtime.get("state") if isinstance(runtime, dict) else "UNKNOWN"
    value = runtime.get("value") if isinstance(runtime, dict) else None
    process = value.get("process") if isinstance(value, dict) and isinstance(value.get("process"), dict) else {}
    control = value.get("canonical_control") if isinstance(value, dict) and isinstance(value.get("canonical_control"), dict) else {}
    fence = value.get("exact_current_fence") if isinstance(value, dict) and isinstance(value.get("exact_current_fence"), dict) else {}
    runtime_id = control.get("runtime_id") if isinstance(control, dict) else None
    client_sha = process.get("client_sha256")
    client_size = process.get("client_size")
    available = (
        runtime_state == "AVAILABLE"
        and isinstance(value, dict)
        and value.get("runtime_access") == "READ_ONLY_ADMITTED"
        and value.get("target_running") is True
        and value.get("runtime_namespace_scope") == "DECLARED_TARGET_ONLY"
        and value.get("external_containers_scanned") is False
        and value.get("target_uniqueness_scope") == "DECLARED_RUNTIME_NAMESPACE"
        and value.get("target_uniqueness") == "PROVEN"
        and value.get("target_process_count") == 1
        and fence.get("match") is True
        and process.get("exact_fence_match") is True
        and isinstance(client_sha, str)
        and bool(client_sha)
        and client_sha == fence.get("sha256")
        and isinstance(client_size, int)
        and client_size == fence.get("size")
        and isinstance(process.get("pid"), int)
        and process.get("pid") > 0
        and isinstance(process.get("process_start_ticks"), int)
        and process.get("process_start_ticks") > 0
        and control.get("registration_present") is True
        and control.get("lease_present") is True
        and control.get("lease_expired") is False
        and control.get("lease_status") == "active"
        and isinstance(runtime_id, str)
        and bool(runtime_id)
        and isinstance(control.get("registration_generation"), int)
        and isinstance(control.get("lease_generation"), int)
    )
    status = RuntimeStatus(
        adapter_id="surveyor",
        adapter_generation=PINNED_PRODUCER_COMMIT,
        runtime_state="ONLINE" if available else "UNKNOWN",
        client_state="UNKNOWN",
        recorder_state="STOPPED",
        authority_state="READ_ONLY",
        session_epoch=None,
        runtime_instance_id=runtime_id if available else None,
        observed_monotonic_ns=ingested_monotonic_ns,
        freshness=Freshness.UNKNOWN,
        reasons=("SURVEYOR_READ_ONLY_NONAUTHORITATIVE",),
    )
    readiness = {"runtime_identity": "AVAILABLE" if available else "UNAVAILABLE"}
    safe_runtime_provenance = runtime if available else {
        "state": "UNKNOWN",
        "evidence_level": "UNKNOWN",
        "value": None,
        "source": "surveyor.runtime",
    }
    return status, readiness, {"runtime_identity": safe_runtime_provenance}


def _capabilities(docs: Mapping[str, Any]) -> tuple[Capability, ...]:
    result: list[Capability] = []
    for relative, doc in sorted(docs.items()):
        if not relative.startswith("aliases/") or not isinstance(doc, dict):
            continue
        alias = doc.get("alias")
        if not isinstance(alias, str):
            continue
        telemetry_path = doc.get("telemetry_file")
        typed_state = None
        if isinstance(telemetry_path, str):
            telemetry = docs.get(telemetry_path) or {}
            source_states = telemetry.get("source_states") if isinstance(telemetry, dict) else {}
            typed = source_states.get("subsystem_typed_reader") if isinstance(source_states, dict) else {}
            typed_state = typed.get("state") if isinstance(typed, dict) else None
        read_supported = (
            doc.get("missing_reader") is None
            and typed_state == "AVAILABLE"
            and isinstance(typed, dict)
            and typed.get("evidence_level") == "PROVEN"
            and isinstance(typed.get("value"), dict)
        )
        capability_id = "surveyor." + alias.removeprefix("TIBIA-RE-").lower().replace("_", "-")
        result.append(Capability(
            capability_id=capability_id,
            semantic_version="1.0",
            read_supported=read_supported,
            action_supported=False,
            source="surveyor",
            notes="read-only evidence projection; no mutation authority",
        ))
    return tuple(result)


def _snapshot(docs: Mapping[str, Any], status: RuntimeStatus, ingested_monotonic_ns: int) -> GameSnapshot:
    player_position = {"x": None, "y": None, "z": None}
    candidate_fields: dict[str, Any] = {}
    player_doc = docs.get("telemetry/player-state.json") or {}
    states = player_doc.get("source_states") if isinstance(player_doc, dict) else {}
    typed = states.get("subsystem_typed_reader") if isinstance(states, dict) else {}
    typed_value = typed.get("value") if isinstance(typed, dict) else None
    if isinstance(typed_value, dict) and typed.get("state") == "AVAILABLE":
        position = typed_value.get("position")
        if isinstance(position, dict):
            candidate_fields["player.position"] = {
                "value": {"x": position.get("x"), "y": position.get("y"), "z": position.get("z")},
                "source": "player_state_typed_reader",
                "semantic_promotion_allowed": False,
            }
    source_quality = {
        "field_sources": {},
        "unknown_fields": ["player.position"],
        "stale_fields": [],
        "candidate_fields": candidate_fields,
    }
    generated_at = (docs.get("surveyor/agent_bundle.json") or {}).get("generated_at")
    return GameSnapshot(
        snapshot_id="surveyor:" + hashlib.sha256(str(generated_at).encode("utf-8")).hexdigest()[:16],
        adapter_id="surveyor",
        adapter_generation=PINNED_PRODUCER_COMMIT,
        ingested_monotonic_ns=ingested_monotonic_ns,
        client_state="UNKNOWN",
        session_epoch=None,
        runtime_instance_id=status.runtime_instance_id,
        source_timestamp=generated_at,
        source_clock_domain="surveyor.generated_at",
        player={"position": player_position},
        source_quality=source_quality,
    )

def load_surveyor_bundle(
    root: Path,
    *,
    producer_commit: str,
    ingested_monotonic_ns: int = 0,
) -> SurveyorReadModel:
    if producer_commit != PINNED_PRODUCER_COMMIT:
        _fail("SURVEYOR_PRODUCER_INCOMPATIBLE", "Surveyor producer commit is not the accepted pin")
    if not isinstance(ingested_monotonic_ns, int) or ingested_monotonic_ns < 0:
        _fail("SURVEYOR_INGEST_TIME_INVALID", "Surveyor ingestion time is invalid")
    root_path = Path(root)
    bundle_root = _open_bundle_root(root_path)
    try:
        entries = _parse_manifest(bundle_root)
        if set(entries) != EXPECTED_INTERFACE_FILES:
            _fail("SURVEYOR_INTERFACE_INCOMPATIBLE", "Surveyor bundle does not match the pinned producer interface")
        payloads = _verify_files(bundle_root, entries)
        _scan_text_payload_privacy(payloads)
        docs = _load_json_documents(payloads)
        _validate_documents(docs)
        _validate_provenance(docs)
        runtime_status, readiness, provenance = _runtime_projection(docs, ingested_monotonic_ns)
        capabilities = _capabilities(docs)
        snapshot = _snapshot(docs, runtime_status, ingested_monotonic_ns)
        return SurveyorReadModel(
            runtime_status=runtime_status,
            snapshot=snapshot,
            capabilities=capabilities,
            readiness=readiness,
            provenance={"producer_commit": producer_commit, **provenance},
        )
    finally:
        _close_bundle_root(bundle_root)
