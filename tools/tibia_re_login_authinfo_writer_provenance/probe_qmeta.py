#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, re, struct
from dataclasses import dataclass
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.dwarf.callframe import FDE

@dataclass(frozen=True)
class Section:
    name: str; offset: int; size: int; va: int; flags: int

class Image:
    def __init__(self,path:Path):
        self.raw=path.read_bytes()
        with path.open('rb') as fh:
            elf=ELFFile(fh)
            self.sections=[Section(s.name,int(s['sh_offset']),int(s['sh_size']),int(s['sh_addr']),int(s['sh_flags'])) for s in elf.iter_sections() if int(s['sh_size'])]
            self.rel={}
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
    def mapped(self,va,n=1):
        try:o=self.va_to_off(va)
        except ValueError:return False
        return 0<=o<=len(self.raw)-n
    def executable(self,va):return any((s.flags&4) and s.va<=va<s.va+s.size for s in self.sections)
    def bytes(self,va,n):o=self.va_to_off(va);return self.raw[o:o+n]
    def u32(self,va):return struct.unpack_from('<I',self.raw,self.va_to_off(va))[0]
    def i32(self,va):return struct.unpack_from('<i',self.raw,self.va_to_off(va))[0]
    def u64(self,va):return struct.unpack_from('<Q',self.raw,self.va_to_off(va))[0]
    def qword(self,va):return self.rel.get(va,self.u64(va) if self.mapped(va,8) else 0)
    def occ(self,text):
        needle=text.encode();out=[];p=0
        while True:
            p=self.raw.find(needle,p)
            if p<0:return out
            va=self.off_to_va(p)
            if va is not None:out.append(va)
            p+=1
    def fde(self,va):
        rows=[x for x in self.fdes if x[0]<=va<x[1]]
        return rows[0] if len(rows)==1 else None
    def snapshot(self,va,limit=500):
        f=self.fde(va)
        if not f:return {'fde':None,'instructions':[]}
        rows=[]
        for i in list(self.md.disasm(self.bytes(f[0],f[1]-f[0]),f[0]))[:limit]:rows.append({'at':hx(i.address),'mnemonic':i.mnemonic,'operand':i.op_str})
        return {'fde':[hx(f[0]),hx(f[1])],'instructions':rows}

def hx(x):return f'0x{x:x}'
def mangled(full):return 'N'+''.join(str(len(x))+x for x in full.split('::'))+'E'

def exact_vtable(img,simple,full):
    expected=mangled(full); rows=[]
    for at in img.occ(simple):
        off=img.va_to_off(at); a=img.raw.rfind(b'\0',max(0,off-192),off)+1; b=img.raw.find(b'\0',off,min(len(img.raw),off+512))
        if b<0:continue
        try:name=img.raw[a:b].decode('ascii')
        except UnicodeDecodeError:continue
        if name!=expected:continue
        nva=img.off_to_va(a)
        for where,val in img.rel.items():
            if val!=nva:continue
            rtti=where-8
            for ts,tv in img.rel.items():
                if tv!=rtti:continue
                ap=ts+8
                if not img.mapped(ap-16,24) or img.u64(ap-16)!=0:continue
                slots=[]
                for off2 in range(0,0xc0,8):
                    if not img.mapped(ap+off2,8):break
                    t=img.qword(ap+off2);slots.append({'offset':hex(off2),'target':hx(t),'executable':img.executable(t)})
                rows.append({'rtti_name':name,'rtti':hx(rtti),'address_point':hx(ap),'slots':slots})
    unique={(r['rtti'],r['address_point']):r for r in rows}
    if len(unique)!=1:raise RuntimeError(f'{full}: {len(unique)} candidates')
    return next(iter(unique.values()))

def safe_cstr(img,va,limit=192):
    if not img.mapped(va):return None
    raw=img.raw[img.va_to_off(va):img.va_to_off(va)+limit]; n=raw.find(b'\0')
    if n<2:return None
    raw=raw[:n]
    if not all(0x20<=c<=0x7e for c in raw):return None
    try:return raw.decode('ascii')
    except UnicodeDecodeError:return None

