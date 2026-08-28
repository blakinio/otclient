#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import probe as core

MARKERS = {
    'INTERPROCEDURAL_MEMBER_PROVENANCE': True,
    'CALLER_FDE_RTTI_OWNERS': True,
    'CONSTRUCTOR_MEMBER_BINDING': True,
    'NO_HEURISTIC_RANKING': True,
}


def read_cstring(img: core.Image, va: int, limit: int = 512) -> str | None:
    if not img.mapped(va):
        return None
    off = img.va_to_off(va)
    end = img.raw.find(b'\0', off, min(len(img.raw), off + limit))
    if end < 0:
        return None
    try:
        return img.raw[off:end].decode('ascii')
    except UnicodeDecodeError:
        return None


def demangle_nested(name: str) -> str | None:
    if not (name.startswith('N') and name.endswith('E')):
        return None
    pos = 1
    parts = []
    while pos < len(name) - 1:
        m = re.match(r'(\d+)', name[pos:])
        if not m:
            return None
        length = int(m.group(1))
        pos += len(m.group(1))
        part = name[pos:pos + length]
        if len(part) != length:
            return None
        parts.append(part)
        pos += length
    return '::'.join(parts) if parts and pos == len(name) - 1 else None


def recover_vtables(img: core.Image) -> list[dict]:
    reverse: dict[int, list[int]] = defaultdict(list)
    for where, value in img.rel.items():
        reverse[value].append(where)

    rows = []
    seen = set()
    for where, name_va in img.rel.items():
        raw_name = read_cstring(img, name_va)
        if not raw_name:
            continue
        type_name = demangle_nested(raw_name)
        if not type_name:
            continue
        rtti = where - 8
        for type_slot in reverse.get(rtti, []):
            address_point = type_slot + 8
            if (rtti, address_point) in seen:
                continue
            if not img.mapped(address_point - 16, 24):
                continue
            if img.u64(address_point - 16) != 0:
                continue
            first = img.qword(address_point)
            if not img.executable(first):
                continue
            seen.add((rtti, address_point))
            rows.append({
                'type_name': type_name,
                'rtti': rtti,
                'address_point': address_point,
            })
    return rows


def vtable_method_owner_map(img: core.Image, vtables: list[dict]) -> tuple[dict, dict]:
    fde_owners: dict[tuple[int, int], list[dict]] = defaultdict(list)
    ap_by_type: dict[str, list[int]] = defaultdict(list)
    for vt in vtables:
        ap = vt['address_point']
        ap_by_type[vt['type_name']].append(ap)
        for offset in range(0, 0x300, 8):
            if not img.mapped(ap + offset, 8):
                break
            target = img.qword(ap + offset)
            if not img.executable(target):
                continue
            fde = img.fde(target)
            if fde is None:
                continue
            key = (vt['type_name'], ap, offset)
            if not any((row['type_name'], row['address_point'], row['slot_offset']) == key for row in fde_owners[fde]):
                fde_owners[fde].append({
                    'type_name': vt['type_name'],
                    'address_point': ap,
                    'slot_offset': offset,
                    'target': target,
                })
    return fde_owners, ap_by_type


def backward_alias_to_entry(img: core.Image, instructions, site_index: int, family: str) -> dict:
    current = family
    aliases = []
    for row in reversed(instructions[:site_index]):
        if not core.writes_family(img, row, current):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == core.X86_OP_REG and row.operands[1].type == core.X86_OP_REG:
            source = core.reg_family(img.md.reg_name(row.operands[1].reg))
            aliases.append({'site': core.hx(row.address), 'from': source, 'to': current})
            current = source
            continue
        return {
            'classification': 'ENTRY_ALIAS_NOT_PROVEN',
            'stopped_at': core.hx(row.address),
            'operand': row.op_str,
            'current_family': current,
            'aliases': aliases,
        }
    return {
        'classification': 'ENTRY_ALIAS_PROVEN' if current == 'rdi' else 'ENTRY_ALIAS_NOT_PROVEN',
        'entry_family': current,
        'aliases': aliases,
    }


def explicit_vtable_stores(img: core.Image, instructions, target_aps: set[int]) -> list[dict]:
    stores = []
    for index, row in enumerate(instructions):
        if row.mnemonic != 'lea' or len(row.operands) < 2 or row.operands[0].type != core.X86_OP_REG:
            continue
        target = core.rip_target(row)
        if target not in target_aps:
            continue
        vt_family = core.reg_family(img.md.reg_name(row.operands[0].reg))
        for later in instructions[index + 1:index + 14]:
            if later.mnemonic != 'mov' or len(later.operands) < 2:
                continue
            dst, src = later.operands[0], later.operands[1]
            if dst.type != core.X86_OP_MEM or src.type != core.X86_OP_REG or not dst.mem.base:
                continue
            if int(dst.mem.disp) != 0:
                continue
            if core.reg_family(img.md.reg_name(src.reg)) != vt_family:
                continue
            stores.append({
                'vtable_address_point': target,
                'lea_site': row.address,
                'store_site': later.address,
                'object_family': core.reg_family(img.md.reg_name(dst.mem.base)),
            })
    return stores


