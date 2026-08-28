#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import member_provenance as provenance
import probe as core

DEPENDENCY_ACCESSOR_PROVENANCE = True
ACCESSOR_TARGET_0XE195B0 = 0xE195B0
AUTHINFO_TYPE = 'tibia::authentication::TAuthenticationAndEncryptionInfo'
NO_SEMANTIC_GUESSING = True


def sanitize_instruction(row) -> dict:
    return {'at': core.hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}


def recover_accessor_member(img: core.Image) -> dict:
    fde = img.fde(ACCESSOR_TARGET_0XE195B0)
    if fde is None:
        raise RuntimeError('accessor FDE unavailable')
    instructions = img.instructions(fde)
    reads = []
    for row in instructions:
        for operand in row.operands:
            if operand.type != core.X86_OP_MEM or not operand.mem.base:
                continue
            base = core.reg_family(img.md.reg_name(operand.mem.base))
            if base != 'rdi':
                continue
            reads.append({
                'site': row.address,
                'member_offset': int(operand.mem.disp),
                'size': int(operand.size or 0),
                'instruction': sanitize_instruction(row),
            })
    unique_offsets = {row['member_offset'] for row in reads}
    if len(unique_offsets) != 1:
        raise RuntimeError(f'accessor member offset ambiguous: {sorted(unique_offsets)}')
    offset = next(iter(unique_offsets))
    return {
        'target': core.hx(ACCESSOR_TARGET_0XE195B0),
        'fde': [core.hx(fde[0]), core.hx(fde[1])],
        'instructions': [sanitize_instruction(row) for row in instructions],
        'member_offset': offset,
        'member_offset_hex': core.hx(offset),
        'reads': [{**row, 'site': core.hx(row['site'])} for row in reads],
    }


def authinfo_owner(img: core.Image) -> dict:
    rows = [row for row in provenance.recover_vtables(img) if row['type_name'] == AUTHINFO_TYPE]
    unique = {(row['rtti'], row['address_point']): row for row in rows}
    if len(unique) != 1:
        raise RuntimeError(f'AuthInfo vtable ambiguous: {len(unique)}')
    return next(iter(unique.values()))


def constructor_writes(img: core.Image, owner: dict, member_offset: int) -> list[dict]:
    records = provenance.find_constructor_records(img, {owner['address_point']})
    rows = []
    for record in records:
        instructions = record['_instructions']
        this_family = record['this_family']
        for row in instructions:
            if row.mnemonic not in ('mov', 'movzx', 'movsx') or len(row.operands) < 2:
                continue
            dst, src = row.operands[0], row.operands[1]
            if dst.type != core.X86_OP_MEM or not dst.mem.base:
                continue
            if core.reg_family(img.md.reg_name(dst.mem.base)) != this_family or int(dst.mem.disp) != member_offset:
                continue
            source = row.op_str.split(',', 1)[1].strip() if ',' in row.op_str else ''
            immediate = int(src.imm) if src.type == core.X86_OP_IMM else None
            rows.append({
                'fde': [core.hx(record['fde'][0]), core.hx(record['fde'][1])],
                'vtable_store_site': core.hx(record['vtable_store_site']),
                'write_site': core.hx(row.address),
                'operand': row.op_str,
                'source': source,
                'immediate_value': immediate,
            })
    return rows


def vtable_method_targets(img: core.Image, owner: dict, max_bytes: int = 0x180) -> list[dict]:
    address_point = owner['address_point']
    rows = []
    seen = set()
    for slot in range(0, max_bytes, 8):
        address = address_point + slot
        if not img.mapped(address, 8):
            break
        target = img.qword(address)
        if not img.executable(target):
            continue
        key = (slot, target)
        if key in seen:
            continue
        seen.add(key)
        fde = img.fde(target)
        rows.append({
            'slot': slot,
            'slot_hex': core.hx(slot),
            'target': target,
            'target_hex': core.hx(target),
            'fde': fde,
        })
    return rows