def context(img,site,before=8,after=8):
    f=img.fde(site)
    if not f:return []
    ins=list(img.md.disasm(img.bytes(f[0],f[1]-f[0]),f[0])); idx=[n for n,x in enumerate(ins) if x.address==site]
    if len(idx)!=1:return []
    k=idx[0];return [{'at':hx(x.address),'mnemonic':x.mnemonic,'operand':x.op_str} for x in ins[max(0,k-before):k+after+1]]

def refscan(img,targets):
    rip={x:[] for x in targets}; direct={x:[] for x in targets}
    for s in img.sections:
        if not(s.flags&4):continue
        for ins in img.md.disasm(img.raw[s.offset:s.offset+s.size],s.va):
            if ins.mnemonic=='call' and ins.operands and ins.operands[0].type==X86_OP_IMM:
                t=int(ins.operands[0].imm)
                if t in direct:direct[t].append(ins.address)
            for op in ins.operands:
                if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
                    t=ins.address+ins.size+int(op.mem.disp)
                    if t in rip:rip[t].append(ins.address)
    return rip,direct

def qstring(img,base,index):
    ent=base+index*8; rel=img.u32(ent); ln=img.u32(ent+4)
    if ln>4096:raise ValueError
    return img.bytes(base+rel,ln).decode('utf-8')

def stringdata_bases_for_literal(img,literal):
    out=set(); ln=len(literal.encode())
    for sva in img.occ(literal):
        lo=max(0,img.va_to_off(sva)-0x10000); hi=img.va_to_off(sva)
        for eoff in range(lo,hi+1,4):
            eva=img.off_to_va(eoff)
            if eva is None or not img.mapped(eva,8):continue
            try:
                rel=img.u32(eva); l=img.u32(eva+4)
            except Exception:continue
            if l!=ln or rel>0x20000:continue
            base=sva-rel
            if base>eva or (eva-base)%8:continue
            idx=(eva-base)//8
            try:
                if qstring(img,base,idx)==literal and qstring(img,base,0):out.add(base)
            except Exception:pass
    return sorted(out)

def parse_meta(img,sbase,mbase):
    if not img.mapped(mbase,56):return None
    try:h=[img.u32(mbase+i*4) for i in range(14)]
    except Exception:return None
    rev,ci,cic,cio,mc,mo,pc,po,ec,eo,cc,co,flags,sc=h
    if not(7<=rev<=20 and ci==0 and 0<mc<=1000 and 14<=mo<200000 and sc<=mc):return None
    rows=[]
    try:
        for i in range(mc):
            p=mbase+(mo+i*6)*4; r=[img.u32(p+j*4) for j in range(6)]; name=qstring(img,sbase,r[0])
            if not name:return None
            rows.append({'index':i,'name':name,'argc':r[1],'param_offset':r[2],'flags':r[4],'meta_type_offset':r[5]})
    except Exception:return None
    return {'revision':rev,'class_name':qstring(img,sbase,0),'method_count':mc,'signal_count':sc,'rows':rows}

def meta_for_method(img,method):
    out=[]
    for sbase in stringdata_bases_for_literal(img,method):
        for mbase in range(max(0,sbase-0x20000)&~3,sbase+0x20000,4):
            m=parse_meta(img,sbase,mbase)
            if not m or method not in {x['name'] for x in m['rows']}:continue
            static=[]
            for where,val in img.rel.items():
                if val==sbase and img.rel.get(where+8)==mbase:
                    st=img.rel.get(where+16)
                    if st is not None and img.executable(st):static.append({'qmetaobject':hx(where-8),'static_metacall':hx(st)})
            out.append({'stringdata':hx(sbase),'metadata':hx(mbase),**m,'static':static})
    uniq={(x['stringdata'],x['metadata']):x for x in out}
    return list(uniq.values())

