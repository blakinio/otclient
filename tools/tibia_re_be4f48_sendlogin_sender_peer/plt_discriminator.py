#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
PEER_TARGET = 0xD052A0
PEER_DIRECT_CALLEE = 0x4D7DC0
HELPER_TARGET = 0x4D8670
ADAPTER_TARGET = 0xBD3050
CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)


def hx(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def demangle_symbol(name: str | None) -> str | None:
    if not name:
        return None
    try:
        row = subprocess.run(
            ["c++filt", name],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return name
    value = row.stdout.strip()
    return value if row.returncode == 0 and value else name


def is_qmeta_activate_symbol(name: str | None) -> bool:
    return bool(name and "QMetaObject::activate(" in name)


def is_qobject_connect_impl_symbol(name: str | None) -> bool:
    return bool(name and "QObject::connectImpl(" in name)


class Image:
    def __init__(self, path: Path):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
        from elftools.dwarf.callframe import FDE
        from elftools.elf.elffile import ELFFile
        from elftools.elf.relocation import RelocationSection

        self.X86_OP_IMM = X86_OP_IMM
        self.X86_OP_MEM = X86_OP_MEM
        self.X86_REG_RIP = X86_REG_RIP
        self.raw = path.read_bytes()
        self.sections: list[tuple[str, int, int, int, int]] = []
        self.relocation_symbols: dict[int, str] = {}
        self.fdes: list[tuple[int, int]] = []
        with path.open("rb") as fh:
            elf = ELFFile(fh)
            for sec in elf.iter_sections():
                size = int(sec["sh_size"])
                if size:
                    self.sections.append(
                        (sec.name, int(sec["sh_offset"]), size, int(sec["sh_addr"]), int(sec["sh_flags"]))
                    )
                if isinstance(sec, RelocationSection):
                    symtab = elf.get_section(int(sec["sh_link"]))
                    for rel in sec.iter_relocations():
                        sym_index = int(rel["r_info_sym"])
                        if not sym_index or symtab is None:
                            continue
                        symbol = symtab.get_symbol(sym_index)
                        if symbol is not None and symbol.name:
                            self.relocation_symbols[int(rel["r_offset"])] = symbol.name
            dwarf = elf.get_dwarf_info()
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

    def section_for_va(self, va: int) -> tuple[str, int, int, int, int] | None:
        for row in self.sections:
            _, _, size, start, _ = row
            if start <= va < start + size:
                return row
        return None

    def va_to_off(self, va: int) -> int:
        row = self.section_for_va(va)
        if row is None:
            raise ValueError(hex(va))
        _, off, _, start, _ = row
        return off + va - start

    def mapped(self, va: int, size: int = 1) -> bool:
        row = self.section_for_va(va)
        if row is None:
            return False
        _, off, sec_size, start, _ = row
        delta = va - start
        return 0 <= delta <= sec_size - size and 0 <= off + delta <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        row = self.section_for_va(va)
        return bool(row and (row[4] & 4))

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def fde(self, va: int) -> tuple[int, int] | None:
        rows = [row for row in self.fdes if row[0] <= va < row[1]]
        return rows[0] if len(rows) == 1 else None

    def instructions(self, start: int, end: int):
        if start >= end or not self.mapped(start, end - start):
            return []
        return list(self.md.disasm(self.bytes(start, end - start), start))


def rip_target(img: Image, ins) -> int | None:
    for op in ins.operands:
        if op.type == img.X86_OP_MEM and op.mem.base == img.X86_REG_RIP:
            return ins.address + ins.size + int(op.mem.disp)
    return None


def direct_call_target(img: Image, ins) -> int | None:
    if ins.mnemonic != "call" or not ins.operands:
        return None
    op = ins.operands[0]
    if op.type != img.X86_OP_IMM:
        return None
    value = int(op.imm)
    return value if img.executable(value) else None


def resolve_plt_stub(img: Image, target: int) -> dict:
    section = img.section_for_va(target)
    section_name = section[0] if section else None
    insns = img.instructions(target, min(target + 0x20, section[3] + section[2] if section else target + 0x20))
    got_slot = None
    for ins in insns[:4]:
        if ins.mnemonic in ("jmp", "call"):
            candidate = rip_target(img, ins)
            if candidate is not None:
                got_slot = candidate
                break
    mangled = img.relocation_symbols.get(got_slot) if got_slot is not None else None
    demangled = demangle_symbol(mangled)
    return {
        "target": hx(target),
        "section": section_name,
        "got_slot": hx(got_slot),
        "relocation_symbol": mangled,
        "demangled_symbol": demangled,
        "instructions": [
            {"site": hx(ins.address), "mnemonic": ins.mnemonic, "op_str": ins.op_str}
            for ins in insns[:4]
        ],
    }


def peer_body(img: Image) -> dict:
    fde = img.fde(PEER_TARGET)
    if fde is None:
        return {"classification": "UNKNOWN_PEER_FDE"}
    insns = img.instructions(*fde)
    calls = [
        {"site": hx(ins.address), "target": hx(target)}
        for ins in insns
        if (target := direct_call_target(img, ins)) is not None
    ]
    return {
        "classification": "EXACT_PEER_FDE",
        "fde": [hx(fde[0]), hx(fde[1])],
        "instruction_count": len(insns),
        "direct_calls": calls,
        "instructions": [
            {
                "site": hx(ins.address),
                "mnemonic": ins.mnemonic,
                "op_str": ins.op_str,
                "rip_target": hx(rip_target(img, ins)),
            }
            for ins in insns
        ],
    }


def connection_helper_call_guard(img: Image) -> dict:
    insns = img.instructions(*CONNECTION_OWNER_FDE)
    helper_indexes = [
        i for i, ins in enumerate(insns)
        if direct_call_target(img, ins) == HELPER_TARGET
    ]
    if len(helper_indexes) != 1:
        return {"classification": "UNKNOWN_HELPER_CALL_COUNT", "count": len(helper_indexes)}
    idx = helper_indexes[0]
    window = insns[max(0, idx - 18) : idx + 1]
    return {
        "classification": "BOUNDED_PRE_HELPER_CALL_WINDOW",
        "helper_call_site": hx(insns[idx].address),
        "instructions": [
            {
                "site": hx(ins.address),
                "mnemonic": ins.mnemonic,
                "op_str": ins.op_str,
                "rip_target": hx(rip_target(img, ins)),
            }
            for ins in window
        ],
    }


def analyze(client: Path, output: Path) -> dict:
    raw = client.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        raise RuntimeError(f"EXACT_CURRENT_CLIENT_FENCE_MISMATCH:size={len(raw)} sha256={actual_sha}")

    img = Image(client)
    peer = peer_body(img)
    peer_call_targets = [row["target"] for row in peer.get("direct_calls", [])]
    if peer_call_targets != [hx(PEER_DIRECT_CALLEE)]:
        raise RuntimeError(f"PEER_DIRECT_CALL_SHAPE_MOVED:{peer_call_targets!r}")

    peer_callee = resolve_plt_stub(img, PEER_DIRECT_CALLEE)
    helper = resolve_plt_stub(img, HELPER_TARGET)
    guard = connection_helper_call_guard(img)

    peer_symbol = peer_callee.get("demangled_symbol")
    helper_symbol = helper.get("demangled_symbol")
    peer_is_signal = is_qmeta_activate_symbol(peer_symbol)
    helper_is_connect_impl = is_qobject_connect_impl_symbol(helper_symbol)

    if peer_is_signal:
        peer_role = "QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE"
        first_missing = "PEER_CLASS_OWNER_NOT_RECOVERED_FROM_EXACT_CURRENT_STATIC_EVIDENCE"
    else:
        peer_role = "UNKNOWN"
        first_missing = "PEER_EVENT_ROLE_NOT_PROVEN_BY_EXACT_PLT_SYMBOL"

    helper_role = "QT_QOBJECT_CONNECT_IMPL" if helper_is_connect_impl else (helper_symbol or "UNKNOWN")
    if helper_symbol and "operator new(" in helper_symbol:
        helper_role = "ALLOCATOR_OPERATOR_NEW"
        first_missing = "PROMOTED_HELPER_TARGET_IS_ALLOCATOR_NOT_A_CONNECTION_PRIMITIVE"

    result = {
        "schema": "otclient.track-a.be4f48-sendlogin-sender-peer.plt-v1",
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
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        },
        "peer_target": hx(PEER_TARGET),
        "peer_direct_callee_target": hx(PEER_DIRECT_CALLEE),
        "connection_helper_target": hx(HELPER_TARGET),
        "sendlogin_adapter_target": hx(ADAPTER_TARGET),
        "peer_body": peer,
        "peer_direct_callee_plt": peer_callee,
        "connection_helper_plt": helper,
        "connection_helper_call_guard": guard,
        "peer_owner_identity": "UNKNOWN",
        "peer_role": peer_role,
        "helper_role": helper_role,
        "sender_endpoint_identity": "UNKNOWN",
        "receiver_endpoint_identity": "UNKNOWN",
        "sendlogin_causal_binding_proven": False,
        "pre_login_sequence_advanced": False,
        "terminal_result": "SOURCE_BLOCKER",
        "first_missing_boundary": first_missing,
        "classification_boundary": (
            "ONE EVIDENCE-DERIVED FOLLOW-UP ONLY: RESOLVE THE TWO ALREADY-OBSERVED PLT TARGETS. "
            "NO NEW CALL GRAPH, RUNTIME, FINAL-WRITER, OR TRACK-B SEARCH IS PERMITTED."
        ),
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
    print("BE4F48_SENDLOGIN_SENDER_PEER_PLT_DISCRIMINATOR=PASS")
    print("PEER_ROLE=" + str(result["peer_role"]))
    print("HELPER_ROLE=" + str(result["helper_role"]))
    print("TERMINAL_RESULT=" + str(result["terminal_result"]))
    print("FIRST_MISSING_BOUNDARY=" + str(result["first_missing_boundary"]))


if __name__ == "__main__":
    main()
