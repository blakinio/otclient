#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

import probe as core
import qmeta_runner as qmeta

EXPECTED_SHA256 = '552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'
EXPECTED_SIZE = 52105824


def exact_full_qmeta(img: core.Image, class_name: str, required: tuple[str, ...]) -> dict:
    anchor = qmeta.exact_qmeta_class(img, class_name, required)
    meta = core.parse_meta(img, anchor['stringdata'], anchor['metadata'])
    if not meta or meta['class_name'] != class_name:
        raise RuntimeError(f'FULL_QMETA_PARSE_FAILED:{class_name}')
    table, targets = core.recover_qmeta_jump_table(img, anchor['static_metacall'], meta['method_count'])
    if len(targets) != meta['method_count']:
        raise RuntimeError(f'FULL_QMETA_TARGET_COUNT_MISMATCH:{class_name}')
    rows = []
    for row in meta['rows']:
        index = int(row['index'])
        rows.append({
            'index': index,
            'name': row['name'],
            'argc': int(row['argc']),
            'role': 'SIGNAL' if index < int(meta['signal_count']) else 'NON_SIGNAL_METHOD',
            'target': int(targets[index]),
        })
    return {
        'class_name': class_name,
        'metadata': int(anchor['metadata']),
        'stringdata': int(anchor['stringdata']),
        'static_metacall': int(anchor['static_metacall']),
        'jump_table': int(table),
        'method_count': int(meta['method_count']),
        'signal_count': int(meta['signal_count']),
        'rows': rows,
    }


def short_method_transfer(img: core.Image, target: int) -> int | None:
    try:
        raw = img.bytes(target, 0x90)
    except Exception:
        return None
    for row in list(img.md.disasm(raw, target))[:28]:
        if row.mnemonic.startswith('ret'):
            return None
        if row.mnemonic == 'jmp':
            if row.operands and row.operands[0].type == core.X86_OP_IMM:
                branch_target = int(row.operands[0].imm)
                if img.executable(branch_target):
                    return branch_target
            return None
    return None


def qmeta_target_candidates(img: core.Image, qmeta_class: dict, peer: int) -> list[dict]:
    out = []
    for row in qmeta_class['rows']:
        target = int(row['target'])
        tail = short_method_transfer(img, target)
        if target != peer and tail != peer:
            continue
        out.append({
            'class': qmeta_class['class_name'],
            'index': row['index'],
            'name': row['name'],
            'argc': row['argc'],
            'role': row['role'],
            'qmeta_target': core.hx(target),
            'peer_match_kind': 'DIRECT_QMETA_TARGET' if target == peer else 'FIRST_UNCONDITIONAL_TAIL_TRANSFER',
            'tail_target': core.hx(tail),
        })
    return out


def aligned_rip_refs(img: core.Image, target: int) -> list[tuple[int, tuple[int, int]]]:
    refs = []
    seen = set()
    for site in qmeta.rip_refs(img, target):
        fde = img.fde(site)
        if not fde or fde in seen:
            continue
        instructions = img.instructions(fde)
        exact = [row for row in instructions if row.address == site and core.rip_target(row) == target]
        if len(exact) != 1:
            continue
        refs.append((site, fde))
        seen.add(fde)
    return refs


