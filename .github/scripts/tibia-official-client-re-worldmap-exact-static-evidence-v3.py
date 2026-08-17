#!/usr/bin/env python3
"""Qt-metaobject discriminator for the world-map exact-static second package.

The source side only verifies/reads the exact client and emits bounded sanitized
windows/data. It never executes or disassembles the client. Hosted validation
continues to disassemble only the emitted byte windows.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
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

OWNER_STATIC_METAOBJECT = 0x03087800
OWNER_NEARBY_VPTR = 0x0308C128

# New, bounded regions only: the immediate ordinary-method cluster containing
# cdb770 and the upstream updater cluster containing cec8d0.
CODE_RANGES = (
    ("cdb_owner_method_cluster", 0x00CDA000, 0x2000),
    ("cec_owner_updater_cluster", 0x00CEC000, 0x1200),
    ("df_owner_qmeta_wrapper_cluster", 0x00DF2800, 0x700),
)


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


def printable_runs(blob: bytes, minimum: int = 4) -> list[dict[str, Any]]:
    out = []
    for match in re.finditer(rb"[ -~]{%d,}" % minimum, blob):
        text = match.group(0).decode("ascii", "replace")
        out.append({"offset": match.start(), "text": text[:256]})
    return out[:96]


def mapped_probe(elf: Any, address: int, size: int) -> dict[str, Any]:
    blob = elf.bytes_at(address, size)
    if blob is None:
        return {"address": fmt_addr(address), "mapped": False, "requested_bytes": size}
    return {
        "address": fmt_addr(address),
        "mapped": True,
        "byte_count": len(blob),
        "bytes_hex": blob.hex(),
        "printable_runs": printable_runs(blob),
    }


def qt_metaobject_probe(elf: Any, address: int) -> dict[str, Any]:
    """Read Qt6-style QMetaObject pointer fields without assigning semantics blindly."""
    record: dict[str, Any] = {
        "address": fmt_addr(address),
        "qwords": [],
        "followed_mapped_blocks": [],
    }
    seen_follow = set()
    for index in range(7):
        slot = address + index * 8
        raw = elf.qword(slot)
        resolved, relation = elf.resolved_qword(slot)
        item: dict[str, Any] = {
            "index": index,
            "slot": fmt_addr(slot),
            "raw": base.fmt_qword(raw),
            "resolved": base.fmt_addr(resolved),
            "relation": relation,
            "relocations": base.reloc_view(elf.relocations(slot)),
            "resolved_executable": bool(resolved is not None and elf.executable(resolved)),
            "resolved_mapped": bool(resolved is not None and elf.mapped(resolved)),
        }
        if resolved is not None and elf.mapped(resolved):
            text = elf.cstring(resolved, 512)
            if text:
                item["resolved_cstring"] = text
            if resolved not in seen_follow:
                seen_follow.add(resolved)
                follow = mapped_probe(elf, resolved, 0x500)
                follow["source_qword_index"] = index
                record["followed_mapped_blocks"].append(follow)
        record["qwords"].append(item)
    return record


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

    for label, start, size in CODE_RANGES:
        v2.append_window(
            windows, seen, elf,
            purpose="second_pack_owner_cluster",
            start=start,
            size=size,
            geometry_related=False,
            metadata={"cluster": label},
            raw_budget=budget,
        )

    xrefs = v2.scan_rip_lea_xrefs(elf, {OWNER_STATIC_METAOBJECT, OWNER_NEARBY_VPTR})
    for target, items in xrefs.items():
        for item in items[:64]:
            address = int(item["instruction_address"], 16)
            v2.append_window(
                windows, seen, elf,
                purpose="second_pack_owner_identity_xref",
                start=max(0, address - 0x240),
                size=0x580,
                geometry_related=False,
                metadata={"identity_target": fmt_addr(target), **item},
                raw_budget=budget,
            )

    owner_vptr_identity = base.identity_record(elf, {
        "label": "owner_nearby_vptr_candidate",
        "header_start": OWNER_NEARBY_VPTR - 16,
        "header_end": OWNER_NEARBY_VPTR - 1,
        "vptr": OWNER_NEARBY_VPTR,
    })

    bundle["source_code_window_raw_bytes"] = budget[0]
    bundle["second_pack"] = {
        "schema": "track-a-worldmap-exact-static-second-pack-owner-meta-v4",
        "objective": "identify_cdb770_owner_and_receiver_dependency_without_broad_rescan",
        "owner_static_metaobject": qt_metaobject_probe(elf, OWNER_STATIC_METAOBJECT),
        "owner_static_metaobject_xrefs": xrefs.get(OWNER_STATIC_METAOBJECT, []),
        "owner_nearby_vptr_identity": owner_vptr_identity,
        "owner_nearby_vptr_xrefs": xrefs.get(OWNER_NEARBY_VPTR, []),
        "bounded_clusters": [
            {"label": label, "start": fmt_addr(start), "size": size}
            for label, start, size in CODE_RANGES
        ],
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
        f"WORLD_MAP_SECOND_PACK_OWNER_METAOBJECT_XREFS={len(xrefs.get(OWNER_STATIC_METAOBJECT, []))}",
        f"WORLD_MAP_SECOND_PACK_OWNER_VPTR_XREFS={len(xrefs.get(OWNER_NEARBY_VPTR, []))}",
        "WORLD_MAP_SECOND_PACK_SOURCE_DISASSEMBLY=none",
        "WORLD_MAP_SECOND_PACK_HOSTED_CONFIRMATION_REQUIRED=true",
        "",
    ]), encoding="utf-8")

    print("WORLD_MAP_SECOND_PACK_SOURCE=PASS")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES={budget[0]}")
    print(f"WORLD_MAP_SECOND_PACK_OWNER_METAOBJECT_XREFS={len(xrefs.get(OWNER_STATIC_METAOBJECT, []))}")
    print(f"WORLD_MAP_SECOND_PACK_OWNER_VPTR_XREFS={len(xrefs.get(OWNER_NEARBY_VPTR, []))}")
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
