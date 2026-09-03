#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

ADAPTER_FDE = (0xBD3050, 0xBD34DD)
QUEUE_VTABLE_AP = 0x30ED588
QUEUE_INSERT = 0xBD24A0
DRAIN_FDE = (0xBD2190, 0xBD2495)

ALLOCATION_HELPER = 0x4D8670
QMETAOBJECT_ACTIVATE = 0x4D7DC0
DRAIN_STATIC_METAOBJECT = 0x30B73E0
DRAIN_SIGNAL_INDEX = 0xBF

UNKNOWN = frozenset()
OBJECT = frozenset({"object"})
OWNER = frozenset({"owner"})
PAIR = frozenset({"object", "owner"})


def hx(value: int) -> str:
    return f"0x{value:x}"


def signed64(value: int) -> int:
    value &= 0xFFFFFFFFFFFFFFFF
    return value - (1 << 64) if value & (1 << 63) else value


def parse_itanium_nested_name(value: str) -> str | None:
    if not value.startswith("N") or not value.endswith("E"):
        return None
    i = 1
    end = len(value) - 1
    parts: list[str] = []
    while i < end:
        j = i
        while j < end and value[j].isdigit():
            j += 1
        if j == i:
            return None
        length = int(value[i:j])
        if length <= 0 or j + length > end:
            return None
        part = value[j : j + length]
        if not part or not all(ch.isalnum() or ch == "_" for ch in part):
            return None
        parts.append(part)
        i = j + length
    return "::".join(parts) if parts and i == end else None


def join_identity(left: frozenset[str], right: frozenset[str]) -> frozenset[str]:
    """Keep identity only when two control-flow facts agree exactly."""
    if not left or not right:
        return UNKNOWN
    return left if left == right else UNKNOWN


def classify_terminal(
    *,
    serialized_identity_proven: bool,
    causal_consumption: bool,
    next_writer_candidate: int | None,
    next_writer_crosscheck: bool,
    first_missing_boundary: str,
) -> dict[str, Any]:
    if not serialized_identity_proven:
        return {
            "queued_gameclientmessage_causal_consumption": False,
            "next_unique_writer_edge": "UNKNOWN",
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": first_missing_boundary,
        }

    if not causal_consumption:
        return {
            "queued_gameclientmessage_causal_consumption": False,
            "next_unique_writer_edge": "UNKNOWN",
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": first_missing_boundary,
        }

    if next_writer_candidate is None or not next_writer_crosscheck:
        return {
            "queued_gameclientmessage_causal_consumption": True,
            "next_unique_writer_edge": "UNKNOWN",
            "final_queue_writer_identified": False,
            "final_tcp_writer_identified": False,
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "QUEUE_DRAIN_CONSUMPTION_PROVEN",
            "FIRST_MISSING_BOUNDARY": first_missing_boundary,
        }

    return {
        "queued_gameclientmessage_causal_consumption": True,
        "next_unique_writer_edge": hx(next_writer_candidate),
        "final_queue_writer_identified": True,
        "final_tcp_writer_identified": False,
        "final_writer_contract": "UNKNOWN",
        "terminal_result": "FINAL_QUEUE_WRITER_PROVEN",
        "FIRST_MISSING_BOUNDARY": first_missing_boundary,
    }


@dataclass(frozen=True)
class Section:
    offset: int
    size: int
    va: int
    flags: int


