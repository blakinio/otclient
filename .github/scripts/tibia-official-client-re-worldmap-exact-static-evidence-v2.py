#!/usr/bin/env python3
"""Disassembler-free source staging plus hosted bounded-window world-map analysis."""

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

BASE_PATH = Path(__file__).with_name("tibia-official-client-re-worldmap-exact-static-evidence.py")
SPEC = importlib.util.spec_from_file_location("worldmap_exact_static_v1", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=BASE_IMPORT_SPEC")
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)

SCHEMA = "track-a-worldmap-exact-static-evidence-v2"
HOSTED_SCHEMA = "track-a-worldmap-exact-static-hosted-validation-v2"
MAX_SOURCE_CODE_BYTES = 256 * 1024
REG64 = (
    "rax", "rcx", "rdx", "rbx", "rsp", "rbp", "rsi", "rdi",
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
)


def fmt_addr(value: int) -> str:
    return f"0x{value:08x}"


def parse_addr(value: str) -> int:
    return int(value, 16)


def exact_source_fence(client: Path) -> tuple[int, str]:
    if not client.is_file() or client.is_symlink():
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=SOURCE_NOT_REGULAR")
    size = client.stat().st_size
    digest = base.sha256_file(client)
    if size != base.EXPECTED_SIZE:
        raise SystemExit(f"WORLD_MAP_STATIC_V2_REFUSED=SIZE:{size}")
    if digest != base.EXPECTED_SHA256:
        raise SystemExit(f"WORLD_MAP_STATIC_V2_REFUSED=SHA256:{digest}")
    return size, digest


def scan_rip_lea_xrefs(elf: Any, targets: set[int]) -> dict[int, list[dict[str, Any]]]:
    """Find canonical x86-64 REX.W LEA reg,[RIP+disp32] references without a disassembler."""
    out: dict[int, list[dict[str, Any]]] = {target: [] for target in targets}
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        blob = elf.data[seg["offset"]:seg["offset"] + seg["filesz"]]
        pos = 1
        while True:
            opcode_index = blob.find(b"\x8d", pos)
            if opcode_index < 0:
                break
            pos = opcode_index + 1
            if opcode_index < 1 or opcode_index + 6 > len(blob):
                continue
            rex = blob[opcode_index - 1]
            modrm = blob[opcode_index + 1]
            if not (0x48 <= rex <= 0x4F):
                continue
            if (modrm & 0xC7) != 0x05:
                continue
            start_index = opcode_index - 1
            address = seg["vaddr"] + start_index
            disp = struct.unpack_from("<i", blob, opcode_index + 2)[0]
            target = address + 7 + disp
            if target not in out:
                continue
            reg = ((modrm >> 3) & 0x7) + (8 if rex & 0x4 else 0)
            instruction = blob[start_index:start_index + 7]
            out[target].append({
                "instruction_address": fmt_addr(address),
                "instruction_bytes": instruction.hex(),
                "decoded_form": f"lea {REG64[reg]},[rip+disp32]",
                "resolved_target": fmt_addr(target),
                "method": "x86_64_rexw_lea_rip_disp32_exact_decode",
            })
    for target in out:
        unique: dict[int, dict[str, Any]] = {}
        for rec in out[target]:
            unique[parse_addr(rec["instruction_address"])] = rec
        out[target] = [unique[key] for key in sorted(unique)][:64]
    return out


def executable_window(elf: Any, start: int, requested: int) -> bytes | None:
    for seg in elf.loads:
        if not (seg["flags"] & 1):
            continue
        seg_start = seg["vaddr"]
        seg_end = seg_start + seg["filesz"]
        if not (seg_start <= start < seg_end):
            continue
        count = min(requested, seg_end - start)
        return elf.bytes_at(start, count)
    return None


def append_window(windows: list[dict[str, Any]], seen: set[int], elf: Any, *,
                  purpose: str, start: int, size: int, geometry_related: bool,
                  metadata: dict[str, Any], raw_budget: list[int]) -> None:
    if start in seen or raw_budget[0] >= MAX_SOURCE_CODE_BYTES:
        return
    blob = executable_window(elf, start, min(size, MAX_SOURCE_CODE_BYTES - raw_budget[0]))
    if not blob:
        return
    seen.add(start)
    raw_budget[0] += len(blob)
    windows.append({
        "purpose": purpose,
        "start_address": fmt_addr(start),
        "byte_count": len(blob),
        "bytes_hex": blob.hex(),
        "geometry_related": geometry_related,
        "metadata": metadata,
    })


