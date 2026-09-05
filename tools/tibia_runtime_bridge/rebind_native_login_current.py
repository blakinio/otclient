from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import struct
from dataclasses import dataclass
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86_const import X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52_105_824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

RTTI_NAMES = {
    "game_client": ("N5tibia6client11TGameClientE", "tibia::client::TGameClient"),
    "character_controller": (
        "N5tibia10gamewindow29TCharacterSelectionControllerE",
        "tibia::gamewindow::TCharacterSelectionController",
    ),
    "player_protocol_handler": (
        "N5tibia4game29TPlayerProtocolMessageHandlerE",
        "tibia::game::TPlayerProtocolMessageHandler",
    ),
    "gameserver_game_session": (
        "N5tibia4game22TGameserverGameSessionE",
        "tibia::game::TGameserverGameSession",
    ),
    "worldmap_handler": (
        "N5tibia8worldmap31TWorldmapProtocolMessageHandlerE",
        "tibia::worldmap::TWorldmapProtocolMessageHandler",
    ),
}


@dataclass(frozen=True)
class Section:
    offset: int
    size: int
    address: int
    flags: int


class BinaryView:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.raw = path.read_bytes()
        if len(self.raw) != EXPECTED_SIZE:
            raise RuntimeError(f"EXACT_CLIENT_SIZE_MISMATCH:{len(self.raw)}")
        digest = hashlib.sha256(self.raw).hexdigest()
        if digest != EXPECTED_SHA256:
            raise RuntimeError(f"EXACT_CLIENT_SHA256_MISMATCH:{digest}")
        with path.open("rb") as handle:
            elf = ELFFile(handle)
            if elf.elfclass != 64 or not elf.little_endian or elf["e_machine"] != "EM_X86_64":
                raise RuntimeError("EXACT_CLIENT_ELF_IDENTITY_MISMATCH")
            self.sections = [
                Section(
                    int(section["sh_offset"]),
                    int(section["sh_size"]),
                    int(section["sh_addr"]),
                    int(section["sh_flags"]),
                )
                for section in elf.iter_sections()
                if int(section["sh_size"]) > 0
            ]
        self.relocations = self._parse_relocations()
        self.by_addend: dict[int, list[int]] = {}
        self.by_offset: dict[int, list[int]] = {}
        for offset, addend in self.relocations:
            self.by_addend.setdefault(addend, []).append(offset)
            self.by_offset.setdefault(offset, []).append(addend)

    def _parse_relocations(self) -> list[tuple[int, int]]:
        raw = self.raw
        if raw[:4] != b"\x7fELF" or raw[4] != 2 or raw[5] != 1:
            raise RuntimeError("CURRENT_CLIENT_NOT_ELF64_LE")
        shoff = struct.unpack_from("<Q", raw, 0x28)[0]
        shentsize = struct.unpack_from("<H", raw, 0x3A)[0]
        shnum = struct.unpack_from("<H", raw, 0x3C)[0]
        relocations: list[tuple[int, int]] = []
        for index in range(shnum):
            header = shoff + index * shentsize
            _, stype, _, _, file_offset, size, _, _, _, entsize = struct.unpack_from(
                "<IIQQQQIIQQ", raw, header
            )
            if stype != 4:  # SHT_RELA
                continue
            step = entsize or 24
            for offset in range(file_offset, file_offset + size, step):
                if offset + 24 > len(raw):
                    break
                r_offset, _, r_addend = struct.unpack_from("<QQq", raw, offset)
                relocations.append((r_offset, r_addend))
        return relocations

    def off_to_va(self, offset: int) -> int | None:
        for section in self.sections:
            if section.offset <= offset < section.offset + section.size:
                return section.address + offset - section.offset
        return None

    def va_to_off(self, address: int) -> int:
        for section in self.sections:
            if section.address <= address < section.address + section.size:
                return section.offset + address - section.address
        raise ValueError(hex(address))

    def u32(self, address: int) -> int:
        return struct.unpack_from("<I", self.raw, self.va_to_off(address))[0]

    def i32(self, address: int) -> int:
        return struct.unpack_from("<i", self.raw, self.va_to_off(address))[0]

    def qword(self, address: int) -> int:
        return struct.unpack_from("<Q", self.raw, self.va_to_off(address))[0]

    def bytes_at(self, address: int, size: int) -> bytes:
        offset = self.va_to_off(address)
        return self.raw[offset : offset + size]

    def executable(self, address: int) -> bool:
        return any(
            section.flags & 4 and section.address <= address < section.address + section.size
            for section in self.sections
        )

    def relocated_value(self, address: int) -> int | None:
        values = self.by_offset.get(address, [])
        if values and len(set(values)) == 1:
            return values[0]
        try:
            return self.qword(address)
        except (ValueError, struct.error):
            return None

    def exact_rtti_vptr(self, mangled: str) -> int:
        needle = mangled.encode() + b"\0"
        name_vas: list[int] = []
        start = 0
        while True:
            position = self.raw.find(needle, start)
            if position < 0:
                break
            if position == 0 or self.raw[position - 1] == 0:
                address = self.off_to_va(position)
                if address is not None:
                    name_vas.append(address)
            start = position + 1
        candidates: list[int] = []
        for name_va in name_vas:
            for target in self.by_addend.get(name_va, []):
                typeinfo = target - 8
                for target2 in self.by_addend.get(typeinfo, []):
                    header = target2 - 8
                    try:
                        if self.qword(header) != 0:
                            continue
                    except (ValueError, struct.error):
                        continue
                    vptr = header + 16
                    first = self.relocated_value(vptr)
                    if first is not None and self.executable(first):
                        candidates.append(vptr)
        unique = sorted(set(candidates))
        if len(unique) != 1:
            raise RuntimeError(f"RTTI_NOT_UNIQUE:{mangled}:{[hex(item) for item in unique]}")
        return unique[0]

    def find_unique_bytes_va(self, needle: bytes) -> int:
        positions: list[int] = []
        start = 0
        while True:
            position = self.raw.find(needle, start)
            if position < 0:
                break
            positions.append(position)
            start = position + 1
        vas = sorted({va for position in positions if (va := self.off_to_va(position)) is not None})
        if len(vas) != 1:
            raise RuntimeError(f"STRING_NOT_UNIQUE:{needle!r}:{[hex(item) for item in vas]}")
        return vas[0]

    def find_stringdata_base(self, class_name: str) -> int:
        encoded = class_name.encode()
        class_va = self.find_unique_bytes_va(encoded + b"\0")
        length_bytes = struct.pack("<I", len(encoded))
        candidates: list[int] = []
        start = 4
        while True:
            length_pos = self.raw.find(length_bytes, start)
            if length_pos < 0:
                break
            entry_pos = length_pos - 4
            entry_va = self.off_to_va(entry_pos)
            if entry_va is not None:
                try:
                    if entry_va + self.u32(entry_va) == class_va:
                        candidates.append(entry_va)
                except (ValueError, struct.error):
                    pass
            start = length_pos + 1
        unique = sorted(set(candidates))
        if len(unique) != 1:
            raise RuntimeError(
                f"STRINGDATA_BASE_NOT_UNIQUE:{class_name}:{[hex(item) for item in unique]}"
            )
        return unique[0]

    def qstring(self, base: int, index: int) -> str:
        relative = self.u32(base + 8 * index)
        length = self.u32(base + 8 * index + 4)
        if length > 4096:
            raise ValueError("qstring length")
        return self.bytes_at(base + relative, length).decode("utf-8", "strict")

    def find_string_index(self, base: int, text: str, *, max_index: int = 1024) -> int:
        hits: list[int] = []
        for index in range(max_index):
            try:
                if self.qstring(base, index) == text:
                    hits.append(index)
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
        if len(hits) != 1:
            raise RuntimeError(f"QSTRING_INDEX_NOT_UNIQUE:{text}:{hits}")
        return hits[0]

    def find_metadata(
        self,
        stringdata: int,
        *,
        class_name: str,
        method_count: int,
        target_name: str,
        expected_target_index: int,
        expected_argc: int,
    ) -> tuple[int, dict[str, Any]]:
        target_name_index = self.find_string_index(stringdata, target_name)
        window_begin = max(0, self.va_to_off(stringdata) - 0x20000)
        window_end = min(len(self.raw) - 56, self.va_to_off(stringdata) + 0x4000)
        candidates: list[tuple[int, dict[str, Any]]] = []
        for offset in range(window_begin, window_end, 4):
            address = self.off_to_va(offset)
            if address is None:
                continue
            try:
                header = [self.u32(address + 4 * index) for index in range(14)]
            except (ValueError, struct.error):
                continue
            if header[0] != 13 or header[1] != 0 or header[4] != method_count:
                continue
            method_data = header[5]
            signal_count = header[13]
            if method_data < 14 or method_data > 8192 or signal_count > method_count:
                continue
            row_address = address + 4 * (method_data + 6 * expected_target_index)
            try:
                row = tuple(self.u32(row_address + 4 * item) for item in range(6))
                if row[0] != target_name_index or row[1] != expected_argc:
                    continue
                if self.qstring(stringdata, row[0]) != target_name:
                    continue
                if self.qstring(stringdata, header[1]) != class_name:
                    continue
                params = tuple(
                    self.u32(address + 4 * (row[2] + item))
                    for item in range(expected_argc + 1)
                )
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
            candidates.append(
                (
                    address,
                    {
                        "revision": header[0],
                        "method_count": method_count,
                        "method_data": method_data,
                        "signal_count": signal_count,
                        "target_index": expected_target_index,
                        "target_name_index": target_name_index,
                        "target_row": list(row),
                        "target_params": list(params),
                    },
                )
            )
        unique_addresses = sorted({address for address, _ in candidates})
        if len(unique_addresses) != 1:
            raise RuntimeError(
                f"QMETA_METADATA_NOT_UNIQUE:{class_name}:{[hex(item) for item in unique_addresses]}"
            )
        address = unique_addresses[0]
        info = next(info for candidate, info in candidates if candidate == address)
        return address, info

    def find_dispatch(self, *, method_count: int, target_index: int) -> dict[str, Any]:
        compare = method_count - 1
        patterns = [b"\x83\xfa" + bytes([compare])] if compare <= 0x7F else []
        patterns.append(b"\x81\xfa" + struct.pack("<I", compare))
        compare_vas: set[int] = set()
        for section in self.sections:
            if not section.flags & 4:
                continue
            data = self.raw[section.offset : section.offset + section.size]
            for pattern in patterns:
                start = 0
                while True:
                    position = data.find(pattern, start)
                    if position < 0:
                        break
                    compare_vas.add(section.address + position)
                    start = position + 1

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        candidates: list[dict[str, Any]] = []
        for compare_va in sorted(compare_vas):
            try:
                code = self.bytes_at(compare_va, 0x180)
            except ValueError:
                continue
            instructions = list(md.disasm(code, compare_va))
            for instruction in instructions[:32]:
                if instruction.mnemonic != "lea" or len(instruction.operands) < 2:
                    continue
                memory = instruction.operands[1]
                if memory.type != X86_OP_MEM or memory.mem.base != X86_REG_RIP:
                    continue
                table = instruction.address + instruction.size + memory.mem.disp
                try:
                    targets = [table + self.i32(table + 4 * index) for index in range(method_count)]
                except (ValueError, struct.error):
                    continue
                if not all(self.executable(target) for target in targets):
                    continue
                target = targets[target_index]
                fence = self.bytes_at(target, 32)
                candidates.append(
                    {
                        "compare": compare_va,
                        "lea": instruction.address,
                        "table": table,
                        "target": target,
                        "target_fence": fence.hex(),
                    }
                )
        dedup = {
            (item["table"], item["target"]): item
            for item in candidates
        }
        unique = list(dedup.values())
        if len(unique) != 1:
            raise RuntimeError(
                "QMETA_DISPATCH_NOT_UNIQUE:"
                + json.dumps(
                    [
                        {key: hex(value) if isinstance(value, int) else value for key, value in item.items()}
                        for item in unique
                    ],
                    sort_keys=True,
                )
            )
        return unique[0]


