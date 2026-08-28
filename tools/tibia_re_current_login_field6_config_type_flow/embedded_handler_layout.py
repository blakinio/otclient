#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe as core

CONFIG_RTTI_RAW_NAME = True
CONFIG_EMBEDDED_HANDLER_LAYOUT = True
PARENT_VTABLE_AP = 0x2F89C38
HANDLER_OFFSET = 0x10
MODE_PARENT_OFFSET = 0x30
MODE_HANDLER_OFFSET = 0x20


def hx(v: int | None) -> str | None:
    return None if v is None else f'0x{v:x}'


def exact_instruction(rows: list, address: int, mnemonic: str, operand: str) -> dict:
    row=next((r for r in rows if r.address==address),None)
    if row is None or row.mnemonic!=mnemonic or row.op_str!=operand:
        actual=None if row is None else (row.mnemonic,row.op_str)
        raise RuntimeError(f'embedded layout instruction mismatch {address:#x}: {actual}')
    return {'at':hx(address),'mnemonic':row.mnemonic,'operand':row.op_str}


def raw_rtti(img: core.Image, address_point: int) -> dict:
    rtti=img.qword(address_point-8)
    name_va=img.qword(rtti+8) if rtti and img.mapped(rtti+8,8) else 0
    raw=core.read_cstr(img,name_va) if name_va else None
    return {
        'vtable_address_point':hx(address_point),
        'rtti':hx(rtti) if rtti else None,
        'name_pointer':hx(name_va) if name_va else None,
        'raw_name':raw,
        'nested_demangle':core.demangle_nested(raw) if raw else None,
        'contains_login_handler_name':bool(raw and 'TLoginProtocolMessageHandler' in raw),
    }


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--client',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result=json.loads(args.output.read_text(encoding='utf-8'))
    img=core.Image(args.client)
    rows=img.instructions(core.OWNER_CTOR_FDE)
    assertions=[
        exact_instruction(rows,0x7D15DF,'mov','edi, 0x38'),
        exact_instruction(rows,0x7D15E7,'call','0x4d8670'),
        exact_instruction(rows,0x7D15F5,'mov','rbp, rax'),
        exact_instruction(rows,0x7D15FC,'lea','rax, [rip + 0x27b8635]'),
        exact_instruction(rows,0x7D1603,'lea','r14, [rbp + 0x10]'),
        exact_instruction(rows,0x7D1607,'mov','qword ptr [rbp], rax'),
        exact_instruction(rows,0x7D1613,'lea','rax, [rip + 0x28e50e6]'),
        exact_instruction(rows,0x7D1622,'mov','qword ptr [rbp + 0x10], rax'),
        exact_instruction(rows,0x7D1677,'mov','dword ptr [rbp + 0x30], edx'),
        exact_instruction(rows,0x7D167E,'mov','qword ptr [rbx + 0x9c0], r14'),
        exact_instruction(rows,0x7D1685,'mov','qword ptr [rbx + 0x9c8], rbp'),
    ]
    # Recompute RIP targets rather than trusting the literals above semantically.
    parent_lea=next(r for r in rows if r.address==0x7D15FC)
    handler_lea=next(r for r in rows if r.address==0x7D1613)
    parent_ap=core.rip_target(parent_lea); handler_ap=core.rip_target(handler_lea)
    if parent_ap!=PARENT_VTABLE_AP: raise RuntimeError(f'parent vtable moved: {parent_ap:#x}')
    if handler_ap!=core.HANDLER_VTABLE_AP: raise RuntimeError(f'handler vtable moved: {handler_ap:#x}')
    rtti=raw_rtti(img,parent_ap)
    result['config_embedded_handler_layout']={
        'classification':'CONFIG_EMBEDDED_HANDLER_LAYOUT',
        'allocation_size':'0x38',
        'parent_vtable_address_point':hx(parent_ap),
        'parent_rtti':rtti,
        'embedded_handler_offset':hx(HANDLER_OFFSET),
        'embedded_handler_vtable_address_point':hx(handler_ap),
        'mode_parent_offset':hx(MODE_PARENT_OFFSET),
        'mode_handler_offset':hx(MODE_HANDLER_OFFSET),
        'owner_handler_offset':'0x9c0',
        'owner_control_block_offset':'0x9c8',
        'relation':'mode parent+0x30 == embedded handler+0x20',
        'instructions':assertions,
        'scope_markers':{'CONFIG_RTTI_RAW_NAME':True},
    }
    if rtti['raw_name']:
        result['config_type_identity']={
            'classification':'CONFIG_TYPE_IDENTITY',
            'vtable_address_point':hx(parent_ap),
            'raw_rtti_name':rtti['raw_name'],
            'nested_demangle':rtti['nested_demangle'],
        }
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('CONFIG_RTTI_RAW_NAME=PASS' if rtti['raw_name'] else 'CONFIG_RTTI_RAW_NAME=UNKNOWN')
    print('CONFIG_EMBEDDED_HANDLER_LAYOUT=PASS')

if __name__=='__main__':main()
