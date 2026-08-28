#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

EXPECTED_SHA256='d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_SIZE=52_105_824
TARGET_FDE=(0x16DA340,0x16DA7FC)
TARGET_SITE=0x16DA716
HANDLER_TYPE='tibia::authentication::TLoginProtocolMessageHandler'
HANDLER_VTABLE_AP=0x30B6700
HANDLER_SLOT=0x60
HANDLER_SLOT_TARGET=0xE25620

LAST_SCALAR_EXACT_REASSERTION=True
LAST_SCALAR_QMETA_OWNER=True
LAST_SCALAR_MEMBER_BINDING=True
NO_HEURISTIC_RANKING=True
NO_SEMANTIC_GUESSING=True
SAFETY={'runtime_access': 'none','official_client_executed': False,'login_performed':False,'secret_access':False,'process_memory_access':False,'packet_capture':False,'raw_client_uploaded':False}

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
            if s.va<=va<s.va+s.size:return s.offset+va-s.va
        raise ValueError(hex(va))
    def off_to_va(self,off):
        for s in self.sections:
            if s.offset<=off<s.offset+s.size:return s.va+off-s.offset
        return None
    def mapped(self,va,size=1):
        try:o=self.va_to_off(va)
        except ValueError:return False
        return 0<=o<=len(self.raw)-size
    def executable(self,va):return any((s.flags&4) and s.va<=va<s.va+s.size for s in self.sections)
    def bytes(self,va,size):o=self.va_to_off(va);return self.raw[o:o+size]
    def u32(self,va):return struct.unpack_from('<I',self.raw,self.va_to_off(va))[0]
    def i32(self,va):return struct.unpack_from('<i',self.raw,self.va_to_off(va))[0]
    def u64(self,va):return struct.unpack_from('<Q',self.raw,self.va_to_off(va))[0]
    def qword(self,va):return self.rel.get(va,self.u64(va) if self.mapped(va,8) else 0)
    def fde(self,va):
        rows=[x for x in self.fdes if x[0]<=va<x[1]];return rows[0] if len(rows)==1 else None
    def instructions(self,fde):
        if fde not in self._ins:self._ins[fde]=list(self.md.disasm(self.bytes(fde[0],fde[1]-fde[0]),fde[0]))
        return self._ins[fde]

def hx(v):return None if v is None else f'0x{v:x}'

def reg_family(img,reg):
    n=reg if isinstance(reg,str) else img.md.reg_name(reg)
    aliases={'rax':'rax','eax':'rax','ax':'rax','al':'rax','rbx':'rbx','ebx':'rbx','bx':'rbx','bl':'rbx','rcx':'rcx','ecx':'rcx','cx':'rcx','cl':'rcx','rdx':'rdx','edx':'rdx','dx':'rdx','dl':'rdx','rsi':'rsi','esi':'rsi','si':'rsi','sil':'rsi','rdi':'rdi','edi':'rdi','di':'rdi','dil':'rdi','rbp':'rbp','ebp':'rbp','bp':'rbp','bpl':'rbp','rsp':'rsp','esp':'rsp','sp':'rsp','spl':'rsp'}
    if n in aliases:return aliases[n]
    m=re.fullmatch(r'(r(?:8|9|1[0-5]))(?:d|w|b)?',n);return m.group(1) if m else n

def writes_family(img,row,family):
    try:_r,w=row.regs_access()
    except Exception:return False
    return family in {reg_family(img,x) for x in w}

def qstring(img,base,index):
    ent=base+index*8; rel=img.u32(ent); ln=img.u32(ent+4)
    if ln>4096 or not img.mapped(base+rel,ln):raise ValueError
    return img.bytes(base+rel,ln).decode('utf-8')

def parse_meta(img,sbase,mbase):
    if not img.mapped(mbase,56):return None
    try:h=[img.u32(mbase+i*4) for i in range(14)]
    except Exception:return None
    rev,ci,_cic,_cio,mc,mo,_pc,_po,_ec,_eo,_cc,_co,flags,sc=h
    if not(7<=rev<=20 and ci==0 and 0<mc<=1000 and 14<=mo<200000 and sc<=mc):return None
    try:class_name=qstring(img,sbase,ci)
    except Exception:return None
    if not class_name or '::' not in class_name:return None
    methods=[]
    try:
        for i in range(mc):
            p=mbase+(mo+i*6)*4; row=[img.u32(p+j*4) for j in range(6)]; name_index,argc,param_offset,_tag,method_flags,_mt=row
            if argc>32 or param_offset>=400000:return None
            methods.append({'index':i,'name':qstring(img,sbase,name_index),'argc':argc,'flags':method_flags})
    except Exception:return None
    return {'class_name':class_name,'method_count':mc,'signal_count':sc,'methods':methods}

