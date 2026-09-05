"""Linear first-transfer facts only; no memory reads, callee or branch traversal."""
from capstone import (Cs, CS_ARCH_X86, CS_MODE_64, CS_GRP_CALL, CS_GRP_RET,
                      CS_GRP_JUMP, CS_GRP_INT, CS_GRP_IRET, CS_GRP_PRIVILEGE)
from capstone.x86_const import X86_OP_REG, X86_OP_MEM, X86_OP_IMM, X86_INS_JMP

ACTIVATE = '_ZN11QMetaObject8activateEP7QObjectPKS_iPPv'
ARGS = ('rdi', 'rsi', 'rdx', 'rcx')
UNKNOWN = 'UNKNOWN'

def decoder():
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return md

def register(md, number):
    name = md.reg_name(number)
    for full, aliases in {
        'rax': ('eax', 'ax', 'al', 'ah'), 'rbx': ('ebx', 'bx', 'bl', 'bh'),
        'rcx': ('ecx', 'cx', 'cl', 'ch'), 'rdx': ('edx', 'dx', 'dl', 'dh'),
        'rdi': ('edi', 'di', 'dil'), 'rsi': ('esi', 'si', 'sil'),
        'rsp': ('esp', 'sp', 'spl'), 'rbp': ('ebp', 'bp', 'bpl'),
    }.items():
        if name == full or name in aliases:
            return full
    if name and name.startswith('r') and name[-1:] in ('b', 'w', 'd') and name[1:-1].isdigit():
        return name[:-1]
    return name

def constant(n, size):
    return {'kind': 'CONSTANT', 'value': n & ((1 << (8 * size)) - 1)}

def qualify_tail(raw, site, target):
    if not 0 < len(raw) <= 5:
        raise ValueError('TAIL_BOUND_INVALID')
    i = next(decoder().disasm(raw, site, count=1), None)
    if (i is None or i.id != X86_INS_JMP or len(i.operands) != 1 or
            i.operands[0].type != X86_OP_IMM or i.operands[0].imm != target):
        raise ValueError('PROMOTED_TAIL_NOT_QUALIFIED')

def project(raw, base, entry=None, max_instructions=128):
    entry = base if entry is None else entry
    if not 0 < len(raw) <= 4096 or not base <= entry < base + len(raw) or not 0 < max_instructions <= 128:
        raise ValueError('ACTIVATION_SCOPE_INVALID')
    md = decoder()
    regs = {'rdi': {'kind': 'ENTRY_RECEIVER'}}
    pc, count = entry, 0

    def finish(kind, target=None):
        boundary = {'kind': kind, 'site': hex(pc)}
        if target is not None:
            boundary['target'] = hex(target)
        transfer = kind in ('DIRECT_CALL', 'DIRECT_TAIL')
        return {'boundary': boundary, 'instructions': count,
                'first_transfer_proven': transfer,
                'resource_limit_hit': kind == 'INSTRUCTION_LIMIT',
                'registers': {r: regs.get(r, UNKNOWN) if transfer else UNKNOWN for r in ARGS},
                'scope': 'linear normal prefix through first transfer; no branch or callee traversal',
                'static_addresses_are_linktime_not_runtime_values': True,
                'exceptional_control_not_modeled': True}

    def assign(op, token):
        name = register(md, op.reg)
        regs.pop(name, None)
        if token is not None and op.size in (4, 8):
            if op.size == 8:
                regs[name] = token
            elif token['kind'] == 'CONSTANT':
                regs[name] = constant(token['value'], 4)

    while base <= pc < base + len(raw):
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
        if m in ('mov', 'movabs') and len(ops) == 2 and ops[0].type == X86_OP_REG:
            src = ops[1]
            token = constant(src.imm, ops[0].size) if src.type == X86_OP_IMM else regs.get(register(md, src.reg)) if src.type == X86_OP_REG and src.size == ops[0].size else None
            assign(ops[0], token)
        elif m == 'lea' and len(ops) == 2 and ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM:
            mem = ops[1].mem
            token = None
            if not mem.segment and not mem.index and ops[0].size == 8:
                name = md.reg_name(mem.base)
                if name == 'rip':
                    token = {'kind': 'STATIC_ADDRESS', 'value': nxt + mem.disp}
                elif name == register(md, mem.base) and mem.disp == 0:
                    token = regs.get(name)
            assign(ops[0], token)
        elif m == 'xor' and len(ops) == 2 and ops[0].type == X86_OP_REG:
            same = ops[1].type == X86_OP_REG and ops[0].reg == ops[1].reg
            assign(ops[0], constant(0, ops[0].size) if same else None)
        elif m in ('add', 'sub') and len(ops) == 2 and ops[0].type == X86_OP_REG:
            token = regs.get(register(md, ops[0].reg))
            if token is not None and token['kind'] == 'CONSTANT' and ops[1].type == X86_OP_IMM:
                token = constant(token['value'] + ops[1].imm * (1 if m == 'add' else -1), ops[0].size)
            else:
                token = None
            assign(ops[0], token)
        elif m == 'push' and len(ops) == 1 and ops[0].size == 8:
            regs.pop('rsp', None)
        elif m == 'pop' and len(ops) == 1 and ops[0].type == X86_OP_REG and ops[0].size == 8:
            regs.pop('rsp', None)
            regs.pop(register(md, ops[0].reg), None)
        elif m not in ('nop', 'endbr64', 'cmp', 'test'):
            return finish('UNMODELED_INSTRUCTION')
        pc = nxt
    return finish('FDE_END_WITHOUT_TRANSFER')

