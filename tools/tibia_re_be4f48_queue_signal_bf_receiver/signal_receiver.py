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
QMETAOBJECT_ACTIVATE = 0x4D7DC0
Q_SLOT_FUNCTION_FIELD = 0x10
MAX_STRING_BYTES = 512


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def signed64(value: int) -> int:
    value &= 0xFFFFFFFFFFFFFFFF
    return value - (1 << 64) if value & (1 << 63) else value


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        p = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
        return p.stdout.strip() or symbol
    except Exception:
        return symbol


def parse_itanium_nested_name(value: str) -> str | None:
    if not value.startswith("N") or not value.endswith("E"):
        return None
    i = 1
    end = len(value) - 1
    parts: list[str] = []
    while i < end:
        j = i
        while j < end and value[j].isdigit():
            j += 1
        if j == i:
            return None
        n = int(value[i:j])
        if n <= 0 or j + n > end:
            return None
        part = value[j : j + n]
        if not part or not all(ch.isalnum() or ch == "_" for ch in part):
            return None
        parts.append(part)
        i = j + n
    return "::".join(parts) if parts and i == end else None


@dataclass(frozen=True)
class Section:
    offset: int
    size: int
    va: int
    flags: int
    name: str


class Image:
    def __init__(self, path: Path) -> None:
        self.path = path
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
                idx = int(rel["r_info_sym"])
                if symtab is not None and idx:
                    try:
                        symbol = symtab.get_symbol(idx).name or None
                    except Exception:
                        symbol = None
                self.relocations[int(rel["r_offset"])] = {
                    "addend": int(rel.entry.get("r_addend", 0)),
                    "symbol": symbol,
                    "type": int(rel["r_info_type"]),
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

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def qword(self, va: int) -> int:
        rel = self.relocations.get(va)
        if rel and rel.get("addend"):
            return int(rel["addend"]) & 0xFFFFFFFFFFFFFFFF
        return struct.unpack("<Q", self.read(va, 8))[0]

    def u32(self, va: int) -> int:
        return struct.unpack("<I", self.read(va, 4))[0]

    def cstring(self, va: int, max_len: int = 1024) -> str:
        off = self.va_to_off(va)
        end = self.raw.find(b"\0", off, min(len(self.raw), off + max_len))
        if end < 0:
            raise RuntimeError(f"unterminated string at {hx(va)}")
        return self.raw[off:end].decode("ascii", "strict")

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


def decode_qt_string(img: Image, base: int, index: int) -> dict[str, Any]:
    if index < 0 or index > 4096 or not img.mapped(base + index * 8, 8):
        return {"index": index, "classification": "INVALID_STRING_INDEX"}
    off = img.u32(base + index * 8)
    length = img.u32(base + index * 8 + 4)
    text = img.read_text(base + off, length) if off <= 0x100000 else None
    return {"index": index, "offset": off, "length": length, "value": text, "classification": "QT6_OFFSET_LENGTH_STRING" if text else "UNRESOLVED_STRING"}


def decode_queue_metaobject(img: Image) -> dict[str, Any]:
    ptrs = [img.qword(QUEUE_STATIC_METAOBJECT + i * 8) for i in range(7)]
    stringdata, metadata = ptrs[1], ptrs[2]
    result: dict[str, Any] = {"anchor": hx(QUEUE_STATIC_METAOBJECT), "owner_identity": "UNKNOWN", "signal_name": "UNKNOWN", "signal_index": QUEUE_SIGNAL_INDEX}
    if not img.mapped(metadata, 56) or not img.mapped(stringdata, 8):
        result["classification"] = "UNMAPPED_QMETA_DATA"
        return result
    header = [img.u32(metadata + i * 4) for i in range(14)]
    names = ("revision","class_name_index","classinfo_count","classinfo_data","method_count","method_data","property_count","property_data","enum_count","enum_data","constructor_count","constructor_data","flags","signal_count")
    h = dict(zip(names, header))
    result["metadata_header"] = h
    owner = decode_qt_string(img, stringdata, h["class_name_index"])
    result["owner_identity"] = owner.get("value") or "UNKNOWN"
    if h["signal_count"] > QUEUE_SIGNAL_INDEX and h["method_count"] > QUEUE_SIGNAL_INDEX:
        row = metadata + h["method_data"] * 4 + QUEUE_SIGNAL_INDEX * 24
        if img.mapped(row, 24):
            raw = [img.u32(row + i * 4) for i in range(6)]
            name = decode_qt_string(img, stringdata, raw[0])
            result["signal_name"] = name.get("value") or "UNKNOWN"
            result["signal_method_raw_u32"] = raw
    result["classification"] = "QUEUE_QMETA_DECODED" if result["owner_identity"] != "UNKNOWN" else "QUEUE_QMETA_UNKNOWN"
    return result


def exec_refs(img: Image, target: int) -> list[int]:
    refs: list[int] = []
    for sec in img.sections:
        if not (sec.flags & 4) or sec.size <= 0:
            continue
        try:
            insns = list(img.md.disasm(img.raw[sec.offset : sec.offset + sec.size], sec.va))
        except Exception:
            continue
        for ins in insns:
            if rip_target(ins) == target:
                refs.append(int(ins.address))
    return sorted(set(refs))


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


def find_signal_body(img: Image) -> dict[str, Any]:
    refs = exec_refs(img, QUEUE_STATIC_METAOBJECT)
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[int,int]] = set()
    for ref in refs:
        fde = img.containing_fde(ref)
        if fde is None or fde in seen:
            continue
        seen.add(fde)
        insns = img.disassemble(*fde)
        for i, ins in enumerate(insns):
            if ins.mnemonic != "call":
                continue
            tgt = direct_target(ins)
            if tgt != QMETAOBJECT_ACTIVATE:
                continue
            idx = resolve_constant_before(img, insns, i, "rdx")
            meta_refs = [int(x.address) for x in insns[max(0,i-16):i] if rip_target(x) == QUEUE_STATIC_METAOBJECT]
            if idx == QUEUE_SIGNAL_INDEX and meta_refs:
                candidates.append({"fde": [hx(fde[0]), hx(fde[1])], "target": hx(fde[0]), "activate_callsite": hx(int(ins.address)), "metaobject_ref_sites": [hx(x) for x in meta_refs], "signal_index": idx})
    unique = {(c["fde"][0], c["fde"][1]): c for c in candidates}
    rows = list(unique.values())
    return {"queue_metaobject_reference_count": len(refs), "candidate_count": len(rows), "candidates": rows, "signal_body_target": rows[0]["target"] if len(rows) == 1 else "UNKNOWN"}


