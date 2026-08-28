#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_SHA256='d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE=52_105_824
OWNER_CTOR_FDE=(0x7D15C0,0x7D1A8A)
CONFIG_OWNER_STORE=0x7D1685
CONFIG_OWNER_OFFSET=0x9C8
CONFIG_MODE_OFFSET=0x30
HANDLER_VTABLE_AP=0x30B6700
HANDLER_SLOT=0x60
HANDLER_SLOT_TARGET=0xE25620

CONFIG_TYPE_IDENTITY=True
CONFIG_TYPE_UNKNOWN=True
CONFIG_OWNED_METHOD_FLOW=True
NO_HEURISTIC_RANKING=True
NO_SEMANTIC_GUESSING=True
SAFETY={'runtime_access':'none','official_client_executed':False,'login_performed':False,'secret_access':False,'process_memory_access':False,'packet_capture':False,'raw_client_uploaded':False}

@dataclass(frozen=True)
class Section:
    offset:int; size:int; va:int; flags:int

class Image:
    def __init__(self,path:Path):
        self.raw=path.read_bytes(); self.rel={}; self._ins={}
        with path.open('rb') as fh:
            elf=ELFFile(fh)
            self.sections=[Section(int(s['sh_offset']),int(s['sh_size']),int(s['sh_addr']),int(s['sh_flags'])) for s in elf.iter_sections() if int(s['sh_size'])]
            for sec in elf.iter_sections():
                if isinstance(sec,RelocationSection):
                    for r in sec.iter_relocations():
                        if r.is_RELA(): self.rel[int(r['r_offset'])]=int(r['r_addend']) & 0xffffffffffffffff
            dwarf=elf.get_dwarf_info()
            self.fdes=sorted((int(e['initial_location']),int(e['initial_location'])+int(e['address_range'])) for e in dwarf.EH_CFI_entries() if isinstance(e,FDE))
        self.md=Cs(CS_ARCH_X86,CS_MODE_64); self.md.detail=True
    def va_to_off(self,va):
        for s in self.sections:
            if s.va<=va<s.va+s.size: return s.offset+va-s.va
        raise ValueError(hex(va))
    def mapped(self,va,size=1):
        try:o=self.va_to_off(va)
        except ValueError:return False
        return 0<=o<=len(self.raw)-size
    def executable(self,va): return any((s.flags&4) and s.va<=va<s.va+s.size for s in self.sections)
    def bytes(self,va,size): o=self.va_to_off(va); return self.raw[o:o+size]
    def u64(self,va): return struct.unpack_from('<Q',self.raw,self.va_to_off(va))[0]
    def qword(self,va): return self.rel.get(va,self.u64(va) if self.mapped(va,8) else 0)
    def fde(self,va):
        rows=[x for x in self.fdes if x[0]<=va<x[1]]; return rows[0] if len(rows)==1 else None
    def instructions(self,fde):
        if fde not in self._ins:self._ins[fde]=list(self.md.disasm(self.bytes(fde[0],fde[1]-fde[0]),fde[0]))
        return self._ins[fde]

def hx(v): return None if v is None else f'0x{v:x}'

def reg_family(img,reg):
    n=reg if isinstance(reg,str) else img.md.reg_name(reg)
    aliases={'rax':'rax','eax':'rax','ax':'rax','al':'rax','rbx':'rbx','ebx':'rbx','bx':'rbx','bl':'rbx','rcx':'rcx','ecx':'rcx','cx':'rcx','cl':'rcx','rdx':'rdx','edx':'rdx','dx':'rdx','dl':'rdx','rsi':'rsi','esi':'rsi','si':'rsi','sil':'rsi','rdi':'rdi','edi':'rdi','di':'rdi','dil':'rdi','rbp':'rbp','ebp':'rbp','bp':'rbp','bpl':'rbp','rsp':'rsp','esp':'rsp','sp':'rsp','spl':'rsp'}
    if n in aliases:return aliases[n]
    m=re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?',n); return m.group(1) if m else n

def read_cstr(img,va,limit=512):
    if not img.mapped(va):return None
    off=img.va_to_off(va); end=img.raw.find(b'\0',off,min(len(img.raw),off+limit))
    if end<0:return None
    try:return img.raw[off:end].decode('ascii')
    except UnicodeDecodeError:return None

