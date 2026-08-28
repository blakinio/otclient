#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from capstone.x86_const import X86_OP_IMM

import probe as core
import qmeta_owner as qmeta

FOCUSED_TIMEOUT_RECOVERY = True
VIABLE_CALLSITE_0XCEDDCB = 0xCEDDCB
VIABLE_CALLER_FDE_0XCEDD90 = (0xCEDD90, 0xCEE0EC)
VIABLE_EDX_VALUE_1 = 1
FRESH_EXACT_REASSERTION = True
FOCUSED_QMETA_OWNER = True
FOCUSED_OWNER_CONSTRUCTOR_BINDING = True
NO_FULL_SCALAR_CENSUS = True
NO_HEURISTIC_RANKING = True
NO_SEMANTIC_GUESSING = True

EXPECTED_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE = 52_105_824
HANDLER_TYPE = 'tibia::authentication::TLoginProtocolMessageHandler'
HANDLER_VTABLE_AP = 0x30B6700
HANDLER_SLOT = 0x60
HANDLER_SLOT_TARGET = 0xE25620
MEMBER_OFFSET = 0x10

SAFETY = {
    'runtime_access': 'none',
    'official_client_executed': False,
    'login_performed': False,
    'secret_access': False,
    'process_memory_access': False,
    'packet_capture': False,
    'raw_client_uploaded': False,
}


def hx(value: int | None) -> str | None:
    return None if value is None else f'0x{value:x}'


def mangle_nested(type_name: str) -> str:
    return 'N' + ''.join(f'{len(part)}{part}' for part in type_name.split('::')) + 'E'


def focused_type_vtables(img: core.Image, type_name: str) -> list[int]:
    reverse: dict[int, list[int]] = defaultdict(list)
    for where, value in img.rel.items():
        reverse[value].append(where)
    rows: set[int] = set()
    needle = mangle_nested(type_name).encode('ascii')
    for name_va in img.occurrences(needle):
        for name_slot in reverse.get(name_va, []):
            rtti = name_slot - 8
            for type_slot in reverse.get(rtti, []):
                ap = type_slot + 8
                if not img.mapped(ap - 16, 24):
                    continue
                if img.u64(ap - 16) != 0:
                    continue
                first = img.qword(ap)
                if img.executable(first):
                    rows.add(ap)
    return sorted(rows)


def verify_fresh_exact(img: core.Image) -> dict:
    digest = hashlib.sha256(img.raw).hexdigest()
    if len(img.raw) != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise RuntimeError('exact current client fence mismatch')
    if img.qword(HANDLER_VTABLE_AP + HANDLER_SLOT) != HANDLER_SLOT_TARGET:
        raise RuntimeError('promoted handler slot target mismatch')
    handler_vtables = focused_type_vtables(img, HANDLER_TYPE)
    if HANDLER_VTABLE_AP not in handler_vtables:
        raise RuntimeError('handler RTTI/vtable identity mismatch')

    fde = img.fde(VIABLE_CALLSITE_0XCEDDCB)
    if fde != VIABLE_CALLER_FDE_0XCEDD90:
        raise RuntimeError(f'viable caller FDE moved: {fde}')
    instructions = img.instructions(fde)
    by = {row.address: row for row in instructions}
    required = {
        0xCEDD9F: ('mov', 'r12, rdi'),
        0xCEDDBB: ('mov', 'rdi, qword ptr [r12 + 0x10]'),
        0xCEDDC0: ('mov', 'edx, 1'),
        0xCEDDC8: ('mov', 'rax, qword ptr [rdi]'),
        0xCEDDCB: ('call', 'qword ptr [rax + 0x60]'),
    }
    reasserted = []
    for address, expected in required.items():
        row = by.get(address)
        if row is None or row.mnemonic != expected[0] or row.op_str != expected[1]:
            actual = None if row is None else (row.mnemonic, row.op_str)
            raise RuntimeError(f'viable callsite instruction mismatch {address:#x}: {actual}')
        reasserted.append({'at': hx(address), 'mnemonic': row.mnemonic, 'operand': row.op_str})

    return {
        'classification': 'FRESH_EXACT_REASSERTION',
        'client_sha256': digest,
        'client_size': len(img.raw),
        'handler_type': HANDLER_TYPE,
        'handler_vtable_address_point': hx(HANDLER_VTABLE_AP),
        'handler_slot': hx(HANDLER_SLOT),
        'handler_slot_target': hx(HANDLER_SLOT_TARGET),
        'viable_caller_fde': [hx(fde[0]), hx(fde[1])],
        'viable_callsite': hx(VIABLE_CALLSITE_0XCEDDCB),
        'viable_edx_value': VIABLE_EDX_VALUE_1,
        'instructions': reasserted,
    }


