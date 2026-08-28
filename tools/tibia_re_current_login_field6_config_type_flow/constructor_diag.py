#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe as core

CONFIG_TYPE_CONSTRUCTOR_DIAGNOSTICS = True


def hx(v: int) -> str:
    return f'0x{v:x}'


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--client',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    result=json.loads(args.output.read_text(encoding='utf-8'))
    img=core.Image(args.client)
    rows=img.instructions(core.OWNER_CTOR_FDE)
    owner_index=next((i for i,r in enumerate(rows) if r.address==core.CONFIG_OWNER_STORE),None)
    if owner_index is None: raise RuntimeError('config owner store missing')
    rbp_defs=[]; rbp_zero_stores=[]; rip_defs=[]
    for i,row in enumerate(rows[:owner_index+1]):
        if core.writes_family(img,row,'rbp'):
            rbp_defs.append({'at':hx(row.address),'mnemonic':row.mnemonic,'operand':row.op_str})
        if row.mnemonic=='mov' and len(row.operands)>=2:
            dst,src=row.operands[0],row.operands[1]
            if dst.type==core.X86_OP_MEM and dst.mem.base and core.reg_family(img,dst.mem.base)=='rbp' and int(dst.mem.disp)==0:
                rec={'at':hx(row.address),'mnemonic':row.mnemonic,'operand':row.op_str,'source_family':core.reg_family(img,src.reg) if src.type==core.X86_OP_REG else None,'rip_definition':None}
                if src.type==core.X86_OP_REG:
                    sf=core.reg_family(img,src.reg)
                    for prev in reversed(rows[:i]):
                        if not core.writes_family(img,prev,sf): continue
                        target=core.rip_target(prev)
                        if prev.mnemonic=='lea' and target is not None:
                            rec['rip_definition']={'at':hx(prev.address),'target':hx(target),'mapped':img.mapped(target-16,24),'offset_to_top_zero':bool(img.mapped(target-16,8) and img.u64(target-16)==0),'type_name':core.type_name_for_ap(img,target) if img.mapped(target-16,24) else None}
                        break
                rbp_zero_stores.append(rec)
        target=core.rip_target(row)
        if target is not None and row.mnemonic=='lea':
            rip_defs.append({'at':hx(row.address),'operand':row.op_str,'target':hx(target),'type_name':core.type_name_for_ap(img,target) if img.mapped(target-16,24) else None})
    start=max(0,owner_index-90)
    bounded=[{'at':hx(r.address),'mnemonic':r.mnemonic,'operand':r.op_str} for r in rows[start:owner_index+8]]
    result['config_type_constructor_diagnostics']={
        'classification':'CONFIG_TYPE_CONSTRUCTOR_DIAGNOSTICS',
        'rbp_definitions':rbp_defs,
        'rbp_zero_stores':rbp_zero_stores,
        'rip_definitions_in_prefix':rip_defs,
        'bounded_constructor_context':bounded,
    }
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('CONFIG_TYPE_CONSTRUCTOR_DIAGNOSTICS=PASS')

if __name__=='__main__': main()
