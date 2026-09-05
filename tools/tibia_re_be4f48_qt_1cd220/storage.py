"""Finite must-value storage analysis over one selected x86-64 FDE.

Tokens denote scalar values, never dynamic class/allocation ownership. Calls
fall through conditionally under the modeled SysV ABI. No callee is analyzed.
"""
from collections import deque
from capstone import (Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_JUMP,
                      CS_GRP_CALL, CS_GRP_RET, CS_GRP_INT, CS_GRP_IRET)
from capstone.x86_const import X86_OP_REG, X86_OP_MEM, X86_OP_IMM

ARGS = ('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')
VOLATILE = ('rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11')
RECEIVER = ('entry:rcx', 0)


def register(md, number):
    name = md.reg_name(number)
    for full, aliases in {
        'rax': ('eax', 'ax', 'al', 'ah'), 'rbx': ('ebx', 'bx', 'bl', 'bh'),
        'rcx': ('ecx', 'cx', 'cl', 'ch'), 'rdx': ('edx', 'dx', 'dl', 'dh'),
        'rsi': ('esi', 'si', 'sil'), 'rdi': ('edi', 'di', 'dil'),
        'rsp': ('esp', 'sp', 'spl'), 'rbp': ('ebp', 'bp', 'bpl'),
    }.items():
        if name == full or name in aliases:
            return full
    if name and name.startswith('r') and name[-1:] in ('b', 'w', 'd') and name[1:-1].isdigit():
        return name[:-1]
    return name


def offset(token, delta):
    if token is None or abs(token[1] + delta) > 1048576:
        return None
    return (token[0], token[1] + delta)


def address(md, op, regs, next_pc):
    if op.type != X86_OP_MEM or op.mem.segment or op.mem.index:
        return None
    base = register(md, op.mem.base)
    if base != md.reg_name(op.mem.base):
        return None  # Address-size override truncates the base value.
    token = ('static_address', next_pc) if base == 'rip' else regs.get(base)
    return offset(token, op.mem.disp)


def stack_address(token):
    return token[1] if token is not None and token[0] == 'private_stack' else None


def value(md, op, regs, memory, next_pc):
    if op.size != 8:
        return None
    if op.type == X86_OP_REG:
        return regs.get(register(md, op.reg))
    if op.type == X86_OP_MEM:
        return memory.get(stack_address(address(md, op, regs, next_pc)))
    return None


def invalidate(memory, dest, width):
    loc = stack_address(dest)
    if loc is None:
        memory.clear()  # Unknown non-stack aliases can still point into the stack.
    else:
        for old in list(memory):
            if loc < old + 8 and old < loc + width:
                del memory[old]


