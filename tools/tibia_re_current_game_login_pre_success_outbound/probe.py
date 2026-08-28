#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP, X86_REG_RSP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

SAFETY = {
    'runtime_access': 'none',
    'login_performed': False,
    'secret_access': False,
    'raw_client_uploaded': False,
}

LOGIN_OUTER_FIELDS = {
    '1': {'storage': 0x30, 'kind': 'varint'},
    '2': {'storage': 0x34, 'kind': 'varint'},
    '3': {'storage': 0x38, 'kind': 'varint'},
    '4': {'storage': 0x18, 'kind': 'bytes'},
    '5': {'storage': 0x20, 'kind': 'bytes'},
    '6': {'storage': 0x3C, 'kind': 'varint'},  # field6 exact-current schema slot
    '7': {'storage': 0x28, 'kind': 'message'},
}

NESTED_AUTH_SLOT_TO_FIELD = {
    0x30: '1',
    0x40: '2',
    0x18: '5',
    0x50: '6',
    0x60: '7',
}


@dataclass(frozen=True)
class Section:
    name: str
    offset: int
    size: int
    va: int
    flags: int


class Image:
    def __init__(self, path: Path):
        self.raw = path.read_bytes()
        with path.open('rb') as fh:
            elf = ELFFile(fh)
            self.sections = [Section(s.name, int(s['sh_offset']), int(s['sh_size']), int(s['sh_addr']), int(s['sh_flags'])) for s in elf.iter_sections() if int(s['sh_size'])]
            self.rel: dict[int, int] = {}
            for sec in elf.iter_sections():
                if isinstance(sec, RelocationSection):
                    for r in sec.iter_relocations():
                        if r.is_RELA():
                            self.rel[int(r['r_offset'])] = int(r['r_addend']) & 0xFFFFFFFFFFFFFFFF
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted((int(e['initial_location']), int(e['initial_location']) + int(e['address_range'])) for e in dwarf.EH_CFI_entries() if isinstance(e, FDE))
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def va_to_off(self, va: int) -> int:
        for s in self.sections:
            if s.va <= va < s.va + s.size:
                return s.offset + va - s.va
        raise ValueError(hex(va))

    def off_to_va(self, off: int) -> int | None:
        for s in self.sections:
            if s.offset <= off < s.offset + s.size:
                return s.va + off - s.offset
        return None

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def bytes(self, va: int, size: int) -> bytes:
        o = self.va_to_off(va)
        return self.raw[o:o + size]

    def u32(self, va: int) -> int:
        return struct.unpack_from('<I', self.raw, self.va_to_off(va))[0]

    def i32(self, va: int) -> int:
        return struct.unpack_from('<i', self.raw, self.va_to_off(va))[0]

    def u64(self, va: int) -> int:
        return struct.unpack_from('<Q', self.raw, self.va_to_off(va))[0]

    def qword(self, va: int) -> int:
        return self.rel.get(va, self.u64(va) if self.mapped(va, 8) else 0)

    def occ(self, text: str) -> list[int]:
        needle = text.encode('utf-8')
        out = []
        p = 0
        while True:
            p = self.raw.find(needle, p)
            if p < 0:
                return out
            va = self.off_to_va(p)
            if va is not None:
                out.append(va)
            p += 1

    def fde(self, va: int) -> tuple[int, int] | None:
        rows = [x for x in self.fdes if x[0] <= va < x[1]]
        return rows[0] if len(rows) == 1 else None

    def instructions(self, fde: tuple[int, int]):
        return list(self.md.disasm(self.bytes(fde[0], fde[1] - fde[0]), fde[0]))


def hx(value: int | None) -> str | None:
    return None if value is None else f'0x{value:x}'


def mangled(full: str) -> str:
    return 'N' + ''.join(str(len(part)) + part for part in full.split('::')) + 'E'


