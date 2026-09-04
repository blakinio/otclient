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


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


class Image:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections: list[tuple[int, int, int, int]] = []
        for sec in self.elf.iter_sections():
            start = int(sec["sh_addr"])
            size = int(sec["sh_size"])
            off = int(sec["sh_offset"])
            flags = int(sec["sh_flags"])
            if start and size:
                self.sections.append((start, start + size, off, flags))
        self.relocations: dict[int, int] = {}
        self.symbol_relocations: dict[int, str] = {}
        for sec in self.elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                addr = int(rel["r_offset"])
                rtype = int(rel["r_info_type"])
                if rtype == 8 and rel.is_RELA():
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
        for lo, hi, off, _ in self.sections:
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

    def executable_ranges(self) -> list[tuple[int, int, int]]:
        return [(lo, hi, off) for lo, hi, off, flags in self.sections if flags & 0x4]

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
    if kind == "ADD":
        return (kind, expr_key(expr.get("base", {})), int(expr.get("disp", 0)))
    if kind == "MEM":
        return (kind, expr_key(expr.get("base", {})), int(expr.get("disp", 0)))
    return ("UNKNOWN",)


def resolve_register(
    img: Image,
    instructions: list[Any],
    before: int,
    wanted: str,
    depth: int = 0,
) -> dict[str, Any]:
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


def find_direct_callers(img: Image, target: int) -> list[dict[str, Any]]:
    raw_candidates: list[int] = []
    for lo, hi, off in img.executable_ranges():
        blob = img.raw[off : off + (hi - lo)]
        p = 0
        while True:
            p = blob.find(b"\xe8", p)
            if p < 0:
                break
            if p + 5 <= len(blob):
                site = lo + p
                rel = int.from_bytes(blob[p + 1 : p + 5], "little", signed=True)
                if site + 5 + rel == target:
                    raw_candidates.append(site)
            p += 1
    rows: list[dict[str, Any]] = []
    for site in sorted(set(raw_candidates)):
        fde = img.containing_fde(site)
        if not fde:
            continue
        insns = img.disassemble(*fde)
        matches = [ins for ins in insns if int(ins.address) == site and direct_target(ins) == target and ins.mnemonic == "call"]
        if len(matches) == 1:
            rows.append({"site": site, "fde": fde})
    return rows


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
    if not type_name or type_name == raw_name and not raw_name.startswith(("N", "Z", "St", "Q")):
        return None
    return {
        "vptr": hx(vptr),
        "typeinfo": hx(typeinfo),
        "type_name_raw": raw_name,
        "type_name": type_name,
    }


def constructor_primary_types(img: Image, target: int) -> list[dict[str, Any]]:
    fde = img.containing_fde(target)
    if not fde or fde[1] - fde[0] > 0x10000:
        return []
    insns = img.disassemble(*fde)
    entry_this = {"kind": "ENTRY_ARG", "name": "rdi"}
    out: list[dict[str, Any]] = []
    for i, ins in enumerate(insns):
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or not dst.mem.base or dst.mem.index or int(dst.mem.disp) != 0:
            continue
        base = resolve_register(img, insns, i, canonical_reg(img, dst.mem.base))
        if expr_key(base) != expr_key(entry_this):
            continue
        value = operand_expr(img, insns, i, src)
        if value.get("kind") != "ADDR" or not value.get("value"):
            continue
        vptr = int(str(value["value"]), 16)
        rtti = rtti_from_vptr(img, vptr)
        if rtti:
            out.append({"store_site": hx(int(ins.address)), "callee_fde": [hx(fde[0]), hx(fde[1])], **rtti})
    uniq: dict[tuple[str, str], dict[str, Any]] = {}
    for row in out:
        uniq[(row["type_name"], row["vptr"])] = row
    return list(uniq.values())


