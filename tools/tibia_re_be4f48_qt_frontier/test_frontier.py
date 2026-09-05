import unittest
from frontier import frontier

class FrontierTests(unittest.TestCase):
    def f(self,h,**kw): return frontier(bytes.fromhex(h),0x1000,**kw)
    def test_return(self):
        r=self.f('90 c3');self.assertTrue(r['complete']);self.assertEqual(r['reachable_instructions'],2)
        self.assertEqual(r['boundaries'],[dict(kind='RETURN',site='0x1001')])
    def test_call_stops(self):
        r=self.f('e8 00000000 0f0b');self.assertTrue(r['complete']);self.assertEqual(r['reachable_instructions'],1)
        self.assertEqual(r['boundaries'],[dict(kind='CALL',site='0x1000',target='0x1005')])
    def test_tail(self):
        r=self.f('eb 20');self.assertTrue(r['complete']);self.assertEqual(r['boundaries'][0]['kind'],'TAIL_JUMP')
    def test_branch(self):
        r=self.f('7401 90 c3');self.assertTrue(r['complete']);self.assertEqual(r['cfg']['0x1000'],['0x1002','0x1003'])
    def test_external_conditional(self):
        r=self.f('7420 c3');self.assertTrue(r['complete']);self.assertEqual(len(r['boundaries']),2)
    def test_cycle(self):
        r=self.f('ebfe');self.assertTrue(r['complete']);self.assertTrue(r['cycle_present']);self.assertFalse(r['termination_proven'])
    def test_diamond(self):
        r=self.f('7403 90 eb01 90 c3');self.assertTrue(r['complete']);self.assertFalse(r['cycle_present'])
    def test_indirect_call(self):
        r=self.f('ffd0');self.assertFalse(r['complete']);self.assertEqual(r['boundaries'][0]['kind'],'INDIRECT_CALL')
    def test_indirect_jump(self):
        r=self.f('ffe0');self.assertFalse(r['complete']);self.assertEqual(r['boundaries'][0]['kind'],'INDIRECT_BRANCH')
    def test_trap(self): self.assertFalse(self.f('0f0b')['complete'])
    def test_syscall(self): self.assertFalse(self.f('0f05')['complete'])
    def test_far_return(self): self.assertFalse(self.f('cb')['complete'])
    def test_transaction(self): self.assertFalse(self.f('c7f800000000')['complete'])
    def test_truncated(self): self.assertFalse(self.f('e8')['complete'])
    def test_fallthrough(self): self.assertFalse(self.f('90')['complete'])
    def test_overlap(self):
        r=self.f('7401 b800000000 c3');self.assertFalse(r['complete']);self.assertIn('OVERLAPPING_DECODE',[x['kind'] for x in r['boundaries']])
    def test_cap(self):
        r=self.f('90c3',instruction_limit=1);self.assertFalse(r['complete']);self.assertTrue(r['limit_reached'])
    def test_empty(self):
        with self.assertRaisesRegex(ValueError,'SCOPE'):self.f('')
    def test_large(self):
        with self.assertRaisesRegex(ValueError,'SCOPE'):self.f('90'*86)
    def test_no_raw_output(self):
        r=self.f('90c3');self.assertNotIn('mnemonic',str(r));self.assertNotIn('bytes',str(r))

if __name__=='__main__': unittest.main()