def exact_vtable(img: Image, simple: str, full: str) -> dict:
    expected = mangled(full)
    rows = []
    for at in img.occ(simple):
        off = img.va_to_off(at)
        a = img.raw.rfind(b'\0', max(0, off - 256), off) + 1
        b = img.raw.find(b'\0', off, min(len(img.raw), off + 768))
        if b < 0:
            continue
        try:
            name = img.raw[a:b].decode('ascii')
        except UnicodeDecodeError:
            continue
        if name != expected:
            continue
        name_va = img.off_to_va(a)
        for where, value in img.rel.items():
            if value != name_va:
                continue
            rtti = where - 8
            for type_slot, type_value in img.rel.items():
                if type_value != rtti:
                    continue
                ap = type_slot + 8
                if not img.mapped(ap - 16, 24) or img.u64(ap - 16) != 0:
                    continue
                slots = []
                for offset in range(0, 0x180, 8):
                    if not img.mapped(ap + offset, 8):
                        break
                    target = img.qword(ap + offset)
                    slots.append({'offset': offset, 'target': target, 'executable': img.executable(target)})
                rows.append({'rtti': rtti, 'address_point': ap, 'slots': slots})
    unique = {(r['rtti'], r['address_point']): r for r in rows}
    if len(unique) != 1:
        raise RuntimeError(f'VTABLE_AMBIGUOUS:{full}:{len(unique)}')
    return next(iter(unique.values()))


def qstring(img: Image, base: int, index: int) -> str:
    ent = base + index * 8
    rel = img.u32(ent)
    ln = img.u32(ent + 4)
    if ln > 4096:
        raise ValueError
    return img.bytes(base + rel, ln).decode('utf-8')


def stringdata_bases_for_literal(img: Image, literal: str) -> list[int]:
    out = set()
    ln = len(literal.encode())
    for sva in img.occ(literal):
        lo = max(0, img.va_to_off(sva) - 0x10000)
        hi = img.va_to_off(sva)
        for eoff in range(lo, hi + 1, 4):
            eva = img.off_to_va(eoff)
            if eva is None or not img.mapped(eva, 8):
                continue
            try:
                rel = img.u32(eva)
                size = img.u32(eva + 4)
            except Exception:
                continue
            if size != ln or rel > 0x20000:
                continue
            base = sva - rel
            if base > eva or (eva - base) % 8:
                continue
            idx = (eva - base) // 8
            try:
                if qstring(img, base, idx) == literal and qstring(img, base, 0):
                    out.add(base)
            except Exception:
                pass
    return sorted(out)


def parse_meta(img: Image, sbase: int, mbase: int) -> dict | None:
    if not img.mapped(mbase, 56):
        return None
    try:
        h = [img.u32(mbase + i * 4) for i in range(14)]
    except Exception:
        return None
    rev, ci, _cic, _cio, mc, mo, _pc, _po, _ec, _eo, _cc, _co, _flags, sc = h
    if not (7 <= rev <= 20 and ci == 0 and 0 < mc <= 1000 and 14 <= mo < 200000 and sc <= mc):
        return None
    rows = []
    try:
        for i in range(mc):
            p = mbase + (mo + i * 6) * 4
            r = [img.u32(p + j * 4) for j in range(6)]
            name = qstring(img, sbase, r[0])
            if not name:
                return None
            rows.append({'index': i, 'name': name, 'argc': r[1], 'param_offset': r[2], 'flags': r[4]})
    except Exception:
        return None
    return {'class_name': qstring(img, sbase, 0), 'method_count': mc, 'signal_count': sc, 'rows': rows}


def recover_qmeta_jump_table(img: Image, static_metacall: int, method_count: int) -> tuple[int, list[int]]:
    ins = list(img.md.disasm(img.bytes(static_metacall, 0x900), static_metacall))[:360]
    candidates = []
    for pos, row in enumerate(ins):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        op = row.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        reg = row.operands[0].reg
        table = row.address + row.size + int(op.mem.disp)
        used = any(any(xop.type == X86_OP_MEM and xop.mem.base == reg and xop.mem.scale == 4 for xop in x.operands) for x in ins[pos + 1:pos + 12])
        if not used:
            continue
        try:
            targets = [table + img.i32(table + 4 * i) for i in range(method_count)]
        except Exception:
            continue
        if not all(img.executable(t) for t in targets):
            continue
        bounded = any(prev.mnemonic == 'cmp' and len(prev.operands) >= 2 and prev.operands[0].type == X86_OP_REG and img.md.reg_name(prev.operands[0].reg) == 'edx' and prev.operands[1].type == X86_OP_IMM and int(prev.operands[1].imm) == method_count - 1 for prev in ins[max(0, pos - 10):pos])
        if bounded:
            candidates.append((table, tuple(targets)))
    unique = set(candidates)
    if len(unique) != 1:
        raise RuntimeError(f'QMETA_JUMP_TABLE_AMBIGUOUS:{len(unique)}')
    table, targets = next(iter(unique))
    return table, list(targets)


