#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
PEER_TARGET = 0xD052A0
HELPER_TARGET = 0x4D8670
ADAPTER_TARGET = 0xBD3050
CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)
MAX_VTABLE_BACKSCAN = 0x200
MAX_STATIC_REFS = 32


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def signed64(value: int) -> int:
    value &= 0xFFFFFFFFFFFFFFFF
    return value - (1 << 64) if value & (1 << 63) else value


def is_plausible_offset_to_top(value: int) -> bool:
    return -0x10000 <= value <= 0x10000


def demangle_type(name: str) -> str:
    try:
        p = subprocess.run(
            ["c++filt", "-t", name],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return name
    value = p.stdout.strip()
    return value if p.returncode == 0 and value else name


@dataclass(frozen=True)
class Section:
    name: str
    offset: int
    size: int
    va: int
    flags: int


class Image:
    def __init__(self, path: Path):
        # Heavy analysis dependencies intentionally stay out of module import so the
        # repository-only TDD contract runs before apt/package materialization.
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import (
            X86_OP_IMM,
            X86_OP_MEM,
            X86_OP_REG,
            X86_REG_RIP,
            X86_REG_RSP,
        )
        from elftools.dwarf.callframe import FDE
        from elftools.elf.elffile import ELFFile
        from elftools.elf.relocation import RelocationSection

        self.X86_OP_IMM = X86_OP_IMM
        self.X86_OP_MEM = X86_OP_MEM
        self.X86_OP_REG = X86_OP_REG
        self.X86_REG_RIP = X86_REG_RIP
        self.X86_REG_RSP = X86_REG_RSP
        self.raw = path.read_bytes()
        self.rel: dict[int, int] = {}
        self.symbols: dict[int, str] = {}
        with path.open("rb") as fh:
            elf = ELFFile(fh)
            self.sections = [
                Section(
                    s.name,
                    int(s["sh_offset"]),
                    int(s["sh_size"]),
                    int(s["sh_addr"]),
                    int(s["sh_flags"]),
                )
                for s in elf.iter_sections()
                if int(s["sh_size"])
            ]
            for sec in elf.iter_sections():
                if isinstance(sec, RelocationSection):
                    for row in sec.iter_relocations():
                        if row.is_RELA():
                            self.rel[int(row["r_offset"])] = int(row["r_addend"]) & 0xFFFFFFFFFFFFFFFF
            dynsym = elf.get_section_by_name(".dynsym")
            if dynsym is not None:
                for symbol in dynsym.iter_symbols():
                    value = int(symbol["st_value"])
                    name = symbol.name
                    if value and name:
                        self.symbols.setdefault(value, name)
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (
                    int(entry["initial_location"]),
                    int(entry["initial_location"]) + int(entry["address_range"]),
                )
                for entry in dwarf.EH_CFI_entries()
                if isinstance(entry, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def va_to_off(self, va: int) -> int:
        for sec in self.sections:
            if sec.va <= va < sec.va + sec.size:
                return sec.offset + va - sec.va
        raise ValueError(hex(va))

    def off_to_va(self, off: int) -> int | None:
        for sec in self.sections:
            if sec.offset <= off < sec.offset + sec.size:
                return sec.va + off - sec.offset
        return None

    def section_for_va(self, va: int) -> Section | None:
        for sec in self.sections:
            if sec.va <= va < sec.va + sec.size:
                return sec
        return None

    def mapped(self, va: int, size: int = 1) -> bool:
        sec = self.section_for_va(va)
        if sec is None or va + size > sec.va + sec.size:
            return False
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        sec = self.section_for_va(va)
        return bool(sec is not None and (sec.flags & 4))

    def non_executable(self, va: int) -> bool:
        sec = self.section_for_va(va)
        return bool(sec is not None and not (sec.flags & 4))

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def u64(self, va: int) -> int:
        return struct.unpack_from("<Q", self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        return self.rel.get(va, self.u64(va) if self.mapped(va, 8) else 0)

    def fde(self, va: int) -> tuple[int, int] | None:
        rows = [row for row in self.fdes if row[0] <= va < row[1]]
        return rows[0] if len(rows) == 1 else None

    def instructions(self, fde: tuple[int, int]):
        if fde[0] >= fde[1] or not self.mapped(fde[0], fde[1] - fde[0]):
            return []
        return list(self.md.disasm(self.bytes(fde[0], fde[1] - fde[0]), fde[0]))

    def exec_instructions(self):
        for sec in self.sections:
            if not (sec.flags & 4):
                continue
            raw = self.raw[sec.offset : sec.offset + sec.size]
            yield from self.md.disasm(raw, sec.va)

    def read_cstring(self, va: int, limit: int = 512) -> str | None:
        if not self.mapped(va):
            return None
        try:
            off = self.va_to_off(va)
        except ValueError:
            return None
        end = self.raw.find(b"\0", off, min(len(self.raw), off + limit))
        if end < 0 or end == off:
            return None
        try:
            return self.raw[off:end].decode("ascii")
        except UnicodeDecodeError:
            return None

    def symbol_for(self, va: int) -> str | None:
        return self.symbols.get(va)


def rip_target(img: Image, ins) -> int | None:
    for op in ins.operands:
        if op.type == img.X86_OP_MEM and op.mem.base == img.X86_REG_RIP:
            return ins.address + ins.size + int(op.mem.disp)
    return None


def direct_target(img: Image, ins) -> int | None:
    if ins.mnemonic not in ("call", "jmp") or not ins.operands:
        return None
    op = ins.operands[0]
    if op.type != img.X86_OP_IMM:
        return None
    value = int(op.imm)
    return value if img.executable(value) else None


def first_tail_and_calls(img: Image, fde: tuple[int, int]) -> tuple[int | None, list[int]]:
    tail = None
    calls: list[int] = []
    for ins in img.instructions(fde):
        target = direct_target(img, ins)
        if target is None:
            continue
        if ins.mnemonic == "call":
            calls.append(target)
        elif ins.mnemonic == "jmp" and tail is None:
            tail = target
    return tail, sorted(set(calls))


def pointer_slots(img: Image, target: int) -> list[int]:
    found = {where for where, value in img.rel.items() if value == target and img.non_executable(where)}
    needle = struct.pack("<Q", target)
    pos = 0
    while True:
        pos = img.raw.find(needle, pos)
        if pos < 0:
            break
        va = img.off_to_va(pos)
        if va is not None and va % 8 == 0 and img.non_executable(va):
            found.add(va)
        pos += 1
    return sorted(found)


def plausible_type_name(value: str | None) -> bool:
    if not value or len(value) > 384:
        return False
    if not re.fullmatch(r"[A-Za-z0-9_.$]+", value):
        return False
    return value[0].isdigit() or value[0] in "NZ"


def vtable_memberships(img: Image, target: int, kind: str) -> list[dict]:
    rows: dict[tuple[int, int, str, int], dict] = {}
    for slot in pointer_slots(img, target):
        for slot_offset in range(0, MAX_VTABLE_BACKSCAN + 1, 8):
            address_point = slot - slot_offset
            header = address_point - 16
            if not img.mapped(header, 16):
                continue
            offset_to_top = signed64(img.qword(header))
            if not is_plausible_offset_to_top(offset_to_top):
                continue
            typeinfo = img.qword(header + 8)
            if not typeinfo or not img.non_executable(typeinfo) or not img.mapped(typeinfo + 8, 8):
                continue
            name_ptr = img.qword(typeinfo + 8)
            if not name_ptr or not img.non_executable(name_ptr):
                continue
            mangled = img.read_cstring(name_ptr)
            if not plausible_type_name(mangled):
                continue
            executable_prefix = 0
            for delta in range(0, 0x40, 8):
                if img.mapped(address_point + delta, 8) and img.executable(img.qword(address_point + delta)):
                    executable_prefix += 1
            if executable_prefix < 2:
                continue
            key = (address_point, typeinfo, mangled, slot_offset)
            rows[key] = {
                "target_kind": kind,
                "pointer_slot": hx(slot),
                "address_point": hx(address_point),
                "slot_offset": hex(slot_offset),
                "offset_to_top": offset_to_top,
                "typeinfo": hx(typeinfo),
                "mangled_type": mangled,
                "demangled_type": demangle_type(mangled),
                "executable_entries_first_0x40": executable_prefix,
            }
    return sorted(rows.values(), key=lambda row: (row["address_point"], row["slot_offset"], row["mangled_type"]))


def constructor_xrefs_and_callers(
    img: Image,
    address_points: set[int],
    callable_targets: set[int],
) -> tuple[list[dict], list[dict]]:
    xrefs: list[dict] = []
    callers: list[dict] = []
    seen_xrefs: set[tuple[int, int]] = set()
    seen_callers: set[tuple[int, int, str]] = set()
    for ins in img.exec_instructions():
        if len(xrefs) < MAX_STATIC_REFS and address_points:
            target = rip_target(img, ins)
            if target in address_points:
                fde = img.fde(ins.address)
                if fde is not None and (ins.address, target) not in seen_xrefs:
                    seen_xrefs.add((ins.address, target))
                    store_after = False
                    dst_reg = ins.operands[0].reg if ins.operands and ins.operands[0].type == img.X86_OP_REG else None
                    local = img.instructions(fde)
                    indexes = [i for i, row in enumerate(local) if row.address == ins.address]
                    if len(indexes) == 1 and dst_reg is not None:
                        for row in local[indexes[0] + 1 : indexes[0] + 9]:
                            if row.mnemonic.startswith("mov") and len(row.operands) >= 2:
                                dst, src = row.operands[0], row.operands[1]
                                if dst.type == img.X86_OP_MEM and src.type == img.X86_OP_REG and src.reg == dst_reg:
                                    store_after = True
                                    break
                    xrefs.append(
                        {
                            "site": hx(ins.address),
                            "address_point": hx(target),
                            "caller_fde": [hx(fde[0]), hx(fde[1])],
                            "mnemonic": ins.mnemonic,
                            "op_str": ins.op_str,
                            "followed_by_pointer_store_within_8": store_after,
                        }
                    )
        if len(callers) < MAX_STATIC_REFS:
            target = direct_target(img, ins)
            if target in callable_targets:
                fde = img.fde(ins.address)
                if fde is not None:
                    key = (fde[0], target, ins.mnemonic)
                    if key not in seen_callers:
                        seen_callers.add(key)
                        callers.append(
                            {
                                "site": hx(ins.address),
                                "kind": ins.mnemonic,
                                "target": hx(target),
                                "caller_fde": [hx(fde[0]), hx(fde[1])],
                            }
                        )
        if len(xrefs) >= MAX_STATIC_REFS and len(callers) >= MAX_STATIC_REFS:
            break
    return xrefs, callers


_REG_ALIASES = {
    "rax": {"rax", "eax", "ax", "al", "ah"},
    "rbx": {"rbx", "ebx", "bx", "bl", "bh"},
    "rcx": {"rcx", "ecx", "cx", "cl", "ch"},
    "rdx": {"rdx", "edx", "dx", "dl", "dh"},
    "rsi": {"rsi", "esi", "si", "sil"},
    "rdi": {"rdi", "edi", "di", "dil"},
    "rbp": {"rbp", "ebp", "bp", "bpl"},
    "rsp": {"rsp", "esp", "sp", "spl"},
}
for _n in range(8, 16):
    _REG_ALIASES[f"r{_n}"] = {f"r{_n}", f"r{_n}d", f"r{_n}w", f"r{_n}b"}


def canonical_reg(name: str) -> str:
    for canonical, aliases in _REG_ALIASES.items():
        if name in aliases:
            return canonical
    return name


def mem_disp_text(value: int) -> str:
    return f"+0x{value:x}" if value >= 0 else f"-0x{-value:x}"


def classify_function_target(value: int) -> str:
    if value == ADAPTER_TARGET:
        return "ADAPTER_FUNCTION"
    if value == PEER_TARGET:
        return "PEER_FUNCTION"
    return f"FUNCTION:{hx(value)}"


def resolve_register(img: Image, window: list, before: int, wanted: str, depth: int = 0) -> dict:
    wanted = canonical_reg(wanted)
    if depth > 6:
        return {"classification": "UNKNOWN", "reason": "MAX_REGISTER_SLICE_DEPTH"}
    for idx in range(before - 1, -1, -1):
        ins = window[idx]
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != img.X86_OP_REG or canonical_reg(img.md.reg_name(dst.reg)) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        base = {"definition_site": hx(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        if ins.mnemonic == "lea" and src is not None and src.type == img.X86_OP_MEM:
            if src.mem.base == img.X86_REG_RIP:
                target = ins.address + ins.size + int(src.mem.disp)
                base["classification"] = classify_function_target(target)
                base["target"] = hx(target)
                return base
            base_name = canonical_reg(img.md.reg_name(src.mem.base)) if src.mem.base else "none"
            if base_name == "rsp":
                base["classification"] = "STACK_TEMP"
                base["stack_displacement"] = mem_disp_text(int(src.mem.disp))
                return base
            base["classification"] = f"OBJECT_ADDRESS:{base_name}{mem_disp_text(int(src.mem.disp))}"
            return base
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == img.X86_OP_IMM:
                base["classification"] = "CONSTANT"
                base["value"] = hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)
                return base
            if src.type == img.X86_OP_REG:
                resolved = resolve_register(img, window, idx, img.md.reg_name(src.reg), depth + 1)
                base["classification"] = resolved.get("classification", "UNKNOWN")
                base["via_register"] = canonical_reg(img.md.reg_name(src.reg))
                base["source"] = resolved
                return base
            if src.type == img.X86_OP_MEM:
                base_name = canonical_reg(img.md.reg_name(src.mem.base)) if src.mem.base else "none"
                if base_name == "rsp":
                    base["classification"] = "STACK_TEMP"
                    base["stack_displacement"] = mem_disp_text(int(src.mem.disp))
                else:
                    base["classification"] = f"OBJECT_FIELD:{base_name}{mem_disp_text(int(src.mem.disp))}"
                return base
        if ins.mnemonic == "xor" and src is not None and src.type == img.X86_OP_REG:
            if canonical_reg(img.md.reg_name(src.reg)) == wanted:
                base["classification"] = "CONSTANT"
                base["value"] = "0x0"
                return base
        base["classification"] = "UNKNOWN"
        base["reason"] = "UNSUPPORTED_DEFINITION"
        return base
    return {"classification": "UNKNOWN", "reason": "NO_BOUNDED_DEFINITION"}


def connection_callsite(img: Image) -> dict:
    instructions = img.instructions(CONNECTION_OWNER_FDE)
    adapter_indexes = [i for i, ins in enumerate(instructions) if rip_target(img, ins) == ADAPTER_TARGET]
    if len(adapter_indexes) != 1:
        return {
            "classification": "UNKNOWN_ADAPTER_REFERENCE_COUNT",
            "adapter_reference_count": len(adapter_indexes),
            "owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        }
    adapter_idx = adapter_indexes[0]
    helper_rows = []
    for idx in range(adapter_idx, min(len(instructions), adapter_idx + 33)):
        ins = instructions[idx]
        if ins.mnemonic == "call" and direct_target(img, ins) == HELPER_TARGET:
            helper_rows.append(idx)
    if len(helper_rows) != 1:
        return {
            "classification": "UNKNOWN_HELPER_CALL_COUNT",
            "adapter_reference_site": hx(instructions[adapter_idx].address),
            "helper_call_count": len(helper_rows),
            "owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        }
    helper_idx = helper_rows[0]
    start = max(0, adapter_idx - 40)
    window = instructions[start : helper_idx + 1]
    call_local_idx = len(window) - 1
    args = {}
    for reg in ("rdi", "rsi", "rdx", "rcx", "r8", "r9"):
        args[reg] = resolve_register(img, window, call_local_idx, reg)

    stack_args = []
    for idx, ins in enumerate(window[:-1]):
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != img.X86_OP_MEM or dst.mem.base != img.X86_REG_RSP:
            continue
        row = {"site": hx(ins.address), "stack_displacement": mem_disp_text(int(dst.mem.disp)), "op_str": ins.op_str}
        if src.type == img.X86_OP_REG:
            row["source"] = resolve_register(img, window, idx, img.md.reg_name(src.reg))
        elif src.type == img.X86_OP_IMM:
            row["source"] = {"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)}
        else:
            row["source"] = {"classification": "UNKNOWN"}
        stack_args.append(row)

    relevant = []
    for ins in window:
        rt = rip_target(img, ins)
        is_anchor = rt in (ADAPTER_TARGET, PEER_TARGET)
        has_arg_dst = bool(
            ins.operands
            and ins.operands[0].type == img.X86_OP_REG
            and canonical_reg(img.md.reg_name(ins.operands[0].reg)) in {"rdi", "rsi", "rdx", "rcx", "r8", "r9"}
        )
        has_stack_dst = bool(ins.operands and ins.operands[0].type == img.X86_OP_MEM and ins.operands[0].mem.base == img.X86_REG_RSP)
        if is_anchor or has_arg_dst or has_stack_dst or ins.address == instructions[helper_idx].address:
            relevant.append({"site": hx(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str, "rip_target": hx(rt)})

    return {
        "classification": "BOUNDED_CONNECTION_CALLSITE",
        "owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        "adapter_reference_site": hx(instructions[adapter_idx].address),
        "peer_reference_sites": [hx(ins.address) for ins in window if rip_target(img, ins) == PEER_TARGET],
        "helper_call_site": hx(instructions[helper_idx].address),
        "helper_target": hx(HELPER_TARGET),
        "register_arguments": args,
        "stack_argument_stores": stack_args,
        "relevant_window": relevant,
        "classification_boundary": "ARGUMENT_PROVENANCE_ONLY; NO_QT_SENDER_RECEIVER_DIRECTION_INFERRED_FROM_POSITION_WITHOUT_HELPER_CONTRACT",
    }


def helper_shape(img: Image) -> dict:
    fde = img.fde(HELPER_TARGET)
    if fde is None:
        return {"classification": "UNKNOWN_HELPER_FDE"}
    transfers = []
    for ins in img.instructions(fde):
        target = direct_target(img, ins)
        if target is None:
            continue
        transfers.append(
            {
                "site": hx(ins.address),
                "kind": ins.mnemonic,
                "target": hx(target),
                "symbol": img.symbol_for(target),
            }
        )
    return {
        "classification": "HELPER_FDE_DIRECT_TRANSFER_CENSUS",
        "fde": [hx(fde[0]), hx(fde[1])],
        "direct_transfers": transfers,
    }


def peer_owner_identity(memberships: list[dict], xrefs: list[dict]) -> tuple[str, str, str | None]:
    direct = [row for row in memberships if row["target_kind"] == "PEER_TARGET"]
    rows = direct if direct else memberships
    classes = {(row["mangled_type"], row["demangled_type"]) for row in rows}
    xref_aps = {row["address_point"] for row in xrefs if row["followed_by_pointer_store_within_8"]}
    supported = [row for row in rows if row["address_point"] in xref_aps]
    supported_classes = {(row["mangled_type"], row["demangled_type"]) for row in supported}
    if len(classes) == 1 and len(supported_classes) == 1 and classes == supported_classes:
        mangled, demangled = next(iter(classes))
        role = "DIRECT_VTABLE_MEMBER" if direct else "TAIL_TARGET_VTABLE_MEMBER"
        return demangled, role, mangled
    return "UNKNOWN", "UNKNOWN", None


def analyze(client: Path, output: Path) -> dict:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(
            f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}"
        )
    img = Image(client)
    peer_fde = img.fde(PEER_TARGET)
    if peer_fde is None:
        raise RuntimeError("PEER_FDE_NOT_UNIQUE")
    tail, peer_calls = first_tail_and_calls(img, peer_fde)

    memberships = vtable_memberships(img, PEER_TARGET, "PEER_TARGET")
    if tail is not None:
        memberships.extend(vtable_memberships(img, tail, "PEER_FIRST_UNCONDITIONAL_TAIL_TARGET"))
    memberships = sorted(
        {(
            row["target_kind"], row["pointer_slot"], row["address_point"], row["slot_offset"], row["mangled_type"]
        ): row for row in memberships}.values(),
        key=lambda row: (row["target_kind"], row["address_point"], row["slot_offset"]),
    )
    address_points = {int(row["address_point"], 16) for row in memberships}
    callable_targets = {PEER_TARGET}
    if tail is not None:
        callable_targets.add(tail)
    xrefs, callers = constructor_xrefs_and_callers(img, address_points, callable_targets)
    owner, role, mangled = peer_owner_identity(memberships, xrefs)

    callsite = connection_callsite(img)
    helper = helper_shape(img)

    result = {
        "schema": "otclient.track-a.be4f48-sendlogin-sender-peer.v1",
        "runtime_access": "none",
        "official_client_executed": False,
        "login_performed": False,
        "credentials_used": False,
        "secret_access": False,
        "process_memory_access": False,
        "packet_capture": False,
        "raw_client_uploaded": False,
        "official_service_e2e_count": 0,
        "track_b_pr_284_modified": False,
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "peer_target": hx(PEER_TARGET),
        "connection_helper_target": hx(HELPER_TARGET),
        "sendlogin_adapter_target": hx(ADAPTER_TARGET),
        "peer_callable": {
            "fde": [hx(peer_fde[0]), hx(peer_fde[1])],
            "instruction_count": len(img.instructions(peer_fde)),
            "first_unconditional_tail_target": hx(tail),
            "direct_call_targets": [hx(value) for value in peer_calls],
        },
        "peer_vtable_memberships": memberships,
        "peer_constructor_vtable_xrefs": xrefs,
        "peer_direct_callers": callers,
        "peer_owner_identity": owner,
        "peer_owner_mangled": mangled,
        "peer_role": role,
        "connection_callsite": callsite,
        "connection_helper": helper,
        "sender_endpoint_identity": "UNKNOWN",
        "receiver_endpoint_identity": "UNKNOWN",
        "sendlogin_causal_binding_proven": False,
        "pre_login_sequence_advanced": False,
        "terminal_result": "DISCOVERY_STAGE_1",
        "first_missing_boundary": "QT_HELPER_SENDER_SIGNAL_RECEIVER_SLOT_ARGUMENT_DIRECTION_NOT_PROVEN",
        "classification_boundary": (
            "STAGE_1 MAY PROVE A PEER CLASS/VTABLE OWNER AND LOCAL CALLSITE PROVENANCE; "
            "IT MUST NOT PROMOTE SENDER/RECEIVER DIRECTION WITHOUT AN EXACT HELPER CONTRACT"
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.client, args.output)
    print("BE4F48_SENDLOGIN_SENDER_PEER_ANALYSIS=PASS")
    print("PEER_OWNER_IDENTITY=" + str(result["peer_owner_identity"]))
    print("PEER_ROLE=" + str(result["peer_role"]))
    print("SENDLOGIN_CAUSAL_BINDING_PROVEN=false")


if __name__ == "__main__":
    main()