class Image:
    """Minimal exact-ELF view for fixed local FDEs; no global call-graph search."""

    def __init__(self, path: Path):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from elftools.dwarf.callframe import FDE
        from elftools.elf.elffile import ELFFile
        from elftools.elf.relocation import RelocationSection

        self.path = path
        self.raw = path.read_bytes()
        with path.open("rb") as fh:
            elf = ELFFile(fh)
            self.sections = [
                Section(
                    int(sec["sh_offset"]),
                    int(sec["sh_size"]),
                    int(sec["sh_addr"]),
                    int(sec["sh_flags"]),
                )
                for sec in elf.iter_sections()
                if int(sec["sh_size"]) > 0
            ]
            self.relocations: dict[int, int] = {}
            for sec in elf.iter_sections():
                if not isinstance(sec, RelocationSection):
                    continue
                for rel in sec.iter_relocations():
                    if rel.is_RELA():
                        self.relocations[int(rel["r_offset"])] = int(rel["r_addend"])
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

    def va_to_off(self, va: int) -> int:
        for sec in self.sections:
            if sec.va <= va < sec.va + sec.size:
                return sec.offset + (va - sec.va)
        raise ValueError(f"unmapped VA {hx(va)}")

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((sec.flags & 4) and sec.va <= va < sec.va + sec.size for sec in self.sections)

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off : off + size]

    def qword(self, va: int) -> int:
        if va in self.relocations:
            return int(self.relocations[va]) & 0xFFFFFFFFFFFFFFFF
        return struct.unpack_from("<Q", self.raw, self.va_to_off(va))[0]

    def cstring(self, va: int, max_len: int = 1024) -> str:
        off = self.va_to_off(va)
        end = self.raw.find(b"\0", off, min(len(self.raw), off + max_len))
        if end < 0:
            raise RuntimeError(f"unterminated string at {hx(va)}")
        return self.raw[off:end].decode("ascii", "strict")

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def fde_instructions(self, target: int) -> tuple[tuple[int, int], list[Any]]:
        bounds = self.containing_fde(target)
        if bounds is None:
            raise RuntimeError(f"no unique FDE for {hx(target)}")
        lo, hi = bounds
        return bounds, list(self.md.disasm(self.bytes(lo, hi - lo), lo))


def insn_record(ins: Any) -> dict[str, Any]:
    return {"at": hx(int(ins.address)), "mnemonic": ins.mnemonic, "operand": ins.op_str}


def context(insns: list[Any], address: int, before: int = 4, after: int = 4) -> list[dict[str, Any]]:
    idx = [i for i, row in enumerate(insns) if int(row.address) == address]
    if len(idx) != 1:
        return []
    i = idx[0]
    return [insn_record(row) for row in insns[max(0, i - before) : i + after + 1]]


def one_at(insns: list[Any], address: int) -> Any:
    rows = [row for row in insns if int(row.address) == address]
    if len(rows) != 1:
        raise RuntimeError(f"expected one instruction at {hx(address)}, got {len(rows)}")
    return rows[0]


def exact_instruction(insns: list[Any], address: int, mnemonic: str, operand: str) -> Any:
    row = one_at(insns, address)
    if row.mnemonic != mnemonic or row.op_str != operand:
        raise RuntimeError(
            f"instruction mismatch at {hx(address)}: expected {mnemonic} {operand!r}, "
            f"got {row.mnemonic} {row.op_str!r}"
        )
    return row


def rip_target(ins: Any) -> int:
    from capstone.x86_const import X86_OP_MEM, X86_REG_RIP

    if len(ins.operands) < 2:
        raise RuntimeError(f"no RIP-relative source operand at {hx(int(ins.address))}")
    op = ins.operands[1]
    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
        raise RuntimeError(f"not RIP-relative at {hx(int(ins.address))}")
    return int(ins.address) + int(ins.size) + int(op.mem.disp)


def decode_vtable(img: Image, address_point: int, slot_limit: int = 0xC0) -> dict[str, Any]:
    if not img.mapped(address_point - 16, 24):
        raise RuntimeError(f"unmapped vtable address point {hx(address_point)}")
    offset_to_top = signed64(img.qword(address_point - 16))
    if not -(1 << 20) < offset_to_top < (1 << 20):
        raise RuntimeError(f"implausible vtable offset-to-top at {hx(address_point)}")
    rtti = img.qword(address_point - 8)
    if not img.mapped(rtti + 8, 8):
        raise RuntimeError(f"unmapped RTTI at {hx(rtti)}")
    name_va = img.qword(rtti + 8)
    mangled = img.cstring(name_va)
    decoded = parse_itanium_nested_name(mangled)
    slots: list[dict[str, Any]] = []
    for off in range(0, slot_limit, 8):
        if not img.mapped(address_point + off, 8):
            break
        target = img.qword(address_point + off)
        slots.append({"offset": hx(off), "target": hx(target), "executable": img.executable(target)})
    return {
        "address_point": hx(address_point),
        "offset_to_top": offset_to_top,
        "rtti": hx(rtti),
        "rtti_mangled": mangled,
        "rtti_decoded": decoded or "UNKNOWN",
        "slots": slots,
    }


