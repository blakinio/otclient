#!/usr/bin/env python3
"""Bounded read-only exact-client world-map static evidence producer."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
from typing import Any, Iterable

EXPECTED_VERSION = "15.32.df7b29"
EXPECTED_SIZE = 51965216
EXPECTED_SHA256 = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
SCHEMA = "track-a-worldmap-exact-static-evidence-v1"
TASK_ID = "OTC-20260816-track-a-worldmap-exact-static-evidence"
CONSUMER_PR = 367

IDENTITIES = (
    {"label": "handler_candidate", "header_start": 0x030871C8, "header_end": 0x030871D7, "vptr": 0x030871D8},
    {"label": "geometry_candidate", "header_start": 0x0308CE60, "header_end": 0x0308CE6F, "vptr": 0x0308CE70},
    {"label": "control_candidate", "header_start": 0x02F683C0, "header_end": 0x02F683CF, "vptr": 0x02F683D0},
)
GEOMETRY_VPTR = 0x0308CE70
GEOMETRY_OFFSETS = (0x18, 0x1C, 0x30, 0x34, 0x48, 0x4C)
PRIORITY_IMMEDIATES = {0x48: 18, 0x4C: 14}
FOLLOW_ON_TOKENS = (
    "TWorldMapViewport",
    "TWorldMapStorage",
    "TWorldMapRenderProvider",
    "TWorldMapCamera",
    "TWorldMapPicker",
    "TWorldmapProtocolMessageHandler",
    "TWorldMapProtocolMessageHandler",
    "TWorldMapExtent",
    "TWorldMapSubfieldExtent",
)

PT_LOAD = 1
SHT_RELA = 4
SHT_RELR = 19
R_X86_64_RELATIVE = 8
ADDR_RE = re.compile(r"^\s*([0-9a-fA-F]+):\s*(.*?)\s*$")
COMMENT_ADDR_RE = re.compile(r"#\s*([0-9a-fA-F]+)(?:\s|$)")
MEM_RE = re.compile(r"\[([^\]]+)\]")
HEX_RE = re.compile(r"0x([0-9a-fA-F]+)")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_addr(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:08x}"


def fmt_qword(value: int | None) -> str:
    return "UNKNOWN" if value is None else f"0x{value:016x}"


def signed64(value: int) -> int:
    return value - (1 << 64) if value & (1 << 63) else value


class Elf64:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        if len(self.data) < 64 or self.data[:4] != b"\x7fELF":
            raise SystemExit("WORLD_MAP_STATIC_REFUSED=NOT_ELF")
        ident = self.data[:16]
        if ident[4] != 2 or ident[5] != 1:
            raise SystemExit("WORLD_MAP_STATIC_REFUSED=ELF_NOT_64LE")
        hdr = struct.unpack_from("<16sHHIQQQIHHHHHH", self.data, 0)
        self.e_machine = hdr[2]
        if self.e_machine != 62:
            raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=ELF_MACHINE:{self.e_machine}")
        self.e_phoff, self.e_shoff = hdr[5], hdr[6]
        self.e_phentsize, self.e_phnum = hdr[9], hdr[10]
        self.e_shentsize, self.e_shnum, self.e_shstrndx = hdr[11], hdr[12], hdr[13]
        self.loads: list[dict[str, int]] = []
        for i in range(self.e_phnum):
            off = self.e_phoff + i * self.e_phentsize
            if off + 56 > len(self.data):
                raise SystemExit("WORLD_MAP_STATIC_REFUSED=TRUNCATED_PROGRAM_HEADERS")
            p_type, p_flags, p_offset, p_vaddr, _p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from(
                "<IIQQQQQQ", self.data, off
            )
            if p_type == PT_LOAD:
                self.loads.append({
                    "flags": p_flags, "offset": p_offset, "vaddr": p_vaddr,
                    "filesz": p_filesz, "memsz": p_memsz, "align": p_align,
                })
        self.sections = self._sections()
        self.relocs_by_addr: dict[int, list[dict[str, Any]]] = {}
        self.relative_target_to_slots: dict[int, list[int]] = {}
        self._parse_relocations()

    def _sections(self) -> list[dict[str, Any]]:
        raw: list[dict[str, Any]] = []
        for i in range(self.e_shnum):
            off = self.e_shoff + i * self.e_shentsize
            if off + 64 > len(self.data):
                raise SystemExit("WORLD_MAP_STATIC_REFUSED=TRUNCATED_SECTION_HEADERS")
            v = struct.unpack_from("<IIQQQQIIQQ", self.data, off)
            raw.append({
                "name_off": v[0], "type": v[1], "flags": v[2], "addr": v[3],
                "offset": v[4], "size": v[5], "link": v[6], "info": v[7],
                "align": v[8], "entsize": v[9], "name": "",
            })
        if not (0 <= self.e_shstrndx < len(raw)):
            return raw
        shstr = raw[self.e_shstrndx]
        blob = self.data[shstr["offset"]:shstr["offset"] + shstr["size"]]
        for sec in raw:
            start = sec["name_off"]
            if start >= len(blob):
                continue
            end = blob.find(b"\0", start)
            if end < 0:
                end = len(blob)
            sec["name"] = blob[start:end].decode("ascii", "replace")
        return raw

    def vaddr_to_offset(self, addr: int, size: int = 1) -> int | None:
        for seg in self.loads:
            start = seg["vaddr"]
            if start <= addr and addr + size <= start + seg["filesz"]:
                return seg["offset"] + (addr - start)
        return None

    def offset_to_vaddr(self, offset: int) -> int | None:
        for seg in self.loads:
            start = seg["offset"]
            if start <= offset < start + seg["filesz"]:
                return seg["vaddr"] + (offset - start)
        return None

    def bytes_at(self, addr: int, size: int) -> bytes | None:
        off = self.vaddr_to_offset(addr, size)
        return None if off is None else self.data[off:off + size]

    def qword(self, addr: int) -> int | None:
        blob = self.bytes_at(addr, 8)
        return None if blob is None or len(blob) != 8 else struct.unpack_from("<Q", blob, 0)[0]

    def cstring(self, addr: int, limit: int = 512) -> str | None:
        off = self.vaddr_to_offset(addr)
        if off is None:
            return None
        end = self.data.find(b"\0", off, min(len(self.data), off + limit))
        if end < 0:
            return None
        raw = self.data[off:end]
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return None
        return text if text and all(ch.isprintable() for ch in text) else None

    def executable(self, addr: int) -> bool:
        return any(
            seg["vaddr"] <= addr < seg["vaddr"] + seg["memsz"] and bool(seg["flags"] & 1)
            for seg in self.loads
        )

    def mapped(self, addr: int) -> bool:
        return any(seg["vaddr"] <= addr < seg["vaddr"] + seg["memsz"] for seg in self.loads)

    def _add_reloc(self, slot: int, kind: str, r_type: int, addend: int | None,
                   target: int | None, section: str) -> None:
        rec = {
            "slot": slot, "kind": kind, "type": r_type, "addend": addend,
            "target": target, "section": section,
        }
        self.relocs_by_addr.setdefault(slot, []).append(rec)
        if target is not None:
            self.relative_target_to_slots.setdefault(target, []).append(slot)

    def _parse_relocations(self) -> None:
        for sec in self.sections:
            if sec["type"] == SHT_RELA:
                entsize = sec["entsize"] or 24
                if entsize < 24:
                    continue
                for i in range(sec["size"] // entsize):
                    off = sec["offset"] + i * entsize
                    if off + 24 > len(self.data):
                        break
                    r_offset, r_info, r_addend = struct.unpack_from("<QQq", self.data, off)
                    r_type = r_info & 0xFFFFFFFF
                    target = r_addend if r_type == R_X86_64_RELATIVE and r_addend >= 0 else None
                    self._add_reloc(r_offset, "RELA", r_type, r_addend, target, sec["name"])
            elif sec["type"] == SHT_RELR:
                entsize = sec["entsize"] or 8
                if entsize != 8:
                    continue
                where = 0
                for off in range(sec["offset"], sec["offset"] + sec["size"], 8):
                    if off + 8 > len(self.data):
                        break
                    entry = struct.unpack_from("<Q", self.data, off)[0]
                    if (entry & 1) == 0:
                        where = entry
                        raw = self.qword(where)
                        self._add_reloc(where, "RELR", R_X86_64_RELATIVE, raw, raw, sec["name"])
                        where += 8
                    else:
                        for bit in range(1, 64):
                            if entry & (1 << bit):
                                slot = where + 8 * (bit - 1)
                                raw = self.qword(slot)
                                self._add_reloc(slot, "RELR", R_X86_64_RELATIVE, raw, raw, sec["name"])
                        where += 8 * 63

    def relocations(self, addr: int) -> list[dict[str, Any]]:
        return list(self.relocs_by_addr.get(addr, ()))

    def resolved_qword(self, addr: int) -> tuple[int | None, str]:
        for rec in self.relocs_by_addr.get(addr, ()):
            if rec["type"] == R_X86_64_RELATIVE and rec["target"] is not None:
                return int(rec["target"]), f'{rec["kind"]}:R_X86_64_RELATIVE'
        return self.qword(addr), "RAW"

    def find_token_strings(self, token: str, max_hits: int = 16) -> list[dict[str, Any]]:
        needle = token.encode("ascii")
        hits: list[dict[str, Any]] = []
        pos = 0
        while len(hits) < max_hits:
            idx = self.data.find(needle, pos)
            if idx < 0:
                break
            pos = idx + 1
            start, floor = idx, max(0, idx - 192)
            while start > floor and self.data[start - 1] != 0:
                start -= 1
            end = self.data.find(b"\0", idx, min(len(self.data), idx + 512))
            if end < 0:
                continue
            raw = self.data[start:end]
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if not text or len(text) > 512 or not all(ch.isprintable() for ch in text):
                continue
            vaddr = self.offset_to_vaddr(start)
            if vaddr is None:
                continue
            rec = {"token": token, "string": text, "string_vaddr": vaddr}
            if rec not in hits:
                hits.append(rec)
        return hits


def reloc_view(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "kind": r["kind"], "type": r["type"],
        "addend": None if r["addend"] is None else fmt_addr(int(r["addend"])),
        "target": None if r["target"] is None else fmt_addr(int(r["target"])),
        "section": r["section"],
    } for r in records]


def demangle_type_name(name: str | None) -> str | None:
    if not name or not shutil.which("c++filt"):
        return None
    try:
        cp = subprocess.run(["c++filt", "-t", name], check=False, text=True,
                            capture_output=True, timeout=5)
    except Exception:
        return None
    out = cp.stdout.strip()
    return out[:512] if cp.returncode == 0 and out and out != name else None


def identity_record(elf: Elf64, spec: dict[str, Any]) -> dict[str, Any]:
    start, vptr = int(spec["header_start"]), int(spec["vptr"])
    raw = elf.bytes_at(start, 16)
    off_raw, ti_raw = elf.qword(vptr - 16), elf.qword(vptr - 8)
    off_resolved, off_relation = elf.resolved_qword(vptr - 16)
    ti_resolved, ti_relation = elf.resolved_qword(vptr - 8)
    typeinfo = None
    if ti_resolved is not None and elf.mapped(ti_resolved):
        meta_raw = elf.qword(ti_resolved)
        meta_resolved, meta_relation = elf.resolved_qword(ti_resolved)
        name_raw = elf.qword(ti_resolved + 8)
        name_ptr, name_relation = elf.resolved_qword(ti_resolved + 8)
        name = elf.cstring(name_ptr) if name_ptr is not None else None
        typeinfo = {
            "address": fmt_addr(ti_resolved),
            "meta_vptr_raw": fmt_qword(meta_raw),
            "meta_vptr_resolved": fmt_addr(meta_resolved),
            "meta_vptr_relation": meta_relation,
            "meta_vptr_relocations": reloc_view(elf.relocations(ti_resolved)),
            "name_pointer_raw": fmt_qword(name_raw),
            "name_pointer_resolved": fmt_addr(name_ptr),
            "name_pointer_relation": name_relation,
            "name_pointer_relocations": reloc_view(elf.relocations(ti_resolved + 8)),
            "rtti_name": name,
            "demangled_name": demangle_type_name(name),
        }
    offset_to_top = signed64(off_resolved) if off_resolved is not None else None
    consistent = (
        raw is not None and off_resolved is not None and abs(offset_to_top) < (1 << 24)
        and ti_resolved is not None and elf.mapped(ti_resolved)
    )
    return {
        "label": spec["label"],
        "window_start": fmt_addr(start),
        "window_end": fmt_addr(int(spec["header_end"])),
        "vptr_address_point": fmt_addr(vptr),
        "raw_hex": None if raw is None else raw.hex(),
        "qword_vptr_minus_16_raw": fmt_qword(off_raw),
        "qword_vptr_minus_16_resolved": fmt_qword(off_resolved),
        "qword_vptr_minus_16_relation": off_relation,
        "qword_vptr_minus_16_relocations": reloc_view(elf.relocations(vptr - 16)),
        "offset_to_top_signed": offset_to_top,
        "qword_vptr_minus_8_raw": fmt_qword(ti_raw),
        "typeinfo_pointer_resolved": fmt_addr(ti_resolved),
        "typeinfo_pointer_relation": ti_relation,
        "typeinfo_pointer_relocations": reloc_view(elf.relocations(vptr - 8)),
        "itanium_layout_consistent": bool(consistent),
        "typeinfo": typeinfo,
        "window_recovered": raw is not None and len(raw) == 16,
    }


def run_objdump(client: Path) -> list[dict[str, Any]]:
    cp = subprocess.run(
        ["objdump", "-d", "-M", "intel", "--no-show-raw-insn", str(client)],
        check=False, text=True, capture_output=True, errors="replace", timeout=720,
    )
    if cp.returncode != 0:
        raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=OBJDUMP_FAILED:{cp.returncode}")
    out: list[dict[str, Any]] = []
    for raw in cp.stdout.splitlines():
        m = ADDR_RE.match(raw)
        if not m:
            continue
        try:
            addr = int(m.group(1), 16)
        except ValueError:
            continue
        text = m.group(2).strip()
        if text:
            out.append({"addr": addr, "text": text})
    return out


def direct_xrefs(lines: list[dict[str, Any]], targets: set[int]) -> dict[int, list[dict[str, Any]]]:
    out = {t: [] for t in targets}
    for insn in lines:
        m = COMMENT_ADDR_RE.search(insn["text"])
        if not m:
            continue
        target = int(m.group(1), 16)
        if target in out:
            out[target].append({
                "instruction_address": fmt_addr(insn["addr"]),
                "instruction": insn["text"][:240],
            })
    return out


def split_operands(rest: str) -> list[str]:
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(rest):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            parts.append(rest[start:i].strip())
            start = i + 1
    parts.append(rest[start:].strip())
    return [p for p in parts if p]


def mem_contains_offset(text: str, offset: int) -> bool:
    for m in MEM_RE.finditer(text):
        expr = m.group(1).lower().replace(" ", "")
        for hm in HEX_RE.finditer(expr):
            if int(hm.group(1), 16) == offset:
                prefix = expr[:hm.start()]
                if prefix.endswith("+") or prefix.endswith("-"):
                    return True
    return False


def classify_field_instruction(text: str, offset: int) -> tuple[str, int | None]:
    stripped = text.split("#", 1)[0].strip()
    tokens = stripped.split(None, 1)
    if not tokens:
        return "unknown", None
    mnemonic = tokens[0].lower()
    operands = split_operands(tokens[1] if len(tokens) > 1 else "")
    field_index = next((i for i, op in enumerate(operands) if mem_contains_offset(op, offset)), None)
    if field_index is None:
        return "unknown", None
    if mnemonic == "lea":
        access = "address"
    elif mnemonic in {"cmp", "test", "push"}:
        access = "read"
    elif mnemonic.startswith("mov"):
        access = "write" if field_index == 0 and mnemonic in {"mov", "movabs"} else "read"
    elif mnemonic in {"add", "sub", "and", "or", "xor", "inc", "dec", "not", "neg",
                      "rol", "ror", "shl", "shr", "sar", "sal", "xadd", "xchg"}:
        access = "read_write" if field_index == 0 else "read"
    else:
        access = "read" if field_index > 0 else "unknown"
    immediate = None
    for i, operand in enumerate(operands):
        if i == field_index:
            continue
        hm = HEX_RE.search(operand)
        if hm:
            value = int(hm.group(1), 16)
            if value <= 0xFFFFFFFF:
                immediate = value
                break
    return access, immediate


def bounded_lines(lines: list[dict[str, Any]], center: int, before: int, after: int,
                  max_lines: int = 360) -> list[dict[str, Any]]:
    lo, hi = max(0, center - before), center + after
    return [x for x in lines if lo <= x["addr"] <= hi][:max_lines]


def vtable_slots(elf: Elf64, address_point: int, count: int = 32) -> list[dict[str, Any]]:
    out = []
    for i in range(count):
        slot_addr = address_point + i * 8
        raw = elf.qword(slot_addr)
        resolved, relation = elf.resolved_qword(slot_addr)
        out.append({
            "index": i, "slot_address": fmt_addr(slot_addr), "raw": fmt_qword(raw),
            "resolved": fmt_addr(resolved), "relation": relation,
            "relocations": reloc_view(elf.relocations(slot_addr)),
            "resolved_executable": bool(resolved is not None and elf.executable(resolved)),
        })
    return out


def geometry_analysis(elf: Elf64, disasm: list[dict[str, Any]],
                      xrefs: list[dict[str, Any]]) -> dict[str, Any]:
    slots = vtable_slots(elf, GEOMETRY_VPTR, 32)
    origins: list[tuple[str, int]] = []
    seen: set[int] = set()
    for xref in xrefs[:20]:
        addr = int(xref["instruction_address"], 16)
        if addr not in seen:
            seen.add(addr)
            origins.append(("geometry_vptr_direct_xref", addr))
    for slot in slots:
        if not slot["resolved_executable"] or slot["resolved"] == "UNKNOWN":
            continue
        addr = int(slot["resolved"], 16)
        if addr not in seen:
            seen.add(addr)
            origins.append((f'geometry_vtable_slot_{slot["index"]}', addr))
        if len(origins) >= 44:
            break
    by_offset = {f"+0x{o:x}": [] for o in GEOMETRY_OFFSETS}
    dedupe: set[tuple[int, int, str, str]] = set()
    for origin_kind, origin_addr in origins:
        window = bounded_lines(
            disasm, origin_addr,
            0xA0 if origin_kind == "geometry_vptr_direct_xref" else 0x20,
            0x360 if origin_kind == "geometry_vptr_direct_xref" else 0x280,
        )
        for insn in window:
            for offset in GEOMETRY_OFFSETS:
                if not mem_contains_offset(insn["text"], offset):
                    continue
                access, immediate = classify_field_instruction(insn["text"], offset)
                key = (insn["addr"], offset, access, origin_kind)
                if key in dedupe:
                    continue
                dedupe.add(key)
                by_offset[f"+0x{offset:x}"].append({
                    "field_offset": f"+0x{offset:x}",
                    "instruction_address": fmt_addr(insn["addr"]),
                    "instruction": insn["text"][:240],
                    "access": access, "immediate": immediate,
                    "origin_kind": origin_kind, "origin_address": fmt_addr(origin_addr),
                    "distance_from_origin": insn["addr"] - origin_addr,
                    "type_affine": True,
                })
    for key in by_offset:
        by_offset[key] = sorted(
            by_offset[key],
            key=lambda r: (int(r["instruction_address"], 16), r["origin_kind"])
        )[:64]
    priority = {}
    for offset, expected in PRIORITY_IMMEDIATES.items():
        observations = [
            r for r in by_offset[f"+0x{offset:x}"]
            if r["access"] in {"write", "read_write"} and r["immediate"] == expected
        ]
        priority[f"+0x{offset:x}"] = {
            "expected_decimal": expected, "expected_hex": f"0x{expected:x}",
            "direct_immediate_write_observed": bool(observations),
            "observations": observations[:16],
        }
    return {
        "geometry_vptr": fmt_addr(GEOMETRY_VPTR), "vtable_slots": slots,
        "origin_count": len(origins),
        "origins": [{"kind": k, "address": fmt_addr(a)} for k, a in origins],
        "field_evidence": by_offset, "priority_values": priority,
        "offsets_with_type_affine_evidence": [k for k, v in by_offset.items() if v],
        "bounded_observation_count": sum(len(v) for v in by_offset.values()),
    }


def build_rtti_graph(elf: Elf64) -> list[dict[str, Any]]:
    graph, seen = [], set()
    for token in FOLLOW_ON_TOKENS:
        for hit in elf.find_token_strings(token):
            string_addr = int(hit["string_vaddr"])
            typeinfos = []
            for name_slot in sorted(set(elf.relative_target_to_slots.get(string_addr, ())))[:16]:
                typeinfo_addr = name_slot - 8
                if not elf.mapped(typeinfo_addr):
                    continue
                name_ptr, _ = elf.resolved_qword(typeinfo_addr + 8)
                if name_ptr != string_addr:
                    continue
                vtables = []
                for ti_slot in sorted(set(elf.relative_target_to_slots.get(typeinfo_addr, ())))[:32]:
                    candidate_vptr = ti_slot + 8
                    off_raw, _ = elf.resolved_qword(candidate_vptr - 16)
                    first_target, first_relation = elf.resolved_qword(candidate_vptr)
                    if off_raw is None or abs(signed64(off_raw)) >= (1 << 24):
                        continue
                    vtables.append({
                        "vptr_address_point": fmt_addr(candidate_vptr),
                        "offset_to_top_signed": signed64(off_raw),
                        "typeinfo_slot_relocations": reloc_view(elf.relocations(ti_slot)),
                        "first_slot_resolved": fmt_addr(first_target),
                        "first_slot_relation": first_relation,
                        "first_slot_executable": bool(first_target is not None and elf.executable(first_target)),
                    })
                typeinfos.append({
                    "typeinfo_address": fmt_addr(typeinfo_addr),
                    "name_pointer_slot": fmt_addr(name_slot),
                    "name_pointer_relocations": reloc_view(elf.relocations(name_slot)),
                    "vtables": vtables[:16],
                })
            key = (token, string_addr)
            if key in seen:
                continue
            seen.add(key)
            graph.append({
                "token": token, "rtti_string": hit["string"],
                "rtti_string_address": fmt_addr(string_addr),
                "demangled_name": demangle_type_name(hit["string"]),
                "typeinfos": typeinfos[:16],
            })
    return graph[:96]


def markdown_report(bundle: dict[str, Any]) -> str:
    lines = [
        "# Track A world-map exact static evidence", "",
        f"- schema: `{bundle['schema']}`", f"- task: `{bundle['task_id']}`",
        f"- consumer: PR `#{bundle['consumer_pr']}`",
        f"- client version: `{bundle['client']['version']}`",
        f"- client size: `{bundle['client']['size']}`",
        f"- client SHA-256: `{bundle['client']['sha256']}`",
        f"- source candidate index: `{bundle['client']['source_candidate_index']}`",
        f"- source runner: `{bundle['client']['source_runner']}`",
        "- runtime access: `none`", "- client executed: `false`",
        "- client bytes mutated: `false`", "- process memory accessed: `false`",
        "- canonical runtime accessed: `false`", "", "## Exact identity windows", "",
    ]
    for item in bundle["identity_windows"]:
        lines.extend([
            f"### {item['label']}", "",
            f"- window: `{item['window_start']}..{item['window_end']}`",
            f"- vptr address point: `{item['vptr_address_point']}`",
            f"- bytes: `{item['raw_hex']}`",
            f"- qword[-2] raw: `{item['qword_vptr_minus_16_raw']}`",
            f"- qword[-2] resolved: `{item['qword_vptr_minus_16_resolved']}`",
            f"- offset-to-top signed: `{item['offset_to_top_signed']}`",
            f"- qword[-1] raw: `{item['qword_vptr_minus_8_raw']}`",
            f"- typeinfo pointer: `{item['typeinfo_pointer_resolved']}`",
            f"- Itanium layout consistent: `{str(item['itanium_layout_consistent']).lower()}`",
        ])
        ti = item.get("typeinfo")
        if ti:
            lines.extend([
                f"- RTTI name: `{ti.get('rtti_name') or 'UNKNOWN'}`",
                f"- RTTI demangled: `{ti.get('demangled_name') or 'UNKNOWN'}`",
                f"- typeinfo name pointer: `{ti.get('name_pointer_resolved')}`",
            ])
        else:
            lines.append("- RTTI/type name: `UNKNOWN`")
        lines.append("")
    lines.extend(["## Direct vptr xrefs", ""])
    for key, items in bundle["direct_vptr_xrefs"].items():
        lines.append(f"### `{key}`")
        if not items:
            lines.append("- `UNKNOWN` (no direct objdump RIP-comment xref recovered)")
        for rec in items[:24]:
            lines.append(f"- `{rec['instruction_address']}` — `{rec['instruction']}`")
        lines.append("")
    lines.extend(["## Geometry field evidence", ""])
    geom = bundle["geometry"]
    for key in [f"+0x{o:x}" for o in GEOMETRY_OFFSETS]:
        lines.append(f"### `{key}`")
        items = geom["field_evidence"].get(key, [])
        if not items:
            lines.append("- `UNKNOWN` — no type-affine bounded instruction recovered.")
        for rec in items[:32]:
            imm = "UNKNOWN" if rec["immediate"] is None else f"0x{rec['immediate']:x}"
            lines.append(
                f"- `{rec['instruction_address']}` `{rec['access']}` immediate `{imm}` "
                f"origin `{rec['origin_kind']}@{rec['origin_address']}` — `{rec['instruction']}`"
            )
        lines.append("")
    lines.extend(["## Priority literals", ""])
    for key, val in geom["priority_values"].items():
        lines.append(
            f"- `{key}` expected `{val['expected_decimal']}` (`{val['expected_hex']}`): "
            f"direct immediate write observed = `{str(val['direct_immediate_write_observed']).lower()}`"
        )
        for rec in val["observations"]:
            lines.append(f"  - `{rec['instruction_address']}` — `{rec['instruction']}`")
    lines.extend(["", "## RTTI/type graph", ""])
    if not bundle["rtti_graph"]:
        lines.append("- `UNKNOWN` — no requested RTTI token graph recovered.")
    for rec in bundle["rtti_graph"]:
        lines.append(
            f"- token `{rec['token']}` string `{rec['rtti_string_address']}` "
            f"`{rec['rtti_string']}`; typeinfo candidates `{len(rec['typeinfos'])}`"
        )
        for ti in rec["typeinfos"][:8]:
            lines.append(f"  - typeinfo `{ti['typeinfo_address']}`; vtable candidates `{len(ti['vtables'])}`")
            for vt in ti["vtables"][:6]:
                lines.append(
                    f"    - vptr `{vt['vptr_address_point']}`, offset-to-top "
                    f"`{vt['offset_to_top_signed']}`, first slot `{vt['first_slot_resolved']}`"
                )
    lines.extend([
        "", "## Readiness", "",
        f"- recovered identity windows: `{bundle['readiness']['identity_windows_recovered']}/3`",
        f"- geometry offsets with type-affine evidence: "
        f"`{','.join(bundle['readiness']['geometry_offsets_with_evidence']) or 'NONE'}`",
        f"- priority +0x48 immediate 18 write: `{str(bundle['readiness']['priority_0x48_18_write']).lower()}`",
        f"- priority +0x4c immediate 14 write: `{str(bundle['readiness']['priority_0x4c_14_write']).lower()}`",
        f"- `WORLD_MAP_STATIC_EVIDENCE_READY={str(bundle['readiness']['WORLD_MAP_STATIC_EVIDENCE_READY']).lower()}`",
        "", "Semantic field names remain `UNKNOWN` unless directly proven above.", "",
    ])
    return "\n".join(lines)


def source_mode(args: argparse.Namespace) -> int:
    client, outdir = Path(args.client), Path(args.outdir)
    if not client.is_file() or client.is_symlink():
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=SOURCE_NOT_REGULAR")
    size, digest = client.stat().st_size, sha256_file(client)
    if size != EXPECTED_SIZE:
        raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=SIZE:{size}")
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=SHA256:{digest}")
    elf = Elf64(client)
    identities = [identity_record(elf, spec) for spec in IDENTITIES]
    disasm = run_objdump(client)
    xref_map = direct_xrefs(disasm, {int(s["vptr"]) for s in IDENTITIES})
    geometry = geometry_analysis(elf, disasm, xref_map.get(GEOMETRY_VPTR, []))
    recovered = sum(1 for x in identities if x["window_recovered"])
    offsets_with_evidence = geometry["offsets_with_type_affine_evidence"]
    p48 = geometry["priority_values"]["+0x48"]["direct_immediate_write_observed"]
    p4c = geometry["priority_values"]["+0x4c"]["direct_immediate_write_observed"]
    evidence_ready = recovered == 3 and bool(offsets_with_evidence)
    bundle = {
        "schema": SCHEMA, "task_id": TASK_ID, "consumer_pr": CONSUMER_PR,
        "client": {
            "version": EXPECTED_VERSION, "size": size, "sha256": digest,
            "source_candidate_index": int(args.candidate_index),
            "source_runner": os.environ.get("RUNNER_NAME", "UNKNOWN"),
            "elf_machine": elf.e_machine,
        },
        "policy": {
            "runtime_access": "none", "canonical_runtime_accessed": False,
            "client_executed": False, "client_bytes_mutated": False,
            "process_memory_accessed": False, "x11_vnc_accessed": False,
            "login_session_accessed": False, "network_accessed_by_analyzer": False,
            "gameplay_accessed": False, "raw_client_uploaded": False,
            "bounded_sanitized_output_only": True,
        },
        "identity_windows": identities,
        "direct_vptr_xrefs": {fmt_addr(k): v[:64] for k, v in xref_map.items()},
        "geometry": geometry, "rtti_graph": build_rtti_graph(elf),
        "readiness": {
            "identity_windows_recovered": recovered,
            "geometry_offsets_with_evidence": offsets_with_evidence,
            "priority_0x48_18_write": p48, "priority_0x4c_14_write": p4c,
            "WORLD_MAP_STATIC_EVIDENCE_READY": evidence_ready,
        },
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "worldmap-static-evidence.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = markdown_report(bundle)
    (outdir / "worldmap-static-evidence.md").write_text(report, encoding="utf-8")
    (outdir / "source-fence.txt").write_text("\n".join([
        f"WORLD_MAP_STATIC_CLIENT_VERSION={EXPECTED_VERSION}",
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
        f"WORLD_MAP_STATIC_EVIDENCE_READY={str(evidence_ready).lower()}", "",
    ]), encoding="utf-8")
    print("=== WORLD_MAP_STATIC_EVIDENCE_BEGIN ===")
    print(report)
    print("=== WORLD_MAP_STATIC_EVIDENCE_END ===")
    print(f"WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED={recovered}")
    print("WORLD_MAP_STATIC_GEOMETRY_OFFSETS_WITH_EVIDENCE=" +
          (",".join(offsets_with_evidence) if offsets_with_evidence else "NONE"))
    print(f"WORLD_MAP_STATIC_PRIORITY_0X48_18_WRITE={str(p48).lower()}")
    print(f"WORLD_MAP_STATIC_PRIORITY_0X4C_14_WRITE={str(p4c).lower()}")
    print(f"WORLD_MAP_STATIC_EVIDENCE_READY={str(evidence_ready).lower()}")
    return 0


def enforce_sanitized_files(root: Path, allowed: set[str]) -> None:
    actual = {p.name for p in root.iterdir() if p.is_file()}
    if actual != allowed:
        raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=UNSAFE_FILE_SET:{sorted(actual)}")
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        data = path.read_bytes()
        if len(data) > 2 * 1024 * 1024:
            raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=OVERSIZED:{path.name}:{len(data)}")
        if data.startswith(b"\x7fELF") or data[:2] == b"MZ":
            raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=RAW_EXECUTABLE:{path.name}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=NON_UTF8:{path.name}") from exc


def validate_mode(args: argparse.Namespace) -> int:
    bundle_dir, outdir = Path(args.bundle_dir), Path(args.outdir)
    allowed = {"worldmap-static-evidence.json", "worldmap-static-evidence.md", "source-fence.txt"}
    enforce_sanitized_files(bundle_dir, allowed)
    bundle = json.loads((bundle_dir / "worldmap-static-evidence.json").read_text(encoding="utf-8"))
    if bundle.get("schema") != SCHEMA:
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=SCHEMA")
    client = bundle.get("client", {})
    if client.get("version") != EXPECTED_VERSION or client.get("size") != EXPECTED_SIZE \
            or client.get("sha256") != EXPECTED_SHA256:
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=EXACT_FENCE")
    expected_policy = {
        "runtime_access": "none", "canonical_runtime_accessed": False,
        "client_executed": False, "client_bytes_mutated": False,
        "process_memory_accessed": False, "x11_vnc_accessed": False,
        "login_session_accessed": False, "gameplay_accessed": False,
        "raw_client_uploaded": False, "bounded_sanitized_output_only": True,
    }
    policy = bundle.get("policy", {})
    for key, value in expected_policy.items():
        if policy.get(key) != value:
            raise SystemExit(f"WORLD_MAP_STATIC_REFUSED=POLICY:{key}")
    identities = bundle.get("identity_windows", [])
    if len(identities) != 3:
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=IDENTITY_COUNT")
    expected_windows = {
        (fmt_addr(int(s["header_start"])), fmt_addr(int(s["header_end"])), fmt_addr(int(s["vptr"])))
        for s in IDENTITIES
    }
    observed_windows = {
        (x.get("window_start"), x.get("window_end"), x.get("vptr_address_point")) for x in identities
    }
    if observed_windows != expected_windows:
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=IDENTITY_ADDRESSES")
    for item in identities:
        raw_hex = item.get("raw_hex")
        if not isinstance(raw_hex, str) or not re.fullmatch(r"[0-9a-f]{32}", raw_hex):
            raise SystemExit("WORLD_MAP_STATIC_REFUSED=IDENTITY_BYTES")
    geometry = bundle.get("geometry", {})
    if geometry.get("geometry_vptr") != fmt_addr(GEOMETRY_VPTR):
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=GEOMETRY_VPTR")
    if sorted(geometry.get("field_evidence", {}).keys()) != sorted(f"+0x{o:x}" for o in GEOMETRY_OFFSETS):
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=GEOMETRY_OFFSETS")
    report = markdown_report(bundle)
    if (bundle_dir / "worldmap-static-evidence.md").read_text(encoding="utf-8") != report:
        raise SystemExit("WORLD_MAP_STATIC_REFUSED=REPORT_NONDETERMINISTIC")
    outdir.mkdir(parents=True, exist_ok=True)
    validation = {
        "schema": "track-a-worldmap-exact-static-hosted-validation-v1",
        "source_schema": SCHEMA, "client_version": EXPECTED_VERSION,
        "client_size": EXPECTED_SIZE, "client_sha256": EXPECTED_SHA256,
        "identity_windows_recovered": bundle["readiness"]["identity_windows_recovered"],
        "geometry_offsets_with_evidence": bundle["readiness"]["geometry_offsets_with_evidence"],
        "priority_0x48_18_write": bundle["readiness"]["priority_0x48_18_write"],
        "priority_0x4c_14_write": bundle["readiness"]["priority_0x4c_14_write"],
        "WORLD_MAP_STATIC_EVIDENCE_READY": bundle["readiness"]["WORLD_MAP_STATIC_EVIDENCE_READY"],
        "github_hosted_validation": True, "raw_client_present": False,
    }
    (outdir / "hosted-validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (outdir / "hosted-validation.txt").write_text("\n".join([
        "WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS",
        f"WORLD_MAP_STATIC_CLIENT_VERSION={EXPECTED_VERSION}",
        f"WORLD_MAP_STATIC_CLIENT_SIZE={EXPECTED_SIZE}",
        f"WORLD_MAP_STATIC_CLIENT_SHA256={EXPECTED_SHA256}",
        f"WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED={validation['identity_windows_recovered']}",
        "WORLD_MAP_STATIC_GEOMETRY_OFFSETS_WITH_EVIDENCE=" +
        (",".join(validation["geometry_offsets_with_evidence"])
         if validation["geometry_offsets_with_evidence"] else "NONE"),
        f"WORLD_MAP_STATIC_PRIORITY_0X48_18_WRITE={str(validation['priority_0x48_18_write']).lower()}",
        f"WORLD_MAP_STATIC_PRIORITY_0X4C_14_WRITE={str(validation['priority_0x4c_14_write']).lower()}",
        f"WORLD_MAP_STATIC_EVIDENCE_READY={str(validation['WORLD_MAP_STATIC_EVIDENCE_READY']).lower()}",
        "",
    ]), encoding="utf-8")
    print("WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS")
    print("=== WORLD_MAP_STATIC_EVIDENCE_BEGIN ===")
    print(report)
    print("=== WORLD_MAP_STATIC_EVIDENCE_END ===")
    print(f"WORLD_MAP_STATIC_EVIDENCE_READY={str(validation['WORLD_MAP_STATIC_EVIDENCE_READY']).lower()}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("source")
    p.add_argument("--client", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--candidate-index", required=True, type=int)
    p = sub.add_parser("validate")
    p.add_argument("--bundle-dir", required=True)
    p.add_argument("--outdir", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return source_mode(args) if args.mode == "source" else validate_mode(args)


if __name__ == "__main__":
    sys.exit(main())
