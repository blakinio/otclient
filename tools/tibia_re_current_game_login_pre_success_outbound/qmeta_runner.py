#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe as core


def exact_qmeta_class(img: core.Image, class_name: str, required: tuple[str, ...]) -> dict:
    candidates = []
    for sbase in core.stringdata_bases_for_literal(img, class_name):
        for mbase in range(max(0, sbase - 0x20000) & ~3, sbase + 0x20000, 4):
            meta = core.parse_meta(img, sbase, mbase)
            if not meta or meta['class_name'] != class_name:
                continue
            names = {row['name'] for row in meta['rows']}
            if not set(required).issubset(names):
                continue
            static = []
            for where, value in img.rel.items():
                if value != sbase or img.rel.get(where + 8) != mbase:
                    continue
                target = img.rel.get(where + 16)
                if target is not None and img.executable(target):
                    static.append(target)
            if len(static) != 1:
                continue
            table, targets = core.recover_qmeta_jump_table(img, static[0], meta['method_count'])
            methods = {}
            for row in meta['rows']:
                if row['name'] not in required:
                    continue
                target = targets[row['index']]
                methods[row['name']] = {
                    'index': row['index'],
                    'target': target,
                    'fde': img.fde(target),
                }
            candidates.append({
                'metadata': mbase,
                'stringdata': sbase,
                'static_metacall': static[0],
                'jump_table': table,
                'methods': methods,
            })
    unique = {(row['metadata'], row['stringdata']): row for row in candidates}
    if len(unique) != 1:
        raise RuntimeError(f'QMETA_CLASS_AMBIGUOUS:{class_name}:{len(unique)}')
    return next(iter(unique.values()))


core.exact_qmeta_class = exact_qmeta_class


def bounded_context(instructions, site: int, before: int = 18, after: int = 20) -> list[dict]:
    indexes = [i for i, row in enumerate(instructions) if row.address == site]
    if len(indexes) != 1:
        raise RuntimeError(f'CONTEXT_SITE_AMBIGUOUS:{site:#x}:{len(indexes)}')
    index = indexes[0]
    return [
        {
            'at': core.hx(row.address),
            'mnemonic': row.mnemonic,
            'operand': row.op_str,
        }
        for row in instructions[max(0, index - before):index + after + 1]
    ]


def add_source_contexts(client: Path, output: Path) -> None:
    result = json.loads(output.read_text(encoding='utf-8'))
    img = core.Image(client)
    producer_fde = tuple(int(value, 16) for value in result['primary_login_producer']['fde'])
    instructions = img.instructions(producer_fde)

    field6_writes = [
        row for row in result['primary_producer_field_presence']['outer_varint_write_evidence']['6']
        if row['destination_offset'] == 236 and row['size'] == 4
    ]
    if len(field6_writes) != 1:
        raise RuntimeError(f'FIELD6_WRITE_AMBIGUOUS:{len(field6_writes)}')
    field6_site = int(field6_writes[0]['at'], 16)

    nested_sites = result['primary_producer_field_presence']['nested_auth_slot_reference_sites']
    required_slots = ('0x30', '0x40', '0x18', '0x50', '0x60')
    for slot in required_slots:
        if len(nested_sites.get(slot, [])) != 1:
            raise RuntimeError(f'NESTED_SOURCE_SITE_AMBIGUOUS:{slot}:{nested_sites.get(slot)}')

    result['field6_source_context'] = {
        'write_site': core.hx(field6_site),
        'write_source': field6_writes[0]['source'],
        'instructions': bounded_context(instructions, field6_site),
        'classification': 'BOUNDED_INSTRUCTION_CONTEXT_ONLY',
    }
    result['nested_source_contexts'] = {
        slot: {
            'reference_site': sites[0],
            'instructions': bounded_context(instructions, int(sites[0], 16)),
            'classification': 'BOUNDED_INSTRUCTION_CONTEXT_ONLY',
        }
        for slot, sites in nested_sites.items()
        if slot in required_slots
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('FIELD6_SOURCE_CONTEXT=PASS')
    print('NESTED_SOURCE_CONTEXTS=PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args, _ = parser.parse_known_args()
    core.main()
    add_source_contexts(args.client, args.output)
