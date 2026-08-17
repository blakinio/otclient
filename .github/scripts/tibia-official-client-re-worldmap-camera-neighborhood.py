#!/usr/bin/env python3
"""Bounded exact-camera neighborhood staging for world-map static RE."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
CAMERA_VPTR = 0x03083968
CAMERA_TYPEINFO = 0x03080500
SOURCE_SCHEMA = "track-a-worldmap-camera-neighborhood-source-v1"
FINAL_SCHEMA = "track-a-worldmap-camera-neighborhood-final-v1"
MAX_RAW_BYTES = 512 * 1024
WINDOW_BEFORE = 0x1000
WINDOW_SIZE = 0x5000


def fmt(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:08x}"


def load_prior(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("worldmap_prior_v2", path)
    if spec is None or spec.loader is None:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=PRIOR_IMPORT_SPEC")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def executable_window(elf: Any, start: int, size: int) -> bytes:
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        seg_start = seg["vaddr"]
        seg_end = seg_start + seg["filesz"]
        if seg_start <= start < seg_end:
            count = min(size, seg_end - start)
            return elf.bytes_at(start, count) or b""
    return b""


def source_mode(args: argparse.Namespace) -> int:
    prior = load_prior(Path(args.prior_v2))
    client = Path(args.client)
    size, digest = prior.exact_source_fence(client)
    if size != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=EXACT_FENCE")
    elf = prior.base.Elf64(client)
    ti, ti_rel = elf.resolved_qword(CAMERA_VPTR - 8)
    if elf.qword(CAMERA_VPTR - 16) != 0 or ti != CAMERA_TYPEINFO:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=IDENTITY")
    name_ptr, name_rel = elf.resolved_qword(ti + 8)
    rtti = elf.cstring(name_ptr) if name_ptr is not None else None
    xrefs = prior.scan_rip_lea_xrefs(elf, {CAMERA_VPTR})[CAMERA_VPTR]
    windows: list[dict[str, Any]] = []
    seen: set[int] = set()
    budget = 0
    for item in xrefs:
        xref = int(item["instruction_address"], 16)
        start = max(0, xref - WINDOW_BEFORE)
        if start in seen or budget >= MAX_RAW_BYTES:
            continue
        blob = executable_window(elf, start, min(WINDOW_SIZE, MAX_RAW_BYTES - budget))
        if not blob:
            continue
        seen.add(start)
        budget += len(blob)
        windows.append({
            "purpose": "camera_vptr_neighborhood",
            "xref": item["instruction_address"],
            "start_address": fmt(start),
            "byte_count": len(blob),
            "bytes_hex": blob.hex(),
        })
    bundle = {
        "schema": SOURCE_SCHEMA,
        "client": {"version": EXPECTED_VERSION, "size": size, "sha256": digest, "source_candidate_index": int(args.candidate_index), "source_runner": os.environ.get("RUNNER_NAME", "UNKNOWN")},
        "policy": {"runtime_access": "none", "client_executed": False, "process_memory_accessed": False, "canonical_state_accessed": False, "client_bytes_mutated": False, "raw_client_uploaded": False},
        "camera_identity": {"vptr": fmt(CAMERA_VPTR), "typeinfo": fmt(ti), "typeinfo_relation": ti_rel, "name_pointer": fmt(name_ptr), "name_relation": name_rel, "rtti": rtti or "UNKNOWN"},
        "camera_vptr_xrefs": xrefs,
        "code_windows": windows,
        "code_window_raw_bytes": budget,
    }
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out / "camera-source.json").write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "camera-source.md").write_text("\n".join([
        "# TWorldMapCamera bounded neighborhood source staging", "",
        f"- exact RTTI: `{rtti or 'UNKNOWN'}`", f"- exact vptr xrefs: `{len(xrefs)}`", f"- windows: `{len(windows)}` / `{budget}` bytes", ""
    ]), encoding="utf-8")
    (out / "source-fence.txt").write_text("\n".join([
        f"WORLD_MAP_CAMERA_CLIENT_VERSION={EXPECTED_VERSION}", f"WORLD_MAP_CAMERA_CLIENT_SIZE={size}", f"WORLD_MAP_CAMERA_CLIENT_SHA256={digest}",
        "WORLD_MAP_CAMERA_RUNTIME_ACCESS=none", "WORLD_MAP_CAMERA_CLIENT_EXECUTED=false", "WORLD_MAP_CAMERA_PROCESS_MEMORY_ACCESSED=false", "WORLD_MAP_CAMERA_CANONICAL_STATE_ACCESSED=false", "WORLD_MAP_CAMERA_RAW_CLIENT_UPLOADED=false",
        f"WORLD_MAP_CAMERA_XREFS={len(xrefs)}", f"WORLD_MAP_CAMERA_CODE_WINDOWS={len(windows)}", f"WORLD_MAP_CAMERA_CODE_RAW_BYTES={budget}", ""
    ]), encoding="utf-8")
    print("WORLD_MAP_CAMERA_SOURCE=PASS")
    print(f"WORLD_MAP_CAMERA_XREFS={len(xrefs)}")
    print(f"WORLD_MAP_CAMERA_CODE_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_CAMERA_CODE_RAW_BYTES={budget}")
    return 0


def disasm(window: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    start = int(window["start_address"], 16)
    path = root / f"camera-{start:08x}.bin"
    path.write_bytes(bytes.fromhex(window["bytes_hex"]))
    cp = subprocess.run([
        "objdump", "-D", "-b", "binary", "-m", "i386:x86-64", "-M", "intel", "--no-show-raw-insn",
        f"--adjust-vma={start}", str(path)
    ], check=False, text=True, capture_output=True, errors="replace", timeout=60)
    if cp.returncode != 0:
        raise SystemExit(f"WORLD_MAP_CAMERA_REFUSED=OBJDUMP:{cp.returncode}")
    out: list[dict[str, Any]] = []
    for line in cp.stdout.splitlines():
        m = re.match(r"^\s*([0-9a-fA-F]+):\s*(.*?)\s*$", line)
        if not m:
            continue
        text = m.group(2).strip()
        if not text:
            continue
        out.append({"address": fmt(int(m.group(1), 16)), "instruction": text, "xref_origin": window["xref"], "window_start": window["start_address"]})
    return out


def hosted_mode(args: argparse.Namespace) -> int:
    root = Path(args.bundle_dir)
    allowed = {"camera-source.json", "camera-source.md", "source-fence.txt"}
    actual = {p.name for p in root.iterdir() if p.is_file()}
    if actual != allowed:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=SOURCE_FILES")
    bundle = json.loads((root / "camera-source.json").read_text(encoding="utf-8"))
    c = bundle.get("client", {})
    if bundle.get("schema") != SOURCE_SCHEMA or c.get("version") != EXPECTED_VERSION or c.get("size") != EXPECTED_SIZE or c.get("sha256") != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=SOURCE_FENCE")
    if subprocess.run(["sh", "-c", "command -v objdump >/dev/null 2>&1"], check=False).returncode != 0:
        raise SystemExit("WORLD_MAP_CAMERA_REFUSED=OBJDUMP_MISSING")
    records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="wm-camera-") as td:
        tmp = Path(td)
        for window in bundle["code_windows"]:
            records.extend(disasm(window, tmp))
    # Deduplicate overlapping neighborhoods while retaining first origin.
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for item in records:
        unique.setdefault((item["address"], item["instruction"]), item)
    records = [unique[key] for key in sorted(unique, key=lambda x: int(x[0], 16))]
    # Extract displacement-oriented candidates only; semantic type anchoring is performed manually in the durable handoff.
    interesting = []
    for item in records:
        text = item["instruction"].lower()
        if any(token in text for token in ("+0x98", "+0xa0", "+0xa8", "+0xb0", "+0xb8", "+0xc0", "+0xc8", "+0xd0", "+0xd4", "+0x138", "+0x148", "0x3f800000")):
            interesting.append(item)
    final = {
        "schema": FINAL_SCHEMA,
        "client": bundle["client"],
        "policy": bundle["policy"],
        "camera_identity": bundle["camera_identity"],
        "camera_vptr_xrefs": bundle["camera_vptr_xrefs"],
        "window_count": len(bundle["code_windows"]),
        "raw_bytes": bundle["code_window_raw_bytes"],
        "instruction_record_count": len(records),
        "interesting_displacement_records": interesting,
        "disassembly_records": records,
        "hosted_validation": {"backend": "gnu_objdump_bounded_binary", "raw_client_present": False, "pass": True},
    }
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    (out / "worldmap-camera-neighborhood-evidence.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "worldmap-camera-neighborhood-evidence.md").write_text("\n".join([
        "# TWorldMapCamera bounded neighborhood evidence", "",
        f"- exact xrefs: `{len(bundle['camera_vptr_xrefs'])}`", f"- windows: `{len(bundle['code_windows'])}` / `{bundle['code_window_raw_bytes']}` bytes",
        f"- unique instructions: `{len(records)}`", f"- displacement-oriented candidates: `{len(interesting)}`", "",
        "Semantic classification is intentionally deferred to the curated consumer handoff.", ""
    ]), encoding="utf-8")
    (out / "hosted-validation.txt").write_text("\n".join([
        "WORLD_MAP_CAMERA_HOSTED_VALIDATION=PASS", f"WORLD_MAP_CAMERA_CLIENT_VERSION={EXPECTED_VERSION}", f"WORLD_MAP_CAMERA_CLIENT_SIZE={EXPECTED_SIZE}", f"WORLD_MAP_CAMERA_CLIENT_SHA256={EXPECTED_SHA256}",
        f"WORLD_MAP_CAMERA_INSTRUCTION_RECORDS={len(records)}", f"WORLD_MAP_CAMERA_INTERESTING_RECORDS={len(interesting)}", ""
    ]), encoding="utf-8")
    print("WORLD_MAP_CAMERA_HOSTED_VALIDATION=PASS")
    print(f"WORLD_MAP_CAMERA_INSTRUCTION_RECORDS={len(records)}")
    print(f"WORLD_MAP_CAMERA_INTERESTING_RECORDS={len(interesting)}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("source"); s.add_argument("--client", required=True); s.add_argument("--candidate-index", required=True, type=int); s.add_argument("--prior-v2", required=True); s.add_argument("--outdir", required=True)
    h = sub.add_parser("hosted"); h.add_argument("--bundle-dir", required=True); h.add_argument("--outdir", required=True)
    a = p.parse_args(); return source_mode(a) if a.mode == "source" else hosted_mode(a)

if __name__ == "__main__":
    sys.exit(main())
