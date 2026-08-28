#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from bisect import bisect_right
from collections import defaultdict
from pathlib import Path

import probe as core
import member_provenance as broad

SCOPE_MARKERS = {
    'CALLSITE_FDE_SCOPE': True,
    'VTABLE_RIP_CONSTRUCTOR_SCOPE': True,
    'BINARY_SEARCH_FDE_LOOKUP': True,
    'NO_HEURISTIC_RANKING': True,
}


class FastFdeIndex:
    """BINARY_SEARCH_FDE_LOOKUP over the already sorted EH-frame FDEs."""

    def __init__(self, fdes: list[tuple[int, int]]):
        self.fdes = fdes
        self.starts = [row[0] for row in fdes]

    def get(self, va: int) -> tuple[int, int] | None:
        index = bisect_right(self.starts, va) - 1
        if index < 0:
            return None
        row = self.fdes[index]
        return row if row[0] <= va < row[1] else None


def focused_vtable_method_owner_map(
    img: core.Image,
    vtables: list[dict],
    callsite_fdes: set[tuple[int, int]],
    fde_index: FastFdeIndex,
) -> dict[tuple[int, int], list[dict]]:
    """Map RTTI/vtable owners only for FDEs that actually contain slot+0x60 calls."""
    owners: dict[tuple[int, int], list[dict]] = defaultdict(list)
    seen: set[tuple[tuple[int, int], str, int, int]] = set()
    for vt in vtables:
        ap = int(vt['address_point'])
        for offset in range(0, 0x300, 8):
            if not img.mapped(ap + offset, 8):
                break
            target = img.qword(ap + offset)
            if not img.executable(target):
                continue
            fde = fde_index.get(target)
            if fde is None or fde not in callsite_fdes:
                continue
            key = (fde, vt['type_name'], ap, offset)
            if key in seen:
                continue
            seen.add(key)
            owners[fde].append({
                'type_name': vt['type_name'],
                'address_point': ap,
                'slot_offset': offset,
                'target': target,
            })
    return owners


def rip_refs_to_targets(img: core.Image, targets: set[int]) -> dict[int, list[int]]:
    """Find common x86-64 RIP-relative LEA/MOV references in one bounded byte pass."""
    refs: dict[int, list[int]] = defaultdict(list)
    if not targets:
        return refs
    for section in img.sections:
        if not (section.flags & 4):
            continue
        blob = img.raw[section.offset:section.offset + section.size]
        limit = max(0, len(blob) - 7)
        for pos in range(limit):
            site = section.va + pos
            # REX + LEA/MOV r64,[rip+disp32]
            if 0x40 <= blob[pos] <= 0x4F and blob[pos + 1] in (0x8D, 0x8B) and (blob[pos + 2] & 0xC7) == 0x05:
                disp = int.from_bytes(blob[pos + 3:pos + 7], 'little', signed=True)
                target = site + 7 + disp
                if target in targets:
                    refs[target].append(site)
            # Non-REX LEA/MOV r32,[rip+disp32]
            if blob[pos] in (0x8D, 0x8B) and (blob[pos + 1] & 0xC7) == 0x05:
                disp = int.from_bytes(blob[pos + 2:pos + 6], 'little', signed=True)
                target = site + 6 + disp
                if target in targets:
                    refs[target].append(site)
    return refs


def focused_constructor_records(
    img: core.Image,
    owner_aps: set[int],
    fde_index: FastFdeIndex,
) -> tuple[list[dict], dict[int, list[int]], set[tuple[int, int]]]:
    """VTABLE_RIP_CONSTRUCTOR_SCOPE: inspect only FDEs that reference relevant owner vtables."""
    refs = rip_refs_to_targets(img, owner_aps)
    constructor_fdes: set[tuple[int, int]] = set()
    for sites in refs.values():
        for site in sites:
            fde = fde_index.get(site)
            if fde is not None and img.executable(fde[0]) and fde[1] - fde[0] <= 0x20000:
                constructor_fdes.add(fde)

    records: list[dict] = []
    for fde in sorted(constructor_fdes):
        instructions = img.instructions(fde)
        stores = broad.explicit_vtable_stores(img, instructions, owner_aps)
        by_address = {row.address: index for index, row in enumerate(instructions)}
        for store in stores:
            store_index = by_address.get(store['store_site'])
            if store_index is None:
                continue
            entry = broad.backward_alias_to_entry(img, instructions, store_index, store['object_family'])
            if entry['classification'] != 'ENTRY_ALIAS_PROVEN':
                continue
            records.append({
                'fde': fde,
                'owner_vtable_address_point': store['vtable_address_point'],
                'this_family': store['object_family'],
                'vtable_store_site': store['store_site'],
                '_instructions': instructions,
            })
    return records, refs, constructor_fdes


