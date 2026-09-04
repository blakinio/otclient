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
QSLOT_FUNCTION_FIELD_HYPOTHESIS = 0x10
MAX_PRODUCER_INSTRUCTIONS = 256
MAX_TARGET_INSTRUCTIONS = 160


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
            Section(int(sec["sh_offset"]), int(sec["sh_size"]), int(sec["sh_addr"]), int(sec["sh_flags"]), sec.name)
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

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

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
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                got = int(ins.address) + int(ins.size) + int(op.mem.disp)
                rel = self.relocations.get(got)
                if rel and rel.get("symbol"):
                    return str(rel["symbol"])
        return None


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        proc = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
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


def writes_register(img: Image, ins: Any, register: str) -> bool:
    if not ins.operands or ins.operands[0].type != X86_OP_REG:
        return False
    return canonical_reg(img, ins.operands[0].reg) == register


def target_identity(img: Image, target: int | None) -> dict[str, Any]:
    if target is None:
        return {"target": None, "symbol": None, "demangled": None, "fde": None}
    raw_symbol = img.plt_symbol(target)
    direct_symbols = img.symbol_names(target)
    symbol = raw_symbol or (direct_symbols[0] if len(direct_symbols) == 1 else None)
    fde = img.containing_fde(target)
    return {
        "target": hx(target),
        "symbol": symbol,
        "demangled": demangle(symbol),
        "direct_symbols": direct_symbols,
        "fde": [hx(fde[0]), hx(fde[1])] if fde else None,
    }