def receiver_storage(raw, base, max_instructions=2048, max_updates=20000):
    if not 0 < len(raw) <= 8192 or not 0 < max_instructions <= 2048 or not 0 < max_updates <= 20000:
        raise ValueError('STORAGE_SCOPE_INVALID')
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    code = {i.address: i for i in md.disasm(raw, base)}
    initial = ({r: ('entry:' + r, 0) for r in ARGS} | {'rsp': ('private_stack', 0)}, {})
    states = {base: initial}
    pending = deque([base])
    updates = 0
    cfg, boundaries, calls = {}, {}, {}
    resource_limit = False

    def boundary(kind, pc, target=None):
        row = {'kind': kind, 'site': hex(pc)}
        if target is not None:
            row['target'] = hex(target)
        boundaries[(kind, pc, target)] = row

    def meet(a, b):
        return tuple({k: v for k, v in x.items() if y.get(k) == v}
                     for x, y in zip(a, b))

    def submit(target, state, pc):
        nonlocal resource_limit
        if target not in code:
            kind = 'UNDECODED_TARGET' if base <= target < base + len(raw) else 'OUTSIDE_FDE'
            boundary(kind, pc, target)
            return
        if target not in states and len(states) >= max_instructions:
            resource_limit = True
            boundary('INSTRUCTION_LIMIT', pc, target)
            return
        incoming = meet(states[target], state) if target in states else state
        if target not in states or states[target] != incoming:
            states[target] = incoming
            pending.append(target)

    while pending:
        if updates >= max_updates:
            boundary('UPDATE_LIMIT', pending[0])
            resource_limit = True
            break
        pc = pending.popleft()
        updates += 1
        i = code.get(pc)
        cfg[pc] = []
        if i is None:
            boundary('UNDECODED_ENTRY', pc)
            continue
        regs, memory = (dict(part) for part in states[pc])
        ops, m, nxt = i.operands, i.mnemonic, pc + i.size

        def assign(name, token):
            regs.pop(name, None)
            if token is not None:
                regs[name] = token

        if i.group(CS_GRP_RET):
            continue
        if (i.group(CS_GRP_INT) or i.group(CS_GRP_IRET) or
                m in ('ud2', 'hlt', 'syscall', 'sysenter', 'sysret', 'sysexit',
                      'xbegin', 'xabort', 'loop', 'loope', 'loopne', 'jcxz', 'jecxz', 'jrcxz')):
            boundary('UNMODELED_CONTROL', pc)
            continue
        if i.group(CS_GRP_JUMP):
            if len(ops) != 1 or ops[0].type != X86_OP_IMM:
                boundary('INDIRECT_BRANCH', pc)
                continue
            targets = [int(ops[0].imm)] + ([] if m == 'jmp' else [nxt])
            cfg[pc] = targets
            for target in targets:
                submit(target, (regs, memory), pc)
            continue
        if any(o.type == X86_OP_MEM and o.mem.segment for o in ops):
            boundary('SEGMENTED_MEMORY', pc)
        if i.group(CS_GRP_CALL):
            calls[pc] = {'site': hex(pc), 'target': hex(ops[0].imm) if ops and ops[0].type == X86_OP_IMM else 'UNKNOWN'}
            for r in VOLATILE:
                regs.pop(r, None)
            regs['rax'] = ('call_return:' + hex(pc), 0)
            memory.clear()
        elif m == 'push':
            sp = stack_address(regs.get('rsp'))
            if len(ops) != 1 or ops[0].size != 8 or sp is None:
                boundary('UNPROVEN_STACK_PUSH', pc)
                continue
            token = value(md, ops[0], regs, memory, nxt)
            dest = offset(regs['rsp'], -8)
            invalidate(memory, dest, 8)
            assign('rsp', dest)
            if dest is not None and token is not None:
                memory[dest[1]] = token
        elif m == 'pop':
            sp = stack_address(regs.get('rsp'))
            if len(ops) != 1 or ops[0].type != X86_OP_REG or ops[0].size != 8 or register(md, ops[0].reg) == 'rsp' or sp is None:
                boundary('UNPROVEN_STACK_POP', pc)
                continue
            token = memory.pop(sp, None)
            assign('rsp', offset(regs['rsp'], 8))
            assign(register(md, ops[0].reg), token)
        elif m in ('mov', 'movabs') and len(ops) == 2:
            token = value(md, ops[1], regs, memory, nxt)
            if ops[0].type == X86_OP_REG:
                assign(register(md, ops[0].reg), token if ops[0].size == 8 else None)
            elif ops[0].type == X86_OP_MEM:
                dest = address(md, ops[0], regs, nxt)
                invalidate(memory, dest, ops[0].size)
                sp = stack_address(dest)
                if sp is not None and ops[0].size == 8 and token is not None:
                    memory[sp] = token
        elif m == 'lea' and len(ops) == 2 and ops[0].type == X86_OP_REG:
            assign(register(md, ops[0].reg), address(md, ops[1], regs, nxt) if ops[0].size == 8 else None)
        elif m in ('add', 'sub') and len(ops) == 2 and ops[0].type == X86_OP_REG:
            name = register(md, ops[0].reg)
            token = offset(regs.get(name), int(ops[1].imm) * (1 if m == 'add' else -1)) if ops[0].size == 8 and ops[1].type == X86_OP_IMM else None
            assign(name, token)
        elif m not in ('cmp', 'test', 'nop', 'endbr64'):
            for r in i.regs_access()[1]:
                regs.pop(register(md, r), None)
            if any(o.type == X86_OP_MEM and o.access & 2 for o in ops):
                memory.clear()
        cfg[pc] = [nxt]
        submit(nxt, (regs, memory), pc)

    converged = not pending and not resource_limit
    stores = []
    if converged:
        for pc, (regs, memory) in sorted(states.items()):
            i = code.get(pc)
            if i is None or i.mnemonic != 'mov' or len(i.operands) != 2:
                continue
            dest, src = i.operands
            if dest.type != X86_OP_MEM or dest.size != 8 or dest.mem.segment:
                continue
            if value(md, src, regs, memory, pc + i.size) != RECEIVER:
                continue
            token = address(md, dest, regs, pc + i.size)
            stores.append({'site': hex(pc), 'width': 8, 'value': 'entry:rcx',
                           'destination': {'base': token[0], 'offset': token[1]} if token else 'UNKNOWN',
                           'private_stack': stack_address(token) is not None,
                           'destination_owner': 'UNKNOWN'})
    rows = [boundaries[k] for k in sorted(boundaries, key=repr)]
    return {'fixedpoint_reached': converged, 'resource_limit_hit': resource_limit,
            'state_updates': updates, 'reachable_instructions': len(states),
            'coverage_complete': converged and not rows,
            'receiver_stores': stores, 'boundaries': rows,
            'calls': [calls[k] for k in sorted(calls)],
            'cfg': {hex(k): [hex(x) for x in sorted(set(cfg[k]))] for k in sorted(cfg)},
            'scope': 'modeled normal prefixes inside this FDE; no reentry from excluded continuations',
            'conditional_on_calls_returning_under_sysv_abi': True,
            'exceptional_control_not_modeled': True, 'termination_proven': False,
            'runtime_registration_or_delivery_proven': False,
            'memory_loads_outside_private_stack': 'UNKNOWN'}


def storage_region(fdes, entry):
    rows = [(lo, hi) for lo, hi in fdes if lo <= entry < hi]
    if len(rows) != 1 or rows[0][0] != entry or not 0 < rows[0][1] - entry <= 8192:
        raise ValueError('NO_UNIQUE_EXACT_STORAGE_FDE')
    return rows[0]
