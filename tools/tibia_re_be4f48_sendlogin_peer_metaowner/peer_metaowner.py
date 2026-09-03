#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

METAOBJECT_ANCHOR = 0x30B68A0
SIGNAL_INDEX = 0
PEER_TARGET = 0xD052A0
ADAPTER_TARGET = 0xBD3050
ADAPTER_REFERENCE_SITE = 0x7C6B34
CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)

MAX_LOCAL_WINDOW_INSTRUCTIONS = 160
MAX_STRING_BYTES = 512


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def printable_identifier(value: str) -> bool:
    return bool(value) and len(value) <= 256 and all(ch.isprintable() and ch not in "\r\n\t" for ch in value)


class Image:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections: list[tuple[int, int, int, str]] = []
        for section in self.elf.iter_sections():
            start = int(section["sh_addr"])
            size = int(section["sh_size"])
            offset = int(section["sh_offset"])
            if start and size:
                self.sections.append((start, start + size, offset, section.name))
        self.relocations: dict[int, dict[str, Any]] = {}
        for section in self.elf.iter_sections():
            if not isinstance(section, RelocationSection):
                continue
            symtab = self.elf.get_section(section["sh_link"]) if section["sh_link"] else None
            for reloc in section.iter_relocations():
                symbol = None
                sym_index = int(reloc["r_info_sym"])
                if symtab is not None and sym_index:
                    try:
                        symbol = symtab.get_symbol(sym_index).name or None
                    except Exception:
                        symbol = None
                self.relocations[int(reloc["r_offset"])] = {
                    "addend": int(reloc.entry.get("r_addend", 0)),
                    "symbol": symbol,
                    "type": int(reloc["r_info_type"]),
                }
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def close(self) -> None:
        self.handle.close()

    def location(self, address: int, size: int = 1) -> tuple[int, str] | None:
        for start, end, offset, name in self.sections:
            if start <= address and address + size <= end:
                return offset + address - start, name
        return None

    def mapped(self, address: int, size: int = 1) -> bool:
        return self.location(address, size) is not None

    def read(self, address: int, size: int) -> bytes:
        loc = self.location(address, size)
        if loc is None:
            raise ValueError(f"unmapped range {hx(address)}+{size}")
        offset, _ = loc
        return self.raw[offset : offset + size]

    def u32(self, address: int) -> int:
        return struct.unpack("<I", self.read(address, 4))[0]

    def u64(self, address: int) -> int:
        return struct.unpack("<Q", self.read(address, 8))[0]

    def ptr(self, address: int) -> dict[str, Any]:
        raw = self.u64(address)
        reloc = self.relocations.get(address)
        resolved = raw
        source = "raw_qword"
        if reloc is not None and reloc.get("addend"):
            resolved = int(reloc["addend"])
            source = "rela_addend"
        return {
            "slot": hx(address),
            "raw": hx(raw),
            "resolved": hx(resolved),
            "source": source,
            "relocation_symbol": reloc.get("symbol") if reloc else None,
            "relocation_type": reloc.get("type") if reloc else None,
        }

    def disassemble(self, start: int, end: int) -> list[Any]:
        return list(self.md.disasm(self.read(start, end - start), start))

    def section_name(self, address: int) -> str | None:
        loc = self.location(address)
        return loc[1] if loc else None

    def read_text(self, address: int, length: int) -> str | None:
        if length < 0 or length > MAX_STRING_BYTES or not self.mapped(address, length):
            return None
        try:
            value = self.read(address, length).decode("utf-8")
        except UnicodeDecodeError:
            return None
        return value if printable_identifier(value) else None

    def plt_symbol(self, target: int) -> str | None:
        if not self.mapped(target, 6):
            return None
        end = target + min(32, max(6, self.location(target)[0] if False else 32))
        try:
            instructions = self.disassemble(target, end)
        except Exception:
            return None
        for ins in instructions[:4]:
            if ins.mnemonic not in ("jmp", "bnd") or not ins.operands:
                continue
            op = ins.operands[-1]
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                got = ins.address + ins.size + int(op.mem.disp)
                reloc = self.relocations.get(got)
                if reloc and reloc.get("symbol"):
                    return str(reloc["symbol"])
        return None


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        result = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
        return result.stdout.strip() or symbol
    except Exception:
        return symbol