def recover_jump_table(img,static,method_count):
    fde=img.fde(static)
    if not fde:raise RuntimeError('static metacall FDE missing')
    rows=img.instructions(fde); candidates=set()
    for pos,row in enumerate(rows):
        if row.mnemonic!='lea' or len(row.operands)<2:continue
        src=row.operands[1]
        if src.type!=X86_OP_MEM or src.mem.base!=X86_REG_RIP:continue
        reg=row.operands[0].reg; table=row.address+row.size+int(src.mem.disp)
        used=any(any(op.type==X86_OP_MEM and op.mem.base==reg and op.mem.scale==4 for op in later.operands) for later in rows[pos+1:pos+12])
        if not used:continue
        try:targets=tuple(table+img.i32(table+4*i) for i in range(method_count))
        except Exception:continue
        if not all(img.executable(t) for t in targets):continue
        bounded=any(prev.mnemonic=='cmp' and len(prev.operands)>=2 and prev.operands[0].type==X86_OP_REG and img.md.reg_name(prev.operands[0].reg)=='edx' and prev.operands[1].type==X86_OP_IMM and int(prev.operands[1].imm)==method_count-1 for prev in rows[max(0,pos-16):pos])
        if bounded:candidates.add((table,targets))
    if len(candidates)!=1:raise RuntimeError(f'jump table ambiguous {len(candidates)}')
    table,targets=next(iter(candidates));return table,list(targets)

def direct_edges_into_target(img):
    out=[]
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1]-fde[0]>0x10000:continue
        for row in img.instructions(fde):
            if row.mnemonic not in ('call','jmp') or not row.operands or row.operands[0].type!=X86_OP_IMM:continue
            t=int(row.operands[0].imm)
            if TARGET_FDE[0]<=t<TARGET_FDE[1]:out.append({'site':row.address,'target':t,'source_fde':fde})
    return out

def static_meta_candidates(img,source_fdes):
    out=[];seen=set()
    for where,sbase in img.rel.items():
        mbase=img.rel.get(where+8); static=img.rel.get(where+16)
        if mbase is None or static is None or not img.executable(static):continue
        if img.fde(static) not in source_fdes:continue
        meta=parse_meta(img,sbase,mbase)
        if not meta:continue
        key=(sbase,mbase,static,meta['class_name'])
        if key in seen:continue
        seen.add(key);out.append({**meta,'static_metaobject':where,'stringdata':sbase,'metadata':mbase,'static_metacall':static})
    return out

def case_block(img,static_fde,case_target,all_targets):
    rows=img.instructions(static_fde); by={r.address:i for i,r in enumerate(rows)}
    if case_target not in by:return []
    out=[]
    for row in rows[by[case_target]:by[case_target]+96]:
        if out and row.address in all_targets:break
        out.append(row)
        if row.mnemonic.startswith('ret') or row.mnemonic=='jmp':break
    return out

def qmeta_owner(img):
    edges=direct_edges_into_target(img); source_fdes={e['source_fde'] for e in edges}; links=[]
    for meta in static_meta_candidates(img,source_fdes):
        sf=img.fde(meta['static_metacall']); rel_edges=[e for e in edges if e['source_fde']==sf]
        if not rel_edges:continue
        try,targets=None,None
        try:table,targets=recover_jump_table(img,meta['static_metacall'],meta['method_count'])
        except RuntimeError:continue
        all_targets=set(targets)
        for method,case in zip(meta['methods'],targets):
            sites={r.address for r in case_block(img,sf,case,all_targets)}; hits=[e for e in rel_edges if e['site'] in sites]
            if hits:links.append({'class_name':meta['class_name'],'method':method,'case_target':hx(case),'direct_edges':[{'site':hx(e['site']),'target':hx(e['target'])} for e in hits]})
    uniq={(x['class_name'],x['method']['index'],x['case_target'],tuple((e['site'],e['target']) for e in x['direct_edges'])):x for x in links}
    links=list(uniq.values())
    return {'classification':'LAST_SCALAR_QMETA_OWNER' if len(links)==1 else 'LAST_SCALAR_QMETA_OWNER_UNKNOWN','link_count':len(links),'links':links,'owner_class':links[0]['class_name'] if len(links)==1 else None,'owner_method':links[0]['method'] if len(links)==1 else None}

