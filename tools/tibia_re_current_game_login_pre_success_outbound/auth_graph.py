#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

import qmeta_runner as base

core = base.core


def direct_calls(img: core.Image, fde: tuple[int, int]) -> list[dict]:
    rows = []
    for ins in img.instructions(fde):
        if ins.mnemonic != 'call' or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type == core.X86_OP_IMM:
            target = int(op.imm)
            rows.append({'site': ins.address, 'target': target, 'target_fde': img.fde(target)})
    return rows


def slot_0x60_calls(img: core.Image, fde: tuple[int, int]) -> list[dict]:
    rows = []
    insns = img.instructions(fde)
    for ins in insns:
        if ins.mnemonic != 'call' or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type != core.X86_OP_MEM or int(op.mem.disp) != 0x60 or not op.mem.base:
            continue
        rows.append({
            'site': core.hx(ins.address),
            'operand': ins.op_str,
            'fde': [core.hx(fde[0]), core.hx(fde[1])],
            'local_dataflow': base.local_virtual_dataflow(img, insns, ins.address, op.mem.base),
            'instructions': base.bounded_context(insns, ins.address, before=36, after=20),
        })
    return rows


def auth_start_gameserver_login_graph(img: core.Image) -> dict:
    auth = base.exact_qmeta_class(
        img,
        'tibia::authentication::TAuthenticationProcessController',
        ('requestCharacterGameserverLogin', 'onStartGameServerLoginStateEntered'),
    )
    root = auth['methods']['onStartGameServerLoginStateEntered']
    if root['fde'] is None:
        raise RuntimeError('AUTH_START_GAMESERVER_LOGIN_FDE_UNKNOWN')

    queue = deque([(root['fde'], 0)])
    seen: set[tuple[int, int]] = {root['fde']}
    graph_fdes = []
    slot_calls = []
    direct_edges = []
    max_depth = 3
    max_fdes = 160

    while queue:
        fde, depth = queue.popleft()
        graph_fdes.append({'fde': [core.hx(fde[0]), core.hx(fde[1])], 'depth': depth})
        slot_calls.extend({**row, 'depth': depth} for row in slot_0x60_calls(img, fde))
        for edge in direct_calls(img, fde):
            direct_edges.append({
                'site': core.hx(edge['site']),
                'target': core.hx(edge['target']),
                'target_fde': ([core.hx(edge['target_fde'][0]), core.hx(edge['target_fde'][1])] if edge['target_fde'] else None),
                'depth': depth,
            })
            target_fde = edge['target_fde']
            if depth >= max_depth or target_fde is None or target_fde in seen:
                continue
            # Keep the graph on bounded application functions and avoid exploding
            # into giant runtime/compiler support regions.
            if target_fde[1] - target_fde[0] > 0x9000:
                continue
            if len(seen) >= max_fdes:
                continue
            seen.add(target_fde)
            queue.append((target_fde, depth + 1))

    return {
        'classification': 'AUTH_START_GAMESERVER_LOGIN_GRAPH',
        'class_name': 'tibia::authentication::TAuthenticationProcessController',
        'root_method': 'onStartGameServerLoginStateEntered',
        'root_target': core.hx(root['target']),
        'root_fde': [core.hx(root['fde'][0]), core.hx(root['fde'][1])],
        'request_character_gameserver_login_target': core.hx(auth['methods']['requestCharacterGameserverLogin']['target']),
        'max_depth': max_depth,
        'visited_fde_count': len(seen),
        'visited_fdes': graph_fdes,
        'direct_edges': direct_edges,
        'virtual_slot_0x60_calls': slot_calls,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    graph = auth_start_gameserver_login_graph(img)
    result['auth_start_gameserver_login_graph'] = graph
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('AUTH_START_GAMESERVER_LOGIN_GRAPH=PASS')
    print('AUTH_START_GRAPH_FDE_COUNT=' + str(graph['visited_fde_count']))
    print('AUTH_START_GRAPH_SLOT_0X60_CALL_COUNT=' + str(len(graph['virtual_slot_0x60_calls'])))


if __name__ == '__main__':
    main()
