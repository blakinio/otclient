"""Bounded callee CFG; call fallthrough is explicitly conditional, not runtime proof."""
from capstone import CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET, CS_GRP_INT, CS_GRP_IRET
from capstone.x86_const import X86_OP_IMM
from continuation import decoder


def qualify_call(raw,site,target):
    ins=next(decoder().disasm(raw,site,count=1),None)
    if not ins or ins.mnemonic!='call' or len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM or ins.operands[0].imm!=target:
        raise ValueError('EXACT_CALLEE_CALLSITE_NOT_QUALIFIED')


def exact_owner(rows,entry,fde):
    candidates=[r for r in rows if r['address']==entry and r['section']!='SHN_UNDEF' and r['type']=='STT_FUNC']
    if len(candidates)!=1: return None
    row=candidates[0]
    return row['name'] if row['name'] and fde==(entry,entry+row['size']) and row['size']>0 else None


def callee_graph(raw,base):
    if not 0<len(raw)<=512: raise ValueError('CALLEE_SCOPE_INVALID')
    md=decoder(); pending=[base]; seen=set(); cfg={}; calls=[]; exits=[]; gaps=[]
    def gap(kind,pc): gaps.append({'kind':kind,'site':hex(pc)})
    while pending:
        pc=pending.pop()
        if pc in seen: continue
        if len(seen)>=64: gap('INSTRUCTION_LIMIT',pc); break
        if not base<=pc<base+len(raw): gap('UNPROVEN_FALLTHROUGH',pc); continue
        ins=next(md.disasm(raw[pc-base:],pc,count=1),None)
        if not ins: gap('UNDECODED',pc); continue
        seen.add(pc);cfg[pc]=[]
        if ins.group(CS_GRP_RET):
            exits.append({'kind':'RETURN','site':hex(pc)});continue
        if ins.group(CS_GRP_INT) or ins.group(CS_GRP_IRET) or ins.mnemonic in ('ud2','hlt','syscall','sysenter','sysret','sysexit','xbegin','xabort'):
            gap('UNMODELED_CONTROL',pc);continue
        if ins.group(CS_GRP_CALL):
            if len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM:
                gap('INDIRECT_CALL',pc);continue
            calls.append({'site':hex(pc),'target':hex(ins.operands[0].imm)})
            successors=[pc+ins.size]
            if pc+ins.size==base+len(raw):
                exits.append({'kind':'CALL_RETURN_OUTSIDE_FDE','site':hex(pc),'target':hex(pc+ins.size)})
                successors=[]
        elif ins.group(CS_GRP_JUMP) or ins.mnemonic in ('loop','loope','loopne','jcxz','jecxz','jrcxz'):
            if len(ins.operands)!=1 or ins.operands[0].type!=X86_OP_IMM:
                gap('INDIRECT_BRANCH',pc);continue
            target=ins.operands[0].imm;successors=[]
            if base<=target<base+len(raw): successors.append(target)
            else: exits.append({'kind':'DIRECT_TAIL' if ins.mnemonic=='jmp' else 'CONDITIONAL_EXIT','site':hex(pc),'target':hex(target)})
            if ins.mnemonic!='jmp': successors.append(pc+ins.size)
        else: successors=[pc+ins.size]
        cfg[pc]=successors;pending.extend(successors)
    # Only metadata and direct edges are facts. Sorting is a stable presentation
    # order; callers must use cfg, not numeric address order, for path ordering.
    return {'complete':not gaps,'reachable_instructions':len(seen),
            'cfg':{hex(pc):[hex(n) for n in sorted(set(cfg[pc]))] for pc in sorted(cfg)},
            'calls':sorted(calls,key=lambda x:int(x['site'],16)),
            'exits':sorted(exits,key=lambda x:int(x['site'],16)),
            'gaps':sorted(gaps,key=lambda x:int(x['site'],16)),
            'conditional_on_calls_returning':True,'exceptional_control_not_modeled':True,
            'runtime_return_or_throw_semantics_proven':False,'termination_proven':False,
            'numeric_list_order_is_execution_order':False,'pre_success_send_sequence_proven':False}
