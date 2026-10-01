#!/usr/bin/env python3
"""Exact-build P0 probe for direct player-position candidates.

Runtime mode is intentionally scoped to relocation-backed TPlayerData objects.
Static mode inspects only the exact fenced ELF, its TPlayerData vtable/type
neighborhood and bounded code references. Neither mode writes process memory or
issues gameplay input. Structural map-strip data is only an independent oracle.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path


PT_LOAD = 1
PF_X = 1
SHT_RELA = 4
R_X86_64_RELATIVE = 8


@dataclass(frozen=True)
class Region:
    begin: int
    end: int
    perms: str
    offset: int
    path: str

    def contains(self, address: int) -> bool:
        return self.begin <= address < self.end


@dataclass(frozen=True)
class LoadSegment:
    offset: int
    vaddr: int
    filesz: int
    memsz: int
    flags: int

    def contains_vaddr(self, address: int, file_backed: bool = False) -> bool:
        size = self.filesz if file_backed else self.memsz
        return self.vaddr <= address < self.vaddr + size

    def contains_offset(self, offset: int) -> bool:
        return self.offset <= offset < self.offset + self.filesz


@dataclass(frozen=True)
class Section:
    index: int
    name: str
    sh_type: int
    flags: int
    addr: int
    offset: int
    size: int
    link: int
    entsize: int

    def contains_vaddr(self, address: int) -> bool:
        return self.addr <= address < self.addr + self.size


@dataclass(frozen=True)
class Rela:
    offset: int
    r_type: int
    sym: int
    addend: int
    section: str


class Elf64:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = path.read_bytes()
        if len(self.data) < 64 or self.data[:4] != b"\x7fELF":
            raise RuntimeError("not an ELF file")
        if self.data[4] != 2 or self.data[5] != 1:
            raise RuntimeError("expected ELF64 little-endian binary")

        header = struct.unpack_from("<16sHHIQQQIHHHHHH", self.data, 0)
        (
            _ident,
            self.e_type,
            self.e_machine,
            _version,
            self.e_entry,
            self.e_phoff,
            self.e_shoff,
            _flags,
            _ehsize,
            self.e_phentsize,
            self.e_phnum,
            self.e_shentsize,
            self.e_shnum,
            self.e_shstrndx,
        ) = header
        if self.e_machine != 62:
            raise RuntimeError(f"expected x86_64 ELF, machine={self.e_machine}")

        self.segments = self._parse_segments()
        self.sections = self._parse_sections()
        self.relocations = self._parse_relocations()

    def _parse_segments(self) -> list[LoadSegment]:
        segments: list[LoadSegment] = []
        for index in range(self.e_phnum):
            at = self.e_phoff + index * self.e_phentsize
            if at + 56 > len(self.data):
                raise RuntimeError("truncated program header table")
            p_type, p_flags, p_offset, p_vaddr, _paddr, p_filesz, p_memsz, _align = struct.unpack_from(
                "<IIQQQQQQ", self.data, at
            )
            if p_type == PT_LOAD:
                segments.append(
                    LoadSegment(
                        offset=p_offset,
                        vaddr=p_vaddr,
                        filesz=p_filesz,
                        memsz=p_memsz,
                        flags=p_flags,
                    )
                )
        return segments

    def _raw_section_headers(self) -> list[tuple[int, ...]]:
        raw: list[tuple[int, ...]] = []
        for index in range(self.e_shnum):
            at = self.e_shoff + index * self.e_shentsize
            if at + 64 > len(self.data):
                raise RuntimeError("truncated section header table")
            raw.append(struct.unpack_from("<IIQQQQIIQQ", self.data, at))
        return raw

    def _parse_sections(self) -> list[Section]:
        raw = self._raw_section_headers()
        names = b""
        if 0 <= self.e_shstrndx < len(raw):
            sh = raw[self.e_shstrndx]
            start, size = sh[4], sh[5]
            names = self.data[start : start + size]

        def read_name(offset: int) -> str:
            if not names or offset >= len(names):
                return ""
            end = names.find(b"\0", offset)
            if end < 0:
                end = len(names)
            return names[offset:end].decode("utf-8", "replace")

        sections: list[Section] = []
        for index, sh in enumerate(raw):
            sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, _info, _align, sh_entsize = sh
            sections.append(
                Section(
                    index=index,
                    name=read_name(sh_name),
                    sh_type=sh_type,
                    flags=sh_flags,
                    addr=sh_addr,
                    offset=sh_offset,
                    size=sh_size,
                    link=sh_link,
                    entsize=sh_entsize,
                )
            )
        return sections

    def _parse_relocations(self) -> dict[int, list[Rela]]:
        result: dict[int, list[Rela]] = {}
        for section in self.sections:
            if section.sh_type != SHT_RELA or not section.size:
                continue
            entsize = section.entsize or 24
            if entsize < 24:
                continue
            end = section.offset + section.size
            for at in range(section.offset, end, entsize):
                if at + 24 > len(self.data):
                    break
                r_offset, r_info, r_addend = struct.unpack_from("<QQq", self.data, at)
                rela = Rela(
                    offset=r_offset,
                    r_type=r_info & 0xFFFFFFFF,
                    sym=r_info >> 32,
                    addend=r_addend,
                    section=section.name,
                )
                result.setdefault(r_offset, []).append(rela)
        return result

    def vaddr_to_offset(self, address: int) -> int:
        for segment in self.segments:
            if segment.contains_vaddr(address, file_backed=True):
                return segment.offset + (address - segment.vaddr)
        raise RuntimeError(f"vaddr 0x{address:x} is not file-backed")

    def offset_to_vaddr(self, offset: int) -> int | None:
        for segment in self.segments:
            if segment.contains_offset(offset):
                return segment.vaddr + (offset - segment.offset)
        return None

    def section_for_vaddr(self, address: int) -> Section | None:
        for section in self.sections:
            if section.size and section.contains_vaddr(address):
                return section
        return None

    def qword(self, address: int) -> int:
        offset = self.vaddr_to_offset(address)
        if offset + 8 > len(self.data):
            raise RuntimeError(f"qword outside file at vaddr 0x{address:x}")
        return struct.unpack_from("<Q", self.data, offset)[0]

    def signed_qword(self, address: int) -> int:
        offset = self.vaddr_to_offset(address)
        return struct.unpack_from("<q", self.data, offset)[0]

    def resolved_qword(self, address: int) -> tuple[int, list[Rela]]:
        raw = self.qword(address)
        relas = self.relocations.get(address, [])
        for rela in relas:
            if rela.r_type == R_X86_64_RELATIVE:
                return rela.addend & ((1 << 64) - 1), relas
        return raw, relas

    def is_exec_vaddr(self, address: int) -> bool:
        return any(
            segment.flags & PF_X and segment.contains_vaddr(address)
            for segment in self.segments
        )

    def executable_segments(self) -> list[LoadSegment]:
        return [segment for segment in self.segments if segment.flags & PF_X and segment.filesz]

    def find_bytes(self, needle: bytes) -> list[int]:
        offsets: list[int] = []
        start = 0
        while True:
            index = self.data.find(needle, start)
            if index < 0:
                break
            offsets.append(index)
            start = index + 1
        return offsets

    def find_rip_xrefs(self, targets: set[int], limit: int = 256) -> list[tuple[int, int, str]]:
        """Find bounded RIP-relative LEA/MOV references in executable segments.

        This is deliberately a narrow x86-64 pattern decoder, not a general
        disassembler. Results are later confirmed with objdump windows.
        """
        found: list[tuple[int, int, str]] = []
        for segment in self.executable_segments():
            start = segment.offset
            data = self.data[start : start + segment.filesz]
            index = 0
            while index + 7 <= len(data):
                cursor = index
                rex = None
                if 0x40 <= data[cursor] <= 0x4F:
                    rex = data[cursor]
                    cursor += 1
                if cursor + 6 > len(data):
                    break
                opcode = data[cursor]
                if opcode not in (0x8D, 0x8B, 0x89):
                    index += 1
                    continue
                modrm = data[cursor + 1]
                if modrm & 0xC7 != 0x05:
                    index += 1
                    continue
                disp = struct.unpack_from("<i", data, cursor + 2)[0]
                instruction_len = (1 if rex is not None else 0) + 6
                instruction_va = segment.vaddr + index
                target = instruction_va + instruction_len + disp
                if target in targets:
                    mnemonic = {0x8D: "lea", 0x8B: "mov_load", 0x89: "mov_store"}[opcode]
                    found.append((instruction_va, target, mnemonic))
                    if len(found) >= limit:
                        return sorted(set(found))
                index += 1
        return sorted(set(found))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", type=int)
    parser.add_argument("--client", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-size", type=int, required=True)
    parser.add_argument("--vptr-offset", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--strips", type=Path)
    parser.add_argument("--object-bytes", type=lambda value: int(value, 0), default=0x1000)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--static-vtable-slots", type=int, default=32)
    parser.add_argument("--static-xref-limit", type=int, default=32)
    parser.add_argument("--static-disasm-limit", type=int, default=16)
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_client_fence(args: argparse.Namespace) -> tuple[Path, int, str]:
    client = args.client.resolve()
    actual_size = client.stat().st_size
    actual_sha = sha256(client)
    if actual_size != args.expected_size:
        raise SystemExit(f"client size mismatch: {actual_size}")
    if actual_sha != args.expected_sha256:
        raise SystemExit(f"client sha256 mismatch: {actual_sha}")
    print("TRACK_A_P0_EXACT_CLIENT_FENCE=true")
    print(f"TRACK_A_P0_CLIENT_SHA256={actual_sha}")
    print(f"TRACK_A_P0_CLIENT_SIZE={actual_size}")
    return client, actual_size, actual_sha


def read_maps(pid: int) -> list[Region]:
    regions: list[Region] = []
    for line in Path(f"/proc/{pid}/maps").read_text().splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) < 5:
            continue
        begin_text, end_text = fields[0].split("-", 1)
        path = fields[5] if len(fields) == 6 else ""
        regions.append(
            Region(
                begin=int(begin_text, 16),
                end=int(end_text, 16),
                perms=fields[1],
                offset=int(fields[2], 16),
                path=path,
            )
        )
    return regions


def resolved_exe(pid: int) -> Path:
    return Path(os.path.realpath(f"/proc/{pid}/exe"))


def main_base(regions: list[Region], client: Path) -> int:
    wanted = str(client.resolve())
    candidates = [region.begin - region.offset for region in regions if region.path == wanted]
    if not candidates:
        raise RuntimeError("client mapping not found in /proc/PID/maps")
    return min(candidates)


def writable_readable(regions: list[Region]) -> list[Region]:
    return [
        region
        for region in regions
        if len(region.perms) >= 2
        and region.perms[0] == "r"
        and region.perms[1] == "w"
        and region.end > region.begin
        and region.end - region.begin <= 512 * 1024 * 1024
    ]


def address_in(regions: list[Region], address: int) -> bool:
    return any(region.contains(address) for region in regions)


def pread_exact(fd: int, address: int, size: int) -> bytes:
    data = os.pread(fd, size, address)
    if len(data) != size:
        raise OSError(f"short read at 0x{address:x}: {len(data)}/{size}")
    return data


def find_typed_hits(fd: int, regions: list[Region], expected_vptr: int) -> list[int]:
    pattern = struct.pack("<Q", expected_vptr)
    hits: list[int] = []
    chunk_size = 1024 * 1024
    overlap = len(pattern) - 1
    rw = writable_readable(regions)
    for region in rw:
        cursor = region.begin
        tail = b""
        while cursor < region.end:
            wanted = min(chunk_size, region.end - cursor)
            try:
                data = os.pread(fd, wanted, cursor)
            except OSError:
                cursor += wanted
                tail = b""
                continue
            if not data:
                cursor += wanted
                tail = b""
                continue
            merged = tail + data
            merged_base = cursor - len(tail)
            search_at = 0
            while True:
                index = merged.find(pattern, search_at)
                if index < 0:
                    break
                address = merged_base + index
                if address % 8 == 0:
                    try:
                        private_data = struct.unpack("<Q", pread_exact(fd, address + 8, 8))[0]
                    except OSError:
                        private_data = 0
                    if private_data and address_in(rw, private_data):
                        hits.append(address)
                search_at = index + 1
            tail = merged[-overlap:] if overlap else b""
            cursor += len(data)
    return sorted(set(hits))


def plausible_u32(value: int) -> bool:
    return 30000 <= value <= 40000


def scan_inline_candidates(blob: bytes) -> list[tuple[str, int, tuple[int, int, int]]]:
    found: list[tuple[str, int, tuple[int, int, int]]] = []
    for offset in range(0, max(0, len(blob) - 12) + 1, 4):
        x, y, z = struct.unpack_from("<III", blob, offset)
        if plausible_u32(x) and plausible_u32(y) and 0 <= z <= 15:
            found.append(("u32x3", offset, (x, y, z)))
    for offset in range(0, max(0, len(blob) - 5) + 1, 2):
        x, y = struct.unpack_from("<HH", blob, offset)
        z = blob[offset + 4]
        if plausible_u32(x) and plausible_u32(y) and 0 <= z <= 15:
            found.append(("u16_u16_u8", offset, (x, y, z)))
    return found


def first_level_pointer_candidates(
    fd: int, regions: list[Region], owner_blob: bytes, limit: int = 48
) -> list[tuple[int, int, str, int, tuple[int, int, int]]]:
    rw = writable_readable(regions)
    results: list[tuple[int, int, str, int, tuple[int, int, int]]] = []
    seen_targets: set[int] = set()
    for owner_offset in range(8, min(len(owner_blob), 0x200) - 7, 8):
        target = struct.unpack_from("<Q", owner_blob, owner_offset)[0]
        if target in seen_targets or not address_in(rw, target):
            continue
        seen_targets.add(target)
        try:
            pointed = os.pread(fd, 0x400, target)
        except OSError:
            continue
        if len(pointed) < 16:
            continue
        for encoding, field_offset, xyz in scan_inline_candidates(pointed):
            results.append((owner_offset, target, encoding, field_offset, xyz))
            if len(results) >= limit:
                return results
    return results


def strip_oracle(path: Path | None) -> None:
    if path is None or not path.is_file():
        print("TRACK_A_P0_STRUCTURAL_ORACLE=unavailable")
        return
    records: list[tuple[int, int, int, int]] = []
    for raw in path.read_text(errors="replace").splitlines()[-500:]:
        fields = raw.split("\t")
        if len(fields) < 4:
            continue
        try:
            records.append(tuple(int(fields[index]) for index in range(4)))
        except ValueError:
            continue
    if not records:
        print("TRACK_A_P0_STRUCTURAL_ORACLE=empty")
        return

    groups: list[list[tuple[int, int, int, int]]] = [[records[0]]]
    for record in records[1:]:
        if record[0] - groups[-1][-1][0] > 500_000_000:
            groups.append([])
        groups[-1].append(record)
    latest = groups[-1]
    floor7 = [(x, y) for _, x, y, z in latest if z == 7]
    if not floor7:
        print(f"TRACK_A_P0_STRUCTURAL_ORACLE=latest_group_without_floor7 records={len(latest)}")
        return
    xs = sorted({x for x, _ in floor7})
    ys = sorted({y for _, y in floor7})
    print(
        "TRACK_A_P0_STRUCTURAL_ORACLE="
        f"records={len(latest)} floor7_x={xs[0]}..{xs[-1]} "
        f"floor7_y={ys[0]}..{ys[-1]} unique_x={len(xs)} unique_y={len(ys)}"
    )
    if len(xs) == 18 and len(ys) == 1:
        center_x = xs[0] + 9
        print(
            "TRACK_A_P0_VERTICAL_STRIP_ORACLE_CANDIDATES="
            f"({center_x},{ys[0] + 7},7),({center_x},{ys[0] - 6},7)"
        )


def extract_ascii_strings(blob: bytes, min_len: int = 4) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    start: int | None = None
    for index, value in enumerate(blob):
        if 32 <= value < 127:
            if start is None:
                start = index
        else:
            if start is not None and index - start >= min_len:
                result.append((start, blob[start:index].decode("ascii", "replace")))
            start = None
    if start is not None and len(blob) - start >= min_len:
        result.append((start, blob[start:].decode("ascii", "replace")))
    return result


def nearby_type_strings(client: Path) -> None:
    data = client.read_bytes()
    needle = b"tibia::game::TPlayerData"
    start = 0
    hits: list[int] = []
    while True:
        index = data.find(needle, start)
        if index < 0:
            break
        hits.append(index)
        start = index + 1
    print(f"TRACK_A_P0_TPLAYERDATA_STRING_HITS={len(hits)}")
    for index in hits[:8]:
        lo = max(0, index - 2048)
        hi = min(len(data), index + 4096)
        compact: list[str] = []
        for _offset, value in extract_ascii_strings(data[lo:hi]):
            if value not in compact:
                compact.append(value)
        print(f"TRACK_A_P0_TPLAYERDATA_STRING_OFFSET=0x{index:x}")
        for value in compact[:60]:
            print(f"TRACK_A_P0_NEAR_TYPE_STRING={value}")


def disassemble_windows(client: Path, addresses: list[int], limit: int) -> None:
    objdump = shutil.which("objdump")
    if not objdump:
        print("TRACK_A_P0_STATIC_OBJDUMP=unavailable")
        return
    print(f"TRACK_A_P0_STATIC_OBJDUMP={objdump}")
    for address in addresses[:limit]:
        start = max(0, address - 32)
        stop = address + 112
        proc = subprocess.run(
            [
                objdump,
                "-d",
                "-M",
                "intel",
                f"--start-address=0x{start:x}",
                f"--stop-address=0x{stop:x}",
                str(client),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=20,
        )
        print(f"TRACK_A_P0_STATIC_DISASM_BEGIN=0x{address:x}")
        for line in proc.stdout.splitlines()[:80]:
            print(f"TRACK_A_P0_STATIC_DISASM={line}")
        print(f"TRACK_A_P0_STATIC_DISASM_END=0x{address:x} rc={proc.returncode}")


def static_elf_probe(args: argparse.Namespace, client: Path) -> int:
    elf = Elf64(client)
    vptr = args.vptr_offset
    section = elf.section_for_vaddr(vptr)
    print("TRACK_A_P0_STATIC_MODE=true")
    print(f"TRACK_A_P0_ELF_TYPE={elf.e_type}")
    print(f"TRACK_A_P0_ELF_ENTRY=0x{elf.e_entry:x}")
    print(f"TRACK_A_P0_STATIC_TPLAYERDATA_VPTR=0x{vptr:x}")
    print(f"TRACK_A_P0_STATIC_TPLAYERDATA_SECTION={section.name if section else 'unknown'}")
    print(f"TRACK_A_P0_STATIC_RELOCATION_OFFSETS={len(elf.relocations)}")

    try:
        offset_to_top = elf.signed_qword(vptr - 16)
        typeinfo, typeinfo_relas = elf.resolved_qword(vptr - 8)
    except RuntimeError as exc:
        raise SystemExit(f"cannot inspect TPlayerData vtable header: {exc}") from exc

    print(f"TRACK_A_P0_STATIC_VTABLE_OFFSET_TO_TOP={offset_to_top}")
    print(f"TRACK_A_P0_STATIC_TYPEINFO=0x{typeinfo:x}")
    for rela in typeinfo_relas:
        print(
            "TRACK_A_P0_STATIC_TYPEINFO_RELA="
            f"type={rela.r_type} sym={rela.sym} addend=0x{rela.addend & ((1 << 64) - 1):x} section={rela.section}"
        )

    function_targets: list[int] = []
    for slot in range(args.static_vtable_slots):
        address = vptr + slot * 8
        try:
            raw = elf.qword(address)
            resolved, relas = elf.resolved_qword(address)
        except RuntimeError:
            break
        classification = "exec" if elf.is_exec_vaddr(resolved) else "nonexec"
        if classification == "exec":
            function_targets.append(resolved)
        rela_text = ",".join(
            f"{rela.r_type}:{rela.sym}:0x{rela.addend & ((1 << 64) - 1):x}"
            for rela in relas
        ) or "none"
        print(
            "TRACK_A_P0_STATIC_VTABLE_SLOT="
            f"{slot} address=0x{address:x} raw=0x{raw:x} resolved=0x{resolved:x} "
            f"class={classification} rela={rela_text}"
        )

    type_string_vas: list[int] = []
    for file_offset in elf.find_bytes(b"tibia::game::TPlayerData"):
        va = elf.offset_to_vaddr(file_offset)
        print(
            "TRACK_A_P0_STATIC_TYPE_STRING="
            f"file_offset=0x{file_offset:x} vaddr={f'0x{va:x}' if va is not None else 'unmapped'}"
        )
        if va is not None:
            type_string_vas.append(va)

    semantic_strings: list[tuple[int, int | None, str]] = []
    for offset, value in extract_ascii_strings(elf.data):
        lowered = value.lower()
        if (
            "position" in lowered
            or "coordinate" in lowered
            or "playerdata" in lowered
            or "worldmap" in lowered
        ):
            semantic_strings.append((offset, elf.offset_to_vaddr(offset), value))
    print(f"TRACK_A_P0_STATIC_SEMANTIC_STRING_COUNT={len(semantic_strings)}")
    for offset, va, value in semantic_strings[:120]:
        compact = value if len(value) <= 180 else value[:177] + "..."
        print(
            "TRACK_A_P0_STATIC_SEMANTIC_STRING="
            f"file_offset=0x{offset:x} vaddr={f'0x{va:x}' if va is not None else 'unmapped'} text={compact}"
        )

    xref_targets = {vptr, typeinfo, *type_string_vas}
    xrefs = elf.find_rip_xrefs(xref_targets, limit=max(args.static_xref_limit, 1))
    print(f"TRACK_A_P0_STATIC_STRUCTURAL_XREFS={len(xrefs)}")
    for address, target, kind in xrefs:
        print(
            "TRACK_A_P0_STATIC_XREF="
            f"address=0x{address:x} target=0x{target:x} kind={kind}"
        )

    disasm_addresses: list[int] = []
    for address, _target, _kind in xrefs:
        if address not in disasm_addresses:
            disasm_addresses.append(address)
    for target in function_targets:
        if target not in disasm_addresses:
            disasm_addresses.append(target)
    disassemble_windows(client, disasm_addresses, args.static_disasm_limit)
    nearby_type_strings(client)
    print("TRACK_A_P0_STATIC_PROBE_COMPLETE=true")
    return 0


def runtime_probe(args: argparse.Namespace, client: Path) -> int:
    if args.pid is None:
        raise SystemExit("--pid is required unless --static-only is used")
    if resolved_exe(args.pid) != client:
        raise SystemExit(f"PID exe mismatch: {resolved_exe(args.pid)} != {client}")

    print(f"TRACK_A_P0_PID={args.pid}")
    regions = read_maps(args.pid)
    base = main_base(regions, client)
    expected_vptr = base + args.vptr_offset
    print(f"TRACK_A_P0_MAIN_BASE=0x{base:x}")
    print(f"TRACK_A_P0_TPLAYERDATA_VPTR=0x{expected_vptr:x}")

    mem_fd = os.open(f"/proc/{args.pid}/mem", os.O_RDONLY | os.O_CLOEXEC)
    try:
        hits = find_typed_hits(mem_fd, regions, expected_vptr)
        print(f"TRACK_A_P0_TPLAYERDATA_TYPED_HITS={len(hits)}")
        for index, address in enumerate(hits):
            print(f"TRACK_A_P0_TPLAYERDATA_OBJECT[{index}]=0x{address:x}")
            blob = os.pread(mem_fd, args.object_bytes, address)
            inline = scan_inline_candidates(blob)
            print(f"TRACK_A_P0_INLINE_XYZ_CANDIDATES[{index}]={len(inline)}")
            for encoding, offset, xyz in inline[:64]:
                print(
                    f"TRACK_A_P0_INLINE_CANDIDATE object=0x{address:x} "
                    f"encoding={encoding} offset=0x{offset:x} xyz={xyz[0]},{xyz[1]},{xyz[2]}"
                )
            pointed = first_level_pointer_candidates(mem_fd, regions, blob)
            print(f"TRACK_A_P0_LEVEL1_XYZ_CANDIDATES[{index}]={len(pointed)}")
            for owner_offset, target, encoding, field_offset, xyz in pointed:
                print(
                    f"TRACK_A_P0_LEVEL1_CANDIDATE object=0x{address:x} owner_offset=0x{owner_offset:x} "
                    f"target=0x{target:x} encoding={encoding} field_offset=0x{field_offset:x} "
                    f"xyz={xyz[0]},{xyz[1]},{xyz[2]}"
                )
    finally:
        os.close(mem_fd)

    strip_oracle(args.strips)
    nearby_type_strings(client)
    print("TRACK_A_P0_PASSIVE_PROBE_COMPLETE=true")
    return 0


def main() -> int:
    args = parse_args()
    client, _actual_size, _actual_sha = exact_client_fence(args)
    if args.static_only:
        return static_elf_probe(args, client)
    return runtime_probe(args, client)


if __name__ == "__main__":
    raise SystemExit(main())