def prove_serialized_queue_identity(img: Image) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(ADAPTER_FDE[0])
    if bounds != ADAPTER_FDE:
        raise RuntimeError(f"adapter FDE moved: {tuple(map(hx, bounds))}")

    required = [
        (0xBD3070, "call", "0x4d8670"),
        (0xBD3087, "mov", "rbx, rax"),
        (0xBD3099, "lea", "r15, [rbx + 0x10]"),
        (0xBD30B6, "mov", "qword ptr [rbx + 0x10], rax"),
        (0xBD31B4, "mov", "rax, qword ptr [r12]"),
        (0xBD31B8, "mov", "rax, qword ptr [rax + 0x68]"),
        (0xBD31BC, "mov", "qword ptr [rsp], r15"),
        (0xBD31C0, "mov", "qword ptr [rsp + 8], rbx"),
        (0xBD31DE, "mov", "rsi, rsp"),
        (0xBD31E1, "mov", "rdi, r12"),
        (0xBD31E4, "call", "rax"),
    ]
    for address, mnemonic, operand in required:
        exact_instruction(insns, address, mnemonic, operand)

    object_vtable_lea = exact_instruction(
        insns, 0xBD30AF, "lea", "rax, [rip + 0x23c622a]"
    )
    object_vtable_ap = rip_target(object_vtable_lea)
    object_vtable = decode_vtable(img, object_vtable_ap)
    if object_vtable["rtti_decoded"] != "tibia::protobuf::protocol::GameclientMessage":
        raise RuntimeError(f"queued object RTTI mismatch: {object_vtable['rtti_decoded']}")

    queue_vtable = decode_vtable(img, QUEUE_VTABLE_AP)
    if queue_vtable["rtti_decoded"] != "tibia::protocol::TProtocolMessageQueue":
        raise RuntimeError(f"queue RTTI mismatch: {queue_vtable['rtti_decoded']}")
    slot = next((row for row in queue_vtable["slots"] if row["offset"] == "0x68"), None)
    if slot is None or slot["target"] != hx(QUEUE_INSERT) or not slot["executable"]:
        raise RuntimeError("queue vslot +0x68 no longer resolves to exact insertion target")

    return {
        "proven": True,
        "adapter_fde": [hx(bounds[0]), hx(bounds[1])],
        "allocation_helper": hx(ALLOCATION_HELPER),
        "queue_item_layout": [
            {"offset": 0, "identity": "object", "value": "allocation+0x10"},
            {"offset": 8, "identity": "owner", "value": "allocation"},
        ],
        "queue_item_width": 16,
        "queue_call": {
            "at": "0xbd31e4",
            "this": "r12",
            "argument": "rsp -> exact 16-byte {object,owner} pair",
            "vslot": "0x68",
            "target": hx(QUEUE_INSERT),
        },
        "queue_vtable": {
            "address_point": queue_vtable["address_point"],
            "rtti_decoded": queue_vtable["rtti_decoded"],
            "vslot_0x68": slot,
        },
        "queued_object_vtable": {
            "address_point": object_vtable["address_point"],
            "rtti_decoded": object_vtable["rtti_decoded"],
            "store_lea_at": "0xbd30af",
            "store_at": "0xbd30b6",
        },
    }


def prove_queue_insert(img: Image) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(QUEUE_INSERT)
    required = [
        (0xBD24B4, "mov", "rcx, qword ptr [rdi + 0xa0]"),
        (0xBD24BB, "mov", "rax, qword ptr [rdi + 0x90]"),
        (0xBD24CF, "movdqu", "xmm2, xmmword ptr [rsi]"),
        (0xBD24D3, "mov", "rdx, qword ptr [rsi + 8]"),
        (0xBD24D7, "movups", "xmmword ptr [rax], xmm2"),
        (0xBD24F3, "add", "rax, 0x10"),
        (0xBD24F7, "mov", "qword ptr [rbx + 0x90], rax"),
    ]
    for address, mnemonic, operand in required:
        exact_instruction(insns, address, mnemonic, operand)
    return {
        "proven": True,
        "target": hx(QUEUE_INSERT),
        "fde": [hx(bounds[0]), hx(bounds[1])],
        "incoming_pair": "rsi -> exact 16-byte {object,owner} pair",
        "storage_end_member": "this+0x90",
        "storage_capacity_member": "this+0xa0",
        "copy_width": 16,
        "advance": 16,
        "proof_context": [insn_record(one_at(insns, address)) for address, _, _ in required],
    }