def direct_edges_into_fde(img: core.Image, target_fde: tuple[int, int]) -> list[dict]:
    raw_candidates: set[tuple[int, int, str]] = set()
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        for opcode, mnemonic in ((0xE8, 'call'), (0xE9, 'jmp')):
            start = 0
            needle = bytes((opcode,))
            while True:
                pos = blob.find(needle, start)
                if pos < 0:
                    break
                if pos + 5 <= len(blob):
                    site = section.va + pos
                    disp = int.from_bytes(blob[pos + 1:pos + 5], 'little', signed=True)
                    target = site + 5 + disp
                    if target_fde[0] <= target < target_fde[1]:
                        raw_candidates.add((site, target, mnemonic))
                start = pos + 1

    rows = []
    for site, target, mnemonic in sorted(raw_candidates):
        source_fde = img.fde(site)
        if source_fde is None or source_fde[1] - source_fde[0] > 0x10000:
            continue
        instruction = next((row for row in img.instructions(source_fde) if row.address == site), None)
        if instruction is None or instruction.mnemonic != mnemonic:
            continue
        if not instruction.operands or instruction.operands[0].type != X86_OP_IMM:
            continue
        if int(instruction.operands[0].imm) != target:
            continue
        rows.append({
            'site': site,
            'target': target,
            'source_fde': source_fde,
            'mnemonic': mnemonic,
        })
    return rows


def focused_meta_candidates(img: core.Image, source_fdes: set[tuple[int, int]]) -> list[dict]:
    rows = []
    seen = set()
    for where, sbase in img.rel.items():
        mbase = img.rel.get(where + 8)
        static_metacall = img.rel.get(where + 16)
        if mbase is None or static_metacall is None:
            continue
        if not img.executable(static_metacall) or img.fde(static_metacall) not in source_fdes:
            continue
        meta = qmeta.parse_meta_candidate(img, sbase, mbase)
        if meta is None:
            continue
        key = (sbase, mbase, static_metacall, meta['class_name'])
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            **meta,
            'static_metaobject': where,
            'stringdata': sbase,
            'metadata': mbase,
            'static_metacall': static_metacall,
        })
    return rows


def qmeta_method_links(img: core.Image, target_fde: tuple[int, int], direct_edges: list[dict]) -> list[dict]:
    source_fdes = {row['source_fde'] for row in direct_edges}
    links = []
    for meta in focused_meta_candidates(img, source_fdes):
        static_fde = img.fde(meta['static_metacall'])
        if static_fde is None:
            continue
        relevant_edges = [row for row in direct_edges if row['source_fde'] == static_fde]
        if not relevant_edges:
            continue
        try:
            jump_table, targets = qmeta.recover_jump_table(img, meta['static_metacall'], meta['method_count'])
        except RuntimeError:
            continue
        all_targets = set(targets)
        for method, case_target in zip(meta['methods'], targets):
            block = qmeta.case_block(img, static_fde, case_target, all_targets)
            sites = {row.address for row in block}
            hits = [edge for edge in relevant_edges if edge['site'] in sites]
            if not hits:
                continue
            links.append({
                'class_name': meta['class_name'],
                'static_metaobject': hx(meta['static_metaobject']),
                'stringdata': hx(meta['stringdata']),
                'metadata': hx(meta['metadata']),
                'static_metacall': hx(meta['static_metacall']),
                'jump_table': hx(jump_table),
                'method': {
                    'index': method['index'],
                    'name': method['name'],
                    'argc': method['argc'],
                    'flags': method['flags'],
                    'return_type': method['return_type'],
                    'parameter_types': method['parameter_types'],
                    'parameter_names': method['parameter_names'],
                    'case_target': hx(case_target),
                },
                'direct_edges': [
                    {'site': hx(edge['site']), 'target': hx(edge['target']), 'mnemonic': edge['mnemonic']}
                    for edge in hits
                ],
            })
    unique = {
        (
            row['class_name'], row['static_metacall'], row['method']['index'], row['method']['case_target'],
            tuple((edge['site'], edge['target']) for edge in row['direct_edges']),
        ): row
        for row in links
    }
    return list(unique.values())


