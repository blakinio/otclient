#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from capstone.x86_const import X86_OP_IMM

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


def qmeta_subset(img: core.Image) -> dict:
    names = (
        'requestCharacterLogin',
        'requestCharacterGameserverLogin',
        'onStartGameServerLoginStateEntered',
        'connectClientToGameserverWithExistingCredentials',
        'loginSuccessful',
    )
    return {name: core.meta_for_method(img, name) for name in names}


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
    producer = next(
        int(row['target'], 16) for row in handler['slots']
        if row['offset'] == '0x60')
    producer_fde = img.fde(producer)
    if not producer_fde:
        raise SystemExit('LOGIN_PRODUCER_FDE_UNKNOWN')

    scan = deep.scan_executable(
        img, auth_targets, int(auth['address_point'], 16),
        int(handler['address_point'], 16))
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
    callers = owner.direct_callers(img, population)
    if len(callers) != 1:
        raise SystemExit(f'AUTHINFO_POPULATION_CALLER_AMBIGUOUS={len(callers)}')
    caller_site = callers[0]
    caller_fde = img.fde(caller_site)
    if not caller_fde:
        raise SystemExit('AUTHINFO_POPULATION_CALLER_FDE_UNKNOWN')

    caller_parents = owner.direct_callers(img, caller_fde[0])
    caller_owners = owner.vtable_owners_for_target(img, caller_fde[0])
    population_snapshot = deep.snapshot_fde(img, population_fde)
    caller_snapshot = deep.snapshot_fde(img, caller_fde)

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
            'snapshot': population_snapshot,
            'direct_calls': calls_in_fde(img, population_fde),
        },
        'population_caller': {
            'call_site': hx(caller_site),
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
        'qmeta': qmeta_subset(img),
        'type_and_method_neighborhoods': {
            term: owner.string_neighborhood(img, term, radius=0x2200)
            for term in terms
        },
        'classification': {
            'population_function': 'PROVEN_STRUCTURALLY',
            'population_caller': 'PROVEN_STRUCTURALLY',
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