def vtable_owned_writes(img: core.Image, owner: dict, member_offset: int) -> list[dict]:
    rows = []
    seen = set()
    for method in vtable_method_targets(img, owner):
        fde = method['fde']
        if fde is None or fde[1] - fde[0] > 0x10000:
            continue
        for row in img.instructions(fde):
            if not row.operands:
                continue
            dst = row.operands[0]
            if dst.type != core.X86_OP_MEM or not dst.mem.base:
                continue
            if core.reg_family(img.md.reg_name(dst.mem.base)) != 'rdi' or int(dst.mem.disp) != member_offset:
                continue
            key = (method['slot'], row.address)
            if key in seen:
                continue
            seen.add(key)
            src = row.operands[1] if len(row.operands) > 1 else None
            rows.append({
                'slot': method['slot_hex'],
                'method_target': method['target_hex'],
                'method_fde': [core.hx(fde[0]), core.hx(fde[1])],
                'write_site': core.hx(row.address),
                'operand': row.op_str,
                'immediate_value': int(src.imm) if src is not None and src.type == core.X86_OP_IMM else None,
            })
    return rows


def all_displacement_writes(img: core.Image, member_offset: int) -> list[dict]:
    # Census only: displacement equality does not prove AuthInfo ownership.
    rows = []
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x10000:
            continue
        for row in img.instructions(fde):
            if not row.operands:
                continue
            dst = row.operands[0]
            if dst.type != core.X86_OP_MEM or int(dst.mem.disp) != member_offset:
                continue
            src = row.operands[1] if len(row.operands) > 1 else None
            rows.append({
                'fde': [core.hx(fde[0]), core.hx(fde[1])],
                'site': core.hx(row.address),
                'base_family': core.reg_family(img.md.reg_name(dst.mem.base)) if dst.mem.base else None,
                'operand': row.op_str,
                'immediate_value': int(src.imm) if src is not None and src.type == core.X86_OP_IMM else None,
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()

    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    core.verify_promoted_target(img)

    guard = result.get('producer_dependency_guard') or {}
    owner = guard.get('unique_target_owner')
    if not owner or owner.get('type_name') != AUTHINFO_TYPE:
        raise RuntimeError('promoted dependency owner is not uniquely TAuthenticationAndEncryptionInfo')

    accessor = recover_accessor_member(img)
    recovered_owner = authinfo_owner(img)
    if core.hx(recovered_owner['address_point']) != owner.get('vtable_address_point'):
        raise RuntimeError('AuthInfo owner address point moved inside exact fence')

    ctor_writes = constructor_writes(img, recovered_owner, accessor['member_offset'])
    method_writes = vtable_owned_writes(img, recovered_owner, accessor['member_offset'])
    census = all_displacement_writes(img, accessor['member_offset'])

    result['dependency_accessor_provenance'] = {
        'classification': 'DEPENDENCY_ACCESSOR_PROVENANCE',
        'owner_type': AUTHINFO_TYPE,
        'owner_vtable_address_point': core.hx(recovered_owner['address_point']),
        'accessor': accessor,
        'constructor_writes': ctor_writes,
        'vtable_owned_method_writes': method_writes,
        'all_same_displacement_write_count': len(census),
        'all_same_displacement_writes': census,
        'value_classification': 'STATIC_DEFAULT_ONLY' if ctor_writes and not method_writes else 'MUTABILITY_NOT_CLOSED',
        'field6_value': None,
        'scope_markers': {
            'ACCESSOR_MEMBER_OFFSET': True,
            'CONSTRUCTOR_WRITES': True,
            'ALL_MEMBER_WRITES': True,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('DEPENDENCY_ACCESSOR_PROVENANCE=PASS')
    print('TAuthenticationAndEncryptionInfo=PASS')
    print('ACCESSOR_TARGET_0XE195B0=PASS')
    print('ACCESSOR_MEMBER_OFFSET=' + accessor['member_offset_hex'])
    print('CONSTRUCTOR_WRITES=' + str(len(ctor_writes)))
    print('ALL_MEMBER_WRITES=' + str(len(census)))
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