def classify(flow, symbol):
    if flow['resource_limit_hit']:
        return 'ANALYSIS_INCOMPLETE', 'ACTIVATION_INSTRUCTION_FRONTIER'
    if not flow['first_transfer_proven']:
        return 'SOURCE_BLOCKER', 'FIRST_TRANSFER_' + flow['boundary']['kind']
    if symbol != ACTIVATE:
        return 'SOURCE_BLOCKER', 'FIRST_TRANSFER_EXACT_ACTIVATE_IMPORT_NOT_PROVEN'
    r = flow['registers']
    if r['rdi'] != {'kind': 'ENTRY_RECEIVER'}:
        return 'SOURCE_BLOCKER', 'ACTIVATE_RECEIVER_ARGUMENT_NOT_PROVEN'
    if (not isinstance(r['rsi'], dict) or r['rsi']['kind'] != 'STATIC_ADDRESS' or
            not isinstance(r['rdx'], dict) or r['rdx']['kind'] != 'CONSTANT'):
        return 'SOURCE_BLOCKER', 'ACTIVATE_STATIC_AND_SCALAR_ARGUMENTS_NOT_PROVEN'
    return 'POSITIVE_EXACT_ACTIVATION_ARGUMENTS', 'ACTIVATION_TO_REGISTERED_RECEIVER_DELIVERY_NOT_PROVEN'

def import_binding(raw, base, rows):
    """Only one selected PLT stub and one exact undefined GOT binding."""
    if not 0 < len(raw) <= 16:
        return None
    md = decoder()
    ins = list(md.disasm(raw, base, count=2))
    if ins and ins[0].mnemonic == 'endbr64':
        ins = ins[1:]
    if not ins or ins[0].id != X86_INS_JMP or len(ins[0].operands) != 1:
        return None
    i, op = ins[0], ins[0].operands[0]
    if (op.type != X86_OP_MEM or op.size != 8 or op.mem.segment or op.mem.index or
            md.reg_name(op.mem.base) != 'rip'):
        return None
    got = i.address + i.size + op.mem.disp
    matches = [r for r in rows if r['offset'] == got]
    if len(matches) != 1:
        return None
    row = matches[0]
    return row['name'] if row['type'] in (6, 7) and row['undefined'] and row['name'] else None
