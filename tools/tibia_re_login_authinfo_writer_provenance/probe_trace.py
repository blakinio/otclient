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


def recover_qmeta_jump_table(img: core.Image, static_metacall: int, method_count: int) -> dict:
    ins = list(img.md.disasm(img.bytes(static_metacall, 0x800), static_metacall))[:320]
    candidates = []
    for pos, row in enumerate(ins):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        op = row.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        reg = row.operands[0].reg
        table = row.address + row.size + int(op.mem.disp)
        used = any(
            any(xop.type == X86_OP_MEM and xop.mem.base == reg and xop.mem.scale == 4 for xop in x.operands)
            for x in ins[pos + 1:pos + 12]
        )
        if not used:
            continue
        try:
            targets = [table + img.i32(table + 4 * i) for i in range(method_count)]
        except Exception:
            continue
        if all(img.executable(target) for target in targets):
            bounded = False
            for prev in ins[max(0, pos - 8):pos]:
                if prev.mnemonic != 'cmp' or len(prev.operands) < 2:
                    continue
                left, right = prev.operands[0], prev.operands[1]
                if left.type != 1 or right.type != X86_OP_IMM:
                    continue
                if img.md.reg_name(left.reg) == 'edx' and int(right.imm) == method_count - 1:
                    bounded = True
            candidates.append((bounded, table, targets))
    uniq = {(table, tuple(targets)) for bounded, table, targets in candidates if bounded}
    if len(uniq) != 1:
        raise RuntimeError(f'QMETA_BOUNDED_JUMP_TABLE_AMBIGUOUS:{len(uniq)}:all={len(candidates)}')
    table, targets = next(iter(uniq))
    return {'table': hx(table), 'targets': [hx(target) for target in targets]}


def exact_qmeta_class(img: core.Image, class_name: str, required_methods: tuple[str, ...]) -> dict:
    candidates = []
    for sbase in core.stringdata_bases_for_literal(img, class_name):
        for mbase in range(max(0, sbase - 0x20000) & ~3, sbase + 0x20000, 4):
            meta = core.parse_meta(img, sbase, mbase)
            if not meta or meta['class_name'] != class_name:
                continue
            names = {row['name'] for row in meta['rows']}
            if not set(required_methods).issubset(names):
                continue
            static = []
            for where, value in img.rel.items():
                if value != sbase or img.rel.get(where + 8) != mbase:
                    continue
                target = img.rel.get(where + 16)
                if target is not None and img.executable(target):
                    static.append({'qmetaobject': hx(where - 8), 'static_metacall': hx(target)})
            if len(static) != 1:
                continue
            jump = recover_qmeta_jump_table(img, int(static[0]['static_metacall'], 16), meta['method_count'])
            methods = []
            for row in meta['rows']:
                if row['name'] not in required_methods:
                    continue
                target = int(jump['targets'][row['index']], 16)
                wrapped = {'stringdata': hx(sbase), 'metadata': hx(mbase), **meta}
                methods.append({
                    'name': row['name'], 'index': row['index'], 'argc': row['argc'],
                    'flags': row['flags'], 'target': hx(target),
                    'params': decode_qmeta_params(img, wrapped, row),
                    'target_fde': fde_key(img, target),
                    'target_edges': calls_in_fde(img, img.fde(target)) if img.fde(target) else [],
                    'target_context': core.context(img, target, 8, 18),
                })
            candidates.append({
                'class_name': class_name, 'stringdata': hx(sbase), 'metadata': hx(mbase),
                'method_count': meta['method_count'], 'signal_count': meta['signal_count'],
                'static': static[0], 'jump_table': jump['table'], 'methods': methods,
            })
    uniq = {(row['stringdata'], row['metadata']): row for row in candidates}
    if len(uniq) != 1:
        raise RuntimeError(f'QMETA_CLASS_AMBIGUOUS:{class_name}:{len(uniq)}')
    return next(iter(uniq.values()))


