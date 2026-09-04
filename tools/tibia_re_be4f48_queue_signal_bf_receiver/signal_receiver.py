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
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

QUEUE_STATIC_METAOBJECT = 0x30B73E0
QUEUE_SIGNAL_INDEX = 0xBF
DRAIN_CALLBACK = 0xBD2190
DRAIN_FDE = (0xBD2190, 0xBD2495)
DRAIN_METAOBJECT_LEA_SITE = 0xBD221D
DRAIN_METAOBJECT_ARG_SITE = 0xBD22AE
DRAIN_ACTIVATE_CALLSITE = 0xBD22C2
QMETAOBJECT_ACTIVATE = 0x4D7DC0
Q_SLOT_FUNCTION_FIELD = 0x10
MAX_STRING_BYTES = 512
BOUNDED_RIP_XREF_ONLY = True


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
            Section(int(s["sh_offset"]), int(s["sh_size"]), int(s["sh_addr"]), int(s["sh_flags"]), s.name)
            for s in self.elf.iter_sections()
            if int(s["sh_size"]) > 0
        ]
        self.relocations: dict[int, dict[str, Any]] = {}
        for sec in self.elf.iter_sections():
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
            (int(e["initial_location"]), int(e["initial_location"]) + int(e["address_range"]))
            for e in dwarf.EH_CFI_entries()
            if isinstance(e, FDE)
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

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def read(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def qword(self, va: int) -> int:
        rel = self.relocations.get(va)
        if rel and rel.get("addend"):
            return int(rel["addend"]) & 0xFFFFFFFFFFFFFFFF
        return struct.unpack("<Q", self.read(va, 8))[0]

    def u32(self, va: int) -> int:
        return struct.unpack("<I", self.read(va, 4))[0]

    def read_text(self, va: int, length: int) -> str | None:
        if length < 0 or length > MAX_STRING_BYTES or not self.mapped(va, length):
            return None
        try:
            text = self.read(va, length).decode("utf-8")
        except UnicodeDecodeError:
            return None
        return text if text and all(ch.isprintable() and ch not in "\r\n\t" for ch in text) else None

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

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
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                got = int(ins.address) + int(ins.size) + int(op.mem.disp)
                rel = self.relocations.get(got)
                if rel and rel.get("symbol"):
                    return str(rel["symbol"])
        return None


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


def rip_target(ins: Any) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return int(ins.address) + int(ins.size) + int(op.mem.disp)
    return None


def direct_target(ins: Any) -> int | None:
    if ins.mnemonic not in ("call", "jmp") or not ins.operands:
        return None
    return int(ins.operands[0].imm) if ins.operands[0].type == X86_OP_IMM else None


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        result = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
        return result.stdout.strip() or symbol
    except Exception:
        return symbol


def decode_qt_string(img: Image, base: int, index: int) -> dict[str, Any]:
    if index < 0 or index > 4096 or not img.mapped(base + index * 8, 8):
        return {"index": index, "classification": "INVALID_STRING_INDEX"}
    offset = img.u32(base + index * 8)
    length = img.u32(base + index * 8 + 4)
    text = img.read_text(base + offset, length) if offset <= 0x100000 else None
    return {
        "index": index,
        "offset": offset,
        "length": length,
        "value": text,
        "classification": "QT6_OFFSET_LENGTH_STRING" if text else "UNRESOLVED_STRING",
    }


def decode_queue_metaobject(img: Image) -> dict[str, Any]:
    ptrs = [img.qword(QUEUE_STATIC_METAOBJECT + i * 8) for i in range(7)]
    stringdata, metadata = ptrs[1], ptrs[2]
    result: dict[str, Any] = {
        "anchor": hx(QUEUE_STATIC_METAOBJECT),
        "owner_identity": "UNKNOWN",
        "signal_name": "UNKNOWN",
        "signal_index": QUEUE_SIGNAL_INDEX,
    }
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
    owner = decode_qt_string(img, stringdata, h["class_name_index"])
    result["owner_identity"] = owner.get("value") or "UNKNOWN"
    if h["signal_count"] > QUEUE_SIGNAL_INDEX and h["method_count"] > QUEUE_SIGNAL_INDEX:
        method_row = metadata + h["method_data"] * 4 + QUEUE_SIGNAL_INDEX * 24
        if img.mapped(method_row, 24):
            raw = [img.u32(method_row + i * 4) for i in range(6)]
            method_name = decode_qt_string(img, stringdata, raw[0])
            result["signal_name"] = method_name.get("value") or "UNKNOWN"
            result["signal_method_raw_u32"] = raw
    result["classification"] = "QUEUE_QMETA_DECODED" if result["owner_identity"] != "UNKNOWN" else "QUEUE_QMETA_UNKNOWN"
    return result


def instruction_at(insns: list[Any], address: int) -> Any | None:
    rows = [ins for ins in insns if int(ins.address) == address]
    return rows[0] if len(rows) == 1 else None


def resolve_static_metaobject_argument(img: Image, insns: list[Any]) -> dict[str, Any]:
    lea = instruction_at(insns, DRAIN_METAOBJECT_LEA_SITE)
    arg = instruction_at(insns, DRAIN_METAOBJECT_ARG_SITE)
    result: dict[str, Any] = {
        "proven": False,
        "lea_site": hx(DRAIN_METAOBJECT_LEA_SITE),
        "argument_site": hx(DRAIN_METAOBJECT_ARG_SITE),
        "expected_static_metaobject": hx(QUEUE_STATIC_METAOBJECT),
    }
    if lea is None or arg is None:
        result["classification"] = "METAOBJECT_CHAIN_INSTRUCTION_NOT_EXACT"
        return result
    if (
        lea.mnemonic != "lea"
        or len(lea.operands) < 2
        or lea.operands[0].type != X86_OP_REG
        or canonical_reg(img, lea.operands[0].reg) != "rbp"
        or rip_target(lea) != QUEUE_STATIC_METAOBJECT
    ):
        result["classification"] = "METAOBJECT_LEA_NOT_EXACT"
        result["lea_op_str"] = lea.op_str
        result["resolved_lea_target"] = hx(rip_target(lea))
        return result
    if (
        arg.mnemonic != "mov"
        or len(arg.operands) < 2
        or arg.operands[0].type != X86_OP_REG
        or arg.operands[1].type != X86_OP_REG
        or canonical_reg(img, arg.operands[0].reg) != "rsi"
        or canonical_reg(img, arg.operands[1].reg) != "rbp"
    ):
        result["classification"] = "METAOBJECT_ARGUMENT_MOVE_NOT_EXACT"
        result["argument_op_str"] = arg.op_str
        return result
    for ins in insns:
        if not (DRAIN_METAOBJECT_LEA_SITE < int(ins.address) < DRAIN_METAOBJECT_ARG_SITE):
            continue
        if not ins.operands or ins.operands[0].type != X86_OP_REG:
            continue
        if canonical_reg(img, ins.operands[0].reg) == "rbp":
            result["classification"] = "METAOBJECT_RBP_REDEFINED_BEFORE_ARGUMENT"
            result["redefinition_site"] = hx(int(ins.address))
            return result
    result.update({
        "classification": "STATIC_METAOBJECT_ARGUMENT_PROVEN",
        "proven": True,
        "register_chain": "0xbd221d: rbp=0x30b73e0 -> 0xbd22ae: rsi=rbp -> 0xbd22c2",
        "static_metaobject": hx(QUEUE_STATIC_METAOBJECT),
    })
    return result


def resolve_constant_before(img: Image, insns: list[Any], before: int, wanted: str) -> int | None:
    wanted = wanted.lower()
    for i in range(before - 1, max(-1, before - 20), -1):
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


def bounded_signal_body_proof(img: Image) -> dict[str, Any]:
    fde = img.containing_fde(DRAIN_CALLBACK)
    result: dict[str, Any] = {
        "bounded": True,
        "drain_callback": hx(DRAIN_CALLBACK),
        "expected_fde": [hx(DRAIN_FDE[0]), hx(DRAIN_FDE[1])],
        "signal_body_target": "UNKNOWN",
    }
    if fde != DRAIN_FDE:
        result["classification"] = "DRAIN_FDE_MISMATCH"
        result["actual_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result
    insns = img.disassemble(*DRAIN_FDE)
    meta = resolve_static_metaobject_argument(img, insns)
    result["static_metaobject_argument"] = meta
    call_sites = [i for i, ins in enumerate(insns) if int(ins.address) == DRAIN_ACTIVATE_CALLSITE]
    if len(call_sites) != 1:
        result["classification"] = "ACTIVATE_CALLSITE_NOT_EXACT"
        return result
    call_index = call_sites[0]
    call = insns[call_index]
    if call.mnemonic != "call" or direct_target(call) != QMETAOBJECT_ACTIVATE:
        result["classification"] = "ACTIVATE_TARGET_MISMATCH"
        return result
    signal_index = resolve_constant_before(img, insns, call_index, "rdx")
    result.update({
        "activate_callsite": hx(DRAIN_ACTIVATE_CALLSITE),
        "activate_target": hx(QMETAOBJECT_ACTIVATE),
        "resolved_signal_index": signal_index,
    })
    if signal_index != QUEUE_SIGNAL_INDEX or not meta.get("proven"):
        result["classification"] = "DRAIN_SIGNAL_BF_BINDING_NOT_PROVEN"
        return result
    result["classification"] = "DRAIN_SIGNAL_BF_BODY_PROVEN"
    result["signal_body_target"] = hx(DRAIN_CALLBACK)
    return result


def exact_lea_refs(img: Image, target: int) -> list[int]:
    """Find exact RIP-relative LEA references using a byte prefilter and per-FDE validation."""
    candidates: set[int] = set()
    validated_fdes: dict[tuple[int, int], dict[int, int | None]] = {}
    for sec in img.sections:
        if sec.name != ".text" or not (sec.flags & 4) or sec.size < 7:
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
                if validated_fdes[fde].get(va) == target:
                    candidates.add(va)
    return sorted(candidates)


def resolve_reg(img: Image, insns: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
    if depth > 8:
        return {"classification": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    caller_saved = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
    for i in range(before - 1, -1, -1):
        ins = insns[i]
        if ins.mnemonic == "call" and wanted in caller_saved:
            return {"classification": "UNKNOWN", "reason": "CALL_CLOBBER_BOUNDARY", "boundary_site": hx(int(ins.address))}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        row: dict[str, Any] = {"definition_site": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            target = rip_target(ins)
            if target is not None:
                row.update({"classification": "STATIC_ADDRESS", "target": hx(target)})
                return row
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            row.update({"classification": "OBJECT_ADDRESS" if base != "rsp" else "STACK_ADDRESS", "base_register": base, "displacement": hx(int(src.mem.disp))})
            return row
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_IMM:
                row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return row
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = resolve_reg(img, insns, i, via, depth + 1)
                row.update({"classification": nested.get("classification", "UNKNOWN"), "via_register": via, "source": nested})
                return row
            if src.type == X86_OP_MEM:
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                if src.mem.base == X86_REG_RSP:
                    row.update({"classification": "STACK_LOAD", "displacement": hx(int(src.mem.disp))})
                    return row
                target = rip_target(ins)
                if target is not None:
                    row.update({"classification": "STATIC_POINTER_LOAD", "address": hx(target)})
                    return row
                row.update({"classification": "OBJECT_FIELD", "base_register": base, "displacement": hx(int(src.mem.disp))})
                return row
        row["classification"] = "UNKNOWN"
        return row
    return {"classification": f"ENTRY_ARG:{wanted}"}


def slot_function_candidates(img: Image, insns: list[Any], start: int, stop: int, signal_body: int) -> list[dict[str, Any]]:
    refs: dict[str, tuple[int, int]] = {}
    candidates: list[dict[str, Any]] = []
    for i in range(start, stop):
        ins = insns[i]
        if ins.mnemonic == "lea" and ins.operands and ins.operands[0].type == X86_OP_REG:
            target = rip_target(ins)
            if target is not None and target not in (signal_body, QUEUE_STATIC_METAOBJECT) and img.containing_fde(target) is not None:
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
        fde = img.containing_fde(target)
        candidates.append({
            "reference_site": hx(int(insns[ref_index].address)),
            "store_site": hx(int(ins.address)),
            "target": hx(target),
            "target_fde": [hx(fde[0]), hx(fde[1])] if fde else None,
        })
    return list({row["target"]: row for row in candidates}.values())


def find_connection_candidates(img: Image, signal_body: int) -> dict[str, Any]:
    refs = exact_lea_refs(img, signal_body)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for ref in refs:
        fde = img.containing_fde(ref)
        if fde is None or fde in seen:
            continue
        seen.add(fde)
        insns = img.disassemble(*fde)
        body_refs = [i for i, ins in enumerate(insns) if rip_target(ins) == signal_body]
        if not body_refs:
            continue
        for call_index, ins in enumerate(insns):
            if ins.mnemonic != "call":
                continue
            target = direct_target(ins)
            if target is None:
                continue
            dm = demangle(img.plt_symbol(target))
            if not dm or "QObject::connectImpl(" not in dm:
                continue
            preceding = [i for i in body_refs if i < call_index and call_index - i <= 180]
            if not preceding:
                continue
            local_start = max(0, call_index - 180)
            rows.append({
                "fde": [hx(fde[0]), hx(fde[1])],
                "connect_callsite": hx(int(ins.address)),
                "connect_target": hx(target),
                "connect_demangled": dm,
                "signal_body_reference_sites": [hx(int(insns[i].address)) for i in preceding],
                "receiver_provenance": resolve_reg(img, insns, call_index, "rcx"),
                "slot_object_provenance": resolve_reg(img, insns, call_index, "r9"),
                "slot_function_candidates": slot_function_candidates(img, insns, local_start, call_index, signal_body),
            })
    return {
        "xref_strategy": "exact .text RIP-relative LEA references only; per-candidate FDE validation",
        "signal_body_reference_count": len(refs),
        "candidate_count": len(rows),
        "candidates": rows,
    }


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")
    img = Image(client)
    try:
        queue_meta = decode_queue_metaobject(img)
        signal = bounded_signal_body_proof(img)
        signal_body = DRAIN_CALLBACK if signal.get("signal_body_target") == hx(DRAIN_CALLBACK) else None
        connections = find_connection_candidates(img, signal_body) if signal_body is not None else {
            "xref_strategy": "not run: signal body not proven",
            "signal_body_reference_count": 0,
            "candidate_count": 0,
            "candidates": [],
        }
        receiver_provenance: Any = "UNKNOWN"
        slot_identity = "UNKNOWN"
        receiver_identity = "UNKNOWN"
        writer_identity = "UNKNOWN"
        next_edge = "UNKNOWN"
        if signal_body is None:
            missing = "QUEUE_SIGNAL_BF_STATIC_METAOBJECT_ARGUMENT_NOT_PROVEN"
        elif connections["candidate_count"] != 1:
            missing = "QUEUE_SIGNAL_BF_CONNECTIMPL_NOT_UNIQUE_FROM_EXACT_SIGNAL_BODY_XREF"
        else:
            connection = connections["candidates"][0]
            receiver_provenance = connection["receiver_provenance"]
            slots = connection["slot_function_candidates"]
            if len(slots) != 1:
                missing = "QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN"
            else:
                slot_identity = slots[0]["target"]
                if receiver_provenance.get("classification") in ("UNKNOWN", "STACK_LOAD"):
                    missing = "QUEUE_SIGNAL_BF_RECEIVER_PROVENANCE_NOT_UNIQUE"
                else:
                    missing = "QUEUE_SIGNAL_BF_RECEIVER_CLASS_OR_WRITER_TYPE_NOT_PROVEN"
        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-receiver.v3",
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
            "bounded_rip_xref_only": BOUNDED_RIP_XREF_ONLY,
            "queue_drain_callback": hx(DRAIN_CALLBACK),
            "queue_drain_fde": [hx(DRAIN_FDE[0]), hx(DRAIN_FDE[1])],
            "queue_drain_activate_callsite": hx(DRAIN_ACTIVATE_CALLSITE),
            "queue_drain_causal_consumption": True,
            "queue_static_metaobject": hx(QUEUE_STATIC_METAOBJECT),
            "queue_metaobject": queue_meta,
            "queue_signal_index": QUEUE_SIGNAL_INDEX,
            "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
            "queue_signal_argv1_identity": "exact GameclientMessage shared pair",
            "queue_signal_body": signal,
            "queue_signal_connections": connections,
            "queue_signal_receiver_provenance": receiver_provenance,
            "queue_signal_receiver_identity": receiver_identity,
            "queue_signal_slot_identity": slot_identity,
            "queue_signal_writer_identity": writer_identity,
            "next_unique_writer_edge": next_edge,
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
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