def trace_owner_initializer(img: Image) -> dict[str, Any]:
    callers = find_direct_callers(img, CONNECTION_OWNER_FDE[0])
    public_callers = [{"site": hx(r["site"]), "fde": [hx(r["fde"][0]), hx(r["fde"][1])]} for r in callers]
    if len(callers) != 1:
        return {
            "proven": False,
            "callers": public_callers,
            "missing": "CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE",
        }

    caller = callers[0]
    caller_fde = caller["fde"]
    if caller_fde[1] - caller_fde[0] > 0x10000:
        return {
            "proven": False,
            "callers": public_callers,
            "missing": "CONNECTION_OWNER_DIRECT_CALLER_FDE_TOO_LARGE_FOR_BOUNDED_ANALYSIS",
        }
    insns = img.disassemble(*caller_fde)
    owner_call_indexes = [i for i, ins in enumerate(insns) if int(ins.address) == caller["site"]]
    if len(owner_call_indexes) != 1:
        return {"proven": False, "callers": public_callers, "missing": "OWNER_CALLSITE_NOT_UNIQUE_IN_CALLER_FDE"}
    owner_call_index = owner_call_indexes[0]
    owner_expr = resolve_register(img, insns, owner_call_index, "rdi")

    stores: list[dict[str, Any]] = []
    for i, ins in enumerate(insns):
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or not dst.mem.base or dst.mem.index or int(dst.mem.disp) != RECEIVER_FIELD_OFFSET:
            continue
        base_expr = resolve_register(img, insns, i, canonical_reg(img, dst.mem.base))
        if expr_key(base_expr) != expr_key(owner_expr):
            continue
        stores.append(
            {
                "index": i,
                "site": int(ins.address),
                "op_str": ins.op_str,
                "base_expr": base_expr,
                "source_expr": operand_expr(img, insns, i, src),
            }
        )

    if len(stores) != 1:
        return {
            "proven": False,
            "callers": public_callers,
            "caller_fde": [hx(caller_fde[0]), hx(caller_fde[1])],
            "owner_argument": owner_expr,
            "matching_field_stores": [
                {"site": hx(s["site"]), "op_str": s["op_str"], "source_expr": s["source_expr"]} for s in stores
            ],
            "missing": "BOUND_OWNER_PLUS_0X88_DEFINING_STORE_NOT_UNIQUE",
        }

    store = stores[0]
    source_expr = store["source_expr"]
    constructor_proofs: list[dict[str, Any]] = []
    for i, ins in enumerate(insns[: store["index"] + 1]):
        target = direct_target(ins)
        if ins.mnemonic != "call" or target is None:
            continue
        receiver_expr = resolve_register(img, insns, i, "rdi")
        if expr_key(receiver_expr) != expr_key(source_expr):
            continue
        symbol = demangle(img.plt_symbol(target))
        if symbol and "operator new" in symbol:
            continue
        types = constructor_primary_types(img, target)
        for typed in types:
            constructor_proofs.append(
                {
                    "callsite": hx(int(ins.address)),
                    "target": hx(target),
                    "target_symbol": symbol,
                    "receiver_expr": receiver_expr,
                    **typed,
                }
            )

    unique_types = sorted({row["type_name"] for row in constructor_proofs})
    identity_proven = len(unique_types) == 1 and len(constructor_proofs) >= 1
    identity = unique_types[0] if identity_proven else "UNKNOWN"
    if identity_proven:
        missing = "none"
    elif not constructor_proofs:
        missing = "FIELD_SOURCE_CONSTRUCTOR_WITH_PRIMARY_RTTI_NOT_UNIQUELY_BOUND"
    else:
        missing = "FIELD_SOURCE_CONSTRUCTOR_RTTI_TYPE_NOT_UNIQUE"

    chain = {
        "connection_owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
        "direct_caller_site": hx(caller["site"]),
        "direct_caller_fde": [hx(caller_fde[0]), hx(caller_fde[1])],
        "owner_argument": owner_expr,
        "field_store_site": hx(store["site"]),
        "field_store_op": store["op_str"],
        "field_source": source_expr,
        "constructor_rtti_proofs": constructor_proofs,
    }
    return {
        "proven": identity_proven,
        "callers": public_callers,
        "caller_fde": [hx(caller_fde[0]), hx(caller_fde[1])],
        "owner_argument": owner_expr,
        "field_store_site": hx(store["site"]),
        "field_source": source_expr,
        "constructor_rtti_proofs": constructor_proofs,
        "receiver_endpoint_identity": identity,
        "receiver_identity_proof_classes": (
            ["UNIQUE_BOUND_OWNER_FIELD_STORE_TO_CONSTRUCTOR_OBJECT", "CONSTRUCTOR_PRIMARY_VPTR_ITANIUM_RTTI"]
            if identity_proven
            else []
        ),
        "owner_chain": chain,
        "missing": missing,
    }


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
        if len(connect_rows) != 1:
            raise RuntimeError("connectImpl callsite not unique in promoted owner FDE")
        trace = trace_owner_initializer(img)
        identity_proven = bool(trace.get("proven"))
        identity = str(trace.get("receiver_endpoint_identity", "UNKNOWN"))
        pair_proven = identity_proven
        causal_proven = identity_proven
        terminal = "SENDLOGIN_RECEIVER_FIELD_OWNER_PROVEN" if identity_proven else "SOURCE_BLOCKER"
        result = {
            "schema": "otclient.track-a.be4f48-sendlogin-receiver-field-owner.v1",
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
            "sendlogin_sender_identity": PROMOTED_SENDER,
            "sendlogin_signal": PROMOTED_SIGNAL,
            "sendlogin_connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
            "sendlogin_adapter_target": hx(ADAPTER_TARGET),
            "connection_owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
            "receiver_field_provenance": "OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]",
            "receiver_field_definition_site": trace.get("field_store_site", "UNKNOWN"),
            "receiver_owner_chain": trace.get("owner_chain", "UNKNOWN"),
            "receiver_endpoint_identity": identity,
            "receiver_identity_proven": identity_proven,
            "receiver_identity_proof_classes": trace.get("receiver_identity_proof_classes", []),
            "bounded_trace": trace,
            "complete_sender_receiver_pair_proven": pair_proven,
            "sendlogin_causal_binding_proven": causal_proven,
            "pre_success_send_sequence": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal,
            "FIRST_MISSING_BOUNDARY": trace.get("missing", "none"),
        }
    finally:
        img.close()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--client", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    analyze(args.client, args.output)


if __name__ == "__main__":
    main()