def prove_drain_consumption(img: Image) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(DRAIN_FDE[0])
    if bounds != DRAIN_FDE:
        raise RuntimeError(f"owned drain FDE moved: {tuple(map(hx, bounds))}")

    required = [
        (0xBD219A, "mov", "rbx, rdi"),
        (0xBD2205, "mov", "rax, qword ptr [rdi + 0x70]"),
        (0xBD2209, "lea", "r13, [rsp + 0x10]"),
        (0xBD220E, "lea", "r12, [rsp + 0x20]"),
        (0xBD2224, "cmp", "rax, qword ptr [rdi + 0x90]"),
        (0xBD2244, "mov", "rax, qword ptr [rbx + 0x70]"),
        (0xBD224F, "mov", "r15, qword ptr [rax + 8]"),
        (0xBD229A, "mov", "rax, qword ptr [rbx + 0x70]"),
        (0xBD229E, "add", "rax, 0x10"),
        (0xBD22A2, "mov", "qword ptr [rbx + 0x70], rax"),
        (0xBD22A6, "mov", "rcx, r12"),
        (0xBD22A9, "mov", "edx, 0xbf"),
        (0xBD22AE, "mov", "rsi, rbp"),
        (0xBD22B1, "mov", "rdi, rbx"),
        (0xBD22B4, "mov", "qword ptr [rsp + 0x28], r13"),
        (0xBD22B9, "mov", "qword ptr [rsp + 0x20], 0"),
        (0xBD22C2, "call", "0x4d7dc0"),
        (0xBD22C7, "mov", "r15, qword ptr [rsp + 0x18]"),
        (0xBD2306, "mov", "rax, qword ptr [rbx + 0x70]"),
        (0xBD230A, "cmp", "qword ptr [rbx + 0x90], rax"),
        (0xBD2317, "movdqu", "xmm1, xmmword ptr [rax]"),
        (0xBD231B, "mov", "rdx, qword ptr [rax + 8]"),
        (0xBD231F, "movaps", "xmmword ptr [rsp + 0x10], xmm1"),
        (0xBD2324, "test", "rdx, rdx"),
        (0xBD233D, "lock add", "dword ptr [rdx + 8], 1"),
    ]
    for address, mnemonic, operand in required:
        exact_instruction(insns, address, mnemonic, operand)

    meta_lea = exact_instruction(insns, 0xBD221D, "lea", "rbp, [rip + 0x24e51bc]")
    meta_target = rip_target(meta_lea)
    if meta_target != DRAIN_STATIC_METAOBJECT:
        raise RuntimeError(
            f"drain static metaobject moved: {hx(meta_target)} != {hx(DRAIN_STATIC_METAOBJECT)}"
        )

    identity_events = [
        {
            "at": "0xbd2317..0xbd231f",
            "source": "queue[this+0x70] exact 16-byte element",
            "destination": "rsp+0x10 exact 16-byte copy",
            "identity": ["object", "owner"],
            "proof_kind": "single movdqu/movaps pair copy",
        },
        {
            "at": "0xbd231b..0xbd233d",
            "source": "copied pair owner qword",
            "destination": "owner control block +0x8 refcount",
            "identity": ["owner"],
            "proof_kind": "owner qword load followed by lock refcount increment",
        },
        {
            "at": "0xbd229a..0xbd22a2",
            "source": "queue begin this+0x70",
            "destination": "queue begin this+0x70",
            "identity": ["object", "owner"],
            "proof_kind": "advance exactly one 16-byte element after original-entry ownership handling",
        },
        {
            "at": "0xbd2209;0xbd22b4",
            "source": "rsp+0x10 exact copied pair",
            "destination": "argv[1] via rsp+0x28",
            "identity": ["object", "owner"],
            "proof_kind": "unique stack-address propagation r13 -> argv[1]",
        },
        {
            "at": "0xbd22c2",
            "source": "argv[1] exact copied pair",
            "destination": "QMetaObject::activate semantic dispatch",
            "identity": ["object", "owner"],
            "proof_kind": "direct call with exact sender/metaobject/signal/argv register setup",
        },
        {
            "at": "0xbd22c7",
            "source": "rsp+0x18 copied owner qword",
            "destination": "post-dispatch owner lifecycle",
            "identity": ["owner"],
            "proof_kind": "owner qword remains live across semantic dispatch",
        },
    ]

    return {
        "proven": True,
        "target": hx(DRAIN_FDE[0]),
        "fde": [hx(bounds[0]), hx(bounds[1])],
        "queue_begin_member": "this+0x70",
        "queue_end_member": "this+0x90",
        "dequeued_pair_width": 16,
        "dequeued_pair_copy": "queue[this+0x70] -> rsp+0x10",
        "queue_begin_advance": 16,
        "owner_refcount_preserved_for_copy": True,
        "identity_events": identity_events,
        "semantic_consumer": {
            "call_at": "0xbd22c2",
            "target": hx(QMETAOBJECT_ACTIVATE),
            "role": "QMetaObject::activate(QObject*, QMetaObject const*, int, void**)",
            "role_provenance": "exact target role promoted by coordinator PR #871; direct target independently re-proved here",
            "sender": "TProtocolMessageQueue this (rdi=rbx)",
            "static_metaobject": hx(meta_target),
            "signal_index": DRAIN_SIGNAL_INDEX,
            "signal_index_hex": hx(DRAIN_SIGNAL_INDEX),
            "argv": "rsp+0x20",
            "argv_0": "null",
            "argv_1": "rsp+0x10 -> exact copied 16-byte {object,owner} pair",
            "context": context(insns, 0xBD22C2, before=9, after=3),
        },
        "causal_consumption_proven": True,
        "writer_edge_search": {
            "performed": False,
            "reason": (
                "the exact identity reaches QMetaObject::activate, but this FDE contains no uniquely "
                "bound receiver/writer target; task scope forbids broad Qt connection or global writer discovery"
            ),
            "candidate": "UNKNOWN",
            "crosscheck": False,
        },
        "proof_context": [insn_record(one_at(insns, address)) for address, _, _ in required],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", type=Path, required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--size", type=int, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    actual_size = args.client.stat().st_size
    actual_sha = hashlib.sha256(args.client.read_bytes()).hexdigest()
    if args.version != EXPECTED_VERSION:
        raise SystemExit(f"version mismatch: {args.version} != {EXPECTED_VERSION}")
    if args.size != EXPECTED_SIZE or actual_size != EXPECTED_SIZE:
        raise SystemExit(
            f"size mismatch: arg={args.size} actual={actual_size} expected={EXPECTED_SIZE}"
        )
    if args.sha256.lower() != EXPECTED_SHA256 or actual_sha != EXPECTED_SHA256:
        raise SystemExit("SHA-256 mismatch for exact-current client")

    img = Image(args.client)
    identity = prove_serialized_queue_identity(img)
    insertion = prove_queue_insert(img)
    drain = prove_drain_consumption(img)

    terminal = classify_terminal(
        serialized_identity_proven=bool(identity["proven"] and insertion["proven"]),
        causal_consumption=bool(drain["causal_consumption_proven"]),
        next_writer_candidate=None,
        next_writer_crosscheck=False,
        first_missing_boundary=(
            "TProtocolMessageQueue signal 0xbf carrying the exact queued GameclientMessage "
            "shared_ptr -> unique connected receiver/writer edge"
        ),
    )

    result: dict[str, Any] = {
        "schema": "otclient.track-a.be4f48-queue-drain-consumption.source.v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "fence_proven": True,
        },
        "serialized_queue_object_identity_proven": bool(identity["proven"] and insertion["proven"]),
        "serialized_queue_object_identity": (
            "16-byte pair {object=allocation+0x10, owner=allocation} copied unchanged "
            "into TProtocolMessageQueue storage"
        ),
        "owned_drain_callback": hx(DRAIN_FDE[0]),
        "owned_drain_fde": [hx(DRAIN_FDE[0]), hx(DRAIN_FDE[1])],
        "analysis": {
            "serialized_queue_identity": identity,
            "queue_insert": insertion,
            "drain_consumption": drain,
        },
        **terminal,
        "field6_value": "UNKNOWN",
        "runtime_access": "none",
        "official_client_execution": False,
        "login_performed": False,
        "credential_access": False,
        "process_memory_access": False,
        "packet_capture": False,
        "ocr_vision_used": False,
        "official_service_e2e_count": 0,
        "raw_client_uploaded": False,
        "track_b_pr_284_modified": False,
        "next_action": (
            "persist this proved queue-drain boundary for clean coordinator promotion; "
            "do not broaden this source task into global Qt/writer discovery"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BE4F48_QUEUE_DRAIN_CONSUMPTION_ANALYSIS=PASS")
    print("TERMINAL_RESULT=" + result["terminal_result"])
    print("FIRST_MISSING_BOUNDARY=" + result["FIRST_MISSING_BOUNDARY"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