def resolve_qslot_producer(img: Image) -> dict[str, Any]:
    fde = img.containing_fde(CONNECTIMPL_CALLSITE)
    result: dict[str, Any] = {
        "proven": False,
        "connectimpl_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
        "qslot_producer_callsite": hx(QSLOT_PRODUCER_CALLSITE),
        "handoff": "UNKNOWN",
    }
    if fde != CONNECTIMPL_FDE:
        result["classification"] = "CONNECTIMPL_FDE_MISMATCH"
        result["actual_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result
    insns = img.disassemble(*CONNECTIMPL_FDE)
    connect = instruction_at(insns, CONNECTIMPL_CALLSITE)
    producer = instruction_at(insns, QSLOT_PRODUCER_CALLSITE)
    if connect is None or connect.mnemonic != "call":
        result["classification"] = "CONNECTIMPL_CALLSITE_NOT_EXACT"
        return result
    connect_target = direct_target(connect)
    connect_id = target_identity(img, connect_target)
    result["connectimpl_target"] = connect_id
    if "QObject::connectImpl(" not in str(connect_id.get("demangled") or ""):
        result["classification"] = "CONNECTIMPL_TARGET_IDENTITY_MISMATCH"
        return result
    if producer is None or producer.mnemonic != "call":
        result["classification"] = "QSLOT_PRODUCER_CALLSITE_NOT_EXACT"
        return result
    producer_target = direct_target(producer)
    result["producer_target"] = target_identity(img, producer_target)
    if producer_target is None or img.containing_fde(producer_target) is None:
        result["classification"] = "QSLOT_PRODUCER_TARGET_FDE_NOT_PROVEN"
        return result
    producer_index = insns.index(producer)
    connect_index = insns.index(connect)
    handoffs = []
    for ins in insns[producer_index + 1 : connect_index]:
        if (
            ins.mnemonic == "mov"
            and len(ins.operands) >= 2
            and ins.operands[0].type == X86_OP_REG
            and ins.operands[1].type == X86_OP_REG
            and canonical_reg(img, ins.operands[0].reg) == "r9"
            and canonical_reg(img, ins.operands[1].reg) == "rax"
        ):
            handoffs.append(ins)
    if len(handoffs) != 1:
        result["classification"] = "QSLOT_RAX_TO_R9_HANDOFF_NOT_UNIQUE"
        result["handoff_sites"] = [hx(int(ins.address)) for ins in handoffs]
        return result
    handoff = handoffs[0]
    for ins in insns[producer_index + 1 : insns.index(handoff)]:
        if writes_register(img, ins, "rax"):
            result["classification"] = "QSLOT_PRODUCER_RAX_REDEFINED_BEFORE_HANDOFF"
            result["redefinition_site"] = hx(int(ins.address))
            return result
    result.update({
        "classification": "QSLOT_PRODUCER_CALL_RETURN_PROVEN",
        "proven": True,
        "handoff": f"{hx(int(handoff.address))}: r9 <- rax",
        "handoff_site": hx(int(handoff.address)),
        "producer_call_target": hx(producer_target),
        "producer_fde": result["producer_target"]["fde"],
    })
    return result


def _bounded_function_summary(img: Image, fde: tuple[int, int], limit: int) -> dict[str, Any]:
    insns = img.disassemble(*fde)
    if len(insns) > limit:
        return {"classification": "FUNCTION_EXCEEDS_BOUNDED_INSTRUCTION_LIMIT", "instruction_count": len(insns)}
    direct_calls = []
    executable_leas = []
    for ins in insns:
        call_target = direct_target(ins)
        if ins.mnemonic == "call" and call_target is not None:
            direct_calls.append({"site": hx(int(ins.address)), **target_identity(img, call_target)})
        if ins.mnemonic == "lea" and ins.operands and ins.operands[0].type == X86_OP_REG:
            target = rip_target(ins)
            if target is not None and img.is_executable_va(target):
                executable_leas.append({
                    "site": hx(int(ins.address)),
                    "register": canonical_reg(img, ins.operands[0].reg),
                    **target_identity(img, target),
                })
    return {
        "classification": "BOUNDED_FUNCTION_SUMMARY",
        "fde": [hx(fde[0]), hx(fde[1])],
        "instruction_count": len(insns),
        "direct_calls": direct_calls,
        "executable_leas": executable_leas,
        "instruction_window": [
            {"address": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
            for ins in insns
        ],
    }


def resolve_qslot_function(img: Image, producer: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "qslot_function_field_hypothesis": hx(QSLOT_FUNCTION_FIELD_HYPOTHESIS),
        "function_target": "UNKNOWN",
    }
    if not producer.get("proven"):
        result["classification"] = "QSLOT_PRODUCER_NOT_PROVEN"
        return result
    target_text = producer.get("producer_call_target")
    target = int(str(target_text), 16)
    fde = img.containing_fde(target)
    if fde is None:
        result["classification"] = "QSLOT_PRODUCER_FDE_NOT_PROVEN"
        return result
    summary = _bounded_function_summary(img, fde, MAX_PRODUCER_INSTRUCTIONS)
    result["producer_summary"] = summary
    if summary.get("classification") != "BOUNDED_FUNCTION_SUMMARY":
        result["classification"] = summary["classification"]
        return result

    insns = img.disassemble(*fde)
    code_refs: dict[str, dict[str, Any]] = {}
    object_aliases: set[str] = set()
    pointer_stores: list[dict[str, Any]] = []
    allocation_calls: list[dict[str, Any]] = []

    for ins in insns:
        if ins.mnemonic == "call":
            target2 = direct_target(ins)
            ident = target_identity(img, target2)
            name = str(ident.get("demangled") or "")
            if "operator new" in name:
                object_aliases = {"rax"}
                allocation_calls.append({"site": hx(int(ins.address)), **ident})
            else:
                object_aliases.discard("rax")
            code_refs.pop("rax", None)
            continue

        if not ins.operands:
            continue
        dst = ins.operands[0]
        src = ins.operands[1] if len(ins.operands) > 1 else None

        if ins.mnemonic == "lea" and dst.type == X86_OP_REG:
            dst_reg = canonical_reg(img, dst.reg)
            target2 = rip_target(ins)
            if target2 is not None and img.is_executable_va(target2):
                code_refs[dst_reg] = {"reference_site": hx(int(ins.address)), **target_identity(img, target2)}
            else:
                code_refs.pop(dst_reg, None)
            object_aliases.discard(dst_reg)
            continue

        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_REG and src is not None:
            dst_reg = canonical_reg(img, dst.reg)
            if src.type == X86_OP_REG:
                src_reg = canonical_reg(img, src.reg)
                if src_reg in code_refs:
                    code_refs[dst_reg] = dict(code_refs[src_reg])
                else:
                    code_refs.pop(dst_reg, None)
                if src_reg in object_aliases:
                    object_aliases.add(dst_reg)
                else:
                    object_aliases.discard(dst_reg)
            else:
                code_refs.pop(dst_reg, None)
                object_aliases.discard(dst_reg)
            continue

        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_MEM and src is not None:
            base = canonical_reg(img, dst.mem.base) if dst.mem.base else None
            disp = int(dst.mem.disp)
            source_ref = None
            if src.type == X86_OP_REG:
                source_ref = code_refs.get(canonical_reg(img, src.reg))
            elif src.type == X86_OP_IMM and img.is_executable_va(int(src.imm)):
                source_ref = {"reference_site": hx(int(ins.address)), **target_identity(img, int(src.imm))}
            if source_ref is not None:
                pointer_stores.append({
                    "store_site": hx(int(ins.address)),
                    "base_register": base,
                    "base_is_allocated_object_alias": base in object_aliases if base else False,
                    "field_offset": hx(disp),
                    **source_ref,
                })
            continue

        if dst.type == X86_OP_REG:
            dst_reg = canonical_reg(img, dst.reg)
            code_refs.pop(dst_reg, None)
            object_aliases.discard(dst_reg)

    result["allocation_calls"] = allocation_calls
    result["executable_pointer_stores"] = pointer_stores
    exact = [
        row for row in pointer_stores
        if row.get("field_offset") == hx(QSLOT_FUNCTION_FIELD_HYPOTHESIS)
        and row.get("base_is_allocated_object_alias") is True
        and row.get("target")
    ]
    unique_targets = sorted({str(row["target"]) for row in exact})
    if len(unique_targets) != 1:
        result["classification"] = "QSLOT_FUNCTION_POINTER_STORE_NOT_UNIQUE"
        result["candidate_count"] = len(exact)
        result["candidate_targets"] = unique_targets
        return result

    function_target = int(unique_targets[0], 16)
    target_fde = img.containing_fde(function_target)
    if target_fde is None:
        result["classification"] = "QSLOT_FUNCTION_TARGET_FDE_NOT_PROVEN"
        return result
    result.update({
        "classification": "QSLOT_FUNCTION_POINTER_STORE_UNIQUE",
        "proven": True,
        "function_target": hx(function_target),
        "function_target_identity": target_identity(img, function_target),
        "function_target_summary": _bounded_function_summary(img, target_fde, MAX_TARGET_INSTRUCTIONS),
        "pointer_store": exact[0],
    })
    return result


def trace_one_writer_edge(img: Image, slot: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"proven": False, "writer_identity": "UNKNOWN", "next_edge": "UNKNOWN"}
    if not slot.get("proven"):
        result["classification"] = "QSLOT_IDENTITY_NOT_PROVEN"
        return result
    target = int(str(slot["function_target"]), 16)
    fde = img.containing_fde(target)
    if fde is None:
        result["classification"] = "QSLOT_TARGET_FDE_NOT_PROVEN"
        return result
    summary = _bounded_function_summary(img, fde, MAX_TARGET_INSTRUCTIONS)
    result["slot_target_summary"] = summary
    direct_calls = summary.get("direct_calls", []) if isinstance(summary, dict) else []
    identity_calls = [
        row for row in direct_calls
        if row.get("demangled") and "operator delete" not in str(row.get("demangled"))
    ]
    if len(identity_calls) != 1:
        result["classification"] = "NEXT_WRITER_EDGE_NOT_UNIQUE"
        result["identity_preserving_direct_call_candidates"] = identity_calls
        return result
    row = identity_calls[0]
    result.update({
        "classification": "ONE_DIRECT_EDGE_CANDIDATE_ONLY",
        "proven": True,
        "writer_identity": row.get("demangled") or row.get("symbol") or row.get("target"),
        "next_edge": row,
    })
    return result


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")
    img = Image(client)
    try:
        producer = resolve_qslot_producer(img)
        slot = resolve_qslot_function(img, producer)
        writer = trace_one_writer_edge(img, slot)

        qslot_identity_proven = bool(slot.get("proven"))
        if not producer.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(producer.get("classification") or "QSLOT_PRODUCER_NOT_PROVEN")
        elif not qslot_identity_proven:
            terminal_result = "SOURCE_BLOCKER"
            missing = str(slot.get("classification") or "QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN")
        elif writer.get("proven"):
            terminal_result = "FINAL_WRITER_EDGE_PROVEN"
            missing = "NONE"
        else:
            terminal_result = "QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN"
            missing = str(writer.get("classification") or "NEXT_WRITER_EDGE_NOT_UNIQUE")

        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-qslot-identity.v1",
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
