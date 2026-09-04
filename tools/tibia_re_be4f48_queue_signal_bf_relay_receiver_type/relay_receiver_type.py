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
QUEUE_SIGNAL_OWNER = "tibia::protocol::TProtocolMessageQueue"
QUEUE_SIGNAL_INDEX = 0xBF
CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)
CONNECTIMPL_CALLSITE = 0xBE2EEE
CONNECTIMPL_TARGET = 0x4D6800
RECEIVER_PROVENANCE = "ENTRY_ARG:rdi"
QSLOT_FUNCTION_TARGET = 0xBD2190
MAX_CSTRING = 512

CALLER_SAVED = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


@dataclass(frozen=True)
class Section:
    offset: int
    size: int
    va: int
    flags: int
    name: str


@dataclass(frozen=True)
class Value:
    kind: str
    value: int = 0


UNKNOWN = Value("unknown", 0)
ENTRY_RDI = Value("entry_rdi", 0)


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

    def cstring(self, va: int) -> str | None:
        if not self.mapped(va):
            return None
        out = bytearray()
        for offset in range(MAX_CSTRING):
            if not self.mapped(va + offset):
                return None
            byte = self.read(va + offset, 1)[0]
            if byte == 0:
                break
            out.append(byte)
        else:
            return None
        try:
            text = out.decode("utf-8")
        except UnicodeDecodeError:
            return None
        return text if text and all(ch.isprintable() for ch in text) else None

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

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
        return {"target": None, "symbol": None, "demangled": None}
    direct_symbols = img.symbol_names(target)
    symbol = img.plt_symbol(target) or (direct_symbols[0] if len(direct_symbols) == 1 else None)
    return {
        "target": hx(target),
        "symbol": symbol,
        "demangled": demangle(symbol),
        "direct_symbols": direct_symbols,
    }


def explicit_register_writes(img: Image, ins: Any) -> set[str]:
    try:
        _, written = ins.regs_access()
        return {canonical_reg(img, reg) for reg in written}
    except Exception:
        if ins.operands and ins.operands[0].type == X86_OP_REG:
            return {canonical_reg(img, ins.operands[0].reg)}
        return set()


def pointer_from_rip_memory(img: Image, ins: Any) -> int | None:
    target = rip_target(ins)
    if target is None:
        return None
    if ins.mnemonic == "lea":
        return target
    if ins.mnemonic.startswith("mov"):
        value = img.qword(target)
        return value if value and img.mapped(value) else None
    return None


