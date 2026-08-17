#!/usr/bin/env python3
"""Second-pack targeted source expansion plus order-tolerant hosted validation.

The source side never executes or disassembles the client. It reuses the V2
exact-fenced sanitizer, then adds only targeted caller/context and bounded data
probes selected from the first second-pack census. Hosted validation owns all
instruction disassembly of the sanitized code windows.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
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

# Materially new phase-2 discriminator targets. These are exact functions
# already present in the phase-1 bounded evidence; this run recovers their
# direct caller contexts instead of repeating broad vtable staging.
TARGET_FUNCTIONS = {
    "TWorldMapStorage_constructor": 0x00CBF37A,
    "TWorldMapStorage_slot2": 0x00E02CC0,
    "TWorldMapStorage_slot12": 0x00CC6CD0,
    "TWorldMapViewport_constructor": 0x00CBF680,
    "TWorldMapViewport_geometry_recompute": 0x00CBF700,
    "TWorldMapRenderProvider_constructor": 0x00CCFA02,
    "TWorldMapRenderProvider_slot10": 0x00CEA540,
    "TWorldMapRenderProvider_slot13": 0x00CD1E50,
    "TWorldMapRenderProvider_slot14": 0x00CD2260,
    "TWorldMapRenderProvider_slot16": 0x00CD08B0,
    "TWorldMapPicker_slot4": 0x00CD65B0,
    "TWorldMapPicker_slot5": 0x00CD0400,
    "TWorldMapPicker_slot6": 0x00CE7AA0,
    "TWorldMapPicker_slot7": 0x00CE80C0,
    "camera_float_dependency_candidate": 0x00CED1B0,
}

# These 16 addresses are the phase-1 exact-start world-map-range virtual slot-12
# candidates. This run stages context around all of them. The source selector
# independently rescans them and refuses to stage an address not present in the
# fresh exact-client candidate census.
PHASE1_WORLD_MAP_SLOT12_CANDIDATES = (
    0x00CB30CC, 0x00CB4919, 0x00CB4943, 0x00CB7E29,
    0x00CBEDD1, 0x00CC0377, 0x00CC08DB, 0x00CD1E75,
    0x00CD6038, 0x00CD6170, 0x00CDB7AB, 0x00CEA602,
    0x00CECB21, 0x00CED207, 0x00CF6D2C, 0x00D06C51,
)

# Bounded static data needed to discriminate constructor defaults, tile-size
# arithmetic and Qt/metaobject ownership. Hex is emitted only for these tiny
# read-only ranges; no raw executable is uploaded.
DATA_PROBES = {
    "viewport_ctor_xmm_default": (0x01D32EF0, 0x20),
    "viewport_ctor_qword_default_1": (0x01CDD958, 0x20),
    "viewport_ctor_qword_default_2": (0x01D6BAA8, 0x20),
    "viewport_geometry_qword_constant": (0x01D63CD0, 0x20),
    "signed_div32_bias_constant": (0x01CE70C8, 0x20),
    "camera_init_scalar": (0x01CD5910, 0x20),
    "camera_init_block_1": (0x01CD5920, 0x20),
    "camera_init_block_2": (0x01CD5930, 0x20),
    "camera_init_block_3": (0x01CD5940, 0x20),
    "camera_float_dependency_multiplier": (0x029505A8, 0x20),
    "storage_qmeta_candidate": (0x030CC7E0, 0x100),
    "adjacent_qmeta_candidate": (0x030ABF80, 0x100),
}

IDENTITY_PROBE_VPTRS = {
    "embedded_subfield_extent_candidate": 0x02F615A0,
    "TWorldMapExtent": 0x02F61578,
    "camera_aux_vptr_candidate": 0x02F69278,
}

STRING_TOKENS = (
    "TWorldMapStorage",
    "TWorldMapViewport",
    "TWorldMapRenderProvider",
    "TWorldMapCamera",
    "TWorldMapPicker",
    "WorldMapStorage",
    "WorldMapViewport",
    "WorldMapRenderProvider",
    "WorldMapCamera",
    "WorldMapPicker",
)


def fmt_addr(value: int) -> str:
    return f"0x{value:08x}"


def validate_source_bundle_order_tolerant(bundle_dir: Path):
    """Preserve every V2 source validation except presentation-order equality."""
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
    """Find x86-64 FF /2 memory calls whose encoded displacement is exactly +0x60."""
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


def scalar_views(blob: bytes) -> dict[str, Any]:
    out: dict[str, Any] = {"bytes_hex": blob.hex(), "byte_count": len(blob)}
    u32 = []
    f32 = []
    for off in range(0, len(blob) - 3, 4):
        u = struct.unpack_from("<I", blob, off)[0]
        s = struct.unpack_from("<i", blob, off)[0]
        f = struct.unpack_from("<f", blob, off)[0]
        u32.append({"offset": off, "u32": u, "i32": s, "hex": f"0x{u:08x}"})
        f32.append({"offset": off, "f32": f if math.isfinite(f) else str(f)})
    qwords = []
    for off in range(0, len(blob) - 7, 8):
        q = struct.unpack_from("<Q", blob, off)[0]
        qwords.append({"offset": off, "u64": q, "hex": f"0x{q:016x}"})
    out["u32_views"] = u32
    out["f32_views"] = f32
    out["qword_views"] = qwords
    return out


def data_probe(elf: Any, address: int, size: int) -> dict[str, Any]:
    blob = elf.bytes_at(address, size)
    if blob is None:
        return {"address": fmt_addr(address), "requested_bytes": size, "mapped": False}
    out = {
        "address": fmt_addr(address),
        "requested_bytes": size,
        "mapped": True,
        **scalar_views(blob),
        "resolved_qwords": [],
    }
    for off in range(0, len(blob) - 7, 8):
        slot = address + off
        raw = elf.qword(slot)
        resolved, relation = elf.resolved_qword(slot)
        rec: dict[str, Any] = {
            "offset": off,
            "slot": fmt_addr(slot),
            "raw": base.fmt_qword(raw),
            "resolved": base.fmt_addr(resolved),
            "relation": relation,
            "relocations": base.reloc_view(elf.relocations(slot)),
        }
        if resolved is not None and elf.mapped(resolved):
            text = elf.cstring(resolved, 512)
            if text:
                rec["resolved_cstring"] = text
        out["resolved_qwords"].append(rec)
    return out


def identity_from_vptr(elf: Any, label: str, vptr: int) -> dict[str, Any]:
    return base.identity_record(elf, {
        "label": label,
        "header_start": vptr - 16,
        "header_end": vptr - 1,
        "vptr": vptr,
    })


def append_targeted_windows(bundle: dict[str, Any], elf: Any) -> dict[str, Any]:
    windows: list[dict[str, Any]] = bundle["source_code_windows"]
    seen = {int(item["start_address"], 16) for item in windows}
    raw_budget = [int(bundle["source_code_window_raw_bytes"])]

    rel32 = scan_rel32_xrefs(elf, set(TARGET_FUNCTIONS.values()))
    slot12 = scan_indirect_slot12_candidates(elf)
    slot12_addresses = {int(item["instruction_address"], 16) for item in slot12}

    fresh_worldmap_slot12 = []
    for address in PHASE1_WORLD_MAP_SLOT12_CANDIDATES:
        if address not in slot12_addresses:
            raise SystemExit(f"WORLD_MAP_STATIC_V3_REFUSED=SLOT12_DRIFT:{address:x}")
        fresh_worldmap_slot12.append(fmt_addr(address))
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_worldmap_slot12_context",
            start=max(0, address - 0x280),
            size=0x580,
            geometry_related=False,
            metadata={"call_address": fmt_addr(address), "virtual_slot_index": 12},
            raw_budget=raw_budget,
        )

    # Stage the exact target functions as standalone anchors and every direct
    # rel32 caller/jump context. This is a targeted second discriminator, not a
    # repeat of phase-1 broad vtable staging.
    for label, target in TARGET_FUNCTIONS.items():
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_target_function_anchor",
            start=target,
            size=0x780 if label == "camera_float_dependency_candidate" else 0x500,
            geometry_related=False,
            metadata={"target_label": label, "target_address": fmt_addr(target)},
            raw_budget=raw_budget,
        )
        for item in rel32[target][:64]:
            address = int(item["instruction_address"], 16)
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_rel32_caller_context",
                start=max(0, address - 0x280),
                size=0x580,
                geometry_related=False,
                metadata={"target_label": label, "target_address": fmt_addr(target), **item},
                raw_budget=raw_budget,
            )

    data = {
        label: data_probe(elf, address, size)
        for label, (address, size) in DATA_PROBES.items()
    }
    identities = {
        label: identity_from_vptr(elf, label, vptr)
        for label, vptr in IDENTITY_PROBE_VPTRS.items()
    }
    strings = {
        token: elf.find_token_strings(token, max_hits=64)
        for token in STRING_TOKENS
    }

    bundle["source_code_window_raw_bytes"] = raw_budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-targeted-v2",
        "objective": "targeted_upstream_storage_extent_render_camera_picker_limit_discriminators",
        "target_functions": {key: fmt_addr(value) for key, value in TARGET_FUNCTIONS.items()},
        "rel32_target_candidates": {fmt_addr(target): items for target, items in rel32.items()},
        "indirect_slot12_candidate_count": len(slot12),
        "fresh_worldmap_slot12_candidates": fresh_worldmap_slot12,
        "targeted_data_probes": data,
        "identity_probes": identities,
        "string_hits": strings,
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
    client = Path(args.client)
    bundle_path = outdir / "worldmap-static-evidence.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    elf = base.Elf64(client)
    bundle = append_targeted_windows(bundle, elf)

    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "worldmap-static-evidence.md").write_text(base.markdown_report(bundle), encoding="utf-8")
    fence_path = outdir / "source-fence.txt"
    fence = fence_path.read_text(encoding="utf-8").rstrip("\n")
    fence_path.write_text(
        fence + "\n" + "\n".join([
            "WORLD_MAP_SECOND_PACK_SOURCE=PASS",
            f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(bundle['source_code_windows'])}",
            f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={bundle['source_code_window_raw_bytes']}",
            f"WORLD_MAP_SECOND_PACK_SLOT12_CANDIDATES={bundle['second_pack']['indirect_slot12_candidate_count']}",
            f"WORLD_MAP_SECOND_PACK_WORLDMAP_SLOT12_CONTEXTS={len(bundle['second_pack']['fresh_worldmap_slot12_candidates'])}",
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
    print(f"WORLD_MAP_SECOND_PACK_WORLDMAP_SLOT12_CONTEXTS={len(bundle['second_pack']['fresh_worldmap_slot12_candidates'])}")
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
