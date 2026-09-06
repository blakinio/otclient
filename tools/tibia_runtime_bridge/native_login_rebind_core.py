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

    def relocated_values(self, address: int) -> list[int]:
        values = self.by_offset.get(address, [])
        if values:
            return sorted(set(values))
        try:
            return [self.qword(address)]
        except (ValueError, struct.error):
            return []

    def exact_rtti_vptr(self, mangled: str) -> int:
        needle = mangled.encode() + b"\0"
        name_vas = self.find_bytes_vas(needle, require_leading_nul=True)
        candidates: set[int] = set()
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
                    first_values = self.relocated_values(vptr)
                    if len(first_values) == 1 and self.executable(first_values[0]):
                        candidates.add(vptr)
        if len(candidates) != 1:
            raise RuntimeError(
                f"RTTI_NOT_UNIQUE:{mangled}:{[hex(item) for item in sorted(candidates)]}"
            )
        return next(iter(candidates))

    def find_bytes_vas(self, needle: bytes, *, require_leading_nul: bool = False) -> list[int]:
        positions: list[int] = []
        start = 0
        while True:
            position = self.raw.find(needle, start)
            if position < 0:
                break
            if not require_leading_nul or position == 0 or self.raw[position - 1] == 0:
                positions.append(position)
            start = position + 1
        return sorted(
            {
                address
                for position in positions
                if (address := self.off_to_va(position)) is not None
            }
        )

    def candidate_stringdata_bases(self, class_name: str) -> list[int]:
        encoded = class_name.encode()
        class_vas = set(self.find_bytes_vas(encoded + b"\0"))
        if not class_vas:
            raise RuntimeError(f"QMETA_CLASS_STRING_NOT_FOUND:{class_name}")
        length_bytes = struct.pack("<I", len(encoded))
        candidates: set[int] = set()
        start = 4
        while True:
            length_pos = self.raw.find(length_bytes, start)
            if length_pos < 0:
                break
            entry_pos = length_pos - 4
            entry_va = self.off_to_va(entry_pos)
            if entry_va is not None:
                try:
                    if entry_va + self.u32(entry_va) in class_vas:
                        candidates.add(entry_va)
                except (ValueError, struct.error):
                    pass
            start = length_pos + 1
        if not candidates:
            raise RuntimeError(f"QMETA_STRINGDATA_NOT_FOUND:{class_name}")
        return sorted(candidates)

    def qstring(self, base: int, index: int) -> str:
        relative = self.u32(base + 8 * index)
        length = self.u32(base + 8 * index + 4)
        if length > 4096:
            raise ValueError("qstring length")
        return self.bytes_at(base + relative, length).decode("utf-8", "strict")

    def string_indexes(self, base: int, text: str, *, max_index: int = 1024) -> list[int]:
        hits: list[int] = []
        for index in range(max_index):
            try:
                if self.qstring(base, index) == text:
                    hits.append(index)
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
        return hits

    def metadata_candidates(
        self,
        stringdata: int,
        *,
        class_name: str,
        method_count: int,
        target_name: str,
        expected_target_index: int,
        expected_argc: int,
    ) -> list[tuple[int, dict[str, Any]]]:
        target_name_indexes = set(self.string_indexes(stringdata, target_name))
        if not target_name_indexes:
            return []
        window_begin = max(0, self.va_to_off(stringdata) - 0x20000)
        window_end = min(len(self.raw) - 56, self.va_to_off(stringdata) + 0x4000)
        candidates: dict[int, dict[str, Any]] = {}
        for offset in range(window_begin, window_end, 4):
            address = self.off_to_va(offset)
            if address is None:
                continue
            try:
                header = [self.u32(address + 4 * index) for index in range(14)]
            except (ValueError, struct.error):
                continue
            if header[0] != 13 or header[4] != method_count:
                continue
            method_data = header[5]
            signal_count = header[13]
            if method_data < 14 or method_data > 8192 or signal_count > method_count:
                continue
            try:
                if self.qstring(stringdata, header[1]) != class_name:
                    continue
                row_address = address + 4 * (method_data + 6 * expected_target_index)
                row = tuple(self.u32(row_address + 4 * item) for item in range(6))
                if row[0] not in target_name_indexes or row[1] != expected_argc:
                    continue
                if self.qstring(stringdata, row[0]) != target_name:
                    continue
                params = tuple(
                    self.u32(address + 4 * (row[2] + item))
                    for item in range(expected_argc + 1)
                )
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
            candidates[address] = {
                "revision": header[0],
                "class_name_index": header[1],
                "method_count": method_count,
                "method_data": method_data,
                "signal_count": signal_count,
                "target_index": expected_target_index,
                "target_name_index": row[0],
                "target_row": list(row),
                "target_params": list(params),
            }
        return sorted(candidates.items())

    def static_metacall(self, stringdata: int, metadata: int) -> dict[str, int]:
        candidates: dict[tuple[int, int], dict[str, int]] = {}
        for string_slot in self.by_addend.get(stringdata, []):
            metadata_slot = string_slot + 8
            if metadata not in self.by_offset.get(metadata_slot, []):
                continue
            metacall_slot = metadata_slot + 8
            values = self.relocated_values(metacall_slot)
            if len(values) != 1 or not self.executable(values[0]):
                continue
            static_metaobject = string_slot - 8
            candidates[(static_metaobject, values[0])] = {
                "static_metaobject": static_metaobject,
                "stringdata_slot": string_slot,
                "metadata_slot": metadata_slot,
                "metacall_slot": metacall_slot,
                "static_metacall": values[0],
            }
        if len(candidates) != 1:
            raise RuntimeError(
                "QMETA_STATIC_METACALL_NOT_UNIQUE:"
                + json.dumps(
                    [
                        {key: hex(value) for key, value in item.items()}
                        for item in candidates.values()
                    ],
                    sort_keys=True,
                )
            )
        return next(iter(candidates.values()))

    def dispatch_from_metacall(
        self,
        static_metacall: int,
        *,
        method_count: int,
        target_index: int,
    ) -> dict[str, Any]:
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        instructions = list(md.disasm(self.bytes_at(static_metacall, 0x1200), static_metacall))
        candidates: dict[tuple[int, int], dict[str, Any]] = {}
        for position, instruction in enumerate(instructions):
            if instruction.mnemonic != "lea" or len(instruction.operands) < 2:
                continue
            memory = instruction.operands[1]
            if memory.type != X86_OP_MEM or memory.mem.base != X86_REG_RIP:
                continue
            table = instruction.address + instruction.size + memory.mem.disp
            register = instruction.operands[0].reg
            context_before = instructions[max(0, position - 24) : position]
            context_after = instructions[position + 1 : position + 12]
            full_range_tokens = {
                f"edx, {method_count - 1}",
                f"edx, 0x{method_count - 1:x}",
            }
            has_full_range = any(
                item.mnemonic == "cmp" and item.op_str in full_range_tokens
                for item in context_before
            )
            has_indexed_use = any(
                operand.type == X86_OP_MEM
                and operand.mem.base == register
                and operand.mem.scale == 4
                for item in context_after
                for operand in item.operands
            )
            if not has_full_range or not has_indexed_use:
                continue
            try:
                targets = [table + self.i32(table + 4 * index) for index in range(method_count)]
            except (ValueError, struct.error):
                continue
            if not all(self.executable(target) for target in targets):
                continue
            target = targets[target_index]
            fence = self.bytes_at(target, 32)
            candidates[(table, target)] = {
                "lea": instruction.address,
                "table": table,
                "target": target,
                "target_fence": fence.hex(),
            }
        if len(candidates) != 1:
            raise RuntimeError(
                "QMETA_DISPATCH_NOT_UNIQUE:"
                + json.dumps(
                    [
                        {key: hex(value) if isinstance(value, int) else value for key, value in item.items()}
                        for item in candidates.values()
                    ],
                    sort_keys=True,
                )
            )
        return next(iter(candidates.values()))