def _discover_class(
    view: BinaryView,
    *,
    class_name: str,
    method_count: int,
    target_name: str,
    target_index: int,
    argc: int,
    with_dispatch: bool,
) -> dict[str, Any]:
    stringdata = view.find_stringdata_base(class_name)
    metadata, metadata_info = view.find_metadata(
        stringdata,
        class_name=class_name,
        method_count=method_count,
        target_name=target_name,
        expected_target_index=target_index,
        expected_argc=argc,
    )
    result: dict[str, Any] = {
        "class_name": class_name,
        "stringdata": stringdata,
        "metadata": metadata,
        **metadata_info,
    }
    if with_dispatch:
        result["dispatch"] = view.find_dispatch(method_count=method_count, target_index=target_index)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()

    view = BinaryView(args.client)
    rtti = {
        name: {
            "mangled": mangled,
            "class_name": class_name,
            "vptr": view.exact_rtti_vptr(mangled),
        }
        for name, (mangled, class_name) in RTTI_NAMES.items()
    }

    game = _discover_class(
        view,
        class_name="tibia::client::TGameClient",
        method_count=44,
        target_name="onRequestLoginWithCredentials",
        target_index=17,
        argc=2,
        with_dispatch=True,
    )
    if game["target_params"] != [0x2B, 0x0A, 0x0A]:
        raise RuntimeError(f"GAME_CLIENT_AUTH_PARAM_TYPES_CHANGED:{game['target_params']!r}")

    character = _discover_class(
        view,
        class_name="tibia::gamewindow::TCharacterSelectionController",
        method_count=26,
        target_name="requestCharacterLogin",
        target_index=0,
        argc=1,
        with_dispatch=False,
    )
    character_stringdata = int(character["stringdata"])
    character_metadata = int(character["metadata"])
    confirm_name = "onCharacterSelectionConfirmed"
    confirm_index = view.find_string_index(character_stringdata, confirm_name)
    method_data = int(character["method_data"])
    confirm_rows: list[dict[str, Any]] = []
    for index in range(int(character["method_count"])):
        row = tuple(
            view.u32(character_metadata + 4 * (method_data + 6 * index + item))
            for item in range(6)
        )
        if row[0] == confirm_index:
            confirm_rows.append(
                {
                    "index": index,
                    "row": list(row),
                    "params": [
                        view.u32(character_metadata + 4 * (row[2] + item))
                        for item in range(row[1] + 1)
                    ],
                }
            )
    if len(confirm_rows) != 1:
        raise RuntimeError(f"CHARACTER_CONFIRM_METHOD_NOT_UNIQUE:{confirm_rows!r}")
    character["confirm"] = confirm_rows[0]
    if character["confirm"]["index"] != 11:
        raise RuntimeError(f"CHARACTER_CONFIRM_INDEX_CHANGED:{character['confirm']['index']}")
    character["dispatch_request"] = view.find_dispatch(method_count=26, target_index=0)
    character["dispatch_confirm"] = view.find_dispatch(method_count=26, target_index=11)

    gameserver = _discover_class(
        view,
        class_name="tibia::authentication::TAuthenticationProcessController",
        method_count=51,
        target_name="requestCharacterGameserverLogin",
        target_index=5,
        argc=0,
        with_dispatch=True,
    )
    gameserver_stringdata = int(gameserver["stringdata"])
    gameserver_metadata = int(gameserver["metadata"])
    start_name = "onStartGameServerLoginStateEntered"
    start_name_index = view.find_string_index(gameserver_stringdata, start_name)
    gameserver_method_data = int(gameserver["method_data"])
    start_rows: list[dict[str, Any]] = []
    for index in range(int(gameserver["method_count"])):
        row = tuple(
            view.u32(gameserver_metadata + 4 * (gameserver_method_data + 6 * index + item))
            for item in range(6)
        )
        if row[0] == start_name_index:
            start_rows.append({"index": index, "row": list(row)})
    if len(start_rows) != 1 or start_rows[0]["index"] != 27:
        raise RuntimeError(f"GAMESERVER_START_METHOD_CHANGED:{start_rows!r}")
    gameserver["start"] = start_rows[0]
    gameserver["dispatch_start"] = view.find_dispatch(method_count=51, target_index=27)

    result = {
        "schema": "otclient.track-a.native-login-current-rebind.v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "rtti": rtti,
        "qmeta": {
            "game_client": game,
            "character_controller": character,
            "authentication_process_controller": gameserver,
        },
        "safety": {
            "runtime_access": "none",
            "official_client_executed": False,
            "credentials_used": False,
            "process_memory_access": False,
            "packet_capture": False,
            "raw_client_retained": False,
            "track_b_pr_284_modified": False,
        },
        "terminal_result": "BE4F48_NATIVE_LOGIN_STATIC_REBIND_PROVEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BE4F48_NATIVE_LOGIN_STATIC_REBIND=PASS")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
