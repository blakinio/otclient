#!/usr/bin/env python3
"""Bounded static dataflow. Output expressions are derived facts, never raw bytes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_OP_REG, X86_OP_MEM, X86_OP_IMM, X86_REG_RIP
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.dwarf.callframe import FDE

EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
VOLATILE = ("rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11")
UNKNOWN = "UNKNOWN"

def hx(v):
    return None if v is None else hex(v)

def verify_fence(raw, version):
    if version != EXPECTED_VERSION or len(raw) != EXPECTED_SIZE or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("EXACT_CLIENT_FENCE_MISMATCH")

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



def reg_name(md, value):
    name = md.reg_name(value)
    for full, aliases in {
        "rax": ("eax", "ax", "al", "ah"), "rbx": ("ebx", "bx", "bl", "bh"),
        "rcx": ("ecx", "cx", "cl", "ch"), "rdx": ("edx", "dx", "dl", "dh"),
        "rdi": ("edi", "di", "dil"), "rsi": ("esi", "si", "sil"),
        "rbp": ("ebp", "bp", "bpl"), "rsp": ("esp", "sp", "spl")
    }.items():
        if name in aliases:
            return full
    if name.startswith("r") and name[-1:] in ("d", "w", "b") and name[1:-1].isdigit():
        return name[:-1]
    return name

def add(a, b):
    if a == UNKNOWN or b == UNKNOWN:
        return UNKNOWN
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    if b == 0:
        return a
    if isinstance(a,str) and a.startswith('add(') and a.endswith(')') and isinstance(b,int):
        base,sep,off=a[4:-1].rpartition(',')
        try:
            return add(base,int(off,0)+b)
        except ValueError:
            pass
    return f"add({a},{hex(b) if isinstance(b, int) else b})"

def base_offset(a):
    if isinstance(a,int):
        return ('numeric',a)
    if isinstance(a,str) and a.startswith('add(') and a.endswith(')'):
        base,_,off=a[4:-1].rpartition(',')
        try:
            return base,int(off,0)
        except ValueError:
            pass
    return a,0

def address(md, ins, operand, regs):
    mem = operand.mem
    if mem.base == X86_REG_RIP:
        return ins.address + ins.size + mem.disp
    base = regs.get(reg_name(md, mem.base), UNKNOWN) if mem.base else 0
    if mem.index:
        idx = regs.get(reg_name(md, mem.index), UNKNOWN)
        if not isinstance(idx, int):
            return UNKNOWN
        base = add(base, idx * mem.scale)
    return add(base, mem.disp)

def value(md, ins, op, regs, memory):
    if op.type == X86_OP_IMM:
        return int(op.imm)
    if op.type == X86_OP_REG:
        return regs.get(reg_name(md, op.reg), UNKNOWN)
    if op.type == X86_OP_MEM:
        addr = address(md, ins, op, regs)
        if addr == UNKNOWN:
            return UNKNOWN
        if op.size==16 and (addr,8) in memory and (add(addr,8),8) in memory:
            return (memory[(addr,8)],memory[(add(addr,8),8)])
        return memory.get((addr, op.size), f"load{op.size * 8}({hex(addr) if isinstance(addr, int) else addr})")
    return UNKNOWN

def execute(md, ins, regs, memory, calls, stores, symbols=None):
    ops = ins.operands
    m = ins.mnemonic
    if m == "call":
        target = value(md, ins, ops[0], regs, memory)
        calls.append({"site": hex(ins.address), "target": hex(target) if isinstance(target, int) else target,
                      "receiver": regs.get("rdi", UNKNOWN),
                      "arguments": {r: regs.get(r, UNKNOWN) for r in ("rdi","rsi","rdx","rcx","r8","r9")}})
        symbol = symbols(target) if symbols and isinstance(target, int) else None
        for r in VOLATILE:
            regs[r] = UNKNOWN
        if symbol and symbol.startswith("_Znwm"):
            regs["rax"] = f"allocation:{hex(ins.address)}"
        return
    if m == "push":
        regs["rsp"] = add(regs.get("rsp", UNKNOWN), -8)
        memory[(regs["rsp"], 8)] = value(md, ins, ops[0], regs, memory)
        return
    if m == "pop":
        regs[reg_name(md, ops[0].reg)] = memory.get((regs.get("rsp"),8),UNKNOWN)
        regs["rsp"] = add(regs.get("rsp",UNKNOWN),8)
        return
    if m in ("cmp","test","nop","endbr64"):
        return
    if m == "lea":
        out = address(md, ins, ops[1], regs)
    elif m in ("mov","movabs","movq","movd","movdqa","movdqu","movaps","movups"):
        out = value(md, ins, ops[1], regs, memory)
    elif m in ("add","sub") and ops[0].type == X86_OP_REG:
        rhs = value(md, ins, ops[1], regs, memory)
        if m == "sub":
            rhs = -rhs if isinstance(rhs,int) else UNKNOWN
        out = add(value(md, ins, ops[0], regs,memory),rhs)
    elif m in ("xor","pxor") and len(ops)==2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg:
        out = 0
    else:
        # No invented semantics: kill every explicitly/implicitly written register.
        for r in ins.regs_access()[1]:
            regs[reg_name(md,r)] = UNKNOWN
        for op in ops:
            if op.type == X86_OP_MEM and op.access & 2:
                memory.clear()
        return
    dst = ops[0]
    if dst.type == X86_OP_REG:
        if dst.size < 8 and not isinstance(out,int):
            out = UNKNOWN
        elif dst.size < 8 and isinstance(out,int):
            out &= (1 << (dst.size * 8)) - 1
        regs[reg_name(md,dst.reg)] = out
    elif dst.type == X86_OP_MEM:
        addr = address(md,ins,dst,regs)
        if addr != UNKNOWN:
            base,off=base_offset(addr)
            for key in list(memory):
                oldbase,oldoff=base_offset(key[0])
                if base==oldbase and off < oldoff+key[1] and oldoff < off+dst.size:
                    del memory[key]
            memory[(addr,dst.size)] = out
            if dst.size==16 and isinstance(out,tuple) and len(out)==2:
                memory[(addr,8)],memory[(add(addr,8),8)]=out
            stores.append({"site":hex(ins.address),"address":addr,"width":dst.size,"value":out})
        else:
            memory.clear()

def trace_block(raw, start, initial=None, memory=None, symbols=None):
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    regs={r:f"arg:{r}" for r in ("rdi","rsi","rdx","rcx","r8","r9")}
    regs["rsp"]=0
    regs.update(initial or {})
    mem=dict(memory or {}); calls=[]; stores=[]
    stop="END_OF_BLOCK"; stop_site=None
    for ins in md.disasm(raw,start):
        if ins.mnemonic.startswith("j") or ins.mnemonic in ("ret","retq","loop"):
            stop="CONTROL_FLOW_BOUNDARY";stop_site=hex(ins.address);break
        execute(md,ins,regs,mem,calls,stores,symbols)
    return {"calls":calls,"stores":stores,"registers":regs,"memory":mem,
            "stop_reason":stop,"stop_site":stop_site,"receiver_identity":UNKNOWN}

def trace_paths(raw, start, initial=None, memory=None, symbols=None, max_steps=4000):
    """Enumerate only this FDE; loops and undecodable/out-of-range edges fail closed."""
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    insns={i.address:i for i in md.disasm(raw,start)}
    regs={r:f'arg:{r}' for r in ('rdi','rsi','rdx','rcx','r8','r9')}
    regs['rsp']=0; regs.update(initial or {})
    pending=[(start,regs,dict(memory or {}),None,frozenset())]
    calls=[];stores=[];tails=[];steps=0;complete=True;reason='ALL_PATHS_TERMINATED'
    while pending:
        pc,regs,mem,zero,visited=pending.pop()
        while pc in insns:
            steps+=1
            if pc in visited or steps>max_steps:
                complete=False;reason='LOOP_OR_PATH_BUDGET';break
            visited=visited|{pc}; ins=insns[pc]; nxt=pc+ins.size; m=ins.mnemonic
            if m.startswith('ret'):
                break
            if m.startswith('j'):
                target=value(md,ins,ins.operands[0],regs,mem)
                if m=='jmp':
                    if isinstance(target,int) and target in insns:
                        pc=target;continue
                    tails.append({'site':hex(pc),'target':hex(target) if isinstance(target,int) else target,
                                  'receiver':regs.get('rdi',UNKNOWN),
                                  'arguments':{r:regs.get(r,UNKNOWN) for r in ('rdi','rsi','rdx','rcx','r8','r9')}})
                    break
                taken = zero if m in ('je','jz') else (not zero if zero is not None else None) if m in ('jne','jnz') else None
                if taken is not False:
                    if not isinstance(target,int) or target not in insns:
                        complete=False;reason='BRANCH_OUTSIDE_FDE'
                    else:
                        pending.append((target,dict(regs),dict(mem),zero,visited))
                if taken is True:
                    break
                pc=nxt;continue
            if m in ('cmp','test'):
                a=value(md,ins,ins.operands[0],regs,mem);b=value(md,ins,ins.operands[1],regs,mem)
                zero=(a==b if m=='cmp' else (a&b)==0) if isinstance(a,int) and isinstance(b,int) else None
            elif ins.eflags:
                zero=None
            execute(md,ins,regs,mem,calls,stores,symbols)
            pc=nxt
        else:
            complete=False;reason='UNDECODED_FALLTHROUGH'
        if steps>max_steps:
            break
    def unique(rows):
        return [json.loads(s) for s in sorted({json.dumps(x,sort_keys=True) for x in rows})]
    return {'complete':complete,'stop_reason':reason,'calls':unique(calls),'stores':unique(stores),
            'tail_edges':unique(tails),'steps':steps}

def analyze(client, version, output):
    verify_fence(client.read_bytes(),version)
    img=Image(client)
    try:
        adapter_fde=img.containing_fde(0xbd3050)
        if not adapter_fde or adapter_fde[0]!=0xbd3050 or adapter_fde[1]-adapter_fde[0]>0x2000:
            raise ValueError("ADAPTER_FDE_NOT_UNIQUE_OR_BOUNDED")
        connection=trace_block(img.read(0x7c6b18,0x7c6b9f-0x7c6b18),0x7c6b18,
                               {"rbx":"promoted:entry_owner"},symbols=img.plt_symbol)
        slot=connection['registers'].get('r9',UNKNOWN)
        mem=connection['memory']
        slot_function=mem.get((add(slot,8),8))
        member=mem.get((add(slot,16),8))
        adjustment=mem.get((add(slot,24),8))
        if not isinstance(slot_function,int) or member!=0xbd3050 or adjustment!=0:
            raise ValueError('EXACT_QSLOT_CONSTRUCTION_NOT_PROVEN')
        slot_fde=img.containing_fde(slot_function)
        if not slot_fde or slot_fde[0]!=slot_function or slot_fde[1]-slot_fde[0]>0x2000:
            raise ValueError('QSLOT_FUNCTION_NOT_UNIQUE_OR_BOUNDED')
        dispatch=trace_paths(img.read(slot_fde[0],slot_fde[1]-slot_fde[0]),slot_fde[0],
                             {'rdi':1,'rsi':slot,'rdx':'qt:receiver','rcx':'qt:argv'},mem,img.plt_symbol)
        adapter_paths=trace_paths(img.read(adapter_fde[0],adapter_fde[1]-adapter_fde[0]),adapter_fde[0],symbols=img.plt_symbol)
        # This phase intentionally emits evidence without converting an incomplete
        # analyzer traversal into a scientific SOURCE_BLOCKER.
        adapter=trace_block(img.read(*[adapter_fde[0],adapter_fde[1]-adapter_fde[0]]),adapter_fde[0])
        for record in (connection,adapter):
            record.pop("memory")
        result={"schema":"otclient.track-a.be4f48-sendlogin-adapter-semantics.v1",
                "exact_client":{"version":version,"size":EXPECTED_SIZE,"sha256":EXPECTED_SHA256},
                "connection_prefix":connection,"adapter_entry_block":adapter,
                "qslot_dispatch_function":hex(slot_function),"qslot_fde":[hex(x) for x in slot_fde],
                "member_pointer":{"function":hex(member),"this_adjustment":adjustment},
                "qslot_invocation_operation_1":dispatch,"adapter_paths":adapter_paths,
                "adapter_fde":[hex(x) for x in adapter_fde],
                "terminal_result":"ANALYSIS_INCOMPLETE",
                "FIRST_MISSING_BOUNDARY":"COMPLETE_QSLOT_AND_ADAPTER_CONTROL_FLOW_ANALYSIS_REQUIRED",
                "sendlogin_receiver_identity":UNKNOWN,"sendlogin_causal_binding_proven":False,
                "field6_value":UNKNOWN,"pre_success_send_sequence":UNKNOWN,
                "runtime_access":"none","official_client_executed":False,
                "login_performed":False,"credentials_used":False,"process_memory_access":False,
                "packet_capture":False,"ocr_vision_used":False,"official_service_e2e_count":0,
                "track_b_pr_284_modified":False}
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
        return result
    finally:
        img.close()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--client",type=Path,required=True)
    p.add_argument("--version",required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    analyze(a.client,a.version,a.output)
