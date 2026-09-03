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
QUEUE_VSLOT_68 = 0xBD24A0
PACKET_PROCESSOR_VSLOT_68 = 0xF4ECA0
FINAL_FRAME_FDE = (0xF4EDD0, 0xF4EF15)
ALLOCATION_HELPER = 0x4D8670


def hx(value: int) -> str:
    return f"0x{value:x}"


def signed64(value: int) -> int:
    value &= 0xFFFFFFFFFFFFFFFF
    return value - (1 << 64) if value & (1 << 63) else value


def is_plausible_offset_to_top(value: int) -> bool:
    return -(1 << 20) < value < (1 << 20)


def parse_itanium_nested_name(value: str) -> str | None:
    """Decode only the simple N<len><component>...E form used by current RTTI.

    This is intentionally not a general C++ demangler. Templates, substitutions and
    qualifiers return None rather than being guessed.
    """
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


@dataclass(frozen=True)
class Section:
    name: str
    offset: int
    size: int
    va: int
    flags: int


class Image:
    """Minimal ELF image view; third-party imports stay lazy for RED/GREEN tests."""

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
                    s.name,
                    int(s["sh_offset"]),
                    int(s["sh_size"]),
                    int(s["sh_addr"]),
                    int(s["sh_flags"]),
                )
                for s in elf.iter_sections()
                if int(s["sh_size"]) > 0
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

    def u64(self, va: int) -> int:
        return struct.unpack_from("<Q", self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        if va in self.relocations:
            return int(self.relocations[va]) & 0xFFFFFFFFFFFFFFFF
        return self.u64(va)

    def cstring(self, va: int, max_len: int = 1024) -> str:
        off = self.va_to_off(va)
        end = self.raw.find(b"\0", off, min(len(self.raw), off + max_len))
        if end < 0:
            raise ValueError(f"unterminated string at {hx(va)}")
        return self.raw[off:end].decode("ascii", "strict")

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        matches = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return matches[0] if len(matches) == 1 else None

    def fde_instructions(self, target: int):
        bounds = self.containing_fde(target)
        if bounds is None:
            raise RuntimeError(f"no unique FDE for {hx(target)}")
        lo, hi = bounds
        return bounds, list(self.md.disasm(self.bytes(lo, hi - lo), lo))


def insn_record(ins: Any) -> dict[str, Any]:
    return {"at": hx(int(ins.address)), "mnemonic": ins.mnemonic, "operand": ins.op_str}


def context(insns: list[Any], address: int, before: int = 5, after: int = 5) -> list[dict[str, Any]]:
    indexes = [i for i, row in enumerate(insns) if int(row.address) == address]
    if len(indexes) != 1:
        return []
    i = indexes[0]
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
        raise RuntimeError(f"no source operand at {hx(int(ins.address))}")
    op = ins.operands[1]
    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
        raise RuntimeError(f"not RIP-relative at {hx(int(ins.address))}")
    return int(ins.address) + int(ins.size) + int(op.mem.disp)


def decode_vtable(img: Image, address_point: int, slot_limit: int = 0xC0) -> dict[str, Any]:
    if not img.mapped(address_point - 16, 24):
        raise RuntimeError(f"unmapped vtable address point {hx(address_point)}")
    offset_to_top = signed64(img.qword(address_point - 16))
    if not is_plausible_offset_to_top(offset_to_top):
        raise RuntimeError(f"implausible offset-to-top {offset_to_top} at {hx(address_point)}")
    rtti = img.qword(address_point - 8)
    if not img.mapped(rtti + 8, 8):
        raise RuntimeError(f"unmapped RTTI {hx(rtti)}")
    name_va = img.qword(rtti + 8)
    mangled = img.cstring(name_va)
    decoded = parse_itanium_nested_name(mangled)
    slots: list[dict[str, Any]] = []
    for off in range(0, slot_limit, 8):
        if not img.mapped(address_point + off, 8):
            break
        target = img.qword(address_point + off)
        slots.append(
            {
                "offset": hx(off),
                "target": hx(target),
                "executable": img.executable(target),
            }
        )
    return {
        "address_point": hx(address_point),
        "offset_to_top": offset_to_top,
        "rtti": hx(rtti),
        "rtti_name_va": hx(name_va),
        "rtti_mangled": mangled,
        "rtti_decoded": decoded or "UNKNOWN",
        "slots": slots,
    }


def direct_call_target(ins: Any) -> int | None:
    from capstone.x86_const import X86_OP_IMM

    if ins.mnemonic != "call" or not ins.operands or ins.operands[0].type != X86_OP_IMM:
        return None
    return int(ins.operands[0].imm)


def memory_displacements(insns: list[Any]) -> list[dict[str, Any]]:
    from capstone.x86_const import X86_OP_MEM

    rows: list[dict[str, Any]] = []
    for ins in insns:
        for op in ins.operands:
            if op.type != X86_OP_MEM:
                continue
            rows.append(
                {
                    "at": hx(int(ins.address)),
                    "mnemonic": ins.mnemonic,
                    "base": img_reg_name(ins, int(op.mem.base)),
                    "index": img_reg_name(ins, int(op.mem.index)),
                    "scale": int(op.mem.scale),
                    "disp": int(op.mem.disp),
                    "disp_hex": hx(int(op.mem.disp) & 0xFFFFFFFFFFFFFFFF),
                }
            )
    return rows


def img_reg_name(ins: Any, reg: int) -> str:
    return ins.reg_name(reg) if reg else ""


def indirect_call_rows(insns: list[Any]) -> list[dict[str, Any]]:
    from capstone.x86_const import X86_OP_IMM, X86_OP_MEM

    out: list[dict[str, Any]] = []
    for ins in insns:
        if ins.mnemonic != "call" or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type == X86_OP_IMM:
            continue
        row: dict[str, Any] = {
            "at": hx(int(ins.address)),
            "operand": ins.op_str,
            "context": context(insns, int(ins.address), before=5, after=3),
        }
        if op.type == X86_OP_MEM:
            row.update(
                {
                    "mode": "indirect_mem",
                    "base": img_reg_name(ins, int(op.mem.base)),
                    "disp": int(op.mem.disp),
                    "disp_hex": hx(int(op.mem.disp) & 0xFFFFFFFFFFFFFFFF),
                }
            )
        else:
            row.update({"mode": "indirect_reg", "reg": img_reg_name(ins, int(op.reg))})
        out.append(row)
    return out


def direct_calls(insns: list[Any]) -> list[dict[str, Any]]:
    out = []
    for ins in insns:
        target = direct_call_target(ins)
        if target is not None:
            out.append({"at": hx(int(ins.address)), "target": hx(target)})
    return out


def prove_adapter(img: Image) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(ADAPTER_FDE[0])
    if bounds != ADAPTER_FDE:
        raise RuntimeError(f"adapter FDE moved: {tuple(map(hx, bounds))}")

    exact_instruction(insns, 0xBD3070, "call", "0x4d8670")
    exact_instruction(insns, 0xBD3087, "mov", "rbx, rax")
    exact_instruction(insns, 0xBD3099, "lea", "r15, [rbx + 0x10]")
    object_vtable_lea = exact_instruction(insns, 0xBD30AF, "lea", "rax, [rip + 0x23c622a]")
    exact_instruction(insns, 0xBD30B6, "mov", "qword ptr [rbx + 0x10], rax")
    exact_instruction(insns, 0xBD31B4, "mov", "rax, qword ptr [r12]")
    exact_instruction(insns, 0xBD31B8, "mov", "rax, qword ptr [rax + 0x68]")
    exact_instruction(insns, 0xBD31BC, "mov", "qword ptr [rsp], r15")
    exact_instruction(insns, 0xBD31C0, "mov", "qword ptr [rsp + 8], rbx")
    exact_instruction(insns, 0xBD31DE, "mov", "rsi, rsp")
    exact_instruction(insns, 0xBD31E1, "mov", "rdi, r12")
    exact_instruction(insns, 0xBD31E4, "call", "rax")

    object_vtable_ap = rip_target(object_vtable_lea)
    queue_vtable = decode_vtable(img, QUEUE_VTABLE_AP)
    queue_slot = next((row for row in queue_vtable["slots"] if row["offset"] == "0x68"), None)
    if not queue_slot or queue_slot["target"] != hx(QUEUE_VSLOT_68) or not queue_slot["executable"]:
        raise RuntimeError("TProtocolMessageQueue +0x68 no longer resolves to expected exact-current target")
    if queue_vtable["rtti_decoded"] != "tibia::protocol::TProtocolMessageQueue":
        raise RuntimeError(f"queue RTTI mismatch: {queue_vtable['rtti_decoded']}")

    object_vtable = decode_vtable(img, object_vtable_ap)
    return {
        "adapter_fde": [hx(bounds[0]), hx(bounds[1])],
        "allocation_helper": hx(ALLOCATION_HELPER),
        "allocation_return_owner_register": "rbx",
        "queued_object_pointer_expression": "allocation+0x10",
        "queue_item_layout": [
            {"offset": 0, "value": "allocation+0x10 (queued object pointer)"},
            {"offset": 8, "value": "allocation (shared ownership/control pointer)"},
        ],
        "queue_call": {
            "at": "0xbd31e4",
            "this": "r12",
            "argument": "rsp -> exact 16-byte pair",
            "resolved_vslot_offset": "0x68",
            "resolved_target": hx(QUEUE_VSLOT_68),
            "context": context(insns, 0xBD31E4, before=11, after=4),
        },
        "queue_vtable": queue_vtable,
        "queued_object_vtable": object_vtable,
        "queued_object_vtable_store": {
            "lea_at": "0xbd30af",
            "store_at": "0xbd30b6",
            "address_point": hx(object_vtable_ap),
        },
    }


def prove_queue_insert(img: Image) -> dict[str, Any]:
    bounds, insns = img.fde_instructions(QUEUE_VSLOT_68)
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
        "target": hx(QUEUE_VSLOT_68),
        "fde": [hx(bounds[0]), hx(bounds[1])],
        "source_pair": "rsi -> 16-byte pair supplied by adapter",
        "queue_begin_or_end_members": ["this+0x90", "this+0xa0"],
        "copy_width": 16,
        "advance": 16,
        "proof_context": [
            insn_record(one_at(insns, address)) for address, _, _ in required
        ],
        "proven": True,
    }


