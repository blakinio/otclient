#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import probe as core
import qmeta_runner as qmeta

EXPECTED_SHA256 = '552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'
EXPECTED_SIZE = 52105824


def direct_dispatch_candidates(img: core.Image, target: int) -> dict:
    fde = img.fde(target)
    if not fde:
        return {
            'classification': 'UNKNOWN_QMETA_TARGET_FDE',
            'qmeta_target_fde': None,
            'instructions': [],
            'candidates': [],
        }
    instructions = img.instructions(fde)
    indexes = [i for i, row in enumerate(instructions) if row.address == target]
    if len(indexes) != 1:
        return {
            'classification': 'UNKNOWN_QMETA_TARGET_ALIGNMENT',
            'qmeta_target_fde': [core.hx(fde[0]), core.hx(fde[1])],
            'instructions': [],
            'candidates': [],
        }
    start = indexes[0]
    window = []
    candidates = []
    for row in instructions[start:start + 28]:
        if row.address > target + 0x90:
            break
        window.append({'at': core.hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str})
        if row.mnemonic in ('call', 'jmp') and row.operands and row.operands[0].type == core.X86_OP_IMM:
            branch_target = int(row.operands[0].imm)
            if img.executable(branch_target) and not (fde[0] <= branch_target < fde[1]):
                branch_fde = img.fde(branch_target)
                candidates.append({
                    'site': core.hx(row.address),
                    'mnemonic': row.mnemonic,
                    'target': core.hx(branch_target),
                    'target_fde': ([core.hx(branch_fde[0]), core.hx(branch_fde[1])] if branch_fde else None),
                })
        if row.mnemonic.startswith('ret'):
            break
        if row.mnemonic == 'jmp' and row.operands and row.operands[0].type == core.X86_OP_IMM:
            branch_target = int(row.operands[0].imm)
            if fde[0] <= branch_target < fde[1]:
                break
    unique_targets = sorted({int(row['target'], 16) for row in candidates})
    if len(unique_targets) == 1:
        classification = 'UNIQUE_EXTERNAL_DIRECT_TRANSFER'
    elif unique_targets:
        classification = 'UNKNOWN_MULTIPLE_EXTERNAL_DIRECT_TRANSFERS'
    else:
        classification = 'UNKNOWN_NO_EXTERNAL_DIRECT_TRANSFER'
    return {
        'classification': classification,
        'qmeta_target_fde': [core.hx(fde[0]), core.hx(fde[1])],
        'instructions': window,
        'candidates': candidates,
    }


def reference_owners(img: core.Image, sites: list[int]) -> list[dict]:
    owners = []
    for site in sites:
        fde = img.fde(site)
        owners.append({
            'site': core.hx(site),
            'fde': ([core.hx(fde[0]), core.hx(fde[1])] if fde else None),
        })
    return owners


def reference_contexts(img: core.Image, kind: str, sites: list[int]) -> list[dict]:
    rows = []
    for site in sites:
        fde = img.fde(site)
        if not fde:
            continue
        instructions = img.instructions(fde)
        try:
            context = qmeta.bounded_context(instructions, site, before=14, after=14)
        except RuntimeError:
            continue
        rows.append({
            'kind': kind,
            'site': core.hx(site),
            'fde': [core.hx(fde[0]), core.hx(fde[1])],
            'instructions': context,
        })
    return rows


def add_sendlogin_binding(client: Path, output: Path) -> None:
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

    send_login = (result.get('queue_qmeta') or {}).get('sendLogin') or {}
    target_text = send_login.get('target')
    if not isinstance(target_text, str):
        raise RuntimeError('SENDLOGIN_QMETA_TARGET_MISSING')
    qmeta_target = int(target_text, 16)
    dispatch = direct_dispatch_candidates(img, qmeta_target)
    unique_targets = sorted({int(row['target'], 16) for row in dispatch['candidates']})
    adapter = unique_targets[0] if len(unique_targets) == 1 else None

    direct_call_refs = qmeta.direct_call_refs(img, adapter) if adapter is not None else []
    rip_refs = qmeta.rip_refs(img, adapter) if adapter is not None else []
    all_refs = sorted(set(direct_call_refs + rip_refs))
    binding_status = 'UNIQUE_ADAPTER_DISCOVERED' if adapter is not None else 'UNKNOWN'

    result['sendlogin_adapter_binding'] = {
        'classification': 'SENDLOGIN_ADAPTER_BINDING',
        'binding_status': binding_status,
        'qmeta_sendlogin_target': core.hx(qmeta_target),
        'qmeta_dispatch': dispatch,
        'adapter_target': core.hx(adapter),
        'adapter_fde': ([core.hx(x) for x in img.fde(adapter)] if adapter is not None and img.fde(adapter) else None),
        'direct_call_refs': [core.hx(site) for site in direct_call_refs],
        'rip_refs': [core.hx(site) for site in rip_refs],
        'reference_owners': reference_owners(img, all_refs),
        'reference_contexts': (
            reference_contexts(img, 'DIRECT_CALL', direct_call_refs)
            + reference_contexts(img, 'RIP_REFERENCE', rip_refs)
        ),
        'causal_binding_proven': False,
        'classification_boundary': 'ADAPTER_XREFS_DO_NOT_BY_THEMSELVES_PROVE_PRE_LOGIN_ORDER',
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('SENDLOGIN_ADAPTER_BINDING=PASS')
    print('SENDLOGIN_ADAPTER_BINDING_STATUS=' + binding_status)
    print('SENDLOGIN_ADAPTER_XREF_COUNT=' + str(len(all_refs)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    add_sendlogin_binding(args.client, args.output)