def connection_block(img: core.Image, adapter: int) -> dict:
    refs = aligned_rip_refs(img, adapter)
    if len(refs) != 1:
        return {
            'classification': 'UNKNOWN_ADAPTER_ALIGNED_OWNER_COUNT',
            'aligned_owner_count': len(refs),
            'aligned_owners': [
                {'site': core.hx(site), 'fde': [core.hx(fde[0]), core.hx(fde[1])]}
                for site, fde in refs
            ],
        }
    site, fde = refs[0]
    instructions = img.instructions(fde)
    indexes = [i for i, row in enumerate(instructions) if row.address == site]
    if len(indexes) != 1:
        return {'classification': 'UNKNOWN_ADAPTER_SITE_ALIGNMENT'}
    index = indexes[0]

    forward = instructions[index:min(len(instructions), index + 20)]
    helper = None
    helper_index = None
    peer_candidates = []
    for offset, row in enumerate(forward):
        if offset > 0 and row.mnemonic == 'call' and row.operands and row.operands[0].type == core.X86_OP_IMM:
            helper = int(row.operands[0].imm)
            helper_index = index + offset
            break
        if row.mnemonic == 'lea':
            target = core.rip_target(row)
            if target is not None and target != adapter and img.executable(target):
                peer_candidates.append((row.address, target))
    peers = sorted({target for _site, target in peer_candidates})
    if helper is None or helper_index is None or len(peers) != 1:
        return {
            'classification': 'UNKNOWN_CONNECTION_BLOCK_SHAPE',
            'owner_fde': [core.hx(fde[0]), core.hx(fde[1])],
            'adapter_reference_site': core.hx(site),
            'peer_candidates': [core.hx(value) for value in peers],
            'helper_target': core.hx(helper),
        }
    peer = peers[0]

    arg_stores = []
    for row in instructions[index:helper_index]:
        if row.mnemonic != 'mov' or len(row.operands) < 2:
            continue
        dst, src = row.operands[0], row.operands[1]
        if dst.type != core.X86_OP_MEM or dst.mem.base != core.X86_REG_RSP or src.type != core.X86_OP_REG:
            continue
        arg_stores.append((row.address, int(dst.mem.disp), src.reg))

    endpoint_rows = []
    scan_start = max(0, index - 24)
    for row in instructions[scan_start:index]:
        if row.mnemonic != 'mov' or len(row.operands) < 2:
            continue
        dst, src = row.operands[0], row.operands[1]
        if dst.type != core.X86_OP_REG or src.type != core.X86_OP_MEM or not src.mem.base:
            continue
        matching_stores = [x for x in arg_stores if x[2] == dst.reg]
        if not matching_stores:
            continue
        endpoint_rows.append({
            'load_site': core.hx(row.address),
            'object_base_register': img.md.reg_name(src.mem.base),
            'object_field_displacement': hex(int(src.mem.disp)),
            'loaded_register': img.md.reg_name(dst.reg),
            'stack_argument_stores': [
                {'site': core.hx(store_site), 'stack_displacement': hex(stack_disp)}
                for store_site, stack_disp, _reg in matching_stores
            ],
        })

    unique_endpoints = {
        (row['object_base_register'], row['object_field_displacement']): row
        for row in endpoint_rows
    }
    endpoints = [unique_endpoints[key] for key in sorted(unique_endpoints)]
    common_bases = {row['object_base_register'] for row in endpoints}
    if len(endpoints) != 2 or len(common_bases) != 1:
        block_class = 'UNKNOWN_ENDPOINT_PAIR'
    else:
        block_class = 'UNIQUE_PAIRED_CALLABLE_CONNECTION_BLOCK'

    return {
        'classification': block_class,
        'owner_fde': [core.hx(fde[0]), core.hx(fde[1])],
        'adapter_reference_site': core.hx(site),
        'adapter_target': core.hx(adapter),
        'peer_target': core.hx(peer),
        'peer_reference_sites': [core.hx(peer_site) for peer_site, value in peer_candidates if value == peer],
        'connection_helper_target': core.hx(helper),
        'endpoint_object_fields': endpoints,
        'bounded_context': qmeta.bounded_context(instructions, site, before=16, after=24),
    }


def direct_calls(img: core.Image, fde: tuple[int, int]) -> list[int]:
    out = []
    for row in img.instructions(fde):
        if row.mnemonic == 'call' and row.operands and row.operands[0].type == core.X86_OP_IMM:
            target = int(row.operands[0].imm)
            if img.executable(target):
                out.append(target)
    return out


def bounded_root_reachability(img: core.Image, result: dict, target: int) -> dict:
    roots = []
    for name in ('connectClientToGameserverWithExistingCredentials', 'onConnectClientToGameserver'):
        row = (result.get('game_client_qmeta') or {}).get(name) or {}
        fde = row.get('fde')
        if isinstance(fde, list) and len(fde) == 2:
            roots.append((name, (int(fde[0], 16), int(fde[1], 16))))
    frontier = deque((name, fde, 0) for name, fde in roots)
    seen = {fde for _name, fde in roots}
    hits = []
    while frontier:
        root_name, fde, depth = frontier.popleft()
        for call_target in direct_calls(img, fde):
            if call_target == target:
                hits.append({'root': root_name, 'caller_fde': [core.hx(fde[0]), core.hx(fde[1])], 'depth': depth})
            if depth >= 2:
                continue
            next_fde = img.fde(call_target)
            if next_fde is None or next_fde in seen or next_fde[1] - next_fde[0] > 0x8000:
                continue
            seen.add(next_fde)
            frontier.append((root_name, next_fde, depth + 1))
    return {
        'classification': 'REACHABLE_FROM_GAMECLIENT_CONNECT_ROOT' if hits else 'UNKNOWN_NO_DIRECT_BOUNDED_REACHABILITY',
        'max_depth': 2,
        'hits': hits,
    }


