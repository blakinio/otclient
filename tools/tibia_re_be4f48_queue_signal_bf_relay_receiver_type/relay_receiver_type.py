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
PROMOTED_RECEIVER_PROVENANCE = True
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
            Section(int(sec["sh_offset"]), int(sec["sh_size"]), int(sec["sh_addr"]))
            for sec in self.elf.iter_sections()
            if int(sec["sh_size"]) > 0
        ]
        self.symbols: dict[int, list[str]] = {}
        self.relocations: dict[int, dict[str, Any]] = {}
        for sec in self.elf.iter_sections():
            if isinstance(sec, SymbolTableSection):
                for sym in sec.iter_symbols():
                    value = int(sym["st_value"])
                    if value and sym.name:
                        self.symbols.setdefault(value, []).append(sym.name)
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                symbol_name = None
                symbol_value = 0
                sym_index = int(rel["r_info_sym"])
                if symtab is not None and sym_index:
                    try:
                        sym = symtab.get_symbol(sym_index)
                        symbol_name = sym.name or None
                        symbol_value = int(sym["st_value"])
                    except Exception:
                        pass
                self.relocations[int(rel["r_offset"])] = {
                    "addend": int(rel.entry.get("r_addend", 0)),
                    "symbol": symbol_name,
                    "symbol_value": symbol_value,
                }
        dwarf = self.elf.get_dwarf_info()
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
        if rel:
            addend = int(rel.get("addend") or 0)
            symbol_value = int(rel.get("symbol_value") or 0)
            if symbol_value:
                return (symbol_value + addend) & 0xFFFFFFFFFFFFFFFF
            if addend:
                return addend & 0xFFFFFFFFFFFFFFFF
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
            b = self.read(va + offset, 1)[0]
            if b == 0:
                break
            out.append(b)
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
        for ins in self.disassemble(target, target + 24)[:4]:
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
        p = subprocess.run(
            ["c++filt", symbol],
            check=True,
            text=True,
            capture_output=True,
            timeout=2,
        )
        return p.stdout.strip() or symbol
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
    op = ins.operands[0]
    return int(op.imm) if op.type == X86_OP_IMM else None


def rip_target(ins: Any) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return int(ins.address) + int(ins.size) + int(op.mem.disp)
    return None


def target_identity(img: Image, target: int | None) -> dict[str, Any]:
    if target is None:
        return {"target": None, "symbol": None, "demangled": None}
    names = img.symbol_names(target)
    symbol = img.plt_symbol(target) or (names[0] if len(names) == 1 else None)
    return {
        "target": hx(target),
        "symbol": symbol,
        "demangled": demangle(symbol),
        "direct_symbols": names,
    }


def written_registers(img: Image, ins: Any) -> set[str]:
    try:
        _, written = ins.regs_access()
        return {canonical_reg(img, reg) for reg in written}
    except Exception:
        return set()


