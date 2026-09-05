"""One selected PLT/GOT relocation binding, never runtime symbol resolution."""
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_INS_CALL, X86_INS_JMP, X86_INS_ENDBR64, X86_OP_IMM, X86_OP_MEM, X86_REG_RIP


def decoder():
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    return md


def qualify_call(raw, site, target):
    i = next(decoder().disasm(raw, site, count=1), None) if len(raw) == 5 else None
    if i is None or i.size != 5 or i.id != X86_INS_CALL or len(i.operands) != 1 or i.operands[0].type != X86_OP_IMM or i.operands[0].imm != target:
        raise ValueError('PROMOTED_DIRECT_CALL_NOT_QUALIFIED')
    return {'site': hex(site), 'target': hex(target), 'kind': 'DIRECT_CALL'}


def plt_slot(raw, target, sections):
    if not 0 < len(raw) <= 16:
        raise ValueError('SELECTED_STUB_BYTE_LIMIT')
    maps = [s for s in sections if s['lo'] <= target < target + 16 <= s['hi']]
    if len(maps) != 1:
        raise ValueError('SELECTED_STUB_MAPPING_NOT_UNIQUE')
    sec = maps[0]
    if sec['name'] not in ('.plt', '.plt.sec') or sec['flags'] & 6 != 6 or sec['entsize'] != 16 or (target-sec['lo']) % 16:
        raise ValueError('SELECTED_TARGET_NOT_ALIGNED_EXECUTABLE_PLT')
    md = decoder()
    i = next(md.disasm(raw, target, count=1), None)
    if i is not None and i.id == X86_INS_ENDBR64:
        i = next(md.disasm(raw[i.size:], target+i.size, count=1), None)
    if i is None or i.id != X86_INS_JMP or len(i.operands) != 1 or i.operands[0].type != X86_OP_MEM:
        raise ValueError('SELECTED_FIRST_STUB_JUMP_NOT_PROVEN')
    op = i.operands[0]
    if i.addr_size != 8 or op.size != 8 or op.mem.base != X86_REG_RIP or op.mem.index or op.mem.segment:
        raise ValueError('SELECTED_JUMP_NOT_64BIT_RIP_RELATIVE')
    got = i.address+i.size+op.mem.disp
    maps = [s for s in sections if s['lo'] <= got < got+8 <= s['hi']]
    if len(maps) != 1 or maps[0]['flags'] & 3 != 3 or maps[0]['flags'] & 4:
        raise ValueError('SELECTED_GOT_MAPPING_NOT_WRITABLE_NONEXEC_UNIQUE')
    return {'stub': hex(target), 'jump_site': hex(i.address), 'got_slot': hex(got), 'section': sec['name']}
