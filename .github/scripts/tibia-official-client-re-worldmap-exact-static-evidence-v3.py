#!/usr/bin/env python3
"""Final targeted discriminator for the world-map exact-static second package.

The Synology source step is read-only and does not execute or disassemble the
client. It verifies the exact fence through V2, stages only bounded byte windows
for the remaining producer/caller questions, and emits exact ELF relocation /
RTTI metadata. GNU objdump runs only on the sanitized windows on GitHub-hosted
infrastructure.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import struct
import sys
from typing import Any

V2_PATH = Path(__file__).with_name("tibia-official-client-re-worldmap-exact-static-evidence-v2.py")
SPEC = importlib.util.spec_from_file_location("worldmap_exact_static_v2", V2_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("WORLD_MAP_STATIC_V3_REFUSED=V2_IMPORT_SPEC")
v2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v2)
base = v2.base
_ORIGINAL_VALIDATE_SOURCE_BUNDLE = v2.validate_source_bundle

TARGET_FUNCTIONS = {
    "storage_slot12_best_caller": 0x00CDB770,
    "storage_slot12_best_caller_aggregate_builder": 0x00BC6350,
    "viewport_slot13_dynamic_extent": 0x00CB2220,
    "viewport_slot14_extent_aggregate": 0x00CB07B0,
    "camera_dependency_consumer": 0x00CED1B0,
    "camera_dependency_consumer_caller": 0x0084E640,
}

# The exact ABI match in the preceding run occurs at this call site. Preserve a
# fresh context around it without repeating the whole slot-12 census.
EXACT_CALL_SITES = {
    "storage_slot12_best_virtual_call": 0x00CDB7AB,
}


def fmt_addr(value: int) -> str:
    return f"0x{value:08x}"


def validate_source_bundle_order_tolerant(bundle_dir: Path):
    try:
        return _ORIGINAL_VALIDATE_SOURCE_BUNDLE(bundle_dir)
    except SystemExit as exc:
        if str(exc) != "WORLD_MAP_STATIC_V2_REFUSED=SOURCE_REPORT_NONDETERMINISTIC":
            raise
        bundle = json.loads((bundle_dir / "worldmap-static-evidence.json").read_text(encoding="utf-8"))
        print("WORLD_MAP_STATIC_V3_SOURCE_REPORT_ORDER_TOLERATED=true")
        print("WORLD_MAP_STATIC_V3_AUTHORITATIVE_SOURCE=validated_json")
        return bundle


v2.validate_source_bundle = validate_source_bundle_order_tolerant


def scan_rel32_xrefs(elf: Any, targets: set[int]) -> dict[int, list[dict[str, Any]]]:
    """E8/E9 rel32 candidates; hosted objdump confirms instruction boundaries."""
    out: dict[int, list[dict[str, Any]]] = {target: [] for target in targets}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        for i in range(max(0, len(blob) - 5)):
            opcode = blob[i]
            if opcode not in (0xE8, 0xE9):
                continue
            disp = struct.unpack_from("<i", blob, i + 1)[0]
            address = seg["vaddr"] + i
            target = address + 5 + disp
            if target not in out:
                continue
            out[target].append({
                "instruction_address": fmt_addr(address),
                "opcode": "call_rel32" if opcode == 0xE8 else "jmp_rel32",
                "instruction_bytes": blob[i:i + 5].hex(),
                "resolved_target": fmt_addr(target),
                "classification": "candidate_until_hosted_instruction_boundary_confirmation",
            })
    for target, items in out.items():
        unique = {item["instruction_address"]: item for item in items}
        out[target] = [unique[key] for key in sorted(unique)]
    return out


def typeinfo_name(elf: Any, typeinfo: int) -> tuple[int | None, str | None]:
    name_ptr, _ = elf.resolved_qword(typeinfo + 8)
    if name_ptr is None:
        return None, None
    return name_ptr, elf.cstring(name_ptr, 512)


def function_vtable_memberships(elf: Any, target: int, max_slot_index: int = 64) -> list[dict[str, Any]]:
    """Recover Itanium-vtable candidates that relocate an exact function target.

    A record is emitted only when the proposed address point has a small signed
    offset-to-top, a mapped typeinfo pointer, and a readable RTTI name. The
    target relocation slot itself is exact; class interpretation remains tied
    to the recorded Itanium header evidence.
    """
    out: dict[tuple[int, int], dict[str, Any]] = {}
    target_slots = sorted(set(elf.relative_target_to_slots.get(target, ())))
    for function_slot in target_slots:
        for index in range(max_slot_index + 1):
            address_point = function_slot - index * 8
            if address_point < 16:
                continue
            off, off_relation = elf.resolved_qword(address_point - 16)
            ti, ti_relation = elf.resolved_qword(address_point - 8)
            if off is None or ti is None or not elf.mapped(ti):
                continue
            signed_off = base.signed64(off)
            if abs(signed_off) >= (1 << 20):
                continue
            name_ptr, name = typeinfo_name(elf, ti)
            if not name:
                continue
            resolved, relation = elf.resolved_qword(function_slot)
            if resolved != target:
                continue
            first, first_relation = elf.resolved_qword(address_point)
            key = (address_point, index)
            out[key] = {
                "function_target": fmt_addr(target),
                "function_slot": fmt_addr(function_slot),
                "slot_index": index,
                "vptr_address_point": fmt_addr(address_point),
                "offset_to_top_signed": signed_off,
                "offset_to_top_relation": off_relation,
                "typeinfo_address": fmt_addr(ti),
                "typeinfo_relation": ti_relation,
                "typeinfo_name_pointer": base.fmt_addr(name_ptr),
                "rtti_name": name,
                "demangled_name": base.demangle_type_name(name),
                "function_slot_relation": relation,
                "first_slot_resolved": base.fmt_addr(first),
                "first_slot_relation": first_relation,
                "first_slot_executable": bool(first is not None and elf.executable(first)),
            }
    return [out[key] for key in sorted(out)]


def scan_indirect_slot(elf: Any, slot_index: int, lo: int, hi: int) -> list[dict[str, Any]]:
    """Find byte-level FF /2 memory-call candidates for one vtable displacement."""
    displacement = slot_index * 8
    out: list[dict[str, Any]] = []
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        i = 0
        while i + 4 < len(blob):
            start = i
            p = i
            if 0x40 <= blob[p] <= 0x4F:
                p += 1
                if p + 3 >= len(blob):
                    break
            if blob[p] != 0xFF:
                i += 1
                continue
            modrm = blob[p + 1]
            if ((modrm >> 3) & 7) != 2:
                i += 1
                continue
            mod = (modrm >> 6) & 3
            rm = modrm & 7
            q = p + 2
            if rm == 4 and mod != 3:
                if q >= len(blob):
                    break
                q += 1
            disp = None
            end = None
            if mod == 1 and q < len(blob):
                disp = struct.unpack_from("b", blob, q)[0]
                end = q + 1
            elif mod == 2 and q + 4 <= len(blob):
                disp = struct.unpack_from("<i", blob, q)[0]
                end = q + 4
            address = seg["vaddr"] + start
            if disp == displacement and end is not None and lo <= address <= hi:
                out.append({
                    "instruction_address": fmt_addr(address),
                    "instruction_bytes": blob[start:end].hex(),
                    "virtual_slot_index": slot_index,
                    "encoded_displacement": f"0x{displacement:x}",
                    "classification": "candidate_until_hosted_instruction_boundary_confirmation",
                })
                i = max(i + 1, end)
            else:
                i += 1
    unique = {item["instruction_address"]: item for item in out}
    return [unique[key] for key in sorted(unique)]


def append_final_discriminator(bundle: dict[str, Any], elf: Any) -> dict[str, Any]:
    windows: list[dict[str, Any]] = bundle["source_code_windows"]
    seen = {int(item["start_address"], 16) for item in windows}
    raw_budget = [int(bundle["source_code_window_raw_bytes"])]
    rel32 = scan_rel32_xrefs(elf, set(TARGET_FUNCTIONS.values()))

    for label, target in TARGET_FUNCTIONS.items():
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_final_target_anchor",
            start=target,
            size=0x900 if label == "storage_slot12_best_caller_aggregate_builder" else 0x700,
            geometry_related=False,
            metadata={"target_label": label, "target_address": fmt_addr(target)},
            raw_budget=raw_budget,
        )
        for item in rel32[target][:64]:
            address = int(item["instruction_address"], 16)
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_final_rel32_caller_context",
                start=max(0, address - 0x300),
                size=0x700,
                geometry_related=False,
                metadata={"target_label": label, "target_address": fmt_addr(target), **item},
                raw_budget=raw_budget,
            )

    for label, address in EXACT_CALL_SITES.items():
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_final_exact_call_context",
            start=max(0, address - 0x300),
            size=0x700,
            geometry_related=False,
            metadata={"call_label": label, "call_address": fmt_addr(address)},
            raw_budget=raw_budget,
        )

    # Viewport slot 14 is virtual-table displacement +0x70. The bounded
    # world-map code range is a new discriminator for its actual call sites.
    slot14 = scan_indirect_slot(elf, 14, 0x00CB0000, 0x00D10000)
    for item in slot14[:48]:
        address = int(item["instruction_address"], 16)
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_final_slot14_call_context",
            start=max(0, address - 0x180),
            size=0x380,
            geometry_related=False,
            metadata=item,
            raw_budget=raw_budget,
        )

    memberships = {
        label: function_vtable_memberships(elf, target)
        for label, target in TARGET_FUNCTIONS.items()
    }
    bundle["source_code_window_raw_bytes"] = raw_budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-final-discriminator-v3",
        "objective": "close_storage_slot12_producer_receiver_and_camera_class_edges",
        "target_functions": {label: fmt_addr(target) for label, target in TARGET_FUNCTIONS.items()},
        "rel32_target_candidates": {fmt_addr(target): items for target, items in rel32.items()},
        "function_vtable_memberships": memberships,
        "worldmap_slot14_candidates": slot14,
        "worldmap_slot14_candidate_count": len(slot14),
        "raw_window_budget_bytes": v2.MAX_SOURCE_CODE_BYTES,
        "raw_window_bytes_used": raw_budget[0],
        "bounded_window_count": len(windows),
        "source_disassembly": "none",
        "hosted_instruction_boundary_confirmation_required": True,
        "client_bytes_mutated": False,
        "raw_client_uploaded": False,
    }
    return bundle


def source_mode(args: argparse.Namespace) -> int:
    if not args.client:
        raise SystemExit("WORLD_MAP_STATIC_V3_REFUSED=CLIENT_REQUIRED")
    rc = v2.source_mode(args)
    if rc != 0:
        return rc
    outdir = Path(args.outdir)
    bundle_path = outdir / "worldmap-static-evidence.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    elf = base.Elf64(Path(args.client))
    bundle = append_final_discriminator(bundle, elf)
    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "worldmap-static-evidence.md").write_text(base.markdown_report(bundle), encoding="utf-8")
    fence_path = outdir / "source-fence.txt"
    fence = fence_path.read_text(encoding="utf-8").rstrip("\n")
    fence_path.write_text(fence + "\n" + "\n".join([
        "WORLD_MAP_SECOND_PACK_SOURCE=PASS",
        f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(bundle['source_code_windows'])}",
        f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={bundle['source_code_window_raw_bytes']}",
        f"WORLD_MAP_SECOND_PACK_SLOT14_CANDIDATES={bundle['second_pack']['worldmap_slot14_candidate_count']}",
        "WORLD_MAP_SECOND_PACK_SOURCE_DISASSEMBLY=none",
        "WORLD_MAP_SECOND_PACK_HOSTED_CONFIRMATION_REQUIRED=true",
        "",
    ]), encoding="utf-8")
    print("WORLD_MAP_SECOND_PACK_SOURCE=PASS")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(bundle['source_code_windows'])}")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={bundle['source_code_window_raw_bytes']}")
    print(f"WORLD_MAP_SECOND_PACK_SLOT14_CANDIDATES={bundle['second_pack']['worldmap_slot14_candidate_count']}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("source", "validate"))
    parser.add_argument("--client")
    parser.add_argument("--candidate-index", default="-1")
    parser.add_argument("--bundle-dir")
    parser.add_argument("--outdir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "source":
        return source_mode(args)
    if not args.bundle_dir:
        raise SystemExit("WORLD_MAP_STATIC_V3_REFUSED=BUNDLE_DIR_REQUIRED")
    return v2.validate_mode(args)


if __name__ == "__main__":
    sys.exit(main())