def rip_lea_refs_to(img: core.Image, target: int) -> list[int]:
    refs: set[int] = set()
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        pos = 0
        while True:
            pos = blob.find(b'\x8d', pos)
            if pos < 0:
                break
            # REX + LEA r64,[RIP+disp32]
            if pos > 0 and 0x40 <= blob[pos - 1] <= 0x4F and pos + 6 <= len(blob):
                modrm = blob[pos + 1]
                if (modrm & 0xC7) == 0x05:
                    start = pos - 1
                    disp = int.from_bytes(blob[pos + 2:pos + 6], 'little', signed=True)
                    if section.va + start + 7 + disp == target:
                        refs.add(section.va + start)
            # LEA r32,[RIP+disp32] (kept as a bounded fallback)
            if pos + 6 <= len(blob):
                modrm = blob[pos + 1]
                if (modrm & 0xC7) == 0x05:
                    disp = int.from_bytes(blob[pos + 2:pos + 6], 'little', signed=True)
                    if section.va + pos + 6 + disp == target:
                        refs.add(section.va + pos)
            pos += 1
    return sorted(refs)


def owner_constructors_focused(img: core.Image, owner_ap: int) -> list[dict]:
    rows = []
    seen: set[tuple[tuple[int, int], str, int]] = set()
    for ref in rip_lea_refs_to(img, owner_ap):
        fde = img.fde(ref)
        if fde is None or fde[1] - fde[0] > 0x10000:
            continue
        instructions = img.instructions(fde)
        for store in core.explicit_vtable_stores(img, instructions, owner_ap):
            key = (fde, store['object_family'], store['store_site'])
            if key in seen:
                continue
            store_index = next((i for i, row in enumerate(instructions) if row.address == store['store_site']), None)
            if store_index is None:
                continue
            entry = core.trace_family_to_entry(img, instructions, store_index, store['object_family'])
            if entry.get('classification') != 'ENTRY_ALIAS_PROVEN':
                continue
            seen.add(key)
            rows.append({
                'fde': fde,
                'this_family': store['object_family'],
                'vtable_store_site': store['store_site'],
                '_instructions': instructions,
            })
    return rows


