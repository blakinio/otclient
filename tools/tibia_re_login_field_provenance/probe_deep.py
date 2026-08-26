#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

import probe_qmeta as core


def h(value: int) -> str:
    return f'0x{value:x}'


def fde_key(img: core.Image, va: int) -> str | None:
    f = img.fde(va)
    return f'{h(f[0])}..{h(f[1])}' if f else None


def snapshot_fde(img: core.Image, fde: tuple[int, int], limit: int = 5000) -> dict:
    lo, hi = fde
    rows = []
    for ins in list(img.md.disasm(img.bytes(lo, hi - lo), lo))[:limit]:
        rows.append({'at': h(ins.address), 'mnemonic': ins.mnemonic, 'operand': ins.op_str})
    return {'fde': [h(lo), h(hi)], 'instructions': rows}


def safe_ascii(img: core.Image, va: int) -> str | None:
    return core.safe_cstr(img, va, 240)


def scan_executable(img: core.Image, auth_targets: dict[str, int], auth_ap: int, handler_ap: int) -> dict:
    target_to_slot = {target: slot for slot, target in auth_targets.items()}
    slot_rip_refs: dict[str, list[int]] = {slot: [] for slot in auth_targets}
    vtable_refs = {'auth': [], 'handler': []}
    direct_calls: list[tuple[int, int]] = []
    rip_exec_refs: dict[int, list[int]] = collections.defaultdict(list)

    for sec in img.sections:
        if not (sec.flags & 4):
            continue
        blob = img.raw[sec.offset:sec.offset + sec.size]
        for ins in img.md.disasm(blob, sec.va):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
                direct_calls.append((ins.address, int(ins.operands[0].imm)))
            for op in ins.operands:
                if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                    continue
                target = ins.address + ins.size + int(op.mem.disp)
                slot = target_to_slot.get(target)
                if slot is not None:
                    slot_rip_refs[slot].append(ins.address)
                if target == auth_ap:
                    vtable_refs['auth'].append(ins.address)
                if target == handler_ap:
                    vtable_refs['handler'].append(ins.address)
                if img.executable(target):
                    rip_exec_refs[target].append(ins.address)
    return {
        'slot_rip_refs': slot_rip_refs,
        'vtable_refs': vtable_refs,
        'direct_calls': direct_calls,
        'rip_exec_refs': rip_exec_refs,
    }


