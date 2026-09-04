#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
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
MAX_SLOT_TARGET_INSTRUCTIONS = 192


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
        if not ins.operands or ins.operands[0].type != X86_OP_REG:
            continue
        if canonical_reg(img, ins.operands[0].reg) == "rax":
            result["classification"] = "QSLOT_ALLOCATION_RAX_REDEFINED_BEFORE_HANDOFF"
            result["redefinition_site"] = hx(int(ins.address))
            return result
    for ins in insns[handoff_index + 1 : connect_index]:
        if not ins.operands or ins.operands[0].type != X86_OP_REG:
            continue
        if canonical_reg(img, ins.operands[0].reg) == "r9":
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
        "executable_pointer_stores": [],
    }
    if not producer.get("proven"):
        result["classification"] = "QSLOT_PRODUCER_NOT_PROVEN"
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    window = [
        ins for ins in insns
        if QSLOT_CONSTRUCTION_WINDOW[0] <= int(ins.address) < QSLOT_CONSTRUCTION_WINDOW[1]
    ]
    result["instructions"] = [
        {"address": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        for ins in window
    ]
    alloc = instruction_at(insns, QSLOT_PRODUCER_CALLSITE)
    handoff_site = int(str(producer["handoff_site"]), 16)
    handoff = instruction_at(insns, handoff_site)
    if alloc is None or handoff is None:
        result["classification"] = "CONSTRUCTION_BOUNDARY_INSTRUCTION_MISSING"
        return result
    alloc_index = insns.index(alloc)
    handoff_index = insns.index(handoff)
    if alloc_index >= handoff_index:
        result["classification"] = "CONSTRUCTION_BOUNDARY_ORDER_INVALID"
        return result

    object_aliases: set[str] = {"rax"}
    code_refs: dict[str, dict[str, Any]] = {}
    object_field_writes: list[dict[str, Any]] = []
    executable_pointer_stores: list[dict[str, Any]] = []

    for ins in insns[alloc_index + 1 : handoff_index]:
        if ins.mnemonic == "call":
            result["classification"] = "CONSTRUCTION_WINDOW_HAS_INTERVENING_CALL"
            result["intervening_callsite"] = hx(int(ins.address))
            return result
        if not ins.operands:
            continue
        dst = ins.operands[0]
        src = ins.operands[1] if len(ins.operands) > 1 else None

        if ins.mnemonic == "lea" and dst.type == X86_OP_REG:
            dst_reg = canonical_reg(img, dst.reg)
            target = rip_target(ins)
            if target is not None and img.is_executable_va(target) and img.containing_fde(target) is not None:
                code_refs[dst_reg] = {
                    "reference_site": hx(int(ins.address)),
                    **target_identity(img, target),
                }
            else:
                code_refs.pop(dst_reg, None)
            object_aliases.discard(dst_reg)
            continue

        if ins.mnemonic.startswith("mov") and dst.type == X86_OP_REG and src is not None:
            dst_reg = canonical_reg(img, dst.reg)
            if src.type == X86_OP_REG:
                src_reg = canonical_reg(img, src.reg)
                if src_reg in object_aliases:
                    object_aliases.add(dst_reg)
                else:
                    object_aliases.discard(dst_reg)
                if src_reg in code_refs:
                    code_refs[dst_reg] = dict(code_refs[src_reg])
                else:
                    code_refs.pop(dst_reg, None)
            elif src.type == X86_OP_IMM:
                object_aliases.discard(dst_reg)
                target = int(src.imm) & 0xFFFFFFFFFFFFFFFF
                if img.is_executable_va(target) and img.containing_fde(target) is not None:
                    code_refs[dst_reg] = {
                        "reference_site": hx(int(ins.address)),
                        **target_identity(img, target),
                    }
                else:
                    code_refs.pop(dst_reg, None)
            else:
                object_aliases.discard(dst_reg)
                code_refs.pop(dst_reg, None)
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
            code_ref = None
            if src.type == X86_OP_REG:
                src_reg = canonical_reg(img, src.reg)
                row["source_kind"] = f"REGISTER:{src_reg}"
                code_ref = code_refs.get(src_reg)
            elif src.type == X86_OP_IMM:
                value = int(src.imm) & 0xFFFFFFFFFFFFFFFF
                row["source_kind"] = "IMMEDIATE"
                row["immediate"] = hx(value)
                if img.is_executable_va(value) and img.containing_fde(value) is not None:
                    code_ref = {"reference_site": hx(int(ins.address)), **target_identity(img, value)}
            elif src.type == X86_OP_MEM:
                row["source_kind"] = "MEMORY"
                target = rip_target(ins)
                if target is not None:
                    row["source_address"] = hx(target)
            if code_ref is not None:
                row["executable_target"] = code_ref
                executable_pointer_stores.append(dict(row))
            object_field_writes.append(row)
            continue

        if dst.type == X86_OP_REG:
            dst_reg = canonical_reg(img, dst.reg)
            object_aliases.discard(dst_reg)
            code_refs.pop(dst_reg, None)

    result.update({
        "classification": "QSLOT_INLINE_CONSTRUCTION_WINDOW_PROVEN",
        "proven": True,
        "fresh_object_origin": f"operator new return @ {hx(QSLOT_PRODUCER_CALLSITE)}",
        "handoff_site": hx(handoff_site),
        "object_field_writes": object_field_writes,
        "executable_pointer_stores": executable_pointer_stores,
    })
    return result


def bounded_target_summary(img: Image, target: int) -> dict[str, Any]:
    fde = img.containing_fde(target)
    if fde is None:
        return {"classification": "TARGET_FDE_NOT_PROVEN", "target": hx(target)}
    insns = img.disassemble(*fde)
    calls = []
    for ins in insns[:MAX_SLOT_TARGET_INSTRUCTIONS]:
        if ins.mnemonic != "call":
            continue
        call_target = direct_target(ins)
        calls.append({"site": hx(int(ins.address)), **target_identity(img, call_target)})
    return {
        "classification": "BOUNDED_SLOT_TARGET_SUMMARY",
        "target": hx(target),
        "fde": [hx(fde[0]), hx(fde[1])],
        "instruction_count": len(insns),
        "summary_instruction_limit": MAX_SLOT_TARGET_INSTRUCTIONS,
        "fully_within_limit": len(insns) <= MAX_SLOT_TARGET_INSTRUCTIONS,
        "direct_calls_in_bounded_prefix": calls,
    }


def resolve_qslot_function(img: Image, construction: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "function_target": "UNKNOWN",
        "proof_basis": "fresh operator-new object + unique executable code pointer store before direct r9 handoff to connectImpl",
    }
    if not construction.get("proven"):
        result["classification"] = "QSLOT_CONSTRUCTION_WINDOW_NOT_PROVEN"
        return result
    stores = list(construction.get("executable_pointer_stores") or [])
    targets = sorted({
        str(row.get("executable_target", {}).get("target"))
        for row in stores
        if row.get("executable_target", {}).get("target")
    })
    result["candidate_store_count"] = len(stores)
    result["candidate_targets"] = targets
    result["candidate_stores"] = stores
    if len(stores) != 1 or len(targets) != 1:
        result["classification"] = "QSLOT_EXECUTABLE_POINTER_STORE_NOT_UNIQUE"
        return result
    target = int(targets[0], 16)
    if img.containing_fde(target) is None:
        result["classification"] = "QSLOT_EXECUTABLE_POINTER_TARGET_FDE_NOT_PROVEN"
        return result
    result.update({
        "classification": "QSLOT_FUNCTION_TARGET_STRUCTURALLY_PROVEN",
        "proven": True,
        "function_target": hx(target),
        "function_target_identity": target_identity(img, target),
        "function_pointer_store": stores[0],
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
    elif len(calls) == 0:
        result["classification"] = "NEXT_WRITER_EDGE_NO_DIRECT_CALL_IN_SLOT_TARGET"
    elif len(calls) == 1:
        result["classification"] = "ONE_DIRECT_CALL_PRESENT_BUT_WRITER_SEMANTICS_NOT_PROVEN"
        result["next_edge"] = calls[0]
    else:
        result["classification"] = "NEXT_WRITER_EDGE_NOT_UNIQUE"
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
        slot = resolve_qslot_function(img, construction)
        writer = trace_one_writer_edge(img, slot)
        qslot_identity_proven = bool(slot.get("proven"))

        if not producer.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(producer.get("classification") or "QSLOT_PRODUCER_NOT_PROVEN")
        elif not construction.get("proven"):
            terminal_result = "SOURCE_BLOCKER"
            missing = str(construction.get("classification") or "QSLOT_CONSTRUCTION_NOT_PROVEN")
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
            "schema": "otclient.track-a.be4f48-queue-signal-bf-qslot-identity.v2",
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
