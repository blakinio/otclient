"""Original synthetic instruction fixtures, no official bytes."""
import unittest
try:
    from callee import qualify_call, callee_graph, exact_owner
except ImportError:
    qualify_call=callee_graph=exact_owner=None


class CalleeContract(unittest.TestCase):
    def require(self,f): self.assertTrue(callable(f),'missing bounded callee behavior')

    def test_exact_call_guard(self):
        self.require(qualify_call)
        qualify_call(bytes.fromhex('e80b000000'),0x1000,0x1010)
        with self.assertRaises(ValueError): qualify_call(bytes.fromhex('e80b000000'),0x1000,0x1011)
        with self.assertRaises(ValueError): qualify_call(bytes.fromhex('e90b000000'),0x1000,0x1010)

    def test_local_calls_are_only_conditional_on_return(self):
        self.require(callee_graph)
        d=callee_graph(bytes.fromhex('e80b000000e806000000c3'),0x1000)
        self.assertEqual(d['calls'],[{'site':'0x1000','target':'0x1010'},{'site':'0x1005','target':'0x1010'}])
        self.assertTrue(d['conditional_on_calls_returning'])
        self.assertFalse(d['runtime_return_or_throw_semantics_proven'])
        self.assertEqual(d['cfg'],{'0x1000':['0x1005'],'0x1005':['0x100a'],'0x100a':[]})

    def test_tail_does_not_traverse_callee(self):
        self.require(callee_graph)
        d=callee_graph(bytes.fromhex('e90b000000'),0x1000)
        self.assertEqual(d['exits'],[{'kind':'DIRECT_TAIL','site':'0x1000','target':'0x1010'}])
        self.assertEqual(d['reachable_instructions'],1)

    def test_call_at_fde_end_is_explicit_return_frontier(self):
        self.require(callee_graph)
        d=callee_graph(bytes.fromhex('e80b000000'),0x1000)
        self.assertEqual(d['exits'],[{'kind':'CALL_RETURN_OUTSIDE_FDE','site':'0x1000','target':'0x1005'}])
        self.assertFalse(d['runtime_return_or_throw_semantics_proven'])

    def test_loop_has_two_edges_and_no_termination_claim(self):
        self.require(callee_graph)
        d=callee_graph(bytes.fromhex('e2fec3'),0x1000)
        self.assertEqual(d['cfg']['0x1000'],['0x1000','0x1002'])
        self.assertFalse(d['termination_proven'])

    def test_unknown_or_truncated_control_is_incomplete(self):
        self.require(callee_graph)
        for raw in ('ffe0','ffd0c3','0f','0f0b','90'):
            self.assertFalse(callee_graph(bytes.fromhex(raw),0x1000)['complete'])

    def test_symbol_identity_must_be_exact_unique_defined_function(self):
        self.require(exact_owner)
        row={'name':'synthetic','address':0x1000,'size':16,'type':'STT_FUNC','section':1}
        self.assertEqual(exact_owner([row],0x1000,(0x1000,0x1010)),'synthetic')
        for rows in ([],[row,row],[dict(row,address=0xfff)],[dict(row,section='SHN_UNDEF')],[dict(row,type='STT_OBJECT')],[dict(row,size=32)]):
            self.assertIsNone(exact_owner(rows,0x1000,(0x1000,0x1010)))


if __name__=='__main__': unittest.main()