def trace_entry_receiver(img: Image, insns: list[Any]) -> dict[str, Any]:
    regs: dict[str, Value] = {"rdi": ENTRY_RDI}
    object_pointer_stores: list[dict[str, Any]] = []
    bounded_calls: list[dict[str, Any]] = []
    receiver_value_at_connect = UNKNOWN

    for ins in insns:
        address = int(ins.address)
        if address > CONNECTIMPL_CALLSITE:
            break

        if ins.mnemonic == "call":
            target = direct_target(ins)
            bounded_calls.append({"site": hx(address), **target_identity(img, target)})
            if address == CONNECTIMPL_CALLSITE:
                receiver_value_at_connect = regs.get("rdi", UNKNOWN)
                break
            for reg in CALLER_SAVED:
                regs[reg] = UNKNOWN
            continue

        if ins.mnemonic.startswith("mov") and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_MEM and src.type == X86_OP_REG:
                base = canonical_reg(img, dst.mem.base) if dst.mem.base else ""
                base_value = regs.get(base, UNKNOWN)
                src_value = regs.get(canonical_reg(img, src.reg), UNKNOWN)
                if base_value.kind == "entry_rdi" and src_value.kind == "ptr" and int(dst.mem.index) == 0:
                    object_pointer_stores.append({
                        "site": hx(address),
                        "object_offset": hx(base_value.value + int(dst.mem.disp)),
                        "pointer": hx(src_value.value),
                        "source_register": canonical_reg(img, src.reg),
                    })
            if dst.type == X86_OP_REG:
                dst_reg = canonical_reg(img, dst.reg)
                if src.type == X86_OP_REG:
                    regs[dst_reg] = regs.get(canonical_reg(img, src.reg), UNKNOWN)
                elif src.type == X86_OP_IMM:
                    value = int(src.imm) & 0xFFFFFFFFFFFFFFFF
                    regs[dst_reg] = Value("ptr", value) if img.mapped(value) else UNKNOWN
                elif src.type == X86_OP_MEM:
                    ptr = pointer_from_rip_memory(img, ins)
                    regs[dst_reg] = Value("ptr", ptr) if ptr is not None else UNKNOWN
                else:
                    regs[dst_reg] = UNKNOWN
            continue

        if ins.mnemonic == "lea" and len(ins.operands) >= 2 and ins.operands[0].type == X86_OP_REG:
            dst_reg = canonical_reg(img, ins.operands[0].reg)
            src = ins.operands[1]
            if src.type != X86_OP_MEM:
                regs[dst_reg] = UNKNOWN
                continue
            if src.mem.base == X86_REG_RIP:
                target = int(ins.address) + int(ins.size) + int(src.mem.disp)
                regs[dst_reg] = Value("ptr", target)
                continue
            base = canonical_reg(img, src.mem.base) if src.mem.base else ""
            base_value = regs.get(base, UNKNOWN)
            if int(src.mem.index) == 0 and base_value.kind == "entry_rdi":
                regs[dst_reg] = Value("entry_rdi", base_value.value + int(src.mem.disp))
            else:
                regs[dst_reg] = UNKNOWN
            continue

        for reg in explicit_register_writes(img, ins):
            if reg not in ("rsp", "rip"):
                regs[reg] = UNKNOWN

    return {
        "classification": "ENTRY_RDI_TO_CONNECT_PROVEN" if receiver_value_at_connect == ENTRY_RDI else "ENTRY_RDI_TO_CONNECT_NOT_REPROVEN",
        "receiver_value_at_connect": {"kind": receiver_value_at_connect.kind, "offset": hx(receiver_value_at_connect.value)},
        "receiver_identity_preserved": receiver_value_at_connect == ENTRY_RDI,
        "object_pointer_stores": object_pointer_stores,
        "bounded_direct_calls": bounded_calls,
    }


def normalize_type_name(value: str | None) -> str | None:
    if not value:
        return None
    for prefix in ("vtable for ", "typeinfo for ", "typeinfo name for "):
        if value.startswith(prefix):
            return value[len(prefix) :]
    return value


def decode_vptr(img: Image, pointer: int) -> dict[str, Any]:
    result: dict[str, Any] = {"vptr": hx(pointer), "proven": False, "type_identity": "UNKNOWN"}
    if not img.mapped(pointer - 16, 24):
        result["classification"] = "VPTR_HEADER_UNMAPPED"
        return result

    offset_to_top_raw = img.qword(pointer - 16)
    typeinfo = img.qword(pointer - 8)
    result["offset_to_top_raw"] = hx(offset_to_top_raw)
    result["typeinfo"] = hx(typeinfo)
    if offset_to_top_raw is None or typeinfo is None or not img.mapped(typeinfo, 16):
        result["classification"] = "VPTR_HEADER_INCOMPLETE"
        return result
    offset_to_top = struct.unpack("<q", struct.pack("<Q", offset_to_top_raw))[0]
    result["offset_to_top"] = offset_to_top
    if offset_to_top != 0:
        result["classification"] = "NON_PRIMARY_VPTR"
        return result

    pointer_symbols = img.symbol_names(pointer) + img.symbol_names(pointer - 16)
    typeinfo_symbols = img.symbol_names(typeinfo)
    result["vptr_symbols"] = pointer_symbols
    result["typeinfo_symbols"] = typeinfo_symbols

    names: list[tuple[str, str]] = []
    for symbol in pointer_symbols + typeinfo_symbols:
        d = normalize_type_name(demangle(symbol))
        if d and d != symbol:
            names.append(("symbol", d))

    name_ptr = img.qword(typeinfo + 8)
    result["typeinfo_name_ptr"] = hx(name_ptr)
    raw_name = img.cstring(name_ptr) if name_ptr is not None else None
    result["typeinfo_raw_name"] = raw_name
    if raw_name:
        d = normalize_type_name(demangle("_ZTS" + raw_name))
        if d and d != "_ZTS" + raw_name:
            names.append(("rtti_name", d))

    unique_names = sorted({name for _, name in names})
    result["candidate_type_names"] = unique_names
    if len(unique_names) == 1:
        result.update({
            "classification": "PRIMARY_VPTR_RTTI_TYPE_PROVEN",
            "proven": True,
            "type_identity": unique_names[0],
            "evidence_sources": sorted({source for source, name in names if name == unique_names[0]}),
        })
    else:
        result["classification"] = "VPTR_TYPE_NAME_NOT_UNIQUE"
    return result


