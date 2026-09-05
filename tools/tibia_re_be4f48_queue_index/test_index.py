import struct
import unittest
from index import selector, dynamic_tags, indexed_record

PLT={'name':'.plt','lo':0x400,'hi':0x500,'flags':6,'entsize':16}
GOT={'name':'.got.plt','lo':0x900,'hi':0xa00,'flags':3,'entsize':8}
STUB=bytes.fromhex('ff25fa0400006803000000e9f0feffff')
TAGS={23:0x1000,2:2400,20:7,6:0x2000,11:24,5:0x3000}
def rawtags(tags=None):
    return b''.join(struct.pack('<qQ',k,v) for k,v in (TAGS if tags is None else tags).items())+bytes(16)

class Rel(dict):
    def __init__(self): super().__init__(r_offset=0x900,r_info_type=7,r_info_sym=3,r_addend=0)
    def is_RELA(self): return True
class Sec(dict):
    def __init__(self,name,typ,addr,size,entsize,link=0):
        super().__init__(sh_type=typ,sh_addr=addr,sh_size=size,sh_entsize=entsize,sh_link=link,sh_flags=2,sh_offset=addr)
        self.name=name
class Rela(Sec):
    def __init__(self):
        super().__init__('.rela.plt','SHT_RELA',0x1000,2400,24,2)
        self.row=Rel();self.queries=[]
    def get_relocation(self,idx):
        self.queries.append(idx)
        if idx!=3: raise AssertionError('UNRELATED_RELOCATION_READ')
        return self.row
    def iter_relocations(self): raise AssertionError('RETIRED_RELOCATION_SCAN')
class Sym(dict):
    name='_ZN4Test4callEv'
    def __init__(self): super().__init__(st_shndx='SHN_UNDEF',st_info={'type':'STT_FUNC','bind':'STB_GLOBAL'})
class Syms(Sec):
    def __init__(self):
        super().__init__('.dynsym','SHT_DYNSYM',0x2000,240,24,3)
        self.symbol=Sym();self.queries=[]
    def num_symbols(self): return 10
    def get_symbol(self,idx):
        self.queries.append(idx)
        if idx!=3: raise AssertionError('UNRELATED_SYMBOL_READ')
        return self.symbol
class Elf:
    def __init__(self):
        self.rela=Rela();self.syms=Syms();self.strings=Sec('.dynstr','SHT_STRTAB',0x3000,512,0)
        self.sections=[self.rela,self.syms,self.strings]
    def iter_sections(self): return iter(self.sections)
    def get_section(self,idx): return {2:self.syms,3:self.strings}.get(idx)

class IndexTests(unittest.TestCase):
    def test_real_section_mapping_interface(self):
        class Proxy:
            def __init__(self, section): self.section=section
            def __getitem__(self, key): return self.section[key]
            def __getattr__(self, key):
                if key=='keys': raise AttributeError(key)
                return getattr(self.section,key)
        elf=Elf(); original=elf.get_section
        elf.iter_sections=lambda: iter([Proxy(s) for s in elf.sections])
        elf.get_section=lambda idx: Proxy(original(idx))
        try: result=indexed_record(elf,TAGS,3,0x900)['symbol']
        except KeyError: result='INVALID_SECTION_ITERATION'
        self.assertEqual(result,'_ZN4Test4callEv')
    def test_contiguous_selector(self):
        r=selector(STUB,0x400,[PLT,GOT],0x900);self.assertIsNotNone(r)
        self.assertEqual((r['candidate_index'],r['push_site'],r['tail_target']),(3,'0x406','0x300'))
    def test_wrong_got(self):
        with self.assertRaises(ValueError): selector(STUB,0x400,[PLT,GOT],0x908)
    def test_negative_selector(self):
        raw=STUB[:7]+b'\xff'*4+STUB[11:]
        with self.assertRaises(ValueError): selector(raw,0x400,[PLT,GOT],0x900)
    def test_no_arbitrary_push_search(self):
        with self.assertRaises(ValueError): selector(STUB[:6]+b'\x90'+STUB[7:],0x400,[PLT,GOT],0x900)
    def test_truncated_stub(self):
        with self.assertRaises(ValueError): selector(STUB[:-1],0x400,[PLT,GOT],0x900)
    def test_tail_not_call(self):
        with self.assertRaises(ValueError): selector(STUB[:11]+b'\xe8'+STUB[12:],0x400,[PLT,GOT],0x900)
    def test_bounded_dynamic_tags(self): self.assertEqual(dynamic_tags(rawtags()),TAGS)
    def test_duplicate_selected_tag(self):
        raw=struct.pack('<qQ',23,0x1000)+rawtags()
        with self.assertRaises(ValueError): dynamic_tags(raw)
    def test_missing_tag(self):
        with self.assertRaises(ValueError): dynamic_tags(rawtags({23:0x1000}))
    def test_dynamic_cap(self):
        with self.assertRaisesRegex(ValueError,'DYNAMIC_ENTRY_LIMIT'): dynamic_tags(rawtags(),max_entries=2)
    def test_null_stops_without_later_duplicate(self):
        self.assertEqual(dynamic_tags(rawtags()+struct.pack('<qQ',23,0x1000)),TAGS)
    def test_wrong_relocation_format(self):
        tags=dict(TAGS);tags[20]=17
        with self.assertRaises(ValueError): dynamic_tags(rawtags(tags))
    def test_one_direct_record_no_iteration(self):
        elf=Elf();r=indexed_record(elf,TAGS,3,0x900);self.assertIsNotNone(r)
        self.assertEqual(r['symbol'],'_ZN4Test4callEv')
        self.assertEqual(r['record_address'],'0x1048')
        self.assertEqual(elf.rela.queries,[3]);self.assertEqual(elf.syms.queries,[3])
        self.assertFalse(r['global_relocation_uniqueness_proven'])
    def test_index_out_of_range(self):
        with self.assertRaises(ValueError): indexed_record(Elf(),TAGS,100,0x900)
    def test_negative_index(self):
        with self.assertRaises(ValueError): indexed_record(Elf(),TAGS,-1,0x900)
    def test_duplicate_table_mapping(self):
        e=Elf();e.sections.append(e.rela)
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_table_size_disagreement(self):
        e=Elf();e.rela['sh_size']=2376
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_table_width_disagreement(self):
        e=Elf();e.rela['sh_entsize']=16
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_wrong_record_offset(self):
        e=Elf();e.rela.row['r_offset']=0x908
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_wrong_record_type(self):
        e=Elf();e.rela.row['r_info_type']=6
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_nonzero_addend(self):
        e=Elf();e.rela.row['r_addend']=1
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_dynamic_symbol_pointer_disagrees(self):
        t=dict(TAGS);t[6]+=24
        with self.assertRaises(ValueError): indexed_record(Elf(),t,3,0x900)
    def test_dynamic_string_pointer_disagrees(self):
        t=dict(TAGS);t[5]+=1
        with self.assertRaises(ValueError): indexed_record(Elf(),t,3,0x900)
    def test_symbol_entry_width_disagrees(self):
        t=dict(TAGS);t[11]=16
        with self.assertRaises(ValueError): indexed_record(Elf(),t,3,0x900)
    def test_defined_symbol(self):
        e=Elf();e.syms.symbol['st_shndx']=5
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_wrong_symbol_type(self):
        e=Elf();e.syms.symbol['st_info']['type']='STT_OBJECT'
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)
    def test_name_limit(self):
        e=Elf();e.syms.symbol.name='_Z'+'x'*512
        with self.assertRaises(ValueError): indexed_record(e,TAGS,3,0x900)

if __name__=='__main__': unittest.main()
