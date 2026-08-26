#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

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
                for s in elf.iter_sections()
                if int(s['sh_size']) > 0
            ]
            self.relocations: dict[int, int] = {}
            for sec in elf.iter_sections():
                if not isinstance(sec, RelocationSection):
                    continue
                for rel in sec.iter_relocations():
                    if not rel.is_RELA():
                        continue
                    self.relocations[int(rel['r_offset'])] = int(rel['r_addend'])
            dwarf = elf.get_dwarf_info()
            self.fdes = sorted(
                (int(entry['initial_location']), int(entry['initial_location']) + int(entry['address_range']))
                for entry in dwarf.EH_CFI_entries()
                if isinstance(entry, FDE)
            )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def off_to_va(self, off: int) -> int | None:
        for s in self.sections:
            if s.offset <= off < s.offset + s.size:
                return s.va + (off - s.offset)
        return None

    def va_to_off(self, va: int) -> int:
        for s in self.sections:
            if s.va <= va < s.va + s.size:
                return s.offset + (va - s.va)
        raise ValueError(f'unmapped VA 0x{va:x}')

    def mapped(self, va: int, size: int = 1) -> bool:
        try:
            off = self.va_to_off(va)
        except ValueError:
            return False
        return 0 <= off <= len(self.raw) - size

    def executable(self, va: int) -> bool:
        return any((s.flags & 4) and s.va <= va < s.va + s.size for s in self.sections)

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        matches = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        if len(matches) != 1:
            return None
        return matches[0]

    def u32(self, va: int) -> int:
        return struct.unpack_from('<I', self.raw, self.va_to_off(va))[0]

    def i32(self, va: int) -> int:
        return struct.unpack_from('<i', self.raw, self.va_to_off(va))[0]

    def bytes(self, va: int, size: int) -> bytes:
        off = self.va_to_off(va)
        return self.raw[off:off + size]

    def string_occurrences(self, value: str) -> list[int]:
        needle = value.encode('utf-8')
        out: list[int] = []
        start = 0
        while True:
            off = self.raw.find(needle, start)
            if off < 0:
                return out
            va = self.off_to_va(off)
            if va is not None:
                out.append(va)
            start = off + 1

    def disasm(self, va: int, size: int = 0x300, limit: int = 160):
        return list(self.md.disasm(self.bytes(va, size), va))[:limit]


def qstring(img: Image, sbase: int, index: int) -> str:
    ent = sbase + index * 8
    rel = img.u32(ent)
    length = img.u32(ent + 4)
    if length > 4096:
        raise ValueError('Qt string too long')
    data = img.bytes(sbase + rel, length)
    return data.decode('utf-8', 'strict')


def find_stringdata(img: Image, class_name: str) -> list[int]:
    out: set[int] = set()
    for sva in img.string_occurrences(class_name):
        lower = max(0, sva - 0x10000)
        for base in range(sva & ~3, lower - 1, -4):
            if not img.mapped(base, 8):
                continue
            try:
                if img.u32(base) != sva - base or img.u32(base + 4) != len(class_name.encode()):
                    continue
                if qstring(img, base, 0) == class_name:
                    out.add(base)
            except (ValueError, UnicodeDecodeError, struct.error):
                continue
    return sorted(out)


def parse_meta(img: Image, sbase: int, mbase: int) -> dict | None:
    if not img.mapped(mbase, 56):
        return None
    try:
        h = [img.u32(mbase + i * 4) for i in range(14)]
    except (ValueError, struct.error):
        return None
    rev, class_index, ci_count, ci_off, method_count, method_off, prop_count, prop_off, enum_count, enum_off, ctor_count, ctor_off, flags, signal_count = h
    if not (7 <= rev <= 20 and class_index == 0 and 0 < method_count <= 1000 and 14 <= method_off < 200000 and signal_count <= method_count):
        return None
    if any(x > 10000 for x in (ci_count, prop_count, enum_count, ctor_count)):
        return None
    rows = []
    try:
        if qstring(img, sbase, class_index) == '':
            return None
        for i in range(method_count):
            base = mbase + (method_off + i * 6) * 4
            row = [img.u32(base + j * 4) for j in range(6)]
            name = qstring(img, sbase, row[0])
            if not name or len(name) > 256:
                return None
            rows.append({'index': i, 'name': name, 'argc': row[1], 'param_offset': row[2], 'tag': row[3], 'flags': row[4], 'meta_type_offset': row[5]})
    except (ValueError, UnicodeDecodeError, struct.error):
        return None
    return {
        'revision': rev,
        'class_index': class_index,
        'method_count': method_count,
        'method_offset': method_off,
        'signal_count': signal_count,
        'rows': rows,
    }


