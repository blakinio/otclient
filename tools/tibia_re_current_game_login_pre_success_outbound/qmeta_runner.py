#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import deque
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


def register_family(name: str) -> str:
    aliases = {
        'rax': 'rax', 'eax': 'rax', 'ax': 'rax', 'al': 'rax', 'ah': 'rax',
        'rbx': 'rbx', 'ebx': 'rbx', 'bx': 'rbx', 'bl': 'rbx', 'bh': 'rbx',
        'rcx': 'rcx', 'ecx': 'rcx', 'cx': 'rcx', 'cl': 'rcx', 'ch': 'rcx',
        'rdx': 'rdx', 'edx': 'rdx', 'dx': 'rdx', 'dl': 'rdx', 'dh': 'rdx',
        'rsi': 'rsi', 'esi': 'rsi', 'si': 'rsi', 'sil': 'rsi',
        'rdi': 'rdi', 'edi': 'rdi', 'di': 'rdi', 'dil': 'rdi',
        'rbp': 'rbp', 'ebp': 'rbp', 'bp': 'rbp', 'bpl': 'rbp',
        'rsp': 'rsp', 'esp': 'rsp', 'sp': 'rsp', 'spl': 'rsp',
    }
    if name in aliases:
        return aliases[name]
    match = re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?', name)
    return match.group(1) if match else name


def writes_register_family(img: core.Image, row, wanted: str) -> bool:
    try:
        _reads, writes = row.regs_access()
    except Exception:
        return False
    return wanted in {register_family(img.md.reg_name(reg)) for reg in writes}


def instruction_predecessors(instructions) -> dict[int, set[int]]:
    by_address = {row.address: row for row in instructions}
    predecessors = {row.address: set() for row in instructions}
    for index, row in enumerate(instructions):
        next_address = instructions[index + 1].address if index + 1 < len(instructions) else None
        successors: set[int] = set()
        mnemonic = row.mnemonic.lower()
        if mnemonic.startswith('ret'):
            pass
        elif mnemonic == 'jmp':
            if row.operands and row.operands[0].type == core.X86_OP_IMM:
                target = int(row.operands[0].imm)
                if target in by_address:
                    successors.add(target)
        elif mnemonic.startswith('j'):
            if row.operands and row.operands[0].type == core.X86_OP_IMM:
                target = int(row.operands[0].imm)
                if target in by_address:
                    successors.add(target)
            if next_address is not None:
                successors.add(next_address)
        else:
            if next_address is not None:
                successors.add(next_address)
        for successor in successors:
            predecessors[successor].add(row.address)
    return predecessors


def backward_register_definition(img: core.Image, instructions, site: int, source_name: str) -> dict:
    by_address = {row.address: row for row in instructions}
    if site not in by_address:
        raise RuntimeError(f'FIELD6_SITE_UNKNOWN:{site:#x}')
    wanted = register_family(source_name)
    predecessors = instruction_predecessors(instructions)
    queue = deque(predecessors[site])
    visited: set[int] = set()
    definitions: dict[int, dict] = {}
    reaches_entry_without_definition = False

    while queue:
        address = queue.popleft()
        if address in visited:
            continue
        visited.add(address)
        row = by_address[address]
        if writes_register_family(img, row, wanted):
            definitions[address] = {
                'definition_site': core.hx(address),
                'mnemonic': row.mnemonic,
                'operand': row.op_str,
                'written_register_family': wanted,
                'instructions': bounded_context(instructions, address, before=14, after=14),
            }
            continue
        preds = predecessors.get(address, set())
        if not preds:
            reaches_entry_without_definition = True
        else:
            queue.extend(preds)

    rows = [definitions[key] for key in sorted(definitions)]
    if len(rows) == 1 and not reaches_entry_without_definition:
        classification = 'CFG_REACHING_DEFINITION_UNIQUE'
    elif rows:
        classification = 'CFG_REACHING_DEFINITION_MULTIPLE_OR_ENTRY'
    else:
        classification = 'CFG_REACHING_DEFINITION_ENTRY_ONLY'
    return {
        'classification': classification,
        'source_register_family': wanted,
        'definitions': rows,
        'reaches_entry_without_definition': reaches_entry_without_definition,
        'visited_instruction_count': len(visited),
    }


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
    field6_source = field6_writes[0]['source']

    nested_sites = result['primary_producer_field_presence']['nested_auth_slot_reference_sites']
    required_slots = ('0x30', '0x40', '0x18', '0x50', '0x60')
    for slot in required_slots:
        if len(nested_sites.get(slot, [])) != 1:
            raise RuntimeError(f'NESTED_SOURCE_SITE_AMBIGUOUS:{slot}:{nested_sites.get(slot)}')

    result['field6_source_context'] = {
        'write_site': core.hx(field6_site),
        'write_source': field6_source,
        'instructions': bounded_context(instructions, field6_site),
        'classification': 'BOUNDED_INSTRUCTION_CONTEXT_ONLY',
    }
    result['field6_backward_source'] = backward_register_definition(
        img,
        instructions,
        field6_site,
        field6_source,
    )
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
    print('FIELD6_BACKWARD_SOURCE=PASS')
    print('NESTED_SOURCE_CONTEXTS=PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args, _ = parser.parse_known_args()
    core.main()
    add_source_contexts(args.client, args.output)