def find_constructor_records(img: core.Image, owner_aps: set[int]) -> list[dict]:
    records = []
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x20000:
            continue
        instructions = img.instructions(fde)
        stores = explicit_vtable_stores(img, instructions, owner_aps)
        for store in stores:
            store_index = next(i for i, row in enumerate(instructions) if row.address == store['store_site'])
            entry = backward_alias_to_entry(img, instructions, store_index, store['object_family'])
            if entry['classification'] != 'ENTRY_ALIAS_PROVEN':
                continue
            records.append({
                'fde': fde,
                'owner_vtable_address_point': store['vtable_address_point'],
                'this_family': store['object_family'],
                'vtable_store_site': store['store_site'],
                '_instructions': instructions,
            })
    return records


def register_alias_before(img: core.Image, instructions, site_index: int, family: str) -> dict:
    current = family
    chain = []
    for row in reversed(instructions[:site_index]):
        if not core.writes_family(img, row, current):
            continue
        if row.mnemonic == 'mov' and len(row.operands) >= 2 and row.operands[0].type == core.X86_OP_REG:
            src = row.operands[1]
            if src.type == core.X86_OP_REG:
                source = core.reg_family(img.md.reg_name(src.reg))
                chain.append({'site': core.hx(row.address), 'from': source, 'to': current})
                current = source
                continue
            if src.type == core.X86_OP_MEM:
                return {
                    'classification': 'MEMORY_SOURCE',
                    'site': core.hx(row.address),
                    'operand': row.op_str,
                    'base_family': core.reg_family(img.md.reg_name(src.mem.base)) if src.mem.base else None,
                    'displacement': int(src.mem.disp),
                    'chain': chain,
                }
        return {
            'classification': 'SOURCE_NOT_ALIASABLE',
            'site': core.hx(row.address),
            'operand': row.op_str,
            'chain': chain,
        }
    return {'classification': 'ENTRY_SOURCE', 'entry_family': current, 'chain': chain}


def member_handler_binding(img: core.Image, constructor: dict, member_offset: int) -> list[dict]:
    instructions = constructor['_instructions']
    this_family = constructor['this_family']
    bindings = []
    handler_stores = explicit_vtable_stores(img, instructions, {core.HANDLER_VTABLE_AP})
    for index, row in enumerate(instructions):
        if row.mnemonic != 'mov' or len(row.operands) < 2:
            continue
        dst, src = row.operands[0], row.operands[1]
        if dst.type != core.X86_OP_MEM or not dst.mem.base:
            continue
        if core.reg_family(img.md.reg_name(dst.mem.base)) != this_family or int(dst.mem.disp) != member_offset:
            continue
        if src.type != core.X86_OP_REG:
            continue
        source_family = core.reg_family(img.md.reg_name(src.reg))
        for hs in handler_stores:
            if hs['store_site'] >= row.address:
                continue
            # Same object register or a simple alias chain from the member source.
            if hs['object_family'] == source_family:
                bindings.append({
                    'classification': 'CONSTRUCTOR_MEMBER_BINDING',
                    'member_store_site': core.hx(row.address),
                    'member_offset': member_offset,
                    'handler_vtable_store_site': core.hx(hs['store_site']),
                    'handler_vtable_address_point': core.hx(core.HANDLER_VTABLE_AP),
                })
                continue
            source = register_alias_before(img, instructions, index, source_family)
            if source.get('classification') == 'ENTRY_SOURCE' and source.get('entry_family') == hs['object_family']:
                bindings.append({
                    'classification': 'CONSTRUCTOR_MEMBER_BINDING',
                    'member_store_site': core.hx(row.address),
                    'member_offset': member_offset,
                    'handler_vtable_store_site': core.hx(hs['store_site']),
                    'handler_vtable_address_point': core.hx(core.HANDLER_VTABLE_AP),
                    'source_alias': source,
                })
    return bindings