def resolve_reg(img: Image, insns: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
    if depth > 8:
        return {"classification": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    caller_saved = {"rax","rcx","rdx","rsi","rdi","r8","r9","r10","r11"}
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
                row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xffffffffffffffff)})
                return row
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = resolve_reg(img, insns, i, via, depth+1)
                row.update({"classification": nested.get("classification","UNKNOWN"), "via_register": via, "source": nested})
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
        row.update({"classification": "UNKNOWN"})
        return row
    return {"classification": f"ENTRY_ARG:{wanted}"}


def slot_function_candidates(img: Image, insns: list[Any], start: int, stop: int, signal_body: int) -> list[dict[str, Any]]:
    refs: dict[str, tuple[int,int]] = {}
    candidates: list[dict[str, Any]] = []
    for i in range(start, stop):
        ins = insns[i]
        if ins.mnemonic == "lea" and ins.operands and ins.operands[0].type == X86_OP_REG:
            target = rip_target(ins)
            if target is not None and target != signal_body and target != QUEUE_STATIC_METAOBJECT and img.executable(target):
                refs[canonical_reg(img, ins.operands[0].reg)] = (i, target)
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or int(dst.mem.disp) != Q_SLOT_FUNCTION_FIELD or src.type != X86_OP_REG:
            continue
        sreg = canonical_reg(img, src.reg)
        if sreg not in refs:
            continue
        ref_i, target = refs[sreg]
        candidates.append({"reference_site": hx(int(insns[ref_i].address)), "store_site": hx(int(ins.address)), "target": hx(target), "target_fde": [hx(x) for x in img.containing_fde(target)] if img.containing_fde(target) else None})
    unique = {c["target"]: c for c in candidates}
    return list(unique.values())