def trace_entry_object(img: Image, insns: list[Any]) -> dict[str, Any]:
    regs: dict[str, Value] = {"rdi": ENTRY_RDI}
    stores: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []

    for ins in insns:
        address = int(ins.address)
        if address > CONNECTIMPL_CALLSITE:
            break

        if ins.mnemonic == "call":
            target = direct_target(ins)
            calls.append({"site": hx(address), **target_identity(img, target)})
            if address == CONNECTIMPL_CALLSITE:
                break
            for reg in CALLER_SAVED:
                regs[reg] = UNKNOWN
            continue

        if ins.mnemonic.startswith("mov") and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_MEM and src.type == X86_OP_REG and int(dst.mem.index) == 0:
                base = canonical_reg(img, dst.mem.base) if dst.mem.base else ""
                base_value = regs.get(base, UNKNOWN)
                src_value = regs.get(canonical_reg(img, src.reg), UNKNOWN)
                if base_value.kind == "entry_rdi" and src_value.kind == "ptr":
                    stores.append({
                        "site": hx(address),
                        "object_offset": hx(base_value.value + int(dst.mem.disp)),
                        "pointer": hx(src_value.value),
                        "base_register": base,
                        "source_register": canonical_reg(img, src.reg),
                    })
            if dst.type == X86_OP_REG:
                dst_reg = canonical_reg(img, dst.reg)
                if src.type == X86_OP_REG:
                    regs[dst_reg] = regs.get(canonical_reg(img, src.reg), UNKNOWN)
                elif src.type == X86_OP_IMM:
                    value = int(src.imm) & 0xFFFFFFFFFFFFFFFF
                    regs[dst_reg] = Value("ptr", value) if img.mapped(value) else UNKNOWN
                elif src.type == X86_OP_MEM and src.mem.base == X86_REG_RIP:
                    where = int(ins.address) + int(ins.size) + int(src.mem.disp)
                    value = img.qword(where)
                    regs[dst_reg] = Value("ptr", value) if value is not None and img.mapped(value) else UNKNOWN
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
                regs[dst_reg] = Value("ptr", int(ins.address) + int(ins.size) + int(src.mem.disp))
                continue
            base = canonical_reg(img, src.mem.base) if src.mem.base else ""
            base_value = regs.get(base, UNKNOWN)
            if int(src.mem.index) == 0 and base_value.kind == "entry_rdi":
                regs[dst_reg] = Value("entry_rdi", base_value.value + int(src.mem.disp))
            else:
                regs[dst_reg] = UNKNOWN
            continue

        for reg in written_registers(img, ins):
            if reg not in ("rsp", "rip"):
                regs[reg] = UNKNOWN

    constructor_calls = [
        row for row in calls
        if "QObject::QObject(" in str(row.get("demangled") or "")
    ]
    return {
        "promoted_receiver_provenance_consumed": PROMOTED_RECEIVER_PROVENANCE,
        "receiver_provenance": RECEIVER_PROVENANCE,
        "bounded_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
        "object_pointer_stores": stores,
        "qobject_constructor_calls": constructor_calls,
        "bounded_direct_calls": calls,
    }


def normalize_type_name(value: str | None) -> str | None:
    if not value:
        return None
    for prefix in ("vtable for ", "typeinfo for ", "typeinfo name for "):
        if value.startswith(prefix):
            return value[len(prefix) :]
    return value


def decode_vptr(img: Image, pointer: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "vptr": hx(pointer),
        "proven": False,
        "type_identity": "UNKNOWN",
    }
    if not img.mapped(pointer - 16, 24):
        result["classification"] = "VPTR_HEADER_UNMAPPED"
        return result

    offset_raw = img.qword(pointer - 16)
    typeinfo = img.qword(pointer - 8)
    result["offset_to_top_raw"] = hx(offset_raw)
    result["typeinfo"] = hx(typeinfo)
    if offset_raw is None or typeinfo is None or not img.mapped(typeinfo, 16):
        result["classification"] = "VPTR_HEADER_INCOMPLETE"
        return result

    offset_to_top = struct.unpack("<q", struct.pack("<Q", offset_raw))[0]
    result["offset_to_top"] = offset_to_top
    if offset_to_top != 0:
        result["classification"] = "NON_PRIMARY_VPTR"
        return result

    candidates: list[tuple[str, str]] = []
    vptr_symbols = img.symbol_names(pointer) + img.symbol_names(pointer - 16)
    typeinfo_symbols = img.symbol_names(typeinfo)
    result["vptr_symbols"] = sorted(set(vptr_symbols))
    result["typeinfo_symbols"] = typeinfo_symbols
    for symbol in vptr_symbols + typeinfo_symbols:
        d = normalize_type_name(demangle(symbol))
        if d and d != symbol:
            candidates.append(("symbol", d))

    name_ptr = img.qword(typeinfo + 8)
    raw_name = img.cstring(name_ptr) if name_ptr is not None else None
    result["typeinfo_name_ptr"] = hx(name_ptr)
    result["typeinfo_raw_name"] = raw_name
    if raw_name:
        d = normalize_type_name(demangle("_ZTS" + raw_name))
        if d and d != "_ZTS" + raw_name:
            candidates.append(("rtti_name", d))

    unique = sorted({name for _, name in candidates})
    result["candidate_type_names"] = unique
    if len(unique) != 1:
        result["classification"] = "VPTR_TYPE_NAME_NOT_UNIQUE"
        return result

    result.update({
        "classification": "PRIMARY_VPTR_RTTI_TYPE_PROVEN",
        "proven": True,
        "type_identity": unique[0],
        "evidence_sources": sorted({src for src, name in candidates if name == unique[0]}),
    })
    return result


