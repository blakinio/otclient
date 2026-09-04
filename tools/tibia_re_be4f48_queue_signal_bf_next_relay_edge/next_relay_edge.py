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
QUEUE_STATIC_METAOBJECT = 0x30B73E0
SELF_RELAY_CONNECTIMPL_CALLSITE = 0xBE2EEE
CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)
CONNECTIMPL_TARGET = 0x4D6800
PROMOTED_RECEIVER_IDENTITY = "tibia::protocol::TProtocolMessageQueue"
PROMOTED_CONNECTION_ROLE = "SIGNAL_RELAY"
PROMOTED_ARGV1_IDENTITY = "exact GameclientMessage shared pair"
PROMOTED_QSLOT_FUNCTION_TARGET = 0xBD2190
MAX_LOCAL_BACKWARD_INSTRUCTIONS = 180
Q_SLOT_FUNCTION_FIELD = 0x10


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


def target_identity(img: Image, target: int | None) -> dict[str, Any]:
    if target is None:
        return {"target": None, "symbol": None, "demangled": None, "fde": None}
    symbols = img.symbol_names(target)
    symbol = img.plt_symbol(target) or (symbols[0] if len(symbols) == 1 else None)
    fde = img.containing_fde(target)
    return {
        "target": hx(target),
        "symbol": symbol,
        "demangled": demangle(symbol),
        "fde": [hx(fde[0]), hx(fde[1])] if fde else None,
    }