def raw_rip_refs(img: core.Image, targets_by_name: dict[str, set[int]]) -> dict[str, list[int]]:
    by_target = {}
    for name, targets in targets_by_name.items():
        for target in targets:
            by_target.setdefault(target, set()).add(name)
    out = {name: [] for name in targets_by_name}
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        for pos in range(0, max(0, len(blob) - 7)):
            if not (0x40 <= blob[pos] <= 0x4f):
                continue
            if blob[pos + 1] not in (0x8d, 0x8b) or (blob[pos + 2] & 0xc7) != 0x05:
                continue
            disp = int.from_bytes(blob[pos + 3:pos + 7], 'little', signed=True)
            site = section.va + pos
            target = (site + 7 + disp) & 0xffffffffffffffff
            for name in by_target.get(target, ()):
                out[name].append(site)
    return out


def schema_storage_target(img: core.Image, literal_site: int, literal_targets: set[int]) -> int | None:
    fde = img.fde(literal_site)
    if not fde:
        return None
    instructions = list(img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]))
    indexes = [i for i, row in enumerate(instructions) if row.address == literal_site]
    if len(indexes) != 1:
        return None
    for row in reversed(instructions[max(0, indexes[0] - 5):indexes[0]]):
        if row.mnemonic != 'lea' or len(row.operands) < 2:
            continue
        op = row.operands[1]
        if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
            continue
        target = row.address + row.size + int(op.mem.disp)
        in_section = any(section.va <= target < section.va + section.size for section in img.sections)
        if target not in literal_targets and in_section:
            return target
    return None


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