def focused_owner_binding(img: core.Image, owner_class: str) -> dict:
    owner_vtables = focused_type_vtables(img, owner_class)
    proof_rows = []
    for owner_ap in owner_vtables:
        for ctor in owner_constructors_focused(img, owner_ap):
            for proof in core.constructor_member_proofs(img, ctor, MEMBER_OFFSET):
                proof_rows.append({
                    'owner_type': owner_class,
                    'owner_vtable_address_point': hx(owner_ap),
                    'constructor_fde': [hx(ctor['fde'][0]), hx(ctor['fde'][1])],
                    **proof,
                })
    unique = {
        (
            row['owner_vtable_address_point'], tuple(row['constructor_fde']), row.get('member_store_site'), row['classification']
        ): row
        for row in proof_rows
    }
    rows = list(unique.values())
    proven = [row for row in rows if row['classification'] == 'PARENT_MEMBER_HANDLER_BINDING_PROVEN']
    return {
        'classification': 'FOCUSED_OWNER_CONSTRUCTOR_BINDING',
        'owner_class': owner_class,
        'owner_vtables': [hx(value) for value in owner_vtables],
        'proof_count': len(proven),
        'proofs': rows,
        'binding': 'PARENT_MEMBER_HANDLER_BINDING_PROVEN' if len(proven) == 1 else 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    img = core.Image(args.client)
    reassertion = verify_fresh_exact(img)
    target_fde = VIABLE_CALLER_FDE_0XCEDD90
    direct_edges = direct_edges_into_fde(img, target_fde)
    links = qmeta_method_links(img, target_fde, direct_edges)

    if len(links) == 1:
        owner = links[0]
        owner_classification = 'FOCUSED_QMETA_OWNER_PROVEN'
        binding = focused_owner_binding(img, owner['class_name'])
    else:
        owner = None
        owner_classification = 'FOCUSED_QMETA_OWNER_UNKNOWN'
        binding = {
            'classification': 'FOCUSED_OWNER_CONSTRUCTOR_BINDING',
            'owner_class': None,
            'owner_vtables': [],
            'proof_count': 0,
            'proofs': [],
            'binding': 'PARENT_MEMBER_HANDLER_BINDING_UNKNOWN',
        }

    if owner is not None and binding['binding'] == 'PARENT_MEMBER_HANDLER_BINDING_PROVEN':
        classification = 'FIELD6_VALUE_PROVEN'
        value = VIABLE_EDX_VALUE_1
        accepted = {
            'site': hx(VIABLE_CALLSITE_0XCEDDCB),
            'fde': [hx(target_fde[0]), hx(target_fde[1])],
            'value': value,
            'owner_class': owner['class_name'],
            'owner_method': owner['method'],
        }
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None
        accepted = None

    result = {
        'schema': 'otclient.track-a.current-login-field6-focused-owner.v1',
        **SAFETY,
        'exact_client': {
            'version': '15.32.75d4a0',
            'sha256': EXPECTED_SHA256,
            'size': EXPECTED_SIZE,
        },
        'fresh_exact_reassertion': reassertion,
        'focused_timeout_recovery': {
            'classification': 'FOCUSED_TIMEOUT_RECOVERY',
            'no_full_scalar_census': NO_FULL_SCALAR_CENSUS,
            'viable_callsite': hx(VIABLE_CALLSITE_0XCEDDCB),
            'viable_caller_fde': [hx(target_fde[0]), hx(target_fde[1])],
            'viable_edx_value': VIABLE_EDX_VALUE_1,
            'direct_edges_into_viable_fde': [
                {
                    'site': hx(row['site']),
                    'target': hx(row['target']),
                    'source_fde': [hx(row['source_fde'][0]), hx(row['source_fde'][1])],
                    'mnemonic': row['mnemonic'],
                }
                for row in direct_edges
            ],
        },
        'focused_qmeta_owner': {
            'classification': 'FOCUSED_QMETA_OWNER',
            'owner_classification': owner_classification,
            'link_count': len(links),
            'links': links,
        },
        'focused_owner_constructor_binding': binding,
        'classification': classification,
        'field6_value': value,
        'accepted_callsite': accepted,
        'scope_markers': {
            'FRESH_EXACT_REASSERTION': FRESH_EXACT_REASSERTION,
            'FOCUSED_QMETA_OWNER': FOCUSED_QMETA_OWNER,
            'FOCUSED_OWNER_CONSTRUCTOR_BINDING': FOCUSED_OWNER_CONSTRUCTOR_BINDING,
            'NO_FULL_SCALAR_CENSUS': NO_FULL_SCALAR_CENSUS,
            'NO_HEURISTIC_RANKING': NO_HEURISTIC_RANKING,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('FOCUSED_TIMEOUT_RECOVERY=PASS')
    print('FRESH_EXACT_REASSERTION=PASS')
    print('FOCUSED_QMETA_OWNER=' + owner_classification)
    print('FOCUSED_OWNER_CONSTRUCTOR_BINDING=' + binding['binding'])
    print('FIELD6_VALUE=' + classification)
    print('NO_FULL_SCALAR_CENSUS=true')
    print('NO_HEURISTIC_RANKING=true')
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
