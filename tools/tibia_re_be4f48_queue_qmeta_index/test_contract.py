import unittest

class Contract(unittest.TestCase):
    def module(self):
        import qmeta_index
        return qmeta_index

    def test_exact_fence_rejects_wrong_source(self):
        with self.assertRaisesRegex(ValueError, 'FENCE'):
            self.module().verify_fence(b'original synthetic fixture', '15.32.be4f48')

    def test_method_row_uses_six_word_stride(self):
        self.assertEqual(self.module().method_row(0x1000,14,191,192,192),0x1000+56+191*24)

    def test_out_of_range_method_is_not_signal(self):
        with self.assertRaises(ValueError):
            self.module().method_row(0x1000,14,191,192,191)

    def test_numeric_dispatch_is_not_registration(self):
        self.assertFalse(self.module().classify_edge({'kind':'tail','target':'0xbd2190'})['connection_proven'])

    def test_unknown_branch_fails_closed(self):
        # test esi,esi; jne +1; ret; ret -- esi intentionally unknown.
        r=self.module().walk(bytes.fromhex('85f67501c3c3'),0x1000,{})
        self.assertEqual(r['stop'],'UNPROVEN_BRANCH_PREDICATE')

    def test_selected_numeric_branch(self):
        r=self.module().walk(bytes.fromhex('85f67501c3c3'),0x1000,{'rsi':0})
        self.assertEqual(r['edge'],{'kind':'return','site':'0x1004'})

    def test_loop_fails_closed(self):
        r=self.module().walk(bytes.fromhex('ebfe'),0x1000,{})
        self.assertEqual(r['stop'],'LOOP_OR_BUDGET')

if __name__=='__main__':
    unittest.main()
