#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

import handler_qmeta as qmeta
import probe as core
import queue_sendlogin as queueprov

GAMESERVER_LOGIN_ROUTE_PROVENANCE = True
AUTH_PROCESS_CLASS = 'tibia::authentication::TAuthenticationProcessController'
REQUEST_METHOD = 'requestCharacterGameserverLogin'
START_METHOD = 'onStartGameServerLoginStateEntered'
INTERPROCEDURAL_RDX_PROPAGATION = True
SLOT_0X60_EDGE = True
FIELD6_EDX_REACHING_VALUE = True
NO_SEMANTIC_GUESSING = True
MAX_ROUTE_DEPTH = 4
MAX_ROUTE_FDES = 64


def recover_auth_qmeta(img: core.Image) -> dict:
    previous = qmeta.HANDLER_QMETA_CLASS
    qmeta.HANDLER_QMETA_CLASS = AUTH_PROCESS_CLASS
    try:
        return qmeta.recover_qmeta(img)
    finally:
        qmeta.HANDLER_QMETA_CLASS = previous


def sanitize_instruction(row) -> dict:
    return {'at': core.hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}


def reaching_edx_with_entry(img: core.Image, instructions, site_index: int, entry_value: int | None) -> dict:
    site = instructions[site_index].address
    pred = core.build_predecessors(instructions)
    by = {row.address: row for row in instructions}
    queue = deque(pred.get(site, set()))
    visited: set[int] = set()
    definitions: dict[int, dict] = {}
    clobbered_paths = 0
    entry_paths = 0
    unknown_entry_paths = 0

    if not pred.get(site, set()):
        entry_paths = 1
        if entry_value is None:
            unknown_entry_paths = 1

    while queue:
        address = queue.popleft()
        if address in visited:
            continue
        visited.add(address)
        row = by[address]
        definition = core.scalar_definition(img, row, 'rdx')
        if definition is not None:
            definitions[address] = definition
            continue
        if row.mnemonic == 'call':
            clobbered_paths += 1
            continue
        predecessors = pred.get(address, set())
        if not predecessors:
            entry_paths += 1
            if entry_value is None:
                unknown_entry_paths += 1
        else:
            queue.extend(predecessors)

    rows = [definitions[key] for key in sorted(definitions)]
    scalar_values = {row['value'] for row in rows if row['kind'] == 'IMM'}
    if entry_paths and entry_value is not None:
        scalar_values.add(int(entry_value) & 0xFFFFFFFF)
    non_scalar = any(row['kind'] != 'IMM' for row in rows)
    if len(scalar_values) == 1 and not non_scalar and not clobbered_paths and not unknown_entry_paths:
        value = next(iter(scalar_values))
        classification = 'UNIQUE_STATIC_SCALAR'
    else:
        value = None
        classification = 'VALUE_NOT_UNIQUELY_PROVEN'
    return {
        'classification': classification,
        'value': value,
        'entry_value': entry_value,
        'definitions': [{**row, 'site': core.hx(row['site'])} for row in rows],
        'clobbered_paths': clobbered_paths,
        'entry_paths': entry_paths,
        'unknown_entry_paths': unknown_entry_paths,
    }


def method_detail(img: core.Image, meta: dict, name: str) -> dict:
    matches = [row for row in meta['methods'] if row['name'] == name]
    if len(matches) != 1:
        raise RuntimeError(f'{name} QMeta method ambiguous: {len(matches)}')
    method = matches[0]
    target = int(method['case_target'])
    fde = img.fde(target)
    if fde is None:
        raise RuntimeError(f'{name} QMeta case FDE unavailable')
    block = queueprov.case_block(img, meta, target)
    instructions = img.instructions(fde)
    by = {row.address: index for index, row in enumerate(instructions)}
    edges = []
    for edge in queueprov.direct_edges(block):
        index = by.get(edge['site'])
        rdx = reaching_edx_with_entry(img, instructions, index, None) if index is not None else None
        edges.append({
            'site': core.hx(edge['site']),
            'target': core.hx(edge['target']),
            'mnemonic': edge['mnemonic'],
            'rdx_at_edge': rdx,
        })
    return {
        'index': method['index'],
        'qmeta_role': 'signal' if method['index'] < meta['signal_count'] else 'method',
        'flags': method['flags'],
        'name': method['name'],
        'argc': method['argc'],
        'return_type': method['return_type'],
        'parameter_types': method['parameter_types'],
        'parameter_names': method['parameter_names'],
        'case_target': core.hx(target),
        'case_fde': [core.hx(fde[0]), core.hx(fde[1])],
        'case_block': [sanitize_instruction(row) for row in block],
        'direct_edges': edges,
    }