def rtti_candidates_matching(img: core.Image, term: str) -> list[dict]:
    reverse = collections.defaultdict(list)
    for where, value in img.rel.items():
        reverse[value].append(where)
    rows = []
    for rtti in sorted(reverse):
        name_va = img.rel.get(rtti + 8)
        name = core.safe_cstr(img, name_va, 512) if name_va is not None else None
        if not name or term.lower() not in name.lower():
            continue
        aps = []
        for type_slot in reverse.get(rtti, []):
            ap = type_slot + 8
            if not img.mapped(ap - 16, 24):
                continue
            slots = []
            for off in range(0, 0x180, 8):
                target = img.qword(ap + off)
                if img.executable(target):
                    slots.append({'offset': hex(off), 'target': hx(target), 'fde': fde_key(img, target)})
            if slots:
                aps.append({'address_point': hx(ap), 'offset_to_top': hx(img.u64(ap - 16)), 'slots': slots})
        if aps:
            rows.append({'rtti': hx(rtti), 'rtti_name': name, 'address_points': aps})
    return rows

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
    rsa_rtti_candidates = rtti_candidates_matching(img, 'rsa')
    rsa_vtables = {}
    for row_index, row in enumerate(rsa_rtti_candidates):
        for ap_index, ap in enumerate(row['address_points']):
            rsa_vtables[f'rsa_{row_index}_{ap_index}'] = int(ap['address_point'], 16)
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

    def exact_cstring_occ(text: str) -> set[int]:
        out = set()
        raw_text = text.encode('utf-8')
        for va in img.occ(text):
            off = img.va_to_off(va)
            before_ok = off == 0 or img.raw[off - 1] == 0
            after = off + len(raw_text)
            after_ok = after < len(img.raw) and img.raw[after] == 0
            if before_ok and after_ok:
                out.add(va)
        return out

    literal_targets = {
        'sessionkey': exact_cstring_occ('sessionkey'),
        'characters': exact_cstring_occ('characters'),
        'worldid': exact_cstring_occ('worldid'),
        'ismaincharacter': exact_cstring_occ('ismaincharacter'),
        'CharName': exact_cstring_occ('CharName'),
    }
    if len(literal_targets['sessionkey']) != 1:
        raise SystemExit(f'SESSIONKEY_LITERAL_AMBIGUOUS={len(literal_targets["sessionkey"])}')

    print('TRACE_PHASE=ELF_SCAN_BEGIN', flush=True)
    generated_login_vtables = {
        'gameclient_message_login': 0x2f9ee90,
        'login_rsa_encrypted_block': 0x2f9ee50,
    }
    login_envelope_aps = (0x2f99320, 0x2f992e0)
    login_envelope_vtables = []
    for ap_value in login_envelope_aps:
        rtti = img.qword(ap_value - 8)
        name_va = img.qword(rtti + 8) if rtti else 0
        name = core.safe_cstr(img, name_va, 512) if name_va else None
        slots = []
        for off in range(0, 0x90, 8):
            target = img.qword(ap_value + off)
            slots.append({
                'offset': hex(off), 'target': hx(target),
                'executable': img.executable(target), 'fde': fde_key(img, target),
            })
        login_envelope_vtables.append({
            'address_point': hx(ap_value), 'rtti': hx(rtti), 'rtti_name': name, 'slots': slots,
        })
    scan = deep.scan_executable(
        img, auth_targets, int(auth['address_point'], 16),
        int(handler['address_point'], 16),
        extra_vtables={
            'gameserver_session': int(game_session['address_point'], 16),
            **rsa_vtables, **generated_login_vtables,
        },
        extra_literal_targets=literal_targets)
    print('TRACE_PHASE=ELF_SCAN_DONE', flush=True)
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
    gameserver_fdes = sorted({img.fde(site) for site in scan['extra_vtable_refs']['gameserver_session'] if img.fde(site)})
    gameserver_setup_fde = max(gameserver_fdes, key=lambda row: row[1] - row[0]) if gameserver_fdes else None
    gameserver_setup_snapshot = deep.snapshot_fde(img, gameserver_setup_fde) if gameserver_setup_fde else None

    def literal_ref_rows(name: str) -> list[dict]:
        return [
            {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 14, 20)}
            for site in scan['extra_literal_refs'].get(name, [])[:200]
        ]

    sessionkey_literal_refs = literal_ref_rows('sessionkey')
    all_literal_targets = set().union(*literal_targets.values()) if literal_targets else set()
    schema_storage_targets = {}
    for name, sites in scan['extra_literal_refs'].items():
        targets = {
            target for site in sites
            if (target := schema_storage_target(img, site, all_literal_targets)) is not None
        }
        schema_storage_targets[name] = targets
    storage_refs = raw_rip_refs(img, schema_storage_targets)
    initializer_fdes = {
        img.fde(site) for sites in scan['extra_literal_refs'].values() for site in sites if img.fde(site)
    }
    schema_storage_runtime_refs = {
        name: [
            {
                'site': hx(site), 'fde': fde_key(img, site),
                'initializer_fde': img.fde(site) in initializer_fdes,
                'context': core.context(img, site, 14, 24),
            }
            for site in sites[:300]
        ]
        for name, sites in storage_refs.items()
    }
    character_keys = ('characters', 'worldid', 'ismaincharacter')
    character_ref_fdes = collections.defaultdict(set)
    for key in character_keys:
        for site in scan['extra_literal_refs'].get(key, []):
            fde = img.fde(site)
            if fde:
                character_ref_fdes[fde].add(key)
    character_parser_literal_refs = [
        {
            'fde': [hx(v) for v in fde],
            'matched_keys': sorted(keys),
            'snapshot': deep.snapshot_fde(img, fde),
        }
        for fde, keys in sorted(character_ref_fdes.items())
        if len(keys) >= 2
    ]

    print('TRACE_PHASE=QMETA_BEGIN', flush=True)
    queue_stringdata = 0x1CE67C0
    queue_metadata = 0x1CE35A0
    queue_meta = core.parse_meta(img, queue_stringdata, queue_metadata)
    if not queue_meta or queue_meta['class_name'] != 'tibia::protocol::TProtocolMessageQueue':
        raise SystemExit('CURRENT_QUEUE_QMETA_CONTRACT_MISMATCH')
    if queue_meta['method_count'] != 355 or queue_meta['signal_count'] != 192:
        raise SystemExit('CURRENT_QUEUE_QMETA_COUNTS_MISMATCH')
    queue_wrapped = {'stringdata': hx(queue_stringdata), 'metadata': hx(queue_metadata), **queue_meta}
    queue_methods = {}
    for wanted in ('receivedLoginChallengeMessage', 'sendLogin'):
        rows = [row for row in queue_meta['rows'] if row['name'] == wanted]
        if len(rows) != 1:
            raise SystemExit(f'CURRENT_QUEUE_METHOD_AMBIGUOUS:{wanted}:{len(rows)}')
        row = rows[0]
        queue_methods[wanted] = {'method': row, 'params': decode_qmeta_params(img, queue_wrapped, row)}
    challenge_types = queue_methods['receivedLoginChallengeMessage']['params']['argument_types']
    send_login_types = queue_methods['sendLogin']['params']['argument_types']
    if len(challenge_types) != 1 or not str(challenge_types[0].get('custom_type') or '').endswith('GameserverMessageLoginChallenge'):
        raise SystemExit('CURRENT_CHALLENGE_TYPE_MISMATCH')
    if len(send_login_types) != 1 or not str(send_login_types[0].get('custom_type') or '').endswith('GameclientMessageLogin'):
        raise SystemExit('CURRENT_SENDLOGIN_TYPE_MISMATCH')

    exact_qmeta_classes = {
        'TProtocolMessageQueue': {
            'class_name': queue_meta['class_name'], 'stringdata': hx(queue_stringdata),
            'metadata': hx(queue_metadata), 'method_count': queue_meta['method_count'],
            'signal_count': queue_meta['signal_count'], 'methods': queue_methods,
        },
        'TLoginRequestUploader': exact_qmeta_class(
            img, 'tibia::authentication::TLoginRequestUploader', ('loginSuccessful',)),
        'TCharacterSelectionController': exact_qmeta_class(
            img, 'tibia::gamewindow::TCharacterSelectionController',
            ('requestCharacterLogin', 'onCharacterSelectionConfirmed')),
        'TGameClient': exact_qmeta_class(
            img, 'tibia::client::TGameClient',
            ('connectClientToGameserverWithExistingCredentials', 'onConnectClientToGameserver')),
    }

    print('TRACE_PHASE=QMETA_DONE', flush=True)
    def selected_method(class_key: str, method_name: str) -> dict:
        rows = [row for row in exact_qmeta_classes[class_key]['methods'] if row['name'] == method_name]
        if len(rows) != 1:
            raise SystemExit(f'SEMANTIC_METHOD_AMBIGUOUS:{class_key}:{method_name}:{len(rows)}')
        return rows[0]

    def immediate_jumps(start: int) -> list[int]:
        return [
            int(ins.operands[0].imm)
            for ins in img.md.disasm(img.bytes(start, 0x80), start)
            if ins.mnemonic == 'jmp' and ins.operands and ins.operands[0].type == X86_OP_IMM
        ]

    runtime_fde_for_key = {}
    for name, rows in schema_storage_runtime_refs.items():
        fdes = {row['fde'] for row in rows if not row['initializer_fde'] and row['fde']}
        if fdes:
            runtime_fde_for_key[name] = sorted(fdes)

    login_success_target = int(selected_method('TLoginRequestUploader', 'loginSuccessful')['target'], 16)
    request_character_target = int(selected_method('TCharacterSelectionController', 'requestCharacterLogin')['target'], 16)
    connect_existing_target = int(selected_method('TGameClient', 'connectClientToGameserverWithExistingCredentials')['target'], 16)
    on_connect_target = int(selected_method('TGameClient', 'onConnectClientToGameserver')['target'], 16)
    connect_existing_jumps = immediate_jumps(connect_existing_target)
    on_connect_jumps = immediate_jumps(on_connect_target)
    if len(connect_existing_jumps) < 1 or len(on_connect_jumps) < 1:
        raise SystemExit('CURRENT_GAMECLIENT_BUSINESS_TARGET_MISSING')

    semantic_targets = {
        'loginSuccessful': login_success_target,
        'requestCharacterLogin': request_character_target,
        'connectClientToGameserverWithExistingCredentials_business': connect_existing_jumps[0],
        'onConnectClientToGameserver_business': on_connect_jumps[0],
    }
    for key, fdes in runtime_fde_for_key.items():
        if len(fdes) == 1:
            semantic_targets[f'{key}_runtime_parser'] = int(fdes[0].split('..', 1)[0], 16)

    semantic_edge_callers = {
        name: [
            {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 12, 18)}
            for site, target in scan['direct_calls'] if target == target_va
        ]
        for name, target_va in semantic_targets.items()
    }
    targeted_semantic_snapshots = {
        name: deep.snapshot_fde(img, fde)
        for name, target_va in semantic_targets.items()
        if (fde := img.fde(target_va)) is not None
    }

    rsa_vtable_refs = {
        name: [
            {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 14, 20)}
            for site in scan['extra_vtable_refs'].get(name, [])[:120]
        ]
        for name in rsa_vtables
    }
    rsa_slot_callers = []
    for row in rsa_rtti_candidates:
        for ap in row['address_points']:
            for slot in ap['slots']:
                target = int(slot['target'], 16)
                callers_for_slot = [site for site, called in scan['direct_calls'] if called == target]
                if callers_for_slot:
                    rsa_slot_callers.append({
                        'rtti_name': row['rtti_name'], 'address_point': ap['address_point'],
                        'slot': slot['offset'], 'target': slot['target'],
                        'callers': [{'site': hx(site), 'fde': fde_key(img, site),
                                     'context': core.context(img, site, 12, 18)} for site in callers_for_slot[:80]],
                    })
    rsa_chain_snapshots = {
        'send_login_adapter': deep.snapshot_fde(img, img.fde(0xbd3050)),
        'client_message_processor': deep.snapshot_fde(img, img.fde(0xc29350)),
    }
    login_adapter_helpers = (0x1a9d850, 0x1aed7f0, 0x1786380, 0x1a8fb40, 0x17b9d90)
    login_adapter_helper_snapshots = {
        hx(target): deep.snapshot_fde(img, img.fde(target))
        for target in login_adapter_helpers if img.fde(target)
    }
    generated_serializers = {
        'GameclientMessageLogin.InternalSerialize': 0x177a7e0,
        'LoginRSAEncryptedBlock.InternalSerialize': 0x1770200,
        'GameclientMessageLogin.ByteSizeLong': 0x17728a0,
        'LoginRSAEncryptedBlock.ByteSizeLong': 0x1772740,
    }
    generated_serializer_callers = {
        name: [
            {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 14, 20)}
            for site, called in scan['direct_calls'] if called == target
        ][:120]
        for name, target in generated_serializers.items()
    }
    login_envelope_serializer_snapshots = {}
    for envelope in login_envelope_vtables:
        slot10 = next((row for row in envelope['slots'] if row['offset'] == '0x10' and row['executable']), None)
        if slot10:
            target = int(slot10['target'], 16)
            fde = img.fde(target)
            if fde:
                login_envelope_serializer_snapshots[envelope['address_point']] = deep.snapshot_fde(img, fde)

    generated_serializer_vtable_refs = {
        name: [
            {'site': hx(site), 'fde': fde_key(img, site), 'context': core.context(img, site, 14, 20)}
            for site in scan['extra_vtable_refs'].get(name, [])[:120]
        ]
        for name in generated_login_vtables
    }

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
            'setup_snapshot': gameserver_setup_snapshot,
        },
        'sessionkey_literal_refs': sessionkey_literal_refs,
        'schema_storage_targets': {
            name: [hx(target) for target in sorted(targets)]
            for name, targets in schema_storage_targets.items()
        },
        'schema_storage_runtime_refs': schema_storage_runtime_refs,
        'character_parser_literal_refs': character_parser_literal_refs,
        'literal_refs': {name: literal_ref_rows(name) for name in literal_targets},
        'exact_qmeta_classes': exact_qmeta_classes,
        'semantic_targets': {name: hx(target) for name, target in semantic_targets.items()},
        'semantic_edge_callers': semantic_edge_callers,
        'targeted_semantic_snapshots': targeted_semantic_snapshots,
        'rsa_rtti_candidates': rsa_rtti_candidates,
        'rsa_vtable_refs': rsa_vtable_refs,
        'rsa_slot_callers': rsa_slot_callers,
        'rsa_chain_snapshots': rsa_chain_snapshots,
        'login_adapter_helper_snapshots': login_adapter_helper_snapshots,
        'generated_serializer_callers': generated_serializer_callers,
        'generated_serializer_vtable_refs': generated_serializer_vtable_refs,
        'login_envelope_vtables': login_envelope_vtables,
        'login_envelope_serializer_snapshots': login_envelope_serializer_snapshots,
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
    print('LOGIN_ENVELOPE_DISCRIMINATOR=PASS')
    print('LOGIN_SPECIFIC_TRANSFORM_DISCRIMINATOR=PASS')
    print('RSA_STATIC_DISCRIMINATOR=' + ('PASS' if rsa_rtti_candidates else 'NO_RTTI_CANDIDATE'))
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
    try:
        raise SystemExit(main())
    except Exception as exc:
        print('AUTHINFO_TRACE_EXCEPTION_TYPE=' + type(exc).__name__, flush=True)
        print('AUTHINFO_TRACE_EXCEPTION=' + str(exc).replace('\n', ' ')[:500], flush=True)
        raise SystemExit(2)