def resolve_receiver_type(img: Image) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proven": False,
        "receiver_provenance": RECEIVER_PROVENANCE,
        "promoted_receiver_provenance_consumed": PROMOTED_RECEIVER_PROVENANCE,
        "receiver_identity": "UNKNOWN",
        "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
        "connection_fde": [hx(CONNECTIMPL_FDE[0]), hx(CONNECTIMPL_FDE[1])],
    }

    if not PROMOTED_RECEIVER_PROVENANCE:
        result["classification"] = "PROMOTED_RECEIVER_PROVENANCE_NOT_AVAILABLE"
        return result

    fde = img.containing_fde(CONNECTIMPL_CALLSITE)
    if fde != CONNECTIMPL_FDE:
        result["classification"] = "CONNECTIMPL_FDE_MISMATCH"
        result["actual_fde"] = [hx(fde[0]), hx(fde[1])] if fde else None
        return result

    insns = img.disassemble(*CONNECTIMPL_FDE)
    connect_rows = [ins for ins in insns if int(ins.address) == CONNECTIMPL_CALLSITE]
    if len(connect_rows) != 1:
        result["classification"] = "CONNECTIMPL_CALLSITE_NOT_UNIQUE_IN_FDE"
        return result
    connect = connect_rows[0]
    actual_target = direct_target(connect)
    if connect.mnemonic != "call" or actual_target != CONNECTIMPL_TARGET:
        result["classification"] = "CONNECTIMPL_CALLSITE_TARGET_MISMATCH"
        result["actual_target"] = hx(actual_target)
        return result

    connect_identity = target_identity(img, CONNECTIMPL_TARGET)
    result["connectimpl_target"] = connect_identity
    if "QObject::connectImpl(" not in str(connect_identity.get("demangled") or ""):
        result["classification"] = "CONNECTIMPL_SYMBOL_IDENTITY_MISMATCH"
        return result

    trace = trace_entry_object(img, insns)
    result["entry_object_trace"] = trace
    if not trace["qobject_constructor_calls"]:
        result["classification"] = "ENTRY_RDI_QOBJECT_CONSTRUCTOR_PROVENANCE_NOT_FOUND"
        return result

    root_stores = [row for row in trace["object_pointer_stores"] if row["object_offset"] == "0x0"]
    result["entry_object_root_pointer_stores"] = root_stores
    if not root_stores:
        result["classification"] = "ENTRY_RDI_ROOT_VPTR_STORE_NOT_FOUND_IN_BOUNDED_FDE"
        return result

    decoded = [
        {**row, "vptr_decode": decode_vptr(img, int(str(row["pointer"]), 16))}
        for row in root_stores
    ]
    result["entry_object_root_pointer_decodes"] = decoded
    active_store = decoded[-1]
    result["active_root_pointer_store"] = active_store
    active = active_store["vptr_decode"]
    if not active.get("proven"):
        result["classification"] = "ACTIVE_ENTRY_RDI_VPTR_TYPE_NOT_PROVEN"
        return result

    identity = str(active["type_identity"])
    result.update({
        "classification": "ENTRY_RDI_ACTIVE_VPTR_TYPE_PROVEN",
        "proven": True,
        "receiver_identity": identity,
        "receiver_matches_signal_owner": identity == QUEUE_SIGNAL_OWNER,
        "signal_owner_cross_check": {
            "queue_signal_owner": QUEUE_SIGNAL_OWNER,
            "qslot_function_target": hx(QSLOT_FUNCTION_TARGET),
            "receiver_matches_signal_owner": identity == QUEUE_SIGNAL_OWNER,
        },
    })
    return result


