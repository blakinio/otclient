from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import sys
from typing import Any

try:
    from elftools.elf.elffile import ELFFile
    from elftools.elf.relocation import RelocationSection
except ImportError as exc:  # pragma: no cover - environment dependency
    raise SystemExit("pyelftools is required for runtime profile discovery") from exc


class ResolverError(ValueError):
    pass


def itanium_nested_name(class_name: str) -> bytes:
    parts = class_name.split("::")
    if not parts or any(not part for part in parts):
        raise ResolverError("class name must contain non-empty C++ components")
    return ("N" + "".join(f"{len(part)}{part}" for part in parts) + "E").encode("ascii") + b"\0"


class ElfImage:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_bytes()
        with path.open("rb") as handle:
            elf = ELFFile(handle)
            if elf.elfclass != 64 or not elf.little_endian:
                raise ResolverError("only little-endian ELF64 is supported")
            self.sections = [
                (
                    section.name,
                    int(section["sh_offset"]),
                    int(section["sh_size"]),
                    int(section["sh_addr"]),
                    int(section["sh_flags"]),
                )
                for section in elf.iter_sections()
            ]
            self.relocations: list[tuple[int, int | None, str]] = []
            for section in elf.iter_sections():
                if not isinstance(section, RelocationSection):
                    continue
                symbols = elf.get_section(section["sh_link"]) if section["sh_link"] else None
                for relocation in section.iter_relocations():
                    symbol_name = ""
                    symbol_index = int(relocation["r_info_sym"])
                    if symbol_index and symbols is not None:
                        try:
                            symbol_name = symbols.get_symbol(symbol_index).name
                        except Exception:
                            symbol_name = ""
                    addend = int(relocation["r_addend"]) if relocation.is_RELA() else None
                    self.relocations.append((int(relocation["r_offset"]), addend, symbol_name))
        self.relocations_by_addend: dict[int, list[int]] = {}
        self.relocation_by_offset: dict[int, int] = {}
        for offset, addend, _ in self.relocations:
            if addend is None:
                continue
            self.relocations_by_addend.setdefault(addend, []).append(offset)
            self.relocation_by_offset[offset] = addend

    def offset_to_va(self, offset: int) -> int | None:
        for _, section_offset, size, va, _ in self.sections:
            if section_offset <= offset < section_offset + size:
                return va + (offset - section_offset)
        return None

    def va_to_offset(self, va: int) -> int:
        for _, section_offset, size, section_va, _ in self.sections:
            if section_va <= va < section_va + size:
                return section_offset + (va - section_va)
        raise ResolverError(f"VA 0x{va:x} is not file-backed")

    def qword(self, va: int) -> int:
        return struct.unpack_from("<Q", self.raw, self.va_to_offset(va))[0]

    def executable(self, va: int) -> bool:
        return any((flags & 0x4) and section_va <= va < section_va + size for _, _, size, section_va, flags in self.sections)

    def find_c_string_vas(self, value: bytes) -> list[int]:
        result: list[int] = []
        start = 0
        while True:
            offset = self.raw.find(value, start)
            if offset < 0:
                break
            va = self.offset_to_va(offset)
            if va is not None:
                result.append(va)
            start = offset + 1
        return result


def resolve_primary_vptrs(image: ElfImage, class_name: str) -> list[int]:
    name_vas = image.find_c_string_vas(itanium_nested_name(class_name))
    typeinfos: set[int] = set()
    for name_va in name_vas:
        for relocation_target in image.relocations_by_addend.get(name_va, []):
            if relocation_target >= 8:
                typeinfos.add(relocation_target - 8)

    vptrs: set[int] = set()
    for typeinfo in typeinfos:
        for relocation_target in image.relocations_by_addend.get(typeinfo, []):
            if relocation_target < 8:
                continue
            header = relocation_target - 8
            try:
                offset_to_top = image.qword(header)
            except ResolverError:
                continue
            if offset_to_top != 0:
                continue
            vptr = header + 16
            first = image.relocation_by_offset.get(vptr)
            if first is None:
                try:
                    first = image.qword(vptr)
                except ResolverError:
                    continue
            if image.executable(first):
                vptrs.add(vptr)
    return sorted(vptrs)


def resolve_profile_targets(binary: Path, profile: dict[str, Any]) -> dict[str, Any]:
    targets = profile.get("targets")
    if not isinstance(targets, dict):
        raise ResolverError("profile targets must be an object")
    image = ElfImage(binary)
    output: dict[str, Any] = {}
    for name, target in sorted(targets.items()):
        if not isinstance(target, dict):
            raise ResolverError(f"target {name} must be an object")
        expected_class = target.get("expected_qt_class")
        if not isinstance(expected_class, str) or not expected_class:
            raise ResolverError(f"target {name} expected_qt_class is missing")
        candidates = resolve_primary_vptrs(image, expected_class)
        output[name] = {
            "expected_qt_class": expected_class,
            "primary_vptr_candidates": [f"0x{value:x}" for value in candidates],
            "unique": len(candidates) == 1,
        }
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rediscover exact-client primary vptrs from ELF RTTI/relocations")
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args(argv)
    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    resolved = resolve_profile_targets(args.binary, profile)
    result = {
        "schema": "otclient.tibia-runtime-bridge.discovery.v1",
        "binary": str(args.binary),
        "targets": resolved,
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if all(item["unique"] for item in resolved.values()) else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ResolverError, OSError, json.JSONDecodeError) as exc:
        print(f"resolver error: {exc}", file=sys.stderr)
        raise SystemExit(2)
