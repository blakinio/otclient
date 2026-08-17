#!/usr/bin/env python3
"""Narrow exact-file discriminator for downstream world-map ownership/data edges."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
from typing import Any

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
SOURCE_SCHEMA = "track-a-worldmap-downstream-targeted-source-v1"
FINAL_SCHEMA = "track-a-worldmap-downstream-targeted-final-v1"
TARGETS = {
    "handler": {"vptr": 0x030871D8, "typeinfo": 0x03085FB8},
    "viewport": {"vptr": 0x0308C9A8, "typeinfo": 0x0308B590},
    "storage": {"vptr": 0x0308CE70, "typeinfo": 0x0308B5F0},
}
FUNCTIONS = {
    "candidate_geometry_fanout": 0x00CDB770,
    "geometry_snapshot_builder": 0x00BC6350,
    "viewport_ctor": 0x00CBF680,
    "viewport_recompute": 0x00CBF700,
    "storage_slot12": 0x00CC6CD0,
}
DATA_POINTS = {
    "viewport_extent_ctor_pair": 0x01CDD958,
    "viewport_ctor_xy_seed": 0x01D32EF0,
    "viewport_secondary_seed": 0x01D6BAA8,
    "viewport_recompute_delta": 0x01D63CD0,
    "signed_div32_round_mask": 0x01CE70C8,
}
MAX_CODE_BYTES = 256 * 1024


def fmt(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:08x}"


def load_prior(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("worldmap_prior_v2", path)
    if spec is None or spec.loader is None:
        raise SystemExit("WORLD_MAP_TARGETED_REFUSED=PRIOR_IMPORT_SPEC")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fence(prior: Any, client: Path) -> tuple[int, str]:
    size, digest = prior.exact_source_fence(client)
    if size != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_TARGETED_REFUSED=EXACT_FENCE")
    return size, digest


def typeinfo_name(elf: Any, typeinfo: int) -> tuple[int | None, str]:
    name_ptr, _rel = elf.resolved_qword(typeinfo + 8)
    return name_ptr, (elf.cstring(name_ptr) if name_ptr is not None else None) or "UNKNOWN"


def identity(elf: Any, name: str, spec: dict[str, int]) -> dict[str, Any]:
    raw_top = elf.qword(spec["vptr"] - 16)
    ti, ti_rel = elf.resolved_qword(spec["vptr"] - 8)
    name_ptr, rtti = typeinfo_name(elf, ti) if ti is not None else (None, "UNKNOWN")
    return {
        "label": name,
        "vptr": fmt(spec["vptr"]),
        "offset_to_top": 0 if raw_top == 0 else raw_top,
        "typeinfo": fmt(ti),
        "expected_typeinfo": fmt(spec["typeinfo"]),
        "typeinfo_relation": ti_rel,
        "rtti_name_pointer": fmt(name_ptr),
        "rtti_name": rtti,
        "consistent": raw_top == 0 and ti == spec["typeinfo"],
    }


def qword_occurrences(elf: Any, value: int, limit: int = 1024) -> list[int]:
    needle = struct.pack("<Q", value)
    out: list[int] = []
    pos = 0
    while len(out) < limit:
        idx = elf.data.find(needle, pos)
        if idx < 0:
            break
        pos = idx + 1
        addr = elf.offset_to_vaddr(idx)
        if addr is not None:
            out.append(addr)
    return sorted(set(out))


def reverse_vtable_owners(elf: Any, function: int) -> list[dict[str, Any]]:
    owners: dict[tuple[int, int], dict[str, Any]] = {}
    for slot_addr in qword_occurrences(elf, function, 2048):
        if elf.executable(slot_addr):
            continue
        for slot_index in range(0, 128):
            address_point = slot_addr - slot_index * 8
            header = address_point - 16
            raw_top = elf.qword(header)
            if raw_top is None:
                continue
            signed_top = raw_top - (1 << 64) if raw_top & (1 << 63) else raw_top
            if not (-0x100000 <= signed_top <= 0x100000):
                continue
            ti, ti_rel = elf.resolved_qword(header + 8)
            if ti is None or not elf.mapped(ti):
                continue
            name_ptr, rtti = typeinfo_name(elf, ti)
            if rtti == "UNKNOWN" or len(rtti) > 400:
                continue
            if not (rtti.startswith("N") or rtti.startswith("St") or rtti.startswith("Z") or "tibia" in rtti):
                continue
            key = (address_point, slot_index)
            owners[key] = {
                "function": fmt(function),
                "slot_address": fmt(slot_addr),
                "address_point": fmt(address_point),
                "slot_index": slot_index,
                "offset_to_top": signed_top,
                "typeinfo": fmt(ti),
                "typeinfo_relation": ti_rel,
                "typeinfo_name_pointer": fmt(name_ptr),
                "rtti_name": rtti,
            }
            break
    return [owners[key] for key in sorted(owners)]


def direct_calls(elf: Any, targets: set[int]) -> dict[int, list[int]]:
    out = {target: [] for target in targets}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        for i in range(0, max(0, len(blob)-5)):
            if blob[i] != 0xE8:
                continue
            disp = struct.unpack_from("<i", blob, i + 1)[0]
            addr = seg["vaddr"] + i
            target = addr + 5 + disp
            if target in out:
                out[target].append(addr)
    return {target: sorted(set(items))[:256] for target, items in out.items()}


def code_window(elf: Any, start: int, size: int) -> bytes:
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        if seg["vaddr"] <= start < seg["vaddr"] + seg["filesz"]:
            count = min(size, seg["vaddr"] + seg["filesz"] - start)
            blob = elf.bytes_at(start, count)
            return blob or b""
    return b""


def source_mode(args: argparse.Namespace) -> int:
    prior = load_prior(Path(args.prior_v2))
    client = Path(args.client)
    size, digest = fence(prior, client)
    elf = prior.base.Elf64(client)
    identities = {name: identity(elf, name, spec) for name, spec in TARGETS.items()}
    if not all(item["consistent"] for item in identities.values()):
        raise SystemExit("WORLD_MAP_TARGETED_REFUSED=IDENTITY")

    vtables = {name: prior.base.vtable_slots(elf, spec["vptr"], 96) for name, spec in TARGETS.items()}
    reverse = {name: reverse_vtable_owners(elf, addr) for name, addr in FUNCTIONS.items()}
    calls = direct_calls(elf, set(FUNCTIONS.values()))
    data: dict[str, Any] = {}
    for name, addr in DATA_POINTS.items():
        blob = elf.bytes_at(addr, 32) or b""
        data[name] = {"address": fmt(addr), "bytes_32_hex": blob.hex(), "qword0": fmt(elf.qword(addr)), "qword1": fmt(elf.qword(addr+8)), "mapped": bool(blob)}

    windows: list[dict[str, Any]] = []
    budget = 0
    fixed_sizes = {
        "candidate_geometry_fanout": 0x1400,
        "geometry_snapshot_builder": 0x1800,
        "viewport_ctor": 0x900,
        "viewport_recompute": 0x900,
        "storage_slot12": 0x800,
    }
    for name, addr in FUNCTIONS.items():
        blob = code_window(elf, addr, fixed_sizes[name])
        if blob and budget + len(blob) <= MAX_CODE_BYTES:
            windows.append({"purpose": name, "start_address": fmt(addr), "byte_count": len(blob), "bytes_hex": blob.hex()})
            budget += len(blob)
    # Stage only primary executable slots for handler/viewport until the first clear metadata boundary.
    for type_name in ("handler", "viewport"):
        staged = 0
        for slot in vtables[type_name]:
            if not slot.get("resolved_executable") or slot.get("resolved") == "UNKNOWN":
                if staged:
                    break
                continue
            addr = int(slot["resolved"], 16)
            blob = code_window(elf, addr, 0x800)
            if blob and budget + len(blob) <= MAX_CODE_BYTES:
                windows.append({"purpose": f"{type_name}_vtable_slot", "start_address": fmt(addr), "byte_count": len(blob), "bytes_hex": blob.hex(), "slot_index": slot["index"], "slot_address": slot["slot_address"]})
                budget += len(blob)
                staged += 1
            if staged >= 48:
                break

    bundle = {
        "schema": SOURCE_SCHEMA,
        "client": {"version": EXPECTED_VERSION, "size": size, "sha256": digest, "source_candidate_index": int(args.candidate_index), "source_runner": os.environ.get("RUNNER_NAME", "UNKNOWN")},
        "policy": {"runtime_access": "none", "client_executed": False, "process_memory_accessed": False, "canonical_state_accessed": False, "client_bytes_mutated": False, "raw_client_uploaded": False},
        "identities": identities,
        "vtable_slots": vtables,
        "reverse_vtable_owners": reverse,
        "direct_calls": {fmt(target): [fmt(x) for x in items] for target, items in calls.items()},
        "data_points": data,
        "code_windows": windows,
        "code_window_raw_bytes": budget,
    }
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out / "targeted-source.json").write_text(json.dumps(bundle, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    (out / "source-fence.txt").write_text("\n".join([
        f"WORLD_MAP_TARGETED_CLIENT_VERSION={EXPECTED_VERSION}", f"WORLD_MAP_TARGETED_CLIENT_SIZE={size}", f"WORLD_MAP_TARGETED_CLIENT_SHA256={digest}",
        "WORLD_MAP_TARGETED_RUNTIME_ACCESS=none", "WORLD_MAP_TARGETED_CLIENT_EXECUTED=false", "WORLD_MAP_TARGETED_PROCESS_MEMORY_ACCESSED=false", "WORLD_MAP_TARGETED_CANONICAL_STATE_ACCESSED=false", "WORLD_MAP_TARGETED_RAW_CLIENT_UPLOADED=false",
        f"WORLD_MAP_TARGETED_CODE_WINDOWS={len(windows)}", f"WORLD_MAP_TARGETED_CODE_RAW_BYTES={budget}", ""
    ]), encoding="utf-8")
    md=["# Targeted world-map source discriminator","",f"- windows: `{len(windows)}` / `{budget}` bytes",""]
    for name, owners in reverse.items():
        md.append(f"- reverse vtable owners `{name}`: `{len(owners)}`")
    md += ["", f"- viewport 18/14 data: `{data['viewport_extent_ctor_pair']['bytes_32_hex'][:16]}` at `0x01cdd958`", ""]
    (out / "targeted-source.md").write_text("\n".join(md), encoding="utf-8")
    print("WORLD_MAP_TARGETED_SOURCE=PASS")
    print(f"WORLD_MAP_TARGETED_CODE_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_TARGETED_CODE_RAW_BYTES={budget}")
    for name, owners in reverse.items(): print(f"WORLD_MAP_TARGETED_REVERSE_{name.upper()}={len(owners)}")
    return 0


def disasm(window: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    start=int(window["start_address"],16); blob=bytes.fromhex(window["bytes_hex"])
    path=root/f"{start:08x}.bin"; path.write_bytes(blob)
    cp=subprocess.run(["objdump","-D","-b","binary","-m","i386:x86-64","-M","intel","--no-show-raw-insn",f"--adjust-vma={start}",str(path)],capture_output=True,text=True,errors="replace",timeout=60)
    if cp.returncode: raise SystemExit(f"WORLD_MAP_TARGETED_REFUSED=OBJDUMP:{cp.returncode}")
    out=[]
    for line in cp.stdout.splitlines():
        line=line.strip()
        if ":" not in line: continue
        left,right=line.split(":",1)
        try: addr=int(left.strip(),16)
        except ValueError: continue
        text=right.strip()
        if text: out.append({"address":fmt(addr),"instruction":text,"purpose":window["purpose"],"slot_index":window.get("slot_index")})
    return out


def hosted_mode(args: argparse.Namespace) -> int:
    root=Path(args.bundle_dir)
    actual={p.name for p in root.iterdir() if p.is_file()}
    if actual != {"targeted-source.json","targeted-source.md","source-fence.txt"}: raise SystemExit("WORLD_MAP_TARGETED_REFUSED=SOURCE_FILES")
    bundle=json.loads((root/"targeted-source.json").read_text())
    c=bundle.get("client",{})
    if bundle.get("schema")!=SOURCE_SCHEMA or c.get("version")!=EXPECTED_VERSION or c.get("size")!=EXPECTED_SIZE or c.get("sha256")!=EXPECTED_SHA256: raise SystemExit("WORLD_MAP_TARGETED_REFUSED=SOURCE_FENCE")
    if subprocess.run(["sh","-c","command -v objdump >/dev/null 2>&1"]).returncode: raise SystemExit("WORLD_MAP_TARGETED_REFUSED=OBJDUMP_MISSING")
    records=[]
    with tempfile.TemporaryDirectory(prefix="wm-targeted-") as td:
        t=Path(td)
        for w in bundle["code_windows"]: records.extend(disasm(w,t))
    final={"schema":FINAL_SCHEMA,"client":bundle["client"],"policy":bundle["policy"],"identities":bundle["identities"],"vtable_slots":bundle["vtable_slots"],"reverse_vtable_owners":bundle["reverse_vtable_owners"],"direct_calls":bundle["direct_calls"],"data_points":bundle["data_points"],"disassembly_records":records,"hosted_validation":{"backend":"gnu_objdump_bounded_binary","raw_client_present":False,"record_count":len(records),"pass":True}}
    out=Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out/"worldmap-downstream-targeted-evidence.json").write_text(json.dumps(final,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (out/"hosted-validation.txt").write_text("\n".join(["WORLD_MAP_TARGETED_HOSTED_VALIDATION=PASS",f"WORLD_MAP_TARGETED_CLIENT_VERSION={EXPECTED_VERSION}",f"WORLD_MAP_TARGETED_CLIENT_SIZE={EXPECTED_SIZE}",f"WORLD_MAP_TARGETED_CLIENT_SHA256={EXPECTED_SHA256}",f"WORLD_MAP_TARGETED_RECORDS={len(records)}",""]),encoding="utf-8")
    md=["# Targeted downstream world-map evidence","",f"- hosted records: `{len(records)}`",""]
    for name, owners in final["reverse_vtable_owners"].items():
        md.append(f"## reverse owners: {name}")
        for o in owners[:24]: md.append(f"- vptr `{o['address_point']}` slot `{o['slot_index']}` typeinfo `{o['typeinfo']}` RTTI `{o['rtti_name']}`")
        md.append("")
    md += ["## data",f"- `0x01cdd958`: `{final['data_points']['viewport_extent_ctor_pair']['bytes_32_hex']}`",""]
    (out/"worldmap-downstream-targeted-evidence.md").write_text("\n".join(md),encoding="utf-8")
    print("WORLD_MAP_TARGETED_HOSTED_VALIDATION=PASS")
    print(f"WORLD_MAP_TARGETED_RECORDS={len(records)}")
    return 0


def main() -> int:
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="mode",required=True)
    s=sub.add_parser("source"); s.add_argument("--client",required=True); s.add_argument("--candidate-index",type=int,required=True); s.add_argument("--prior-v2",required=True); s.add_argument("--outdir",required=True)
    h=sub.add_parser("hosted"); h.add_argument("--bundle-dir",required=True); h.add_argument("--outdir",required=True)
    a=p.parse_args(); return source_mode(a) if a.mode=="source" else hosted_mode(a)

if __name__=="__main__": sys.exit(main())
