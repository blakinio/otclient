"""One encoded selector and directly indexed dynamic record, no relocation scan."""
import re
import struct
from binding import decoder, plt_slot
from capstone.x86_const import X86_INS_JMP, X86_INS_PUSH, X86_OP_IMM

REQUIRED={23,2,20,6,11,5}


def selector(raw, target, sections, got):
    if len(raw)!=16:
        raise ValueError('SELECTOR_STUB_WIDTH_INVALID')
    stub=plt_slot(raw,target,sections)
    if int(stub['got_slot'],16)!=got:
        raise ValueError('PROMOTED_GOT_SLOT_CHANGED')
    instructions=list(decoder().disasm(raw,target))
    if len(instructions)!=3 or [i.size for i in instructions]!=[6,5,5]:
        raise ValueError('SELECTOR_CONTIGUOUS_LAYOUT_NOT_PROVEN')
    first,push,tail=instructions
    if first.id!=X86_INS_JMP or push.id!=X86_INS_PUSH or len(push.operands)!=1 or push.operands[0].type!=X86_OP_IMM or push.operands[0].imm<0:
        raise ValueError('SELECTOR_NONNEGATIVE_PUSH_NOT_PROVEN')
    if tail.id!=X86_INS_JMP or len(tail.operands)!=1 or tail.operands[0].type!=X86_OP_IMM:
        raise ValueError('SELECTOR_DIRECT_TAIL_NOT_PROVEN')
    return {**stub,'candidate_index':push.operands[0].imm,'push_site':hex(push.address),
            'tail_site':hex(tail.address),'tail_target':hex(tail.operands[0].imm),
            'unresolved_path_execution_proven':False}


def dynamic_tags(raw, max_entries=512):
    if not 0<max_entries<=512 or len(raw)%16:
        raise ValueError('DYNAMIC_ENTRY_SHAPE_INVALID')
    found={}
    for idx in range(min(len(raw)//16,max_entries)):
        key,value=struct.unpack_from('<qQ',raw,idx*16)
        if key==0:
            if set(found)!=REQUIRED:
                raise ValueError('DYNAMIC_SELECTED_TAG_MISSING')
            if found[20]!=7 or found[11]!=24:
                raise ValueError('DYNAMIC_RELA_OR_SYMENT_INVALID')
            return found
        if key in REQUIRED:
            if key in found:
                raise ValueError('DYNAMIC_SELECTED_TAG_DUPLICATE')
            found[key]=value
    raise ValueError('DYNAMIC_ENTRY_LIMIT' if len(raw)//16>=max_entries else 'DYNAMIC_NULL_NOT_FOUND')


def indexed_record(elf, tags, index, got):
    if set(tags)!=REQUIRED or tags[20]!=7 or tags[11]!=24:
        raise ValueError('INDEXED_DYNAMIC_CONTRACT_INVALID')
    sections=list(elf.iter_sections())
    def owner(address):
        owners=[s for s in sections if s['sh_flags']&2 and s['sh_addr']<=address<s['sh_addr']+s['sh_size']]
        if len(owners)!=1:
            raise ValueError('INDEXED_TABLE_MAPPING_NOT_UNIQUE')
        return owners[0]
    table=owner(tags[23])
    size=int(table['sh_size'])
    if table['sh_type']!='SHT_RELA' or table['sh_addr']!=tags[23] or size!=tags[2] or size%24 or table['sh_entsize']!=24:
        raise ValueError('INDEXED_RELA_TABLE_CONTRACT_INVALID')
    count=size//24
    if not isinstance(index,int) or not 0<=index<count:
        raise ValueError('INDEXED_RELOCATION_INDEX_INVALID')
    syms=elf.get_section(table['sh_link'])
    sym_owner=owner(tags[6])
    if syms is None or syms['sh_type']!='SHT_DYNSYM' or syms['sh_addr']!=tags[6] or syms['sh_entsize']!=24 or any(syms[k]!=sym_owner[k] for k in ('sh_type','sh_addr','sh_offset','sh_size','sh_entsize','sh_link')):
        raise ValueError('INDEXED_DYNAMIC_SYMBOL_METADATA_DISAGREES')
    strings=elf.get_section(syms['sh_link'])
    str_owner=owner(tags[5])
    if strings is None or strings['sh_type']!='SHT_STRTAB' or strings['sh_addr']!=tags[5] or any(strings[k]!=str_owner[k] for k in ('sh_type','sh_addr','sh_offset','sh_size','sh_link')):
        raise ValueError('INDEXED_DYNAMIC_STRING_METADATA_DISAGREES')
    row=table.get_relocation(index)  # Exactly one direct indexed row, never iteration.
    if not row.is_RELA() or int(row['r_offset'])!=got or int(row['r_info_type'])!=7 or int(row['r_addend'])!=0:
        raise ValueError('INDEXED_RECORD_GOT_OR_TYPE_DISAGREES')
    symidx=int(row['r_info_sym'])
    if not 0<symidx<syms.num_symbols():
        raise ValueError('INDEXED_SYMBOL_INDEX_INVALID')
    symbol=syms.get_symbol(symidx)
    if symbol['st_shndx']!='SHN_UNDEF' or symbol['st_info']['type']!='STT_FUNC' or symbol['st_info']['bind'] not in ('STB_GLOBAL','STB_WEAK'):
        raise ValueError('INDEXED_SYMBOL_NOT_UNDEFINED_FUNCTION')
    name=symbol.name
    if not isinstance(name,str) or not 1<=len(name)<=512 or not re.fullmatch(r'_Z[A-Za-z0-9_.$]+',name):
        raise ValueError('INDEXED_SYMBOL_NAME_INVALID')
    return {'record_index':index,'record_address':hex(tags[23]+24*index),
            'table_address':hex(tags[23]),'table_row_count':count,'table_entry_width':24,
            'got_slot':hex(got),'relocation_type':'R_X86_64_JUMP_SLOT','addend':0,
            'symbol':name,'symbol_index':symidx,'symbol_binding':symbol['st_info']['bind'],
            'symbol_defined':False,'relocation_records_read':1,'symbol_names_resolved':1,
            'global_relocation_uniqueness_proven':False,'runtime_resolution_proven':False}