def neighborhood(img,term,radius=0x1000):
    rows=[]
    for va in img.occ(term)[:8]:
        off=img.va_to_off(va); lo=max(0,off-radius); hi=min(len(img.raw),off+radius)
        strings=[]
        for m in re.finditer(rb'[ -~]{3,160}\x00',img.raw[lo:hi]):
            txt=m.group()[:-1].decode('ascii','ignore')
            sva=img.off_to_va(lo+m.start())
            if sva is not None:strings.append({'va':hx(sva),'text':txt})
        rows.append({'occurrence':hx(va),'strings':strings[:180]})
    return rows

def main():
    a=argparse.ArgumentParser();a.add_argument('--client',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    img=Image(args.client)
    auth=exact_vtable(img,'TAuthenticationAndEncryptionInfo','tibia::authentication::TAuthenticationAndEncryptionInfo')
    handler=exact_vtable(img,'TLoginProtocolMessageHandler','tibia::authentication::TLoginProtocolMessageHandler')
    auth_targets={r['offset']:int(r['target'],16) for r in auth['slots'] if r['executable']}
    producer=next(int(r['target'],16) for r in handler['slots'] if r['offset']=='0x60')
    targets=set(auth_targets.values())|{producer,int(auth['address_point'],16),int(handler['address_point'],16)}
    rip,direct=refscan(img,targets)
    slot_rows={}
    for off,t in auth_targets.items():
        sites=sorted(set(rip.get(t,[])+direct.get(t,[])))[:120]
        slot_rows[off]={'target':hx(t),'snapshot':img.snapshot(t,260),'rip_refs':[hx(x) for x in rip.get(t,[])[:200]],'direct_calls':[hx(x) for x in direct.get(t,[])[:200]],'contexts':[{'site':hx(x),'fde':('.'.join(hx(y) for y in img.fde(x)) if img.fde(x) else None),'context':context(img,x)} for x in sites]}
    methods=['sendLoginMessage','onLoginFinishedSuccessfullyEntered','onConfirmationCodeLoginSuccessful','loginSuccessful','receivedLoginChallengeMessage']
    qmeta={m:meta_for_method(img,m) for m in methods}
    terms=['TAuthenticationAndEncryptionInfo','TLoginProtocolMessageHandler','TPlaySessionData','sendLoginMessage','onLoginFinishedSuccessfullyEntered','onConfirmationCodeLoginSuccessful','loginSuccessful','session','character','password','token','challenge']
    result={
      'schema':'otclient.track-a.current-game-login-field-provenance.qmeta.v1',
      'runtime_access':'none','login_performed':False,'secret_access':False,'raw_client_uploaded':False,
      'authentication_info':auth,'login_handler':handler,
      'producer':{'target':hx(producer),'snapshot':img.snapshot(producer,1800),'rip_refs':[hx(x) for x in rip.get(producer,[])],'direct_calls':[hx(x) for x in direct.get(producer,[])], 'contexts':[{'site':hx(x),'context':context(img,x)} for x in sorted(set(rip.get(producer,[])+direct.get(producer,[])))[:120]]},
      'auth_slots':slot_rows,
      'auth_vtable_refs':[{'site':hx(x),'context':context(img,x)} for x in rip.get(int(auth['address_point'],16),[])[:120]],
      'handler_vtable_refs':[{'site':hx(x),'context':context(img,x)} for x in rip.get(int(handler['address_point'],16),[])[:120]],
      'qmeta_by_method':qmeta,
      'string_neighborhoods':{t:neighborhood(img,t) for t in terms},
      'classification':{'user_facing_semantic_field_names':'UNKNOWN','password_session_to_rsa_field_mapping':'UNKNOWN'}
    }
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('CURRENT_GAME_LOGIN_FIELD_QMETA_PROVENANCE=PASS')
    print('AUTH_EXECUTABLE_SLOT_COUNT='+str(len(auth_targets)))
    for m,rows in qmeta.items():print(f'QMETA_METHOD_{m}={len(rows)}')
    print('RAW_CLIENT_UPLOADED=false');print('LOGIN_PERFORMED=false');print('SECRET_ACCESS=false')

if __name__=='__main__':main()
