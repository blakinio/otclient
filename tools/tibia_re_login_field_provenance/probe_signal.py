#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from capstone.x86_const import X86_OP_IMM

import probe_qmeta as core


def hx(v: int) -> str:
    return f'0x{v:x}'


def calls_in_snapshot(img: core.Image, va: int, limit: int = 3000) -> list[dict]:
    fde = img.fde(va)
    if not fde:
        return []
    out = []
    for ins in list(img.md.disasm(img.bytes(fde[0], fde[1] - fde[0]), fde[0]))[:limit]:
        if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
            target = int(ins.operands[0].imm)
            out.append({
                'site': hx(ins.address),
                'target': hx(target),
                'target_snapshot': img.snapshot(target, 120) if img.executable(target) else None,
            })
    return out


def direct_callers(img: core.Image, targets: set[int]) -> dict[int, list[int]]:
    out = {t: [] for t in targets}
    for sec in img.sections:
        if not (sec.flags & 4):
            continue
        for ins in img.md.disasm(img.raw[sec.offset:sec.offset + sec.size], sec.va):
            if ins.mnemonic != 'call' or not ins.operands or ins.operands[0].type != X86_OP_IMM:
                continue
            t = int(ins.operands[0].imm)
            if t in out:
                out[t].append(ins.address)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    img = core.Image(args.client)

    rows = core.meta_for_method(img, 'requestCharacterLogin')
    controller = [r for r in rows if r.get('class_name') == 'tibia::gamewindow::TCharacterSelectionController']
    if len(controller) != 1:
        raise SystemExit(f'CHARACTER_SELECTION_QMETA_AMBIGUOUS={len(controller)}')
    meta = controller[0]
    method_rows = [r for r in meta['rows'] if r['name'] == 'requestCharacterLogin']
    if len(method_rows) != 1:
        raise SystemExit(f'REQUEST_CHARACTER_LOGIN_METHOD_AMBIGUOUS={len(method_rows)}')
    static_rows = meta.get('static') or []
    if len(static_rows) != 1:
        raise SystemExit(f'CHARACTER_SELECTION_STATIC_METACALL_AMBIGUOUS={len(static_rows)}')
    static_metacall = int(static_rows[0]['static_metacall'], 16)
    static_snapshot = img.snapshot(static_metacall, 3000)
    calls = calls_in_snapshot(img, static_metacall)
    targets = {int(c['target'], 16) for c in calls if c.get('target_snapshot')}
    callers = direct_callers(img, targets)

    target_rows = []
    for target in sorted(targets):
        sites = callers[target]
        target_rows.append({
            'target': hx(target),
            'target_fde': img.snapshot(target, 800),
            'direct_callers': [
                {
                    'site': hx(site),
                    'fde': [hx(x) for x in img.fde(site)] if img.fde(site) else None,
                    'context': core.context(img, site, 16, 16),
                }
                for site in sites[:200]
            ],
        })

    result = {
        'schema': 'otclient.track-a.current-game-login-field-provenance.character-signal.v1',
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'qmeta': {
            'class_name': meta['class_name'],
            'stringdata': meta['stringdata'],
            'metadata': meta['metadata'],
            'method': method_rows[0],
            'static': static_rows[0],
        },
        'static_metacall_snapshot': static_snapshot,
        'static_metacall_direct_calls': calls,
        'direct_call_targets_and_callers': target_rows,
        'classification': {
            'request_payload_type': 'tibia::authentication::TCharacterLoginData',
            'field_semantics': 'UNKNOWN',
            'password_session_to_rsa_field_mapping': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_CHARACTER_LOGIN_SIGNAL_PROVENANCE=PASS')
    print('QMETA_CLASS=' + meta['class_name'])
    print('QMETA_METHOD=requestCharacterLogin')
    print('QMETA_STATIC_METACALL=' + hx(static_metacall))
    print('STATIC_DIRECT_CALL_COUNT=' + str(len(calls)))
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