def queue_vslot_summaries(img: Image, queue_vtable: dict[str, Any]) -> list[dict[str, Any]]:
    """Inspect only executable vslots of the already-proven queue vtable.

    No unrelated code/global writer scan is performed. A consumer candidate must
    touch both exact queue members used by insertion and contain an indirect call.
    """
    summaries: list[dict[str, Any]] = []
    seen: set[int] = set()
    for slot in queue_vtable["slots"]:
        if not slot["executable"]:
            continue
        target = int(slot["target"], 16)
        if target in seen:
            continue
        seen.add(target)
        bounds = img.containing_fde(target)
        if bounds is None:
            summaries.append(
                {
                    "slot_offset": slot["offset"],
                    "target": slot["target"],
                    "fde": None,
                    "queue_member_accesses": [],
                    "indirect_calls": [],
                    "consumer_candidate": False,
                }
            )
            continue
        _, insns = img.fde_instructions(target)
        mem = memory_displacements(insns)
        member_hits = [row for row in mem if row["disp"] in {0x90, 0xA0}]
        hit_disps = {row["disp"] for row in member_hits}
        icalls = indirect_call_rows(insns)
        candidate = target != QUEUE_VSLOT_68 and hit_disps == {0x90, 0xA0} and bool(icalls)
        summaries.append(
            {
                "slot_offset": slot["offset"],
                "target": slot["target"],
                "fde": [hx(bounds[0]), hx(bounds[1])],
                "queue_member_accesses": member_hits[:40],
                "indirect_calls": icalls[:20],
                "direct_calls": direct_calls(insns)[:40],
                "consumer_candidate": candidate,
            }
        )
    return summaries


