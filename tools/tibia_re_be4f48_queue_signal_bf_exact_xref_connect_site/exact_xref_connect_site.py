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

QUEUE_SIGNAL_NAME = "clientMessageReadyToProcess"
QUEUE_SIGNAL_INDEX = 0xBF
QUEUE_SIGNAL_BODY = 0xBD2190
SIGNAL_BODY_FDE = (0xBD2190, 0xBD2495)
ACTIVATE_CALLSITE = 0xBD22C2
QMETAOBJECT_ACTIVATE = 0x4D7DC0
SELF_RELAY_CONNECTIMPL_CALLSITE = 0xBE2EEE
CONSUMED_CONSTRUCTOR_FDE = (0xBE2A50, 0xBE3086)
CONNECTIMPL_TARGET = 0x4D6800
CONNECTIMPL_ABI_SRET = True
PROMOTED_RECEIVER_IDENTITY = "tibia::protocol::TProtocolMessageQueue"
PROMOTED_ARGV1_IDENTITY = "exact GameclientMessage shared pair"
Q_SLOT_FUNCTION_FIELD = 0x10
MAX_LOCAL_BACKWARD_INSTRUCTIONS = 180
MAX_STRING_BYTES = 512


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

    def section_for_va(self, va: int) -> Section | None:
        rows = [sec for sec in self.sections if sec.va <= va < sec.va + sec.size]
        return rows[0] if len(rows) == 1 else None

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def read(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def qword(self, va: int) -> int | None:
        rel = self.relocations.get(va)
        if rel and rel.get("addend"):
            return int(rel["addend"]) & 0xFFFFFFFFFFFFFFFF
        if not self.mapped(va, 8):
            return None
        return struct.unpack("<Q", self.read(va, 8))[0]

    def u32(self, va: int) -> int:
        return struct.unpack("<I", self.read(va, 4))[0]

    def read_text(self, va: int, length: int) -> str | None:
        if length <= 0 or length > MAX_STRING_BYTES or not self.mapped(va, length):
            return None
        try:
            text = self.read(va, length).decode("utf-8")
        except UnicodeDecodeError:
            return None
        return text if all(ch.isprintable() and ch not in "\r\n\t" for ch in text) else None

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


def resolve_reg(img: Image, insns: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
    if depth > 8:
        return {"classification": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    caller_saved = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
    start = max(-1, before - MAX_LOCAL_BACKWARD_INSTRUCTIONS)
    for i in range(before - 1, start, -1):
        ins = insns[i]
        if ins.mnemonic == "call" and wanted in caller_saved:
            return {"classification": "UNKNOWN", "reason": "CALL_CLOBBER_BOUNDARY", "boundary_site": hx(int(ins.address))}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        row: dict[str, Any] = {"definition_site": hx(int(ins.address))}
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            target = rip_target(ins)
            if target is not None:
                row.update({"classification": "STATIC_ADDRESS", "target": hx(target)})
                return row
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            row.update({"classification": "STACK_ADDRESS" if base in ("rsp", "rbp") else "OBJECT_ADDRESS", "base_register": base, "displacement": int(src.mem.disp)})
            return row
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_IMM:
                row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return row
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = resolve_reg(img, insns, i, via, depth + 1)
                row.update({"classification": nested.get("classification", "UNKNOWN"), "via_register": via, "source": nested})
                for key in ("target", "base_register", "displacement"):
                    if key in nested:
                        row[key] = nested[key]
                return row
            if src.type == X86_OP_MEM:
                target = rip_target(ins)
                if target is not None:
                    row.update({"classification": "STATIC_POINTER_LOAD", "address": hx(target), "value": hx(img.qword(target))})
                    return row
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                row.update({"classification": "OBJECT_FIELD", "base_register": base, "displacement": int(src.mem.disp)})
                return row
        row["classification"] = "UNKNOWN"
        return row
    return {"classification": f"ENTRY_ARG:{wanted}"}


def resolve_constant_before(img: Image, insns: list[Any], before: int, wanted: str) -> int | None:
    wanted = wanted.lower()
    for i in range(before - 1, max(-1, before - 24), -1):
        ins = insns[i]
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        if ins.mnemonic.startswith("mov") and src is not None and src.type == X86_OP_IMM:
            return int(src.imm) & 0xFFFFFFFFFFFFFFFF
        if ins.mnemonic == "xor" and src is not None and src.type == X86_OP_REG and canonical_reg(img, src.reg) == wanted:
            return 0
        return None
    return None


def decode_qt_string(img: Image, base: int, index: int) -> dict[str, Any]:
    if index < 0 or index > 4096 or not img.mapped(base + index * 8, 8):
        return {"index": index, "classification": "INVALID_STRING_INDEX"}
    offset = img.u32(base + index * 8)
    length = img.u32(base + index * 8 + 4)
    address = base + offset
    text = img.read_text(address, length) if offset <= 0x100000 else None
    return {
        "index": index,
        "offset": offset,
        "length": length,
        "address": hx(address) if text else None,
        "value": text,
        "classification": "QT6_OFFSET_LENGTH_STRING" if text else "UNRESOLVED_STRING",
    }


def decode_queue_metaobject(img: Image, static_metaobject: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "anchor": hx(static_metaobject),
        "owner_identity": "UNKNOWN",
        "signal_name": "UNKNOWN",
        "signal_index": QUEUE_SIGNAL_INDEX,
        "signal_method_row": None,
        "signal_name_address": None,
    }
    if not img.mapped(static_metaobject, 56):
        result["classification"] = "UNMAPPED_STATIC_METAOBJECT"
        return result
    ptrs = [img.qword(static_metaobject + i * 8) for i in range(7)]
    if any(value is None for value in ptrs[:3]):
        result["classification"] = "STATIC_METAOBJECT_POINTERS_UNRESOLVED"
        return result
    stringdata, metadata = int(ptrs[1]), int(ptrs[2])
    if not img.mapped(metadata, 56) or not img.mapped(stringdata, 8):
        result["classification"] = "UNMAPPED_QMETA_DATA"
        return result
    header = [img.u32(metadata + i * 4) for i in range(14)]
    names = (
        "revision", "class_name_index", "classinfo_count", "classinfo_data", "method_count", "method_data",
        "property_count", "property_data", "enum_count", "enum_data", "constructor_count", "constructor_data", "flags", "signal_count",
    )
    h = dict(zip(names, header))
    result["metadata_header"] = h
    result["stringdata"] = hx(stringdata)
    result["metadata"] = hx(metadata)
    owner = decode_qt_string(img, stringdata, h["class_name_index"])
    result["owner_identity"] = owner.get("value") or "UNKNOWN"
    if h["signal_count"] <= QUEUE_SIGNAL_INDEX or h["method_count"] <= QUEUE_SIGNAL_INDEX:
        result["classification"] = "SIGNAL_INDEX_OUTSIDE_QMETA_METHODS"
        return result
    method_row = metadata + h["method_data"] * 4 + QUEUE_SIGNAL_INDEX * 24
    if not img.mapped(method_row, 24):
        result["classification"] = "UNMAPPED_SIGNAL_METHOD_ROW"
        return result
    raw = [img.u32(method_row + i * 4) for i in range(6)]
    method_name = decode_qt_string(img, stringdata, raw[0])
    result["signal_method_raw_u32"] = raw
    result["signal_method_row"] = hx(method_row)
    result["signal_name"] = method_name.get("value") or "UNKNOWN"
    result["signal_name_address"] = method_name.get("address")
    result["classification"] = "QUEUE_QMETA_SIGNAL_DECODED"
    return result


def derive_queue_signal_identity(img: Image) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "signal_body": hx(QUEUE_SIGNAL_BODY),
        "signal_body_fde": [hx(SIGNAL_BODY_FDE[0]), hx(SIGNAL_BODY_FDE[1])],
        "activate_callsite": hx(ACTIVATE_CALLSITE),
        "derived_static_metaobject": "UNKNOWN",
    }
    actual_fde = img.containing_fde(QUEUE_SIGNAL_BODY)
    if actual_fde != SIGNAL_BODY_FDE:
        result["classification"] = "SIGNAL_BODY_FDE_MISMATCH"
        result["actual_fde"] = [hx(actual_fde[0]), hx(actual_fde[1])] if actual_fde else None
        return result
    insns = img.disassemble(*SIGNAL_BODY_FDE)
    call_rows = [(i, ins) for i, ins in enumerate(insns) if int(ins.address) == ACTIVATE_CALLSITE]
    if len(call_rows) != 1:
        result["classification"] = "ACTIVATE_CALLSITE_NOT_EXACT"
        return result
    call_index, call = call_rows[0]
    if call.mnemonic != "call" or direct_target(call) != QMETAOBJECT_ACTIVATE:
        result["classification"] = "ACTIVATE_TARGET_MISMATCH"
        result["actual_target"] = hx(direct_target(call))
        return result
    signal_index = resolve_constant_before(img, insns, call_index, "rdx")
    result["resolved_signal_index"] = signal_index
    if signal_index != QUEUE_SIGNAL_INDEX:
        result["classification"] = "SIGNAL_INDEX_NOT_EXACT"
        return result
    meta_provenance = resolve_reg(img, insns, call_index, "rsi")
    result["static_metaobject_argument_provenance"] = meta_provenance
    target_text = meta_provenance.get("target")
    if meta_provenance.get("classification") != "STATIC_ADDRESS" or not isinstance(target_text, str):
        result["classification"] = "STATIC_METAOBJECT_NOT_DERIVED_FROM_ACTIVATE_ARGUMENT"
        return result
    static_metaobject = int(target_text, 16)
    qmeta = decode_queue_metaobject(img, static_metaobject)
    result["derived_static_metaobject"] = hx(static_metaobject)
    result["queue_metaobject"] = qmeta
    if qmeta.get("owner_identity") != PROMOTED_RECEIVER_IDENTITY:
        result["classification"] = "DERIVED_QMETA_OWNER_MISMATCH"
        return result
    if qmeta.get("signal_name") != QUEUE_SIGNAL_NAME:
        result["classification"] = "DERIVED_QMETA_SIGNAL_NAME_MISMATCH"
        return result
    result.update({"classification": "EXACT_QUEUE_SIGNAL_IDENTITY_DERIVED", "proven": True})
    return result


def exact_lea_refs(img: Image, target: int) -> list[dict[str, Any]]:
    """Search only exact RIP-relative LEA references to one exact target, then validate each candidate inside its FDE."""
    candidates: dict[int, dict[str, Any]] = {}
    validated_fdes: dict[tuple[int, int], dict[int, int | None]] = {}
    for sec in img.sections:
        if sec.name != ".text" or not (sec.flags & 0x4) or sec.size < 7:
            continue
        data = img.raw[sec.offset : sec.offset + sec.size]
        for op_at in range(0, len(data) - 6):
            if data[op_at] != 0x8D or (data[op_at + 1] & 0xC7) != 0x05:
                continue
            starts = [op_at]
            if op_at > 0 and 0x40 <= data[op_at - 1] <= 0x4F:
                starts.insert(0, op_at - 1)
            for start in starts:
                va = sec.va + start
                decoded = list(img.md.disasm(data[start : min(len(data), start + 15)], va, count=1))
                if len(decoded) != 1 or decoded[0].mnemonic != "lea" or rip_target(decoded[0]) != target:
                    continue
                fde = img.containing_fde(va)
                if fde is None:
                    continue
                if fde not in validated_fdes:
                    mapping: dict[int, int | None] = {}
                    for ins in img.disassemble(*fde):
                        if ins.mnemonic == "lea":
                            mapping[int(ins.address)] = rip_target(ins)
                    validated_fdes[fde] = mapping
                if validated_fdes[fde].get(va) != target:
                    continue
                candidates[va] = {
                    "site": hx(va),
                    "target": hx(target),
                    "fde": [hx(fde[0]), hx(fde[1])],
                    "section": sec.name,
                }
    return [candidates[key] for key in sorted(candidates)]


def exact_data_refs(img: Image, target: int) -> list[dict[str, Any]]:
    """Search exact pointer-valued data references only; no semantic/global object census is performed."""
    rows: dict[int, dict[str, Any]] = {}
    for site, rel in sorted(img.relocations.items()):
        if int(rel.get("addend", 0)) != target:
            continue
        sec = img.section_for_va(site)
        if sec is None or (sec.flags & 0x4) or not (sec.flags & 0x2):
            continue
        rows[site] = {
            "site": hx(site),
            "target": hx(target),
            "section": sec.name,
            "source": "ELF_RELOCATION_ADDEND",
        }
    needle = struct.pack("<Q", target & 0xFFFFFFFFFFFFFFFF)
    for sec in img.sections:
        if (sec.flags & 0x4) or not (sec.flags & 0x2) or sec.size < 8:
            continue
        data = img.raw[sec.offset : sec.offset + sec.size]
        start = 0
        while True:
            pos = data.find(needle, start)
            if pos < 0:
                break
            site = sec.va + pos
            if pos % 8 == 0 and site not in rows:
                rows[site] = {
                    "site": hx(site),
                    "target": hx(target),
                    "section": sec.name,
                    "source": "ALIGNED_RAW_QWORD",
                }
            start = pos + 1
    return [rows[key] for key in sorted(rows)]


def enumerate_exact_signal_references(img: Image, identity: dict[str, Any]) -> dict[str, Any]:
    qmeta = identity.get("queue_metaobject") or {}
    derived_meta = identity.get("derived_static_metaobject")
    needles: list[dict[str, Any]] = [
        {"name": "signal_body", "target": QUEUE_SIGNAL_BODY, "signal_specific": True},
    ]
    for name, raw, specific in (
        ("signal_method_row", qmeta.get("signal_method_row"), True),
        ("signal_name_storage", qmeta.get("signal_name_address"), True),
        ("derived_queue_static_metaobject", derived_meta, False),
    ):
        if isinstance(raw, str) and raw not in ("UNKNOWN", ""):
            needles.append({"name": name, "target": int(raw, 16), "signal_specific": specific})

    refs: dict[tuple[str, str, str], dict[str, Any]] = {}
    data_wrapper_count = 0
    for needle in needles:
        target = int(needle["target"])
        for row in exact_lea_refs(img, target):
            key = (str(row["site"]), "CODE_LEA", str(needle["name"]))
            refs[key] = {
                **row,
                "reference_kind": "CODE_LEA",
                "needle": needle["name"],
                "signal_specific": bool(needle["signal_specific"]),
            }
        for data_row in exact_data_refs(img, target):
            data_site = int(str(data_row["site"]), 16)
            key = (str(data_row["site"]), "DATA_POINTER", str(needle["name"]))
            refs[key] = {
                **data_row,
                "reference_kind": "DATA_POINTER",
                "needle": needle["name"],
                "signal_specific": bool(needle["signal_specific"]),
            }
            for code_row in exact_lea_refs(img, data_site):
                data_wrapper_count += 1
                wrapper_key = (str(code_row["site"]), "CODE_LEA_TO_EXACT_DATA_REF", str(needle["name"]))
                refs[wrapper_key] = {
                    **code_row,
                    "reference_kind": "CODE_LEA_TO_EXACT_DATA_REF",
                    "needle": needle["name"],
                    "exact_data_site": data_row["site"],
                    "exact_data_source": data_row["source"],
                    "signal_specific": bool(needle["signal_specific"]),
                }
    rows = sorted(refs.values(), key=lambda row: (int(str(row["site"]), 16), str(row["reference_kind"]), str(row["needle"])))
    signal_rows = [row for row in rows if row["signal_specific"]]
    return {
        "strategy": "exact derived signal needles only: body, derived method/name metadata, derived class metaobject context, exact pointer data refs and LEA-to-exact-data wrappers",
        "needles": [{"name": n["name"], "target": hx(int(n["target"])), "signal_specific": n["signal_specific"]} for n in needles],
        "references": rows,
        "exact_signal_reference_count": len(signal_rows),
        "exact_signal_context_reference_count": len(rows),
        "data_wrapper_reference_count": data_wrapper_count,
    }


def _tainted_body_stores(img: Image, insns: list[Any], ref_index: int, call_index: int) -> list[dict[str, Any]]:
    ref = insns[ref_index]
    if ref.mnemonic != "lea" or not ref.operands or ref.operands[0].type != X86_OP_REG or rip_target(ref) != QUEUE_SIGNAL_BODY:
        return []
    tainted = {canonical_reg(img, ref.operands[0].reg)}
    stores: list[dict[str, Any]] = []
    for ins in insns[ref_index + 1 : call_index]:
        if not ins.operands:
            continue
        dst = ins.operands[0]
        src = ins.operands[1] if len(ins.operands) > 1 else None
        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_MEM and src is not None and src.type == X86_OP_REG:
            source = canonical_reg(img, src.reg)
            if source in tainted:
                base = canonical_reg(img, dst.mem.base) if dst.mem.base else "none"
                stores.append({
                    "site": hx(int(ins.address)),
                    "base_register": base,
                    "displacement": int(dst.mem.disp),
                    "source_register": source,
                })
        if dst.type != X86_OP_REG:
            continue
        dst_reg = canonical_reg(img, dst.reg)
        source_tainted = bool(src is not None and src.type == X86_OP_REG and canonical_reg(img, src.reg) in tainted)
        if ins.mnemonic.startswith("mov") and source_tainted:
            tainted.add(dst_reg)
        elif dst_reg in tainted:
            tainted.remove(dst_reg)
    return stores


def _reference_role(img: Image, insns: list[Any], ref_index: int, call_index: int, reference: dict[str, Any]) -> dict[str, Any]:
    needle = reference["needle"]
    if needle in ("signal_method_row", "signal_name_storage"):
        return {"classification": "EXACT_SIGNAL_METADATA_REFERENCE", "causal_signal_identity": True}
    if needle != "signal_body":
        return {"classification": "CLASS_METAOBJECT_CONTEXT_ONLY", "causal_signal_identity": False}
    stores = _tainted_body_stores(img, insns, ref_index, call_index)
    if any(row["displacement"] == Q_SLOT_FUNCTION_FIELD for row in stores):
        return {
            "classification": "EXACT_SIGNAL_BODY_USED_AS_QSLOT_CALLABLE",
            "causal_signal_identity": False,
            "stores": stores,
        }
    signal_arg = resolve_reg(img, insns, call_index, "rdx")
    if signal_arg.get("classification") == "STACK_ADDRESS":
        base = signal_arg.get("base_register")
        disp = signal_arg.get("displacement")
        matched = [row for row in stores if row["base_register"] == base and row["displacement"] == disp]
        if matched:
            return {
                "classification": "EXACT_SIGNAL_BODY_IN_CONNECT_SIGNAL_DESCRIPTOR",
                "causal_signal_identity": True,
                "signal_argument_provenance": signal_arg,
                "matched_stores": matched,
            }
    return {
        "classification": "EXACT_SIGNAL_BODY_REFERENCE_ROLE_UNRESOLVED",
        "causal_signal_identity": False,
        "signal_argument_provenance": signal_arg,
        "stores": stores,
    }


def _slot_function_candidates(img: Image, insns: list[Any], start: int, stop: int) -> list[dict[str, Any]]:
    refs: dict[str, tuple[int, int]] = {}
    rows: list[dict[str, Any]] = []
    for i in range(start, stop):
        ins = insns[i]
        if ins.mnemonic == "lea" and ins.operands and ins.operands[0].type == X86_OP_REG:
            target = rip_target(ins)
            if target is not None and img.is_executable_va(target) and img.containing_fde(target) is not None:
                refs[canonical_reg(img, ins.operands[0].reg)] = (i, target)
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or int(dst.mem.disp) != Q_SLOT_FUNCTION_FIELD or src.type != X86_OP_REG:
            continue
        source_reg = canonical_reg(img, src.reg)
        if source_reg not in refs:
            continue
        ref_index, target = refs[source_reg]
        symbols = img.symbol_names(target)
        symbol = img.plt_symbol(target) or (symbols[0] if len(symbols) == 1 else None)
        fde = img.containing_fde(target)
        rows.append({
            "reference_site": hx(int(insns[ref_index].address)),
            "store_site": hx(int(ins.address)),
            "target": hx(target),
            "target_fde": [hx(fde[0]), hx(fde[1])] if fde else None,
            "symbol": symbol,
            "demangled": demangle(symbol),
        })
    unique = {str(row["target"]): row for row in rows}
    return [unique[key] for key in sorted(unique)]


def trace_connect_arguments(img: Image, insns: list[Any], call_index: int) -> dict[str, Any]:
    call = insns[call_index]
    local_start = max(0, call_index - MAX_LOCAL_BACKWARD_INSTRUCTIONS)
    return {
        "callsite": hx(int(call.address)),
        "connectimpl_abi": "nontrivial QMetaObject::Connection return uses hidden sret in rdi; explicit args shift to rsi/r9",
        "connection_return_storage_provenance": resolve_reg(img, insns, call_index, "rdi"),
        "sender_provenance": resolve_reg(img, insns, call_index, "rsi"),
        "signal_argument_provenance": resolve_reg(img, insns, call_index, "rdx"),
        "receiver_provenance": resolve_reg(img, insns, call_index, "rcx"),
        "method_argument_provenance": resolve_reg(img, insns, call_index, "r8"),
        "slot_object_provenance": resolve_reg(img, insns, call_index, "r9"),
        "slot_function_candidates": _slot_function_candidates(img, insns, local_start, call_index),
    }


def find_exact_signal_connect_candidates(img: Image, references: dict[str, Any]) -> dict[str, Any]:
    connect_symbol = img.plt_symbol(CONNECTIMPL_TARGET)
    connect_demangled = demangle(connect_symbol)
    if not connect_demangled or "QObject::connectImpl(" not in connect_demangled:
        return {
            "connectimpl_target_verified": False,
            "connectimpl_target": hx(CONNECTIMPL_TARGET),
            "connectimpl_demangled": connect_demangled,
            "candidate_count": 0,
            "consumed_candidate_count": 0,
            "candidates": [],
            "consumed_candidates": [],
        }
    code_refs = [
        row for row in references["references"]
        if row["signal_specific"] and row["reference_kind"] in ("CODE_LEA", "CODE_LEA_TO_EXACT_DATA_REF") and row.get("fde")
    ]
    by_fde: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for row in code_refs:
        fde_raw = row["fde"]
        fde = (int(fde_raw[0], 16), int(fde_raw[1], 16))
        by_fde.setdefault(fde, []).append(row)

    candidates: list[dict[str, Any]] = []
    consumed: list[dict[str, Any]] = []
    for fde, fde_refs in sorted(by_fde.items()):
        insns = img.disassemble(*fde)
        index_by_addr = {int(ins.address): i for i, ins in enumerate(insns)}
        for call_index, ins in enumerate(insns):
            if ins.mnemonic != "call" or direct_target(ins) != CONNECTIMPL_TARGET:
                continue
            callsite = int(ins.address)
            local_refs: list[dict[str, Any]] = []
            for ref in fde_refs:
                site = int(str(ref["site"]), 16)
                ref_index = index_by_addr.get(site)
                if ref_index is None or ref_index >= call_index or call_index - ref_index > MAX_LOCAL_BACKWARD_INSTRUCTIONS:
                    continue
                role = _reference_role(img, insns, ref_index, call_index, ref)
                local_refs.append({**ref, "role": role})
            causal = [row for row in local_refs if row["role"].get("causal_signal_identity")]
            if not causal:
                continue
            row = {
                "fde": [hx(fde[0]), hx(fde[1])],
                "connect_callsite": hx(callsite),
                "connect_target": hx(CONNECTIMPL_TARGET),
                "connect_demangled": connect_demangled,
                "exact_signal_references": local_refs,
                "causal_exact_signal_reference_count": len(causal),
                "arguments": trace_connect_arguments(img, insns, call_index),
            }
            if callsite == SELF_RELAY_CONNECTIMPL_CALLSITE or fde == CONSUMED_CONSTRUCTOR_FDE:
                row["classification"] = "CONSUMED_PROMOTED_CONSTRUCTOR_CONTEXT"
                consumed.append(row)
            else:
                row["classification"] = "DOWNSTREAM_EXACT_SIGNAL_CONNECT_CANDIDATE"
                candidates.append(row)
    unique = {str(row["connect_callsite"]): row for row in candidates}
    consumed_unique = {str(row["connect_callsite"]): row for row in consumed}
    return {
        "connectimpl_target_verified": True,
        "connectimpl_target": hx(CONNECTIMPL_TARGET),
        "connectimpl_demangled": connect_demangled,
        "candidate_count": len(unique),
        "consumed_candidate_count": len(consumed_unique),
        "candidates": [unique[key] for key in sorted(unique)],
        "consumed_candidates": [consumed_unique[key] for key in sorted(consumed_unique)],
    }


def classify_exact_signal_connect_site(candidates: dict[str, Any]) -> dict[str, Any]:
    rows = candidates.get("candidates", [])
    result = {
        "terminal_result": "SOURCE_BLOCKER",
        "first_missing_boundary": "UNKNOWN",
        "next_unique_relay_edge": "UNKNOWN",
        "next_endpoint_identity": "UNKNOWN",
        "next_relay_identity_preserved": False,
    }
    if not candidates.get("connectimpl_target_verified"):
        result["first_missing_boundary"] = "CONNECTIMPL_TARGET_IDENTITY_NOT_VERIFIED_ON_EXACT_CLIENT"
        return result
    if len(rows) == 0:
        result["first_missing_boundary"] = "NO_DOWNSTREAM_CONNECTIMPL_CAUSALLY_TIED_TO_EXACT_SIGNAL_REFERENCES"
        return result
    if len(rows) > 1:
        result["first_missing_boundary"] = "MULTIPLE_DOWNSTREAM_CONNECTIMPL_SITES_SURVIVE_EXACT_SIGNAL_DISCRIMINATOR"
        return result
    row = rows[0]
    slots = row.get("arguments", {}).get("slot_function_candidates", [])
    endpoints = []
    for slot in slots:
        identity = slot.get("demangled") or slot.get("symbol")
        if identity:
            endpoints.append({"kind": "QSLOT_CALLABLE", "identity": identity, "target": slot.get("target")})
    unique_endpoints = {(str(ep["kind"]), str(ep["identity"])): ep for ep in endpoints}
    result["next_unique_relay_edge"] = row["connect_callsite"]
    if len(unique_endpoints) != 1:
        result["first_missing_boundary"] = "DOWNSTREAM_CONNECT_ENDPOINT_IDENTITY_NOT_UNIQUELY_PROVEN"
        return result
    endpoint = list(unique_endpoints.values())[0]
    result.update({
        "terminal_result": "QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE_PROVEN",
        "first_missing_boundary": "none",
        "next_endpoint_identity": f"{endpoint['kind']}:{endpoint['identity']}",
        "next_relay_identity_preserved": True,
    })
    return result


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")
    img = Image(client)
    try:
        identity = derive_queue_signal_identity(img)
        if identity.get("proven"):
            references = enumerate_exact_signal_references(img, identity)
            candidates = find_exact_signal_connect_candidates(img, references)
            classification = classify_exact_signal_connect_site(candidates)
        else:
            references = {
                "strategy": "not run: exact queue signal identity derivation failed",
                "needles": [],
                "references": [],
                "exact_signal_reference_count": 0,
                "exact_signal_context_reference_count": 0,
                "data_wrapper_reference_count": 0,
            }
            candidates = {
                "connectimpl_target_verified": False,
                "candidate_count": 0,
                "consumed_candidate_count": 0,
                "candidates": [],
                "consumed_candidates": [],
            }
            classification = {
                "terminal_result": "SOURCE_BLOCKER",
                "first_missing_boundary": "EXACT_QUEUE_SIGNAL_METAOBJECT_IDENTITY_NOT_DERIVED",
                "next_unique_relay_edge": "UNKNOWN",
                "next_endpoint_identity": "UNKNOWN",
                "next_relay_identity_preserved": False,
            }
        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-exact-xref-connect-site.v1",
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
            "queue_signal_name": QUEUE_SIGNAL_NAME,
            "queue_signal_index": QUEUE_SIGNAL_INDEX,
            "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
            "queue_signal_body": hx(QUEUE_SIGNAL_BODY),
            "queue_signal_argv1_identity": PROMOTED_ARGV1_IDENTITY,
            "queue_signal_receiver_identity": PROMOTED_RECEIVER_IDENTITY,
            "queue_signal_connection_role": "SIGNAL_RELAY",
            "self_relay_connectimpl_callsite": hx(SELF_RELAY_CONNECTIMPL_CALLSITE),
            "consumed_constructor_fde": [hx(CONSUMED_CONSTRUCTOR_FDE[0]), hx(CONSUMED_CONSTRUCTOR_FDE[1])],
            "derived_queue_static_metaobject": identity.get("derived_static_metaobject", "UNKNOWN"),
            "exact_queue_signal_identity": identity,
            "exact_signal_references": references,
            "exact_signal_reference_count": int(references["exact_signal_reference_count"]),
            "exact_signal_connect_candidates": candidates,
            "exact_signal_connect_candidate_count": int(candidates["candidate_count"]),
            "next_unique_relay_edge": classification["next_unique_relay_edge"],
            "next_endpoint_identity": classification["next_endpoint_identity"],
            "next_relay_identity_preserved": classification["next_relay_identity_preserved"],
            "queue_signal_writer_identity": "UNKNOWN",
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": classification["terminal_result"],
            "FIRST_MISSING_BOUNDARY": classification["first_missing_boundary"],
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