def candidate_population_fdes(img: core.Image, slot_refs: dict[str, list[int]], producer_fde: tuple[int, int]) -> list[dict]:
    by_fde: dict[tuple[int, int], dict[str, list[int]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for slot, sites in slot_refs.items():
        for site in sites:
            f = img.fde(site)
            if f:
                by_fde[f][slot].append(site)
    rows = []
    for fde, slots in by_fde.items():
        if fde == producer_fde:
            continue
        distinct = sorted(slots)
        refs = sum(len(v) for v in slots.values())
        rows.append({
            'fde_tuple': fde,
            'fde': [h(fde[0]), h(fde[1])],
            'distinct_auth_slots': distinct,
            'distinct_auth_slot_count': len(distinct),
            'ref_count': refs,
            'slot_sites': {k: [h(x) for x in v] for k, v in sorted(slots.items())},
        })
    rows.sort(key=lambda x: (x['distinct_auth_slot_count'], x['ref_count']), reverse=True)
    return rows[:8]


def analyze_candidate(img: core.Image, row: dict, scan: dict) -> dict:
    fde = row.pop('fde_tuple')
    lo, hi = fde
    instructions = list(img.md.disasm(img.bytes(lo, hi - lo), lo))
    direct_targets: dict[int, list[int]] = collections.defaultdict(list)
    literals = []
    source_offsets: dict[str, set[str]] = collections.defaultdict(set)

    for ins in instructions:
        if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            direct_targets[int(ins.operands[0].imm)].append(ins.address)
        for reg in ('rdx', 'rsi', 'rcx', 'rbx', 'rdi'):
            for match in re.finditer(r'\[' + reg + r'(?: \+ (0x[0-9a-f]+))?\]', ins.op_str):
                source_offsets[reg].add(match.group(1) or '0x0')
        for op in ins.operands:
            if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                continue
            target = ins.address + ins.size + int(op.mem.disp)
            direct = safe_ascii(img, target)
            indirect = None
            if img.mapped(target, 8):
                q = img.qword(target)
                indirect = safe_ascii(img, q)
            if direct or indirect:
                literals.append({
                    'site': h(ins.address),
                    'target': h(target),
                    'direct_ascii': direct,
                    'qword_target_ascii': indirect,
                })

    callers = [site for site, target in scan['direct_calls'] if target == lo]
    data_relocs = [where for where, value in img.rel.items() if value == lo]
    rip_refs = scan['rip_exec_refs'].get(lo, [])

    call_summaries = []
    for target, sites in sorted(direct_targets.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:120]:
        call_summaries.append({
            'target': h(target),
            'sites': [h(x) for x in sites[:50]],
            'target_fde': fde_key(img, target),
            'target_snapshot': img.snapshot(target, 36) if img.executable(target) else None,
        })

    row.update({
        'snapshot': snapshot_fde(img, fde),
        'direct_callers': [
            {'site': h(x), 'fde': fde_key(img, x), 'context': core.context(img, x, 12, 12)}
            for x in callers[:120]
        ],
        'rip_code_refs_to_fde_start': [
            {'site': h(x), 'fde': fde_key(img, x), 'context': core.context(img, x, 10, 10)}
            for x in rip_refs[:120]
        ],
        'data_relocations_to_fde_start': [h(x) for x in data_relocs[:200]],
        'rip_ascii_literals': literals[:400],
        'memory_base_offsets': {k: sorted(v, key=lambda x: int(x, 16)) for k, v in source_offsets.items()},
        'direct_call_targets': call_summaries,
    })
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    img = core.Image(args.client)
    auth = core.exact_vtable(
        img, 'TAuthenticationAndEncryptionInfo',
        'tibia::authentication::TAuthenticationAndEncryptionInfo')
    handler = core.exact_vtable(
        img, 'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler')
    auth_targets = {
        row['offset']: int(row['target'], 16)
        for row in auth['slots'] if row['executable']
    }
    producer = next(int(row['target'], 16) for row in handler['slots'] if row['offset'] == '0x60')
    producer_fde = img.fde(producer)
    if not producer_fde:
        raise SystemExit('PRODUCER_FDE_UNKNOWN')

    scan = scan_executable(
        img, auth_targets, int(auth['address_point'], 16), int(handler['address_point'], 16))
    candidates = candidate_population_fdes(img, scan['slot_rip_refs'], producer_fde)
    analyzed = [analyze_candidate(img, dict(row), scan) for row in candidates]

    result = {
        'schema': 'otclient.track-a.current-game-login-field-provenance.deep.v1',
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'authentication_info': {
            'rtti': auth['rtti'],
            'address_point': auth['address_point'],
            'executable_slots': {k: h(v) for k, v in auth_targets.items()},
        },
        'login_handler': {
            'rtti': handler['rtti'],
            'address_point': handler['address_point'],
            'producer': h(producer),
            'producer_fde': [h(producer_fde[0]), h(producer_fde[1])],
        },
        'auth_slot_rip_refs': {k: [h(x) for x in v] for k, v in scan['slot_rip_refs'].items()},
        'population_fde_candidates': analyzed,
        'classification': {
            'source_object_type': 'UNKNOWN',
            'user_facing_semantic_field_names': 'UNKNOWN',
            'password_session_to_rsa_field_mapping': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_DEEP_FIELD_PROVENANCE=PASS')
    for idx, row in enumerate(analyzed):
        print(f'POPULATION_FDE_{idx}=' + '..'.join(row['fde']))
        print(f'POPULATION_FDE_{idx}_SLOT_COUNT={row["distinct_auth_slot_count"]}')
        print(f'POPULATION_FDE_{idx}_CALLERS={len(row["direct_callers"])}')
        print(f'POPULATION_FDE_{idx}_LITERALS={len(row["rip_ascii_literals"])}')
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
