#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from capstone import CS_ARCH_X86, CS_MODE_64, Cs
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)
CONNECTIMPL_CALLSITE = 0x7C6B9F
RECEIVER_FIELD_OFFSET = 0x88
ADAPTER_TARGET = 0xBD3050
PROMOTED_SENDER = "tibia::authentication::TLoginProtocolMessageHandler"
PROMOTED_SIGNAL = "sendLoginMessage"
CALLER_SAVED = {"rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"}
ENTRY_OWNER = {"kind": "ENTRY_ARG", "name": "rdi"}


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


class Image:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections: list[tuple[int, int, int]] = []
        for sec in self.elf.iter_sections():
            start = int(sec["sh_addr"])
            size = int(sec["sh_size"])
            off = int(sec["sh_offset"])
            if start and size:
                self.sections.append((start, start + size, off))
        self.relocations: dict[int, int] = {}
        self.symbol_relocations: dict[int, str] = {}
        for sec in self.elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                addr = int(rel["r_offset"])
                if int(rel["r_info_type"]) == 8 and rel.is_RELA():
                    self.relocations[addr] = int(rel["r_addend"]) & 0xFFFFFFFFFFFFFFFF
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
            (int(e["initial_location"]), int(e["initial_location"]) + int(e["address_range"]))
            for e in dwarf.EH_CFI_entries()
            if isinstance(e, FDE)
        )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def close(self) -> None:
        self.handle.close()

    def loc(self, va: int, size: int = 1) -> int:
        for lo, hi, off in self.sections:
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
        if va in self.relocations:
            return self.relocations[va]
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
        p = subprocess.run(cmd, check=True, text=True, capture_output=True, timeout=2)
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
    if ins.mnemonic not in ("call", "jmp") or not ins.operands or ins.operands[0].type != X86_OP_IMM:
        return None
    return int(ins.operands[0].imm)


def expr_key(expr: dict[str, Any]) -> tuple[Any, ...]:
    kind = expr.get("kind")
    if kind in ("ENTRY_ARG", "CONST", "ADDR", "CALL_RESULT", "UNKNOWN"):
        return (kind, expr.get("name"), expr.get("value"), expr.get("target"), expr.get("reason"))
    if kind in ("ADD", "MEM"):
        return (kind, expr_key(expr.get("base", {})), int(expr.get("disp", 0)))
    return ("UNKNOWN",)


def resolve_register(img: Image, instructions: list[Any], before: int, wanted: str, depth: int = 0) -> dict[str, Any]:
    if depth > 14:
        return {"kind": "UNKNOWN", "reason": "MAX_SLICE_DEPTH"}
    for i in range(before - 1, -1, -1):
        ins = instructions[i]
        if ins.mnemonic == "call":
            if wanted == "rax":
                return {"kind": "CALL_RESULT", "target": hx(direct_target(ins)), "site": hx(int(ins.address))}
            if wanted in CALLER_SAVED:
                return {"kind": "UNKNOWN", "reason": "CALL_CLOBBER", "site": hx(int(ins.address))}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        site = hx(int(ins.address))
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_REG:
                out = resolve_register(img, instructions, i, canonical_reg(img, src.reg), depth + 1)
                return {**out, "via": wanted, "site": site}
            if src.type == X86_OP_IMM:
                return {"kind": "CONST", "value": hx(int(src.imm) & 0xFFFFFFFFFFFFFFFF), "site": site}
            if src.type == X86_OP_MEM:
                if src.mem.base == X86_REG_RIP:
                    addr = int(ins.address) + int(ins.size) + int(src.mem.disp)
                    return {"kind": "MEM", "base": {"kind": "ADDR", "value": hx(addr)}, "disp": 0, "site": site}
                if src.mem.base and not src.mem.index:
                    base = resolve_register(img, instructions, i, canonical_reg(img, src.mem.base), depth + 1)
                    return {"kind": "MEM", "base": base, "disp": int(src.mem.disp), "site": site}
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            if src.mem.base == X86_REG_RIP and not src.mem.index:
                addr = int(ins.address) + int(ins.size) + int(src.mem.disp)
                return {"kind": "ADDR", "value": hx(addr), "site": site}
            if src.mem.base and not src.mem.index:
                base = resolve_register(img, instructions, i, canonical_reg(img, src.mem.base), depth + 1)
                return {"kind": "ADD", "base": base, "disp": int(src.mem.disp), "site": site}
        if ins.mnemonic == "xor" and src is not None and src.type == X86_OP_REG and canonical_reg(img, src.reg) == wanted:
            return {"kind": "CONST", "value": "0x0", "site": site}
        return {"kind": "UNKNOWN", "reason": "UNSUPPORTED_REGISTER_DEFINITION", "site": site, "op": ins.op_str}
    return {"kind": "ENTRY_ARG", "name": wanted}


