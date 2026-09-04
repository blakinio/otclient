#!/usr/bin/env python3
"""Exact queue metadata and a numeric static-metacall path, not registration."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_IMM, X86_OP_REG, X86_OP_MEM, X86_REG_RIP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.dwarf.callframe import FDE

VERSION='15.32.be4f48'
SIZE=52105824
SHA='552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'

def verify_fence(raw,version):
    if version!=VERSION or len(raw)!=SIZE or hashlib.sha256(raw).hexdigest()!=SHA:
        raise ValueError('EXACT_CLIENT_FENCE_MISMATCH')

def method_row(metadata,offset,index,count,signals):
    if not (14<=offset<=4096 and 0<=index<count<=4096 and index<signals<=count):
        raise ValueError('INVALID_EXACT_METHOD_INDEX')
    return metadata+offset*4+index*24

def classify_edge(edge):
    return {'connection_proven':False,'classification':'NUMERIC_DISPATCH_ONLY',
            'next_endpoint_identity':'UNKNOWN'}

def reg(md,op):
    n=md.reg_name(op.reg)
    groups={'rax':['eax','ax','al','ah'],'rbx':['ebx','bx','bl','bh'],
            'rcx':['ecx','cx','cl','ch'],'rdx':['edx','dx','dl','dh'],
            'rdi':['edi','di','dil'],'rsi':['esi','si','sil'],
            'rbp':['ebp','bp','bpl'],'rsp':['esp','sp','spl']}
    for full,aliases in groups.items():
        if n in aliases:return full
    if n.startswith('r') and n[-1:] in ('d','w','b') and n[1:-1].isdigit():return n[:-1]
    return n

def walk(raw,start,initial,read=None,max_steps=200):
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    code={i.address:i for i in md.disasm(raw,start)}
    regs={'rdi':'entry:object','rcx':'entry:argv'};regs.update(initial)
    flags=None;pc=start;seen=set();trace=[]
    def addr(ins,op):
        m=op.mem
        if m.base==X86_REG_RIP:return ins.address+ins.size+m.disp
        b=regs.get(md.reg_name(m.base)) if m.base else 0
        ix=regs.get(md.reg_name(m.index)) if m.index else 0
        return b+ix*m.scale+m.disp if isinstance(b,int) and isinstance(ix,int) else None
    def val(ins,op):
        if op.type==X86_OP_IMM:return int(op.imm)
        if op.type==X86_OP_REG:
            v=regs.get(reg(md,op))
            if isinstance(v,int):
                if md.reg_name(op.reg) in ('ah','bh','ch','dh'):v>>=8
                return v&((1<<(op.size*8))-1)
            return v if op.size==8 else None
        if op.type==X86_OP_MEM:
            a=addr(ins,op)
            if isinstance(a,int) and read:
                try:return int.from_bytes(read(a,op.size),'little')
                except ValueError:return None
        return None
    def result(stop,edge=None):return {'stop':stop,'steps':len(trace),'edge':edge,'path':trace}
    while pc in code:
        if pc in seen or len(trace)>=max_steps:return result('LOOP_OR_BUDGET')
        seen.add(pc);i=code[pc];m=i.mnemonic;ops=i.operands;nxt=pc+i.size
        trace.append({'site':hex(pc),'operation':m})
        if m.startswith('ret'):return result('EDGE_REACHED',{'kind':'return','site':hex(pc)})
        if m.startswith('loop') or m in ('jrcxz','jecxz','jcxz'):return result('UNSUPPORTED_CONTROL_FLOW')
        if m=='call' or m=='jmp':
            target=val(i,ops[0])
            if m=='jmp' and isinstance(target,int) and target in code:pc=target;continue
            return result('EDGE_REACHED' if isinstance(target,int) else 'UNRESOLVED_TARGET',
                          {'kind':'call' if m=='call' else 'tail','site':hex(pc),
                           'target':hex(target) if isinstance(target,int) else 'UNKNOWN',
                           'receiver':regs.get('rdi','UNKNOWN')})
        if m.startswith('j'):
            if flags is None:return result('UNPROVEN_BRANCH_PREDICATE')
            z,c,s,o=flags
            choices={'je':z,'jz':z,'jne':not z,'jnz':not z,'ja':not c and not z,
                     'jae':not c,'jb':c,'jbe':c or z,'jg':not z and s==o,
                     'jge':s==o,'jl':s!=o,'jle':z or s!=o,'js':s,'jns':not s}
            if m not in choices:return result('UNSUPPORTED_BRANCH')
            target=val(i,ops[0]);trace[-1]['taken']=choices[m]
            pc=target if choices[m] else nxt;continue
        if m in ('cmp','test'):
            a,b=val(i,ops[0]),val(i,ops[1]);flags=None
            if isinstance(a,int) and isinstance(b,int):
                bits=ops[0].size*8;mask=(1<<bits)-1;a&=mask;b&=mask
                v=((a-b) if m=='cmp' else a&b)&mask
                flags=(v==0,a<b if m=='cmp' else False,bool(v>>(bits-1)),
                       bool(((a^b)&(a^v))>>(bits-1)) if m=='cmp' else False)
        elif m in ('mov','movabs','movsxd','movsx','movzx','lea','add','sub','xor') and ops[0].type==X86_OP_REG:
            out=addr(i,ops[1]) if m=='lea' else val(i,ops[1])
            if m in ('movsxd','movsx') and isinstance(out,int):
                bits=ops[1].size*8
                if out&(1<<(bits-1)):out-=1<<bits
            if m in ('add','sub','xor'):
                old=val(i,ops[0])
                if m=='xor' and ops[1].type==X86_OP_REG and ops[0].reg==ops[1].reg:out=0
                elif isinstance(old,int) and isinstance(out,int):out=old+out if m=='add' else old-out if m=='sub' else old^out
                else:out=None
            if ops[0].size<4:out=None
            elif isinstance(out,int):out&=(1<<(ops[0].size*8))-1
            elif ops[0].size<8:out=None
            regs[reg(md,ops[0])]=out
            if i.eflags:flags=None
        elif m not in ('nop','endbr64'):
            # A stack write, implicit write, or unsupported semantic is not skipped.
            return result('UNSUPPORTED_INSTRUCTION')
        pc=nxt
    return result('OUTSIDE_DECODED_FDE')

def analyze(img):
    meta=0x30b73e0;strings=img.qword(meta+8);data=img.qword(meta+16);fn=img.qword(meta+24)
    def u32(a):return int.from_bytes(img.read(a,4),'little')
    def string(index):
        if not 0<=index<4096:raise ValueError('STRING_INDEX_OUTSIDE_BOUND')
        off=u32(strings+index*8);length=u32(strings+index*8+4)
        if not 0<length<128 or off>0x100000:raise ValueError('STRING_OUTSIDE_BOUND')
        return img.read(strings+off,length).decode('utf-8')
    header=[u32(data+i*4) for i in range(14)]
    if header[0]!=10:raise ValueError('UNQUALIFIED_QMETA_REVISION')
    row=method_row(data,header[5],191,header[4],header[13])
    owner=string(header[1]);name=string(u32(row))
    if owner!='tibia::protocol::TProtocolMessageQueue' or name!='clientMessageReadyToProcess' or row!=0x1ce47c0:
        raise ValueError('EXACT_QMETA_TUPLE_MISMATCH')
    fde=img.containing_fde(fn)
    if not fde or fde[0]!=fn or fde[1]-fde[0]>65536:raise ValueError('NON_UNIQUE_OR_UNBOUNDED_STATIC_METACALL')
    path=walk(img.read(fde[0],fde[1]-fde[0]),fde[0],{'rsi':0,'rdx':191},img.read)
    edge=path.get('edge') or {}
    proven=path['stop']=='EDGE_REACHED' and edge.get('target')=='0xbd2190' and edge.get('receiver')=='entry:object'
    return {'schema':'otclient.track-a.be4f48-queue-qmeta-index.v1',
            'exact_client':{'version':VERSION,'size':SIZE,'sha256':SHA},
            'queue_static_metaobject':hex(meta),'queue_signal_index':'0xbf','queue_signal_method_row':hex(row),
            'queue_owner':owner,'queue_signal_name':name,'qmeta_revision':header[0],
            'static_metacall':hex(fn),'static_metacall_fde':[hex(x) for x in fde],
            'conditional_numeric_inputs':{'esi':0,'edx':'0xbf'},'selected_path':path,
            'index_to_signal_dispatch_proven':proven,'connection_registration_proven':False,
            'terminal_result':'SOURCE_BLOCKER' if proven else 'ANALYSIS_INCOMPLETE',
            'FIRST_MISSING_BOUNDARY':'EXACT_STATIC_METACALL_DISPATCH_DOES_NOT_IDENTIFY_CONNECTION_REGISTRATION' if proven else 'COMPLETE_SELECTED_STATIC_METACALL_PATH_REQUIRED',
            'classification':classify_edge(edge),'next_endpoint_identity':'UNKNOWN','final_writer_contract':'UNKNOWN',
            'field6_value':'UNKNOWN','pre_success_send_sequence':'UNKNOWN','runtime_access':'none',
            'official_client_executed':False,'login_performed':False,'credentials_used':False,
            'process_memory_access':False,'packet_capture':False,'ocr_vision_used':False,
            'official_service_e2e_count':0,'track_b_pr_284_modified':False}

class Image:
    def __init__(self, path: Path) -> None:
        self.raw = path.read_bytes()
        self.handle = path.open("rb")
        self.elf = ELFFile(self.handle)
        self.sections: list[tuple[int, int, int, int]] = []
        for sec in self.elf.iter_sections():
            start = int(sec["sh_addr"])
            size = int(sec["sh_size"])
            off = int(sec["sh_offset"])
            flags = int(sec["sh_flags"])
            if start and size:
                self.sections.append((start, start + size, off, flags))

        self.relative_relocations: dict[int, int] = {}
        self.symbol_relocations: dict[int, str] = {}
        for sec in self.elf.iter_sections():
            if not isinstance(sec, RelocationSection):
                continue
            symtab = self.elf.get_section(sec["sh_link"]) if sec["sh_link"] else None
            for rel in sec.iter_relocations():
                addr = int(rel["r_offset"])
                if int(rel["r_info_type"]) == 8 and rel.is_RELA():
                    self.relative_relocations[addr] = int(rel["r_addend"]) & 0xFFFFFFFFFFFFFFFF
                idx = int(rel["r_info_sym"])
                if symtab is not None and idx:
                    try:
                        name = symtab.get_symbol(idx).name or ""
                    except Exception:
                        name = ""
                    if name:
                        self.symbol_relocations[addr] = name

        dwarf = self.elf.get_dwarf_info()
        self.fdes = sorted(
            (int(entry["initial_location"]), int(entry["initial_location"]) + int(entry["address_range"]))
            for entry in dwarf.EH_CFI_entries()
            if isinstance(entry, FDE)
        )
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
        self.md.detail = True

    def close(self) -> None:
        self.handle.close()

    def loc(self, va: int, size: int = 1) -> int:
        for lo, hi, off, _flags in self.sections:
            if lo <= va and va + size <= hi:
                return off + va - lo
        raise ValueError(f"unmapped {hx(va)}")

    def read(self, va: int, size: int) -> bytes:
        off = self.loc(va, size)
        return self.raw[off : off + size]

    def disassemble(self, lo: int, hi: int) -> list[Any]:
        return list(self.md.disasm(self.read(lo, hi - lo), lo))

    def containing_fde(self, va: int) -> tuple[int, int] | None:
        rows = [(lo, hi) for lo, hi in self.fdes if lo <= va < hi]
        return rows[0] if len(rows) == 1 else None

    def qword(self, va: int) -> int | None:
        if va in self.relative_relocations:
            return self.relative_relocations[va]
        try:
            return int.from_bytes(self.read(va, 8), "little")
        except Exception:
            return None

    def cstring(self, va: int, limit: int = 512) -> str | None:
        try:
            off = self.loc(va)
        except Exception:
            return None
        end = self.raw.find(b"\0", off, min(len(self.raw), off + limit))
        if end < 0:
            return None
        try:
            return self.raw[off:end].decode("utf-8")
        except UnicodeDecodeError:
            return None

    def plt_symbol(self, target: int) -> str | None:
        try:
            rows = self.disassemble(target, target + 24)
        except Exception:
            return None
        for ins in rows[:4]:
            if ins.mnemonic != "jmp" or not ins.operands:
                continue
            op = ins.operands[0]
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                got = int(ins.address) + int(ins.size) + int(op.mem.disp)
                if got in self.symbol_relocations:
                    return self.symbol_relocations[got]
        return None




if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--client',type=Path,required=True);p.add_argument('--version',required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();verify_fence(args.client.read_bytes(),args.version)
    img=Image(args.client)
    try:result=analyze(img)
    finally:img.close()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
