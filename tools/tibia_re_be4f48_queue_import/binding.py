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


def relocation_binding(elf, got, max_rows=65536):
    if not 0 < max_rows <= 65536:
        raise ValueError('RELOCATION_ROW_LIMIT_INVALID')
    hits, seen = [], 0
    for sec in elf.iter_sections():
        if sec['sh_type'] not in ('SHT_RELA', 'SHT_REL'):
            continue
        for rel in sec.iter_relocations():
            seen += 1
            if seen > max_rows:
                raise ValueError('RELOCATION_ROW_LIMIT')
            if int(rel['r_offset']) == got:
                hits.append((sec, rel))
    if len(hits) != 1:
        raise ValueError('SELECTED_GOT_RELOCATION_NOT_UNIQUE')
    sec, rel = hits[0]
    if not rel.is_RELA() or int(rel['r_info_type']) != 7 or int(rel['r_addend']) != 0:
        raise ValueError('SELECTED_RELOCATION_NOT_ZERO_ADDEND_JUMP_SLOT')
    idx = int(rel['r_info_sym'])
    table = elf.get_section(sec['sh_link'])
    if table is None or table['sh_type'] != 'SHT_DYNSYM' or not 0 < idx < table.num_symbols():
        raise ValueError('SELECTED_DYNAMIC_SYMBOL_TABLE_OR_INDEX_INVALID')
    symbol = table.get_symbol(idx)  # Only selected row; no other symbol names.
    if symbol['st_shndx'] != 'SHN_UNDEF' or symbol['st_info']['type'] != 'STT_FUNC' or symbol['st_info']['bind'] not in ('STB_GLOBAL', 'STB_WEAK'):
        raise ValueError('SELECTED_SYMBOL_NOT_UNDEFINED_DYNAMIC_FUNCTION')
    name = symbol.name
    if not isinstance(name, str) or not 1 <= len(name) <= 512 or not re.fullmatch(r'_Z[A-Za-z0-9_.$]+', name):
        raise ValueError('SELECTED_SYMBOL_NAME_NOT_BOUNDED_ASCII_MANGLED')
    return {'symbol': name, 'symbol_index': idx, 'relocation_section': sec.name,
            'relocation_type': 'R_X86_64_JUMP_SLOT', 'got_slot': hex(got),
            'addend': 0, 'symbol_binding': symbol['st_info']['bind'],
            'symbol_type': 'STT_FUNC', 'symbol_defined': False,
            'numeric_relocation_rows_inspected': seen, 'resolved_symbol_count': 1,
            'runtime_resolution_proven': False}