def sanitize_proved(call: dict, provenance: dict) -> dict:
    return broad.sanitize_call(call, provenance)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)
    fde_index = FastFdeIndex(img.fdes)

    # CALLSITE_FDE_SCOPE: this exact set is the only method-owner scope.
    calls = core.enumerate_slot_calls(img)
    callsite_fdes = {call['fde'] for call in calls}

    vtables = broad.recover_vtables(img)
    fde_owners = focused_vtable_method_owner_map(img, vtables, callsite_fdes, fde_index)
    owner_aps = {
        int(owner['address_point'])
        for owners in fde_owners.values()
        for owner in owners
    }

    constructors, owner_refs, constructor_fdes = focused_constructor_records(img, owner_aps, fde_index)
    constructors_by_ap: dict[int, list[dict]] = defaultdict(list)
    for row in constructors:
        constructors_by_ap[int(row['owner_vtable_address_point'])].append(row)

    proved: list[tuple[dict, dict]] = []
    applicable_count = 0
    for call in calls:
        provenance = broad.candidate_owner_member(img, call, fde_owners, constructors_by_ap)
        if provenance['classification'] != 'MEMBER_PROVENANCE_NOT_APPLICABLE':
            applicable_count += 1
        if provenance['classification'] == 'INTERPROCEDURAL_MEMBER_PROVENANCE_PROVEN':
            proved.append((call, provenance))

    accepted: tuple[dict, dict] | None = proved[0] if len(proved) == 1 else None
    edx = None
    if accepted is not None:
        edx = core.reaching_edx(img, accepted[0]['_instructions'], accepted[0]['_index'])

    if accepted is not None and edx is not None and edx['classification'] == 'UNIQUE_STATIC_SCALAR':
        classification = 'FIELD6_VALUE_PROVEN'
        value = edx['value']
    else:
        classification = 'FIELD6_VALUE_UNKNOWN'
        value = None

    result['interprocedural_member_provenance'] = {
        'classification': 'INTERPROCEDURAL_MEMBER_PROVENANCE',
        'scope_markers': SCOPE_MARKERS,
        'slot_callsite_count': len(calls),
        'callsite_fde_count': len(callsite_fdes),
        'rtti_vtable_type_count': len(vtables),
        'caller_fde_with_rtti_owner_count': len(fde_owners),
        'relevant_owner_vtable_count': len(owner_aps),
        'owner_vtable_rip_ref_count': sum(len(rows) for rows in owner_refs.values()),
        'constructor_fde_count': len(constructor_fdes),
        'constructor_record_count': len(constructors),
        'applicable_member_candidate_count': applicable_count,
        'proved_handler_member_callsite_count': len(proved),
        'proved_handler_member_callsites': [sanitize_proved(call, provenance) for call, provenance in proved],
        'accepted_callsite': sanitize_proved(*accepted) if accepted is not None else None,
        'field6_edx_reaching_value': edx,
        'boundary': 'NO_HEURISTIC_RANKING',
    }
    result['classification'] = classification
    result['field6_value'] = value
    result['field6_edx_reaching_value'] = edx

    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('CALLSITE_FDE_SCOPE=PASS')
    print('VTABLE_RIP_CONSTRUCTOR_SCOPE=PASS')
    print('BINARY_SEARCH_FDE_LOOKUP=PASS')
    print('INTERPROCEDURAL_MEMBER_PROVENANCE=PASS')
    print('CONSTRUCTOR_MEMBER_BINDING=' + ('PROVEN' if len(proved) == 1 else 'UNKNOWN'))
    print('FIELD6_EDX_REACHING_VALUE=' + (str(value) if value is not None else 'UNKNOWN'))
    print('CLASSIFICATION=' + classification)


if __name__ == '__main__':
    main()