def demangle_nested(name):
    if not name or not(name.startswith('N') and name.endswith('E')):return None
    pos=1; parts=[]
    while pos<len(name)-1:
        m=re.match(r'(\d+)',name[pos:])
        if not m:return None
        ln=int(m.group(1)); pos+=len(m.group(1)); part=name[pos:pos+ln]
        if len(part)!=ln:return None
        parts.append(part); pos+=ln
    return '::'.join(parts) if parts and pos==len(name)-1 else None

def type_name_for_ap(img,ap):
    rtti=img.qword(ap-8)
    if not rtti or not img.mapped(rtti+8,8):return None
    name_va=img.qword(rtti+8); return demangle_nested(read_cstr(img,name_va))

def rip_target(row):
    for op in row.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:return row.address+row.size+int(op.mem.disp)
    return None

def writes_family(img,row,fam):
    try:_r,w=row.regs_access()
    except Exception:return False
    return fam in {reg_family(img,x) for x in w}

def config_vtable_from_ctor(img):
    if img.fde(CONFIG_OWNER_STORE)!=OWNER_CTOR_FDE: raise RuntimeError('owner constructor moved')
    rows=img.instructions(OWNER_CTOR_FDE); by={r.address:i for i,r in enumerate(rows)}; oi=by.get(CONFIG_OWNER_STORE)
    if oi is None:raise RuntimeError('config owner store missing')
    store=rows[oi]
    if store.mnemonic!='mov' or store.op_str!='qword ptr [rbx + 0x9c8], rbp':raise RuntimeError('config owner store mismatch')
    # Find the last [rbp] vtable write before committing rbp to owner+0x9c8.
    candidates=[]
    for i,row in enumerate(rows[:oi]):
        if row.mnemonic!='mov' or len(row.operands)<2:continue
        dst,src=row.operands[0],row.operands[1]
        if dst.type!=X86_OP_MEM or reg_family(img,dst.mem.base)!='rbp' or int(dst.mem.disp)!=0 or src.type!=X86_OP_REG:continue
        sf=reg_family(img,src.reg)
        target=None; def_site=None
        for prev in reversed(rows[:i]):
            if not writes_family(img,prev,sf):continue
            if prev.mnemonic=='lea' and len(prev.operands)>=2 and prev.operands[0].type==X86_OP_REG and prev.operands[1].type==X86_OP_MEM and prev.operands[1].mem.base==X86_REG_RIP:
                target=prev.address+prev.size+int(prev.operands[1].mem.disp); def_site=prev.address
            break
        if target and img.mapped(target-16,24) and img.u64(target-16)==0 and img.executable(img.qword(target)):
            candidates.append({'store_site':row.address,'definition_site':def_site,'address_point':target})
    if not candidates:return {'classification':'CONFIG_TYPE_UNKNOWN','candidates':[]}
    # rbp can be reused for later objects: keep only stores after its last assignment before owner commit.
    last_rbp_def=-1
    for i,row in enumerate(rows[:oi]):
        if writes_family(img,row,'rbp'): last_rbp_def=max(last_rbp_def,i)
    scoped=[c for c in candidates if by.get(c['store_site'],-1)>=last_rbp_def]
    if not scoped: scoped=[candidates[-1]]
    unique={c['address_point']:c for c in scoped}
    if len(unique)!=1:return {'classification':'CONFIG_TYPE_UNKNOWN','candidates':[{**c,'store_site':hx(c['store_site']),'definition_site':hx(c['definition_site']),'address_point':hx(c['address_point']),'type_name':type_name_for_ap(img,c['address_point'])} for c in scoped]}
    c=next(iter(unique.values())); name=type_name_for_ap(img,c['address_point'])
    if not name:return {'classification':'CONFIG_TYPE_UNKNOWN','candidates':[]}
    return {'classification':'CONFIG_TYPE_IDENTITY','type_name':name,'vtable_address_point':hx(c['address_point']),'store_site':hx(c['store_site']),'definition_site':hx(c['definition_site'])}

def vtable_targets(img,ap,max_slots=48):
    rows=[]; bad=0
    for slot in range(max_slots):
        target=img.qword(ap+slot*8)
        if img.executable(target): rows.append({'slot':slot*8,'target':target}); bad=0
        else:
            bad+=1
            if bad>=3 and rows:break
    return rows

def direct_callees(img,fde):
    out=[]
    for row in img.instructions(fde):
        if row.mnemonic=='call' and row.operands and row.operands[0].type==X86_OP_IMM:
            t=int(row.operands[0].imm); tf=img.fde(t)
            if tf and tf[1]-tf[0]<=0x10000:out.append(tf)
    return out

