import unittest
from binding import qualify_call, plt_slot, relocation_binding

PLT = {'name': '.plt', 'lo': 0x400, 'hi': 0x500, 'flags': 6, 'entsize': 16}
GOT = {'name': '.got.plt', 'lo': 0x900, 'hi': 0xa00, 'flags': 3, 'entsize': 8}
JMP = bytes.fromhex('ff25fa040000')

class Rel(dict):
    def __init__(self, off=0x900, kind=7, idx=3, addend=0, rela=True):
        super().__init__(r_offset=off, r_info_type=kind, r_info_sym=idx, r_addend=addend)
        self.rela = rela
    def is_RELA(self): return self.rela

class Section(dict):
    def __init__(self, rows):
        super().__init__(sh_type='SHT_RELA', sh_link=2)
        self.name, self.rows = '.rela.plt', rows
    def iter_relocations(self): return iter(self.rows)

class Symbol(dict):
    def __init__(self):
        super().__init__(st_shndx='SHN_UNDEF', st_info={'type':'STT_FUNC','bind':'STB_GLOBAL'})
        self.name = '_ZN4Test4callEv'

class Symbols(dict):
    def __init__(self, symbol):
        super().__init__(sh_type='SHT_DYNSYM')
        self.symbol, self.queries = symbol, []
    def num_symbols(self): return 10
    def get_symbol(self, idx):
        self.queries.append(idx)
        if idx != 3: raise AssertionError('UNRELATED_SYMBOL_RESOLUTION')
        return self.symbol

class Elf:
    def __init__(self, rows=None):
        self.relocs = [Section(rows if rows is not None else [Rel()])]
        self.sym = Symbols(Symbol())
    def iter_sections(self): return iter(self.relocs)
    def get_section(self, idx):
        if idx != 2: raise AssertionError('UNRELATED_SECTION_RESOLUTION')
        return self.sym

class BindingTests(unittest.TestCase):
    def test_exact_call(self):
        self.assertEqual(qualify_call(bytes.fromhex('e8fb020000'),0x100,0x400), {'site':'0x100','target':'0x400','kind':'DIRECT_CALL'})
    def test_wrong_call_target(self):
        with self.assertRaises(ValueError): qualify_call(bytes.fromhex('e8fb020000'),0x100,0x401)
    def test_jump_is_not_call(self):
        with self.assertRaises(ValueError): qualify_call(bytes.fromhex('e9fb020000'),0x100,0x400)
    def test_call_scope_cap(self):
        with self.assertRaises(ValueError): qualify_call(b'\x90'*6,0x100,0x400)
    def test_selected_first_rip_jump(self):
        self.assertEqual(plt_slot(JMP,0x400,[PLT,GOT]), {'stub':'0x400','jump_site':'0x400','got_slot':'0x900','section':'.plt'})
    def test_endbr_then_jump(self):
        raw=bytes.fromhex('f30f1efaff25f6040000')
        result=plt_slot(raw,0x400,[PLT,GOT]); self.assertIsNotNone(result)
        self.assertEqual(result['got_slot'],'0x900')
    def test_no_search_past_other_instruction(self):
        with self.assertRaises(ValueError): plt_slot(b'\x90'+JMP,0x400,[PLT,GOT])
    def test_not_native_body(self):
        with self.assertRaises(ValueError): plt_slot(JMP,0x400,[dict(PLT,name='.text'),GOT])
    def test_stub_alignment(self):
        with self.assertRaises(ValueError): plt_slot(JMP,0x401,[PLT,GOT])
    def test_stub_scope(self):
        with self.assertRaises(ValueError): plt_slot(JMP+b'\x90'*11,0x400,[PLT,GOT])
    def test_duplicate_mapping(self):
        with self.assertRaises(ValueError): plt_slot(JMP,0x400,[PLT,PLT,GOT])
    def test_got_must_be_writable_nonexec(self):
        with self.assertRaises(ValueError): plt_slot(JMP,0x400,[PLT,dict(GOT,flags=6)])
    def test_segmented_jump_rejected(self):
        with self.assertRaises(ValueError): plt_slot(b'\x64'+JMP,0x400,[PLT,GOT])
    def test_address32_jump_rejected(self):
        with self.assertRaises(ValueError): plt_slot(b'\x67'+JMP,0x400,[PLT,GOT])
    def test_unrelated_names_never_resolved(self):
        elf=Elf([Rel(off=0x950,idx=8),Rel(),Rel(off=0x958,idx=9)])
        result=relocation_binding(elf,0x900); self.assertIsNotNone(result)
        self.assertEqual(result['symbol'],'_ZN4Test4callEv')
        self.assertEqual(elf.sym.queries,[3])
    def test_duplicate_slot(self):
        with self.assertRaises(ValueError): relocation_binding(Elf([Rel(),Rel()]),0x900)
    def test_missing_slot(self):
        with self.assertRaises(ValueError): relocation_binding(Elf([]),0x900)
    def test_wrong_relocation_kind(self):
        with self.assertRaises(ValueError): relocation_binding(Elf([Rel(kind=6)]),0x900)
    def test_nonzero_addend(self):
        with self.assertRaises(ValueError): relocation_binding(Elf([Rel(addend=1)]),0x900)
    def test_rel_not_rela(self):
        with self.assertRaises(ValueError): relocation_binding(Elf([Rel(rela=False)]),0x900)
    def test_row_limit_incomplete(self):
        with self.assertRaisesRegex(ValueError,'RELOCATION_ROW_LIMIT'):
            relocation_binding(Elf([Rel(),Rel(off=0x950)]),0x900,max_rows=1)
    def test_defined_symbol_rejected(self):
        elf=Elf(); elf.sym.symbol['st_shndx']=5
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)
    def test_not_dynamic_symbol_table(self):
        elf=Elf(); elf.sym['sh_type']='SHT_SYMTAB'
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)
    def test_invalid_function_kind(self):
        elf=Elf(); elf.sym.symbol['st_info']['type']='STT_OBJECT'
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)
    def test_local_binding_rejected(self):
        elf=Elf(); elf.sym.symbol['st_info']['bind']='STB_LOCAL'
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)
    def test_unbounded_name_rejected(self):
        elf=Elf(); elf.sym.symbol.name='_Z'+'x'*512
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)
    def test_nonascii_name_rejected(self):
        elf=Elf(); elf.sym.symbol.name='_Zé'
        with self.assertRaises(ValueError): relocation_binding(elf,0x900)

if __name__ == '__main__': unittest.main()
