"""First normal-control transfer only; no callee execution or value inference."""
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET, CS_GRP_INT, CS_GRP_IRET
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP


def decoder():
    md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
    return md


def qualify_branch(raw,site,target):
    ins=next(decoder().disasm(raw,site,count=1),None)
    if not ins or ins.mnemonic!='jne' or len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM or ins.operands[0].imm!=target:
        raise ValueError('EXACT_CONTINUATION_BRANCH_NOT_QUALIFIED')


def bounded_region(fdes,entry):
    rows=[(lo,hi) for lo,hi in fdes if lo<=entry<hi]
    if len(rows)!=1 or not 0<rows[0][1]-rows[0][0]<=512:
        raise ValueError('NO_UNIQUE_BOUNDED_CONTINUATION_FDE')
    return rows[0]


def first_transfers(raw,base,entry):
    if not 0<len(raw)<=512 or not base<=entry<base+len(raw):
        raise ValueError('CONTINUATION_SCOPE_INVALID')
    md=decoder(); pending=[entry]; seen=set(); edges={}; boundaries=[]; complete=True
    def boundary(kind,site,target=None):
        row={'kind':kind,'site':hex(site)}
        if target is not None: row['target']=hex(target)
        boundaries.append(row)
    while pending:
        pc=pending.pop()
        if pc in seen: continue
        if len(seen)>=64:
            boundary('INSTRUCTION_LIMIT',pc); complete=False; break
        if not base<=pc<base+len(raw):
            boundary('OUTSIDE_REGION',pc); complete=False; continue
        ins=next(md.disasm(raw[pc-base:],pc,count=1),None)
        if ins is None:
            boundary('UNDECODED',pc); complete=False; continue
        seen.add(pc); edges[pc]=[]
        if ins.group(CS_GRP_CALL):
            if len(ins.operands)==1 and ins.operands[0].type==X86_OP_IMM:
                boundary('CALL',pc,ins.operands[0].imm)
            else: boundary('INDIRECT_CALL',pc); complete=False
            continue
        if ins.group(CS_GRP_RET): boundary('RETURN',pc); continue
        if ins.group(CS_GRP_INT) or ins.group(CS_GRP_IRET) or ins.mnemonic in ('ud2','hlt','syscall','sysenter','sysret','sysexit','xbegin'):
            boundary('UNMODELED_CONTROL',pc); complete=False; continue
        if ins.group(CS_GRP_JUMP) or ins.mnemonic in ('loop','loope','loopne','jcxz','jecxz','jrcxz'):
            if len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM:
                boundary('INDIRECT_BRANCH',pc); complete=False; continue
            targets=[ins.operands[0].imm]
            if ins.mnemonic!='jmp': targets.append(pc+ins.size)
        else: targets=[pc+ins.size]
        for target in targets:
            if not base<=target<base+len(raw):
                boundary('OUTSIDE_REGION',pc,target); complete=False
            else: edges[pc].append(target); pending.append(target)
    # Any reachable cycle can avoid the observed boundary indefinitely; do not
    # claim every normal path reaches a first transfer without a termination proof.
    active=set(); done=set()
    def cyclic(pc):
        if pc in active: return True
        if pc in done: return False
        active.add(pc)
        found=any(cyclic(n) for n in edges.get(pc,[]))
        active.remove(pc); done.add(pc)
        return found
    if cyclic(entry): boundary('CYCLE_UNPROVEN',entry); complete=False
    unique={tuple(sorted(r.items())):r for r in boundaries}
    return {'complete':complete,'reachable_instructions':len(seen),
            'cfg':{hex(pc):[hex(n) for n in sorted(set(edges[pc]))] for pc in sorted(edges)},
            'boundaries':sorted(unique.values(),key=lambda r:(int(r['site'],16),r['kind'],r.get('target','')))}


def plt_extent(sections,target):
    rows=[(lo,hi) for name,lo,hi in sections if name in ('.plt','.plt.sec','.plt.got') and lo<=target<hi]
    return min(16,rows[0][1]-target) if len(rows)==1 else None


def plt_binding(raw,base,relocations):
    rows=list(decoder().disasm(raw,base,count=2))
    if rows and rows[0].mnemonic=='endbr64': rows=rows[1:]
    if not rows: return None
    ins=rows[0]
    if ins.mnemonic!='jmp' or len(ins.operands)!=1: return None
    op=ins.operands[0]
    if op.type!=X86_OP_MEM or op.mem.base!=X86_REG_RIP or op.mem.index!=0 or op.mem.segment!=0: return None
    return relocations.get(ins.address+ins.size+op.mem.disp)
