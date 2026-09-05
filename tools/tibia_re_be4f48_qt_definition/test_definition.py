import struct
import unittest
from definition import lookup, NAME

H = 3389874950

def fixture():
    data = bytearray(4096)
    def section(i, typ, off, size, flags=2, entsize=0, link=0):
        return dict(index=i, type=typ, off=off, size=size, addr=off+0x10000,
                    flags=flags, entsize=entsize, link=link)
    sections = [section(0,'SHT_NULL',0,0,0),section(1,'SHT_DYNAMIC',128,80,3,16),
                section(2,'SHT_GNU_HASH',256,64,2,0,3),
                section(3,'SHT_DYNSYM',512,96,2,24,4),
                section(4,'SHT_STRTAB',768,600),section(5,'SHT_PROGBITS',2048,256,6)]
    for i,(tag,val) in enumerate([(0x6ffffef5,0x10100),(6,0x10200),(11,24),(5,0x10300),(0,0)]):
        struct.pack_into('<QQ',data,128+16*i,tag,val)
    struct.pack_into('<IIIIQII',data,256,1,1,1,5,(1<<(H%64))|(1<<((H>>5)%64)),1,H|1)
    struct.pack_into('<IBBHQQ',data,536,1,0x12,0,5,0x10800,32)
    data[769:769+len(NAME)+1] = NAME.encode()+b'\0'
    return data, sections

class DefinitionTests(unittest.TestCase):
    def test_positive(self):
        d,s=fixture(); r=lookup(d,s)
        self.assertEqual(r['symbol_index'],1)
        self.assertEqual(r['address'],'0x10800')
        self.assertEqual(r['size'],32)
        self.assertEqual(r['name'],NAME)
        self.assertEqual(r['chain_entries'],1)
        self.assertEqual(r['candidate_names'],1)

    def rejects(self, change, marker):
        d,s=fixture(); change(d,s)
        with self.assertRaisesRegex(ValueError,marker): lookup(d,s)

    def test_zero_buckets(self): self.rejects(lambda d,s:struct.pack_into('<I',d,256,0),'HASH_HEADER')
    def test_nonpower_bloom(self): self.rejects(lambda d,s:struct.pack_into('<I',d,264,3),'HASH_HEADER')
    def test_shift(self): self.rejects(lambda d,s:struct.pack_into('<I',d,268,64),'HASH_HEADER')
    def test_bloom_negative(self): self.rejects(lambda d,s:struct.pack_into('<Q',d,272,0),'BLOOM_NEGATIVE')
    def test_bucket_empty(self): self.rejects(lambda d,s:struct.pack_into('<I',d,280,0),'BUCKET_EMPTY')
    def test_bucket_outside_symbols(self): self.rejects(lambda d,s:struct.pack_into('<I',d,280,9),'SYMBOL_INDEX')
    def test_undefined(self): self.rejects(lambda d,s:struct.pack_into('<H',d,542,0),'DEFINITION_RECORD')
    def test_wrong_type(self): self.rejects(lambda d,s:d.__setitem__(540,0x11),'DEFINITION_RECORD')
    def test_local(self): self.rejects(lambda d,s:d.__setitem__(540,2),'DEFINITION_RECORD')
    def test_hidden(self): self.rejects(lambda d,s:d.__setitem__(541,2),'DEFINITION_RECORD')
    def test_zero_extent(self): self.rejects(lambda d,s:struct.pack_into('<Q',d,552,0),'DEFINITION_EXTENT')
    def test_extent_outside(self): self.rejects(lambda d,s:struct.pack_into('<Q',d,552,257),'DEFINITION_EXTENT')
    def test_nonexec(self): self.rejects(lambda d,s:s[5].update(flags=2),'DEFINITION_EXTENT')
    def test_nobits(self): self.rejects(lambda d,s:s[5].update(type='SHT_NOBITS'),'DEFINITION_EXTENT')
    def test_name_outside(self): self.rejects(lambda d,s:struct.pack_into('<I',d,536,600),'NAME_OFFSET')
    def test_name_nonterminated(self): self.rejects(lambda d,s:s[4].update(size=2),'NAME_TERMINATOR')
    def test_name_nonascii(self): self.rejects(lambda d,s:d.__setitem__(769,255),'NAME_ASCII')
    def test_name_cap(self): self.rejects(lambda d,s:d.__setitem__(slice(769,1282),b'x'*513),'NAME_TERMINATOR')
    def test_dynamic_duplicate(self): self.rejects(lambda d,s:struct.pack_into('<QQ',d,176,6,0x10200),'DYNAMIC_TAGS')
    def test_wrong_dynamic_pointer(self): self.rejects(lambda d,s:struct.pack_into('<Q',d,136,0x10101),'SECTION_MAPPING')
    def test_wrong_syment(self): self.rejects(lambda d,s:struct.pack_into('<Q',d,168,16),'DYNAMIC_TAGS')
    def test_wrong_link(self): self.rejects(lambda d,s:s[3].update(link=2),'SECTION_LINK')
    def test_chain_cap(self):
        d,s=fixture();struct.pack_into('<I',d,284,H)
        with self.assertRaisesRegex(ValueError,'HASH_CHAIN_LIMIT'):lookup(d,s,chain_limit=1)
    def test_candidate_cap(self):
        d,s=fixture()
        with self.assertRaisesRegex(ValueError,'HASH_CANDIDATE_LIMIT'):lookup(d,s,candidate_limit=0)
    def test_hash_collision_skips_unrelated_name(self):
        d,s=fixture();struct.pack_into('<II',d,284,42,H|1)
        struct.pack_into('<IBBHQQ',d,560,1,0x12,0,5,0x10800,32)
        struct.pack_into('<I',d,536,999999)
        r=lookup(d,s);self.assertEqual(r['symbol_index'],2);self.assertEqual(r['candidate_names'],1)
    def test_duplicate_full_match(self):
        d,s=fixture();struct.pack_into('<II',d,284,H,H|1)
        d[560:584]=d[536:560]
        with self.assertRaisesRegex(ValueError,'NAME_MATCH_COUNT'):lookup(d,s)
    def test_full_name_mismatch(self): self.rejects(lambda d,s:d.__setitem__(769,ord('X')),'NAME_MATCH_COUNT')
    def test_ambiguous_extent(self):
        def change(d,s):s.append(dict(s[5],index=6))
        self.rejects(change,'DEFINITION_EXTENT')
    def test_no_function_content_reads(self):
        d,s=fixture()
        class Guard:
            def __len__(self): return len(d)
            def __getitem__(self,k):
                if not isinstance(k,slice) or k.start>=2048 or k.stop>1368:
                    raise AssertionError('unrelated content read')
                return d[k]
        self.assertEqual(lookup(Guard(),s)['symbol_index'],1)

if __name__ == '__main__': unittest.main()