def slot_call_row(img: core.Image, fde: tuple[int, int], instructions, index: int, entry_value: int | None, depth: int) -> dict:
    row = instructions[index]
    binding = core.bind_callsite_owner(img, instructions, index)
    guard = queueprov.exact_target_guard(img, instructions, index)
    edx = reaching_edx_with_entry(img, instructions, index, entry_value)
    return {
        'site': core.hx(row.address),
        'fde': [core.hx(fde[0]), core.hx(fde[1])],
        'depth': depth,
        'operand': row.op_str,
        'binding': binding,
        'exact_target_guard': guard,
        'edx': edx,
        'rsi_origin': core.trace_register_origin(img, instructions, index, 'rsi'),
    }


def route_graph(img: core.Image, method: dict) -> dict:
    start_target = int(method['case_target'], 16)
    start_fde = img.fde(start_target)
    if start_fde is None:
        raise RuntimeError('route start FDE unavailable')
    start_instructions = img.instructions(start_fde)
    block_sites = {int(row['at'], 16) for row in method['case_block']}
    initial = []
    by = {row.address: i for i, row in enumerate(start_instructions)}
    for row in start_instructions:
        if row.address not in block_sites or row.mnemonic not in ('call', 'jmp') or not row.operands or row.operands[0].type != core.X86_OP_IMM:
            continue
        index = by[row.address]
        rdx = reaching_edx_with_entry(img, start_instructions, index, None)
        initial.append((int(row.operands[0].imm), rdx.get('value') if rdx.get('classification') == 'UNIQUE_STATIC_SCALAR' else None, row.address, row.mnemonic))

    queue = deque()
    graph_edges = []
    visited: set[tuple[tuple[int, int], int | None]] = set()
    slot_calls = []
    for target, entry_value, site, mnemonic in initial:
        target_fde = img.fde(target)
        graph_edges.append({'site': core.hx(site), 'target': core.hx(target), 'depth': 0, 'mnemonic': mnemonic, 'entry_rdx': entry_value})
        if target_fde and target_fde[1] - target_fde[0] <= 0x10000:
            queue.append((target_fde, entry_value, 1))

    while queue and len(visited) < MAX_ROUTE_FDES:
        fde, entry_value, depth = queue.popleft()
        key = (fde, entry_value)
        if key in visited or depth > MAX_ROUTE_DEPTH:
            continue
        visited.add(key)
        instructions = img.instructions(fde)
        for index, row in enumerate(instructions):
            if row.mnemonic == 'call' and row.operands and row.operands[0].type == core.X86_OP_MEM:
                mem = row.operands[0]
                if int(mem.mem.disp) == core.HANDLER_SLOT and mem.mem.base:
                    slot_calls.append(slot_call_row(img, fde, instructions, index, entry_value, depth))
            if depth == MAX_ROUTE_DEPTH or row.mnemonic not in ('call', 'jmp') or not row.operands or row.operands[0].type != core.X86_OP_IMM:
                continue
            target = int(row.operands[0].imm)
            target_fde = img.fde(target)
            if target_fde is None or target_fde[1] - target_fde[0] > 0x10000:
                continue
            rdx = reaching_edx_with_entry(img, instructions, index, entry_value)
            propagated = rdx.get('value') if rdx.get('classification') == 'UNIQUE_STATIC_SCALAR' else None
            graph_edges.append({
                'site': core.hx(row.address),
                'target': core.hx(target),
                'depth': depth,
                'mnemonic': row.mnemonic,
                'source_fde': [core.hx(fde[0]), core.hx(fde[1])],
                'entry_rdx': propagated,
            })
            queue.append((target_fde, propagated, depth + 1))

    return {
        'visited_fdes': [
            {'fde': [core.hx(fde[0]), core.hx(fde[1])], 'entry_rdx': entry}
            for fde, entry in sorted(visited, key=lambda item: (item[0][0], -1 if item[1] is None else item[1]))
        ],
        'direct_edges': graph_edges,
        'slot_0x60_calls': slot_calls,
        'bounded': len(visited) < MAX_ROUTE_FDES,
    }


