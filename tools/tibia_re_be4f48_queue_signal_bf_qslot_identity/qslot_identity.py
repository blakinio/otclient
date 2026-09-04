#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.sections import SymbolTableSection

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

QUEUE_SIGNAL_INDEX = 0xBF
QUEUE_SIGNAL_BODY = 0xBD2190
CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)
CONNECTIMPL_CALLSITE = 0xBE2EEE
QSLOT_PRODUCER_CALLSITE = 0xBE2EB1
QSLOT_CONSTRUCTION_WINDOW = (0xBE2E80, 0xBE2EEE)
QSLOT_IMPL_STORE_SITE = 0xBE2EBF
QSLOT_IMPL_REGISTER = "r13"
QSLOT_PAYLOAD_SOURCE_LEA = 0xBE2E86
QSLOT_PAYLOAD_HIGH_ZERO_STORE = 0xBE2E8D
QSLOT_PAYLOAD_LOW_STACK_STORE = 0xBE2E9A
QSLOT_PAYLOAD_XMM_LOAD = 0xBE2EB6
QSLOT_PAYLOAD_STORE_SITE = 0xBE2ED6
QSLOT_DISPATCH_CALL_BRANCH = (0xBE4E38, 0xBE4E52)
MAX_SLOT_TARGET_INSTRUCTIONS = 192
MAX_REGISTER_TRANSFER_HOPS = 4


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


@dataclass(frozen=True)
class Section:
    offset: int
    size: int
    va: int
    flags: int
    name: str