def find_metadata(img: Image, sbase: int, required_names: Iterable[str]) -> list[tuple[int, dict]]:
    required = set(required_names)
    results = []
    lo = max(0, sbase - 0x20000)
    hi = sbase + 0x20000
    for mbase in range(lo & ~3, hi, 4):
        meta = parse_meta(img, sbase, mbase)
        if not meta:
            continue
        names = {r['name'] for r in meta['rows']}
        if required.issubset(names):
            results.append((mbase, meta))
    return results


def find_qmeta_static_metacall(img: Image, sbase: int, mbase: int) -> list[dict]:
    out = []
    rel = img.relocations
    for where, addend in rel.items():
        if addend != sbase:
            continue
        if rel.get(where + 8) != mbase:
            continue
        st = rel.get(where + 16)
        if st is None or not img.executable(st):
            continue
        out.append({'qmetaobject': where - 8, 'static_metacall': st})
    return out


def recover_jump_table(img: Image, st: int, method_count: int) -> dict:
    ins = img.disasm(st, 0x700, 260)
    candidates = []
    for pos, x in enumerate(ins):
        if x.mnemonic != 'lea' or len(x.operands) < 2:
            continue
        op = x.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        reg = x.operands[0].reg
        table = x.address + x.size + op.mem.disp
        used = any(
            any(yop.type == X86_OP_MEM and yop.mem.base == reg and yop.mem.scale == 4 for yop in y.operands)
            for y in ins[pos + 1:pos + 12]
        )
        if not used:
            continue
        try:
            targets = [table + img.i32(table + i * 4) for i in range(method_count)]
        except (ValueError, struct.error):
            continue
        score = sum(img.executable(t) for t in targets)
        candidates.append((score, table, targets))
    candidates.sort(reverse=True)
    if not candidates or candidates[0][0] != method_count:
        raise RuntimeError('complete Qt jump table not found')
    score, table, targets = candidates[0]
    return {'table': table, 'targets': targets, 'score': score}


def immediate_edges(img: Image, start: int, size: int = 0x280) -> list[dict]:
    out = []
    for ins in img.disasm(start, size, 120):
        if ins.mnemonic.startswith('ret'):
            break
        if ins.mnemonic not in {'call', 'jmp'} or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type == X86_OP_IMM:
            target = int(op.imm)
            if img.executable(target):
                out.append({'at': ins.address, 'kind': ins.mnemonic, 'target': target})
        if ins.mnemonic == 'jmp':
            break
    return out


def function_control_transfers(img: Image, start: int, limit: int = 1200) -> dict:
    bounds = img.containing_fde(start)
    if bounds is None:
        raise RuntimeError(f'no unique FDE for 0x{start:x}')
    lo, hi = bounds
    rows = []
    for ins in list(img.md.disasm(img.bytes(lo, hi - lo), lo))[:limit]:
        if ins.mnemonic not in {'call', 'jmp'} or not ins.operands:
            continue
        op = ins.operands[0]
        row = {'at': ins.address, 'kind': ins.mnemonic, 'operand': ins.op_str}
        if op.type == X86_OP_IMM:
            row['mode'] = 'direct'
            row['target'] = int(op.imm)
        elif op.type == X86_OP_MEM:
            row['mode'] = 'indirect_mem'
            row['base'] = img.md.reg_name(op.mem.base) if op.mem.base else ''
            row['index'] = img.md.reg_name(op.mem.index) if op.mem.index else ''
            row['scale'] = int(op.mem.scale)
            row['disp'] = int(op.mem.disp)
        else:
            row['mode'] = 'indirect_reg'
            row['reg'] = img.md.reg_name(op.reg)
        rows.append(row)
    return {'fde': (lo, hi), 'transfers': rows}

