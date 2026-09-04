#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

CONNECTIMPL_CALLSITE = 0x7C6B9F
RECEIVER_FIELD_OFFSET = 0x88
ADAPTER_TARGET = 0xBD3050
PROMOTED_SENDER = "tibia::authentication::TLoginProtocolMessageHandler"
PROMOTED_SIGNAL = "sendLoginMessage"
PROMOTED_RECEIVER_PROVENANCE = "OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]"
CONNECTIMPL_RECEIVER_REG = "rcx"
OBJECT_TIED_THIS_REGISTER = "rdi"
CALLER_SAVED = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


class Image:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections: list[tuple[int, int, int, int]] = []
        for sec in self.elf.iter_sections():
            start = int(sec["sh_addr"])
            size = int(sec["sh_size"])
            off = int(sec["sh_offset"])
            flags = int(sec["sh_flags"])
            if start and size:
                self.sections.append((start, start + size, off, flags))

        self.relative_relocations: dict[int, int] = {}
        self.symbol_relocations: dict[int, str] = {}
        for sec in self.elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                addr = int(rel["r_offset"])
                if int(rel["r_info_type"]) == 8 and rel.is_RELA():
                    self.relative_relocations[addr] = int(rel["r_addend"]) & 0xFFFFFFFFFFFFFFFF
                idx = int(rel["r_info_sym"])
                if symtab is not None and idx:
                    try:
                        name = symtab.get_symbol(idx).name or ""
                    except Exception:
                        name = ""
                    if name:
                        self.symbol_relocations[addr] = name

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

    def loc(self, va: int, size: int = 1) -> int:
        for lo, hi, off, _flags in self.sections:
            if lo <= va and va + size <= hi:
                return off + va - lo
        raise ValueError(f"unmapped {hx(va)}")

    def read(self, va: int, size: int) -> bytes:
        off = self.loc(va, size)
        return self.raw[off : off + size]

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def qword(self, va: int) -> int | None:
        if va in self.relative_relocations:
            return self.relative_relocations[va]
        try:
            return int.from_bytes(self.read(va, 8), "little")
        except Exception:
            return None

    def cstring(self, va: int, limit: int = 512) -> str | None:
        try:
            off = self.loc(va)
        except Exception:
            return None
        end = self.raw.find(b"\0", off, min(len(self.raw), off + limit))
        if end < 0:
            return None
        try:
            return self.raw[off:end].decode("utf-8")
        except UnicodeDecodeError:
            return None

    def plt_symbol(self, target: int) -> str | None:
        try:
            rows = self.disassemble(target, target + 24)
        except Exception:
            return None
        for ins in rows[:4]:
            if ins.mnemonic != "jmp" or not ins.operands:
                continue
            op = ins.operands[0]
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                got = int(ins.address) + int(ins.size) + int(op.mem.disp)
                if got in self.symbol_relocations:
                    return self.symbol_relocations[got]
        return None


def demangle(symbol: str | None, type_name: bool = False) -> str | None:
    if not symbol:
        return None
    cmd = ["c++filt"] + (["-t"] if type_name else []) + [symbol]
    try:
        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, timeout=2)
        return proc.stdout.strip() or symbol
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
    if ins.mnemonic not in ("call", "jmp") or not ins.operands or ins.operands[0].type != X86_OP_IMM:
        return None
    return int(ins.operands[0].imm)


def stack_deltas(img: Image, instructions: list[Any]) -> list[int]:
    delta = 0
    before: list[int] = []
    for ins in instructions:
        before.append(delta)
        if ins.mnemonic in ("sub", "add") and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_REG and canonical_reg(img, dst.reg) == "rsp" and src.type == X86_OP_IMM:
                amount = int(src.imm)
                delta += -amount if ins.mnemonic == "sub" else amount
        elif ins.mnemonic == "push":
            delta -= 8
        elif ins.mnemonic == "pop":
            delta += 8
    return before


def stack_key(img: Image, ins: Any, delta_before: int, operand_index: int) -> int | None:
    if operand_index >= len(ins.operands):
        return None
    op = ins.operands[operand_index]
    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RSP:
        return None
    return delta_before + int(op.mem.disp)


