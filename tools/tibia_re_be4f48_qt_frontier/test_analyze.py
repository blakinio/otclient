import unittest
from unittest.mock import patch
import analyze
import io

class MetadataTests(unittest.TestCase):
    def test_analyzer_never_constructs_eager_sections(self):
        class Elf:
            elfclass=64; little_endian=True
            stream_len=4096
            def __getitem__(self,k): return {'e_machine':'EM_X86_64','e_shentsize':64,'e_shoff':2048}[k]
            def num_sections(self): return 0
            def iter_sections(self): raise AssertionError('eager GNU hash arrays')
        class Path:
            def read_bytes(self): return b'fixture'
            def open(self,mode): return io.BytesIO(b'fixture')
        with patch.object(analyze,'ELFFile',return_value=Elf()), patch.object(analyze,'verify_fence'), patch.object(analyze,'qualify_dependency_fence'), patch.object(analyze,'verify_member'), patch.object(analyze,'lookup',return_value={}), patch.object(analyze,'selected_body',return_value=b'\xc3'), patch.object(analyze,'frontier',return_value={'complete':True,'limit_reached':False}):
            self.assertEqual(analyze.analyze({'version':'fixture','qtcore':{}},Path(),Path())['terminal_result'],'POSITIVE_EXACT_SYMBOL_CONTROL_FRONTIER')
    def test_metadata_never_constructs_section_objects(self):
        class Elf:
            stream_len=4096
            def __getitem__(self,k): return {'e_shentsize':64,'e_shoff':2048}[k]
            def num_sections(self): return 1
            def _get_section_header(self,i):
                return dict(sh_type='SHT_GNU_HASH',sh_addr=256,sh_offset=256,
                            sh_size=64,sh_flags=2,sh_entsize=0,sh_link=3)
            def iter_sections(self): raise AssertionError('eager GNU hash arrays')
            def get_section(self,i): raise AssertionError('eager GNU hash arrays')
        self.assertTrue(hasattr(analyze,'section_metadata'),'missing header-only metadata reader')
        self.assertEqual(analyze.section_metadata(Elf())[0]['type'],'SHT_GNU_HASH')

if __name__=='__main__': unittest.main()
