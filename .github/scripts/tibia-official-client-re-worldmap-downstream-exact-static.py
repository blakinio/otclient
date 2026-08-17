#!/usr/bin/env python3
"""Bounded downstream world-map exact-static evidence producer."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
from typing import Any

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
SOURCE_SCHEMA = "track-a-worldmap-downstream-exact-static-source-v1"
FINAL_SCHEMA = "track-a-worldmap-downstream-exact-static-final-v1"
TASK_ID = "OTC-20260817-track-a-worldmap-downstream-exact-static-evidence"
CONSUMER_PR = 367
MAX_SOURCE_CODE_BYTES = 768 * 1024
MAX_WINDOWS = 256
MAX_SLOT_WINDOWS_PER_TYPE = 48
MAX_DIRECT_CALLERS_PER_FUNCTION = 8
MAX_INDIRECT_SLOT12_WINDOWS = 64
STORAGE_SLOT12_FUNCTION = 0x00CC6CD0
STORAGE_SLOT12_INDEX = 12
STORAGE_SLOT12_DISP = STORAGE_SLOT12_INDEX * 8
TARGETS = {
    "storage": {"vptr": 0x0308CE70, "typeinfo": 0x0308B5F0},
    "render_provider": {"vptr": 0x02F6C258, "typeinfo": 0x03089B70},
    "camera": {"vptr": 0x03083968, "typeinfo": 0x03080500},
    "picker": {"vptr": 0x02F6B7C8, "typeinfo": 0x03086888},
}
WORLD_MAP_ANCHORS = (
    0x00CBF37A, 0x00CC6CD0, 0x00CB0180, 0x00CB01D0,
    0x00CEC8D0, 0x019A8A80, 0x00820970, 0x00DEDDA0, 0x008205C0,
)


def fmt_addr(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:08x}"


def parse_addr(value: str) -> int:
    return int(value, 16)


def load_prior(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("worldmap_prior_v2", path)
    if spec is None or spec.loader is None:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=PRIOR_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.MAX_SOURCE_CODE_BYTES = MAX_SOURCE_CODE_BYTES
    return module


def exact_fence(prior: Any, client: Path) -> tuple[int, str]:
    size, digest = prior.exact_source_fence(client)
    if size != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=EXACT_FENCE")
    return size, digest


def identity(prior: Any, elf: Any, name: str, spec: dict[str, int]) -> dict[str, Any]:
    raw_top = elf.qword(spec["vptr"] - 16)
    typeinfo, typeinfo_relation = elf.resolved_qword(spec["vptr"] - 8)
    name_ptr = None
    name_relation = "UNKNOWN"
    rtti_name = "UNKNOWN"
    if typeinfo is not None:
        name_ptr, name_relation = elf.resolved_qword(typeinfo + 8)
        if name_ptr is not None:
            rtti_name = elf.cstring(name_ptr) or "UNKNOWN"
    signed_top = None
    if raw_top is not None:
        signed_top = raw_top - (1 << 64) if raw_top & (1 << 63) else raw_top
    return {
        "label": name,
        "vptr_address_point": fmt_addr(spec["vptr"]),
        "offset_to_top_raw": fmt_addr(raw_top),
        "offset_to_top_signed": signed_top,
        "typeinfo_pointer": fmt_addr(typeinfo),
        "typeinfo_relation": typeinfo_relation,
        "expected_typeinfo": fmt_addr(spec["typeinfo"]),
        "typeinfo_matches_expected": typeinfo == spec["typeinfo"],
        "typeinfo_name_pointer": fmt_addr(name_ptr),
        "typeinfo_name_relation": name_relation,
        "rtti_name": rtti_name,
        "itanium_layout_consistent": raw_top == 0 and typeinfo == spec["typeinfo"],
    }


def scan_direct_calls(elf: Any, targets: set[int]) -> dict[int, list[int]]:
    out = {target: [] for target in targets}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        pos = 0
        while True:
            idx = blob.find(b"\xe8", pos)
            if idx < 0:
                break
            pos = idx + 1
            if idx + 5 > len(blob):
                continue
            disp = struct.unpack_from("<i", blob, idx + 1)[0]
            address = seg["vaddr"] + idx
            target = address + 5 + disp
            if target in out:
                out[target].append(address)
    return {target: sorted(set(items)) for target, items in out.items()}


def scan_indirect_call_disp(elf: Any, wanted: int) -> list[dict[str, Any]]:
    hits: dict[int, dict[str, Any]] = {}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        for i in range(len(blob) - 8):
            if blob[i] != 0xFF:
                continue
            modrm = blob[i + 1]
            if ((modrm >> 3) & 7) != 2:
                continue
            mod, rm = (modrm >> 6) & 3, modrm & 7
            if mod == 3:
                continue
            p = i + 2
            sib = None
            if rm == 4:
                sib = blob[p]
                p += 1
            disp = None
            if mod == 1:
                disp = struct.unpack_from("<b", blob, p)[0]
            elif mod == 2:
                disp = struct.unpack_from("<i", blob, p)[0]
            elif mod == 0 and rm == 5:
                disp = struct.unpack_from("<i", blob, p)[0]
            elif mod == 0 and rm == 4 and sib is not None and (sib & 7) == 5:
                disp = struct.unpack_from("<i", blob, p)[0]
            if disp != wanted:
                continue
            prefix = 1 if i > 0 and 0x40 <= blob[i - 1] <= 0x4F else 0
            address = seg["vaddr"] + i - prefix
            hits[address] = {
                "instruction_address": fmt_addr(address),
                "modrm": f"0x{modrm:02x}",
                "displacement": fmt_addr(wanted),
            }
    return [hits[key] for key in sorted(hits)]


def scan_pair_hits(elf: Any) -> list[dict[str, Any]]:
    needle = struct.pack("<II", 18, 14)
    out: list[dict[str, Any]] = []
    pos = 0
    while len(out) < 128:
        idx = elf.data.find(needle, pos)
        if idx < 0:
            break
        pos = idx + 1
        address = elf.offset_to_vaddr(idx)
        if address is not None:
            out.append({"address": fmt_addr(address), "executable": elf.executable(address), "bytes": needle.hex()})
    return out


def add_window(prior: Any, windows: list[dict[str, Any]], seen: set[int], elf: Any,
               purpose: str, start: int, size: int, metadata: dict[str, Any], budget: list[int]) -> bool:
    if len(windows) >= MAX_WINDOWS or budget[0] >= MAX_SOURCE_CODE_BYTES:
        return False
    before = len(windows)
    prior.append_window(
        windows, seen, elf,
        purpose=purpose,
        start=start,
        size=size,
        geometry_related=True,
        metadata=metadata,
        raw_budget=budget,
    )
    return len(windows) > before


def build_windows(prior: Any, elf: Any, slots: dict[str, list[dict[str, Any]]],
                  direct_calls: dict[int, list[int]], vptr_xrefs: dict[int, list[dict[str, Any]]],
                  indirect_slot12: list[dict[str, Any]], pair_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []
    seen: set[int] = set()
    budget = [0]

    add_window(prior, windows, seen, elf, "storage_slot12_function", STORAGE_SLOT12_FUNCTION, 0x1800,
               {"type": "storage", "slot_index": STORAGE_SLOT12_INDEX, "function": fmt_addr(STORAGE_SLOT12_FUNCTION)}, budget)

    for type_name in ("render_provider", "camera", "picker"):
        staged = 0
        for slot in slots[type_name]:
            if not slot.get("resolved_executable") or slot.get("resolved") == "UNKNOWN":
                continue
            function = parse_addr(slot["resolved"])
            if add_window(prior, windows, seen, elf, f"{type_name}_vtable_slot", function, 0x900,
                          {"type": type_name, "slot_index": slot["index"], "slot_address": slot["slot_address"], "function": slot["resolved"]}, budget):
                staged += 1
            if staged >= MAX_SLOT_WINDOWS_PER_TYPE:
                break

    for type_name, spec in TARGETS.items():
        for item in vptr_xrefs.get(spec["vptr"], [])[:24]:
            address = parse_addr(item["instruction_address"])
            add_window(prior, windows, seen, elf, f"{type_name}_vptr_xref", max(address - 0x180, 0), 0x700,
                       {"type": type_name, "target_vptr": fmt_addr(spec["vptr"]), "xref": fmt_addr(address)}, budget)

    function_meta: dict[int, tuple[str, int]] = {STORAGE_SLOT12_FUNCTION: ("storage", STORAGE_SLOT12_INDEX)}
    for type_name in ("render_provider", "camera", "picker"):
        for slot in slots[type_name]:
            if slot.get("resolved_executable") and slot.get("resolved") != "UNKNOWN":
                function_meta.setdefault(parse_addr(slot["resolved"]), (type_name, int(slot["index"])))
    for function, (type_name, slot_index) in function_meta.items():
        for call_address in direct_calls.get(function, [])[:MAX_DIRECT_CALLERS_PER_FUNCTION]:
            add_window(prior, windows, seen, elf, f"{type_name}_direct_caller", max(call_address - 0x280, 0), 0x800,
                       {"type": type_name, "slot_index": slot_index, "target_function": fmt_addr(function), "call_address": fmt_addr(call_address)}, budget)

    def distance(item: dict[str, Any]) -> tuple[int, int]:
        address = parse_addr(item["instruction_address"])
        return min(abs(address - anchor) for anchor in WORLD_MAP_ANCHORS), address

    for item in sorted(indirect_slot12, key=distance)[:MAX_INDIRECT_SLOT12_WINDOWS]:
        address = parse_addr(item["instruction_address"])
        add_window(prior, windows, seen, elf, "storage_slot12_indirect_caller_candidate", max(address - 0x380, 0), 0x900,
                   {"call_address": fmt_addr(address), "slot_displacement": fmt_addr(STORAGE_SLOT12_DISP), "anchor_distance": distance(item)[0]}, budget)

    for hit in pair_hits:
        if hit["executable"]:
            address = parse_addr(hit["address"])
            add_window(prior, windows, seen, elf, "packed_18_14_executable_hit", max(address - 0x180, 0), 0x500,
                       {"pair_address": hit["address"], "pair_bytes": hit["bytes"]}, budget)
    return windows


def source_mode(args: argparse.Namespace) -> int:
    prior = load_prior(Path(args.prior_v2))
    client = Path(args.client)
    outdir = Path(args.outdir)
    size, digest = exact_fence(prior, client)
    elf = prior.base.Elf64(client)
    identities = {name: identity(prior, elf, name, spec) for name, spec in TARGETS.items()}
    if not all(item["itanium_layout_consistent"] for item in identities.values()):
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=TARGET_IDENTITY_MISMATCH")

    slots = {name: prior.base.vtable_slots(elf, spec["vptr"], 96) for name, spec in TARGETS.items()}
    functions = {STORAGE_SLOT12_FUNCTION}
    for name in ("render_provider", "camera", "picker"):
        functions.update(parse_addr(slot["resolved"]) for slot in slots[name] if slot.get("resolved_executable") and slot.get("resolved") != "UNKNOWN")
    direct_calls = scan_direct_calls(elf, functions)
    vptr_xrefs = prior.scan_rip_lea_xrefs(elf, {spec["vptr"] for spec in TARGETS.values()})
    indirect = scan_indirect_call_disp(elf, STORAGE_SLOT12_DISP)
    pair_hits = scan_pair_hits(elf)
    windows = build_windows(prior, elf, slots, direct_calls, vptr_xrefs, indirect, pair_hits)
    raw_bytes = sum(item["byte_count"] for item in windows)

    for type_name in ("render_provider", "camera", "picker"):
        if not any(item["purpose"] == f"{type_name}_vtable_slot" for item in windows):
            raise SystemExit(f"WORLD_MAP_DOWNSTREAM_REFUSED=NO_{type_name.upper()}_WINDOWS")
    if not any(item["purpose"] == "storage_slot12_function" for item in windows):
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=NO_STORAGE_SLOT12_WINDOW")

    bundle = {
        "schema": SOURCE_SCHEMA,
        "task_id": TASK_ID,
        "consumer_pr": CONSUMER_PR,
        "client": {"version": EXPECTED_VERSION, "size": size, "sha256": digest, "source_candidate_index": int(args.candidate_index), "source_runner": os.environ.get("RUNNER_NAME", "UNKNOWN")},
        "policy": {"runtime_access": "none", "canonical_state_accessed": False, "client_process_accessed": False, "process_memory_accessed": False, "x11_vnc_accessed": False, "login_session_accessed": False, "gameplay_accessed": False, "client_executed": False, "client_bytes_mutated": False, "raw_client_uploaded": False, "owner_funded_ai_api_used": False, "bounded_sanitized_output_only": True},
        "identities": identities,
        "vtable_slots": slots,
        "direct_calls": {fmt_addr(target): [fmt_addr(address) for address in addresses] for target, addresses in direct_calls.items()},
        "vptr_xrefs": {fmt_addr(target): items for target, items in vptr_xrefs.items()},
        "storage_slot12_indirect_call_candidates": indirect,
        "packed_18_14_hits": pair_hits,
        "code_windows": windows,
        "code_window_raw_bytes": raw_bytes,
        "source_disassembly_backend": "none",
        "hosted_disassembly_required": True,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "downstream-source-evidence.json").write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = [
        "# Downstream world-map exact-static source staging", "",
        f"- client: `{EXPECTED_VERSION}` / `{size}` / `{digest}`",
        f"- windows: `{len(windows)}` / `{raw_bytes}` raw bytes",
        f"- direct callers of Storage slot 12: `{len(direct_calls.get(STORAGE_SLOT12_FUNCTION, []))}`",
        f"- indirect `[reg+0x60]` candidates: `{len(indirect)}`", "",
    ]
    for name, item in identities.items():
        report += [f"- {name}: vptr `{item['vptr_address_point']}`, typeinfo `{item['typeinfo_pointer']}`, RTTI `{item['rtti_name']}`"]
    report += ["", "Semantic conclusions are deferred to hosted bounded disassembly and consumer PR #367.", ""]
    (outdir / "downstream-source-evidence.md").write_text("\n".join(report), encoding="utf-8")
    (outdir / "source-fence.txt").write_text("\n".join([
        f"WORLD_MAP_DOWNSTREAM_CLIENT_VERSION={EXPECTED_VERSION}",
        f"WORLD_MAP_DOWNSTREAM_CLIENT_SIZE={size}",
        f"WORLD_MAP_DOWNSTREAM_CLIENT_SHA256={digest}",
        f"WORLD_MAP_DOWNSTREAM_SOURCE_CANDIDATE_INDEX={int(args.candidate_index)}",
        "WORLD_MAP_DOWNSTREAM_RUNTIME_ACCESS=none",
        "WORLD_MAP_DOWNSTREAM_CLIENT_EXECUTED=false",
        "WORLD_MAP_DOWNSTREAM_PROCESS_MEMORY_ACCESSED=false",
        "WORLD_MAP_DOWNSTREAM_CANONICAL_STATE_ACCESSED=false",
        "WORLD_MAP_DOWNSTREAM_RAW_CLIENT_UPLOADED=false",
        f"WORLD_MAP_DOWNSTREAM_CODE_WINDOWS={len(windows)}",
        f"WORLD_MAP_DOWNSTREAM_CODE_RAW_BYTES={raw_bytes}", "",
    ]), encoding="utf-8")
    print("WORLD_MAP_DOWNSTREAM_SOURCE=PASS")
    print(f"WORLD_MAP_DOWNSTREAM_CODE_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_DOWNSTREAM_CODE_RAW_BYTES={raw_bytes}")
    print(f"WORLD_MAP_DOWNSTREAM_SLOT12_DIRECT_CALLERS={len(direct_calls.get(STORAGE_SLOT12_FUNCTION, []))}")
    print(f"WORLD_MAP_DOWNSTREAM_SLOT12_INDIRECT_CALL_CANDIDATES={len(indirect)}")
    for name in ("render_provider", "camera", "picker"):
        count = sum(1 for item in windows if item["purpose"] == f"{name}_vtable_slot")
        print(f"WORLD_MAP_DOWNSTREAM_{name.upper()}_SLOT_WINDOWS={count}")
    return 0


def validate_source(bundle_dir: Path) -> dict[str, Any]:
    allowed = {"downstream-source-evidence.json", "downstream-source-evidence.md", "source-fence.txt"}
    actual = {path.name for path in bundle_dir.iterdir() if path.is_file()}
    if actual != allowed:
        raise SystemExit(f"WORLD_MAP_DOWNSTREAM_REFUSED=SOURCE_FILE_SET:{sorted(actual)}")
    for path in bundle_dir.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        if len(data) > 8 * 1024 * 1024 or data.startswith(b"\x7fELF") or data[:2] == b"MZ":
            raise SystemExit(f"WORLD_MAP_DOWNSTREAM_REFUSED=UNSAFE_SOURCE_ARTIFACT:{path.name}")
        data.decode("utf-8")
    bundle = json.loads((bundle_dir / "downstream-source-evidence.json").read_text(encoding="utf-8"))
    client = bundle.get("client", {})
    if bundle.get("schema") != SOURCE_SCHEMA or client.get("version") != EXPECTED_VERSION or client.get("size") != EXPECTED_SIZE or client.get("sha256") != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=SOURCE_FENCE")
    if bundle.get("policy", {}).get("runtime_access") != "none" or bundle.get("policy", {}).get("raw_client_uploaded") is not False:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=SOURCE_POLICY")
    raw = sum(len(bytes.fromhex(item["bytes_hex"])) for item in bundle.get("code_windows", []))
    if raw != bundle.get("code_window_raw_bytes") or raw > MAX_SOURCE_CODE_BYTES:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=SOURCE_WINDOW_BUDGET")
    return bundle


def interesting(text: str) -> bool:
    lower = text.lower()
    op = lower.split(None, 1)[0] if lower else ""
    return op in {"call", "cmp", "test", "lea", "imul", "mul", "idiv", "div", "shl", "shr", "sar", "sal", "and", "or", "xor", "sub", "add", "mov", "movq", "movd", "movdqu", "movups", "movaps"} or any(token in lower for token in ("0x12", "0xe", "0x20", "+0x38", "+0x48", "+0x4c"))


def context(records: list[dict[str, Any]], address: int, before: int = 0x180, after: int = 0x90) -> list[dict[str, Any]]:
    selected = [item for item in records if address - before <= item["addr"] <= address + after]
    unique = {(item["addr"], item["text"], item["purpose"]): item for item in selected}
    return [{"address": fmt_addr(item["addr"]), "instruction": item["text"], "purpose": item["purpose"], "metadata": item.get("metadata", {})} for item in sorted(unique.values(), key=lambda x: x["addr"])]


def hosted_mode(args: argparse.Namespace) -> int:
    prior = load_prior(Path(args.prior_v2))
    bundle = validate_source(Path(args.bundle_dir))
    outdir = Path(args.outdir)
    if subprocess.run(["sh", "-c", "command -v objdump >/dev/null 2>&1"], check=False).returncode != 0:
        raise SystemExit("WORLD_MAP_DOWNSTREAM_REFUSED=HOSTED_OBJDUMP_MISSING")
    records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="worldmap-downstream-") as temp:
        root = Path(temp)
        for window in bundle["code_windows"]:
            records.extend(prior.disassemble_window(window, root))

    by_type: dict[str, list[dict[str, Any]]] = {"storage": [], "render_provider": [], "camera": [], "picker": [], "other": []}
    for item in records:
        if not interesting(item["text"]):
            continue
        bucket = "other"
        for name in ("storage", "render_provider", "camera", "picker"):
            if item["purpose"].startswith(name):
                bucket = name
                break
        if len(by_type[bucket]) < 1200:
            by_type[bucket].append({"address": fmt_addr(item["addr"]), "instruction": item["text"], "purpose": item["purpose"], "origin": fmt_addr(item["origin"]), "metadata": item.get("metadata", {})})

    call_sites: list[dict[str, Any]] = []
    direct = [parse_addr(value) for value in bundle.get("direct_calls", {}).get(fmt_addr(STORAGE_SLOT12_FUNCTION), [])]
    for address in direct:
        call_sites.append({"kind": "direct_call_to_storage_slot12", "call_address": fmt_addr(address), "context": context(records, address)})
    staged_indirect = {parse_addr(item["metadata"]["call_address"]) for item in bundle["code_windows"] if item["purpose"] == "storage_slot12_indirect_caller_candidate"}
    for candidate in bundle.get("storage_slot12_indirect_call_candidates", []):
        address = parse_addr(candidate["instruction_address"])
        if address in staged_indirect:
            call_sites.append({"kind": "indirect_virtual_slot12_candidate", "call_address": candidate["instruction_address"], "context": context(records, address)})
        if len(call_sites) >= 96:
            break

    downstream: dict[str, Any] = {}
    for name in ("render_provider", "camera", "picker"):
        executable = [slot for slot in bundle["vtable_slots"][name] if slot.get("resolved_executable")]
        staged = sorted({int(item["metadata"]["slot_index"]) for item in bundle["code_windows"] if item["purpose"] == f"{name}_vtable_slot"})
        downstream[name] = {"identity": bundle["identities"][name], "executable_vtable_slots": executable, "staged_slot_indices": staged, "interesting_instructions": by_type[name]}

    immediate_hits = []
    for item in records:
        text = item["text"].lower()
        if re.search(r"(?<![0-9a-f])0x12(?![0-9a-f])", text) or re.search(r"(?<![0-9a-f])0xe(?![0-9a-f])", text):
            immediate_hits.append({"address": fmt_addr(item["addr"]), "instruction": item["text"], "purpose": item["purpose"], "metadata": item.get("metadata", {})})
            if len(immediate_hits) >= 256:
                break

    ready = bool(call_sites) and all(downstream[name]["staged_slot_indices"] for name in ("render_provider", "camera", "picker"))
    final = {
        "schema": FINAL_SCHEMA,
        "task_id": TASK_ID,
        "consumer_pr": CONSUMER_PR,
        "client": bundle["client"],
        "policy": bundle["policy"],
        "source_summary": {"code_window_count": len(bundle["code_windows"]), "code_window_raw_bytes": bundle["code_window_raw_bytes"], "packed_18_14_hits": bundle["packed_18_14_hits"], "vptr_xrefs": bundle["vptr_xrefs"]},
        "storage_slot12": {"function": fmt_addr(STORAGE_SLOT12_FUNCTION), "slot_index": STORAGE_SLOT12_INDEX, "direct_callers": bundle.get("direct_calls", {}).get(fmt_addr(STORAGE_SLOT12_FUNCTION), []), "indirect_candidate_count": len(bundle.get("storage_slot12_indirect_call_candidates", [])), "staged_call_sites": call_sites, "interesting_instructions": by_type["storage"]},
        "downstream": downstream,
        "bounded_immediate_18_14_instruction_hits": immediate_hits,
        "hosted_validation": {"backend": "gnu_objdump_bounded_binary", "raw_client_present": False, "instruction_records_examined": len(records), "WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY": ready},
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "worldmap-downstream-exact-static-evidence.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Downstream world-map exact-static evidence", "",
        f"- client: `{EXPECTED_VERSION}` / `{EXPECTED_SIZE}` / `{EXPECTED_SHA256}`",
        f"- bounded windows: `{len(bundle['code_windows'])}` / `{bundle['code_window_raw_bytes']}` bytes",
        f"- hosted instruction records: `{len(records)}`",
        f"- `WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY={str(ready).lower()}`", "",
        "## Storage slot-12 caller contexts", "",
    ]
    for site in call_sites[:32]:
        lines += [f"### {site['kind']} @ `{site['call_address']}`"]
        lines += [f"- `{item['address']}` `{item['instruction']}`" for item in site["context"][:48]]
        lines += [""]
    lines += ["## Downstream vtables", ""]
    for name in ("render_provider", "camera", "picker"):
        data = downstream[name]
        lines += [f"### {name}", f"- RTTI: `{data['identity']['rtti_name']}`", f"- staged slot indices: `{','.join(str(x) for x in data['staged_slot_indices'])}`", ""]
        lines += [f"- `{item['address']}` `{item['instruction']}` ({item['purpose']})" for item in data["interesting_instructions"][:160]]
        lines += [""]
    lines += ["## Bounded immediate 18/14 hits", "", f"- hits: `{len(immediate_hits)}`", "", "No semantic field rename or patch design is asserted by this producer.", ""]
    (outdir / "worldmap-downstream-exact-static-evidence.md").write_text("\n".join(lines), encoding="utf-8")
    (outdir / "hosted-validation.txt").write_text("\n".join([
        "WORLD_MAP_DOWNSTREAM_HOSTED_VALIDATION=PASS",
        f"WORLD_MAP_DOWNSTREAM_CLIENT_VERSION={EXPECTED_VERSION}",
        f"WORLD_MAP_DOWNSTREAM_CLIENT_SIZE={EXPECTED_SIZE}",
        f"WORLD_MAP_DOWNSTREAM_CLIENT_SHA256={EXPECTED_SHA256}",
        f"WORLD_MAP_DOWNSTREAM_CODE_WINDOWS={len(bundle['code_windows'])}",
        f"WORLD_MAP_DOWNSTREAM_CODE_RAW_BYTES={bundle['code_window_raw_bytes']}",
        f"WORLD_MAP_DOWNSTREAM_STORAGE_CALL_SITE_CONTEXTS={len(call_sites)}",
        f"WORLD_MAP_DOWNSTREAM_RENDER_PROVIDER_STAGED_SLOTS={len(downstream['render_provider']['staged_slot_indices'])}",
        f"WORLD_MAP_DOWNSTREAM_CAMERA_STAGED_SLOTS={len(downstream['camera']['staged_slot_indices'])}",
        f"WORLD_MAP_DOWNSTREAM_PICKER_STAGED_SLOTS={len(downstream['picker']['staged_slot_indices'])}",
        f"WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY={str(ready).lower()}", "",
    ]), encoding="utf-8")
    print("WORLD_MAP_DOWNSTREAM_HOSTED_VALIDATION=PASS")
    print(f"WORLD_MAP_DOWNSTREAM_STORAGE_CALL_SITE_CONTEXTS={len(call_sites)}")
    print(f"WORLD_MAP_DOWNSTREAM_RENDER_PROVIDER_STAGED_SLOTS={len(downstream['render_provider']['staged_slot_indices'])}")
    print(f"WORLD_MAP_DOWNSTREAM_CAMERA_STAGED_SLOTS={len(downstream['camera']['staged_slot_indices'])}")
    print(f"WORLD_MAP_DOWNSTREAM_PICKER_STAGED_SLOTS={len(downstream['picker']['staged_slot_indices'])}")
    print(f"WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY={str(ready).lower()}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    source = sub.add_parser("source")
    source.add_argument("--client", required=True)
    source.add_argument("--candidate-index", required=True, type=int)
    source.add_argument("--prior-v2", required=True)
    source.add_argument("--outdir", required=True)
    hosted = sub.add_parser("hosted")
    hosted.add_argument("--bundle-dir", required=True)
    hosted.add_argument("--prior-v2", required=True)
    hosted.add_argument("--outdir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return source_mode(args) if args.mode == "source" else hosted_mode(args)


if __name__ == "__main__":
    sys.exit(main())