def bounded_follow_up(img: Image, adapter: dict[str, Any], queue_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = [row for row in queue_summaries if row["consumer_candidate"]]
    result: dict[str, Any] = {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "unique_consumer": None,
        "queued_object_virtual_target": None,
        "reaches_packet_processor_plus_0x68": False,
        "reaches_final_frame_fde": False,
    }
    if len(candidates) != 1:
        return result

    consumer = candidates[0]
    result["unique_consumer"] = {
        "slot_offset": consumer["slot_offset"],
        "target": consumer["target"],
        "fde": consumer["fde"],
    }

    # A writer target may be resolved only when the consumer itself exposes one
    # unambiguous virtual slot. Multiple indirect calls remain scientific UNKNOWN.
    indirect = consumer["indirect_calls"]
    mem_slots = [
        row
        for row in indirect
        if row.get("mode") == "indirect_mem" and 0 <= int(row.get("disp", -1)) <= 0xB8
    ]
    unique_offsets = sorted({int(row["disp"]) for row in mem_slots})
    if len(unique_offsets) != 1:
        return result

    slot_off = unique_offsets[0]
    object_vtable = adapter["queued_object_vtable"]
    object_slot = next((row for row in object_vtable["slots"] if row["offset"] == hx(slot_off)), None)
    if not object_slot or not object_slot["executable"]:
        return result
    target = int(object_slot["target"], 16)
    result["queued_object_virtual_target"] = {
        "slot_offset": hx(slot_off),
        "target": hx(target),
        "object_rtti": object_vtable["rtti_decoded"],
    }

    bounds = img.containing_fde(target)
    if bounds is None:
        return result
    _, writer_insns = img.fde_instructions(target)
    direct = {int(row["target"], 16) for row in direct_calls(writer_insns)}
    result["queued_object_virtual_target"]["fde"] = [hx(bounds[0]), hx(bounds[1])]
    result["queued_object_virtual_target"]["direct_calls"] = [
        {"at": row["at"], "target": row["target"]} for row in direct_calls(writer_insns)[:60]
    ]
    result["queued_object_virtual_target"]["indirect_calls"] = indirect_call_rows(writer_insns)[:30]
    result["reaches_packet_processor_plus_0x68"] = PACKET_PROCESSOR_VSLOT_68 in direct
    result["reaches_final_frame_fde"] = FINAL_FRAME_FDE[0] in direct
    return result


def classify(adapter: dict[str, Any], queue_insert: dict[str, Any], follow: dict[str, Any]) -> dict[str, Any]:
    queue_identity = (
        f"16-byte pair {{object={adapter['queued_object_pointer_expression']}, "
        "owner=allocation}} copied unchanged into TProtocolMessageQueue storage"
    )

    if follow["candidate_count"] != 1:
        return {
            "serialized_queue_object_identity": queue_identity,
            "final_queue_writer_identified": False,
            "final_queue_writer_identity": "UNKNOWN",
            "final_tcp_writer_identified": False,
            "final_tcp_writer_identity": "UNKNOWN",
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": (
                "queued 16-byte sendLogin item -> unique TProtocolMessageQueue drain/consumer "
                f"(bounded vtable candidates={follow['candidate_count']})"
            ),
            "next_action": (
                "use the emitted queue-vslot-local evidence for at most one narrow discriminator; "
                "do not broaden to a global writer/socket sweep"
            ),
        }

    if follow["queued_object_virtual_target"] is None:
        consumer = follow["unique_consumer"]
        return {
            "serialized_queue_object_identity": queue_identity,
            "final_queue_writer_identified": False,
            "final_queue_writer_identity": "UNKNOWN",
            "final_tcp_writer_identified": False,
            "final_tcp_writer_identity": "UNKNOWN",
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": (
                f"unique queue consumer {consumer['target']} -> unique queued-object writer vslot"
            ),
            "next_action": (
                "use the emitted consumer call contexts for at most one local object-provenance discriminator"
            ),
        }

    writer = follow["queued_object_virtual_target"]
    if not (follow["reaches_packet_processor_plus_0x68"] or follow["reaches_final_frame_fde"]):
        return {
            "serialized_queue_object_identity": queue_identity,
            "final_queue_writer_identified": True,
            "final_queue_writer_identity": (
                f"{writer['object_rtti']} vslot {writer['slot_offset']} -> {writer['target']}"
            ),
            "final_tcp_writer_identified": False,
            "final_tcp_writer_identity": "UNKNOWN",
            "final_writer_contract": "UNKNOWN",
            "terminal_result": "SOURCE_BLOCKER",
            "FIRST_MISSING_BOUNDARY": (
                f"queued-object writer {writer['target']} -> current packet/frame/TCP egress"
            ),
            "next_action": (
                "inspect only the emitted writer-local calls for one object-provenance edge; no global TCP sweep"
            ),
        }

    # Reaching one known downstream address directly is still not sufficient to claim
    # final TCP ownership. The positive state is deliberately unreachable until a
    # second independent object/ownership check is implemented from emitted evidence.
    return {
        "serialized_queue_object_identity": queue_identity,
        "final_queue_writer_identified": True,
        "final_queue_writer_identity": (
            f"{writer['object_rtti']} vslot {writer['slot_offset']} -> {writer['target']}"
        ),
        "final_tcp_writer_identified": False,
        "final_tcp_writer_identity": "UNKNOWN",
        "final_writer_contract": "UNKNOWN",
        "terminal_result": "SOURCE_BLOCKER",
        "FIRST_MISSING_BOUNDARY": (
            "known downstream packet/frame candidate reached -> independently cross-checked final TCP writer ownership"
        ),
        "next_action": "add at most one independent local ownership cross-check from this exact reached node",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    actual_size = args.client.stat().st_size
    actual_sha = hashlib.sha256(args.client.read_bytes()).hexdigest()
    if args.version != EXPECTED_VERSION:
        raise SystemExit(f"version mismatch: {args.version} != {EXPECTED_VERSION}")
    if args.size != EXPECTED_SIZE or actual_size != EXPECTED_SIZE:
        raise SystemExit(f"size mismatch: arg={args.size} actual={actual_size} expected={EXPECTED_SIZE}")
    if args.sha256.lower() != EXPECTED_SHA256 or actual_sha != EXPECTED_SHA256:
        raise SystemExit("SHA-256 mismatch for exact-current client")

    img = Image(args.client)
    adapter = prove_adapter(img)
    queue_insert = prove_queue_insert(img)
    queue_summaries = queue_vslot_summaries(img, adapter["queue_vtable"])
    follow = bounded_follow_up(img, adapter, queue_summaries)
    terminal = classify(adapter, queue_insert, follow)

    result: dict[str, Any] = {
        "schema": "otclient.track-a.be4f48-final-login-writer.source.v1",
        "exact_client": {
            "version": EXPECTED_VERSION,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
            "fence_proven": True,
        },
        "sendlogin_adapter_identified": True,
        "analysis": {
            "adapter": adapter,
            "queue_insert": queue_insert,
            "queue_vslot_summaries": queue_summaries,
            "bounded_follow_up": follow,
            "known_downstream_seeds_not_promoted_without_causal_reach": {
                "packet_processor_plus_0x68": hx(PACKET_PROCESSOR_VSLOT_68),
                "final_frame_fde": [hx(FINAL_FRAME_FDE[0]), hx(FINAL_FRAME_FDE[1])],
            },
        },
        **terminal,
        "field6_value": "UNKNOWN",
        "runtime_access": "none",
        "official_client_execution": False,
        "login_performed": False,
        "credential_access": False,
        "process_memory_access": False,
        "packet_capture": False,
        "official_service_e2e_count": 0,
        "raw_client_uploaded": False,
        "track_b_pr_284_modified": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("BE4F48_FINAL_LOGIN_WRITER_ANALYSIS=PASS")
    print("TERMINAL_RESULT=" + result["terminal_result"])
    print("FIRST_MISSING_BOUNDARY=" + result["FIRST_MISSING_BOUNDARY"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