def resolve_stack_slot(
    img: Image,
    instructions: list[Any],
    before: int,
    wanted_key: int,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 12:
        return {"classification": "UNKNOWN", "reason": "MAX_STACK_DEPTH"}
    for i in range(before - 1, -1, -1):
        ins = instructions[i]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        if stack_key(img, ins, deltas[i], 0) != wanted_key:
            continue
        src = ins.operands[1]
        row: dict[str, Any] = {"site": hx(int(ins.address)), "stack_key": wanted_key, "op_str": ins.op_str}
        if src.type == X86_OP_REG:
            nested = resolve_register(img, instructions, i, canonical_reg(img, src.reg), deltas, depth + 1)
            row.update({"classification": nested.get("classification", "UNKNOWN"), "source": nested})
        elif src.type == X86_OP_IMM:
            row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
        elif src.type == X86_OP_MEM:
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            nested = resolve_register(img, instructions, i, base, deltas, depth + 1) if base != "none" else None
            row.update(
                {
                    "classification": "OBJECT_FIELD",
                    "base_register": base,
                    "displacement": hx(int(src.mem.disp)),
                    "base": nested,
                }
            )
        else:
            row.update({"classification": "UNKNOWN", "reason": "UNSUPPORTED_STACK_STORE_SOURCE"})
        return row
    return {"classification": "UNKNOWN", "reason": "NO_STACK_STORE_FOR_KEY", "stack_key": wanted_key}


def resolve_register(
    img: Image,
    instructions: list[Any],
    before: int,
    wanted: str,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 12:
        return {"classification": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    for i in range(before - 1, -1, -1):
        ins = instructions[i]
        if ins.mnemonic == "call" and wanted in CALLER_SAVED:
            return {"classification": "UNKNOWN", "reason": "CALL_CLOBBER_BOUNDARY", "boundary_site": hx(int(ins.address))}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        row: dict[str, Any] = {"definition_site": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = resolve_register(img, instructions, i, via, deltas, depth + 1)
                row.update({"classification": nested.get("classification", "UNKNOWN"), "via_register": via, "source": nested})
                return row
            if src.type == X86_OP_IMM:
                row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return row
            if src.type == X86_OP_MEM:
                if src.mem.base == X86_REG_RSP:
                    key = deltas[i] + int(src.mem.disp)
                    nested = resolve_stack_slot(img, instructions, i, key, deltas, depth + 1)
                    row.update({"classification": nested.get("classification", "UNKNOWN"), "stack_key": key, "source": nested})
                    return row
                if src.mem.base == X86_REG_RIP:
                    addr = int(ins.address) + int(ins.size) + int(src.mem.disp)
                    row.update({"classification": "STATIC_POINTER_LOAD", "address": hx(addr)})
                    return row
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                nested = resolve_register(img, instructions, i, base, deltas, depth + 1) if base != "none" else None
                row.update(
                    {
                        "classification": "OBJECT_FIELD",
                        "base_register": base,
                        "displacement": hx(int(src.mem.disp)),
                        "base": nested,
                    }
                )
                return row
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            if src.mem.base == X86_REG_RIP and not src.mem.index:
                addr = int(ins.address) + int(ins.size) + int(src.mem.disp)
                row.update({"classification": "STATIC_ADDRESS", "address": hx(addr)})
                return row
            if src.mem.base and not src.mem.index:
                base = canonical_reg(img, src.mem.base)
                nested = resolve_register(img, instructions, i, base, deltas, depth + 1)
                row.update(
                    {
                        "classification": "OBJECT_ADDRESS",
                        "base_register": base,
                        "displacement": hx(int(src.mem.disp)),
                        "base": nested,
                    }
                )
                return row
        if ins.mnemonic == "xor" and src is not None and src.type == X86_OP_REG and canonical_reg(img, src.reg) == wanted:
            row.update({"classification": "CONSTANT", "value": "0x0"})
            return row
        row.update({"classification": "UNKNOWN", "reason": "UNSUPPORTED_REGISTER_DEFINITION"})
        return row
    return {"classification": f"ENTRY_ARG:{wanted}", "reason": "NO_BOUNDED_DEFINITION"}


def walk_dict(value: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(value, dict):
        out.append(value)
        for nested in value.values():
            out.extend(walk_dict(nested))
    elif isinstance(value, list):
        for nested in value:
            out.extend(walk_dict(nested))
    return out


def anchored_to_entry_rdi(value: Any) -> bool:
    return any(row.get("classification") == "ENTRY_ARG:rdi" for row in walk_dict(value))


def receiver_field_leaves(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in walk_dict(value):
        if (
            row.get("classification") == "OBJECT_FIELD"
            and row.get("base_register") == "rbx"
            and row.get("displacement") == hx(RECEIVER_FIELD_OFFSET)
            and anchored_to_entry_rdi(row.get("base"))
        ):
            rows.append(row)
    return rows


def prove_hidden_sret(img: Image, instructions: list[Any], call_index: int) -> dict[str, Any]:
    storage_reg = None
    storage_site = None
    for i in range(call_index - 1, max(-1, call_index - 24), -1):
        ins = instructions[i]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type == X86_OP_REG and src.type == X86_OP_REG and canonical_reg(img, dst.reg) == "rdi":
            storage_reg = canonical_reg(img, src.reg)
            storage_site = hx(int(ins.address))
            break
    if storage_reg is None:
        return {"proven": False, "reason": "CONNECTIMPL_HIDDEN_SRET_STORAGE_NOT_FOUND"}

    for i in range(call_index + 1, min(len(instructions), call_index + 24)):
        ins = instructions[i]
        target = direct_target(ins)
        if ins.mnemonic != "call" or target is None:
            continue
        dm = demangle(img.plt_symbol(target))
        if not dm or not dm.startswith("QMetaObject::Connection::~Connection()"):
            continue
        arg_reg = None
        arg_site = None
        for j in range(i - 1, call_index, -1):
            prev = instructions[j]
            if not prev.mnemonic.startswith("mov") or len(prev.operands) < 2:
                continue
            dst, src = prev.operands[0], prev.operands[1]
            if dst.type == X86_OP_REG and src.type == X86_OP_REG and canonical_reg(img, dst.reg) == "rdi":
                arg_reg = canonical_reg(img, src.reg)
                arg_site = hx(int(prev.address))
                break
        proven = arg_reg == storage_reg and arg_reg is not None
        return {
            "proven": proven,
            "storage_register": storage_reg,
            "storage_definition_site": storage_site,
            "destructor_callsite": hx(int(ins.address)),
            "destructor_argument_register": arg_reg,
            "destructor_argument_definition_site": arg_site,
            "reason": "none" if proven else "CONNECTIMPL_HIDDEN_SRET_STORAGE_MISMATCH",
        }
    return {
        "proven": False,
        "storage_register": storage_reg,
        "storage_definition_site": storage_site,
        "reason": "CONNECTION_DESTRUCTOR_NOT_FOUND_AFTER_CONNECTIMPL",
    }


def resolve_receiver_argument(img: Image, instructions: list[Any], call_index: int) -> dict[str, Any]:
    deltas = stack_deltas(img, instructions)
    resolved = resolve_register(img, instructions, call_index, CONNECTIMPL_RECEIVER_REG, deltas)
    leaves = receiver_field_leaves(resolved)
    sites = sorted({str(row.get("definition_site")) for row in leaves if row.get("definition_site")})
    proven = len(leaves) == 1 and len(sites) == 1
    return {
        "proven": proven,
        "provenance": PROMOTED_RECEIVER_PROVENANCE if proven else "UNKNOWN",
        "field_leaf_count": len(leaves),
        "field_load_sites": sites,
        "slice": resolved,
    }


def classify_receiver_field_value_use(
    img: Image,
    instructions: list[Any],
    call_index: int,
    receiver: dict[str, Any],
    hidden_sret: dict[str, Any],
) -> dict[str, Any]:
    call = instructions[call_index]
    target = direct_target(call)
    dm = demangle(img.plt_symbol(target)) if target is not None else None
    primitive_ok = bool(dm and "QObject::connectImpl(" in dm)
    proven = bool(receiver.get("proven")) and bool(hidden_sret.get("proven")) and primitive_ok
    return {
        "proven": proven,
        "classification": "QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT" if proven else "UNKNOWN",
        "callsite": hx(int(call.address)),
        "target": hx(target),
        "demangled": dm,
        "formal_receiver_register": CONNECTIMPL_RECEIVER_REG if hidden_sret.get("proven") else "UNKNOWN",
        "receiver_field_load_sites": receiver.get("field_load_sites", []),
        "missing": (
            "none"
            if proven
            else "EXACT_RECEIVER_FIELD_TO_CONNECTIMPL_RECEIVER_ARGUMENT_HANDOFF_NOT_PROVEN"
        ),
    }


def same_receiver_field_value(value: Any, exact_load_site: str) -> bool:
    return any(
        row.get("classification") == "OBJECT_FIELD"
        and row.get("base_register") == "rbx"
        and row.get("displacement") == hx(RECEIVER_FIELD_OFFSET)
        and row.get("definition_site") == exact_load_site
        and anchored_to_entry_rdi(row.get("base"))
        for row in walk_dict(value)
    )


def rtti_from_vptr(img: Image, vptr: int) -> dict[str, Any] | None:
    typeinfo = img.qword(vptr - 8)
    if not typeinfo:
        return None
    name_ptr = img.qword(typeinfo + 8)
    if not name_ptr:
        return None
    raw_name = img.cstring(name_ptr)
    if not raw_name or len(raw_name) > 300:
        return None
    type_name = demangle(raw_name, type_name=True)
    if not type_name:
        return None
    return {"vptr": hx(vptr), "typeinfo": hx(typeinfo), "type_name_raw": raw_name, "type_name": type_name}


def inspect_constructor_vptr_edge(img: Image, target: int) -> dict[str, Any]:
    fde = img.containing_fde(target)
    if not fde or fde[1] - fde[0] > 0x4000:
        return {"identity_proven": False, "reason": "TYPE_EDGE_CALLEE_NOT_BOUNDED"}
    insns = img.disassemble(*fde)
    deltas = stack_deltas(img, insns)
    candidates: list[dict[str, Any]] = []
    for i, ins in enumerate(insns[:96]):
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or not dst.mem.base or dst.mem.index or int(dst.mem.disp) != 0:
            continue
        base = resolve_register(img, insns, i, canonical_reg(img, dst.mem.base), deltas)
        if base.get("classification") != "ENTRY_ARG:rdi":
            continue
        value: int | None = None
        if src.type == X86_OP_REG:
            resolved = resolve_register(img, insns, i, canonical_reg(img, src.reg), deltas)
            if resolved.get("classification") == "STATIC_ADDRESS" and resolved.get("address"):
                value = int(str(resolved["address"]), 16)
        elif src.type == X86_OP_IMM:
            value = int(src.imm) & 0xFFFFFFFFFFFFFFFF
        if value is None:
            continue
        rtti = rtti_from_vptr(img, value)
        if rtti:
            candidates.append({"store_site": hx(int(ins.address)), "callee_fde": [hx(fde[0]), hx(fde[1])], **rtti})
    types = sorted({str(row["type_name"]) for row in candidates})
    proven = len(types) == 1 and len(candidates) >= 1
    return {
        "identity_proven": proven,
        "identity": types[0] if proven else "UNKNOWN",
        "proof_class": "OBJECT_TIED_CALLEE_PRIMARY_VPTR_ITANIUM_RTTI" if proven else "none",
        "candidates": candidates,
        "reason": "none" if proven else ("TYPE_EDGE_PRIMARY_VPTR_RTTI_NOT_FOUND" if not candidates else "TYPE_EDGE_RTTI_NOT_UNIQUE"),
    }


def find_unique_object_tied_type_edge(
    img: Image,
    instructions: list[Any],
    call_index: int,
    receiver: dict[str, Any],
) -> dict[str, Any]:
    sites = receiver.get("field_load_sites", [])
    if len(sites) != 1:
        return {"proven": False, "candidate_count": 0, "candidates": [], "missing": "RECEIVER_FIELD_LOAD_SITE_NOT_UNIQUE"}
    load_site = str(sites[0])
    load_addr = int(load_site, 16)
    indexes = [i for i, ins in enumerate(instructions) if int(ins.address) == load_addr]
    if len(indexes) != 1 or indexes[0] >= call_index:
        return {"proven": False, "candidate_count": 0, "candidates": [], "missing": "RECEIVER_FIELD_LOAD_NOT_IN_IMMEDIATE_PRE_CONNECT_SLICE"}
    load_index = indexes[0]
    deltas = stack_deltas(img, instructions)
    candidates: list[dict[str, Any]] = []

    # This scan is deliberately restricted to the exact value lifetime from its defining
    # field load to the selected connectImpl call. No owner-FDE/global census is performed.
    for i in range(load_index + 1, call_index):
        ins = instructions[i]
        target = direct_target(ins)
        if ins.mnemonic == "call" and target is not None:
            resolved_this = resolve_register(img, instructions, i, OBJECT_TIED_THIS_REGISTER, deltas)
            if same_receiver_field_value(resolved_this, load_site):
                candidates.append(
                    {
                        "kind": "DIRECT_CALL_WITH_EXACT_RECEIVER_FIELD_VALUE",
                        "site": hx(int(ins.address)),
                        "target": hx(target),
                        "symbol": img.plt_symbol(target),
                        "demangled": demangle(img.plt_symbol(target)),
                        "matching_arguments": [
                            {"register": OBJECT_TIED_THIS_REGISTER, "resolution": resolved_this}
                        ],
                    }
                )

        for op_index, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or not op.mem.base or op.mem.index or int(op.mem.disp) != 0:
                continue
            base_reg = canonical_reg(img, op.mem.base)
            resolved_base = resolve_register(img, instructions, i, base_reg, deltas)
            if not same_receiver_field_value(resolved_base, load_site):
                continue
            candidates.append(
                {
                    "kind": "PRIMARY_OBJECT_ZERO_OFFSET_DEREFERENCE",
                    "site": hx(int(ins.address)),
                    "op_str": ins.op_str,
                    "operand_index": op_index,
                    "base_register": base_reg,
                    "base_resolution": resolved_base,
                }
            )

    # Deduplicate one instruction that is both a call argument preparation consumer and
    # a zero-offset dereference record only by its semantic key; distinct uses remain distinct.
    unique: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in candidates:
        unique[(str(row.get("kind")), str(row.get("site")), str(row.get("target", row.get("op_str", ""))))] = row
    candidates = list(unique.values())

    if not candidates:
        return {
            "proven": False,
            "candidate_count": 0,
            "candidates": [],
            "load_site": load_site,
            "slice_end": hx(int(instructions[call_index].address)),
            "missing": "NO_UNIQUE_OBJECT_TIED_TYPE_EDGE_IN_EXACT_FIELD_VALUE_LIFETIME",
        }
    if len(candidates) != 1:
        return {
            "proven": False,
            "candidate_count": len(candidates),
            "candidates": candidates,
            "load_site": load_site,
            "slice_end": hx(int(instructions[call_index].address)),
            "missing": "OBJECT_TIED_TYPE_EDGE_NOT_UNIQUE_IN_EXACT_FIELD_VALUE_LIFETIME",
        }

    edge = candidates[0]
    if edge["kind"] == "PRIMARY_OBJECT_ZERO_OFFSET_DEREFERENCE":
        return {
            "proven": False,
            "candidate_count": 1,
            "candidates": candidates,
            "selected_edge": edge,
            "load_site": load_site,
            "slice_end": hx(int(instructions[call_index].address)),
            "missing": "PRIMARY_VPTR_VALUE_RUNTIME_DEPENDENT_NO_STATIC_RTTI_BINDING",
        }

    matching_regs = [row["register"] for row in edge.get("matching_arguments", [])]
    if OBJECT_TIED_THIS_REGISTER not in matching_regs:
        return {
            "proven": False,
            "candidate_count": 1,
            "candidates": candidates,
            "selected_edge": edge,
            "load_site": load_site,
            "slice_end": hx(int(instructions[call_index].address)),
            "missing": "UNIQUE_OBJECT_TIED_CALL_DOES_NOT_CARRY_RECEIVER_AS_THIS",
        }

    target = int(str(edge["target"]), 16)
    identity = inspect_constructor_vptr_edge(img, target)
    return {
        "proven": bool(identity.get("identity_proven")),
        "candidate_count": 1,
        "candidates": candidates,
        "selected_edge": edge,
        "identity": identity,
        "load_site": load_site,
        "slice_end": hx(int(instructions[call_index].address)),
        "missing": "none" if identity.get("identity_proven") else str(identity.get("reason", "UNIQUE_OBJECT_TIED_TYPE_EDGE_DID_NOT_PROVE_IDENTITY")),
    }


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={sha}")

    img = Image(client)
    try:
        fde = img.containing_fde(CONNECTIMPL_CALLSITE)
        if not fde:
            raise RuntimeError("selected connectImpl callsite is not uniquely contained in one FDE")
        instructions = img.disassemble(*fde)
        indexes = [i for i, ins in enumerate(instructions) if int(ins.address) == CONNECTIMPL_CALLSITE]
        if len(indexes) != 1:
            raise RuntimeError("selected connectImpl callsite is not unique in containing FDE")
        call_index = indexes[0]
        call = instructions[call_index]
        target = direct_target(call)
        dm = demangle(img.plt_symbol(target)) if target is not None else None
        if call.mnemonic != "call" or target is None or not dm or "QObject::connectImpl(" not in dm:
            raise RuntimeError(f"selected call no longer resolves to QObject::connectImpl: {dm}")

        hidden_sret = prove_hidden_sret(img, instructions, call_index)
        receiver = resolve_receiver_argument(img, instructions, call_index)
        use = classify_receiver_field_value_use(img, instructions, call_index, receiver, hidden_sret)

        if use["proven"]:
            type_edge = find_unique_object_tied_type_edge(img, instructions, call_index, receiver)
        else:
            type_edge = {"proven": False, "candidate_count": 0, "candidates": [], "missing": use["missing"]}

        identity_proven = bool(type_edge.get("proven"))
        identity = "UNKNOWN"
        proof_classes: list[str] = []
        if identity_proven:
            identity_data = type_edge.get("identity", {})
            identity = str(identity_data.get("identity", "UNKNOWN"))
            proof_class = str(identity_data.get("proof_class", "none"))
            if identity != "UNKNOWN" and proof_class != "none":
                proof_classes = [proof_class]
            else:
                identity_proven = False
                identity = "UNKNOWN"

        pair_proven = identity_proven
        causal_proven = identity_proven
        terminal = "SENDLOGIN_RECEIVER_FIELD_USE_IDENTITY_PROVEN" if identity_proven else "SOURCE_BLOCKER"
        missing = "none" if identity_proven else str(type_edge.get("missing", use.get("missing", "UNKNOWN")))

        result = {
            "schema": "otclient.track-a.be4f48-sendlogin-receiver-field-88-use-semantics.v1",
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
            "sendlogin_sender_identity": PROMOTED_SENDER,
            "sendlogin_signal": PROMOTED_SIGNAL,
            "sendlogin_connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
            "sendlogin_connectimpl_target": hx(target),
            "sendlogin_connectimpl_demangled": dm,
            "sendlogin_adapter_target": hx(ADAPTER_TARGET),
            "connectimpl_hidden_sret_proof": hidden_sret,
            "sendlogin_receiver_provenance": receiver.get("provenance", "UNKNOWN"),
            "receiver_argument_resolution": receiver,
            "receiver_field_value_use": use.get("classification", "UNKNOWN"),
            "receiver_field_value_use_proven": bool(use.get("proven")),
            "receiver_field_value_use_evidence": use,
            "object_tied_type_edge": type_edge,
            "sendlogin_receiver_identity": identity,
            "sendlogin_receiver_identity_proven": identity_proven,
            "sendlogin_receiver_identity_proof_classes": proof_classes,
            "complete_sender_receiver_pair_proven": pair_proven,
            "sendlogin_causal_binding_proven": causal_proven,
            "pre_success_send_sequence": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal,
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
