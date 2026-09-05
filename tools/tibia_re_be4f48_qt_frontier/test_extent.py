import unittest
import frontier

class ExtentTests(unittest.TestCase):
    def test_exact_selected_read_only(self):
        self.assertTrue(hasattr(frontier,'selected_body'))
        class Raw:
            def __len__(self):return 4096
            def __getitem__(self,k):
                assert k.start==100 and k.stop==185
                return b'\x90'*85
        s=[dict(index=14,addr=0x1d3ff0,size=85,off=100,flags=6,type='SHT_PROGBITS')]
        r=dict(address='0x1d3ff0',size=85,section_index=14,symbol_index=3860)
        self.assertEqual(len(frontier.selected_body(Raw(),s,r)),85)
        for key,value in [('address','0x1d3ff1'),('size',86),('section_index',15),('symbol_index',3861)]:
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'PROMOTED_DEFINITION_CHANGED'):
                frontier.selected_body(Raw(),s,dict(r,**{key:value}))
        with self.assertRaisesRegex(ValueError,'SYMBOL_MAPPING'):
            frontier.selected_body(Raw(),s+[dict(s[0],index=15,addr=0x1d3ff8,size=8)],r)

if __name__=='__main__':unittest.main()