def exact_qmeta_class(img: Image, class_name: str, required: tuple[str, ...]) -> dict:
    candidates = []
    seed = required[0]
    for sbase in stringdata_bases_for_literal(img, seed):
        for mbase in range(max(0, sbase - 0x20000) & ~3, sbase + 0x20000, 4):
            meta = parse_meta(img, sbase, mbase)
            if not meta or meta['class_name'] != class_name:
                continue
            names = {r['name'] for r in meta['rows']}
            if not set(required).issubset(names):
                continue
            static = []
            for where, value in img.rel.items():
                if value == sbase and img.rel.get(where + 8) == mbase:
                    target = img.rel.get(where + 16)
                    if target is not None and img.executable(target):
                        static.append(target)
            if len(static) != 1:
                continue
            table, targets = recover_qmeta_jump_table(img, static[0], meta['method_count'])
            methods = {}
            for row in meta['rows']:
                if row['name'] in required:
                    target = targets[row['index']]
                    methods[row['name']] = {'index': row['index'], 'target': target, 'fde': img.fde(target)}
            candidates.append({'metadata': mbase, 'stringdata': sbase, 'static_metacall': static[0], 'jump_table': table, 'methods': methods})
    unique = {(x['metadata'], x['stringdata']): x for x in candidates}
    if len(unique) != 1:
        raise RuntimeError(f'QMETA_CLASS_AMBIGUOUS:{class_name}:{len(unique)}')
    return next(iter(unique.values()))


def slot_target(vtable: dict, offset: int) -> int:
    rows = [r for r in vtable['slots'] if r['offset'] == offset and r['executable']]
    if len(rows) != 1:
        raise RuntimeError(f'VTABLE_SLOT_AMBIGUOUS:{offset:#x}:{len(rows)}')
    return rows[0]['target']


def rip_target(ins) -> int | None:
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return ins.address + ins.size + int(op.mem.disp)
    return None


def producer_stack_object_base(img: Image, instructions, vtable_ap: int) -> tuple[int, int]:
    candidates = []
    for i, ins in enumerate(instructions):
        if ins.mnemonic != 'lea' or len(ins.operands) < 2 or ins.operands[0].type != X86_OP_REG:
            continue
        if rip_target(ins) != vtable_ap:
            continue
        reg = ins.operands[0].reg
        for row in instructions[i + 1:i + 8]:
            if row.mnemonic != 'mov' or len(row.operands) < 2:
                continue
            dst, src = row.operands[0], row.operands[1]
            if dst.type == X86_OP_MEM and dst.mem.base == X86_REG_RSP and src.type == X86_OP_REG and src.reg == reg:
                candidates.append((ins.address, int(dst.mem.disp)))
                break
    if not candidates:
        raise RuntimeError('LOGIN_STACK_OBJECT_MISSING')
    bases = {base for _, base in candidates}
    if len(bases) != 1:
        raise RuntimeError(f'LOGIN_STACK_OBJECT_BASE_AMBIGUOUS:{len(candidates)}:{candidates}')
    # The same stack object can receive its generated vtable again during cleanup.
    # The earliest reference is the construction boundary; later same-base references
    # are teardown/reset and do not create a second login object.
    return min(candidates, key=lambda row: row[0])


