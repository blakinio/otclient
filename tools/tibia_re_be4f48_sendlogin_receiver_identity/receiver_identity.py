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

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)
CONNECTIMPL_CALLSITE = 0x7C6B9F
RECEIVER_FIELD_OFFSET = 0x88
ADAPTER_TARGET = 0xBD3050
PROMOTED_SENDER = "tibia::authentication::TLoginProtocolMessageHandler"
PROMOTED_SIGNAL = "sendLoginMessage"


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def signed64(value: int) -> int:
    value &= 0xFFFFFFFFFFFFFFFF
    return value - (1 << 64) if value & (1 << 63) else value


def parse_itanium_nested_name(value: str) -> str | None:
    if not value.startswith("N") or not value.endswith("E"):
        return None
    i = 1
    end = len(value) - 1
    out: list[str] = []
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
        out.append(part)
        i = j + n
    return "::".join(out) if out and i == end else None


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

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def read(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def qword(self, va: int) -> int:
        rel = self.relocations.get(va)
        if rel and rel.get("addend"):
            return int(rel["addend"]) & 0xFFFFFFFFFFFFFFFF
        return struct.unpack("<Q", self.read(va, 8))[0]

    def cstring(self, va: int, max_len: int = 1024) -> str:
        off = self.va_to_off(va)
        end = self.raw.find(b"\0", off, min(len(self.raw), off + max_len))
        if end < 0:
            raise RuntimeError(f"unterminated string at {hx(va)}")
        return self.raw[off:end].decode("ascii", "strict")

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

    def fde_instructions(self, target: int) -> tuple[tuple[int, int], list[Any]]:
        fde = self.containing_fde(target)
        if fde is None:
            raise RuntimeError(f"no unique FDE for {hx(target)}")
        return fde, self.disassemble(*fde)

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
        p = subprocess.run(["c++filt", symbol], text=True, capture_output=True, check=True, timeout=2)
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
    return int(ins.operands[0].imm) if ins.operands[0].type == X86_OP_IMM else None


def rip_target(ins: Any) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return int(ins.address) + int(ins.size) + int(op.mem.disp)
    return None


def decode_vtable(img: Image, ap: int) -> dict[str, Any] | None:
    if not img.mapped(ap - 16, 24):
        return None
    try:
        offset_to_top = signed64(img.qword(ap - 16))
        if not -(1 << 20) < offset_to_top < (1 << 20):
            return None
        rtti = img.qword(ap - 8)
        if not img.mapped(rtti + 8, 8):
            return None
        name_va = img.qword(rtti + 8)
        mangled = img.cstring(name_va)
        decoded = parse_itanium_nested_name(mangled)
        return {"address_point": hx(ap), "rtti": hx(rtti), "rtti_mangled": mangled, "rtti_decoded": decoded or "UNKNOWN"}
    except Exception:
        return None


def field_refs(img: Image, insns: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i, ins in enumerate(insns):
        for opi, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or not op.mem.base:
                continue
            if canonical_reg(img, op.mem.base) != "rbx" or int(op.mem.disp) != RECEIVER_FIELD_OFFSET:
                continue
            role = "READ"
            if opi == 0 and ins.mnemonic.startswith(("mov", "lea")):
                role = "WRITE" if ins.mnemonic.startswith("mov") else "ADDRESS"
            rows.append({"index": i, "site": hx(int(ins.address)), "mnemonic": ins.mnemonic, "op_str": ins.op_str, "operand_index": opi, "role": role})
    return rows


def receiver_definition(img: Image, insns: list[Any], call_index: int) -> dict[str, Any]:
    for i in range(call_index - 1, max(-1, call_index - 40), -1):
        ins = insns[i]
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != "rcx":
            continue
        if len(ins.operands) < 2:
            break
        src = ins.operands[1]
        if src.type == X86_OP_MEM and src.mem.base and canonical_reg(img, src.mem.base) == "rbx" and int(src.mem.disp) == RECEIVER_FIELD_OFFSET:
            return {"proven": True, "site": hx(int(ins.address)), "op_str": ins.op_str, "provenance": "OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]"}
        return {"proven": False, "site": hx(int(ins.address)), "op_str": ins.op_str, "reason": "RCX_DEFINITION_NOT_RECEIVER_FIELD"}
    return {"proven": False, "reason": "RCX_DEFINITION_NOT_FOUND"}


def find_object_aliases(img: Image, insns: list[Any], start: int, end: int, seed: str) -> set[str]:
    aliases = {seed}
    changed = True
    while changed:
        changed = False
        for ins in insns[start:end]:
            if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
                continue
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_REG and src.type == X86_OP_REG:
                d, s = canonical_reg(img, dst.reg), canonical_reg(img, src.reg)
                if s in aliases and d not in aliases:
                    aliases.add(d); changed = True
    return aliases


def constructor_vtable_identities(img: Image, target: int) -> dict[str, Any]:
    fde = img.containing_fde(target)
    if fde is None:
        return {"target": hx(target), "classification": "NO_UNIQUE_CONSTRUCTOR_FDE", "vtable_candidates": []}
    insns = img.disassemble(*fde)
    aliases = find_object_aliases(img, insns, 0, min(len(insns), 80), "rdi")
    rows: list[dict[str, Any]] = []
    rip_defs: dict[str, tuple[int, int]] = {}
    for i, ins in enumerate(insns[:120]):
        if ins.mnemonic == "lea" and len(ins.operands) >= 2 and ins.operands[0].type == X86_OP_REG:
            target_va = rip_target(ins)
            if target_va is not None:
                rip_defs[canonical_reg(img, ins.operands[0].reg)] = (i, target_va)
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        dst, src = ins.operands[0], ins.operands[1]
        if dst.type != X86_OP_MEM or not dst.mem.base or int(dst.mem.disp) != 0:
            continue
        if canonical_reg(img, dst.mem.base) not in aliases or src.type != X86_OP_REG:
            continue
        sreg = canonical_reg(img, src.reg)
        if sreg not in rip_defs:
            continue
        _, ap = rip_defs[sreg]
        vt = decode_vtable(img, ap)
        if vt:
            rows.append({"store_site": hx(int(ins.address)), **vt})
    unique = sorted({r["rtti_decoded"] for r in rows if r.get("rtti_decoded") not in (None, "UNKNOWN")})
    return {"target": hx(target), "fde": [hx(fde[0]), hx(fde[1])], "vtable_candidates": rows, "unique_rtti_identities": unique}


def source_for_store(img: Image, insns: list[Any], store_index: int) -> dict[str, Any]:
    ins = insns[store_index]
    src = ins.operands[1] if len(ins.operands) > 1 else None
    if src is None or src.type != X86_OP_REG:
        return {"classification": "NON_REGISTER_STORE_SOURCE"}
    wanted = canonical_reg(img, src.reg)
    chain: list[dict[str, Any]] = []
    for i in range(store_index - 1, -1, -1):
        row = insns[i]
        if row.mnemonic == "call" and wanted == "rax":
            tgt = direct_target(row)
            sym = img.plt_symbol(tgt) if tgt else None
            return {"classification": "CALL_RETURN", "register": wanted, "call_site": hx(int(row.address)), "target": hx(tgt), "symbol": sym, "demangled": demangle(sym), "chain": chain}
        if not row.operands:
            continue
        dst = row.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src2 = row.operands[1] if len(row.operands) > 1 else None
        chain.append({"site": hx(int(row.address)), "mnemonic": row.mnemonic, "op_str": row.op_str})
        if src2 is None:
            return {"classification": "UNKNOWN", "chain": chain}
        if src2.type == X86_OP_REG:
            wanted = canonical_reg(img, src2.reg)
            continue
        if src2.type == X86_OP_MEM:
            if src2.mem.base:
                return {"classification": "OBJECT_FIELD", "base_register": canonical_reg(img, src2.mem.base), "displacement": hx(int(src2.mem.disp)), "chain": chain}
            return {"classification": "MEMORY_LOAD", "chain": chain}
        if src2.type == X86_OP_IMM:
            return {"classification": "CONSTANT", "value": hx(int(src2.imm)), "chain": chain}
        return {"classification": "UNKNOWN", "chain": chain}
    return {"classification": f"ENTRY_ARG:{wanted}", "chain": chain}


def constructor_candidates_between(img: Image, insns: list[Any], start: int, stop: int, object_reg: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i in range(start, stop):
        ins = insns[i]
        if ins.mnemonic != "call":
            continue
        tgt = direct_target(ins)
        if tgt is None:
            continue
        sym = img.plt_symbol(tgt)
        if demangle(sym) == "operator new(unsigned long)":
            continue
        # Require a local move/copy of the candidate object into rdi before the call.
        bound = False
        for j in range(i - 1, max(start - 1, i - 10), -1):
            x = insns[j]
            if len(x.operands) < 2 or not x.mnemonic.startswith("mov"):
                continue
            if x.operands[0].type == X86_OP_REG and x.operands[1].type == X86_OP_REG:
                if canonical_reg(img, x.operands[0].reg) == "rdi" and canonical_reg(img, x.operands[1].reg) == object_reg:
                    bound = True; break
        if bound:
            rows.append({"index": i, "call_site": hx(int(ins.address)), "target": hx(tgt), "vtable_proof": constructor_vtable_identities(img, tgt)})
    return rows


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={sha}")
    img = Image(client)
    try:
        fde = img.containing_fde(CONNECTIMPL_CALLSITE)
        if fde != CONNECTION_OWNER_FDE:
            raise RuntimeError(f"connection owner FDE mismatch: {fde}")
        insns = img.disassemble(*CONNECTION_OWNER_FDE)
        call_indexes = [i for i, ins in enumerate(insns) if int(ins.address) == CONNECTIMPL_CALLSITE]
        if len(call_indexes) != 1:
            raise RuntimeError("selected connectImpl callsite not unique")
        call_idx = call_indexes[0]
        call_target = direct_target(insns[call_idx])
        call_symbol = img.plt_symbol(call_target) if call_target else None
        call_demangled = demangle(call_symbol)
        if not call_demangled or "QObject::connectImpl(" not in call_demangled:
            raise RuntimeError(f"selected call no longer connectImpl: {call_demangled}")
        recv = receiver_definition(img, insns, call_idx)
        refs = field_refs(img, insns)
        stores = [r for r in refs if r["role"] == "WRITE" and r["index"] < call_idx]
        store_details: list[dict[str, Any]] = []
        identities: set[str] = set()
        for row in stores:
            idx = int(row["index"])
            src = source_for_store(img, insns, idx)
            detail: dict[str, Any] = {**row, "source": src, "constructor_candidates": []}
            # If the stored register was sourced from rax, inspect bounded constructor calls after the last allocator/copy.
            src_reg = None
            op = insns[idx].operands[1]
            if op.type == X86_OP_REG:
                src_reg = canonical_reg(img, op.reg)
            if src_reg:
                start = max(0, idx - 160)
                ctors = constructor_candidates_between(img, insns, start, idx, src_reg)
                detail["constructor_candidates"] = ctors
                for ctor in ctors:
                    for ident in ctor.get("vtable_proof", {}).get("unique_rtti_identities", []):
                        identities.add(str(ident))
            store_details.append(detail)
        receiver_identity = next(iter(identities)) if len(identities) == 1 else "UNKNOWN"
        identity_proven = receiver_identity != "UNKNOWN" and len(stores) == 1
        complete_pair = bool(recv.get("proven")) and identity_proven
        causal = complete_pair
        if not recv.get("proven"):
            missing = "RECEIVER_PROVENANCE_NOT_REPRODUCED_AT_CONNECTIMPL"
        elif len(stores) == 0:
            missing = "NO_REACHING_RECEIVER_FIELD_DEFINITION_IN_CONNECTION_OWNER_FDE"
        elif len(stores) > 1:
            missing = "RECEIVER_FIELD_HAS_MULTIPLE_REACHING_STORE_CANDIDATES"
        elif not identity_proven:
            missing = "RECEIVER_FIELD_STORE_SOURCE_CLASS_IDENTITY_NOT_UNIQUELY_PROVEN"
        else:
            missing = "NONE"
        terminal = "SENDLOGIN_RECEIVER_IDENTITY_PROVEN" if identity_proven else "SOURCE_BLOCKER"
        result = {
            "schema": "otclient.track-a.be4f48-sendlogin-receiver-identity.v1",
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
            "connection_owner_fde": [hx(CONNECTION_OWNER_FDE[0]), hx(CONNECTION_OWNER_FDE[1])],
            "connectimpl_callsite": hx(CONNECTIMPL_CALLSITE),
            "connectimpl_target": hx(call_target),
            "connectimpl_demangled": call_demangled,
            "sendlogin_sender_identity": PROMOTED_SENDER,
            "sendlogin_signal": PROMOTED_SIGNAL,
            "sendlogin_adapter_target": hx(ADAPTER_TARGET),
            "receiver_field_offset": hx(RECEIVER_FIELD_OFFSET),
            "receiver_endpoint_provenance": recv.get("provenance", "UNKNOWN"),
            "receiver_definition": recv,
            "receiver_field_references": [{k: v for k, v in r.items() if k != "index"} for r in refs],
            "receiver_field_store_count": len(stores),
            "receiver_field_store_details": [{k: v for k, v in r.items() if k != "index"} for r in store_details],
            "receiver_identity_candidates": sorted(identities),
            "receiver_endpoint_identity": receiver_identity,
            "receiver_identity_proven": identity_proven,
            "complete_sender_receiver_pair_proven": complete_pair,
            "sendlogin_adapter_bound_to_receiver": complete_pair,
            "sendlogin_causal_binding_proven": causal,
            "pre_success_send_sequence": "UNKNOWN",
            "field6_value": "UNKNOWN",
            "terminal_result": terminal,
            "FIRST_MISSING_BOUNDARY": missing,
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
    a = p.parse_args()
    analyze(a.client, a.output)


if __name__ == "__main__":
    main()
