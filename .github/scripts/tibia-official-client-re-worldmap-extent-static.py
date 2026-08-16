#!/usr/bin/env python3
from __future__ import annotations
import argparse,bisect,hashlib,json,re,struct,sys
from collections import defaultdict,deque
from pathlib import Path
from capstone import CS_ARCH_X86,CS_MODE_64,Cs,CS_AC_READ,CS_AC_WRITE
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM,X86_OP_REG,X86_REG_RIP
from elftools.dwarf.callframe import FDE
from elftools.elf.elffile import ELFFile

SIZE=51965216
SHA='e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe'
TYPES={
 'TWorldMapExtent':'N5tibia8worldmap15TWorldMapExtentE',
 'TWorldMapSubfieldExtent':'N5tibia8worldmap23TWorldMapSubfieldExtentE',
 'TWorldMapViewport':'N5tibia8worldmap17TWorldMapViewportE',
 'TWorldMapStorage':'N5tibia8worldmap16TWorldMapStorageE',
 'TWorldmapProtocolMessageHandler':'N5tibia8worldmap31TWorldmapProtocolMessageHandlerE',
 'TWorldMapRenderProvider':'N5tibia8worldmap23TWorldMapRenderProviderE',
 'TWorldMapCamera':'N5tibia8renderer15TWorldMapCameraE',
 'TWorldMapPicker':'N5tibia8worldmap15TWorldMapPickerE'}
KEYS=('worldmap','world map','viewport','subfield','mapscale','map scale','oncameraviewportchanged','worldmappicker')
SMALL={7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,26,28,30,32,33,36,88,252,520,768,1008}

def req(v,m):
 if not v: print('WORLDMAP_STATIC_FAIL='+m,file=sys.stderr); raise SystemExit(2)
 print('WORLDMAP_STATIC_OK='+m)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

class V:
 def __init__(self,p):
  self.p=p; self.d=p.read_bytes(); self.f=p.open('rb'); self.e=ELFFile(self.f); self.s=[]
  for x in self.e.iter_segments():
   if x['p_type']=='PT_LOAD' and int(x['p_filesz']): self.s.append((int(x['p_vaddr']),int(x['p_offset']),int(x['p_filesz']),int(x['p_memsz']),int(x['p_flags'])))
  req(self.s,'load_segments')
 def close(self): self.f.close()
 def va(self,o):
  for a,b,n,_,_ in self.s:
   if b<=o<b+n:return a+o-b
 def off(self,a,n=1):
  for v,o,z,_,_ in self.s:
   if v<=a and a+n<=v+z:return o+a-v
 def read(self,a,n):
  o=self.off(a,n); return None if o is None else self.d[o:o+n]
 def u64(self,a):
  b=self.read(a,8); return None if b is None else struct.unpack('<Q',b)[0]
 def i64(self,a):
  b=self.read(a,8); return None if b is None else struct.unpack('<q',b)[0]
 def exe(self,a): return any(v<=a<v+m and f&1 for v,_,_,m,f in self.s)
 def find(self,b):
  out=[]; i=0
  while True:
   i=self.d.find(b,i)
   if i<0:return out
   a=self.va(i)
   if a is not None:out.append((i,a))
   i+=1
 def qrefs(self,targets):
  r=defaultdict(list)
  for _,o,n,_,_ in self.s:
   for p in range(o+((-o)&7),o+n-7,8):
    x=struct.unpack_from('<Q',self.d,p)[0]
    if x in targets:
     a=self.va(p)
     if a is not None:r[x].append(a)
  return r

def ranges(v):
 out={}
 try:
  for x in v.e.get_dwarf_info().EH_CFI_entries():
   if isinstance(x,FDE):
    a=int(x['initial_location']); b=a+int(x['address_range'])
    if a<b and v.exe(a):out[a]=(a,b)
 except Exception as e: print('WORLDMAP_STATIC_WARN=eh_frame:'+type(e).__name__,file=sys.stderr)
 req(out,'eh_frame_function_ranges'); return [out[k] for k in sorted(out)]
def lookup_fn(rs):
 starts=[a for a,_ in rs]
 def q(x):
  i=bisect.bisect_right(starts,x)-1
  return starts[i] if i>=0 and rs[i][0]<=x<rs[i][1] else None
 return q

