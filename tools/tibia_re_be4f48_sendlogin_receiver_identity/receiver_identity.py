#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
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

CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)
CONNECTIMPL_CALLSITE = 0x7C6B9F
RECEIVER_FIELD_OFFSET = 0x88
ADAPTER_TARGET = 0xBD3050
CONNECTIMPL_HAS_HIDDEN_SRET = True
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
            start, size, off, flags = int(sec["sh_addr"]), int(sec["sh_size"]), int(sec["sh_offset"]), int(sec["sh_flags"])
            if start and size:
                self.sections.append((start, start + size, off, flags))
        self.relocations: dict[int, str] = {}
        for sec in self.elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                idx = int(rel["r_info_sym"])
                if symtab is not None and idx:
                    try:
                        name = symtab.get_symbol(idx).name or ""
                    except Exception:
                        name = ""
                    if name:
                        self.relocations[int(rel["r_offset"])] = name
        dwarf = self.elf.get_dwarf_info()
        self.fdes = sorted(
            (int(e["initial_location"]), int(e["initial_location"]) + int(e["address_range"]))
            for e in dwarf.EH_CFI_entries() if isinstance(e, FDE)
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
        return self.raw[off:off+size]

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi-lo), lo))

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

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
                if got in self.relocations:
                    return self.relocations[got]
        return None


def demangle(symbol: str | None) -> str | None:
    if not symbol:
        return None
    try:
        p = subprocess.run(["c++filt", symbol], check=True, text=True, capture_output=True, timeout=2)
        return p.stdout.strip() or symbol
    except Exception:
        return symbol


def canonical_reg(img: Image, reg: int) -> str:
    name = img.md.reg_name(reg)
    aliases = {
        "eax":"rax","ax":"rax","al":"rax","ah":"rax","ebx":"rbx","bx":"rbx","bl":"rbx","bh":"rbx",
        "ecx":"rcx","cx":"rcx","cl":"rcx","ch":"rcx","edx":"rdx","dx":"rdx","dl":"rdx","dh":"rdx",
        "esi":"rsi","si":"rsi","sil":"rsi","edi":"rdi","di":"rdi","dil":"rdi","ebp":"rbp","bp":"rbp","bpl":"rbp",
        "esp":"rsp","sp":"rsp","spl":"rsp",
    }
    if name in aliases:
        return aliases[name]
    for n in range(8,16):
        if name in (f"r{n}d", f"r{n}w", f"r{n}b"):
            return f"r{n}"
    return name


def direct_target(ins: Any) -> int | None:
    if ins.mnemonic not in ("call", "jmp") or not ins.operands or ins.operands[0].type != X86_OP_IMM:
        return None
    return int(ins.operands[0].imm)


def stack_deltas(img: Image, instructions: list[Any]) -> list[int]:
    delta = 0
    before: list[int] = []
    for ins in instructions:
        before.append(delta)
        if ins.mnemonic in ("sub", "add") and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == X86_OP_REG and canonical_reg(img, dst.reg) == "rsp" and src.type == X86_OP_IMM:
                amount = int(src.imm)
                delta += -amount if ins.mnemonic == "sub" else amount
        elif ins.mnemonic == "push":
            delta -= 8
        elif ins.mnemonic == "pop":
            delta += 8
    return before


def stack_key(img: Image, ins: Any, delta_before: int, operand_index: int) -> int | None:
    if operand_index >= len(ins.operands):
        return None
    op = ins.operands[operand_index]
    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RSP:
        return None
    return delta_before + int(op.mem.disp)


