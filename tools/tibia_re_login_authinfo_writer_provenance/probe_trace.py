#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

import probe_deep as deep
import probe_owner as owner
import probe_qmeta as core


def hx(value: int) -> str:
    return f'0x{value:x}'


def fde_key(img: core.Image, va: int) -> str | None:
    row = img.fde(va)
    return '..'.join(hx(v) for v in row) if row else None


def calls_in_fde(img: core.Image, fde: tuple[int, int]) -> list[dict]:
    rows: list[dict] = []
    for ins in img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]):
        if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            target = int(ins.operands[0].imm)
            rows.append({'site': hx(ins.address), 'target': hx(target), 'target_fde': fde_key(img, target)})
    return rows


def argument_slice(img: core.Image, site: int, before: int = 80) -> list[dict]:
    fde = img.fde(site)
    if not fde:
        return []
    ins = list(img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]))
    indexes = [i for i, row in enumerate(ins) if row.address == site]
    if len(indexes) != 1:
        return []
    start = max(0, indexes[0] - before)
    interesting = re.compile(r'\b(rdi|rsi|rdx|rcx|r8|r9|edi|esi|edx|ecx|r8d|r9d)\b')
    rows = []
    for row in ins[start:indexes[0] + 1]:
        if interesting.search(row.op_str) or row.mnemonic in ('call', 'lea'):
            rows.append({'at': hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str})
    return rows


def devirtualized_guard(img: core.Image, fde: tuple[int, int]) -> dict:
    expected_targets = []
    virtual_slots = []
    for ins in img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]):
        if ins.mnemonic == 'lea' and len(ins.operands) >= 2:
            op = ins.operands[1]
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                expected_targets.append(ins.address + ins.size + int(op.mem.disp))
        if ins.mnemonic == 'mov' and len(ins.operands) >= 2:
            op = ins.operands[1]
            if op.type == X86_OP_MEM and op.mem.disp >= 0x100:
                virtual_slots.append(int(op.mem.disp))
    expected = expected_targets[0] if expected_targets else None
    slot = virtual_slots[0] if virtual_slots else None
    return {'expected_target': hx(expected) if expected is not None else None,
            'virtual_slot': hex(slot) if slot is not None else None}


def decode_qmeta_params(img: core.Image, meta: dict, row: dict) -> dict:
    sbase = int(meta['stringdata'], 16)
    mbase = int(meta['metadata'], 16)
    argc = int(row['argc'])
    offset = int(row['param_offset'])
    raw = [img.u32(mbase + 4 * (offset + i)) for i in range(1 + 2 * argc)]
    def decode_type(value: int):
        if value & 0x80000000:
            idx = value & 0x7fffffff
            try:
                return {'raw': hex(value), 'custom_type': core.qstring(img, sbase, idx)}
            except Exception:
                return {'raw': hex(value), 'custom_type': None}
        return {'raw': hex(value), 'builtin_type_id': value}
    return {
        'return_type': decode_type(raw[0]) if raw else None,
        'argument_types': [decode_type(v) for v in raw[1:1 + argc]],
        'argument_name_indexes': raw[1 + argc:1 + 2 * argc],
    }


def valid_qmeta_records(img: core.Image, method: str) -> list[dict]:
    rows = []
    for meta in core.meta_for_method(img, method):
        if not meta.get('static'):
            continue
        selected = [row for row in meta['rows'] if row['name'] == method]
        for row in selected:
            rows.append({
                'class_name': meta['class_name'],
                'stringdata': meta['stringdata'],
                'metadata': meta['metadata'],
                'static': meta['static'],
                'method': row,
                'params': decode_qmeta_params(img, meta, row),
            })
    return rows