def rip_target(img: Image, ins: Any) -> int | None:
    for operand in ins.operands:
        if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP:
            return ins.address + ins.size + int(operand.mem.disp)
    return None


def direct_target(ins: Any) -> int | None:
    if ins.mnemonic not in ("call", "jmp") or not ins.operands:
        return None
    op = ins.operands[0]
    return int(op.imm) if op.type == X86_OP_IMM else None


def canonical_reg(img: Image, reg_id: int) -> str:
    name = img.md.reg_name(reg_id)
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


def classify_static(address: int) -> str:
    if address == PEER_TARGET:
        return "PEER_FUNCTION"
    if address == ADAPTER_TARGET:
        return "ADAPTER_FUNCTION"
    if address == METAOBJECT_ANCHOR:
        return "METAOBJECT_ANCHOR"
    return f"STATIC_ADDRESS:{hx(address)}"


def fmt_disp(value: int) -> str:
    return f"+0x{value:x}" if value >= 0 else f"-0x{-value:x}"


def same_stack_slot(ins: Any, displacement: int) -> bool:
    if not ins.operands:
        return False
    dst = ins.operands[0]
    return dst.type == X86_OP_MEM and dst.mem.base == X86_REG_RSP and int(dst.mem.disp) == displacement


def resolve_reg(img: Image, window: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
    if depth > 8:
        return {"classification": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    caller_saved = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
    for idx in range(before - 1, -1, -1):
        ins = window[idx]
        if ins.mnemonic == "call" and wanted in caller_saved:
            return {"classification": "UNKNOWN", "reason": "CALL_CLOBBER_BOUNDARY", "boundary_site": hx(ins.address)}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        out: dict[str, Any] = {"definition_site": hx(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            if src.mem.base == X86_REG_RIP:
                target = ins.address + ins.size + int(src.mem.disp)
                out.update({"classification": classify_static(target), "target": hx(target)})
                return out
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            disp = int(src.mem.disp)
            if base == "rsp":
                out.update({"classification": "STACK_ADDRESS", "stack_displacement": fmt_disp(disp), "stack_displacement_value": disp})
            else:
                base_value = resolve_reg(img, window, idx, base, depth + 1) if base != "none" else None
                out.update({"classification": "OBJECT_ADDRESS", "base_register": base, "displacement": fmt_disp(disp), "base": base_value})
            return out
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_IMM:
                out.update({"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)})
                return out
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                resolved = resolve_reg(img, window, idx, via, depth + 1)
                out.update({"classification": resolved.get("classification", "UNKNOWN"), "via_register": via, "source": resolved})
                return out
            if src.type == X86_OP_MEM:
                if src.mem.base == X86_REG_RIP:
                    target = ins.address + ins.size + int(src.mem.disp)
                    out.update({"classification": "STATIC_POINTER_LOAD", "address": hx(target), "relocation": img.relocations.get(target)})
                    return out
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                disp = int(src.mem.disp)
                if base == "rsp":
                    for store_idx in range(idx - 1, -1, -1):
                        store = window[store_idx]
                        if not same_stack_slot(store, disp) or len(store.operands) < 2:
                            continue
                        val = store.operands[1]
                        if val.type == X86_OP_REG:
                            resolved = resolve_reg(img, window, store_idx, canonical_reg(img, val.reg), depth + 1)
                            out.update({"classification": resolved.get("classification", "UNKNOWN"), "stack_displacement": fmt_disp(disp), "source": resolved})
                            return out
                        if val.type == X86_OP_IMM:
                            out.update({"classification": "CONSTANT", "stack_displacement": fmt_disp(disp), "value": hx(int(val.imm) & 0xFFFFFFFFFFFFFFFF)})
                            return out
                    out.update({"classification": "STACK_LOAD", "stack_displacement": fmt_disp(disp)})
                    return out
                base_value = resolve_reg(img, window, idx, base, depth + 1) if base != "none" else None
                out.update({"classification": "OBJECT_FIELD", "base_register": base, "displacement": fmt_disp(disp), "base": base_value})
                return out
        if ins.mnemonic == "xor" and src is not None and src.type == X86_OP_REG and canonical_reg(img, src.reg) == wanted:
            out.update({"classification": "CONSTANT", "value": "0x0"})
            return out
        out.update({"classification": "UNKNOWN", "reason": "UNSUPPORTED_DEFINITION"})
        return out
    return {"classification": f"ENTRY_ARG:{wanted}", "reason": "NO_LOCAL_DEFINITION"}


def decode_qt_string(img: Image, base: int, index: int) -> dict[str, Any]:
    if index < 0 or index > 4096 or not img.mapped(base + index * 8, 8):
        return {"index": index, "classification": "INVALID_STRING_INDEX"}
    offset = img.u32(base + index * 8)
    length = img.u32(base + index * 8 + 4)
    value = img.read_text(base + offset, length) if offset <= 0x100000 else None
    return {
        "index": index,
        "offset": offset,
        "length": length,
        "address": hx(base + offset) if offset <= 0x100000 else None,
        "value": value,
        "classification": "QT6_OFFSET_LENGTH_STRING" if value is not None else "UNRESOLVED_STRING",
    }


def decode_metaobject(img: Image) -> dict[str, Any]:
    field_names = ("superdata", "stringdata", "metadata", "static_metacall", "related_metaobjects", "metatypes", "extradata")
    fields = {name: img.ptr(METAOBJECT_ANCHOR + i * 8) for i, name in enumerate(field_names)}
    stringdata = int(fields["stringdata"]["resolved"], 16)
    metadata = int(fields["metadata"]["resolved"], 16)
    result: dict[str, Any] = {
        "anchor": hx(METAOBJECT_ANCHOR),
        "anchor_section": img.section_name(METAOBJECT_ANCHOR),
        "fields": fields,
        "layout": "QT_QMETAOBJECT_D_POINTER_FIELDS",
        "owner_identity": "UNKNOWN",
        "owner_proven": False,
        "signal_index": SIGNAL_INDEX,
        "signal_binding": "UNKNOWN",
    }
    if not img.mapped(metadata, 56) or not img.mapped(stringdata, 8):
        result["classification"] = "UNMAPPED_STRINGDATA_OR_METADATA"
        return result
    header = [img.u32(metadata + i * 4) for i in range(14)]
    names = (
        "revision", "class_name_index", "classinfo_count", "classinfo_data", "method_count", "method_data",
        "property_count", "property_data", "enum_count", "enum_data", "constructor_count", "constructor_data", "flags", "signal_count",
    )
    decoded = dict(zip(names, header))
    result["metadata_header"] = decoded
    header_valid = (
        5 <= decoded["revision"] <= 20
        and decoded["class_name_index"] <= 4096
        and decoded["method_count"] <= 4096
        and decoded["signal_count"] <= decoded["method_count"]
        and decoded["method_data"] <= 1_000_000
    )
    result["metadata_header_valid"] = header_valid
    class_string = decode_qt_string(img, stringdata, decoded["class_name_index"])
    result["class_name_string"] = class_string
    if header_valid and class_string.get("value"):
        result["owner_identity"] = class_string["value"]
        result["owner_proven"] = True
    if header_valid and decoded["signal_count"] > SIGNAL_INDEX and decoded["method_count"] > SIGNAL_INDEX:
        method_address = metadata + decoded["method_data"] * 4
        if img.mapped(method_address, 24):
            raw = [img.u32(method_address + i * 4) for i in range(6)]
            method_name = decode_qt_string(img, stringdata, raw[0])
            result["signal_method_raw_u32"] = raw
            result["signal_name_string"] = method_name
            result["signal_binding"] = "METAOBJECT_METHOD_INDEX_0"
    result["classification"] = "METAOBJECT_OWNER_PROVEN" if result["owner_proven"] else "METAOBJECT_OWNER_UNKNOWN"
    return result


def stack_payloads(img: Image, window: list[Any], before: int) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for idx, ins in enumerate(window[:before]):
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or dst.mem.base != X86_REG_RSP:
            continue
        row: dict[str, Any] = {"site": hx(ins.address), "stack_displacement": fmt_disp(int(dst.mem.disp)), "stack_displacement_value": int(dst.mem.disp), "op_str": ins.op_str}
        if src.type == X86_OP_REG:
            row["source"] = resolve_reg(img, window, idx, canonical_reg(img, src.reg))
        elif src.type == X86_OP_IMM:
            row["source"] = {"classification": "CONSTANT", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF)}
        else:
            row["source"] = {"classification": "UNRESOLVED_STORE_SOURCE"}
        payloads.append(row)
    return payloads


def contains_classification(value: Any, wanted: str) -> bool:
    if isinstance(value, dict):
        if value.get("classification") == wanted:
            return True
        return any(contains_classification(v, wanted) for v in value.values())
    if isinstance(value, list):
        return any(contains_classification(v, wanted) for v in value)
    return False


def analyze_connection(img: Image, owner: str) -> dict[str, Any]:
    instructions = img.disassemble(*CONNECTION_OWNER_FDE)
    anchor_indexes = [i for i, ins in enumerate(instructions) if ins.address == ADAPTER_REFERENCE_SITE and rip_target(img, ins) == ADAPTER_TARGET]
    result: dict[str, Any] = {
        "owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        "adapter_reference_site": hx(ADAPTER_REFERENCE_SITE),
        "adapter_reference_exact_count": len(anchor_indexes),
        "actual_qt_connection_primitive": "UNKNOWN",
        "actual_qt_connection_callsite": None,
        "sender_endpoint_identity": "UNKNOWN",
        "receiver_endpoint_identity": "UNKNOWN",
        "peer_signal_bound_to_connection": False,
        "sendlogin_adapter_bound_to_connection": False,
        "sendlogin_causal_binding_proven": False,
    }
    if len(anchor_indexes) != 1:
        result["classification"] = "ADAPTER_REFERENCE_NOT_EXACT"
        return result
    center = anchor_indexes[0]
    start = max(0, center - MAX_LOCAL_WINDOW_INSTRUCTIONS)
    end = min(len(instructions), center + MAX_LOCAL_WINDOW_INSTRUCTIONS + 1)
    window = instructions[start:end]
    local_center = center - start
    refs: list[dict[str, Any]] = []
    for ins in window:
        target = rip_target(img, ins)
        if target in (PEER_TARGET, ADAPTER_TARGET, METAOBJECT_ANCHOR):
            refs.append({"site": hx(ins.address), "target": hx(target), "classification": classify_static(target), "mnemonic": ins.mnemonic, "op_str": ins.op_str})
    result["bounded_reference_sites"] = refs
    calls: list[dict[str, Any]] = []
    candidates: list[tuple[int, dict[str, Any]]] = []
    for idx, ins in enumerate(window):
        if ins.mnemonic != "call":
            continue
        target = direct_target(ins)
        if target is None:
            calls.append({"site": hx(ins.address), "target": None, "classification": "INDIRECT_CALL", "op_str": ins.op_str})
            continue
        symbol = img.plt_symbol(target)
        dm = demangle(symbol)
        row = {"site": hx(ins.address), "target": hx(target), "target_section": img.section_name(target), "symbol": symbol, "demangled": dm}
        calls.append(row)
        text = (dm or symbol or "").lower()
        if "qobject" in text and "connect" in text and "disconnect" not in text and "connectnotify" not in text:
            candidates.append((idx, row))
    result["bounded_calls"] = calls
    result["qt_connection_candidate_count"] = len(candidates)
    result["qt_connection_candidates"] = [row for _, row in candidates]
    if len(candidates) != 1:
        result["classification"] = "QT_CONNECTION_PRIMITIVE_NOT_UNIQUE"
        return result
    call_idx, primitive = candidates[0]
    primitive_name = primitive.get("demangled") or primitive.get("symbol") or "UNKNOWN"
    result["actual_qt_connection_primitive"] = primitive_name
    result["actual_qt_connection_callsite"] = primitive["site"]
    args = {reg: resolve_reg(img, window, call_idx, reg) for reg in ("rdi", "rsi", "rdx", "rcx", "r8", "r9")}
    payloads = stack_payloads(img, window, call_idx)
    result["connection_register_arguments"] = args
    result["connection_stack_payloads"] = payloads
    peer_refs_before = [row for row in refs if row["classification"] == "PEER_FUNCTION" and int(row["site"], 16) <= int(primitive["site"], 16)]
    adapter_refs_before = [row for row in refs if row["classification"] == "ADAPTER_FUNCTION" and int(row["site"], 16) <= int(primitive["site"], 16)]
    signal_stack = args["rsi"].get("stack_displacement_value") if args["rsi"].get("classification") == "STACK_ADDRESS" else None
    slot_stack = args["rcx"].get("stack_displacement_value") if args["rcx"].get("classification") == "STACK_ADDRESS" else None
    if signal_stack is not None:
        matching = [row for row in payloads if row["stack_displacement_value"] == signal_stack]
        result["peer_signal_bound_to_connection"] = any(contains_classification(row, "PEER_FUNCTION") for row in matching)
    if slot_stack is not None:
        matching = [row for row in payloads if row["stack_displacement_value"] == slot_stack]
        result["sendlogin_adapter_bound_to_connection"] = any(contains_classification(row, "ADAPTER_FUNCTION") for row in matching)
    # Keep reference presence as evidence only; it is never promoted to binding by adjacency.
    result["peer_reference_before_connection_count"] = len(peer_refs_before)
    result["adapter_reference_before_connection_count"] = len(adapter_refs_before)
    lower = primitive_name.lower()
    if "connectimpl" in lower or "qobject::connect(" in lower:
        result["qt_call_contract"] = {"sender_register": "rdi", "receiver_register": "rdx", "signal_register": "rsi", "slot_or_method_register": "rcx"}
        if result["peer_signal_bound_to_connection"] and owner != "UNKNOWN":
            result["sender_endpoint_identity"] = owner
        # A receiver register provenance is retained, but no class identity is fabricated from a field/entry argument.
        result["receiver_endpoint_provenance"] = args["rdx"]
    else:
        result["qt_call_contract"] = "UNSUPPORTED_EXACT_CONNECT_SIGNATURE"
    if result["peer_signal_bound_to_connection"] and result["sendlogin_adapter_bound_to_connection"] and result["sender_endpoint_identity"] != "UNKNOWN" and result["receiver_endpoint_identity"] != "UNKNOWN":
        result["sendlogin_causal_binding_proven"] = True
    result["classification"] = "BOUNDED_QT_CONNECTION_CALL_PROVEN"
    return result


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")
    img = Image(client)
    try:
        meta = decode_metaobject(img)
        connection = analyze_connection(img, str(meta.get("owner_identity", "UNKNOWN")))
    finally:
        img.close()
    owner = str(meta.get("owner_identity", "UNKNOWN"))
    primitive = str(connection.get("actual_qt_connection_primitive", "UNKNOWN"))
    sender = str(connection.get("sender_endpoint_identity", "UNKNOWN"))
    receiver = str(connection.get("receiver_endpoint_identity", "UNKNOWN"))
    causal = bool(connection.get("sendlogin_causal_binding_proven", False))
    signal_bound = meta.get("signal_binding") == "METAOBJECT_METHOD_INDEX_0"
    positive = owner != "UNKNOWN" and signal_bound and primitive != "UNKNOWN" and sender != "UNKNOWN" and receiver != "UNKNOWN" and causal
    if owner == "UNKNOWN":
        missing = "PEER_METAOBJECT_OWNER_NOT_UNIQUELY_DECODED"
    elif not signal_bound:
        missing = "PEER_SIGNAL_INDEX_0_NOT_BOUND_IN_METAOBJECT"
    elif primitive == "UNKNOWN":
        missing = "ACTUAL_QT_CONNECTION_PRIMITIVE_NOT_UNIQUE_IN_BOUNDED_NEIGHBORHOOD"
    elif not connection.get("peer_signal_bound_to_connection"):
        missing = "PEER_SIGNAL_TO_QT_CONNECTION_DATAFLOW_NOT_PROVEN"
    elif not connection.get("sendlogin_adapter_bound_to_connection"):
        missing = "SENDLOGIN_ADAPTER_TO_QT_CONNECTION_DATAFLOW_NOT_PROVEN"
    elif sender == "UNKNOWN" or receiver == "UNKNOWN":
        missing = "SENDER_RECEIVER_ENDPOINT_IDENTITY_NOT_PROVEN"
    elif not causal:
        missing = "SENDLOGIN_CAUSAL_BINDING_NOT_PROVEN"
    else:
        missing = "NONE"
    result = {
        "schema": "otclient.track-a.be4f48-sendlogin-peer-metaowner.v1",
        "runtime_access": "none",
        "official_client_executed": False,
        "login_performed": False,
        "credentials_used": False,
        "secret_access": False,
        "process_memory_access": False,
        "packet_capture": False,
        "raw_client_uploaded": False,
        "official_service_e2e_count": 0,
        "track_b_pr_284_modified": False,
        "exact_client": {"version": EXPECTED_VERSION, "size": EXPECTED_SIZE, "sha256": EXPECTED_SHA256},
        "metaobject_anchor": hx(METAOBJECT_ANCHOR),
        "signal_index": SIGNAL_INDEX,
        "peer_target": hx(PEER_TARGET),
        "sendlogin_adapter_target": hx(ADAPTER_TARGET),
        "adapter_reference_site": hx(ADAPTER_REFERENCE_SITE),
        "connection_owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        "peer_metaobject": meta,
        "peer_owner_identity": owner,
        "peer_signal_binding": meta.get("signal_binding", "UNKNOWN"),
        "actual_qt_connection_primitive": primitive,
        "actual_qt_connection_callsite": connection.get("actual_qt_connection_callsite"),
        "sender_endpoint_identity": sender,
        "receiver_endpoint_identity": receiver,
        "sendlogin_causal_binding_proven": causal,
        "connection_analysis": connection,
        "pre_login_sequence_advanced": False,
        "terminal_result": "SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN" if positive else "SOURCE_BLOCKER",
        "first_missing_boundary": missing,
        "classification_boundary": "EXACT_STATIC_METAOBJECT_PLUS_BOUNDED_LOCAL_QT_CONNECTION_ONLY; NO_RUNTIME_OR_GLOBAL_DISCOVERY",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.client, args.output)
    print("BE4F48_SENDLOGIN_PEER_METAOWNER_ANALYSIS=PASS")
    print("PEER_OWNER_IDENTITY=" + str(result["peer_owner_identity"]))
    print("ACTUAL_QT_CONNECTION_PRIMITIVE=" + str(result["actual_qt_connection_primitive"]))
    print("SENDLOGIN_CAUSAL_BINDING_PROVEN=" + str(result["sendlogin_causal_binding_proven"]).lower())
    print("TERMINAL_RESULT=" + str(result["terminal_result"]))


if __name__ == "__main__":
    main()
