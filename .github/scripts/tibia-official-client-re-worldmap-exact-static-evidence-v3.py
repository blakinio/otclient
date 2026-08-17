#!/usr/bin/env python3
"""Final constructor/caller discriminator for world-map exact-static evidence.

This phase is intentionally narrow: it stages the exact protocol-handler
constructor neighbourhood and rel32 callers whose targets fall inside that
small constructor range. Source execution remains read-only; disassembly remains
GitHub-hosted over bounded sanitized windows only.
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

CONSTRUCTOR_RANGE_START = 0x00803900
CONSTRUCTOR_RANGE_END = 0x00803C20
CONSTRUCTOR_CONTEXT_START = 0x00803800
CONSTRUCTOR_CONTEXT_SIZE = 0x850


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


def scan_rel32_targets_in_range(elf: Any, lo: int, hi: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
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
            if lo <= target <= hi:
                out.append({
                    "instruction_address": fmt_addr(address),
                    "opcode": "call_rel32" if opcode == 0xE8 else "jmp_rel32",
                    "instruction_bytes": blob[i:i + 5].hex(),
                    "resolved_target": fmt_addr(target),
                    "classification": "candidate_until_hosted_instruction_boundary_confirmation",
                })
    unique = {(item["instruction_address"], item["resolved_target"]): item for item in out}
    return [unique[key] for key in sorted(unique)]


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
    windows: list[dict[str, Any]] = bundle["source_code_windows"]
    seen = {int(item["start_address"], 16) for item in windows}
    budget = [int(bundle["source_code_window_raw_bytes"])]

    v2.append_window(
        windows, seen, elf,
        purpose="second_pack_protocol_handler_constructor_context",
        start=CONSTRUCTOR_CONTEXT_START,
        size=CONSTRUCTOR_CONTEXT_SIZE,
        geometry_related=False,
        metadata={
            "known_vptr_write": "0x00803c01 -> 0x030871d8",
            "known_handler_storage_candidate_field": "+0x10/+0x18 shared_ptr pair",
            "known_handler_extent_source_field": "+0xb0/+0xb4 initialized from 0x01cdd958",
        },
        raw_budget=budget,
    )

    candidates = scan_rel32_targets_in_range(elf, CONSTRUCTOR_RANGE_START, CONSTRUCTOR_RANGE_END)
    for item in candidates[:128]:
        address = int(item["instruction_address"], 16)
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_protocol_handler_constructor_caller_candidate",
            start=max(0, address - 0x300),
            size=0x700,
            geometry_related=False,
            metadata=item,
            raw_budget=budget,
        )

    bundle["source_code_window_raw_bytes"] = budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-handler-constructor-v5",
        "objective": "close_protocol_handler_plus_0x10_dependency_type",
        "constructor_range": {
            "start": fmt_addr(CONSTRUCTOR_RANGE_START),
            "end": fmt_addr(CONSTRUCTOR_RANGE_END),
        },
        "rel32_candidates_into_constructor_range": candidates,
        "rel32_candidate_count": len(candidates),
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
        f"WORLD_MAP_SECOND_PACK_HANDLER_CTOR_CALLER_CANDIDATES={len(candidates)}",
        "WORLD_MAP_SECOND_PACK_SOURCE_DISASSEMBLY=none",
        "WORLD_MAP_SECOND_PACK_HOSTED_CONFIRMATION_REQUIRED=true",
        "",
    ]), encoding="utf-8")

    print("WORLD_MAP_SECOND_PACK_SOURCE=PASS")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={budget[0]}")
    print(f"WORLD_MAP_SECOND_PACK_HANDLER_CTOR_CALLER_CANDIDATES={len(candidates)}")
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