def writes_overlapping(instructions, start_at: int, stack_offset: int, width: int = 4) -> list[dict]:
    rows = []
    for ins in instructions:
        if ins.address < start_at or not ins.operands:
            continue
        dst = ins.operands[0]
        if dst.type != X86_OP_MEM or dst.mem.base != X86_REG_RSP:
            continue
        size = int(dst.size or 0)
        if size <= 0:
            continue
        lo = int(dst.mem.disp)
        hi = lo + size
        if max(lo, stack_offset) < min(hi, stack_offset + width):
            src = ins.op_str.split(',', 1)[1].strip() if ',' in ins.op_str else ''
            rows.append({'at': ins.address, 'mnemonic': ins.mnemonic, 'operand': ins.op_str, 'destination_offset': lo, 'size': size, 'source': src})
    return rows


def field_presence_from_writes(writes: list[dict], exact_offset: int) -> str:
    exact = [w for w in writes if w['destination_offset'] == exact_offset and w['size'] == 4]
    if exact:
        return 'PRESENT'
    if writes:
        return 'NO_EXACT_WRITE_OVERLAP_ONLY'
    return 'NOT_WRITTEN_IN_PRIMARY_PRODUCER'


def refs_to_targets_in_fde(img: Image, instructions, targets: dict[int, int]) -> dict[str, list[int]]:
    out = {f'0x{k:x}': [] for k in targets}
    reverse = {v: k for k, v in targets.items()}
    for ins in instructions:
        target = rip_target(ins)
        if target in reverse:
            out[f'0x{reverse[target]:x}'].append(ins.address)
        if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            target = int(ins.operands[0].imm)
            if target in reverse:
                out[f'0x{reverse[target]:x}'].append(ins.address)
    return out


def direct_calls(img: Image, fde: tuple[int, int] | None) -> list[int]:
    if not fde:
        return []
    out = []
    for ins in img.instructions(fde):
        if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            out.append(int(ins.operands[0].imm))
    return out


