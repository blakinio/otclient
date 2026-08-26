#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from capstone.x86_const import X86_OP_IMM

import probe_qmeta as core


def hx(v: int) -> str:
    return f'0x{v:x}'


def direct_callers(img: core.Image, target: int) -> list[int]:
    out = []
    for sec in img.sections:
        if not (sec.flags & 4):
            continue
        for ins in img.md.disasm(img.raw[sec.offset:sec.offset + sec.size], sec.va):
            if ins.mnemonic == 'call' and ins.operands and ins.operands[0].type == X86_OP_IMM:
                if int(ins.operands[0].imm) == target:
                    out.append(ins.address)
    return sorted(set(out))


def rtti_name(img: core.Image, rtti: int) -> str | None:
    name_va = img.rel.get(rtti + 8)
    if name_va is None:
        return None
    return core.safe_cstr(img, name_va, 512)


def vtable_owners_for_target(img: core.Image, target: int) -> list[dict]:
    rows = []
    for slot_addr, addend in img.rel.items():
        if addend != target:
            continue
        for off in range(0, 0x300, 8):
            ap = slot_addr - off
            if not img.mapped(ap - 16, 24):
                continue
            try:
                offset_to_top = img.u64(ap - 16)
            except Exception:
                continue
            typeinfo = img.rel.get(ap - 8)
            if typeinfo is None:
                continue
            name = rtti_name(img, typeinfo)
            if not name or not name.startswith(('N', 'Z', 'S')):
                continue
            # A primary address point commonly has offset-to-top 0. Keep nonzero
            # candidates too, but expose the value rather than silently assuming.
            rows.append({
                'slot_address': hx(slot_addr),
                'slot_offset': hex(off),
                'address_point': hx(ap),
                'offset_to_top_u64': hx(offset_to_top),
                'rtti': hx(typeinfo),
                'rtti_name': name,
            })
    uniq = {(r['slot_address'], r['address_point'], r['rtti']): r for r in rows}
    return sorted(uniq.values(), key=lambda r: (int(r['offset_to_top_u64'], 16) != 0, int(r['slot_offset'], 16), r['rtti_name']))


def reloc_owners_for_fde(img: core.Image, lo: int, hi: int) -> list[dict]:
    rows = []
    for where, addend in img.rel.items():
        if not (lo <= addend < hi):
            continue
        name_candidates = []
        for off in range(0, 0x300, 8):
            ap = where - off
            if not img.mapped(ap - 16, 24):
                continue
            typeinfo = img.rel.get(ap - 8)
            if typeinfo is None:
                continue
            name = rtti_name(img, typeinfo)
            if name:
                name_candidates.append({
                    'address_point': hx(ap),
                    'slot_offset': hex(off),
                    'rtti': hx(typeinfo),
                    'rtti_name': name,
                })
        rows.append({'relocation': hx(where), 'target': hx(addend), 'owners': name_candidates[:32]})
    return rows[:300]


def string_neighborhood(img: core.Image, needle: str, radius: int = 0x1800) -> list[dict]:
    rows = []
    for va in img.occ(needle)[:16]:
        off = img.va_to_off(va)
        lo = max(0, off - radius)
        hi = min(len(img.raw), off + radius)
        vals = []
        for m in re.finditer(rb'[ -~]{3,180}\x00', img.raw[lo:hi]):
            text = m.group(0)[:-1].decode('ascii', 'ignore')
            sva = img.off_to_va(lo + m.start())
            if sva is not None:
                vals.append({'va': hx(sva), 'text': text})
        rows.append({'occurrence': hx(va), 'strings': vals[:240]})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    img = core.Image(args.client)
    handler = core.exact_vtable(
        img, 'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler')
    auth = core.exact_vtable(
        img, 'TAuthenticationAndEncryptionInfo',
        'tibia::authentication::TAuthenticationAndEncryptionInfo')

    population = 0xe27110
    population_fde = img.fde(population)
    if population_fde != (0xe27110, 0xe284b4):
        raise SystemExit(f'CURRENT_POPULATION_FDE_MOVED={population_fde!r}')
    callers = direct_callers(img, population)
    if callers != [0x7d86f8]:
        raise SystemExit('CURRENT_POPULATION_CALLER_SET_MOVED=' + ','.join(hx(x) for x in callers))
    caller_site = callers[0]
    caller_fde = img.fde(caller_site)
    if caller_fde != (0x7d86a0, 0x7d87a2):
        raise SystemExit(f'CURRENT_POPULATION_CALLER_FDE_MOVED={caller_fde!r}')

    owners = vtable_owners_for_target(img, caller_fde[0])
    owner_names = sorted({r['rtti_name'] for r in owners})
    neighborhoods = {}
    for name in owner_names:
        # Itanium nested names still contain simple identifiers in clear text.
        parts = re.findall(r'[A-Za-z_][A-Za-z0-9_]{3,}', name)
        for part in parts[-4:]:
            if part.startswith(('tibia', 'std', 'QObject')):
                continue
            if part not in neighborhoods:
                neighborhoods[part] = string_neighborhood(img, part)

    result = {
        'schema': 'otclient.track-a.current-game-login-field-provenance.owner.v1',
        'runtime_access': 'none',
        'login_performed': False,
        'secret_access': False,
        'raw_client_uploaded': False,
        'exact_current_anchors': {
            'auth_rtti': auth['rtti'],
            'auth_address_point': auth['address_point'],
            'handler_rtti': handler['rtti'],
            'handler_address_point': handler['address_point'],
            'population_fde': [hx(population_fde[0]), hx(population_fde[1])],
            'population_direct_callers': [hx(x) for x in callers],
            'caller_fde': [hx(caller_fde[0]), hx(caller_fde[1])],
        },
        'caller_full_snapshot': img.snapshot(caller_fde[0], 1200),
        'caller_vtable_owners': owners,
        'caller_fde_relocation_owners': reloc_owners_for_fde(img, caller_fde[0], caller_fde[1]),
        'owner_name_neighborhoods': neighborhoods,
        'population_literal_neighborhoods': {
            'Request connection to gameserver ': string_neighborhood(img, 'Request connection to gameserver '),
            ' requested (Charakter': string_neighborhood(img, ' requested (Charakter'),
            'TPlaySessionData': string_neighborhood(img, 'TPlaySessionData'),
            'PlaySessionData': string_neighborhood(img, 'PlaySessionData'),
        },
        'classification': {
            'caller_owner_type': 'DISCOVERY_ONLY',
            'source_object_type': 'UNKNOWN',
            'user_facing_semantic_field_names': 'UNKNOWN',
            'password_session_to_rsa_field_mapping': 'UNKNOWN',
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CURRENT_GAME_LOGIN_POPULATION_OWNER_PROVENANCE=PASS')
    print('POPULATION_CALLER=' + hx(caller_site))
    print('POPULATION_CALLER_FDE=' + '..'.join(hx(x) for x in caller_fde))
    print('CALLER_VTABLE_OWNER_COUNT=' + str(len(owners)))
    for row in owners[:20]:
        print('CALLER_OWNER=' + row['rtti_name'] + '@' + row['rtti'])
    print('RAW_CLIENT_UPLOADED=false')
    print('LOGIN_PERFORMED=false')
    print('SECRET_ACCESS=false')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