def layouts(v):
 out={}; nvas=set()
 for k,m in TYPES.items():
  occ=v.find(m.encode()); out[k]={'mangled':m,'name_occurrences':[{'file_offset':o,'va':a} for o,a in occ],'typeinfo_candidates':[],'vtable_candidates':[]}; nvas|={a for _,a in occ}
 nref=v.qrefs(nvas); tis=set()
 for it in out.values():
  for x in it['name_occurrences']:
   for r in nref.get(x['va'],[]):
    a=r-8; first=v.u64(a)
    if first is not None:
     z={'va':a,'name_pointer_at':r,'typeinfo_vptr':first}
     if z not in it['typeinfo_candidates']:it['typeinfo_candidates'].append(z); tis.add(a)
 tref=v.qrefs(tis)
 for it in out.values():
  for ti in it['typeinfo_candidates']:
   for r in tref.get(ti['va'],[]):
    top=v.i64(r-8); first=v.u64(r+8)
    if top is None or first is None or abs(top)>0x100000 or not v.exe(first):continue
    ap=r+8; ent=[]; bad=0
    for i in range(96):
     f=v.u64(ap+i*8)
     if f is None:break
     if v.exe(f):ent.append({'slot':i,'function':f});bad=0
     else:
      bad+=1
      if ent and bad>=2:break
    it['vtable_candidates'].append({'start':r-8,'typeinfo_pointer_at':r,'address_point':ap,'offset_to_top':top,'entries':ent})
 return out

def strings(v):
 out={}
 for m in re.finditer(rb'[\x20-\x7e]{5,200}\x00',v.d):
  s=m.group()[:-1].decode('ascii','ignore'); low=s.lower()
  if any(k in low for k in KEYS):
   a=v.va(m.start())
   if a is not None:out[a]=s
 return out

def scan(v,rs,types,ss):
 q=lookup_fn(rs); labels=defaultdict(set); seeds=set()
 for k,it in types.items():
  for x in it['name_occurrences']:labels[x['va']].add('type_name:'+k)
  for x in it['typeinfo_candidates']:labels[x['va']].add('typeinfo:'+k)
  for x in it['vtable_candidates']:
   labels[x['start']].add('vtable_start:'+k);labels[x['address_point']].add('vtable_ap:'+k)
   for e in x['entries']:seeds.add(q(e['function']) or e['function'])
 for a,s in ss.items():labels[a].add('semantic:'+s[:100])
 text=v.e.get_section_by_name('.text');req(text is not None,'text_section');base=int(text['sh_addr'])
 md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True; refs=defaultdict(list);calls=defaultdict(set);rev=defaultdict(set)
 for ins in md.disasm(text.data(),base):
  fn=q(ins.address)
  if fn is None:continue
  if ins.mnemonic=='call' and ins.operands and ins.operands[0].type==X86_OP_IMM:
   t=int(ins.operands[0].imm)&((1<<64)-1); c=q(t) or t; calls[fn].add(c);rev[c].add(fn)
  for op in ins.operands:
   t=None
   if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:t=ins.address+ins.size+op.mem.disp
   elif op.type==X86_OP_IMM:t=int(op.imm)
   if t in labels:
    for l in labels[t]:refs[l].append({'function':fn,'instruction':ins.address,'target':t});seeds.add(fn)
 return refs,calls,rev,seeds

def expand(seeds,calls,rev,q):
 seen=set(seeds);d=deque((x,0) for x in seeds)
 while d:
  f,n=d.popleft()
  if n>=2:continue
  for x in set(calls.get(f,()))|set(rev.get(f,())):
   x=q(x) or x
   if x not in seen:seen.add(x);d.append((x,n+1))
 return seen

def fninfo(v,ab,md,targets):
 a,b=ab;raw=v.read(a,b-a)
 if raw is None:return {'start':a,'end':b,'unmapped':True}
 aliases={'rdi'};consts={}; fields={};writes=[];calls=[];regs={}
 def rn(i):return md.reg_name(i) or str(i)
 for ins in md.disasm(raw,a):
  ops=ins.operands
  if ins.mnemonic=='call' and ops and ops[0].type==X86_OP_IMM:calls.append(int(ops[0].imm)&((1<<64)-1))
  if ins.mnemonic in ('mov','lea') and len(ops)>=2 and ops[0].type==X86_OP_REG:
   dst=rn(ops[0].reg);src=ops[1]
   if src.type==X86_OP_REG:
    sn=rn(src.reg)
    if sn in aliases:aliases.add(dst)
    if sn in regs:regs[dst]=regs[sn]
    else:regs.pop(dst,None)
   elif src.type==X86_OP_IMM:regs[dst]=int(src.imm)
   elif src.type==X86_OP_MEM and src.mem.base and rn(src.mem.base) in aliases and src.mem.index==0 and src.mem.disp==0:aliases.add(dst);regs.pop(dst,None)
   else:regs.pop(dst,None)
  for i,op in enumerate(ops):
   if op.type==X86_OP_IMM:
    x=int(op.imm)
    if abs(x) in SMALL:consts[x]=consts.get(x,0)+1
   elif op.type==X86_OP_MEM:
    base=rn(op.mem.base) if op.mem.base else ''
    if base in aliases and op.mem.index==0 and 0<=op.mem.disp<=0x4000:
     ac='r' if op.access==CS_AC_READ else 'w' if op.access==CS_AC_WRITE else 'rw';key=(op.mem.disp,ac,ins.mnemonic);fields[key]=fields.get(key,0)+1
     if ac in ('w','rw') and i==0 and len(ops)>1:
      s=ops[1];val=None;src=''
      if s.type==X86_OP_IMM:val=int(s.imm);src='imm'
      elif s.type==X86_OP_REG and rn(s.reg) in regs:val=regs[rn(s.reg)];src='reg:'+rn(s.reg)
      if val is not None:writes.append({'instruction':ins.address,'offset':op.mem.disp,'value':val,'source':src})
 return {'start':a,'end':b,'size':b-a,'notable_constants':[{'value':x,'count':consts[x]} for x in sorted(consts,key=lambda z:(abs(z),z))], 'this_field_accesses':[{'offset':o,'access':ac,'mnemonic':mn,'count':n} for (o,ac,mn),n in sorted(fields.items())], 'this_constant_writes':writes,'direct_calls':sorted(set(calls))}