def find_connection_candidates(img: Image, signal_body: int) -> dict[str, Any]:
    refs = exec_refs(img, signal_body)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int,int]] = set()
    for ref in refs:
        fde = img.containing_fde(ref)
        if fde is None or fde in seen:
            continue
        seen.add(fde)
        insns = img.disassemble(*fde)
        body_refs = [i for i,x in enumerate(insns) if rip_target(x) == signal_body]
        meta_refs = [i for i,x in enumerate(insns) if rip_target(x) == QUEUE_STATIC_METAOBJECT]
        if not body_refs:
            continue
        for ci, ins in enumerate(insns):
            if ins.mnemonic != "call":
                continue
            tgt = direct_target(ins)
            if tgt is None:
                continue
            dm = demangle(img.plt_symbol(tgt))
            if not dm or "QObject::connectImpl(" not in dm:
                continue
            if not any(i < ci and ci - i <= 180 for i in body_refs):
                continue
            local_start = max(0, ci - 180)
            slots = slot_function_candidates(img, insns, local_start, ci, signal_body)
            row = {
                "fde": [hx(fde[0]), hx(fde[1])],
                "connect_callsite": hx(int(ins.address)),
                "connect_target": hx(tgt),
                "connect_demangled": dm,
                "signal_body_reference_sites": [hx(int(insns[i].address)) for i in body_refs if local_start <= i < ci],
                "queue_metaobject_reference_sites": [hx(int(insns[i].address)) for i in meta_refs if local_start <= i < ci],
                "receiver_provenance": resolve_reg(img, insns, ci, "rcx"),
                "slot_object_provenance": resolve_reg(img, insns, ci, "r9"),
                "slot_function_candidates": slots,
            }
            rows.append(row)
    return {"signal_body_reference_count": len(refs), "candidate_count": len(rows), "candidates": rows}


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={sha}")
    img = Image(client)
    try:
        queue_meta = decode_queue_metaobject(img)
        signal = find_signal_body(img)
        signal_body = int(signal["signal_body_target"],16) if signal["signal_body_target"] != "UNKNOWN" else None
        connections = find_connection_candidates(img, signal_body) if signal_body is not None else {"signal_body_reference_count":0,"candidate_count":0,"candidates":[]}
        receiver_identity = "UNKNOWN"
        slot_identity = "UNKNOWN"
        writer_identity = "UNKNOWN"
        next_edge = "UNKNOWN"
        terminal = "SOURCE_BLOCKER"
        if signal_body is None:
            missing = "QUEUE_SIGNAL_BF_BODY_NOT_UNIQUELY_PROVEN"
        elif connections["candidate_count"] != 1:
            missing = "QUEUE_SIGNAL_BF_CONNECTIMPL_NOT_UNIQUE"
        else:
            c = connections["candidates"][0]
            slots = c["slot_function_candidates"]
            if len(slots) != 1:
                missing = "QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN"
            else:
                slot_identity = slots[0]["target"]
                receiver_prov = c["receiver_provenance"]
                if receiver_prov.get("classification") in ("UNKNOWN", "STACK_LOAD"):
                    missing = "QUEUE_SIGNAL_BF_RECEIVER_PROVENANCE_NOT_UNIQUE"
                else:
                    receiver_identity = json.dumps(receiver_prov, sort_keys=True)
                    terminal = "QUEUE_SIGNAL_BF_RECEIVER_PROVEN"
                    missing = "QUEUE_SIGNAL_BF_RECEIVER_CLASS_OR_WRITER_TYPE_NOT_PROVEN"
        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-receiver.v1",
            "runtime_access": "none",
            "official_client_executed": False,
            "login_performed": False,
            "credentials_used": False,
            "process_memory_access": False,
            "packet_capture": False,
            "ocr_vision_used": False,
            "official_service_e2e_count": 0,
            "track_b_pr_284_modified": False,
            "exact_client": {"version":EXPECTED_VERSION,"size":EXPECTED_SIZE,"sha256":EXPECTED_SHA256},
            "queue_drain_callback": hx(DRAIN_CALLBACK),
            "queue_drain_causal_consumption": True,
            "queue_static_metaobject": hx(QUEUE_STATIC_METAOBJECT),
            "queue_metaobject": queue_meta,
            "queue_signal_index": QUEUE_SIGNAL_INDEX,
            "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
            "queue_signal_argv1_identity": "exact GameclientMessage shared pair",
            "queue_signal_body": signal,
            "queue_signal_connections": connections,
            "queue_signal_receiver_identity": receiver_identity,
            "queue_signal_slot_identity": slot_identity,
            "queue_signal_writer_identity": writer_identity,
            "next_unique_writer_edge": next_edge,
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal,
            "FIRST_MISSING_BOUNDARY": missing,
        }
    finally:
        img.close()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n",encoding="utf-8")
    return result


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--client",type=Path,required=True); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(); analyze(a.client,a.output)


if __name__ == "__main__":
    main()