def _resolve_reg(img: Image, insns: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
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
            row.update({"classification": "OBJECT_ADDRESS", "base_register": base, "displacement": hx(int(src.mem.disp))})
            return row
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_IMM:
                row.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return row
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = _resolve_reg(img, insns, i, via, depth + 1)
                row.update({"classification": nested.get("classification", "UNKNOWN"), "via_register": via, "source": nested})
                return row
            if src.type == X86_OP_MEM:
                target = rip_target(ins)
                if target is not None:
                    row.update({"classification": "STATIC_POINTER_LOAD", "address": hx(target), "value": hx(img.qword(target))})
                    return row
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                row.update({"classification": "OBJECT_FIELD", "base_register": base, "displacement": hx(int(src.mem.disp))})
                return row
        row["classification"] = "UNKNOWN"
        return row
    return {"classification": f"ENTRY_ARG:{wanted}"}


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
        rows.append({
            "reference_site": hx(int(insns[ref_index].address)),
            "store_site": hx(int(ins.address)),
            "target": hx(target),
        })
    unique = {str(row["target"]): row for row in rows}
    return [unique[key] for key in sorted(unique)]


def trace_connect_arguments(img: Image, insns: list[Any], call_index: int) -> dict[str, Any]:
    call = insns[call_index]
    callsite = int(call.address)
    local_start = max(0, call_index - MAX_LOCAL_BACKWARD_INSTRUCTIONS)
    body_refs = [
        hx(int(ins.address))
        for ins in insns[local_start:call_index]
        if rip_target(ins) == QUEUE_SIGNAL_BODY
    ]
    meta_refs = [
        hx(int(ins.address))
        for ins in insns[local_start:call_index]
        if rip_target(ins) == QUEUE_STATIC_METAOBJECT
    ]
    if callsite == SELF_RELAY_CONNECTIMPL_CALLSITE:
        slot_candidates = [{"target": hx(PROMOTED_QSLOT_FUNCTION_TARGET), "classification": "PROMOTED_NOT_RECONSTRUCTED"}]
        receiver = {"classification": "ENTRY_ARG:rdi", "identity": PROMOTED_RECEIVER_IDENTITY, "provenance": "PROMOTED_NOT_RECONSTRUCTED"}
    else:
        slot_candidates = _slot_function_candidates(img, insns, local_start, call_index)
        receiver = _resolve_reg(img, insns, call_index, "rcx")
    body_is_slot = any(row.get("target") == hx(QUEUE_SIGNAL_BODY) for row in slot_candidates)
    return {
        "callsite": hx(callsite),
        "sender_provenance": _resolve_reg(img, insns, call_index, "rdi"),
        "signal_argument_provenance": _resolve_reg(img, insns, call_index, "rsi"),
        "method_argument_provenance": _resolve_reg(img, insns, call_index, "rdx"),
        "receiver_provenance": receiver,
        "aux_argument_provenance": _resolve_reg(img, insns, call_index, "r8"),
        "slot_object_provenance": {"classification": "PROMOTED_NOT_RECONSTRUCTED"} if callsite == SELF_RELAY_CONNECTIMPL_CALLSITE else _resolve_reg(img, insns, call_index, "r9"),
        "queue_signal_body_reference_sites": body_refs,
        "queue_static_metaobject_reference_sites": meta_refs,
        "slot_function_candidates": slot_candidates,
        "queue_signal_body_used_as_slot_callable": body_is_slot,
        "identity_preserving_source_candidate": bool(body_refs and not body_is_slot),
    }


def enumerate_bounded_connect_candidates(img: Image) -> dict[str, Any]:
    actual_fde = img.containing_fde(SELF_RELAY_CONNECTIMPL_CALLSITE)
    result: dict[str, Any] = {
        "scope": "queue constructor FDE only",
        "expected_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "connectimpl_target": target_identity(img, CONNECTIMPL_TARGET),
        "candidate_count": 0,
        "candidates": [],
    }
    if actual_fde != CONNECTIMPL_FDE:
        result["classification"] = "QUEUE_CONSTRUCTOR_FDE_MISMATCH"
        result["actual_fde"] = [hx(actual_fde[0]), hx(actual_fde[1])] if actual_fde else None
        return result
    insns = img.disassemble(*CONNECTIMPL_FDE)
    rows: list[dict[str, Any]] = []
    for index, ins in enumerate(insns):
        if ins.mnemonic != "call" or direct_target(ins) != CONNECTIMPL_TARGET:
            continue
        callsite = int(ins.address)
        relation = "SELF_RELAY" if callsite == SELF_RELAY_CONNECTIMPL_CALLSITE else ("BEFORE_SELF_RELAY" if callsite < SELF_RELAY_CONNECTIMPL_CALLSITE else "AFTER_SELF_RELAY")
        rows.append({
            "callsite": hx(callsite),
            "relation_to_promoted_self_relay": relation,
            "arguments": trace_connect_arguments(img, insns, index),
        })
    result["candidate_count"] = len(rows)
    result["candidates"] = rows
    self_rows = [row for row in rows if row["relation_to_promoted_self_relay"] == "SELF_RELAY"]
    result["self_relay_present_exactly_once"] = len(self_rows) == 1
    result["classification"] = "BOUNDED_QUEUE_CONSTRUCTOR_CONNECTS_ENUMERATED" if len(self_rows) == 1 else "PROMOTED_SELF_RELAY_NOT_EXACT_IN_FDE"
    return result


def _endpoint_identity(row: dict[str, Any]) -> tuple[str, str]:
    args = row["arguments"]
    receiver = args.get("receiver_provenance", {})
    if receiver.get("classification") == "ENTRY_ARG:rdi":
        return PROMOTED_RECEIVER_IDENTITY, "receiver entry object uses promoted exact type"
    slots = [candidate for candidate in args.get("slot_function_candidates", []) if candidate.get("target") != hx(QUEUE_SIGNAL_BODY)]
    if len(slots) == 1:
        return f"callable:{slots[0]['target']}", "unique bounded callable target"
    return "UNKNOWN", "endpoint type/callable is not unique in bounded connection context"


def classify_next_relay_edge(connections: dict[str, Any]) -> dict[str, Any]:
    if not connections.get("self_relay_present_exactly_once"):
        return {
            "terminal_result": "SOURCE_BLOCKER",
            "first_missing_boundary": "PROMOTED_SELF_RELAY_NOT_EXACTLY_PRESENT_IN_BOUNDED_QUEUE_CONSTRUCTOR_FDE",
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "next_relay_identity_preserved": False,
        }
    rows = [
        row
        for row in connections.get("candidates", [])
        if row.get("relation_to_promoted_self_relay") != "SELF_RELAY"
        and row.get("arguments", {}).get("identity_preserving_source_candidate") is True
    ]
    if not rows:
        return {
            "terminal_result": "SOURCE_BLOCKER",
            "first_missing_boundary": "NO_ADDITIONAL_IDENTITY_PRESERVING_QUEUE_SIGNAL_CONNECT_IN_BOUNDED_CONSTRUCTOR_CONTEXT",
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "next_relay_identity_preserved": False,
        }
    if len(rows) != 1:
        return {
            "terminal_result": "SOURCE_BLOCKER",
            "first_missing_boundary": "MULTIPLE_IDENTITY_PRESERVING_QUEUE_SIGNAL_CONNECTS_IN_BOUNDED_CONSTRUCTOR_CONTEXT",
            "candidate_callsites": [row["callsite"] for row in rows],
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "next_relay_identity_preserved": False,
        }
    row = rows[0]
    endpoint, endpoint_basis = _endpoint_identity(row)
    if endpoint == "UNKNOWN":
        return {
            "terminal_result": "SOURCE_BLOCKER",
            "first_missing_boundary": f"UNIQUE_QUEUE_SIGNAL_CONNECT_AT_{row['callsite']}_ENDPOINT_IDENTITY_NOT_UNIQUELY_PROVEN",
            "candidate_callsites": [row["callsite"]],
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "next_relay_identity_preserved": False,
        }
    return {
        "terminal_result": "QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_PROVEN",
        "first_missing_boundary": "none",
        "next_unique_relay_edge": row["callsite"],
        "next_endpoint_identity": endpoint,
        "next_endpoint_identity_basis": endpoint_basis,
        "next_relay_identity_preserved": True,
    }


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    actual_size = len(raw)
    if actual_size != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={actual_size} sha256={actual_sha}")
    img = Image(client)
    try:
        connections = enumerate_bounded_connect_candidates(img)
        decision = classify_next_relay_edge(connections)
        endpoint = decision["next_endpoint_identity"]
        writer_like = endpoint != "UNKNOWN" and any(token in endpoint.lower() for token in ("writer", "socket", "network", "transport"))
        result = {
            "schema": "otclient.track-a.be4f48-queue-signal-bf-next-relay-edge.v1",
            "runtime_access": "none",
            "official_client_executed": False,
            "login_performed": False,
            "credentials_used": False,
            "process_memory_access": False,
            "packet_capture": False,
            "ocr_vision_used": False,
            "official_service_e2e_count": 0,
            "track_b_pr_284_modified": False,
            "track_b_current_wire_delta": "NOT_PROVEN",
            "exact_client_fence_proven": True,
            "exact_client": {"version": EXPECTED_VERSION, "size": EXPECTED_SIZE, "sha256": EXPECTED_SHA256},
            "queue_signal_name": QUEUE_SIGNAL_NAME,
            "queue_signal_index": QUEUE_SIGNAL_INDEX,
            "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
            "queue_signal_argv1_identity": PROMOTED_ARGV1_IDENTITY,
            "queue_signal_receiver_identity": PROMOTED_RECEIVER_IDENTITY,
            "queue_signal_connection_role": PROMOTED_CONNECTION_ROLE,
            "qslot_function_target": hx(PROMOTED_QSLOT_FUNCTION_TARGET),
            "promoted_self_relay_callsite": hx(SELF_RELAY_CONNECTIMPL_CALLSITE),
            "bounded_connection_context": connections,
            "next_unique_relay_edge": decision["next_unique_relay_edge"],
            "next_endpoint_identity": endpoint,
            "next_relay_identity_preserved": decision["next_relay_identity_preserved"],
            "next_relay_gameclientmessage_pair": PROMOTED_ARGV1_IDENTITY if decision["next_relay_identity_preserved"] else "UNKNOWN",
            "queue_signal_writer_identity": endpoint if writer_like else "UNKNOWN",
            "final_queue_writer_identified": bool(writer_like),
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": decision["terminal_result"],
            "FIRST_MISSING_BOUNDARY": decision["first_missing_boundary"],
            "NEXT_ACTION": "clean coordinator promotion from fresh trusted main" if decision["terminal_result"] == "QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_PROVEN" else "clean coordinator promotion of the precise bounded source blocker before admitting any further source step",
        }
        for key in ("candidate_callsites", "next_endpoint_identity_basis"):
            if key in decision:
                result[key] = decision[key]
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