def raw_occurrences(img,needle):
    out=[];start=0
    while True:
        off=img.raw.find(needle,start)
        if off<0:break
        va=img.off_to_va(off)
        if va is not None:out.append(va)
        start=off+1
    return out

def mangle_nested(name):return ('N'+''.join(f'{len(p)}{p}' for p in name.split('::'))+'E').encode('ascii')
def type_vtables(img,type_name):
    reverse=defaultdict(list)
    for where,value in img.rel.items():reverse[value].append(where)
    aps=set()
    for nva in raw_occurrences(img,mangle_nested(type_name)):
        for ns in reverse.get(nva,[]):
            rtti=ns-8
            for ts in reverse.get(rtti,[]):
                ap=ts+8
                if img.mapped(ap-16,24) and img.u64(ap-16)==0 and img.executable(img.qword(ap)):aps.add(ap)
    return sorted(aps)
def rip_refs_to(img,target):
    refs=[]
    for fde in img.fdes:
        if not img.executable(fde[0]) or fde[1]-fde[0]>0x10000:continue
        for row in img.instructions(fde):
            for op in row.operands:
                if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP and row.address+row.size+int(op.mem.disp)==target:refs.append((fde,row.address))
    return refs

def entry_aliases(img,rows,upto):
    aliases={'rdi'}
    for row in rows[:upto]:
        if row.mnemonic=='mov' and len(row.operands)>=2 and row.operands[0].type==X86_OP_REG:
            dst=reg_family(img,row.operands[0].reg);src=row.operands[1]
            if src.type==X86_OP_REG and reg_family(img,src.reg) in aliases:aliases.add(dst)
            elif dst in aliases and dst!='rdi':aliases.discard(dst)
    return aliases

def member_binding(img,owner_class):
    if not owner_class:return {'classification':'LAST_SCALAR_MEMBER_BINDING_UNKNOWN','reason':'OWNER_UNKNOWN','proofs':[]}
    if 'authentication' not in owner_class.lower():return {'classification':'LAST_SCALAR_MEMBER_BINDING','binding':'REJECTED_OWNER_NOT_AUTH','owner_class':owner_class,'proofs':[]}
    proofs=[]
    for ap in type_vtables(img,owner_class):
        for fde,ref in rip_refs_to(img,ap):
            rows=img.instructions(fde); ri=next((i for i,r in enumerate(rows) if r.address==ref),None)
            if ri is None:continue
            # Constructor candidate only when vtable AP is stored into entry-this object.
            for i,row in enumerate(rows[ri:ri+12],start=ri):
                if row.mnemonic!='mov' or len(row.operands)<2:continue
                dst,src=row.operands[0],row.operands[1]
                if dst.type!=X86_OP_MEM or src.type!=X86_OP_REG:continue
                base=reg_family(img,dst.mem.base) if dst.mem.base else None
                if int(dst.mem.disp)!=0 or base not in entry_aliases(img,rows,i):continue
                # Look for an owner+0x20 store and a same-FDE control block with embedded handler+0x10.
                for j,m in enumerate(rows[i+1:],start=i+1):
                    if m.mnemonic!='mov' or len(m.operands)<2:continue
                    mdst,msrc=m.operands[0],m.operands[1]
                    if mdst.type!=X86_OP_MEM or int(mdst.mem.disp)!=0x20 or reg_family(img,mdst.mem.base)!=base or msrc.type!=X86_OP_REG:continue
                    source=reg_family(img,msrc.reg); handler=False; detail=[]
                    for prev in rows[max(i,j-100):j]:
                        if prev.mnemonic=='lea' and len(prev.operands)>=2 and prev.operands[0].type==X86_OP_REG and reg_family(img,prev.operands[0].reg)!='':
                            op=prev.operands[1]
                            if op.type==X86_OP_MEM and reg_family(img,op.mem.base)==source and int(op.mem.disp)==0x10:
                                child=reg_family(img,prev.operands[0].reg)
                                # Search handler vtable definition/store on child.
                                for later in rows[rows.index(prev)+1:j+1]:
                                    if later.mnemonic=='mov' and len(later.operands)>=2 and later.operands[0].type==X86_OP_MEM and reg_family(img,later.operands[0].mem.base)==child and int(later.operands[0].mem.disp)==0:
                                        handler=True;detail.append({'child_lea':hx(prev.address),'handler_store':hx(later.address)})
                    proofs.append({'constructor_fde':[hx(fde[0]),hx(fde[1])],'member_store':hx(m.address),'source_family':source,'embedded_handler_pattern':handler,'detail':detail})
    proven=[p for p in proofs if p['embedded_handler_pattern']]
    return {'classification':'LAST_SCALAR_MEMBER_BINDING','binding':'PROVEN' if len(proven)==1 else 'UNKNOWN','owner_class':owner_class,'proof_count':len(proven),'proofs':proofs}