def source_code_windows(elf: Any, xrefs: dict[int, list[dict[str, Any]]],
                        geometry_slots: list[dict[str, Any]], rtti_graph: list[dict[str, Any]]) -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []
    seen: set[int] = set()
    budget = [0]

    for target in sorted(xrefs):
        for rec in xrefs[target][:16]:
            start = parse_addr(rec["instruction_address"])
            append_window(
                windows, seen, elf,
                purpose="direct_vptr_xref",
                start=start,
                size=0x700 if target == base.GEOMETRY_VPTR else 0x380,
                geometry_related=(target == base.GEOMETRY_VPTR),
                metadata={"target_vptr": fmt_addr(target)},
                raw_budget=budget,
            )

    for slot in geometry_slots:
        if not slot.get("resolved_executable") or slot.get("resolved") == "UNKNOWN":
            continue
        start = parse_addr(slot["resolved"])
        append_window(
            windows, seen, elf,
            purpose="geometry_vtable_function",
            start=start,
            size=0x480,
            geometry_related=True,
            metadata={"vtable_slot_index": slot["index"], "geometry_vptr": fmt_addr(base.GEOMETRY_VPTR)},
            raw_budget=budget,
        )

    follow_on_count = 0
    for record in rtti_graph:
        for typeinfo in record.get("typeinfos", []):
            for vtable in typeinfo.get("vtables", []):
                target = vtable.get("first_slot_resolved")
                if not vtable.get("first_slot_executable") or target in {None, "UNKNOWN"}:
                    continue
                start = parse_addr(target)
                append_window(
                    windows, seen, elf,
                    purpose="follow_on_rtti_vtable_first_slot",
                    start=start,
                    size=0x380,
                    geometry_related=False,
                    metadata={
                        "token": record.get("token"),
                        "rtti_string": record.get("rtti_string"),
                        "typeinfo_address": typeinfo.get("typeinfo_address"),
                        "vptr_address_point": vtable.get("vptr_address_point"),
                    },
                    raw_budget=budget,
                )
                follow_on_count += 1
                if follow_on_count >= 24:
                    return windows
    return windows


def empty_geometry(geometry_slots: list[dict[str, Any]], xrefs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "geometry_vptr": fmt_addr(base.GEOMETRY_VPTR),
        "vtable_slots": geometry_slots,
        "origin_count": len(xrefs) + sum(1 for s in geometry_slots if s.get("resolved_executable")),
        "origins": [
            {"kind": "direct_vptr_xref_raw_decode", "address": x["instruction_address"]}
            for x in xrefs
        ],
        "field_evidence": {f"+0x{o:x}": [] for o in base.GEOMETRY_OFFSETS},
        "priority_values": {
            f"+0x{o:x}": {
                "expected_decimal": expected,
                "expected_hex": f"0x{expected:x}",
                "direct_immediate_write_observed": False,
                "observations": [],
            }
            for o, expected in base.PRIORITY_IMMEDIATES.items()
        },
        "offsets_with_type_affine_evidence": [],
        "bounded_observation_count": 0,
        "source_disassembly_backend": "none",
    }