class Image:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections = [
            Section(
                offset=int(sec["sh_offset"]),
                size=int(sec["sh_size"]),
                va=int(sec["sh_addr"]),
                flags=int(sec["sh_flags"]),
                name=sec.name,
            )
            for sec in self.elf.iter_sections()
            if int(sec["sh_size"]) > 0
        ]
        self.relocations: dict[int, dict[str, Any]] = {}
        self.symbols: dict[int, list[str]] = {}
        for sec in self.elf.iter_sections():
            if isinstance(sec, SymbolTableSection):
                for sym in sec.iter_symbols():
                    value = int(sym["st_value"])
                    name = sym.name or ""
                    if value and name:
                        self.symbols.setdefault(value, []).append(name)
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                symbol = None
                sym_index = int(rel["r_info_sym"])
                if symtab is not None and sym_index:
                    try:
                        symbol = symtab.get_symbol(sym_index).name or None
                    except Exception:
                        symbol = None
                self.relocations[int(rel["r_offset"])] = {
                    "addend": int(rel.entry.get("r_addend", 0)),
                    "symbol": symbol,
                }
        dwarf = self.elf.get_dwarf_info()
        self.fdes = sorted(
            (int(entry["initial_location"]), int(entry["initial_location"]) + int(entry["address_range"]))
            for entry in dwarf.EH_CFI_entries()
            if isinstance(entry, FDE)
        )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def close(self) -> None:
        self.handle.close()

    def va_to_off(self, va: int) -> int:
        for sec in self.sections:
            if sec.va <= va < sec.va + sec.size:
                return sec.offset + va - sec.va
        raise ValueError(f"unmapped VA {hx(va)}")

    def read(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def qword(self, va: int) -> int | None:
        rel = self.relocations.get(va)
        if rel and rel.get("addend"):
            return int(rel["addend"]) & 0xFFFFFFFFFFFFFFFF
        if not self.mapped(va, 8):
            return None
        return struct.unpack("<Q", self.read(va, 8))[0]

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def is_executable_va(self, va: int) -> bool:
        return any((sec.flags & 0x4) and sec.va <= va < sec.va + sec.size for sec in self.sections)

    def symbol_names(self, va: int) -> list[str]:
        return sorted(set(self.symbols.get(va, [])))

    def plt_symbol(self, target: int) -> str | None:
        if not self.mapped(target, 6):
            return None
        try:
            insns = self.disassemble(target, target + 24)
        except Exception:
            return None
        for ins in insns[:4]:
            if ins.mnemonic != "jmp" or not ins.operands:
                continue
            op = ins.operands[0]
            if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                continue
            got = int(ins.address) + int(ins.size) + int(op.mem.disp)
            rel = self.relocations.get(got)
            if rel and rel.get("symbol"):
                return str(rel["symbol"])
        return None


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        result = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
        return result.stdout.strip() or symbol
    except Exception:
        return symbol


def canonical_reg(img: Image, reg: int) -> str:
    name = img.md.reg_name(reg)
    aliases = {
        "eax": "rax", "ax": "rax", "al": "rax", "ah": "rax",
        "ebx": "rbx", "bx": "rbx", "bl": "rbx", "bh": "rbx",
        "ecx": "rcx", "cx": "rcx", "cl": "rcx", "ch": "rcx",
        "edx": "rdx", "dx": "rdx", "dl": "rdx", "dh": "rdx",
        "esi": "rsi", "si": "rsi", "sil": "rsi",
        "edi": "rdi", "di": "rdi", "dil": "rdi",
        "ebp": "rbp", "bp": "rbp", "bpl": "rbp",
        "esp": "rsp", "sp": "rsp", "spl": "rsp",
    }
    if name in aliases:
        return aliases[name]
    for n in range(8, 16):
        if name in (f"r{n}d", f"r{n}w", f"r{n}b"):
            return f"r{n}"
    return name


def direct_target(ins: Any) -> int | None:
    if ins.mnemonic not in ("call", "jmp") or not ins.operands:
        return None
    return int(ins.operands[0].imm) if ins.operands[0].type == X86_OP_IMM else None


def rip_target(ins: Any) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return int(ins.address) + int(ins.size) + int(op.mem.disp)
    return None


def instruction_at(insns: list[Any], address: int) -> Any | None:
    rows = [ins for ins in insns if int(ins.address) == address]
    return rows[0] if len(rows) == 1 else None


def explicit_register_write(img: Image, ins: Any, register: str) -> bool:
    try:
        _, written = ins.regs_access()
        return any(canonical_reg(img, reg) == register for reg in written)
    except Exception:
        return bool(
            ins.mnemonic.startswith(("mov", "lea", "pop"))
            and ins.operands
            and ins.operands[0].type == X86_OP_REG
            and canonical_reg(img, ins.operands[0].reg) == register
        )


def memory_operand_matches(img: Image, op: Any, base: str, disp: int) -> bool:
    return bool(
        op.type == X86_OP_MEM
        and canonical_reg(img, op.mem.base) == base
        and int(op.mem.disp) == disp
    )


def target_identity(img: Image, target: int | None) -> dict[str, Any]:
    if target is None:
        return {"target": None, "symbol": None, "demangled": None, "fde": None}
    direct_symbols = img.symbol_names(target)
    symbol = img.plt_symbol(target) or (direct_symbols[0] if len(direct_symbols) == 1 else None)
    fde = img.containing_fde(target)
    return {
        "target": hx(target),
        "symbol": symbol,
        "demangled": demangle(symbol),
        "direct_symbols": direct_symbols,
        "fde": [hx(fde[0]), hx(fde[1])] if fde else None,
    }


def resolve_qslot_producer(img: Image) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
        "connectimpl_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "qslot_producer_callsite": hx(QSLOT_PRODUCER_CALLSITE),
        "handoff": "UNKNOWN",
        "allocation_size": "UNKNOWN",
    }
    fde = img.containing_fde(CONNECTIMPL_CALLSITE)
    if fde != CONNECTIMPL_FDE:
        result["classification"] = "CONNECTIMPL_FDE_MISMATCH"
        result["actual_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result
    insns = img.disassemble(*CONNECTIMPL_FDE)
    connect = instruction_at(insns, CONNECTIMPL_CALLSITE)
    alloc = instruction_at(insns, QSLOT_PRODUCER_CALLSITE)
    if connect is None or connect.mnemonic != "call":
        result["classification"] = "CONNECTIMPL_CALLSITE_NOT_EXACT"
        return result
    connect_identity = target_identity(img, direct_target(connect))
    result["connectimpl_target"] = connect_identity
    if "QObject::connectImpl(" not in str(connect_identity.get("demangled") or ""):
        result["classification"] = "CONNECTIMPL_TARGET_IDENTITY_MISMATCH"
        return result
    if alloc is None or alloc.mnemonic != "call":
        result["classification"] = "QSLOT_ALLOCATION_CALLSITE_NOT_EXACT"
        return result
    allocation_identity = target_identity(img, direct_target(alloc))
    result["allocation_target"] = allocation_identity
    if "operator new" not in str(allocation_identity.get("demangled") or ""):
        result["classification"] = "QSLOT_ALLOCATION_TARGET_NOT_OPERATOR_NEW"
        return result

    alloc_index = insns.index(alloc)
    connect_index = insns.index(connect)
    for ins in reversed(insns[max(0, alloc_index - 16) : alloc_index]):
        if ins.mnemonic == "call":
            break
        if not explicit_register_write(img, ins, "rdi"):
            continue
        if len(ins.operands) >= 2 and ins.operands[1].type == X86_OP_IMM:
            result["allocation_size"] = hx(int(ins.operands[1].imm) & 0xFFFFFFFFFFFFFFFF)
            result["allocation_size_site"] = hx(int(ins.address))
        break

    handoffs = []
    for index in range(alloc_index + 1, connect_index):
        ins = insns[index]
        if (
            ins.mnemonic == "mov"
            and len(ins.operands) >= 2
            and ins.operands[0].type == X86_OP_REG
            and ins.operands[1].type == X86_OP_REG
            and canonical_reg(img, ins.operands[0].reg) == "r9"
            and canonical_reg(img, ins.operands[1].reg) == "rax"
        ):
            handoffs.append((index, ins))
    if len(handoffs) != 1:
        result["classification"] = "QSLOT_RAX_TO_R9_HANDOFF_NOT_UNIQUE"
        result["handoff_sites"] = [hx(int(ins.address)) for _, ins in handoffs]
        return result
    handoff_index, handoff = handoffs[0]
    intervening_calls = [ins for ins in insns[alloc_index + 1 : handoff_index] if ins.mnemonic == "call"]
    if intervening_calls:
        result["classification"] = "QSLOT_ALLOCATION_TO_HANDOFF_HAS_INTERVENING_CALL"
        result["intervening_calls"] = [hx(int(ins.address)) for ins in intervening_calls]
        return result
    for ins in insns[alloc_index + 1 : handoff_index]:
        if explicit_register_write(img, ins, "rax"):
            result["classification"] = "QSLOT_ALLOCATION_RAX_REDEFINED_BEFORE_HANDOFF"
            result["redefinition_site"] = hx(int(ins.address))
            return result
    for ins in insns[handoff_index + 1 : connect_index]:
        if explicit_register_write(img, ins, "r9"):
            result["classification"] = "QSLOT_R9_REDEFINED_BEFORE_CONNECTIMPL"
            result["redefinition_site"] = hx(int(ins.address))
            return result

    result.update({
        "classification": "QSLOT_FRESH_ALLOCATION_TO_CONNECT_HANDOFF_PROVEN",
        "proven": True,
        "allocation_callsite": hx(QSLOT_PRODUCER_CALLSITE),
        "handoff": f"{hx(int(handoff.address))}: r9 <- rax",
        "handoff_site": hx(int(handoff.address)),
    })
    return result


def resolve_qslot_construction_window(img: Image, producer: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "window": [hx(QSLOT_CONSTRUCTION_WINDOW[0]), hx(QSLOT_CONSTRUCTION_WINDOW[1])],
        "instructions": [],
        "object_field_writes": [],
    }
    if not producer.get("proven"):
        result["classification"] = "QSLOT_PRODUCER_NOT_PROVEN"
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    result["instructions"] = [
        {"address": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        for ins in insns
        if QSLOT_CONSTRUCTION_WINDOW[0] <= int(ins.address) < QSLOT_CONSTRUCTION_WINDOW[1]
    ]
    alloc = instruction_at(insns, QSLOT_PRODUCER_CALLSITE)
    connect = instruction_at(insns, CONNECTIMPL_CALLSITE)
    handoff_site = int(str(producer["handoff_site"]), 16)
    handoff = instruction_at(insns, handoff_site)
    if alloc is None or connect is None or handoff is None:
        result["classification"] = "CONSTRUCTION_BOUNDARY_INSTRUCTION_MISSING"
        return result
    alloc_index = insns.index(alloc)
    connect_index = insns.index(connect)
    handoff_index = insns.index(handoff)
    if not (alloc_index < handoff_index < connect_index):
        result["classification"] = "CONSTRUCTION_BOUNDARY_ORDER_INVALID"
        return result

    object_aliases: set[str] = {"rax"}
    object_field_writes: list[dict[str, Any]] = []
    for ins in insns[alloc_index + 1 : connect_index]:
        if ins.mnemonic == "call":
            result["classification"] = "CONSTRUCTION_WINDOW_HAS_INTERVENING_CALL"
            result["intervening_callsite"] = hx(int(ins.address))
            return result
        if not ins.operands:
            continue
        dst = ins.operands[0]
        src = ins.operands[1] if len(ins.operands) > 1 else None
        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_REG and src is not None:
            dst_reg = canonical_reg(img, dst.reg)
            if src.type == X86_OP_REG and canonical_reg(img, src.reg) in object_aliases:
                object_aliases.add(dst_reg)
            else:
                object_aliases.discard(dst_reg)
            continue
        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_MEM and src is not None:
            base = canonical_reg(img, dst.mem.base) if dst.mem.base else None
            if base not in object_aliases:
                continue
            row: dict[str, Any] = {
                "store_site": hx(int(ins.address)),
                "base_register": base,
                "field_offset": hx(int(dst.mem.disp)),
                "op_str": ins.op_str,
                "source_kind": "UNKNOWN",
            }
            if src.type == X86_OP_REG:
                row["source_kind"] = f"REGISTER:{canonical_reg(img, src.reg)}"
            elif src.type == X86_OP_IMM:
                row["source_kind"] = "IMMEDIATE"
                row["immediate"] = hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)
            elif src.type == X86_OP_MEM:
                row["source_kind"] = "MEMORY"
                target = rip_target(ins)
                if target is not None:
                    row["source_address"] = hx(target)
            object_field_writes.append(row)

    result.update({
        "classification": "QSLOT_INLINE_CONSTRUCTION_WINDOW_PROVEN",
        "proven": True,
        "fresh_object_origin": f"operator new return @ {hx(QSLOT_PRODUCER_CALLSITE)}",
        "allocation_size": producer.get("allocation_size", "UNKNOWN"),
        "handoff_site": hx(handoff_site),
        "object_field_writes": object_field_writes,
    })
    return result


def trace_qslot_impl_register(img: Image, construction: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "store_site": hx(QSLOT_IMPL_STORE_SITE),
        "register": QSLOT_IMPL_REGISTER,
        "target": "UNKNOWN",
        "trace": [],
    }
    if not construction.get("proven"):
        result["classification"] = "QSLOT_CONSTRUCTION_WINDOW_NOT_PROVEN"
        return result
    store_rows = [row for row in construction.get("object_field_writes", []) if row.get("store_site") == hx(QSLOT_IMPL_STORE_SITE)]
    if len(store_rows) != 1:
        result["classification"] = "QSLOT_IMPL_STORE_SITE_NOT_UNIQUE"
        result["store_rows"] = store_rows
        return result
    store_row = store_rows[0]
    result["store"] = store_row
    if store_row.get("field_offset") != "0x8" or store_row.get("source_kind") != f"REGISTER:{QSLOT_IMPL_REGISTER}":
        result["classification"] = "QSLOT_IMPL_STORE_SHAPE_MISMATCH"
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    store = instruction_at(insns, QSLOT_IMPL_STORE_SITE)
    if store is None:
        result["classification"] = "QSLOT_IMPL_STORE_INSTRUCTION_MISSING"
        return result
    cursor = insns.index(store)
    tracked = QSLOT_IMPL_REGISTER
    caller_saved = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
    hops = 0
    while hops <= MAX_REGISTER_TRANSFER_HOPS:
        writer = None
        for index in range(cursor - 1, -1, -1):
            ins = insns[index]
            if ins.mnemonic == "call" and tracked in caller_saved:
                result["classification"] = "QSLOT_IMPL_REGISTER_CLOBBER_BOUNDARY"
                result["clobber_site"] = hx(int(ins.address))
                result["tracked_register"] = tracked
                return result
            if explicit_register_write(img, ins, tracked):
                writer = (index, ins)
                break
        if writer is None:
            result["classification"] = "QSLOT_IMPL_REGISTER_ENTRY_VALUE"
            result["tracked_register"] = tracked
            return result
        index, ins = writer
        step: dict[str, Any] = {
            "address": hx(int(ins.address)),
            "mnemonic": ins.mnemonic,
            "op_str": ins.op_str,
            "register": tracked,
        }
        result["trace"].append(step)
        src = ins.operands[1] if len(ins.operands) > 1 else None
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
            target = rip_target(ins)
            step["source_kind"] = "RIP_EXECUTABLE_ADDRESS"
            step["target"] = hx(target)
            if target is None or not img.is_executable_va(target) or img.containing_fde(target) is None:
                result["classification"] = "QSLOT_IMPL_LEA_TARGET_NOT_EXECUTABLE_FDE"
                return result
            result.update({
                "classification": "QSLOT_IMPL_REGISTER_TARGET_PROVEN",
                "proven": True,
                "target": hx(target),
                "target_identity": target_identity(img, target),
                "source_site": hx(int(ins.address)),
            })
            return result
        if ins.mnemonic.startswith("mov") and src is not None and src.type == X86_OP_IMM:
            target = int(src.imm) & 0xFFFFFFFFFFFFFFFF
            if not img.is_executable_va(target) or img.containing_fde(target) is None:
                result["classification"] = "QSLOT_IMPL_IMMEDIATE_TARGET_NOT_EXECUTABLE_FDE"
                return result
            result.update({
                "classification": "QSLOT_IMPL_REGISTER_TARGET_PROVEN",
                "proven": True,
                "target": hx(target),
                "target_identity": target_identity(img, target),
                "source_site": hx(int(ins.address)),
            })
            return result
        if ins.mnemonic.startswith("mov") and src is not None and src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
            pointer_site = rip_target(ins)
            pointer = img.qword(pointer_site) if pointer_site is not None else None
            if pointer is None or not img.is_executable_va(pointer) or img.containing_fde(pointer) is None:
                result["classification"] = "QSLOT_IMPL_RIP_POINTER_TARGET_NOT_EXECUTABLE_FDE"
                return result
            result.update({
                "classification": "QSLOT_IMPL_REGISTER_TARGET_PROVEN",
                "proven": True,
                "target": hx(pointer),
                "target_identity": target_identity(img, pointer),
                "source_site": hx(int(ins.address)),
            })
            return result
        if ins.mnemonic.startswith("mov") and src is not None and src.type == X86_OP_REG:
            source_reg = canonical_reg(img, src.reg)
            step["source_kind"] = "REGISTER_TRANSFER"
            step["source_register"] = source_reg
            tracked = source_reg
            cursor = index
            hops += 1
            continue
        result["classification"] = "QSLOT_IMPL_REGISTER_WRITER_UNSUPPORTED"
        result["writer"] = step
        return result
    result["classification"] = "QSLOT_IMPL_REGISTER_TRANSFER_HOP_LIMIT"
    return result


def trace_qslot_callable_payload(img: Image, construction: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "payload_store_site": hx(QSLOT_PAYLOAD_STORE_SITE),
        "source_lea_site": hx(QSLOT_PAYLOAD_SOURCE_LEA),
        "target": "UNKNOWN",
        "adjustment": "UNKNOWN",
    }
    if not construction.get("proven"):
        result["classification"] = "QSLOT_CONSTRUCTION_WINDOW_NOT_PROVEN"
        return result
    rows = [row for row in construction.get("object_field_writes", []) if row.get("store_site") == hx(QSLOT_PAYLOAD_STORE_SITE)]
    if len(rows) != 1:
        result["classification"] = "QSLOT_PAYLOAD_STORE_SITE_NOT_UNIQUE"
        result["store_rows"] = rows
        return result
    payload_store_row = rows[0]
    result["payload_store"] = payload_store_row
    if payload_store_row.get("field_offset") != "0x10" or payload_store_row.get("source_kind") != "REGISTER:xmm5":
        result["classification"] = "QSLOT_PAYLOAD_STORE_SHAPE_MISMATCH"
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    source_lea = instruction_at(insns, QSLOT_PAYLOAD_SOURCE_LEA)
    high_zero = instruction_at(insns, QSLOT_PAYLOAD_HIGH_ZERO_STORE)
    low_store = instruction_at(insns, QSLOT_PAYLOAD_LOW_STACK_STORE)
    xmm_load = instruction_at(insns, QSLOT_PAYLOAD_XMM_LOAD)
    payload_store = instruction_at(insns, QSLOT_PAYLOAD_STORE_SITE)
    if None in (source_lea, high_zero, low_store, xmm_load, payload_store):
        result["classification"] = "QSLOT_PAYLOAD_EXACT_CHAIN_INSTRUCTION_MISSING"
        return result
    assert source_lea is not None and high_zero is not None and low_store is not None and xmm_load is not None and payload_store is not None

    if not (
        source_lea.mnemonic == "lea"
        and len(source_lea.operands) >= 2
        and source_lea.operands[0].type == X86_OP_REG
        and canonical_reg(img, source_lea.operands[0].reg) == "rax"
        and rip_target(source_lea) == QUEUE_SIGNAL_BODY
    ):
        result["classification"] = "QSLOT_PAYLOAD_SOURCE_LEA_MISMATCH"
        return result
    if not (
        low_store.mnemonic.startswith("mov")
        and len(low_store.operands) >= 2
        and memory_operand_matches(img, low_store.operands[0], "rbp", -0x60)
        and low_store.operands[1].type == X86_OP_REG
        and canonical_reg(img, low_store.operands[1].reg) == "rax"
    ):
        result["classification"] = "QSLOT_PAYLOAD_LOW_STACK_STORE_MISMATCH"
        return result
    if not (
        high_zero.mnemonic.startswith("mov")
        and len(high_zero.operands) >= 2
        and memory_operand_matches(img, high_zero.operands[0], "rbp", -0x58)
        and high_zero.operands[1].type == X86_OP_IMM
        and int(high_zero.operands[1].imm) == 0
    ):
        result["classification"] = "QSLOT_PAYLOAD_HIGH_ZERO_STORE_MISMATCH"
        return result
    if not (
        xmm_load.mnemonic == "movdqa"
        and len(xmm_load.operands) >= 2
        and xmm_load.operands[0].type == X86_OP_REG
        and canonical_reg(img, xmm_load.operands[0].reg) == "xmm5"
        and memory_operand_matches(img, xmm_load.operands[1], "rbp", -0x60)
    ):
        result["classification"] = "QSLOT_PAYLOAD_XMM_LOAD_MISMATCH"
        return result
    if not (
        payload_store.mnemonic == "movups"
        and len(payload_store.operands) >= 2
        and memory_operand_matches(img, payload_store.operands[0], "rax", 0x10)
        and payload_store.operands[1].type == X86_OP_REG
        and canonical_reg(img, payload_store.operands[1].reg) == "xmm5"
    ):
        result["classification"] = "QSLOT_PAYLOAD_FINAL_STORE_MISMATCH"
        return result

    low_index = insns.index(low_store)
    lea_index = insns.index(source_lea)
    for ins in insns[lea_index + 1 : low_index]:
        if explicit_register_write(img, ins, "rax"):
            result["classification"] = "QSLOT_PAYLOAD_RAX_REDEFINED_BEFORE_LOW_STORE"
            result["redefinition_site"] = hx(int(ins.address))
            return result
    xmm_index = insns.index(xmm_load)
    payload_index = insns.index(payload_store)
    for ins in insns[xmm_index + 1 : payload_index]:
        if explicit_register_write(img, ins, "xmm5"):
            result["classification"] = "QSLOT_PAYLOAD_XMM5_REDEFINED_BEFORE_OBJECT_STORE"
            result["redefinition_site"] = hx(int(ins.address))
            return result

    target = rip_target(source_lea)
    if target is None or not img.is_executable_va(target) or img.containing_fde(target) is None:
        result["classification"] = "QSLOT_PAYLOAD_TARGET_NOT_EXECUTABLE_FDE"
        return result
    result.update({
        "classification": "QSLOT_CALLABLE_PAYLOAD_PAIR_PROVEN",
        "proven": True,
        "target": hx(target),
        "target_identity": target_identity(img, target),
        "adjustment": 0,
        "low_stack_store_site": hx(QSLOT_PAYLOAD_LOW_STACK_STORE),
        "high_zero_store_site": hx(QSLOT_PAYLOAD_HIGH_ZERO_STORE),
        "xmm_load_site": hx(QSLOT_PAYLOAD_XMM_LOAD),
        "payload_pair": [hx(target), "0x0"],
    })
    return result


def prove_dispatch_to_payload(
    img: Image,
    impl_provenance: dict[str, Any],
    callable_payload: dict[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "branch_window": [hx(QSLOT_DISPATCH_CALL_BRANCH[0]), hx(QSLOT_DISPATCH_CALL_BRANCH[1])],
        "dispatcher_target": impl_provenance.get("target", "UNKNOWN"),
        "callable_target": callable_payload.get("target", "UNKNOWN"),
    }
    if not impl_provenance.get("proven") or not callable_payload.get("proven"):
        result["classification"] = "QSLOT_DISPATCH_INPUT_PROOF_MISSING"
        return result
    dispatcher = int(str(impl_provenance["target"]), 16)
    fde = img.containing_fde(dispatcher)
    if fde is None or not (fde[0] <= QSLOT_DISPATCH_CALL_BRANCH[0] < QSLOT_DISPATCH_CALL_BRANCH[1] <= fde[1]):
        result["classification"] = "QSLOT_DISPATCH_BRANCH_NOT_IN_IMPL_FDE"
        result["dispatcher_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result
    insns = img.disassemble(*fde)
    branch = [ins for ins in insns if QSLOT_DISPATCH_CALL_BRANCH[0] <= int(ins.address) < QSLOT_DISPATCH_CALL_BRANCH[1]]
    result["instructions"] = [
        {"address": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        for ins in branch
    ]
    required = {
        0xBE4E38: ("mov", "rcx", "rsi", 0x10),
        0xBE4E3C: ("add", "rdx", "rsi", 0x18),
        0xBE4E43: ("test", "cl", None, None),
        0xBE4E46: ("je", None, None, None),
        0xBE4E50: ("jmp", "rcx", None, None),
    }
    for address, (mnemonic, reg, mem_base, mem_disp) in required.items():
        ins = instruction_at(insns, address)
        if ins is None or ins.mnemonic != mnemonic:
            result["classification"] = "QSLOT_DISPATCH_REQUIRED_INSTRUCTION_MISMATCH"
            result["mismatch_site"] = hx(address)
            return result
        if address in (0xBE4E38, 0xBE4E3C):
            if len(ins.operands) < 2 or ins.operands[0].type != X86_OP_REG or canonical_reg(img, ins.operands[0].reg) != reg:
                result["classification"] = "QSLOT_DISPATCH_REGISTER_SHAPE_MISMATCH"
                result["mismatch_site"] = hx(address)
                return result
            if not memory_operand_matches(img, ins.operands[1], str(mem_base), int(mem_disp)):
                result["classification"] = "QSLOT_DISPATCH_PAYLOAD_OFFSET_MISMATCH"
                result["mismatch_site"] = hx(address)
                return result
        if address == 0xBE4E43:
            if len(ins.operands) < 2 or ins.operands[0].type != X86_OP_REG or canonical_reg(img, ins.operands[0].reg) != "rcx" or ins.operands[1].type != X86_OP_IMM or int(ins.operands[1].imm) != 1:
                result["classification"] = "QSLOT_DISPATCH_LOWBIT_TEST_MISMATCH"
                return result
        if address == 0xBE4E46:
            if not ins.operands or ins.operands[0].type != X86_OP_IMM or int(ins.operands[0].imm) != 0xBE4E50:
                result["classification"] = "QSLOT_DISPATCH_DIRECT_BRANCH_TARGET_MISMATCH"
                return result
        if address == 0xBE4E50:
            if not ins.operands or ins.operands[0].type != X86_OP_REG or canonical_reg(img, ins.operands[0].reg) != "rcx":
                result["classification"] = "QSLOT_DISPATCH_FINAL_JUMP_MISMATCH"
                return result

    callable_target = int(str(callable_payload["target"]), 16)
    adjustment = int(callable_payload.get("adjustment", 1))
    if callable_target & 1:
        result["classification"] = "QSLOT_PAYLOAD_IS_VIRTUAL_MEMBER_POINTER_VARIANT"
        return result
    if adjustment != 0:
        result["classification"] = "QSLOT_PAYLOAD_NONZERO_THIS_ADJUSTMENT"
        return result
    result.update({
        "classification": "QSLOT_DISPATCH_DIRECT_CALLABLE_TARGET_PROVEN",
        "proven": True,
        "dispatcher_fde": [hx(fde[0]), hx(fde[1])],
        "payload_function_offset": "0x10",
        "payload_adjustment_offset": "0x18",
        "lowbit": callable_target & 1,
        "direct_jump_site": "0xbe4e50",
    })
    return result


def bounded_target_summary(img: Image, target: int) -> dict[str, Any]:
    fde = img.containing_fde(target)
    if fde is None:
        return {"classification": "TARGET_FDE_NOT_PROVEN", "target": hx(target)}
    insns = img.disassemble(*fde)
    prefix = insns[:MAX_SLOT_TARGET_INSTRUCTIONS]
    calls = []
    for ins in prefix:
        if ins.mnemonic != "call":
            continue
        calls.append({"site": hx(int(ins.address)), **target_identity(img, direct_target(ins))})
    return {
        "classification": "BOUNDED_SLOT_TARGET_SUMMARY",
        "target": hx(target),
        "fde": [hx(fde[0]), hx(fde[1])],
        "instruction_count": len(insns),
        "summary_instruction_limit": MAX_SLOT_TARGET_INSTRUCTIONS,
        "fully_within_limit": len(insns) <= MAX_SLOT_TARGET_INSTRUCTIONS,
        "direct_calls_in_bounded_prefix": calls,
        "instruction_prefix": [
            {"address": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
            for ins in prefix
        ],
    }


def resolve_qslot_function(
    img: Image,
    producer: dict[str, Any],
    construction: dict[str, Any],
    impl_provenance: dict[str, Any],
    callable_payload: dict[str, Any],
    dispatch_proof: dict[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "function_target": "UNKNOWN",
        "proof_basis": "fresh 0x20 QSlotObjectBase allocation; +0x8 dispatcher; exact +0x10/+0x18 callable payload pair; dispatcher direct-member-pointer branch",
    }
    if not producer.get("proven") or not construction.get("proven"):
        result["classification"] = "QSLOT_OBJECT_CONSTRUCTION_NOT_PROVEN"
        return result
    if producer.get("allocation_size") != "0x20":
        result["classification"] = "QSLOT_ALLOCATION_SIZE_NOT_0X20"
        return result
    writes = list(construction.get("object_field_writes") or [])
    refcount = [row for row in writes if row.get("field_offset") == "0x0" and row.get("source_kind") == "IMMEDIATE" and row.get("immediate") == "0x1"]
    impl = [row for row in writes if row.get("store_site") == hx(QSLOT_IMPL_STORE_SITE) and row.get("field_offset") == "0x8" and row.get("source_kind") == f"REGISTER:{QSLOT_IMPL_REGISTER}"]
    payload = [row for row in writes if row.get("store_site") == hx(QSLOT_PAYLOAD_STORE_SITE) and row.get("field_offset") == "0x10" and row.get("source_kind") == "REGISTER:xmm5"]
    result["layout_cross_check"] = {
        "allocation_size": producer.get("allocation_size"),
        "refcount_init_candidates": refcount,
        "impl_store_candidates": impl,
        "payload_store_candidates": payload,
    }
    if len(refcount) != 1 or len(impl) != 1 or len(payload) != 1:
        result["classification"] = "QSLOT_OBJECT_LAYOUT_CROSS_CHECK_FAILED"
        return result
    if not impl_provenance.get("proven"):
        result["classification"] = str(impl_provenance.get("classification") or "QSLOT_IMPL_REGISTER_TARGET_NOT_PROVEN")
        return result
    if not callable_payload.get("proven"):
        result["classification"] = str(callable_payload.get("classification") or "QSLOT_CALLABLE_PAYLOAD_NOT_PROVEN")
        return result
    if not dispatch_proof.get("proven"):
        result["classification"] = str(dispatch_proof.get("classification") or "QSLOT_DISPATCH_TO_PAYLOAD_NOT_PROVEN")
        return result
    target = int(str(callable_payload["target"]), 16)
    result.update({
        "classification": "QSLOT_CALLABLE_TARGET_PROVEN",
        "proven": True,
        "function_target": hx(target),
        "function_target_identity": target_identity(img, target),
        "dispatch_impl_target": impl_provenance.get("target"),
        "dispatch_impl_identity": impl_provenance.get("target_identity"),
        "function_pointer_store": payload[0],
        "function_target_summary": bounded_target_summary(img, target),
    })
    return result


def trace_one_writer_edge(img: Image, slot: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "writer_identity": "UNKNOWN",
        "next_edge": "UNKNOWN",
    }
    if not slot.get("proven"):
        result["classification"] = "QSLOT_IDENTITY_NOT_PROVEN"
        return result
    target = int(str(slot["function_target"]), 16)
    summary = bounded_target_summary(img, target)
    result["slot_target_summary"] = summary
    calls = list(summary.get("direct_calls_in_bounded_prefix") or [])
    result["direct_call_candidates"] = calls
    if not summary.get("fully_within_limit"):
        result["classification"] = "NEXT_WRITER_EDGE_WITHHELD_TARGET_EXCEEDS_BOUND"
    elif not calls:
        result["classification"] = "NEXT_WRITER_EDGE_NO_DIRECT_CALL_IN_SLOT_TARGET"
    else:
        result["classification"] = "NEXT_WRITER_EDGE_SEMANTICS_NOT_UNIQUELY_PROVEN"
    return result


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")
    img = Image(client)
    try:
        producer = resolve_qslot_producer(img)
        construction = resolve_qslot_construction_window(img, producer)
        impl_provenance = trace_qslot_impl_register(img, construction)
        callable_payload = trace_qslot_callable_payload(img, construction)
        dispatch_proof = prove_dispatch_to_payload(img, impl_provenance, callable_payload)
        slot = resolve_qslot_function(img, producer, construction, impl_provenance, callable_payload, dispatch_proof)
        writer = trace_one_writer_edge(img, slot)
        qslot_identity_proven = bool(slot.get("proven"))

        if not producer.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(producer.get("classification") or "QSLOT_PRODUCER_NOT_PROVEN")
        elif not construction.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(construction.get("classification") or "QSLOT_CONSTRUCTION_NOT_PROVEN")
        elif not impl_provenance.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(impl_provenance.get("classification") or "QSLOT_IMPL_REGISTER_TARGET_NOT_PROVEN")
        elif not callable_payload.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(callable_payload.get("classification") or "QSLOT_CALLABLE_PAYLOAD_NOT_PROVEN")
        elif not dispatch_proof.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(dispatch_proof.get("classification") or "QSLOT_DISPATCH_TO_PAYLOAD_NOT_PROVEN")
        elif not qslot_identity_proven:
            terminal_result = "SOURCE_BLOCKER"
            missing = str(slot.get("classification") or "QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN")
        elif writer.get("proven"):
            terminal_result = "FINAL_WRITER_EDGE_PROVEN"
            missing = "NONE"
        else:
            terminal_result = "QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN"
            missing = str(writer.get("classification") or "NEXT_WRITER_EDGE_NOT_UNIQUELY_PROVEN")

        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-qslot-identity.v4",
            "runtime_access": "none",
            "official_client_executed": False,
            "login_performed": False,
            "credentials_used": False,
            "process_memory_access": False,
            "packet_capture": False,
            "ocr_vision_used": False,
            "official_service_e2e_count": 0,
            "track_b_pr_284_modified": False,
            "exact_client": {"version": EXPECTED_VERSION, "size": EXPECTED_SIZE, "sha256": EXPECTED_SHA256},
            "queue_sender_identity": "tibia::protocol::TProtocolMessageQueue",
            "queue_signal_name": "clientMessageReadyToProcess",
            "queue_signal_index": QUEUE_SIGNAL_INDEX,
            "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
            "queue_signal_body": hx(QUEUE_SIGNAL_BODY),
            "queue_signal_argv1_identity": "exact GameclientMessage shared pair",
            "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
            "connectimpl_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
            "queue_signal_receiver_provenance": "ENTRY_ARG:rdi",
            "qslot_producer_callsite": hx(QSLOT_PRODUCER_CALLSITE),
            "qslot_object_producer": producer,
            "qslot_construction_window": construction,
            "qslot_impl_register_provenance": impl_provenance,
            "qslot_callable_payload_provenance": callable_payload,
            "qslot_dispatch_proof": dispatch_proof,
            "qslot_dispatch_impl_target": impl_provenance.get("target", "UNKNOWN"),
            "qslot_function_target": slot.get("function_target", "UNKNOWN"),
            "qslot_identity_proven": qslot_identity_proven,
            "qslot_function_proof": slot,
            "queue_signal_writer_identity": writer.get("writer_identity", "UNKNOWN"),
            "next_unique_writer_edge": writer.get("next_edge", "UNKNOWN"),
            "writer_edge_proof": writer,
            "final_queue_writer_identified": bool(writer.get("proven")),
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal_result,
            "FIRST_MISSING_BOUNDARY": missing,
        }
    finally:
        img.close()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.client, args.output)


if __name__ == "__main__":
    main()