def main():
 p=argparse.ArgumentParser();p.add_argument('--client',type=Path,required=True);p.add_argument('--input-source',required=True);p.add_argument('--output-json',type=Path,required=True);p.add_argument('--output-text',type=Path,required=True);a=p.parse_args()
 req(a.client.is_file(),'client_present');req(a.client.stat().st_size==SIZE,'exact_client_size');sha=digest(a.client);req(sha==SHA,'exact_client_sha256')
 v=V(a.client)
 try:
  rs=ranges(v);q=lookup_fn(rs);types=layouts(v);ss=strings(v);req(ss,'worldmap_semantic_strings');refs,calls,rev,seeds=scan(v,rs,types,ss);req(seeds,'worldmap_seed_functions');rel=expand(seeds,calls,rev,q);by={x[0]:x for x in rs};md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
  targets=set(ss)
  for it in types.values():
   targets|={x['va'] for x in it['name_occurrences']}|{x['va'] for x in it['typeinfo_candidates']}
   for x in it['vtable_candidates']:targets|={x['start'],x['address_point']}
  funcs=[fninfo(v,by[x],md,targets) for x in sorted(rel) if x in by]
  fl=defaultdict(set)
  for l,xs in refs.items():
   for x in xs:fl[x['function']].add(l)
  edges=[]
  for f in sorted(rel):
   for c in sorted(calls.get(f,())):
    c=q(c) or c
    if c in rel and (fl.get(f) or fl.get(c)):edges.append({'caller':f,'callee':c,'caller_labels':sorted(fl.get(f,()))[:8],'callee_labels':sorted(fl.get(c,()))[:8]})
  hits=[]
  for f in funcs:
   vals={abs(x['value']) for x in f['notable_constants']};wr=[x for x in f['this_constant_writes'] if abs(int(x['value'])) in (14,18)]
   if 14 in vals or 18 in vals or wr:hits.append({'function':f['start'],'has_14':14 in vals,'has_18':18 in vals,'constant_writes_14_18':wr,'labels':sorted(fl.get(f['start'],()))[:16]})
  res={'schema_version':1,'exact_client':{'version':'15.32.df7b29','size':SIZE,'sha256':sha,'platform':'official_native_linux_only','source':a.input_source},'analysis':{'function_range_count':len(rs),'semantic_worldmap_string_count':len(ss),'seed_function_count':len(seeds),'relevant_function_count':len(funcs),'call_graph_depth':2},'types':types,'semantic_strings':[{'va':x,'text':ss[x]} for x in sorted(ss)],'code_refs':dict(sorted(refs.items())),'functions':funcs,'cross_edges':edges,'dimension_hits':hits,'classification':{'client_fence':'PROVEN','type_surface_inventory':'PROVEN_EXACT_RTTI_NAME_STRINGS','typeinfo_vtable_candidates':'CANDIDATE_STRUCTURAL','function_xrefs':'PROVEN_DIRECT_CODE_REFERENCES_WHERE_RECORDED','dimension_field_ownership':'REQUIRES_EVIDENCE_REVIEW','full_patch_graph':'REQUIRES_EVIDENCE_REVIEW'}}
  a.output_json.parent.mkdir(parents=True,exist_ok=True);a.output_json.write_text(json.dumps(res,indent=2,sort_keys=True))
  lines=['WORLDMAP_STATIC_RESULT=EXACT_CLIENT_GRAPH_EXTRACTED','WORLDMAP_STATIC_CLIENT_SHA256='+sha,'WORLDMAP_STATIC_FUNCTION_RANGES='+str(len(rs)),'WORLDMAP_STATIC_SEMANTIC_STRINGS='+str(len(ss)),'WORLDMAP_STATIC_SEED_FUNCTIONS='+str(len(seeds)),'WORLDMAP_STATIC_RELEVANT_FUNCTIONS='+str(len(funcs)),'WORLDMAP_STATIC_DIMENSION_HITS='+str(len(hits))]
  for k,it in types.items():lines.append(f"WORLDMAP_STATIC_TYPE={k};names={len(it['name_occurrences'])};typeinfo={len(it['typeinfo_candidates'])};vtables={len(it['vtable_candidates'])}")
  lines.append('WORLDMAP_STATIC_COMPLETE=true');a.output_text.write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
 finally:v.close()
 return 0
if __name__=='__main__':raise SystemExit(main())
