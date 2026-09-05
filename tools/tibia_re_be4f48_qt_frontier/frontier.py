"""Bounded symbol-local first-transfer CFG, no target traversal."""
from capstone import (Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_CALL, CS_GRP_RET,
                      CS_GRP_JUMP, CS_GRP_INT, CS_GRP_IRET, CS_GRP_PRIVILEGE)
from capstone.x86_const import X86_OP_IMM

def selected_body(raw,sections,record):
    if any(record.get(k)!=v for k,v in dict(address='0x1d3ff0',size=85,section_index=14,symbol_index=3860).items()):
        raise ValueError('PROMOTED_DEFINITION_CHANGED')
    lo,hi=0x1d3ff0,0x1d4045
    owners=[s for s in sections if s['flags']&2 and s['size']>0 and s['addr']<hi and lo<s['addr']+s['size']]
    if len(owners)!=1 or owners[0]['index']!=14 or owners[0]['flags']&6!=6 or owners[0]['type']=='SHT_NOBITS':
        raise ValueError('SYMBOL_MAPPING')
    s=owners[0];offset=s['off']+lo-s['addr']
    if not s['addr']<=lo<hi<=s['addr']+s['size'] or not 0<=offset<offset+85<=len(raw):
        raise ValueError('SYMBOL_MAPPING')
    return raw[offset:offset+85]

def frontier(raw, base, instruction_limit=64):
    if not 0<len(raw)<=85: raise ValueError('SYMBOL_SCOPE_INVALID')
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    pending=[base];decoded={};edges={};boundaries=[];complete=True;limit=False
    def boundary(kind,site,target=None,known=True):
        nonlocal complete
        row=dict(kind=kind,site=hex(site))
        if target is not None:row['target']=hex(target)
        boundaries.append(row)
        if not known:complete=False
    while pending:
        pc=pending.pop()
        if pc in decoded:continue
        if len(decoded)>=min(instruction_limit,64):
            boundary('INSTRUCTION_LIMIT',pc,known=False);limit=True;break
        if not base<=pc<base+len(raw):
            boundary('FALLTHROUGH_OUTSIDE_SYMBOL',pc,known=False);continue
        ins=next(md.disasm(raw[pc-base:],pc,count=1),None)
        if ins is None:
            boundary('UNDECODED',pc,known=False);continue
        if any(lo<pc+ins.size and pc<hi for lo,hi in decoded.items()):
            boundary('OVERLAPPING_DECODE',pc,known=False);continue
        decoded[pc]=pc+ins.size;edges[pc]=[]
        if ins.group(CS_GRP_INT) or ins.group(CS_GRP_IRET) or ins.group(CS_GRP_PRIVILEGE) or ins.mnemonic in (
                'ud2','hlt','syscall','sysenter','sysret','sysexit','xbegin','xabort','xend','retf','retfq','lcall','ljmp'):
            boundary('UNMODELED_CONTROL',pc,known=False);continue
        if ins.group(CS_GRP_CALL):
            if len(ins.operands)==1 and ins.operands[0].type==X86_OP_IMM:
                boundary('CALL',pc,ins.operands[0].imm)
            else:boundary('INDIRECT_CALL',pc,known=False)
            continue
        if ins.group(CS_GRP_RET):boundary('RETURN',pc);continue
        if ins.group(CS_GRP_JUMP) or ins.mnemonic in ('loop','loope','loopne','jcxz','jecxz','jrcxz'):
            if len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM:
                boundary('INDIRECT_BRANCH',pc,known=False);continue
            target=ins.operands[0].imm
            if base<=target<base+len(raw):edges[pc].append(target);pending.append(target)
            else:boundary('TAIL_JUMP' if ins.mnemonic=='jmp' else 'CONDITIONAL_EXIT',pc,target)
            if ins.mnemonic=='jmp':continue
        fall=pc+ins.size
        if fall>=base+len(raw):boundary('FALLTHROUGH_OUTSIDE_SYMBOL',pc,fall,known=False)
        else:edges[pc].append(fall);pending.append(fall)
    active=set();done=set()
    def cycle(pc):
        if pc in active:return True
        if pc in done:return False
        active.add(pc)
        found=any(cycle(n) for n in edges.get(pc,[]))
        active.remove(pc);done.add(pc);return found
    cycle_present=cycle(base)
    unique={tuple(sorted(r.items())):r for r in boundaries}
    rows=sorted(unique.values(),key=lambda r:(int(r['site'],16),r['kind'],r.get('target','')))
    return dict(complete=complete,reachable_instructions=len(decoded),
                cfg={hex(pc):[hex(n) for n in sorted(set(edges[pc]))] for pc in sorted(edges)},
                boundaries=rows,cycle_present=cycle_present,limit_reached=limit,
                termination_proven=False,runtime_path_feasibility_proven=False)