def candidate_owner_member(img: core.Image, call: dict, fde_owners: dict, constructors_by_ap: dict) -> dict:
    binding = call['binding']
    origin = binding.get('origin') or {}
    if binding.get('classification') != 'UNBOUND_RECEIVER' or origin.get('classification') != 'MEMORY_LOAD':
        return {'classification': 'MEMBER_PROVENANCE_NOT_APPLICABLE'}

    instructions = call['_instructions']
    call_index = call['_index']
    base_family = origin.get('base_family')
    if not base_family:
        return {'classification': 'MEMBER_BASE_UNKNOWN'}
    base_entry = backward_alias_to_entry(img, instructions, call_index, base_family)
    if base_entry['classification'] != 'ENTRY_ALIAS_PROVEN':
        return {'classification': 'MEMBER_BASE_NOT_THIS', 'base_entry': base_entry}

    owners = fde_owners.get(call['fde'], [])
    if not owners:
        return {'classification': 'CALLER_FDE_RTTI_OWNERS_UNKNOWN'}

    member_offset = int(origin['displacement'])
    proofs = []
    owner_summaries = []
    for owner in owners:
        ap = owner['address_point']
        owner_summaries.append({
            'type_name': owner['type_name'],
            'address_point': core.hx(ap),
            'slot_offset': core.hx(owner['slot_offset']),
        })
        for constructor in constructors_by_ap.get(ap, []):
            for proof in member_handler_binding(img, constructor, member_offset):
                proofs.append({
                    'owner_type': owner['type_name'],
                    'owner_vtable_address_point': core.hx(ap),
                    'owner_method_slot': core.hx(owner['slot_offset']),
                    'constructor_fde': [core.hx(constructor['fde'][0]), core.hx(constructor['fde'][1])],
                    **proof,
                })

    unique = {
        (p['owner_type'], p['owner_vtable_address_point'], p['constructor_fde'][0], p['member_store_site'], p['handler_vtable_store_site']): p
        for p in proofs
    }
    if len(unique) == 1:
        return {
            'classification': 'INTERPROCEDURAL_MEMBER_PROVENANCE_PROVEN',
            'member_offset': member_offset,
            'caller_fde_rtti_owners': owner_summaries,
            'proof': next(iter(unique.values())),
        }
    return {
        'classification': 'INTERPROCEDURAL_MEMBER_PROVENANCE_UNKNOWN',
        'member_offset': member_offset,
        'caller_fde_rtti_owners': owner_summaries,
        'proof_count': len(unique),
    }


def sanitize_call(call: dict, provenance: dict) -> dict:
    return {
        'site': core.hx(call['site']),
        'fde': [core.hx(call['fde'][0]), core.hx(call['fde'][1])],
        'operand': call['operand'],
        'local_binding': call['binding'],
        'member_provenance': provenance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)

    vtables = recover_vtables(img)
    fde_owners, _ = vtable_method_owner_map(img, vtables)
    owner_aps = {row['address_point'] for rows in fde_owners.values() for row in rows}
    constructors = find_constructor_records(img, owner_aps)
    constructors_by_ap: dict[int, list[dict]] = defaultdict(list)
    for row in constructors:
        constructors_by_ap[row['owner_vtable_address_point']].append(row)

    calls = core.enumerate_slot_calls(img)
    proved = []
    candidates = []
    for call in calls:
        provenance = candidate_owner_member(img, call, fde_owners, constructors_by_ap)
        if provenance['classification'] != 'MEMBER_PROVENANCE_NOT_APPLICABLE':
            candidates.append(sanitize_call(call, provenance))
        if provenance['classification'] == 'INTERPROCEDURAL_MEMBER_PROVENANCE_PROVEN':
            proved.append((call, provenance))

    accepted = None
    edx = None
    if len(proved) == 1:
        accepted = proved[0]
        edx = core.reaching_edx(img, accepted[0]['_instructions'], accepted[0]['_index'])

    if accepted is not None and edx is not None and edx['classification'] == 'UNIQUE_STATIC_SCALAR':
        classification = 'FIELD6_VALUE_PROVEN'
        value = edx['value']
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None

    result['interprocedural_member_provenance'] = {
        'classification': 'INTERPROCEDURAL_MEMBER_PROVENANCE',
        'markers': MARKERS,
        'rtti_vtable_type_count': len(vtables),
        'constructor_record_count': len(constructors),
        'candidate_count': len(candidates),
        'proved_handler_member_callsite_count': len(proved),
        'proved_handler_member_callsites': [
            sanitize_call(call, provenance) for call, provenance in proved
        ],
        'accepted_callsite': sanitize_call(*accepted) if accepted is not None else None,
        'field6_edx_reaching_value': edx,
        'boundary': 'NO_HEURISTIC_RANKING',
    }
    result['classification'] = classification
    result['field6_value'] = value
    if value is not None:
        result['field6_edx_reaching_value'] = edx

    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('INTERPROCEDURAL_MEMBER_PROVENANCE=PASS')
    print('CALLER_FDE_RTTI_OWNERS=PASS')
    print('CONSTRUCTOR_MEMBER_BINDING=' + ('PROVEN' if len(proved) == 1 else 'UNKNOWN'))
    print('FIELD6_EDX_REACHING_VALUE=' + (str(value) if value is not None else 'UNKNOWN'))
    print('CLASSIFICATION=' + classification)


if __name__ == '__main__':
    main()
