#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

import handler_qmeta as qmeta
import probe as core

QUEUE_SENDLOGIN_PROVENANCE = True
QUEUE_CLASS = 'tibia::protocol::TProtocolMessageQueue'
SLOT_0X60_EDGE = True
FIELD6_EDX_REACHING_VALUE = True
NO_SEMANTIC_GUESSING = True
MAX_DEPTH = 3


def recover_queue_qmeta(img: core.Image) -> dict:
    previous = qmeta.HANDLER_QMETA_CLASS
    qmeta.HANDLER_QMETA_CLASS = QUEUE_CLASS
    try:
        return qmeta.recover_qmeta(img)
    finally:
        qmeta.HANDLER_QMETA_CLASS = previous


def sanitize_instruction(row) -> dict:
    return {'at': core.hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}


def case_block(img: core.Image, meta: dict, target: int) -> list:
    fde = img.fde(target)
    if fde is None:
        raise RuntimeError('sendLogin QMeta case FDE unavailable')
    instructions = img.instructions(fde)
    by = {row.address: i for i, row in enumerate(instructions)}
    if target not in by:
        raise RuntimeError('sendLogin case target is not instruction aligned')
    other_targets = {int(row['case_target']) for row in meta['methods'] if int(row['case_target']) != target}
    start = by[target]
    out = []
    for row in instructions[start:start + 96]:
        if out and row.address in other_targets:
            break
        out.append(row)
        mnemonic = row.mnemonic.lower()
        if mnemonic.startswith('ret'):
            break
        if mnemonic == 'jmp':
            break
    return out


def direct_edges(rows) -> list[dict]:
    out = []
    for row in rows:
        if row.mnemonic not in ('call', 'jmp') or not row.operands or row.operands[0].type != core.X86_OP_IMM:
            continue
        out.append({'site': row.address, 'target': int(row.operands[0].imm), 'mnemonic': row.mnemonic})
    return out


def exact_target_guard(img: core.Image, instructions, call_index: int) -> dict | None:
    call = instructions[call_index]
    if call.mnemonic != 'call' or not call.operands or call.operands[0].type != core.X86_OP_MEM:
        return None
    mem = call.operands[0]
    if int(mem.mem.disp) != core.HANDLER_SLOT or not mem.mem.base:
        return None
    vtable_family = core.reg_family(img.md.reg_name(mem.mem.base))
    target_loads = []
    compare_sites = []
    for row in instructions[max(0, call_index - 32):call_index]:
        if row.mnemonic == 'lea' and core.rip_target(row) == core.HANDLER_SLOT_TARGET and row.operands and row.operands[0].type == core.X86_OP_REG:
            target_loads.append((row.address, core.reg_family(img.md.reg_name(row.operands[0].reg))))
        if row.mnemonic == 'cmp' and len(row.operands) >= 2:
            families = []
            for op in row.operands[:2]:
                if op.type == core.X86_OP_REG:
                    families.append(core.reg_family(img.md.reg_name(op.reg)))
            compare_sites.append((row.address, families, row.op_str))
    for load_site, target_family in target_loads:
        for compare_site, families, operand in compare_sites:
            if target_family in families and vtable_family in families:
                return {
                    'classification': 'EXACT_PRODUCER_TARGET_GUARD',
                    'target_load_site': core.hx(load_site),
                    'compare_site': core.hx(compare_site),
                    'compare_operand': operand,
                    'producer_target': core.hx(core.HANDLER_SLOT_TARGET),
                }
    return None


def slot_calls_in_fde(img: core.Image, fde: tuple[int, int], depth: int) -> list[dict]:
    instructions = img.instructions(fde)
    rows = []
    for index, row in enumerate(instructions):
        if row.mnemonic != 'call' or not row.operands or row.operands[0].type != core.X86_OP_MEM:
            continue
        mem = row.operands[0]
        if int(mem.mem.disp) != core.HANDLER_SLOT or not mem.mem.base:
            continue
        binding = core.bind_callsite_owner(img, instructions, index)
        guard = exact_target_guard(img, instructions, index)
        edx = core.reaching_edx(img, instructions, index)
        rows.append({
            'site': core.hx(row.address),
            'fde': [core.hx(fde[0]), core.hx(fde[1])],
            'depth': depth,
            'operand': row.op_str,
            'binding': binding,
            'exact_target_guard': guard,
            'edx': edx,
        })
    return rows