def add_sendlogin_connection(client: Path, output: Path) -> None:
    result = json.loads(output.read_text(encoding='utf-8'))
    img = core.Image(client)
    actual_sha = hashlib.sha256(img.raw).hexdigest()
    if actual_sha != EXPECTED_SHA256 or len(img.raw) != EXPECTED_SIZE:
        raise RuntimeError('EXACT_CURRENT_CLIENT_FENCE_MISMATCH')
    exact = result.get('exact_client') or {}
    if exact.get('sha256') != EXPECTED_SHA256 or exact.get('size') != EXPECTED_SIZE:
        raise RuntimeError('RESULT_EXACT_CURRENT_CLIENT_FENCE_MISMATCH')
    if result.get('runtime_access') != 'none' or result.get('login_performed') is not False or result.get('secret_access') is not False:
        raise RuntimeError('SOURCE_ONLY_SAFETY_CONTRACT_MISMATCH')

    adapter_text = (result.get('sendlogin_adapter_binding') or {}).get('adapter_target')
    if not isinstance(adapter_text, str):
        raise RuntimeError('SENDLOGIN_ADAPTER_TARGET_MISSING')
    adapter = int(adapter_text, 16)
    block = connection_block(img, adapter)
    peer_text = block.get('peer_target')
    peer = int(peer_text, 16) if isinstance(peer_text, str) else None

    game_client = exact_full_qmeta(
        img,
        'tibia::client::TGameClient',
        ('connectClientToGameserverWithExistingCredentials', 'onConnectClientToGameserver'),
    )
    peer_candidates = qmeta_target_candidates(img, game_client, peer) if peer is not None else []

    queue = exact_full_qmeta(
        img,
        'tibia::protocol::TProtocolMessageQueue',
        ('sendLogin', 'sendEnterWorld', 'receivedLoginSuccessMessage'),
    )
    sendlogin_rows = [row for row in queue['rows'] if row['name'] == 'sendLogin']
    if len(sendlogin_rows) != 1:
        raise RuntimeError(f'SENDLOGIN_QMETA_ROW_AMBIGUOUS:{len(sendlogin_rows)}')
    sendlogin_role = sendlogin_rows[0]['role']

    peer_unique = len(peer_candidates) == 1
    peer_role = peer_candidates[0]['role'] if peer_unique else 'UNKNOWN'
    complementary_roles = peer_unique and peer_role == 'SIGNAL' and sendlogin_role == 'NON_SIGNAL_METHOD'
    structural_connection = block.get('classification') == 'UNIQUE_PAIRED_CALLABLE_CONNECTION_BLOCK'
    causal_binding_proven = structural_connection and complementary_roles

    reachability = {'classification': 'UNKNOWN_PEER_QMETA_IDENTITY', 'max_depth': 2, 'hits': []}
    if peer_unique:
        reachability = bounded_root_reachability(img, result, int(peer_candidates[0]['qmeta_target'], 16))

    if causal_binding_proven and reachability['classification'] == 'REACHABLE_FROM_GAMECLIENT_CONNECT_ROOT':
        status = 'PROVEN_GAMECLIENT_SIGNAL_TO_SENDLOGIN_ON_CONNECT_PATH'
    elif causal_binding_proven:
        status = 'PROVEN_QT_SIGNAL_TO_SENDLOGIN_CONNECTION_ROOT_PATH_UNKNOWN'
    elif peer_unique:
        status = 'PEER_QMETA_IDENTIFIED_CAUSAL_DIRECTION_UNKNOWN'
    else:
        status = 'UNKNOWN'

    result['sendlogin_connection_binding'] = {
        'classification': 'SENDLOGIN_CONNECTION_BINDING',
        'binding_status': status,
        'connection_block': block,
        'peer_qmeta_candidates': peer_candidates,
        'peer_qmeta_unique': peer_unique,
        'peer_qmeta_role': peer_role,
        'sendlogin_qmeta_role': sendlogin_role,
        'causal_binding_proven': causal_binding_proven,
        'bounded_gameclient_root_reachability': reachability,
        'classification_boundary': (
            'CONNECTION_PAIR_PROVES_SIGNAL_TO_SENDLOGIN_ONLY_WHEN_CURRENT_QMETA_ROLES_ARE_UNIQUE; '
            'BOUNDED_ROOT_REACHABILITY_IS_REPORTED_SEPARATELY'
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('SENDLOGIN_CONNECTION_BINDING=PASS')
    print('SENDLOGIN_CONNECTION_BINDING_STATUS=' + status)
    print('SENDLOGIN_CONNECTION_PEER_QMETA_COUNT=' + str(len(peer_candidates)))
    print('SENDLOGIN_CONNECTION_CAUSAL_BINDING=' + ('true' if causal_binding_proven else 'false'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    add_sendlogin_connection(args.client, args.output)
