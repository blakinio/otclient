#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

import qmeta_runner as base

core = base.core
CONSTRUCTOR_FDE_ANCHOR = '0x7d15c0'
CONNECT_TARGET = 0x4D6800
OWNER_FIELD = 0x9C0


def find_handler_constructor(img: core.Image, handler: dict) -> tuple[int, int]:
    refs = base.rip_refs(img, handler['address_point'])
    candidates = []
    for ref in refs:
        fde = img.fde(ref)
        if fde is None:
            continue
        insns = img.instructions(fde)
        has_owner_store = any(
            ins.mnemonic == 'mov'
            and ins.operands
            and ins.operands[0].type == core.X86_OP_MEM
            and int(ins.operands[0].mem.disp) == OWNER_FIELD
            for ins in insns
        )
        if has_owner_store:
            candidates.append(fde)
    unique = sorted(set(candidates))
    if len(unique) != 1:
        raise RuntimeError(f'HANDLER_CONSTRUCTOR_AMBIGUOUS:{len(unique)}:{unique}')
    return unique[0]


def connection_thunks(img: core.Image, constructor_fde: tuple[int, int]) -> list[dict]:
    insns = img.instructions(constructor_fde)
    thunks = []
    seen = set()
    for index, ins in enumerate(insns):
        if ins.mnemonic != 'call' or not ins.operands or ins.operands[0].type != core.X86_OP_IMM:
            continue
        if int(ins.operands[0].imm) != CONNECT_TARGET:
            continue
        thunk = None
        store = None
        handler_load = None
        for row in reversed(insns[max(0, index - 28):index]):
            if handler_load is None and row.mnemonic == 'mov' and len(row.operands) >= 2:
                dst, src = row.operands[0], row.operands[1]
                if src.type == core.X86_OP_MEM and int(src.mem.disp) == OWNER_FIELD:
                    handler_load = row
            if store is None and row.mnemonic == 'mov' and len(row.operands) >= 2:
                dst, src = row.operands[0], row.operands[1]
                if dst.type == core.X86_OP_MEM and int(dst.mem.disp) == 8 and src.type == core.X86_OP_REG:
                    source_reg = src.reg
                    store = row
                    store_index = next(i for i, x in enumerate(insns) if x.address == row.address)
                    for prev in reversed(insns[max(0, store_index - 8):store_index]):
                        if prev.mnemonic != 'lea' or len(prev.operands) < 2:
                            continue
                        if prev.operands[0].type != core.X86_OP_REG or prev.operands[0].reg != source_reg:
                            continue
                        target = core.rip_target(prev)
                        if target is not None and img.executable(target):
                            thunk = target
                            break
            if thunk is not None and handler_load is not None:
                break
        if thunk is None:
            continue
        key = (ins.address, thunk)
        if key in seen:
            continue
        seen.add(key)
        thunks.append({
            'connect_site': core.hx(ins.address),
            'thunk_target': core.hx(thunk),
            'thunk_fde': ([core.hx(x) for x in img.fde(thunk)] if img.fde(thunk) else None),
            'handler_owner_load': ({'at': core.hx(handler_load.address), 'operand': handler_load.op_str} if handler_load else None),
            'constructor_context': base.bounded_context(insns, ins.address, before=24, after=8),
        })
    return thunks


def direct_edges(img: core.Image, fde: tuple[int, int]) -> list[tuple[int, int, str]]:
    rows = []
    for ins in img.instructions(fde):
        if ins.mnemonic not in ('call', 'jmp') or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type == core.X86_OP_IMM:
            target = int(op.imm)
            if img.executable(target):
                rows.append((ins.address, target, ins.mnemonic))
    return rows


def slot_0x60_calls(img: core.Image, fde: tuple[int, int]) -> list[dict]:
    insns = img.instructions(fde)
    out = []
    for ins in insns:
        if ins.mnemonic != 'call' or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type != core.X86_OP_MEM or int(op.mem.disp) != 0x60 or not op.mem.base:
            continue
        out.append({
            'site': core.hx(ins.address),
            'operand': ins.op_str,
            'local_dataflow': base.local_virtual_dataflow(img, insns, ins.address, op.mem.base),
            'context': base.bounded_context(insns, ins.address, before=32, after=16),
        })
    return out


def thunk_graph(img: core.Image, thunk: int) -> dict:
    root_fde = img.fde(thunk)
    if root_fde is None:
        return {'classification': 'NO_UNIQUE_THUNK_FDE', 'root': core.hx(thunk)}
    queue = deque([(root_fde, 0)])
    seen = {root_fde}
    visited = []
    slots = []
    max_depth = 2
    max_fdes = 48
    while queue:
        fde, depth = queue.popleft()
        visited.append({'fde': [core.hx(fde[0]), core.hx(fde[1])], 'depth': depth})
        for row in slot_0x60_calls(img, fde):
            slots.append({**row, 'depth': depth, 'fde': [core.hx(fde[0]), core.hx(fde[1])]})
        if depth >= max_depth:
            continue
        for _site, target, _kind in direct_edges(img, fde):
            target_fde = img.fde(target)
            if target_fde is None or target_fde in seen:
                continue
            if target_fde[1] - target_fde[0] > 0x9000 or len(seen) >= max_fdes:
                continue
            seen.add(target_fde)
            queue.append((target_fde, depth + 1))
    return {
        'classification': 'BOUNDED_HANDLER_CONNECTION_THUNK_GRAPH',
        'root': core.hx(thunk),
        'root_fde': [core.hx(root_fde[0]), core.hx(root_fde[1])],
        'max_depth': max_depth,
        'visited_fde_count': len(seen),
        'visited_fdes': visited,
        'slot_0x60_calls': slots,
    }


def handler_connection_thunk_graph(img: core.Image) -> dict:
    handler = core.exact_vtable(
        img,
        'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler',
    )
    constructor_fde = find_handler_constructor(img, handler)
    thunks = connection_thunks(img, constructor_fde)
    for row in thunks:
        row['graph'] = thunk_graph(img, int(row['thunk_target'], 16))
    slot_calls = [
        {'connect_site': row['connect_site'], 'thunk_target': row['thunk_target'], **call}
        for row in thunks
        for call in row['graph'].get('slot_0x60_calls', [])
    ]
    return {
        'classification': 'HANDLER_CONNECTION_THUNK_GRAPH',
        'constructor_fde': [core.hx(constructor_fde[0]), core.hx(constructor_fde[1])],
        'constructor_anchor': CONSTRUCTOR_FDE_ANCHOR,
        'handler_vtable_address_point': core.hx(handler['address_point']),
        'handler_slot_0x60_target': core.hx(core.slot_target(handler, 0x60)),
        'connection_count': len(thunks),
        'connections': thunks,
        'reachable_slot_0x60_calls': slot_calls,
        'reachable_slot_0x60_call_count': len(slot_calls),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    graph = handler_connection_thunk_graph(img)
    result['handler_connection_thunk_graph'] = graph
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('HANDLER_CONNECTION_THUNK_GRAPH=PASS')
    print('HANDLER_CONNECTION_COUNT=' + str(graph['connection_count']))
    print('HANDLER_CONNECTION_REACHABLE_SLOT_0X60_CALL_COUNT=' + str(graph['reachable_slot_0x60_call_count']))


if __name__ == '__main__':
    main()