def locate_class(img: Image, class_name: str, required_methods: list[str]) -> dict:
    s_candidates = find_stringdata(img, class_name)
    matches = []
    for sbase in s_candidates:
        for mbase, meta in find_metadata(img, sbase, required_methods):
            qmos = find_qmeta_static_metacall(img, sbase, mbase)
            for qmo in qmos:
                try:
                    jt = recover_jump_table(img, qmo['static_metacall'], meta['method_count'])
                except RuntimeError:
                    continue
                rows = []
                for row in meta['rows']:
                    rows.append({**row, 'target': jt['targets'][row['index']]})
                matches.append({
                    'class': class_name,
                    'stringdata': sbase,
                    'metadata': mbase,
                    'qmetaobject': qmo['qmetaobject'],
                    'static_metacall': qmo['static_metacall'],
                    'jump_table': jt['table'],
                    'method_count': meta['method_count'],
                    'signal_count': meta['signal_count'],
                    'methods': rows,
                })
    if len(matches) != 1:
        raise RuntimeError(f'{class_name}: expected one complete Qt meta match, got {len(matches)}')
    return matches[0]


def dynamic_symbols(path: Path, patterns: tuple[str, ...]) -> list[str]:
    out = []
    with path.open('rb') as fh:
        elf = ELFFile(fh)
        dyn = elf.get_section_by_name('.dynsym')
        if dyn is None:
            return out
        for sym in dyn.iter_symbols():
            name = sym.name
            low = name.lower()
            if any(p.lower() in low for p in patterns):
                out.append(name)
    return sorted(set(out))


def hx(v: int) -> str:
    return f'0x{v:x}'


def sanitize_transfer(row: dict) -> dict:
    out = dict(row)
    out['at'] = hx(int(out['at']))
    if 'target' in out:
        out['target'] = hx(int(out['target']))
    if 'disp' in out:
        out['disp_hex'] = hex(int(out['disp']))
    return out


def sanitize_class(c: dict, method_filter: re.Pattern[str] | None = None) -> dict:
    methods = c['methods']
    if method_filter:
        methods = [m for m in methods if method_filter.search(m['name'])]
    return {
        'class': c['class'],
        'stringdata': hx(c['stringdata']),
        'metadata': hx(c['metadata']),
        'qmetaobject': hx(c['qmetaobject']),
        'static_metacall': hx(c['static_metacall']),
        'jump_table': hx(c['jump_table']),
        'method_count': c['method_count'],
        'signal_count': c['signal_count'],
        'methods': [
            {
                'index': m['index'],
                'name': m['name'],
                'argc': m['argc'],
                'target': hx(m['target']),
                'edges': [{**e, 'at': hx(e['at']), 'target': hx(e['target'])} for e in immediate_edges(GLOBAL_IMAGE, m['target'])],
            }
            for m in methods
        ],
    }