def qmeta_subset(img: core.Image) -> dict:
    names = (
        'requestCharacterLogin',
        'requestCharacterGameserverLogin',
        'onStartGameServerLoginStateEntered',
        'connectClientToGameserverWithExistingCredentials',
        'loginSuccessful',
        'receivedLoginChallengeMessage',
    )
    return {name: valid_qmeta_records(img, name) for name in names}


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
    game_client = core.exact_vtable(
        img, 'TGameClient', 'tibia::client::TGameClient')
    game_session = core.exact_vtable(
        img, 'TGameserverGameSession', 'tibia::game::TGameserverGameSession')
    auth_targets = {
        row['offset']: int(row['target'], 16)
        for row in auth['slots'] if row['executable']
    }
    producer = next(
        int(row['target'], 16) for row in handler['slots']
        if row['offset'] == '0x60')
    producer_fde = img.fde(producer)
    if not producer_fde:
        raise SystemExit('LOGIN_PRODUCER_FDE_UNKNOWN')

    scan = deep.scan_executable(
        img, auth_targets, int(auth['address_point'], 16),
        int(handler['address_point'], 16),
        extra_vtables={'gameserver_session': int(game_session['address_point'], 16)})
    candidates = deep.candidate_population_fdes(
        img, scan['slot_rip_refs'], producer_fde)

    if not candidates:
        raise SystemExit('AUTHINFO_POPULATION_CANDIDATE_MISSING')
    top_score = (
        candidates[0]['distinct_auth_slot_count'],
        candidates[0]['ref_count'],
    )
    top = [
        row for row in candidates
        if (row['distinct_auth_slot_count'], row['ref_count']) == top_score
    ]
    if len(top) != 1 or top_score[0] < 5:
        raise SystemExit(f'AUTHINFO_POPULATION_AMBIGUOUS={len(top)}:{top_score!r}')

    population_fde = tuple(top[0]['fde_tuple'])
    population = population_fde[0]
    callers = sorted(site for site, target in scan['direct_calls'] if target == population)
    if len(callers) != 1:
        raise SystemExit(f'AUTHINFO_POPULATION_CALLER_AMBIGUOUS={len(callers)}')
    caller_site = callers[0]
    caller_fde = img.fde(caller_site)
    if not caller_fde:
        raise SystemExit('AUTHINFO_POPULATION_CALLER_FDE_UNKNOWN')

    guard = devirtualized_guard(img, caller_fde)
    guard_target = int(guard['expected_target'], 16) if guard['expected_target'] else None
    guard_slot = int(guard['virtual_slot'], 16) if guard['virtual_slot'] else None
    if guard_target is None or guard_slot is None:
        raise SystemExit('CALLER_DEVIRTUALIZATION_GUARD_UNKNOWN')
    game_client_ap = int(game_client['address_point'], 16)
    game_client_slot_target = img.qword(game_client_ap + guard_slot)
    devirtualized_owner_candidates = owner.vtable_owners_for_target(img, guard_target, max_slot=0x800)
    caller_object_tgameclient_slot_match = game_client_slot_target == guard_target

    caller_parents = sorted(site for site, target in scan['direct_calls'] if target == caller_fde[0])
    caller_owners = owner.vtable_owners_for_target(img, caller_fde[0])
    population_snapshot = deep.snapshot_fde(img, population_fde)
    caller_snapshot = deep.snapshot_fde(img, caller_fde)

    auth_slot_ref_fdes = {}
    for slot, sites in scan['slot_rip_refs'].items():
        grouped = {}
        for site in sites:
            fde = img.fde(site)
            key = '..'.join(hx(v) for v in fde) if fde else 'UNKNOWN'
            grouped.setdefault(key, []).append(hx(site))
        auth_slot_ref_fdes[slot] = grouped
    gameserver_session_vtable_refs = [
        {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 18, 18)}
        for site in scan['extra_vtable_refs']['gameserver_session'][:160]
    ]

    terms = (
        'TPlaySessionData',
        'TCharacterLoginData',
        'SessionKey',
        'sessionkey',
        'requestCharacterGameserverLogin',
        'connectClientToGameserverWithExistingCredentials',
    )
    result = {
        'schema': 'otclient.track-a.current-game-login-authinfo-writer-provenance.trace.v1',
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'authentication_info': {
            'rtti': auth['rtti'],
            'address_point': auth['address_point'],
        },
        'login_producer': {
            'target': hx(producer),
            'fde': [hx(v) for v in producer_fde],
        },
        'population': {
            'derived_candidate_score': list(top_score),
            'fde': [hx(v) for v in population_fde],
            'auth_slot_sites': top[0]['slot_sites'],
            'auth_slot_contexts': {
                slot: [
                    {'site': site, 'context': core.context(img, int(site, 16), 14, 14)}
                    for site in sites
                ]
                for slot, sites in top[0]['slot_sites'].items()
            },
            'snapshot': population_snapshot,
            'direct_calls': calls_in_fde(img, population_fde),
        },
        'population_caller': {
            'call_site': hx(caller_site),
            'devirtualization_guard': guard,
            'tgameclient': {
                'rtti': game_client['rtti'],
                'address_point': game_client['address_point'],
                'guard_slot_target': hx(game_client_slot_target),
                'caller_object_tgameclient_slot_match': caller_object_tgameclient_slot_match,
            },
            'devirtualized_owner_candidates': devirtualized_owner_candidates,
            'fde': [hx(v) for v in caller_fde],
            'snapshot': caller_snapshot,
            'argument_slice': argument_slice(img, caller_site),
            'direct_parent_callers': [
                {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 20, 20)}
                for site in caller_parents[:120]
            ],
            'vtable_owners': caller_owners,
            'relocation_owners': owner.reloc_owners_for_fde(
                img, caller_fde[0], caller_fde[1]),
        },
        'gameserver_session': {
            'rtti': game_session['rtti'],
            'address_point': game_session['address_point'],
            'gameserver_session_vtable_refs': gameserver_session_vtable_refs,
        },
        'auth_slot_ref_fdes': auth_slot_ref_fdes,
        'qmeta': qmeta_subset(img),
        'type_and_method_neighborhoods': {
            term: owner.string_neighborhood(img, term, radius=0x2200)
            for term in terms
        },
        'classification': {
            'population_function': 'PROVEN_STRUCTURALLY',
            'population_caller': 'PROVEN_STRUCTURALLY',
            'caller_object_tgameclient_slot_match': caller_object_tgameclient_slot_match,
            'source_semantics': 'DISCOVERY_ONLY',
            'password_session_to_rsa_field_mapping': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_AUTHINFO_WRITER_TRACE=PASS')
    print('AUTHINFO_POPULATION_FDE=' + '..'.join(hx(v) for v in population_fde))
    print('AUTHINFO_POPULATION_CALLER=' + hx(caller_site))
    print('AUTHINFO_POPULATION_CALLER_FDE=' + '..'.join(hx(v) for v in caller_fde))
    print('AUTHINFO_POPULATION_CALLER_OWNER_COUNT=' + str(len(caller_owners)))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