def resolve_stack_slot(
    img: Image,
    instructions: list[Any],
    before: int,
    wanted_key: int,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 10:
        return {"classification":"UNKNOWN","reason":"MAX_STACK_DEPTH"}
    for i in range(before-1, -1, -1):
        ins = instructions[i]
        if not ins.mnemonic.startswith("mov") or len(ins.operands) < 2:
            continue
        if stack_key(img, ins, deltas[i], 0) != wanted_key:
            continue
        src = ins.operands[1]
        row: dict[str, Any] = {"classification":"STACK_STORE","site":hx(int(ins.address)),"stack_key":wanted_key,"op_str":ins.op_str}
        if src.type == X86_OP_REG:
            nested = resolve_register(img, instructions, i, canonical_reg(img, src.reg), deltas, depth+1)
            row.update({"classification":nested.get("classification","UNKNOWN"),"source":nested})
        elif src.type == X86_OP_IMM:
            row.update({"classification":"CONSTANT","value":hx(int(src.imm)&0xffffffffffffffff)})
        elif src.type == X86_OP_MEM:
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            row.update({"classification":"OBJECT_FIELD","base_register":base,"displacement":hx(int(src.mem.disp))})
        else:
            row["classification"] = "UNKNOWN"
        return row
    return {"classification":"UNKNOWN","reason":"NO_STACK_STORE_FOR_KEY","stack_key":wanted_key}


def resolve_register(
    img: Image,
    instructions: list[Any],
    before: int,
    wanted: str,
    deltas: list[int],
    depth: int = 0,
) -> dict[str, Any]:
    if depth > 10:
        return {"classification":"UNKNOWN","reason":"MAX_SLICE_DEPTH"}
    for i in range(before-1, -1, -1):
        ins = instructions[i]
        if ins.mnemonic == "call" and wanted in CALLER_SAVED:
            return {"classification":"UNKNOWN","reason":"CALL_CLOBBER_BOUNDARY","boundary_site":hx(int(ins.address))}
        if not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_REG or canonical_reg(img, dst.reg) != wanted:
            continue
        src = ins.operands[1] if len(ins.operands) > 1 else None
        row: dict[str, Any] = {"definition_site":hx(int(ins.address)),"mnemonic":ins.mnemonic,"op_str":ins.op_str}
        if ins.mnemonic.startswith("mov") and src is not None:
            if src.type == X86_OP_REG:
                via = canonical_reg(img, src.reg)
                nested = resolve_register(img, instructions, i, via, deltas, depth+1)
                row.update({"classification":nested.get("classification","UNKNOWN"),"via_register":via,"source":nested})
                return row
            if src.type == X86_OP_MEM:
                if src.mem.base == X86_REG_RSP:
                    key = deltas[i] + int(src.mem.disp)
                    nested = resolve_stack_slot(img, instructions, i, key, deltas, depth+1)
                    row.update({"classification":nested.get("classification","UNKNOWN"),"stack_key":key,"source":nested})
                    return row
                base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
                row.update({"classification":"OBJECT_FIELD","base_register":base,"displacement":hx(int(src.mem.disp))})
                return row
            if src.type == X86_OP_IMM:
                row.update({"classification":"CONSTANT","value":hx(int(src.imm)&0xffffffffffffffff)})
                return row
        if ins.mnemonic == "lea" and src is not None and src.type == X86_OP_MEM:
            base = canonical_reg(img, src.mem.base) if src.mem.base else "none"
            row.update({"classification":"OBJECT_ADDRESS" if base != "rsp" else "STACK_ADDRESS","base_register":base,"displacement":hx(int(src.mem.disp))})
            return row
        return {**row,"classification":"UNKNOWN","reason":"UNSUPPORTED_DEFINITION"}
    return {"classification":f"ENTRY_ARG:{wanted}","reason":"NO_BOUNDED_DEFINITION"}


def contains_receiver_field(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("classification") == "OBJECT_FIELD" and value.get("base_register") == "rbx" and value.get("displacement") == hx(RECEIVER_FIELD_OFFSET):
            return True
        return any(contains_receiver_field(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_receiver_field(v) for v in value)
    return False


def resolve_receiver_argument(img: Image, instructions: list[Any], call_index: int) -> dict[str, Any]:
    deltas = stack_deltas(img, instructions)
    resolved = resolve_register(img, instructions, call_index, "rcx", deltas)
    proven = contains_receiver_field(resolved)
    return {
        "proven": proven,
        "classification": resolved.get("classification","UNKNOWN"),
        "provenance": "OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]" if proven else "UNKNOWN",
        "slice": resolved,
    }


def receiver_field_refs(img: Image, instructions: list[Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reads: list[dict[str, Any]] = []
    writes: list[dict[str, Any]] = []
    for ins in instructions:
        for oi, op in enumerate(ins.operands):
            if op.type != X86_OP_MEM or not op.mem.base or canonical_reg(img, op.mem.base) != "rbx" or int(op.mem.disp) != RECEIVER_FIELD_OFFSET:
                continue
            row={"site":hx(int(ins.address)),"mnemonic":ins.mnemonic,"op_str":ins.op_str,"operand_index":oi}
            if oi == 0 and ins.mnemonic.startswith("mov"):
                writes.append(row)
            else:
                reads.append(row)
    return reads, writes


def analyze(client: Path, output: Path) -> dict[str, Any]:
    raw = client.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={sha}")
    img=Image(client)
    try:
        fde=img.containing_fde(CONNECTIMPL_CALLSITE)
        if fde != CONNECTION_OWNER_FDE:
            raise RuntimeError(f"connection owner FDE mismatch: {fde}")
        insns=img.disassemble(*fde)
        indexes=[i for i,x in enumerate(insns) if int(x.address)==CONNECTIMPL_CALLSITE]
        if len(indexes)!=1:
            raise RuntimeError("connectImpl callsite not unique")
        ci=indexes[0]
        target=direct_target(insns[ci])
        dm=demangle(img.plt_symbol(target)) if target else None
        if not dm or "QObject::connectImpl(" not in dm:
            raise RuntimeError(f"selected call no longer QObject::connectImpl: {dm}")
        recv=resolve_receiver_argument(img,insns,ci)
        reads,writes=receiver_field_refs(img,insns)
        receiver_identity="UNKNOWN"
        identity_proven=False
        pair_proven=False
        causal=False
        if not recv["proven"]:
            missing="STACK_AWARE_RECEIVER_PROVENANCE_NOT_BOUND_TO_RBX_PLUS_0X88"
        elif writes:
            missing="RECEIVER_FIELD_HAS_LOCAL_WRITE_BUT_TYPE_OWNERSHIP_NOT_PROVEN"
        else:
            missing="RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE"
        result={
            "schema":"otclient.track-a.be4f48-sendlogin-receiver-identity.v2",
            "runtime_access":"none",
            "official_client_executed":False,
            "login_performed":False,
            "credentials_used":False,
            "process_memory_access":False,
            "packet_capture":False,
            "ocr_vision_used":False,
            "official_service_e2e_count":0,
            "track_b_pr_284_modified":False,
            "exact_client":{"version":EXPECTED_VERSION,"size":EXPECTED_SIZE,"sha256":EXPECTED_SHA256},
            "connectimpl_has_hidden_sret":CONNECTIMPL_HAS_HIDDEN_SRET,
            "connection_owner_fde":[hx(fde[0]),hx(fde[1])],
            "connectimpl_callsite":hx(CONNECTIMPL_CALLSITE),
            "connectimpl_target":hx(target),
            "connectimpl_demangled":dm,
            "sendlogin_sender_identity":PROMOTED_SENDER,
            "sendlogin_signal":PROMOTED_SIGNAL,
            "sendlogin_adapter_target":hx(ADAPTER_TARGET),
            "receiver_field_offset":hx(RECEIVER_FIELD_OFFSET),
            "receiver_endpoint_provenance":recv["provenance"],
            "receiver_argument_resolution":recv,
            "receiver_field_read_count":len(reads),
            "receiver_field_write_count":len(writes),
            "receiver_field_reads":reads,
            "receiver_field_writes":writes,
            "receiver_endpoint_identity":receiver_identity,
            "receiver_identity_proven":identity_proven,
            "complete_sender_receiver_pair_proven":pair_proven,
            "sendlogin_adapter_bound_to_receiver":pair_proven,
            "sendlogin_causal_binding_proven":causal,
            "pre_success_send_sequence":"UNKNOWN",
            "field6_value":"UNKNOWN",
            "terminal_result":"SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY":missing,
        }
    finally:
        img.close()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--client",type=Path,required=True); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(); analyze(a.client,a.output)


if __name__ == "__main__":
    main()