def source_mode(args: argparse.Namespace) -> int:
    client = Path(args.client)
    outdir = Path(args.outdir)
    size, digest = exact_source_fence(client)
    elf = base.Elf64(client)
    identities = [base.identity_record(elf, spec) for spec in base.IDENTITIES]
    targets = {int(spec["vptr"]) for spec in base.IDENTITIES}
    xrefs = scan_rip_lea_xrefs(elf, targets)
    geometry_slots = base.vtable_slots(elf, base.GEOMETRY_VPTR, 32)
    rtti_graph = base.build_rtti_graph(elf)
    windows = source_code_windows(elf, xrefs, geometry_slots, rtti_graph)
    geometry = empty_geometry(geometry_slots, xrefs.get(base.GEOMETRY_VPTR, []))
    recovered = sum(1 for item in identities if item.get("window_recovered"))

    direct = {
        fmt_addr(target): [
            {
                "instruction_address": rec["instruction_address"],
                "instruction": (
                    f"{rec['decoded_form']} # {target:x}; bytes={rec['instruction_bytes']}"
                ),
                "instruction_bytes": rec["instruction_bytes"],
                "resolved_target": rec["resolved_target"],
                "method": rec["method"],
            }
            for rec in records
        ]
        for target, records in xrefs.items()
    }

    bundle = {
        "schema": SCHEMA,
        "task_id": base.TASK_ID,
        "consumer_pr": base.CONSUMER_PR,
        "client": {
            "version": base.EXPECTED_VERSION,
            "size": size,
            "sha256": digest,
            "source_candidate_index": int(args.candidate_index),
            "source_runner": os.environ.get("RUNNER_NAME", "UNKNOWN"),
            "elf_machine": elf.e_machine,
        },
        "policy": {
            "runtime_access": "none",
            "canonical_runtime_accessed": False,
            "client_executed": False,
            "client_bytes_mutated": False,
            "process_memory_accessed": False,
            "x11_vnc_accessed": False,
            "login_session_accessed": False,
            "network_accessed_by_analyzer": False,
            "gameplay_accessed": False,
            "raw_client_uploaded": False,
            "bounded_sanitized_output_only": True,
        },
        "identity_windows": identities,
        "direct_vptr_xrefs": direct,
        "geometry": geometry,
        "rtti_graph": rtti_graph,
        "source_code_windows": windows,
        "source_code_window_raw_bytes": sum(item["byte_count"] for item in windows),
        "source_xref_decoder": "x86_64_rexw_lea_rip_disp32_exact_decode",
        "hosted_disassembly_required": True,
        "readiness": {
            "identity_windows_recovered": recovered,
            "geometry_offsets_with_evidence": [],
            "priority_0x48_18_write": False,
            "priority_0x4c_14_write": False,
            "WORLD_MAP_STATIC_EVIDENCE_READY": False,
        },
    }

    outdir.mkdir(parents=True, exist_ok=True)
    report = base.markdown_report(bundle)
    (outdir / "worldmap-static-evidence.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (outdir / "worldmap-static-evidence.md").write_text(report, encoding="utf-8")
    (outdir / "source-fence.txt").write_text("\n".join([
        f"WORLD_MAP_STATIC_CLIENT_VERSION={base.EXPECTED_VERSION}",
        f"WORLD_MAP_STATIC_CLIENT_SIZE={size}",
        f"WORLD_MAP_STATIC_CLIENT_SHA256={digest}",
        f"WORLD_MAP_STATIC_SOURCE_CANDIDATE_INDEX={int(args.candidate_index)}",
        f"WORLD_MAP_STATIC_SOURCE_RUNNER={os.environ.get('RUNNER_NAME', 'UNKNOWN')}",
        "WORLD_MAP_STATIC_RUNTIME_ACCESS=none",
        "WORLD_MAP_STATIC_CLIENT_EXECUTED=false",
        "WORLD_MAP_STATIC_CLIENT_BYTES_MUTATED=false",
        "WORLD_MAP_STATIC_PROCESS_MEMORY_ACCESSED=false",
        "WORLD_MAP_STATIC_CANONICAL_RUNTIME_ACCESSED=false",
        "WORLD_MAP_STATIC_RAW_CLIENT_UPLOADED=false",
        f"WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED={recovered}",
        f"WORLD_MAP_STATIC_DIRECT_GEOMETRY_VPTR_XREF_COUNT={len(xrefs.get(base.GEOMETRY_VPTR, []))}",
        f"WORLD_MAP_STATIC_BOUNDED_CODE_WINDOWS={len(windows)}",
        f"WORLD_MAP_STATIC_BOUNDED_CODE_RAW_BYTES={bundle['source_code_window_raw_bytes']}",
        "WORLD_MAP_STATIC_SOURCE_DISASSEMBLY=none",
        "WORLD_MAP_STATIC_HOSTED_DISASSEMBLY_REQUIRED=true",
        "WORLD_MAP_STATIC_EVIDENCE_READY=false",
        "",
    ]), encoding="utf-8")
    print("WORLD_MAP_STATIC_SOURCE_V2=PASS")
    print(f"WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED={recovered}")
    for target in sorted(xrefs):
        print(f"WORLD_MAP_STATIC_DIRECT_VPTR_XREF_COUNT_{target:08X}={len(xrefs[target])}")
    print(f"WORLD_MAP_STATIC_BOUNDED_CODE_WINDOWS={len(windows)}")
    print(f"WORLD_MAP_STATIC_BOUNDED_CODE_RAW_BYTES={bundle['source_code_window_raw_bytes']}")
    print("=== WORLD_MAP_STATIC_EVIDENCE_BEGIN ===")
    print(report)
    print("=== WORLD_MAP_STATIC_EVIDENCE_END ===")
    return 0


def disassemble_window(window: dict[str, Any], temp_root: Path) -> list[dict[str, Any]]:
    start = parse_addr(window["start_address"])
    blob = bytes.fromhex(window["bytes_hex"])
    path = temp_root / f"window-{start:016x}.bin"
    path.write_bytes(blob)
    cp = subprocess.run(
        [
            "objdump", "-D", "-b", "binary", "-m", "i386:x86-64", "-M", "intel",
            "--no-show-raw-insn", f"--adjust-vma={start}", str(path),
        ],
        check=False,
        text=True,
        capture_output=True,
        errors="replace",
        timeout=60,
    )
    if cp.returncode != 0:
        raise SystemExit(f"WORLD_MAP_STATIC_V2_REFUSED=HOSTED_OBJDUMP:{cp.returncode}:{start:x}")
    records: list[dict[str, Any]] = []
    for raw in cp.stdout.splitlines():
        match = base.ADDR_RE.match(raw)
        if not match:
            continue
        try:
            address = int(match.group(1), 16)
        except ValueError:
            continue
        text = match.group(2).strip()
        if text:
            records.append({
                "addr": address,
                "text": text,
                "purpose": window["purpose"],
                "origin": start,
                "geometry_related": bool(window.get("geometry_related")),
                "metadata": window.get("metadata", {}),
            })
    return records


def hosted_field_evidence(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_offset = {f"+0x{o:x}": [] for o in base.GEOMETRY_OFFSETS}
    seen: set[tuple[int, int, str]] = set()
    for insn in records:
        if not insn.get("geometry_related"):
            continue
        for offset in base.GEOMETRY_OFFSETS:
            if not base.mem_contains_offset(insn["text"], offset):
                continue
            access, immediate = base.classify_field_instruction(insn["text"], offset)
            key = (insn["addr"], offset, access)
            if key in seen:
                continue
            seen.add(key)
            by_offset[f"+0x{offset:x}"].append({
                "field_offset": f"+0x{offset:x}",
                "instruction_address": fmt_addr(insn["addr"]),
                "instruction": insn["text"][:240],
                "access": access,
                "immediate": immediate,
                "origin_kind": insn["purpose"],
                "origin_address": fmt_addr(insn["origin"]),
                "distance_from_origin": insn["addr"] - insn["origin"],
                "type_affine": True,
                "window_metadata": insn.get("metadata", {}),
                "disassembly_backend": "gnu_objdump_hosted_bounded_binary",
            })
    for key in by_offset:
        by_offset[key] = sorted(
            by_offset[key], key=lambda rec: (parse_addr(rec["instruction_address"]), rec["origin_kind"])
        )[:96]
    return by_offset


def enrich_direct_xrefs(bundle: dict[str, Any], records: list[dict[str, Any]]) -> None:
    by_addr = {rec["addr"]: rec["text"] for rec in records if rec["purpose"] == "direct_vptr_xref"}
    for items in bundle.get("direct_vptr_xrefs", {}).values():
        for item in items:
            address = parse_addr(item["instruction_address"])
            if address in by_addr:
                item["hosted_disassembly"] = by_addr[address][:240]
                item["hosted_disassembly_backend"] = "gnu_objdump_hosted_bounded_binary"


def enrich_geometry(bundle: dict[str, Any], records: list[dict[str, Any]]) -> None:
    field_evidence = hosted_field_evidence(records)
    offsets = [key for key, items in field_evidence.items() if items]
    priority: dict[str, Any] = {}
    for offset, expected in base.PRIORITY_IMMEDIATES.items():
        key = f"+0x{offset:x}"
        observations = [
            rec for rec in field_evidence[key]
            if rec["access"] in {"write", "read_write"} and rec["immediate"] == expected
        ]
        priority[key] = {
            "expected_decimal": expected,
            "expected_hex": f"0x{expected:x}",
            "direct_immediate_write_observed": bool(observations),
            "observations": observations[:24],
        }
    geometry = bundle["geometry"]
    geometry["field_evidence"] = field_evidence
    geometry["priority_values"] = priority
    geometry["offsets_with_type_affine_evidence"] = offsets
    geometry["bounded_observation_count"] = sum(len(items) for items in field_evidence.values())
    geometry["hosted_disassembly_backend"] = "gnu_objdump_hosted_bounded_binary"
    geometry["source_disassembly_backend"] = "none"
    bundle["readiness"] = {
        "identity_windows_recovered": sum(1 for item in bundle["identity_windows"] if item.get("window_recovered")),
        "geometry_offsets_with_evidence": offsets,
        "priority_0x48_18_write": priority["+0x48"]["direct_immediate_write_observed"],
        "priority_0x4c_14_write": priority["+0x4c"]["direct_immediate_write_observed"],
        "WORLD_MAP_STATIC_EVIDENCE_READY": (
            sum(1 for item in bundle["identity_windows"] if item.get("window_recovered")) == 3
            and bool(offsets)
        ),
    }


def validate_source_bundle(bundle_dir: Path) -> dict[str, Any]:
    allowed = {"worldmap-static-evidence.json", "worldmap-static-evidence.md", "source-fence.txt"}
    base.enforce_sanitized_files(bundle_dir, allowed)
    bundle = json.loads((bundle_dir / "worldmap-static-evidence.json").read_text(encoding="utf-8"))
    if bundle.get("schema") != SCHEMA:
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=SCHEMA")
    client = bundle.get("client", {})
    if (
        client.get("version") != base.EXPECTED_VERSION
        or client.get("size") != base.EXPECTED_SIZE
        or client.get("sha256") != base.EXPECTED_SHA256
    ):
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=EXACT_FENCE")
    policy = bundle.get("policy", {})
    required_policy = {
        "runtime_access": "none",
        "canonical_runtime_accessed": False,
        "client_executed": False,
        "client_bytes_mutated": False,
        "process_memory_accessed": False,
        "x11_vnc_accessed": False,
        "login_session_accessed": False,
        "gameplay_accessed": False,
        "raw_client_uploaded": False,
        "bounded_sanitized_output_only": True,
    }
    for key, expected in required_policy.items():
        if policy.get(key) != expected:
            raise SystemExit(f"WORLD_MAP_STATIC_V2_REFUSED=POLICY:{key}")
    identities = bundle.get("identity_windows", [])
    if len(identities) != 3 or not all(item.get("window_recovered") for item in identities):
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=IDENTITY_WINDOWS")
    expected_windows = {
        (base.fmt_addr(int(spec["header_start"])), base.fmt_addr(int(spec["header_end"])), base.fmt_addr(int(spec["vptr"])))
        for spec in base.IDENTITIES
    }
    observed_windows = {
        (item.get("window_start"), item.get("window_end"), item.get("vptr_address_point"))
        for item in identities
    }
    if observed_windows != expected_windows:
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=IDENTITY_ADDRESSES")
    windows = bundle.get("source_code_windows")
    if not isinstance(windows, list):
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=CODE_WINDOWS")
    raw_total = 0
    for window in windows:
        blob = bytes.fromhex(window["bytes_hex"])
        if len(blob) != window["byte_count"]:
            raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=CODE_WINDOW_LENGTH")
        raw_total += len(blob)
    if raw_total != bundle.get("source_code_window_raw_bytes") or raw_total > MAX_SOURCE_CODE_BYTES:
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=CODE_WINDOW_BUDGET")
    source_report = base.markdown_report(bundle)
    if (bundle_dir / "worldmap-static-evidence.md").read_text(encoding="utf-8") != source_report:
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=SOURCE_REPORT_NONDETERMINISTIC")
    return bundle


def validate_mode(args: argparse.Namespace) -> int:
    bundle_dir = Path(args.bundle_dir)
    outdir = Path(args.outdir)
    bundle = validate_source_bundle(bundle_dir)
    if subprocess.run(["sh", "-c", "command -v objdump >/dev/null 2>&1"], check=False).returncode != 0:
        raise SystemExit("WORLD_MAP_STATIC_V2_REFUSED=HOSTED_OBJDUMP_MISSING")

    all_records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="worldmap-static-v2-") as temp:
        temp_root = Path(temp)
        for window in bundle["source_code_windows"]:
            all_records.extend(disassemble_window(window, temp_root))

    enrich_direct_xrefs(bundle, all_records)
    enrich_geometry(bundle, all_records)
    bundle["schema"] = SCHEMA
    bundle["hosted_validation"] = {
        "disassembly_backend": "gnu_objdump_hosted_bounded_binary",
        "raw_client_present": False,
        "bounded_window_count": len(bundle["source_code_windows"]),
        "bounded_raw_bytes": bundle["source_code_window_raw_bytes"],
        "instruction_records_examined": len(all_records),
    }

    outdir.mkdir(parents=True, exist_ok=True)
    report = base.markdown_report(bundle)
    (outdir / "worldmap-static-evidence.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (outdir / "worldmap-static-evidence.md").write_text(report, encoding="utf-8")
    validation = {
        "schema": HOSTED_SCHEMA,
        "source_schema": SCHEMA,
        "client_version": base.EXPECTED_VERSION,
        "client_size": base.EXPECTED_SIZE,
        "client_sha256": base.EXPECTED_SHA256,
        "identity_windows_recovered": bundle["readiness"]["identity_windows_recovered"],
        "geometry_offsets_with_evidence": bundle["readiness"]["geometry_offsets_with_evidence"],
        "priority_0x48_18_write": bundle["readiness"]["priority_0x48_18_write"],
        "priority_0x4c_14_write": bundle["readiness"]["priority_0x4c_14_write"],
        "WORLD_MAP_STATIC_EVIDENCE_READY": bundle["readiness"]["WORLD_MAP_STATIC_EVIDENCE_READY"],
        "github_hosted_validation": True,
        "raw_client_present": False,
        "bounded_code_window_count": len(bundle["source_code_windows"]),
        "bounded_code_raw_bytes": bundle["source_code_window_raw_bytes"],
    }
    (outdir / "hosted-validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (outdir / "hosted-validation.txt").write_text("\n".join([
        "WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS",
        "WORLD_MAP_STATIC_HOSTED_DISASSEMBLY_BACKEND=gnu_objdump_bounded_binary",
        f"WORLD_MAP_STATIC_CLIENT_VERSION={base.EXPECTED_VERSION}",
        f"WORLD_MAP_STATIC_CLIENT_SIZE={base.EXPECTED_SIZE}",
        f"WORLD_MAP_STATIC_CLIENT_SHA256={base.EXPECTED_SHA256}",
        f"WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED={validation['identity_windows_recovered']}",
        "WORLD_MAP_STATIC_GEOMETRY_OFFSETS_WITH_EVIDENCE=" + (
            ",".join(validation["geometry_offsets_with_evidence"])
            if validation["geometry_offsets_with_evidence"] else "NONE"
        ),
        f"WORLD_MAP_STATIC_PRIORITY_0X48_18_WRITE={str(validation['priority_0x48_18_write']).lower()}",
        f"WORLD_MAP_STATIC_PRIORITY_0X4C_14_WRITE={str(validation['priority_0x4c_14_write']).lower()}",
        f"WORLD_MAP_STATIC_EVIDENCE_READY={str(validation['WORLD_MAP_STATIC_EVIDENCE_READY']).lower()}",
        "",
    ]), encoding="utf-8")
    print("WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS")
    print("=== WORLD_MAP_STATIC_EVIDENCE_BEGIN ===")
    print(report)
    print("=== WORLD_MAP_STATIC_EVIDENCE_END ===")
    print("WORLD_MAP_STATIC_GEOMETRY_OFFSETS_WITH_EVIDENCE=" + (
        ",".join(validation["geometry_offsets_with_evidence"])
        if validation["geometry_offsets_with_evidence"] else "NONE"
    ))
    print(f"WORLD_MAP_STATIC_PRIORITY_0X48_18_WRITE={str(validation['priority_0x48_18_write']).lower()}")
    print(f"WORLD_MAP_STATIC_PRIORITY_0X4C_14_WRITE={str(validation['priority_0x4c_14_write']).lower()}")
    print(f"WORLD_MAP_STATIC_EVIDENCE_READY={str(validation['WORLD_MAP_STATIC_EVIDENCE_READY']).lower()}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    source = sub.add_parser("source")
    source.add_argument("--client", required=True)
    source.add_argument("--outdir", required=True)
    source.add_argument("--candidate-index", required=True, type=int)
    validate = sub.add_parser("validate")
    validate.add_argument("--bundle-dir", required=True)
    validate.add_argument("--outdir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return source_mode(args) if args.mode == "source" else validate_mode(args)


if __name__ == "__main__":
    sys.exit(main())
