#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.dwarf.callframe import FDE


@dataclass(frozen=True)
class Section:
    name: str
    offset: int
    size: int
    va: int
    flags: int


class Image:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_bytes()
        with path.open('rb') as fh:
            elf = ELFFile(fh)
            self.sections = [
                Section(s.name, int(s['sh_offset']), int(s['sh_size']), int(s['sh_addr']), int(s['sh_flags']))
                for s in elf.iter_sections() if int(s['sh_size']) > 0
            ]
            self.relocations: dict[int, int] = {}
            for sec in elf.iter_sections():
                if not isinstance(sec, RelocationSection):
                    continue
                for rel in sec.iter_relocations():
                    if rel.is_RELA():
                        self.relocations[int(rel['r_offset'])] = int(rel['r_addend'])
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (int(e['initial_location']), int(e['initial_location']) + int(e['address_range']))
                for e in dwarf.EH_CFI_entries() if isinstance(e, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def off_to_va(self, off: int) -> int | None:
        for sec in self.sections:
            if sec.offset <= off < sec.offset + sec.size:
                return sec.va + off - sec.offset
        return None

    def va_to_off(self, va: int) -> int:
        for sec in self.sections:
            if sec.va <= va < sec.va + sec.size:
                return sec.offset + va - sec.va
        raise ValueError(f'unmapped VA 0x{va:x}')

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((sec.flags & 4) and sec.va <= va < sec.va + sec.size for sec in self.sections)

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off:off + size]

    def u64(self, va: int) -> int:
        return struct.unpack_from('<Q', self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        if va in self.relocations:
            return int(self.relocations[va]) & 0xffffffffffffffff
        return self.u64(va)

    def string_occurrences(self, value: str) -> list[int]:
        needle = value.encode('utf-8')
        out: list[int] = []
        pos = 0
        while True:
            off = self.raw.find(needle, pos)
            if off < 0:
                return out
            va = self.off_to_va(off)
            if va is not None:
                out.append(va)
            pos = off + 1

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def fde_instructions(self, va: int, limit: int = 240) -> dict:
        fde = self.containing_fde(va)
        if not fde:
            raise RuntimeError(f'no unique FDE for 0x{va:x}')
        lo, hi = fde
        rows = []
        for ins in list(self.md.disasm(self.bytes(lo, hi - lo), lo))[:limit]:
            rows.append({'at': hx(ins.address), 'mnemonic': ins.mnemonic, 'operand': ins.op_str})
        return {'fde': [hx(lo), hx(hi)], 'instructions': rows}


def hx(value: int) -> str:
    return f'0x{value:x}'


def expected_mangled_full(full: str) -> str:
    return 'N' + ''.join(str(len(part)) + part for part in full.split('::')) + 'E'


def rtti_vtable_candidates(img: Image, simple_name: str) -> list[dict]:
    found = {}
    for occurrence in img.string_occurrences(simple_name):
        off = img.va_to_off(occurrence)
        start = img.raw.rfind(b'\0', max(0, off - 192), off) + 1
        end = img.raw.find(b'\0', off, min(len(img.raw), off + 512))
        if end < 0:
            continue
        try:
            text = img.raw[start:end].decode('ascii')
        except UnicodeDecodeError:
            continue
        if simple_name not in text or '::' in text or not text.startswith('N'):
            continue
        name_va = img.off_to_va(start)
        if name_va is None:
            continue
        for name_ref, addend in img.relocations.items():
            if addend != name_va:
                continue
            rtti = name_ref - 8
            aps = []
            for type_slot, type_addend in img.relocations.items():
                if type_addend != rtti:
                    continue
                ap = type_slot + 8
                if not img.mapped(ap - 16, 24) or img.u64(ap - 16) != 0:
                    continue
                slots = []
                for slot_off in range(0, 0xc0, 8):
                    if not img.mapped(ap + slot_off, 8):
                        break
                    target = img.qword(ap + slot_off)
                    slots.append({'offset': hex(slot_off), 'target': hx(target), 'executable': img.executable(target)})
                aps.append({'address_point': hx(ap), 'slots': slots})
            if aps:
                found[(text, rtti)] = {'rtti_name': text, 'rtti': hx(rtti), 'address_points': aps}
    return sorted(found.values(), key=lambda row: (row['rtti_name'], row['rtti']))


def recover_exact_named_vtable(img: Image, simple_name: str, full_name: str) -> dict:
    expected = expected_mangled_full(full_name)
    rows = [row for row in rtti_vtable_candidates(img, simple_name) if row['rtti_name'] == expected]
    if len(rows) != 1:
        raise RuntimeError(f'{full_name}: expected one exact RTTI row, got {len(rows)}')
    aps = rows[0]['address_points']
    if len(aps) != 1:
        raise RuntimeError(f'{full_name}: expected one vtable AP, got {len(aps)}')
    return {'rtti_name': rows[0]['rtti_name'], 'rtti': rows[0]['rtti'], **aps[0]}


def slot_target(vtable: dict, offset: str) -> int:
    rows = {row['offset']: row for row in vtable['slots']}
    row = rows.get(offset)
    if not row or not row.get('executable'):
        raise RuntimeError(f'missing executable vslot {offset}')
    return int(row['target'], 16)


def reference_scan(img: Image, rip_targets: set[int], direct_targets: set[int]) -> dict:
    rip = {target: [] for target in rip_targets}
    direct = {target: [] for target in direct_targets}
    for sec in img.sections:
        if not (sec.flags & 4):
            continue
        blob = img.raw[sec.offset:sec.offset + sec.size]
        for ins in img.md.disasm(blob, sec.va):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
                target = int(ins.operands[0].imm)
                if target in direct:
                    direct[target].append(ins.address)
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    target = ins.address + ins.size + int(op.mem.disp)
                    if target in rip:
                        rip[target].append(ins.address)
    return {'rip': rip, 'direct': direct}


def instruction_context(img: Image, center: int, before: int = 7, after: int = 7) -> list[dict]:
    fde = img.containing_fde(center)
    if not fde:
        return []
    lo, hi = fde
    ins = list(img.md.disasm(img.bytes(lo, hi - lo), lo))
    indexes = [i for i, row in enumerate(ins) if row.address == center]
    if len(indexes) != 1:
        return []
    idx = indexes[0]
    return [
        {'at': hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}
        for row in ins[max(0, idx-before):min(len(ins), idx+after+1)]
    ]


def safe_cstring(img: Image, va: int, limit: int = 160) -> str | None:
    if not img.mapped(va, 1):
        return None
    off = img.va_to_off(va)
    chunk = img.raw[off:off+limit]
    nul = chunk.find(b'\0')
    if nul < 2:
        return None
    raw = chunk[:nul]
    if not all(0x20 <= b <= 0x7e for b in raw):
        return None
    try:
        text = raw.decode('ascii')
    except UnicodeDecodeError:
        return None
    return text if len(text) <= limit else None


def static_keyword_strings(img: Image, tokens: tuple[str, ...], max_hits: int = 1600) -> dict[int, str]:
    out: dict[int, str] = {}
    lower_tokens = tuple(token.lower() for token in tokens)
    for match in re.finditer(rb'[ -~]{4,160}\x00', img.raw):
        raw = match.group(0)[:-1]
        try:
            text = raw.decode('ascii')
        except UnicodeDecodeError:
            continue
        low = text.lower()
        if not any(token in low for token in lower_tokens):
            continue
        va = img.off_to_va(match.start())
        if va is not None:
            out[va] = text
            if len(out) >= max_hits:
                break
    return out


def fde_key(img: Image, site: int) -> str | None:
    fde = img.containing_fde(site)
    return f'{hx(fde[0])}..{hx(fde[1])}' if fde else None


def bounded_contexts(img: Image, sites: list[int], limit: int = 80) -> list[dict]:
    rows = []
    for site in sites[:limit]:
        rows.append({'site': hx(site), 'fde': fde_key(img, site), 'context': instruction_context(img, site)})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--version', required=True)
    ap.add_argument('--packed-sha256', required=True)
    ap.add_argument('--unpacked-sha256', required=True)
    ap.add_argument('--unpacked-size', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    img = Image(args.client)
    auth = recover_exact_named_vtable(
        img, 'TAuthenticationAndEncryptionInfo',
        'tibia::authentication::TAuthenticationAndEncryptionInfo')
    handler = recover_exact_named_vtable(
        img, 'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler')

    selected_offsets = ('0x10', '0x18', '0x30', '0x40', '0x50', '0x60', '0x90')
    getter_targets = {offset: slot_target(auth, offset) for offset in selected_offsets}
    producer = slot_target(handler, '0x60')
    producer_snapshot = img.fde_instructions(producer, limit=1800)
    producer_fde = f'{producer_snapshot["fde"][0]}..{producer_snapshot["fde"][1]}'

    keyword_map = static_keyword_strings(
        img,
        ('session', 'character', 'password', 'account', 'auth', 'token', 'challenge', 'asset', 'version', 'build', 'login'),
    )
    rip_targets = set(getter_targets.values()) | {int(auth['address_point'], 16)} | set(keyword_map)
    direct_targets = set(getter_targets.values()) | {producer}
    refs = reference_scan(img, rip_targets, direct_targets)

    identity_refs = {}
    relevant_fdes = {producer_fde}
    for offset, target in getter_targets.items():
        rip_sites = refs['rip'].get(target, [])
        direct_sites = refs['direct'].get(target, [])
        contexts = bounded_contexts(img, sorted(set(rip_sites + direct_sites)))
        identity_refs[offset] = {
            'target': hx(target),
            'rip_identity_refs': [hx(x) for x in rip_sites[:200]],
            'direct_calls': [hx(x) for x in direct_sites[:200]],
            'contexts': contexts,
        }
        relevant_fdes.update(row['fde'] for row in contexts if row.get('fde'))

    auth_ap = int(auth['address_point'], 16)
    auth_vtable_refs = bounded_contexts(img, refs['rip'].get(auth_ap, []), limit=120)
    relevant_fdes.update(row['fde'] for row in auth_vtable_refs if row.get('fde'))

    semantic_contexts = []
    for target, text in sorted(keyword_map.items()):
        for site in refs['rip'].get(target, []):
            key = fde_key(img, site)
            if key not in relevant_fdes:
                continue
            semantic_contexts.append({
                'literal': text,
                'literal_va': hx(target),
                'site': hx(site),
                'fde': key,
                'context': instruction_context(img, site),
            })
            if len(semantic_contexts) >= 240:
                break
        if len(semantic_contexts) >= 240:
            break

    producer_rip_literals = []
    lo, hi = [int(v, 16) for v in producer_snapshot['fde']]
    for ins in img.md.disasm(img.bytes(lo, hi-lo), lo):
        for op in ins.operands:
            if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                continue
            target = ins.address + ins.size + int(op.mem.disp)
            direct = safe_cstring(img, target)
            indirect = None
            if img.mapped(target, 8):
                q = img.qword(target)
                indirect = safe_cstring(img, q)
            if direct or indirect:
                producer_rip_literals.append({
                    'site': hx(ins.address),
                    'target': hx(target),
                    'direct_ascii': direct,
                    'qword_target_ascii': indirect,
                })

    auth_slot_snapshots = {
        offset: {'target': hx(target), 'snapshot': img.fde_instructions(target, limit=320)}
        for offset, target in getter_targets.items()
    }

    result = {
        'schema': 'otclient.track-a.current-game-login-field-provenance.discovery.v1',
        'exact_client': {
            'version': args.version,
            'packed_sha256': args.packed_sha256,
            'unpacked_sha256': args.unpacked_sha256,
            'unpacked_size': args.unpacked_size,
        },
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'authentication_info': auth,
        'login_handler': handler,
        'producer': {
            'slot': '0x60',
            'target': hx(producer),
            'snapshot': producer_snapshot,
            'rip_ascii_literals': producer_rip_literals,
        },
        'auth_slot_snapshots': auth_slot_snapshots,
        'auth_slot_identity_refs': identity_refs,
        'auth_vtable_refs': auth_vtable_refs,
        'semantic_keyword_contexts': semantic_contexts,
        'classification': {
            'field_value_provenance': 'DISCOVERY_ONLY',
            'user_facing_semantic_field_names': 'UNKNOWN',
            'password_session_to_rsa_field_mapping': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_FIELD_PROVENANCE_PROBE=PASS')
    print('CURRENT_CLIENT_VERSION=' + args.version)
    print('LOGIN_HANDLER_PRODUCER=' + hx(producer))
    for offset, target in getter_targets.items():
        print(f'AUTH_SLOT_{offset}={hx(target)}')
    print('SEMANTIC_KEYWORD_CONTEXT_COUNT=' + str(len(semantic_contexts)))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