def bounded_pre_success_sequence(img: Image, game_client: dict, queue: dict) -> dict:
    qmethods = queue['methods']
    send_targets = {name: row['target'] for name, row in qmethods.items() if name.startswith('send')}
    success = qmethods['receivedLoginSuccessMessage']['target']
    roots = [game_client['methods'][name]['fde'] for name in ('connectClientToGameserverWithExistingCredentials', 'onConnectClientToGameserver')]
    roots = [r for r in roots if r]
    seen_fdes = set(roots)
    frontier = deque((r, 0) for r in roots)
    found: dict[str, list[dict]] = {name: [] for name in send_targets}
    success_edges = []
    while frontier:
        fde, depth = frontier.popleft()
        for target in direct_calls(img, fde):
            for name, send_target in send_targets.items():
                if target == send_target:
                    found[name].append({'caller_fde': fde, 'depth': depth})
            if target == success:
                success_edges.append({'caller_fde': fde, 'depth': depth})
            if depth >= 2:
                continue
            next_fde = img.fde(target)
            if next_fde and next_fde not in seen_fdes and (next_fde[1] - next_fde[0]) < 0x8000:
                seen_fdes.add(next_fde)
                frontier.append((next_fde, depth + 1))
    proven_sends = [name for name, rows in found.items() if rows]
    classification = 'PROVEN_BOUNDED' if 'sendLogin' in proven_sends else 'UNKNOWN'
    return {
        'classification': classification,
        'search_depth': 2,
        'root_fdes': [[hx(a), hx(b)] for a, b in roots],
        'proved_send_methods': proven_sends,
        'send_edges': {name: [{'caller_fde': [hx(x['caller_fde'][0]), hx(x['caller_fde'][1])], 'depth': x['depth']} for x in rows] for name, rows in found.items()},
        'received_login_success_direct_edges_in_bounded_graph': [{'caller_fde': [hx(x['caller_fde'][0]), hx(x['caller_fde'][1])], 'depth': x['depth']} for x in success_edges],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    img = Image(args.client)
    handler = exact_vtable(img, 'TLoginProtocolMessageHandler', 'tibia::authentication::TLoginProtocolMessageHandler')
    auth = exact_vtable(img, 'TAuthenticationAndEncryptionInfo', 'tibia::authentication::TAuthenticationAndEncryptionInfo')
    login_type = exact_vtable(img, 'GameclientMessageLogin', 'tibia::protobuf::protocol::GameclientMessageLogin')
    nested_type = exact_vtable(img, 'LoginRSAEncryptedBlock', 'tibia::protobuf::protocol::LoginRSAEncryptedBlock')
    producer = slot_target(handler, 0x60)
    producer_fde = img.fde(producer)
    if not producer_fde:
        raise RuntimeError('PRIMARY_LOGIN_PRODUCER_FDE_UNKNOWN')
    pins = img.instructions(producer_fde)

    construction_at, stack_base = producer_stack_object_base(img, pins, login_type['address_point'])
    outer_fields = {}
    outer_write_evidence = {}
    for field, spec in LOGIN_OUTER_FIELDS.items():
        if spec['kind'] != 'varint':
            continue
        absolute = stack_base + spec['storage']
        writes = writes_overlapping(pins, construction_at, absolute, 4)
        outer_fields[field] = field_presence_from_writes(writes, absolute)
        outer_write_evidence[field] = [{**w, 'at': hx(w['at'])} for w in writes]

    auth_slot_targets = {slot: slot_target(auth, slot) for slot in NESTED_AUTH_SLOT_TO_FIELD}
    auth_refs = refs_to_targets_in_fde(img, pins, auth_slot_targets)
    nested_fields = {}
    for slot, field in NESTED_AUTH_SLOT_TO_FIELD.items():
        refs = auth_refs[f'0x{slot:x}']
        nested_fields[field] = 'SOURCE_REFERENCED_BY_PRIMARY_PRODUCER' if refs else 'NO_SOURCE_REFERENCE_IN_PRIMARY_PRODUCER'

    queue = exact_qmeta_class(img, 'tibia::protocol::TProtocolMessageQueue', ('sendLogin', 'sendEnterWorld', 'sendSecondaryLogin', 'receivedLoginSuccessMessage'))
    game_client = exact_qmeta_class(img, 'tibia::client::TGameClient', ('connectClientToGameserverWithExistingCredentials', 'onConnectClientToGameserver'))
    sequence = bounded_pre_success_sequence(img, game_client, queue)

    result = {
        'schema': 'otclient.track-a.current-game-login-pre-success-outbound.v1',
        **SAFETY,
        'exact_client': {'sha256': hashlib.sha256(img.raw).hexdigest(), 'size': len(img.raw)},
        'primary_login_producer': {
            'target': hx(producer),
            'fde': [hx(producer_fde[0]), hx(producer_fde[1])],
            'login_stack_object_construct_at': hx(construction_at),
            'login_stack_object_base_offset': hex(stack_base),
            'login_message_vtable': hx(login_type['address_point']),
            'nested_message_vtable': hx(nested_type['address_point']),
        },
        'primary_producer_field_presence': {
            'outer_fields': outer_fields,
            'outer_varint_write_evidence': outer_write_evidence,
            'nested_fields': nested_fields,
            'nested_auth_slot_reference_sites': {k: [hx(x) for x in v] for k, v in auth_refs.items()},
            'classification_boundary': 'SOURCE_REFERENCE_DOES_NOT_PROVE_NONEMPTY_RUNTIME_STRING',
        },
        'queue_qmeta': {name: {'index': row['index'], 'target': hx(row['target']), 'fde': [hx(row['fde'][0]), hx(row['fde'][1])] if row['fde'] else None} for name, row in queue['methods'].items()},
        'game_client_qmeta': {name: {'index': row['index'], 'target': hx(row['target']), 'fde': [hx(row['fde'][0]), hx(row['fde'][1])] if row['fde'] else None} for name, row in game_client['methods'].items()},
        'pre_success_send_sequence': sequence,
        'markers': {'PRIMARY_PRODUCER_FIELD_PRESENCE': True, 'PRE_SUCCESS_SEND_SEQUENCE': True},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_PRE_SUCCESS_OUTBOUND=PASS')
    print('PRIMARY_PRODUCER_FIELD_PRESENCE=PASS')
    print('PRE_SUCCESS_SEND_SEQUENCE=' + sequence['classification'])
    print('OUTER_FIELD6=' + outer_fields.get('6', 'UNKNOWN'))
    for field in ('1', '2', '5', '6', '7'):
        print(f'NESTED_FIELD_{field}=' + nested_fields.get(field, 'UNKNOWN'))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')


if __name__ == '__main__':
    main()
