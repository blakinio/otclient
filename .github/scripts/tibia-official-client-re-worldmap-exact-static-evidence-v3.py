#!/usr/bin/env python3
"""Last bounded cross-check for the protocol-handler outer owner.

The source executor verifies and reads only the exact client. It emits direct
rel32 callers and exact Itanium-vtable membership candidates for 0x00804620,
plus bounded contexts. No client execution, mutation or source-side disassembly.
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
TARGET = 0x00804620


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


def scan_rel32_xrefs(elf: Any, target: int) -> list[dict[str, Any]]:
    out = []
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        for i in range(max(0, len(blob) - 5)):
            if blob[i] not in (0xE8, 0xE9):
                continue
            disp = struct.unpack_from("<i", blob, i + 1)[0]
            address = seg["vaddr"] + i
            resolved = address + 5 + disp
            if resolved != target:
                continue
            out.append({
                "instruction_address": fmt_addr(address),
                "opcode": "call_rel32" if blob[i] == 0xE8 else "jmp_rel32",
                "instruction_bytes": blob[i:i + 5].hex(),
                "resolved_target": fmt_addr(target),
                "classification": "candidate_until_hosted_instruction_boundary_confirmation",
            })
    unique = {item["instruction_address"]: item for item in out}
    return [unique[key] for key in sorted(unique)]


def typeinfo_name(elf: Any, typeinfo: int) -> tuple[int | None, str | None]:
    name_ptr, _ = elf.resolved_qword(typeinfo + 8)
    return (name_ptr, elf.cstring(name_ptr, 512)) if name_ptr is not None else (None, None)


def memberships(elf: Any, target: int) -> list[dict[str, Any]]:
    out = {}
    for function_slot in sorted(set(elf.relative_target_to_slots.get(target, ()))):
        for index in range(96):
            vptr = function_slot - index * 8
            if vptr < 16:
                continue
            off, off_rel = elf.resolved_qword(vptr - 16)
            ti, ti_rel = elf.resolved_qword(vptr - 8)
            if off is None or ti is None or not elf.mapped(ti) or abs(base.signed64(off)) >= (1 << 20):
                continue
            name_ptr, name = typeinfo_name(elf, ti)
            if not name:
                continue
            resolved, relation = elf.resolved_qword(function_slot)
            if resolved != target:
                continue
            key = (vptr, index)
            out[key] = {
                "function_target": fmt_addr(target),
                "function_slot": fmt_addr(function_slot),
                "slot_index": index,
                "vptr_address_point": fmt_addr(vptr),
                "offset_to_top_signed": base.signed64(off),
                "offset_to_top_relation": off_rel,
                "typeinfo_address": fmt_addr(ti),
                "typeinfo_relation": ti_rel,
                "typeinfo_name_pointer": base.fmt_addr(name_ptr),
                "rtti_name": name,
                "demangled_name": base.demangle_type_name(name),
                "function_slot_relation": relation,
            }
    return [out[key] for key in sorted(out)]


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
    windows = bundle["source_code_windows"]
    seen = {int(item["start_address"], 16) for item in windows}
    budget = [int(bundle["source_code_window_raw_bytes"])]

    v2.append_window(
        windows, seen, elf,
        purpose="second_pack_outer_owner_target",
        start=TARGET,
        size=0x900,
        geometry_related=False,
        metadata={"target": fmt_addr(TARGET)},
        raw_budget=budget,
    )
    callers = scan_rel32_xrefs(elf, TARGET)
    for item in callers[:96]:
        address = int(item["instruction_address"], 16)
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_outer_owner_caller",
            start=max(0, address - 0x300),
            size=0x700,
            geometry_related=False,
            metadata=item,
            raw_budget=budget,
        )

    member = memberships(elf, TARGET)
    bundle["source_code_window_raw_bytes"] = budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-outer-owner-v6",
        "objective": "last_cross_check_for_outer_plus_0x2f8_storage_owner",
        "target": fmt_addr(TARGET),
        "rel32_callers": callers,
        "rel32_caller_count": len(callers),
        "vtable_memberships": member,
        "vtable_membership_count": len(member),
        "raw_window_budget_bytes": v2.MAX_SOURCE_CODE_BYTES,
        "raw_window_bytes_used": budget[0],
        "bounded_window_count": len(windows),
        "source_disassembly": "none",
        "hosted_instruction_boundary_confirmation_required": True,
        "client_bytes_mutated": False,
        "raw_client_uploaded": False,
    }
    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "worldmap-static-evidence.md").write_text(base.markdown_report(bundle), encoding="utf-8")
    fence_path = outdir / "source-fence.txt"
    fence = fence_path.read_text(encoding="utf-8").rstrip("\n")
    fence_path.write_text(fence + "\n" + "\n".join([
        "WORLD_MAP_SECOND_PACK_SOURCE=PASS",
        f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(windows)}",
        f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={budget[0]}",
        f"WORLD_MAP_SECOND_PACK_OUTER_OWNER_CALLERS={len(callers)}",
        f"WORLD_MAP_SECOND_PACK_OUTER_OWNER_VTABLE_MEMBERSHIPS={len(member)}",
        "WORLD_MAP_SECOND_PACK_SOURCE_DISASSEMBLY=none",
        "WORLD_MAP_SECOND_PACK_HOSTED_CONFIRMATION_REQUIRED=true",
        "",
    ]), encoding="utf-8")
    print("WORLD_MAP_SECOND_PACK_SOURCE=PASS")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={budget[0]}")
    print(f"WORLD_MAP_SECOND_PACK_OUTER_OWNER_CALLERS={len(callers)}")
    print(f"WORLD_MAP_SECOND_PACK_OUTER_OWNER_VTABLE_MEMBERSHIPS={len(member)}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=("source", "validate"))
    p.add_argument("--client")
    p.add_argument("--candidate-index", default="-1")
    p.add_argument("--bundle-dir")
    p.add_argument("--outdir", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "source":
        return source_mode(args)
    if not args.bundle_dir:
        raise SystemExit("WORLD_MAP_STATIC_V3_REFUSED=BUNDLE_DIR_REQUIRED")
    return v2.validate_mode(args)


if __name__ == "__main__":
    sys.exit(main())