def operand_expr(img: Image, instructions: list[Any], index: int, op: Any) -> dict[str, Any]:
    if op.type == X86_OP_REG:
        return resolve_register(img, instructions, index, canonical_reg(img, op.reg))
    if op.type == X86_OP_IMM:
        return {"kind": "CONST", "value": hx(int(op.imm) & 0xFFFFFFFFFFFFFFFF)}
    if op.type == X86_OP_MEM:
        if op.mem.base == X86_REG_RIP:
            addr = int(instructions[index].address) + int(instructions[index].size) + int(op.mem.disp)
            return {"kind": "MEM", "base": {"kind": "ADDR", "value": hx(addr)}, "disp": 0}
        if op.mem.base and not op.mem.index:
            base = resolve_register(img, instructions, index, canonical_reg(img, op.mem.base))
            return {"kind": "MEM", "base": base, "disp": int(op.mem.disp)}
    return {"kind": "UNKNOWN", "reason": "UNSUPPORTED_OPERAND"}


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
    if not type_name or (type_name == raw_name and not raw_name.startswith(("N", "Z", "St", "Q"))):
        return None
    return {"vptr": hx(vptr), "typeinfo": hx(typeinfo), "type_name_raw": raw_name, "type_name": type_name}


def typed_vptr_events(img: Image, instructions: list[Any], object_expr: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i, ins in enumerate(instructions):
        if ins.mnemonic not in ("mov", "movabs", "cmp") or len(ins.operands) < 2:
            continue
        left, right = ins.operands[0], ins.operands[1]
        if left.type != X86_OP_MEM or not left.mem.base or left.mem.index or int(left.mem.disp) != 0:
            continue
        base = resolve_register(img, instructions, i, canonical_reg(img, left.mem.base))
        if expr_key(base) != expr_key(object_expr):
            continue
        value = operand_expr(img, instructions, i, right)
        if value.get("kind") != "ADDR" or not value.get("value"):
            continue
        rtti = rtti_from_vptr(img, int(str(value["value"]), 16))
        if rtti:
            rows.append({"site": hx(int(ins.address)), "operation": ins.mnemonic, "object": base, **rtti})
    unique: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        unique[(row["site"], row["type_name"], row["vptr"])] = row
    return list(unique.values())


def recover_in_fde_owner_identity(img: Image, owner_insns: list[Any]) -> dict[str, Any]:
    events = typed_vptr_events(img, owner_insns, ENTRY_OWNER)
    types = sorted({row["type_name"] for row in events})
    proven = len(types) == 1 and len(events) >= 1
    return {
        "proven": proven,
        "identity": types[0] if proven else "UNKNOWN",
        "types": types,
        "events": events,
        "proof_classes": ["ENTRY_OBJECT_VPTR_BINDING", "ITANIUM_RTTI"] if proven else [],
        "missing": "none" if proven else ("ENTRY_OBJECT_TYPED_VPTR_NOT_FOUND_IN_FDE" if not events else "ENTRY_OBJECT_TYPED_VPTR_TYPE_NOT_UNIQUE"),
    }


def callee_primary_types(img: Image, target: int) -> list[dict[str, Any]]:
    fde = img.containing_fde(target)
    if not fde or fde == CONNECTION_OWNER_FDE or fde[1] - fde[0] > 0x10000:
        return []
    insns = img.disassemble(*fde)
    events = typed_vptr_events(img, insns, ENTRY_OWNER)
    types = sorted({row["type_name"] for row in events})
    if len(types) != 1:
        return []
    return [{"callee_fde": [hx(fde[0]), hx(fde[1])], "identity": types[0], "events": events}]


def follow_unique_identity_edge(img: Image, owner_insns: list[Any]) -> dict[str, Any]:
    bound_calls: list[dict[str, Any]] = []
    for i, ins in enumerate(owner_insns):
        target = direct_target(ins)
        if ins.mnemonic != "call" or target is None:
            continue
        this_expr = resolve_register(img, owner_insns, i, "rdi")
        if expr_key(this_expr) != expr_key(ENTRY_OWNER):
            continue
        bound_calls.append({"site": hx(int(ins.address)), "target": target, "target_hex": hx(target), "symbol": demangle(img.plt_symbol(target))})
    if len(bound_calls) != 1:
        return {
            "proven": False,
            "identity": "UNKNOWN",
            "entry_object_bound_direct_calls": [{k: v for k, v in row.items() if k != "target"} for row in bound_calls],
            "missing": "ENTRY_OBJECT_IDENTITY_EDGE_NOT_UNIQUE" if bound_calls else "ENTRY_OBJECT_IDENTITY_EDGE_NOT_FOUND",
        }
    edge = bound_calls[0]
    typed = callee_primary_types(img, int(edge["target"]))
    if len(typed) != 1:
        return {
            "proven": False,
            "identity": "UNKNOWN",
            "entry_object_bound_direct_calls": [{k: v for k, v in edge.items() if k != "target"}],
            "followed_edge": {k: v for k, v in edge.items() if k != "target"},
            "missing": "UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN",
        }
    return {
        "proven": True,
        "identity": typed[0]["identity"],
        "entry_object_bound_direct_calls": [{k: v for k, v in edge.items() if k != "target"}],
        "followed_edge": {k: v for k, v in edge.items() if k != "target"},
        "callee_type_evidence": typed[0],
        "proof_classes": ["UNIQUE_ENTRY_OBJECT_DIRECT_EDGE", "CALLEE_ENTRY_OBJECT_VPTR_ITANIUM_RTTI"],
        "missing": "none",
    }


def choose_owner_identity(in_fde: dict[str, Any], edge: dict[str, Any]) -> dict[str, Any]:
    if in_fde.get("proven") and edge.get("proven"):
        if in_fde.get("identity") != edge.get("identity"):
            return {"proven": False, "identity": "UNKNOWN", "proof_classes": [], "missing": "OWNER_IDENTITY_PROOF_CLASSES_DISAGREE"}
        return {
            "proven": True,
            "identity": in_fde["identity"],
            "proof_classes": sorted(set(in_fde.get("proof_classes", []) + edge.get("proof_classes", []))),
            "missing": "none",
        }
    if in_fde.get("proven"):
        return {"proven": True, "identity": in_fde["identity"], "proof_classes": in_fde.get("proof_classes", []), "missing": "none"}
    if edge.get("proven"):
        return {"proven": True, "identity": edge["identity"], "proof_classes": edge.get("proof_classes", []), "missing": "none"}
    missing = str(in_fde.get("missing") or "ENTRY_OBJECT_TYPE_UNKNOWN")
    if missing == "ENTRY_OBJECT_TYPED_VPTR_NOT_FOUND_IN_FDE":
        missing = str(edge.get("missing") or missing)
    return {"proven": False, "identity": "UNKNOWN", "proof_classes": [], "missing": missing}


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={sha}")
    img = Image(client)
    try:
        owner_fde = img.containing_fde(CONNECTIMPL_CALLSITE)
        if owner_fde != CONNECTION_OWNER_FDE:
            raise RuntimeError(f"connection owner FDE mismatch: {owner_fde}")
        owner_insns = img.disassemble(*owner_fde)
        connect_rows = [ins for ins in owner_insns if int(ins.address) == CONNECTIMPL_CALLSITE]
        if len(connect_rows) != 1 or connect_rows[0].mnemonic != "call":
            raise RuntimeError("promoted connectImpl callsite is not one unique call in owner FDE")

        in_fde = recover_in_fde_owner_identity(img, owner_insns)
        edge = follow_unique_identity_edge(img, owner_insns) if not in_fde.get("proven") else {
            "proven": False,
            "identity": "UNKNOWN",
            "not_followed": True,
            "reason": "IN_FDE_OWNER_IDENTITY_ALREADY_TERMINAL",
            "missing": "none",
        }
        owner = choose_owner_identity(in_fde, edge)
        owner_proven = bool(owner.get("proven"))
        owner_identity = str(owner.get("identity", "UNKNOWN"))

        receiver_identity = "UNKNOWN"
        receiver_proven = False
        pair_proven = False
        causal_proven = False
        terminal = "SENDLOGIN_CONNECTION_OWNER_TYPE_PROVEN" if owner_proven else "SOURCE_BLOCKER"
        first_missing = "none" if owner_proven else str(owner.get("missing") or "ENTRY_OBJECT_TYPE_UNKNOWN")
        result = {
            "schema": "otclient.track-a.be4f48-sendlogin-connection-owner-type.v1",
            "runtime_access": "none",
            "official_client_executed": False,
            "login_performed": False,
            "credentials_used": False,
            "process_memory_access": False,
            "packet_capture": False,
            "ocr_vision_used": False,
            "official_service_e2e_count": 0,
            "track_b_pr_284_modified": False,
            "exact_client_fence_proven": True,
            "exact_client": {"version": EXPECTED_VERSION, "size": EXPECTED_SIZE, "sha256": EXPECTED_SHA256},
            "sendlogin_sender_identity": PROMOTED_SENDER,
            "sendlogin_signal": PROMOTED_SIGNAL,
            "sendlogin_connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
            "sendlogin_adapter_target": hx(ADAPTER_TARGET),
            "connection_owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
            "connection_owner_entry_object": "ENTRY_ARG:rdi",
            "connection_owner_identity": owner_identity,
            "connection_owner_identity_proven": owner_proven,
            "connection_owner_identity_proof_classes": owner.get("proof_classes", []),
            "connection_owner_identity_evidence": {"in_fde": in_fde, "unique_edge": edge},
            "sendlogin_receiver_provenance": "OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]",
            "sendlogin_receiver_identity": receiver_identity,
            "sendlogin_receiver_identity_proven": receiver_proven,
            "receiver_typing_disposition": "NOT_ATTEMPTED_WITHOUT_UNIQUE_OWNER_LAYOUT_ROUTE" if owner_proven else "BLOCKED_BY_OWNER_IDENTITY",
            "complete_sender_receiver_pair_proven": pair_proven,
            "sendlogin_causal_binding_proven": causal_proven,
            "pre_success_send_sequence": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal,
            "FIRST_MISSING_BOUNDARY": first_missing,
            "NEXT_ACTION": "clean coordinator promotion" if owner_proven else "one newly admitted bounded step only if coordinator authorizes it",
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
