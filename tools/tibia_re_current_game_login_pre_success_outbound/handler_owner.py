#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import qmeta_runner as base

core = base.core
OWNER_FIELD = 0x9C0


def mem_uses_owner_field(ins) -> bool:
    return any(
        op.type == core.X86_OP_MEM and int(op.mem.disp) == OWNER_FIELD
        for op in ins.operands
    )


def local_slot_calls_after_load(img: core.Image, instructions, load_index: int, loaded_reg: int) -> list[dict]:
    aliases = {loaded_reg}
    rows = []
    for ins in instructions[load_index + 1:min(len(instructions), load_index + 96)]:
        if ins.mnemonic.startswith('ret'):
            break
        if ins.mnemonic == 'mov' and len(ins.operands) >= 2:
            dst, src = ins.operands[0], ins.operands[1]
            if dst.type == core.X86_OP_REG and src.type == core.X86_OP_REG and src.reg in aliases:
                aliases.add(dst.reg)
            if dst.type == core.X86_OP_REG and dst.reg in aliases and not (src.type == core.X86_OP_REG and src.reg in aliases):
                aliases.discard(dst.reg)
        if ins.mnemonic != 'call' or not ins.operands:
            continue
        op = ins.operands[0]
        if op.type != core.X86_OP_MEM or int(op.mem.disp) != 0x60 or not op.mem.base:
            continue
        # Accept only when the vtable base was loaded from one of the exact
        # owner-field pointer aliases shortly before this call.
        vreg = op.mem.base
        vtable_load = None
        site_index = next(i for i, row in enumerate(instructions) if row.address == ins.address)
        for row in reversed(instructions[max(load_index + 1, site_index - 16):site_index]):
            if row.mnemonic != 'mov' or len(row.operands) < 2:
                continue
            dst, src = row.operands[0], row.operands[1]
            if dst.type != core.X86_OP_REG or dst.reg != vreg:
                continue
            if src.type == core.X86_OP_MEM and src.mem.disp == 0 and src.mem.base in aliases:
                vtable_load = row
                break
        if vtable_load is not None:
            rows.append({
                'site': core.hx(ins.address),
                'operand': ins.op_str,
                'vtable_load_site': core.hx(vtable_load.address),
                'vtable_load_operand': vtable_load.op_str,
                'context': base.bounded_context(instructions, ins.address, before=28, after=16),
            })
    return rows


def handler_owner_field_refs(img: core.Image) -> dict:
    handler = core.exact_vtable(
        img,
        'TLoginProtocolMessageHandler',
        'tibia::authentication::TLoginProtocolMessageHandler',
    )
    refs = []
    direct_slot_calls = []
    for section in img.sections:
        if not (section.flags & 4):
            continue
        for ins in img.md.disasm(img.raw[section.offset:section.offset + section.size], section.va):
            if not mem_uses_owner_field(ins):
                continue
            fde = img.fde(ins.address)
            instructions = img.instructions(fde) if fde else []
            row = {
                'site': core.hx(ins.address),
                'mnemonic': ins.mnemonic,
                'operand': ins.op_str,
                'fde': ([core.hx(fde[0]), core.hx(fde[1])] if fde else None),
                'context': (base.bounded_context(instructions, ins.address, before=22, after=28) if fde else []),
            }
            if fde and ins.mnemonic == 'mov' and len(ins.operands) >= 2:
                dst, src = ins.operands[0], ins.operands[1]
                if dst.type == core.X86_OP_REG and src.type == core.X86_OP_MEM and int(src.mem.disp) == OWNER_FIELD:
                    index = next(i for i, x in enumerate(instructions) if x.address == ins.address)
                    calls = local_slot_calls_after_load(img, instructions, index, dst.reg)
                    row['local_slot_0x60_calls'] = calls
                    direct_slot_calls.extend({'owner_load_site': row['site'], **call} for call in calls)
            refs.append(row)
    return {
        'classification': 'HANDLER_OWNER_FIELD_REF_CENSUS',
        'owner_field': '0x9c0',
        'handler_vtable_address_point': core.hx(handler['address_point']),
        'handler_slot_0x60_target': core.hx(base.core.slot_target(handler, 0x60)),
        'ref_count': len(refs),
        'refs': refs,
        'owner_field_to_slot_0x60_calls': direct_slot_calls,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    result = json.loads(args.output.read_text(encoding='utf-8'))
    img = core.Image(args.client)
    census = handler_owner_field_refs(img)
    result['handler_owner_field_refs'] = census
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('HANDLER_OWNER_FIELD_REF_CENSUS=PASS')
    print('HANDLER_OWNER_FIELD_REF_COUNT=' + str(census['ref_count']))
    print('HANDLER_OWNER_FIELD_SLOT_0X60_CALL_COUNT=' + str(len(census['owner_field_to_slot_0x60_calls'])))


if __name__ == '__main__':
    main()