GLOBAL_IMAGE: Image


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--version', required=True)
    ap.add_argument('--packed-sha256', required=True)
    ap.add_argument('--unpacked-sha256', required=True)
    ap.add_argument('--unpacked-size', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    global GLOBAL_IMAGE
    GLOBAL_IMAGE = Image(args.client)

    queue = locate_class(GLOBAL_IMAGE, 'tibia::protocol::TProtocolMessageQueue', ['sendLogin'])
    tcp_classes = []
    for class_name in ('tibia::network::TGameserverTCPConnection', 'tibia::network::TTCPConnection'):
        try:
            tcp_classes.append(locate_class(GLOBAL_IMAGE, class_name, []))
        except RuntimeError as exc:
            tcp_classes.append({'class': class_name, 'error': str(exc)})

    send = [m for m in queue['methods'] if m['name'] == 'sendLogin']
    if len(send) != 1:
        raise RuntimeError(f'expected one sendLogin method, got {len(send)}')
    send = send[0]
    send_edges = immediate_edges(GLOBAL_IMAGE, send['target'])
    if len(send_edges) != 1 or send_edges[0]['kind'] != 'jmp':
        raise RuntimeError(f'expected one terminal sendLogin case jump, got {send_edges!r}')
    send_login_adapter = int(send_edges[0]['target'])
    adapter_flow = function_control_transfers(GLOBAL_IMAGE, send_login_adapter)
    adapter_indirect_calls = [
        row for row in adapter_flow['transfers']
        if row['kind'] == 'call' and row['mode'].startswith('indirect_')
    ]
    adapter_virtual_disps = sorted({
        int(row['disp']) for row in adapter_indirect_calls
        if row['mode'] == 'indirect_mem' and int(row.get('disp', 0)) >= 0
    })

    selected = re.compile(r'(login|write|send|data|message|connect|socket|packet)', re.I)
    result = {
        'schema': 'otclient.track-a.current-game-login-wire-writer.discovery.v1',
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
        'queue': sanitize_class(queue, selected),
        'send_login': {
            'index': send['index'],
            'target': hx(send['target']),
            'edges': [{**e, 'at': hx(e['at']), 'target': hx(e['target'])} for e in send_edges],
        },
        'send_login_adapter': {
            'address': hx(send_login_adapter),
            'adapter_fde': [hx(adapter_flow['fde'][0]), hx(adapter_flow['fde'][1])],
            'control_transfers': [sanitize_transfer(row) for row in adapter_flow['transfers']],
            'adapter_indirect_calls': [sanitize_transfer(row) for row in adapter_indirect_calls],
            'indirect_memory_displacements': [hex(value) for value in adapter_virtual_disps],
        },
        'tcp_metaobjects': [sanitize_class(c, selected) if 'error' not in c else c for c in tcp_classes],
        'dynamic_symbols': dynamic_symbols(args.client, ('QDataStream', 'QTcpSocket', 'QIODevice', 'writeRawData'))[:300],
        'classification': {
            'current_sendlogin_qmeta': 'PROVEN',
            'current_sendlogin_first_direct_edges': 'PROVEN',
            'current_sendlogin_adapter_fde': 'PROVEN',
            'current_sendlogin_adapter_indirect_calls': 'PROVEN',
            'current_tcp_metaobjects': 'DISCOVERY_ONLY',
            'final_writer_contract': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_WIRE_PROBE=PASS')
    print('CURRENT_CLIENT_VERSION=' + args.version)
    print('CURRENT_CLIENT_UNPACKED_SHA256=' + args.unpacked_sha256)
    print('QUEUE_STRINGDATA=' + hx(queue['stringdata']))
    print('QUEUE_METADATA=' + hx(queue['metadata']))
    print('QUEUE_STATIC_METACALL=' + hx(queue['static_metacall']))
    print('SENDLOGIN_INDEX=' + str(send['index']))
    print('SENDLOGIN_TARGET=' + hx(send['target']))
    print('SENDLOGIN_DIRECT_EDGE_COUNT=' + str(len(send_edges)))
    for i, edge in enumerate(send_edges[:12]):
        print(f'SENDLOGIN_EDGE_{i}={edge["kind"]}@{hx(edge["at"])}->{hx(edge["target"])}')
    print('SENDLOGIN_ADAPTER=' + hx(send_login_adapter))
    print('SENDLOGIN_ADAPTER_FDE=' + hx(adapter_flow['fde'][0]) + '..' + hx(adapter_flow['fde'][1]))
    print('SENDLOGIN_ADAPTER_INDIRECT_CALL_COUNT=' + str(len(adapter_indirect_calls)))
    print('SENDLOGIN_ADAPTER_INDIRECT_MEMORY_DISPS=' + ','.join(hex(value) for value in adapter_virtual_disps))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