def classify_connection_role(receiver: dict[str, Any]) -> dict[str, Any]:
    identity = str(receiver.get("receiver_identity", "UNKNOWN"))
    if not receiver.get("proven"):
        return {
            "role": "UNKNOWN",
            "proven": False,
            "classification": "RECEIVER_TYPE_NOT_PROVEN",
        }
    if identity == QUEUE_SIGNAL_OWNER:
        return {
            "role": "SIGNAL_RELAY",
            "proven": True,
            "classification": "SAME_SIGNAL_OWNER_RECEIVER_AND_PROMOTED_QSLOT_SIGNAL_BODY",
            "receiver_identity": identity,
            "signal_owner": QUEUE_SIGNAL_OWNER,
            "signal_name": QUEUE_SIGNAL_NAME,
            "qslot_function_target": hx(QSLOT_FUNCTION_TARGET),
        }
    return {
        "role": "OTHER",
        "proven": True,
        "classification": "PROVEN_RECEIVER_IS_NOT_QUEUE_SIGNAL_OWNER",
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
        "classification": "NEXT_RELAY_EDGE_NOT_FOLLOWED_WITHOUT_A_NEW_UNIQUE_IDENTITY_PRESERVING_EDGE",
        "identity_preserved": "exact GameclientMessage shared pair",
    }


def analyze(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    actual_size = len(raw)
    actual_sha = hashlib.sha256(raw).hexdigest()
    exact = actual_size == EXPECTED_SIZE and actual_sha == EXPECTED_SHA256

    result: dict[str, Any] = {
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
        "promoted_receiver_provenance_consumed": PROMOTED_RECEIVER_PROVENANCE,
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
        result.update({
            "queue_signal_receiver_identity": "UNKNOWN",
            "queue_signal_receiver_identity_proven": False,
            "queue_signal_connection_role": "UNKNOWN",
            "next_unique_relay_edge": "UNKNOWN",
            "next_endpoint_identity": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": "EXACT_CLIENT_FENCE_MISMATCH",
            "next_action": "refresh exact current fence before further source analysis",
        })
        return result

    img = Image(path)
    try:
        receiver = resolve_receiver_type(img)
        role = classify_connection_role(receiver)
        next_edge = trace_one_relay_edge(receiver, role)
    finally:
        img.close()

    result["receiver_type_evidence"] = receiver
    result["connection_role_evidence"] = role
    result["next_relay_edge_evidence"] = next_edge
    result["queue_signal_receiver_identity"] = receiver.get("receiver_identity", "UNKNOWN")
    result["queue_signal_receiver_identity_proven"] = bool(receiver.get("proven"))
    result["queue_signal_connection_role"] = role.get("role", "UNKNOWN")
    result["next_unique_relay_edge"] = next_edge.get("edge", "UNKNOWN")
    result["next_endpoint_identity"] = next_edge.get("endpoint_identity", "UNKNOWN")

    if receiver.get("proven") and role.get("proven"):
        result["terminal_result"] = "QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_PROVEN"
        result["FIRST_MISSING_BOUNDARY"] = "NEXT_RELAY_EDGE_NOT_UNIQUELY_PROVEN_WITHIN_BOUNDED_RECEIVER_TYPE_PROOF"
        result["next_action"] = "clean coordinator promotion before any Track B decision"
    else:
        result["terminal_result"] = "SOURCE_BLOCKER"
        result["FIRST_MISSING_BOUNDARY"] = str(
            receiver.get("classification") if not receiver.get("proven") else role.get("classification")
        )
        result["next_action"] = "clean coordinator promotion; any further research requires one newly admitted bounded source step"
    return result


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
