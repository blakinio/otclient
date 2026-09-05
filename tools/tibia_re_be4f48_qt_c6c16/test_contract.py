"""Original synthetic bytes only; never official-client fixtures."""
import unittest
try:
    from continuation import qualify_branch, bounded_region, first_transfers, plt_binding
except ImportError:
    qualify_branch = bounded_region = first_transfers = plt_binding = None


class Contract(unittest.TestCase):
    def require(self, function):
        self.assertTrue(callable(function), 'required bounded continuation behavior missing')

    def test_branch_exact(self):
        self.require(qualify_branch)
        qualify_branch(bytes.fromhex('0f850a000000'), 0x1000, 0x1010)
        with self.assertRaises(ValueError):
            qualify_branch(bytes.fromhex('0f850a000000'), 0x1000, 0x1011)
        with self.assertRaises(ValueError):
            qualify_branch(bytes.fromhex('e90b000000'), 0x1000, 0x1010)

    def test_unique_containing_bounded_fde(self):
        self.require(bounded_region)
        self.assertEqual(bounded_region([(0x1000,0x1100)],0x1010), (0x1000,0x1100))
        for rows in ([],[(0x1000,0x1100)]*2,[(0x1000,0x1400)]):
            with self.assertRaises(ValueError): bounded_region(rows,0x1010)

    def test_stop_at_first_call(self):
        self.require(first_transfers)
        result=first_transfers(bytes.fromhex('90e80a000000e814000000c3'),0x1000,0x1000)
        self.assertEqual(result['boundaries'],[{'kind':'CALL','site':'0x1001','target':'0x1010'}])
        self.assertEqual(result['reachable_instructions'],2)

    def test_both_conditional_edges(self):
        self.require(first_transfers)
        result=first_transfers(bytes.fromhex('7405e809000000c3'),0x1000,0x1000)
        self.assertEqual({x['kind'] for x in result['boundaries']},{'CALL','RETURN'})

    def test_unknowns_do_not_look_complete(self):
        self.require(first_transfers)
        for data in ('ffe0','0f','ebfe'):
            result=first_transfers(bytes.fromhex(data),0x1000,0x1000)
            self.assertFalse(result['complete'])

    def test_no_scan_beyond_first_transfer(self):
        self.require(first_transfers)
        result=first_transfers(bytes.fromhex('c30f'),0x1000,0x1000)
        self.assertTrue(result['complete'])
        self.assertEqual(result['reachable_instructions'],1)

    def test_loop_is_not_a_fallthrough_proof(self):
        self.require(first_transfers)
        result=first_transfers(bytes.fromhex('e2fec3'),0x1000,0x1000)
        self.assertFalse(result['complete'])

    def test_segment_override_is_not_plain_got_binding(self):
        self.require(plt_binding)
        self.assertIsNone(plt_binding(bytes.fromhex('64ff2509000000'),0x1000,{0x1010:'synthetic_import'}))

    def test_plt_only_actual_first_jump(self):
        self.require(plt_binding)
        self.assertEqual(plt_binding(bytes.fromhex('ff250a000000'),0x1000,{0x1010:'synthetic_import'}),'synthetic_import')
        self.assertIsNone(plt_binding(bytes.fromhex('c3ff2509000000'),0x1000,{0x1010:'synthetic_import'}))
        self.assertIsNone(plt_binding(bytes.fromhex('ff250a000000'),0x1000,{}))


if __name__=='__main__': unittest.main()
