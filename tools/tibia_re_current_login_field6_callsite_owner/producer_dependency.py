#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import member_provenance as provenance
import probe as core

PRODUCER_DEPENDENCY_GUARD = True
HANDLER_MEMBER_OFFSET_0X10 = 0x10
DEPENDENCY_VIRTUAL_SLOT_0X98 = 0x98
DEPENDENCY_TARGET_0XE195B0 = 0xE195B0
RTTI_OWNER_RECOVERY = True
NO_SEMANTIC_GUESSING = True


def instruction_index(instructions, address: int) -> int:
    rows = [i for i, row in enumerate(instructions) if row.address == address]
    if len(rows) != 1:
        raise RuntimeError(f'instruction address ambiguous: {address:#x}:{len(rows)}')
    return rows[0]


def bounded_context(instructions, address: int, before: int = 8, after: int = 10) -> list[dict]:
    index = instruction_index(instructions, address)
    return [
        {'at': core.hx(row.address), 'mnemonic': row.mnemonic, 'operand': row.op_str}
        for row in instructions[max(0, index - before):index + after + 1]
    ]


def prove_guard(img: core.Image) -> dict:
    fde = img.fde(core.HANDLER_SLOT_TARGET)
    if fde is None:
        raise RuntimeError('producer FDE unavailable')
    instructions = img.instructions(fde)
    # Exact-current producer promotion already fences 0xe25620. Re-prove the
    # dependency guard structurally instead of trusting old instruction prose.
    matches = []
    for index, row in enumerate(instructions):
        if row.mnemonic != 'mov' or len(row.operands) < 2:
            continue
        dst, src = row.operands[0], row.operands[1]
        if dst.type != core.X86_OP_REG or src.type != core.X86_OP_MEM or not src.mem.base:
            continue
        if core.reg_family(img.md.reg_name(dst.reg)) != 'rdi':
            continue
        if core.reg_family(img.md.reg_name(src.mem.base)) != 'rdi' or int(src.mem.disp) != HANDLER_MEMBER_OFFSET_0X10:
            continue
        window = instructions[index:index + 8]
        slot_load = None
        compare = None
        target_lea = None
        for candidate in instructions[max(0, index - 6):index + 8]:
            if candidate.mnemonic == 'lea' and core.rip_target(candidate) == DEPENDENCY_TARGET_0XE195B0:
                target_lea = candidate
        for candidate in window:
            if candidate.mnemonic == 'mov' and len(candidate.operands) >= 2:
                cdst, csrc = candidate.operands[0], candidate.operands[1]
                if cdst.type == core.X86_OP_REG and csrc.type == core.X86_OP_MEM and int(csrc.mem.disp) == DEPENDENCY_VIRTUAL_SLOT_0X98:
                    slot_load = candidate
            if candidate.mnemonic == 'cmp' and DEPENDENCY_TARGET_0XE195B0:
                compare = candidate if 'rax' in candidate.op_str and 'rdx' in candidate.op_str else compare
        if target_lea and slot_load and compare:
            matches.append((row, target_lea, slot_load, compare))
    if len(matches) != 1:
        raise RuntimeError(f'producer dependency guard ambiguous: {len(matches)}')
    member_load, target_lea, slot_load, compare = matches[0]
    return {
        'classification': 'PRODUCER_DEPENDENCY_GUARD',
        'producer_fde': [core.hx(fde[0]), core.hx(fde[1])],
        'handler_member_offset': core.hx(HANDLER_MEMBER_OFFSET_0X10),
        'member_load_site': core.hx(member_load.address),
        'target_load_site': core.hx(target_lea.address),
        'virtual_slot': core.hx(DEPENDENCY_VIRTUAL_SLOT_0X98),
        'virtual_slot_load_site': core.hx(slot_load.address),
        'dependency_target': core.hx(DEPENDENCY_TARGET_0XE195B0),
        'compare_site': core.hx(compare.address),
        'context': bounded_context(instructions, member_load.address, before=6, after=12),
    }


def recover_target_owners(img: core.Image) -> list[dict]:
    vtables = provenance.recover_vtables(img)
    rows = []
    for vtable in vtables:
        address_point = int(vtable['address_point'])
        slot_address = address_point + DEPENDENCY_VIRTUAL_SLOT_0X98
        if not img.mapped(slot_address, 8):
            continue
        target = img.qword(slot_address)
        if target != DEPENDENCY_TARGET_0XE195B0:
            continue
        fde = img.fde(target)
        rows.append({
            'type_name': vtable['type_name'],
            'rtti': core.hx(int(vtable['rtti'])),
            'vtable_address_point': core.hx(address_point),
            'slot': core.hx(DEPENDENCY_VIRTUAL_SLOT_0X98),
            'target': core.hx(target),
            'target_fde': [core.hx(fde[0]), core.hx(fde[1])] if fde else None,
        })
    unique = {
        (row['type_name'], row['vtable_address_point'], row['slot']): row
        for row in rows
    }
    return [unique[key] for key in sorted(unique)]


def target_direct_contexts(img: core.Image) -> list[dict]:
    rows = []
    seen = set()
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1] - fde[0] > 0x10000:
            continue
        for instruction in img.instructions(fde):
            if instruction.mnemonic not in ('call', 'jmp') or not instruction.operands:
                continue
            if instruction.operands[0].type != core.X86_OP_IMM:
                continue
            if int(instruction.operands[0].imm) != DEPENDENCY_TARGET_0XE195B0:
                continue
            key = (instruction.address, fde)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                'site': core.hx(instruction.address),
                'fde': [core.hx(fde[0]), core.hx(fde[1])],
                'mnemonic': instruction.mnemonic,
                'context': bounded_context(img.instructions(fde), instruction.address, before=6, after=6),
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

    guard = prove_guard(img)
    owners = recover_target_owners(img)
    direct = target_direct_contexts(img)

    if len(owners) == 1:
        owner_classification = 'UNIQUE_RTTI_VTABLE_OWNER'
        unique_owner = owners[0]
    elif not owners:
        owner_classification = 'NO_RTTI_VTABLE_OWNER'
        unique_owner = None
    else:
        owner_classification = 'MULTIPLE_RTTI_VTABLE_OWNERS'
        unique_owner = None

    guard.update({
        'target_owner_classification': owner_classification,
        'target_vtable_owners': owners,
        'unique_target_owner': unique_owner,
        'target_direct_call_or_jump_contexts': direct,
        'semantic_name': 'UNKNOWN',
        'field6_value': None,
        'scope_markers': {
            'HANDLER_MEMBER_OFFSET_0X10': True,
            'DEPENDENCY_VIRTUAL_SLOT_0X98': True,
            'DEPENDENCY_TARGET_0XE195B0': True,
            'RTTI_OWNER_RECOVERY': RTTI_OWNER_RECOVERY,
            'NO_SEMANTIC_GUESSING': NO_SEMANTIC_GUESSING,
        },
    })
    result['producer_dependency_guard'] = guard
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    print('PRODUCER_DEPENDENCY_GUARD=PASS')
    print('HANDLER_MEMBER_OFFSET_0X10=PASS')
    print('DEPENDENCY_VIRTUAL_SLOT_0X98=PASS')
    print('DEPENDENCY_TARGET_0XE195B0=PASS')
    print('RTTI_OWNER_RECOVERY=' + owner_classification)
    print('NO_SEMANTIC_GUESSING=true')


if __name__ == '__main__':
    main()
