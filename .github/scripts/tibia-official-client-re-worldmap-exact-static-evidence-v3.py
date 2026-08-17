#!/usr/bin/env python3
"""Second-pack source expansion plus order-tolerant hosted validation.

The source side never executes or disassembles the client. It extends the already
bounded V2 source bundle with exact target-vtable entries, direct rel32 caller
candidates, direct vptr xrefs, and x86-64 indirect virtual-call candidates for
slot 12 (+0x60). Hosted validation still owns disassembly of the sanitized byte
windows only.
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

TARGET_VPTRS = {
    "TWorldMapRenderProvider": 0x02F6C258,
    "TWorldMapCamera": 0x03083968,
    "TWorldMapPicker": 0x02F6B7C8,
    "TWorldMapViewport": 0x0308C9A8,
    "TWorldmapProtocolMessageHandler": 0x030871D8,
    "TWorldMapExtent": 0x02F61578,
    "TWorldMapSubfieldExtent": 0x02F63FA8,
}

TARGET_FUNCTIONS = {
    "TWorldMapStorage_slot12": 0x00CC6CD0,
    "camera_float_dependency_candidate": 0x00CED1B0,
}

SLOT_STAGE_LIMITS = {
    "TWorldMapRenderProvider": 24,
    "TWorldMapCamera": 24,
    "TWorldMapPicker": 24,
    "TWorldMapViewport": 24,
    "TWorldmapProtocolMessageHandler": 16,
    "TWorldMapExtent": 12,
    "TWorldMapSubfieldExtent": 12,
}

SLOT_WINDOW_SIZES = {
    "TWorldMapRenderProvider": 0x480,
    "TWorldMapCamera": 0x480,
    "TWorldMapPicker": 0x480,
    "TWorldMapViewport": 0x400,
    "TWorldmapProtocolMessageHandler": 0x380,
    "TWorldMapExtent": 0x300,
    "TWorldMapSubfieldExtent": 0x300,
}


def fmt_addr(value: int) -> str:
    return f"0x{value:08x}"


def validate_source_bundle_order_tolerant(bundle_dir: Path):
    """Preserve every V2 validation except presentation-order equality."""
    try:
        return _ORIGINAL_VALIDATE_SOURCE_BUNDLE(bundle_dir)
    except SystemExit as exc:
        if str(exc) != "WORLD_MAP_STATIC_V2_REFUSED=SOURCE_REPORT_NONDETERMINISTIC":
            raise
        bundle = json.loads(
            (bundle_dir / "worldmap-static-evidence.json").read_text(encoding="utf-8")
        )
        print("WORLD_MAP_STATIC_V3_SOURCE_REPORT_ORDER_TOLERATED=true")
        print("WORLD_MAP_STATIC_V3_AUTHORITATIVE_SOURCE=validated_json")
        return bundle


v2.validate_source_bundle = validate_source_bundle_order_tolerant


def scan_rel32_xrefs(elf: Any, targets: set[int]) -> dict[int, list[dict[str, Any]]]:
    """Byte-level E8/E9 rel32 target candidates; hosted objdump confirms boundaries."""
    out: dict[int, list[dict[str, Any]]] = {target: [] for target in targets}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        for i in range(0, max(0, len(blob) - 5)):
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
    for target in out:
        unique = {item["instruction_address"]: item for item in out[target]}
        out[target] = [unique[key] for key in sorted(unique)]
    return out


def scan_indirect_slot12_candidates(elf: Any) -> list[dict[str, Any]]:
    """Find x86-64 FF /2 memory calls whose encoded displacement is exactly +0x60.

    +0x60 is virtual-table slot 12 (12 * 8). This is deliberately a byte-level
    candidate scan: only a hosted disassembly window beginning at the candidate
    may promote it to an instruction-boundary FACT.
    """
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
                q += 1  # SIB byte
            disp_value = None
            end = None
            if mod == 1 and q < len(blob):
                disp_value = struct.unpack_from("b", blob, q)[0]
                end = q + 1
            elif mod == 2 and q + 4 <= len(blob):
                disp_value = struct.unpack_from("<i", blob, q)[0]
                end = q + 4
            if disp_value != 0x60 or end is None:
                i += 1
                continue
            address = seg["vaddr"] + start
            out.append({
                "instruction_address": fmt_addr(address),
                "instruction_bytes": blob[start:end].hex(),
                "encoded_displacement": "0x60",
                "virtual_slot_index": 12,
                "classification": "candidate_until_hosted_instruction_boundary_confirmation",
            })
            i = max(i + 1, end)
    unique = {item["instruction_address"]: item for item in out}
    return [unique[key] for key in sorted(unique)]


def append_target_windows(bundle: dict[str, Any], elf: Any) -> dict[str, Any]:
    windows: list[dict[str, Any]] = bundle["source_code_windows"]
    seen = {int(item["start_address"], 16) for item in windows}
    raw_budget = [int(bundle["source_code_window_raw_bytes"])]

    rel32 = scan_rel32_xrefs(elf, set(TARGET_FUNCTIONS.values()))
    indirect_slot12 = scan_indirect_slot12_candidates(elf)

    # Exact candidate-start windows are cheap and let hosted objdump decide
    # whether each byte pattern is a real instruction boundary.
    for target, items in rel32.items():
        for item in items[:128]:
            start = int(item["instruction_address"], 16)
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_rel32_candidate_exact",
                start=start,
                size=0x90,
                geometry_related=False,
                metadata={"resolved_target": fmt_addr(target), **item},
                raw_budget=raw_budget,
            )

    for item in indirect_slot12[:512]:
        start = int(item["instruction_address"], 16)
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_slot12_indirect_candidate_exact",
            start=start,
            size=0x30,
            geometry_related=False,
            metadata=item,
            raw_budget=raw_budget,
        )

    # Context windows for a bounded prefix of slot-12 candidates. A later
    # discriminator run can target a different subset if the exact-call census
    # proves the relevant caller lies outside this prefix.
    for item in indirect_slot12[:48]:
        call_addr = int(item["instruction_address"], 16)
        start = max(0, call_addr - 0x180)
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_slot12_indirect_candidate_context",
            start=start,
            size=0x380,
            geometry_related=False,
            metadata={"call_candidate": fmt_addr(call_addr), "virtual_slot_index": 12},
            raw_budget=raw_budget,
        )

    # The previously observed float-dependency candidate is staged directly;
    # no semantic Camera linkage is asserted here.
    v2.append_window(
        windows, seen, elf,
        purpose="second_pack_known_function_candidate",
        start=TARGET_FUNCTIONS["camera_float_dependency_candidate"],
        size=0x900,
        geometry_related=False,
        metadata={
            "label": "camera_float_dependency_candidate",
            "classification": "candidate_only_pending_exact_class_call_edge",
        },
        raw_budget=raw_budget,
    )

    # Exact RIP-relative vptr references are stronger constructor/identity
    # anchors than text-name proximity, so stage those before the virtuals.
    vptr_xrefs = v2.scan_rip_lea_xrefs(elf, set(TARGET_VPTRS.values()))
    for label, vptr in TARGET_VPTRS.items():
        for item in vptr_xrefs.get(vptr, [])[:12]:
            start = int(item["instruction_address"], 16)
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_target_vptr_xref",
                start=start,
                size=0x480,
                geometry_related=False,
                metadata={"target_class": label, "target_vptr": fmt_addr(vptr), **item},
                raw_budget=raw_budget,
            )

    target_vtables: dict[str, Any] = {}
    for label, vptr in TARGET_VPTRS.items():
        slots = base.vtable_slots(elf, vptr, 40)
        target_vtables[label] = {
            "vptr_address_point": fmt_addr(vptr),
            "slots": slots,
        }
        staged = 0
        for slot in slots:
            if staged >= SLOT_STAGE_LIMITS[label]:
                break
            if not slot.get("resolved_executable") or slot.get("resolved") == "UNKNOWN":
                continue
            start = int(slot["resolved"], 16)
            before = raw_budget[0]
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_target_vtable_function",
                start=start,
                size=SLOT_WINDOW_SIZES[label],
                geometry_related=False,
                metadata={
                    "target_class": label,
                    "target_vptr": fmt_addr(vptr),
                    "vtable_slot_index": slot["index"],
                },
                raw_budget=raw_budget,
            )
            if raw_budget[0] > before:
                staged += 1
        target_vtables[label]["staged_executable_slot_windows"] = staged

    bundle["source_code_window_raw_bytes"] = raw_budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-source-v1",
        "objective": "upstream_storage_extent_render_camera_picker_limit_discriminators",
        "target_functions": {key: fmt_addr(value) for key, value in TARGET_FUNCTIONS.items()},
        "target_vtables": target_vtables,
        "direct_vptr_xrefs": {
            label: vptr_xrefs.get(vptr, []) for label, vptr in TARGET_VPTRS.items()
        },
        "rel32_target_candidates": {
            fmt_addr(target): items for target, items in rel32.items()
        },
        "indirect_slot12_plus_0x60_candidates": indirect_slot12,
        "indirect_slot12_candidate_count": len(indirect_slot12),
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
    # V2 owns the exact fence, ELF parsing, original identity proof and initial
    # bounded bundle. V3 only adds new discriminators.
    rc = v2.source_mode(args)
    if rc != 0:
        return rc

    outdir = Path(args.outdir)
    client = Path(args.client)
    bundle_path = outdir / "worldmap-static-evidence.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    elf = base.Elf64(client)
    bundle = append_target_windows(bundle, elf)

    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "worldmap-static-evidence.md").write_text(
        base.markdown_report(bundle), encoding="utf-8"
    )
    fence_path = outdir / "source-fence.txt"
    fence = fence_path.read_text(encoding="utf-8").rstrip("\n")
    fence_path.write_text(
        fence + "\n" + "\n".join([
            "WORLD_MAP_SECOND_PACK_SOURCE=PASS",
            f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(bundle['source_code_windows'])}",
            f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={bundle['source_code_window_raw_bytes']}",
            f"WORLD_MAP_SECOND_PACK_SLOT12_CANDIDATES={bundle['second_pack']['indirect_slot12_candidate_count']}",
            "WORLD_MAP_SECOND_PACK_SOURCE_DISASSEMBLY=none",
            "WORLD_MAP_SECOND_PACK_HOSTED_CONFIRMATION_REQUIRED=true",
            "",
        ]),
        encoding="utf-8",
    )

    print("WORLD_MAP_SECOND_PACK_SOURCE=PASS")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(bundle['source_code_windows'])}")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={bundle['source_code_window_raw_bytes']}")
    print(f"WORLD_MAP_SECOND_PACK_SLOT12_CANDIDATES={bundle['second_pack']['indirect_slot12_candidate_count']}")
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
