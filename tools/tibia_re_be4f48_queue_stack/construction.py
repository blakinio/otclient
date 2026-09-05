"""Exact linear private-stack cells and raw pointer escape; no logical object typing."""
from capstone import (Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_CALL, CS_GRP_JUMP,
                      CS_GRP_RET, CS_GRP_INT, CS_GRP_IRET, CS_GRP_PRIVILEGE)
from capstone.x86_const import X86_OP_REG, X86_OP_MEM, X86_OP_IMM, X86_INS_JMP

ARGS = ('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')

def decoder():
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return md

def reg(md, n):
    name = md.reg_name(n)
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

def scalar(n, size=8):
    return {'kind': 'CONSTANT', 'value': n & ((1 << (size * 8)) - 1)}

def stack(n):
    return {'kind': 'STACK_ADDRESS', 'offset': n}

def construct(raw, base, max_instructions=128):
    if not 0 < len(raw) <= 42 or not 0 < max_instructions <= 128:
        raise ValueError('STACK_CONSTRUCTION_SCOPE_INVALID')
    md = decoder()
    regs = {r: {'kind': 'ENTRY_ARG', 'register': r} for r in ARGS}
    regs['rsp'] = stack(0)
    sp, pc, count = 0, base, 0
    cells, writes = {}, []

    def finish(kind, target=None):
        boundary = {'kind': kind, 'site': hex(pc)}
        if target is not None:
            boundary['target'] = hex(target)
        escapes = []
        transfer = kind in ('DIRECT_CALL', 'DIRECT_TAIL')
        if transfer and cells:
            for r in ARGS:
                token = regs.get(r)
                if token is not None and token['kind'] == 'STACK_ADDRESS' and sp <= token['offset'] < 0:
                    escapes.append({'register': r, 'frame_offset': token['offset'],
                                    'relative_cell_offsets': [k - token['offset'] for k in sorted(cells)]})
        return {'boundary': boundary, 'instructions': count,
                'resource_limit_hit': kind == 'INSTRUCTION_LIMIT',
                'construction_escape_proven': bool(escapes and cells),
                'live_frame': {'low': sp, 'high': 0, 'relative_to': 'ENTRY_RSP'},
                'live_cells': [{'offset': k, 'width': 8, 'value': cells[k]} for k in sorted(cells)],
                'writes': writes, 'escapes': escapes, 'logical_object_type': 'UNKNOWN',
                'scope': 'linear normal prefix before first boundary; no callee, branch, or external memory traversal',
                'static_addresses_are_linktime_not_runtime_values': True,
                'runtime_escape_or_callee_use_proven': False,
                'exceptional_control_not_modeled': True}

    def adjust(delta):
        nonlocal sp
        new = sp + delta
        if not -4096 <= new <= 0:
            return False
        sp = new
        regs['rsp'] = stack(sp)
        for off in list(cells):
            if not sp <= off < off + 8 <= 0:
                del cells[off]
        return True

    def address(op, nxt):
        if op.type != X86_OP_MEM or op.mem.segment or op.mem.index:
            return None
        name = md.reg_name(op.mem.base)
        if name != reg(md, op.mem.base):
            return None
        if name == 'rip':
            return {'kind': 'STATIC_ADDRESS', 'value': nxt + op.mem.disp}
        token = regs.get(name)
        if token is not None and token['kind'] == 'STACK_ADDRESS':
            return stack(token['offset'] + op.mem.disp)
        return token if token is not None and op.mem.disp == 0 else None

    def value(op, nxt):
        if op.type == X86_OP_IMM:
            return scalar(op.imm, op.size)
        if op.type == X86_OP_REG:
            token = regs.get(reg(md, op.reg))
            if op.size == 8:
                return token
            if op.size == 4 and token is not None and token['kind'] == 'CONSTANT':
                return scalar(token['value'], 4)
        if op.type == X86_OP_MEM and op.size == 8:
            addr = address(op, nxt)
            if addr is not None and addr['kind'] == 'STACK_ADDRESS':
                return cells.get(addr['offset'])
        return None

    def assign(op, token):
        name = reg(md, op.reg)
        if name == 'rsp':
            return False
        regs.pop(name, None)
        if op.size == 8 and token is not None:
            regs[name] = token
        elif op.size == 4 and token is not None and token['kind'] == 'CONSTANT':
            regs[name] = scalar(token['value'], 4)
        return True

    def write(addr, width, token):
        off = addr['offset'] if addr is not None and addr['kind'] == 'STACK_ADDRESS' else None
        if off is None:
            cells.clear()  # Unknown non-stack aliases may still overlap this frame.
        else:
            for old in list(cells):
                if off < old + 8 and old < off + width:
                    del cells[old]
        private = off is not None and sp <= off < off + width <= 0
        if private and width == 8 and token is not None:
            cells[off] = token
        writes.append({'site': hex(pc), 'stack_offset': off if off is not None else 'UNKNOWN',
                       'width': width, 'within_live_frame': private,
                       'value': token if token is not None else 'UNKNOWN'})

    while pc < base + len(raw):
        if count >= max_instructions:
            return finish('INSTRUCTION_LIMIT')
        i = next(md.disasm(raw[pc-base:], pc, count=1), None)
        if i is None:
            return finish('UNDECODED')
        count += 1
        ops, m, nxt = i.operands, i.mnemonic, pc + i.size
        if (i.group(CS_GRP_PRIVILEGE) or i.group(CS_GRP_INT) or i.group(CS_GRP_IRET) or
                m in ('ud2', 'syscall', 'sysenter', 'sysret', 'sysexit', 'xbegin', 'xabort')):
            return finish('UNMODELED_CONTROL')
        if i.group(CS_GRP_RET):
            return finish('RETURN')
        if i.group(CS_GRP_CALL):
            return finish('DIRECT_CALL', ops[0].imm) if len(ops) == 1 and ops[0].type == X86_OP_IMM else finish('INDIRECT_CALL')
        if i.group(CS_GRP_JUMP):
            if i.id == X86_INS_JMP and len(ops) == 1 and ops[0].type == X86_OP_IMM and not base <= ops[0].imm < base + len(raw):
                return finish('DIRECT_TAIL', ops[0].imm)
            return finish('BRANCH_STOP')
        if m in ('mov', 'movabs') and len(ops) == 2:
            token = value(ops[1], nxt)
            if ops[0].type == X86_OP_REG:
                if not assign(ops[0], token):
                    return finish('UNMODELED_STACK_REBASE')
            elif ops[0].type == X86_OP_MEM:
                write(address(ops[0], nxt), ops[0].size, token)
            else:
                return finish('UNMODELED_INSTRUCTION')
        elif m == 'lea' and len(ops) == 2 and ops[0].type == X86_OP_REG:
            if not assign(ops[0], address(ops[1], nxt) if ops[0].size == 8 else None):
                return finish('UNMODELED_STACK_REBASE')
        elif m in ('add', 'sub') and len(ops) == 2 and ops[0].type == X86_OP_REG:
            if reg(md, ops[0].reg) == 'rsp':
                if ops[0].size != 8 or ops[1].type != X86_OP_IMM or not adjust(ops[1].imm * (1 if m == 'add' else -1)):
                    return finish('UNPROVEN_STACK_ALLOCATION')
            elif not assign(ops[0], None):
                return finish('UNMODELED_STACK_REBASE')
        elif m == 'xor' and len(ops) == 2 and ops[0].type == X86_OP_REG:
            token = scalar(0, ops[0].size) if ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg else None
            if not assign(ops[0], token):
                return finish('UNMODELED_STACK_REBASE')
        elif m == 'push' and len(ops) == 1 and ops[0].size == 8:
            token = value(ops[0], nxt)
            if not adjust(-8):
                return finish('UNPROVEN_STACK_ALLOCATION')
            write(stack(sp), 8, token)
        elif m == 'pop' and len(ops) == 1 and ops[0].type == X86_OP_REG and ops[0].size == 8 and reg(md, ops[0].reg) != 'rsp':
            token = cells.get(sp)
            if not adjust(8):
                return finish('UNPROVEN_STACK_ALLOCATION')
            assign(ops[0], token)
        elif m not in ('nop', 'endbr64', 'cmp', 'test'):
            return finish('UNMODELED_INSTRUCTION')
        pc = nxt
    return finish('FDE_END_WITHOUT_TRANSFER')

def qualify_tail(raw, site, target):
    if not 0 < len(raw) <= 5:
        raise ValueError('TAIL_BOUND_INVALID')
    i = next(decoder().disasm(raw, site, count=1), None)
    if i is None or i.id != X86_INS_JMP or len(i.operands) != 1 or i.operands[0].type != X86_OP_IMM or i.operands[0].imm != target:
        raise ValueError('PROMOTED_TAIL_NOT_QUALIFIED')