def entry_aliases_until(img,rows,index):
    aliases={'rdi'}
    for row in rows[:index]:
        if row.mnemonic=='mov' and len(row.operands)>=2 and row.operands[0].type==X86_OP_REG:
            dst=reg_family(img,row.operands[0].reg); src=row.operands[1]
            if src.type==X86_OP_REG and reg_family(img,src.reg) in aliases:aliases.add(dst)
            elif dst in aliases and dst!='rdi':aliases.discard(dst)
    return aliases

def scan_fde(img,fde,depth):
    rows=img.instructions(fde); mode_reads=[]; slot_calls=[]; edx_defs=[]
    for i,row in enumerate(rows):
        if row.mnemonic=='mov' and len(row.operands)>=2:
            dst,src=row.operands[0],row.operands[1]
            if src.type==X86_OP_MEM and int(src.mem.disp)==CONFIG_MODE_OFFSET and src.mem.base:
                aliases=entry_aliases_until(img,rows,i)
                if reg_family(img,src.mem.base) in aliases:
                    mode_reads.append({'site':hx(row.address),'operand':row.op_str,'dst_family':reg_family(img,dst.reg) if dst.type==X86_OP_REG else None})
            if dst.type==X86_OP_REG and reg_family(img,dst.reg)=='rdx':edx_defs.append({'site':hx(row.address),'operand':row.op_str})
        if row.mnemonic=='call' and row.operands and row.operands[0].type==X86_OP_MEM and int(row.operands[0].mem.disp)==HANDLER_SLOT:
            slot_calls.append({'site':hx(row.address),'operand':row.op_str})
    return {'fde':[hx(fde[0]),hx(fde[1])],'depth':depth,'config_mode_reads':mode_reads,'slot_0x60_calls':slot_calls,'edx_defs':edx_defs}

def owned_flow(img,identity):
    if identity['classification']!='CONFIG_TYPE_IDENTITY':return {'classification':'CONFIG_OWNED_METHOD_FLOW_UNKNOWN','visited_fdes':[],'interesting':[]}
    ap=int(identity['vtable_address_point'],16); roots=[]
    for row in vtable_targets(img,ap):
        f=img.fde(row['target'])
        if f and f not in roots:roots.append(f)
    q=deque((f,0) for f in roots); seen=set(); scans=[]
    while q:
        f,d=q.popleft()
        if f in seen or d>2:continue
        seen.add(f); scans.append(scan_fde(img,f,d))
        if d<2:
            for c in direct_callees(img,f):
                if c not in seen:q.append((c,d+1))
    interesting=[s for s in scans if s['config_mode_reads'] or s['slot_0x60_calls']]
    both=[s for s in interesting if s['config_mode_reads'] and s['slot_0x60_calls']]
    return {'classification':'CONFIG_OWNED_METHOD_FLOW' if interesting else 'CONFIG_OWNED_METHOD_FLOW_UNKNOWN','root_vtable_target_count':len(roots),'visited_fde_count':len(scans),'interesting':interesting,'same_fde_mode_and_slot_count':len(both),'same_fde_mode_and_slot':both}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--client',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    img=Image(args.client); digest=hashlib.sha256(img.raw).hexdigest()
    if digest!=EXPECTED_SHA256 or len(img.raw)!=EXPECTED_SIZE:raise RuntimeError('exact current fence mismatch')
    if img.qword(HANDLER_VTABLE_AP+HANDLER_SLOT)!=HANDLER_SLOT_TARGET:raise RuntimeError('handler slot mismatch')
    identity=config_vtable_from_ctor(img); flow=owned_flow(img,identity)
    classification='FIELD6_VALUE_UNKNOWN'; value=None
    # This task may identify causal candidates but never infer a value without explicit same-FDE dataflow proof.
    result={'schema':'otclient.track-a.current-login-field6-config-type-flow.v1',**SAFETY,'exact_client':{'version':'15.32.75d4a0','sha256':digest,'size':len(img.raw)},'config_type_identity':identity,'config_owned_method_flow':flow,'classification':classification,'field6_value':value,'scope_markers':{'NO_HEURISTIC_RANKING':True,'NO_SEMANTIC_GUESSING':True}}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('CONFIG_TYPE_IDENTITY='+identity['classification']);print('CONFIG_OWNED_METHOD_FLOW='+flow['classification']);print('FIELD6_VALUE_UNKNOWN=true');print('NO_HEURISTIC_RANKING=true');print('NO_SEMANTIC_GUESSING=true')
if __name__=='__main__':main()
