"""Finite must-identity dataflow over one FDE; no concrete loop unrolling."""
from collections import deque
from capstone import Cs,CS_ARCH_X86,CS_MODE_64
from capstone.x86_const import X86_OP_REG,X86_OP_MEM,X86_OP_IMM
from static_flow import reg_name

ARGS=('rdi','rsi','rdx','rcx','r8','r9')
VOLATILE=('rax','rcx','rdx','rsi','rdi','r8','r9','r10','r11')

def receiver_flow(raw,start,max_updates=20000):
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
    code={i.address:i for i in md.disasm(raw,start)}
    # State: registers definitely equal to entry receiver, exact private stack
    # pointer offsets, stack slots definitely holding that receiver. Join is meet.
    initial=(frozenset({'rcx'}),{'rsp':0},frozenset())
    states={start:initial};pending=deque([start]);updates=0;frontiers={}
    def join(a,b):
        return (a[0]&b[0],{r:v for r,v in a[1].items() if b[1].get(r)==v},a[2]&b[2])
    def event(kind,site,target=None,condition=None,state=None):
        row={'kind':kind,'site':hex(site)}
        if target is not None:row['target']=hex(target)
        if condition:row.update(condition=condition,taken='conditional_not_evaluated')
        if state is not None:row['receiver_registers']=sorted(state[0])
        frontiers[(kind,site,target)]=row
    def submit(target,state,site,condition=None):
        if target not in code:
            kind='UNDECODED_INTERNAL_TARGET' if start<=target<start+len(raw) else 'BRANCH_OUTSIDE_FDE' if condition else 'UNDECODED_FALLTHROUGH'
            event(kind,site,target,condition,state);return
        new=join(states[target],state) if target in states else state
        if target not in states or new!=states[target]:states[target]=new;pending.append(target)
    while pending:
        pc=pending.popleft();updates+=1
        if updates>max_updates:event('FIXPOINT_BUDGET',pc);break
        if pc not in code:event('UNDECODED_ENTRY',pc);continue
        i=code[pc];m=i.mnemonic;ops=i.operands;nxt=pc+i.size
        known,sp,mem=states[pc];known=set(known);sp=dict(sp);mem=set(mem)
        def reg(op):return reg_name(md,op.reg)
        def address(op):
            if op.type!=X86_OP_MEM or op.mem.index:return None
            b=sp.get(reg_name(md,op.mem.base)) if op.mem.base else None
            return b+op.mem.disp if b is not None else None
        def identity(op):
            return (op.type==X86_OP_REG and op.size==8 and reg(op) in known) or (op.type==X86_OP_MEM and op.size==8 and address(op) in mem)
        def setreg(name,bit,offset=None):
            known.discard(name);sp.pop(name,None)
            if bit:known.add(name)
            if offset is not None and -4096<=offset<=0:sp[name]=offset
        def state():return (frozenset(known),sp,frozenset(mem))
        if m.startswith('ret'):continue
        if m.startswith('loop') or m in ('jrcxz','jecxz','jcxz'):
            event('UNSUPPORTED_CONTROL_FLOW',pc,state=state());continue
        if m.startswith('j'):
            if not ops or ops[0].type!=X86_OP_IMM:
                event('UNRESOLVED_BRANCH',pc,state=state());continue
            submit(int(ops[0].imm),state(),pc,m)
            if m!='jmp':submit(nxt,state(),pc)
            continue
        if m=='call':
            for r in VOLATILE:known.discard(r);sp.pop(r,None)
            mem.clear()
        elif m=='push':
            if ops[0].size!=8:event('UNSUPPORTED_STACK_WIDTH',pc);continue
            off=sp.get('rsp');bit=identity(ops[0])
            if off is None or off-8 < -4096:event('UNPROVEN_STACK',pc);continue
            off-=8;mem.discard(off)
            if bit:mem.add(off)
            sp['rsp']=off
        elif m=='pop':
            if ops[0].type!=X86_OP_REG or ops[0].size!=8 or reg(ops[0])=='rsp':event('UNSUPPORTED_STACK_POP',pc);continue
            off=sp.get('rsp')
            if off is None or not -4096<=off<=-8:event('UNPROVEN_STACK',pc);continue
            setreg(reg(ops[0]),off in mem);mem.discard(off);sp['rsp']=off+8
        elif m in ('mov','movabs') and ops[0].type==X86_OP_REG:
            bit=identity(ops[1]) if ops[0].size==8 else False
            offset=sp.get(reg(ops[1])) if ops[1].type==X86_OP_REG and ops[0].size==8 and ops[1].size==8 else None
            setreg(reg(ops[0]),bit,offset)
        elif m=='lea' and ops[0].type==X86_OP_REG:
            setreg(reg(ops[0]),False,address(ops[1]) if ops[0].size==8 else None)
        elif m in ('add','sub') and ops[0].type==X86_OP_REG:
            name=reg(ops[0]);off=sp.get(name)
            value=int(ops[1].imm) if ops[1].type==X86_OP_IMM else None
            exact_zero=value==0 and ops[0].size==8
            setreg(name,name in known and exact_zero,(off+(value if m=='add' else -value)) if off is not None and value is not None and ops[0].size==8 else None)
        elif m=='mov' and ops[0].type==X86_OP_MEM:
            off=address(ops[0]);bit=identity(ops[1]);size=ops[0].size
            if off is None:mem.clear()
            else:
                mem={a for a in mem if not (off<a+8 and a<off+size)}
                if size==8 and bit:mem.add(off)
        elif m not in ('cmp','test','nop','endbr64'):
            for r in i.regs_access()[1]:setreg(reg_name(md,r),False)
            if any(op.type==X86_OP_MEM and op.access&2 for op in ops):mem.clear()
        submit(nxt,state(),pc)
    calls=[]
    # Emit from final converged incoming states, never from a transient iteration.
    if not pending and updates<=max_updates:
        for pc,s in sorted(states.items()):
            i=code.get(pc)
            if not i or i.mnemonic!='call':continue
            carrier=[r for r in ARGS if r in s[0]]
            if carrier:
                target=hex(int(i.operands[0].imm)) if i.operands[0].type==X86_OP_IMM else 'UNKNOWN'
                calls.append({'site':hex(pc),'target':target,'receiver_argument_registers':carrier})
    rows=[frontiers[k] for k in sorted(frontiers,key=repr)]
    return {'fixedpoint_reached':not pending and updates<=max_updates,
            'state_updates':updates,'reachable_instructions':len(states),
            'receiver_delegations':calls,'incomplete_boundaries':rows,
            'complete':not rows and not pending and updates<=max_updates,
            'scope':'must identity on all modeled paths inside selected FDE; external continuations excluded'}