def resolve_receiver_type(img: Image) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "receiver_provenance": RECEIVER_PROVENANCE,
        "receiver_identity": "UNKNOWN",
        "connection_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
    }
    fde = img.containing_fde(CONNECTIMPL_CALLSITE)
    if fde != CONNECTIMPL_FDE:
        result["classification"] = "CONNECTIMPL_FDE_MISMATCH"
        result["actual_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    call = instruction_at(insns, CONNECTIMPL_CALLSITE)
    if call is None or call.mnemonic != "call" or direct_target(call) != CONNECTIMPL_TARGET:
        result["classification"] = "CONNECTIMPL_CALLSITE_TARGET_MISMATCH"
        result["actual_target"] = hx(direct_target(call)) if call else None
        return result
    connect_identity = target_identity(img, CONNECTIMPL_TARGET)
    result["connectimpl_target"] = connect_identity
    if "QObject::connectImpl(" not in str(connect_identity.get("demangled") or ""):
        result["classification"] = "CONNECTIMPL_SYMBOL_IDENTITY_MISMATCH"
        return result

    trace = trace_entry_receiver(img, insns)
    result["entry_receiver_trace"] = trace
    if not trace.get("receiver_identity_preserved"):
        result["classification"] = "ENTRY_RDI_RECEIVER_PROVENANCE_NOT_REPROVEN"
        return result

    root_stores = [row for row in trace["object_pointer_stores"] if row.get("object_offset") == "0x0"]
    result["entry_object_root_pointer_stores"] = root_stores
    if not root_stores:
        result["classification"] = "ENTRY_RDI_ROOT_VPTR_STORE_NOT_FOUND_IN_BOUNDED_FDE"
        return result

    decoded: list[dict[str, Any]] = []
    for row in root_stores:
        pointer = int(str(row["pointer"]), 16)
        item = {**row, "vptr_decode": decode_vptr(img, pointer)}
        decoded.append(item)
    result["entry_object_root_pointer_decodes"] = decoded

    last = decoded[-1]
    active = last["vptr_decode"]
    result["active_root_pointer_store"] = last
    if not active.get("proven"):
        result["classification"] = "ACTIVE_ENTRY_RDI_VPTR_TYPE_NOT_PROVEN"
        return result

    receiver_identity = str(active["type_identity"])
    signal_owner_cross_check = receiver_identity == QUEUE_SIGNAL_OWNER
    result["signal_owner_cross_check"] = {
        "queue_signal_owner": QUEUE_SIGNAL_OWNER,
        "qslot_function_target": hx(QSLOT_FUNCTION_TARGET),
        "receiver_matches_signal_owner": signal_owner_cross_check,
    }
    result.update({
        "classification": "ENTRY_RDI_ACTIVE_VPTR_TYPE_PROVEN",
        "proven": True,
        "receiver_identity": receiver_identity,
        "receiver_matches_signal_owner": signal_owner_cross_check,
    })
    return result


def classify_connection_role(receiver: dict[str, Any]) -> dict[str, Any]:
    identity = receiver.get("receiver_identity", "UNKNOWN")
    if not receiver.get("proven"):
        return {"role": "UNKNOWN", "proven": False, "classification": "RECEIVER_TYPE_NOT_PROVEN"}
    if identity == QUEUE_SIGNAL_OWNER:
        return {
            "role": "SIGNAL_RELAY",
            "proven": True,
            "classification": "SAME_SIGNAL_OWNER_RECEIVER_AND_QSLOT_SIGNAL_BODY",
            "receiver_identity": identity,
            "signal_owner": QUEUE_SIGNAL_OWNER,
            "qslot_function_target": hx(QSLOT_FUNCTION_TARGET),
            "signal_name": QUEUE_SIGNAL_NAME,
        }
    return {
        "role": "UNKNOWN",
        "proven": False,
        "classification": "RECEIVER_TYPE_PROVEN_BUT_QSLOT_SIGNAL_COMPATIBILITY_NOT_PROVEN",
        "receiver_identity": identity,
        "signal_owner": QUEUE_SIGNAL_OWNER,
    }


def trace_one_relay_edge(receiver: dict[str, Any], role: dict[str, Any]) -> dict[str, Any]:
    if not receiver.get("proven") or role.get("role") != "SIGNAL_RELAY":
        return {
            "proven": False,
            "edge": "UNKNOWN",
            "endpoint_identity": "UNKNOWN",
            "classification": "RELAY_ROLE_NOT_PROVEN",
        }
    return {
        "proven": False,
        "edge": "UNKNOWN",
        "endpoint_identity": "UNKNOWN",
        "classification": "NEXT_RELAY_EDGE_OUTSIDE_BOUNDED_RECEIVER_TYPE_PROOF",
        "identity_preserved": "exact GameclientMessage shared pair",
    }


def analyze(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    actual_size = len(raw)
    actual_sha = hashlib.sha256(raw).hexdigest()
    exact = actual_size == EXPECTED_SIZE and actual_sha == EXPECTED_SHA256
    base: dict[str, Any] = {
        "schema": "otclient.track-a.be4f48-queue-signal-bf-relay-receiver-type.source-result.v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": actual_size,
            "sha256": actual_sha,
            "proven": exact,
        },
        "queue_signal_name": QUEUE_SIGNAL_NAME,
        "queue_signal_index": QUEUE_SIGNAL_INDEX,
        "queue_signal_index_hex": hx(QUEUE_SIGNAL_INDEX),
        "queue_signal_argv1_identity": "exact GameclientMessage shared pair",
        "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
        "connectimpl_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "receiver_provenance": RECEIVER_PROVENANCE,
        "qslot_function_target": hx(QSLOT_FUNCTION_TARGET),
        "runtime_access": "none",
        "official_client_executed": False,
        "login_performed": False,
        "credentials_used": False,
        "process_memory_access": False,
        "packet_capture": False,
        "ocr_vision_used": False,
        "official_service_e2e_count": 0,
        "track_b_pr_284_modified": False,
        "final_queue_writer_identified": False,
        "final_tcp_writer_identified": False,
        "final_writer_contract": "UNKNOWN",
        "field6_value": "UNKNOWN",
    }
    if not exact:
        base.update({
            "queue_signal_receiver_identity": "UNKNOWN",
            "queue_signal_receiver_identity_proven": False,
            "queue_signal_connection_role": "UNKNOWN",
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": "EXACT_CLIENT_FENCE_MISMATCH",
            "next_action": "refresh exact current fence before any further source analysis",
        })
        return base

    img = Image(path)
    try:
        receiver = resolve_receiver_type(img)
        role = classify_connection_role(receiver)
        next_edge = trace_one_relay_edge(receiver, role)
    finally:
        img.close()

    base["receiver_type_evidence"] = receiver
    base["connection_role_evidence"] = role
    base["next_relay_edge_evidence"] = next_edge
    base["queue_signal_receiver_identity"] = receiver.get("receiver_identity", "UNKNOWN")
    base["queue_signal_receiver_identity_proven"] = bool(receiver.get("proven"))
    base["queue_signal_connection_role"] = role.get("role", "UNKNOWN")
    base["next_unique_relay_edge"] = next_edge.get("edge", "UNKNOWN")
    base["next_endpoint_identity"] = next_edge.get("endpoint_identity", "UNKNOWN")

    if receiver.get("proven") and role.get("proven"):
        base["terminal_result"] = "QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN"
        base["FIRST_MISSING_BOUNDARY"] = "NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF"
        base["next_action"] = "clean coordinator promotion before any Track B decision"
    else:
        base["terminal_result"] = "SOURCE_BLOCKER"
        base["FIRST_MISSING_BOUNDARY"] = str(receiver.get("classification") if not receiver.get("proven") else role.get("classification"))
        base["next_action"] = "clean coordinator promotion; any further work requires one newly admitted bounded receiver-provenance step"
    return base


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = analyze(args.client)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