def bounded_graph(img: core.Image, initial_edges: list[dict]) -> dict:
    queue = deque()
    visited: set[tuple[int, int]] = set()
    graph_edges = []
    slot_calls = []
    for edge in initial_edges:
        fde = img.fde(edge['target'])
        if fde and fde[1] - fde[0] <= 0x10000:
            queue.append((fde, 1))
        graph_edges.append({**edge, 'site': core.hx(edge['site']), 'target': core.hx(edge['target']), 'depth': 0})

    while queue:
        fde, depth = queue.popleft()
        if fde in visited or depth > MAX_DEPTH:
            continue
        visited.add(fde)
        slot_calls.extend(slot_calls_in_fde(img, fde, depth))
        if depth == MAX_DEPTH:
            continue
        for row in img.instructions(fde):
            if row.mnemonic not in ('call', 'jmp') or not row.operands or row.operands[0].type != core.X86_OP_IMM:
                continue
            target = int(row.operands[0].imm)
            target_fde = img.fde(target)
            graph_edges.append({
                'site': core.hx(row.address),
                'target': core.hx(target),
                'depth': depth,
                'mnemonic': row.mnemonic,
                'source_fde': [core.hx(fde[0]), core.hx(fde[1])],
            })
            if target_fde and target_fde not in visited and target_fde[1] - target_fde[0] <= 0x10000:
                queue.append((target_fde, depth + 1))
    return {
        'visited_fdes': [[core.hx(a), core.hx(b)] for a, b in sorted(visited)],
        'direct_edges': graph_edges,
        'slot_0x60_calls': slot_calls,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)
    meta = recover_queue_qmeta(img)

    send_login = [row for row in meta['methods'] if row['name'] == 'sendLogin']
    if len(send_login) != 1:
        raise RuntimeError(f'sendLogin QMeta method ambiguous: {len(send_login)}')
    method = send_login[0]
    target = int(method['case_target'])
    block = case_block(img, meta, target)
    initial_edges = direct_edges(block)
    graph = bounded_graph(img, initial_edges)

    accepted = []
    for call in graph['slot_0x60_calls']:
        bound = call['binding'].get('classification') in ('BOUND_HANDLER_OWNER_FIELD', 'BOUND_HANDLER_EXPLICIT_VTABLE')
        guarded = call['exact_target_guard'] is not None
        if bound or guarded:
            accepted.append(call)

    scalar = [call for call in accepted if call['edx'].get('classification') == 'UNIQUE_STATIC_SCALAR']
    values = {call['edx'].get('value') for call in scalar}
    if len(accepted) == 1 and len(scalar) == 1 and len(values) == 1:
        classification = 'FIELD6_VALUE_PROVEN'
        value = next(iter(values))
        accepted_call = scalar[0]
        result['classification'] = classification
        result['field6_value'] = value
        result['accepted_callsite'] = accepted_call
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None
        accepted_call = None

    result['queue_sendlogin_provenance'] = {
        'classification': 'QUEUE_SENDLOGIN_PROVENANCE',
        'class_name': QUEUE_CLASS,
        'qmeta_revision': meta['revision'],
        'qmeta_method_count': meta['method_count'],
        'sendlogin': {
            'index': method['index'],
            'name': method['name'],
            'argc': method['argc'],
            'return_type': method['return_type'],
            'parameter_types': method['parameter_types'],
            'parameter_names': method['parameter_names'],
            'case_target': core.hx(target),
            'case_fde': [core.hx(x) for x in img.fde(target)] if img.fde(target) else None,
            'case_block': [sanitize_instruction(row) for row in block],
        },
        'graph': graph,
        'accepted_slot_call_count': len(accepted),
        'accepted_slot_calls': accepted,
        'field6_value_classification': classification,
        'field6_value': value,
        'accepted_callsite': accepted_call,
        'scope_markers': {
            'PARAMETER_TYPES': True,
            'PARAMETER_NAMES': True,
            'SLOT_0X60_EDGE': SLOT_0X60_EDGE,
            'FIELD6_EDX_REACHING_VALUE': FIELD6_EDX_REACHING_VALUE,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('QUEUE_SENDLOGIN_PROVENANCE=PASS')
    print('TProtocolMessageQueue=PASS')
    print('sendLogin=PASS')
    print('PARAMETER_TYPES=PASS')
    print('PARAMETER_NAMES=PASS')
    print('SLOT_0X60_EDGE=' + ('PASS' if graph['slot_0x60_calls'] else 'NONE'))
    print('FIELD6_EDX_REACHING_VALUE=' + classification)
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