def discover_class(
    view: BinaryView,
    *,
    class_name: str,
    method_count: int,
    target_name: str,
    target_index: int,
    argc: int,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    diagnostics: dict[str, list[str]] = {"stringdata": [], "metadata": []}
    for stringdata in view.candidate_stringdata_bases(class_name):
        diagnostics["stringdata"].append(hex(stringdata))
        for metadata, metadata_info in view.metadata_candidates(
            stringdata,
            class_name=class_name,
            method_count=method_count,
            target_name=target_name,
            expected_target_index=target_index,
            expected_argc=argc,
        ):
            diagnostics["metadata"].append(hex(metadata))
            try:
                metaobject = view.static_metacall(stringdata, metadata)
                dispatch = view.dispatch_from_metacall(
                    metaobject["static_metacall"],
                    method_count=method_count,
                    target_index=target_index,
                )
            except RuntimeError:
                continue
            candidates.append(
                {
                    "class_name": class_name,
                    "stringdata": stringdata,
                    "metadata": metadata,
                    **metadata_info,
                    "metaobject": metaobject,
                    "dispatch": dispatch,
                }
            )
    unique: dict[tuple[int, int, int], dict[str, Any]] = {
        (item["stringdata"], item["metadata"], item["metaobject"]["static_metacall"]): item
        for item in candidates
    }
    if len(unique) != 1:
        raise RuntimeError(
            f"QMETA_CLASS_CONTRACT_NOT_UNIQUE:{class_name}:"
            + json.dumps(
                {
                    "diagnostics": diagnostics,
                    "accepted": [
                        {
                            "stringdata": hex(item["stringdata"]),
                            "metadata": hex(item["metadata"]),
                            "static_metacall": hex(item["metaobject"]["static_metacall"]),
                        }
                        for item in unique.values()
                    ],
                },
                sort_keys=True,
            )
        )
    return next(iter(unique.values()))


def find_named_method(
    view: BinaryView,
    discovered: dict[str, Any],
    *,
    name: str,
    expected_index: int,
    expected_argc: int,
) -> dict[str, Any]:
    stringdata = int(discovered["stringdata"])
    metadata = int(discovered["metadata"])
    method_data = int(discovered["method_data"])
    method_count = int(discovered["method_count"])
    name_indexes = set(view.string_indexes(stringdata, name))
    rows: list[dict[str, Any]] = []
    for index in range(method_count):
        row = tuple(
            view.u32(metadata + 4 * (method_data + 6 * index + item))
            for item in range(6)
        )
        if row[0] not in name_indexes:
            continue
        if row[1] != expected_argc:
            continue
        params = [
            view.u32(metadata + 4 * (row[2] + item))
            for item in range(expected_argc + 1)
        ]
        rows.append({"index": index, "row": list(row), "params": params})
    if len(rows) != 1 or rows[0]["index"] != expected_index:
        raise RuntimeError(f"QMETA_NAMED_METHOD_CHANGED:{name}:{rows!r}")
    result = rows[0]
    result["dispatch"] = view.dispatch_from_metacall(
        int(discovered["metaobject"]["static_metacall"]),
        method_count=method_count,
        target_index=expected_index,
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args(argv)

    view = BinaryView(args.client)
    rtti = {
        name: {
            "mangled": mangled,
            "class_name": class_name,
            "vptr": view.exact_rtti_vptr(mangled),
        }
        for name, (mangled, class_name) in RTTI_NAMES.items()
    }

    game = discover_class(
        view,
        class_name="tibia::client::TGameClient",
        method_count=44,
        target_name="onRequestLoginWithCredentials",
        target_index=17,
        argc=2,
    )
    if game["target_params"] != [0x2B, 0x0A, 0x0A]:
        raise RuntimeError(f"GAME_CLIENT_AUTH_PARAM_TYPES_CHANGED:{game['target_params']!r}")

    character = discover_class(
        view,
        class_name="tibia::gamewindow::TCharacterSelectionController",
        method_count=26,
        target_name="requestCharacterLogin",
        target_index=0,
        argc=1,
    )
    character["confirm"] = find_named_method(
        view,
        character,
        name="onCharacterSelectionConfirmed",
        expected_index=11,
        expected_argc=1,
    )

    gameserver = discover_class(
        view,
        class_name="tibia::authentication::TAuthenticationProcessController",
        method_count=51,
        target_name="requestCharacterGameserverLogin",
        target_index=5,
        argc=0,
    )
    gameserver["start"] = find_named_method(
        view,
        gameserver,
        name="onStartGameServerLoginStateEntered",
        expected_index=27,
        expected_argc=0,
    )

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