def reassert(img):
    digest=hashlib.sha256(img.raw).hexdigest()
    if digest!=EXPECTED_SHA256 or len(img.raw)!=EXPECTED_SIZE:raise RuntimeError('exact client fence mismatch')
    if img.qword(HANDLER_VTABLE_AP+HANDLER_SLOT)!=HANDLER_SLOT_TARGET:raise RuntimeError('handler slot mismatch')
    if img.fde(TARGET_SITE)!=TARGET_FDE:raise RuntimeError(f'target FDE moved {img.fde(TARGET_SITE)}')
    rows=img.instructions(TARGET_FDE);by={r.address:r for r in rows}
    expected={0x16DA705:('mov','rdi, qword ptr [r14 + 0x10]'),0x16DA70E:('xor','edx, edx'),0x16DA713:('mov','rax, qword ptr [rdi]'),0x16DA716:('call','qword ptr [rax + 0x60]')}
    asserted=[]
    for a,e in expected.items():
        r=by.get(a)
        if not r or (r.mnemonic,r.op_str)!=e:raise RuntimeError(f'instruction mismatch {a:#x}: {None if not r else (r.mnemonic,r.op_str)}')
        asserted.append({'at':hx(a),'mnemonic':r.mnemonic,'operand':r.op_str})
    return {'classification':'LAST_SCALAR_EXACT_REASSERTION','fde':[hx(TARGET_FDE[0]),hx(TARGET_FDE[1])],'callsite':hx(TARGET_SITE),'edx_value':0,'instructions':asserted}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--client',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    img=Image(args.client); exact=reassert(img);owner=qmeta_owner(img);binding=member_binding(img,owner.get('owner_class'))
    classification='FIELD6_VALUE_UNKNOWN';value=None;accepted=None
    if owner['classification']=='LAST_SCALAR_QMETA_OWNER' and binding.get('binding')=='PROVEN':classification='FIELD6_VALUE_PROVEN';value=0;accepted={'callsite':hx(TARGET_SITE),'owner_class':owner['owner_class'],'owner_method':owner['owner_method']}
    result={'schema':'otclient.track-a.current-login-field6-last-scalar-owner.v1',**SAFETY,'exact_client':{'version':'15.32.75d4a0','sha256':hashlib.sha256(img.raw).hexdigest(),'size':len(img.raw)},'last_scalar_exact_reassertion':exact,'last_scalar_qmeta_owner':owner,'last_scalar_member_binding':binding,'classification':classification,'field6_value':value,'accepted_callsite':accepted,'scope_markers':{'NO_HEURISTIC_RANKING':True,'NO_SEMANTIC_GUESSING':True}}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('LAST_SCALAR_EXACT_REASSERTION=PASS');print('LAST_SCALAR_QMETA_OWNER='+owner['classification']);print('LAST_SCALAR_MEMBER_BINDING='+binding['classification']);print(classification+'=true');print('NO_HEURISTIC_RANKING=true');print('NO_SEMANTIC_GUESSING=true')
if __name__=='__main__':main()