def global_slot_partition(img: core.Image) -> dict:
    calls = core.enumerate_slot_calls(img)
    candidate_rows = []
    value_counter: Counter[int] = Counter()
    guarded = []
    guarded_scalar = []
    bound_scalar = []
    for call in calls:
        instructions = call['_instructions']
        index = call['_index']
        edx = core.reaching_edx(img, instructions, index)
        guard = queueprov.exact_target_guard(img, instructions, index)
        binding = call['binding']
        is_scalar = edx.get('classification') == 'UNIQUE_STATIC_SCALAR'
        is_bound = binding.get('classification') in ('BOUND_HANDLER_OWNER_FIELD', 'BOUND_HANDLER_EXPLICIT_VTABLE')
        if is_scalar:
            value_counter[int(edx['value'])] += 1
        if guard is not None or is_scalar or is_bound:
            row = {
                'site': core.hx(call['site']),
                'fde': [core.hx(call['fde'][0]), core.hx(call['fde'][1])],
                'operand': call['operand'],
                'binding': binding,
                'exact_target_guard': guard,
                'edx': edx,
                'rsi_origin': core.trace_register_origin(img, instructions, index, 'rsi'),
            }
            candidate_rows.append(row)
            if guard is not None:
                guarded.append(row)
            if guard is not None and is_scalar:
                guarded_scalar.append(row)
            if is_bound and is_scalar:
                bound_scalar.append(row)

    accepted = []
    accepted.extend(guarded_scalar)
    for row in bound_scalar:
        if row not in accepted:
            accepted.append(row)
    return {
        'slot_callsite_count': len(calls),
        'candidate_count': len(candidate_rows),
        'static_scalar_count': sum(value_counter.values()),
        'static_scalar_value_histogram': {str(key): value_counter[key] for key in sorted(value_counter)},
        'exact_target_guard_count': len(guarded),
        'exact_target_guard_scalar_count': len(guarded_scalar),
        'bound_scalar_count': len(bound_scalar),
        'candidate_callsites': candidate_rows,
        'accepted_callsites': accepted,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)
    meta = recover_auth_qmeta(img)
    request = method_detail(img, meta, REQUEST_METHOD)
    start = method_detail(img, meta, START_METHOD)
    graph = route_graph(img, start)
    partition = global_slot_partition(img)

    route_accepted = []
    for call in graph['slot_0x60_calls']:
        bound = call['binding'].get('classification') in ('BOUND_HANDLER_OWNER_FIELD', 'BOUND_HANDLER_EXPLICIT_VTABLE')
        guarded = call['exact_target_guard'] is not None
        if (bound or guarded) and call['edx'].get('classification') == 'UNIQUE_STATIC_SCALAR':
            route_accepted.append(call)

    accepted = route_accepted if route_accepted else partition['accepted_callsites']
    values = {row['edx']['value'] for row in accepted if row['edx'].get('classification') == 'UNIQUE_STATIC_SCALAR'}
    if len(accepted) == 1 and len(values) == 1:
        classification = 'FIELD6_VALUE_PROVEN'
        value = next(iter(values))
        result['classification'] = classification
        result['field6_value'] = value
        result['accepted_callsite'] = accepted[0]
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None

    result['gameserver_login_route_provenance'] = {
        'classification': 'GAMESERVER_LOGIN_ROUTE_PROVENANCE',
        'class_name': AUTH_PROCESS_CLASS,
        'qmeta_revision': meta['revision'],
        'qmeta_method_count': meta['method_count'],
        'qmeta_signal_count': meta['signal_count'],
        'request_character_gameserver_login': request,
        'on_start_gameserver_login_state_entered': start,
        'route_graph': graph,
        'route_accepted_slot_call_count': len(route_accepted),
        'route_accepted_slot_calls': route_accepted,
        'global_slot_partition': partition,
        'field6_value_classification': classification,
        'field6_value': value,
        'accepted_callsite': accepted[0] if len(accepted) == 1 else None,
        'scope_markers': {
            'INTERPROCEDURAL_RDX_PROPAGATION': INTERPROCEDURAL_RDX_PROPAGATION,
            'SLOT_0X60_EDGE': SLOT_0X60_EDGE,
            'FIELD6_EDX_REACHING_VALUE': FIELD6_EDX_REACHING_VALUE,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print('GAMESERVER_LOGIN_ROUTE_PROVENANCE=PASS')
    print('TAuthenticationProcessController=PASS')
    print('requestCharacterGameserverLogin=PASS')
    print('INTERPROCEDURAL_RDX_PROPAGATION=PASS')
    print('SLOT_0X60_EDGE=' + ('PASS' if graph['slot_0x60_calls'] else 'NONE'))
    print('EXACT_TARGET_GUARD_COUNT=' + str(partition['exact_target_guard_count']))
    print('FIELD6_EDX_REACHING_VALUE=' + classification)
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
