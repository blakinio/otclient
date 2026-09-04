import unittest
from types import SimpleNamespace

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

    def test_selected_signed_relative_jump_table(self):
        raw=bytes.fromhex('81fabf0000007710488d05f10f0000486314904801d0ffe0c3')
        def read(addr,size):
            self.assertEqual((addr,size),(0x2000+191*4,4))
            return (-0x1000).to_bytes(4,'little',signed=True)
        # Selected signed offset jumps back to start; loop must be detected.
        r=self.module().walk(raw,0x1000,{'rdx':191},read)
        self.assertEqual(r['stop'],'LOOP_OR_BUDGET')

    def test_out_of_range_table_is_not_read(self):
        raw=bytes.fromhex('81fabf0000007710488d05f10f0000486314904801d0ffe0c3')
        def read(addr,size):
            self.fail('out-of-range index read')
        r=self.module().walk(raw,0x1000,{'rdx':192},read)
        self.assertEqual(r['edge'],{'kind':'return','site':'0x1018'})

    def test_unmapped_image_is_value_error(self):
        with self.assertRaises(ValueError):
            self.module().Image.loc(SimpleNamespace(sections=[]),0x1000)

    def test_exact_revision_13_layout(self):
        self.module().qualify_header([13,0,0,0,355,14,0,0,0,0,0,0,0,192])
        with self.assertRaises(ValueError):
            self.module().qualify_header([10,0,0,0,355,14,0,0,0,0,0,0,0,192])

    def test_writable_memory_is_not_a_constant(self):
        img=SimpleNamespace(sections=[(0x1000,0x2000,0,3)],relative_relocations={},read=lambda a,s:b'\0'*s)
        with self.assertRaises(ValueError):self.module().readonly_read(img,0x1000,4)

    def test_saved_receiver_survives_stack_prologue(self):
        r=self.module().walk(bytes.fromhex('574831ff5fe9f31f0000'),0x1000,{})
        self.assertEqual(r['edge']['receiver'],'entry:object')

    def test_stack_store_clobbers_saved_value(self):
        r=self.module().walk(bytes.fromhex('574831c0488904245fe9f21f0000'),0x1000,{})
        self.assertEqual(r['edge']['receiver'],0)

    def test_stack_arithmetic_and_frame_copy(self):
        r=self.module().walk(bytes.fromhex('554889e54883ec084883c4085de9ef1f0000'),0x1000,{})
        self.assertEqual(r['stop'],'EDGE_REACHED')

    def test_non64_stack_operation_is_not_modeled_as_qword(self):
        r=self.module().walk(bytes.fromhex('576650585fe800000000'),0x1000,{})
        self.assertEqual(r['stop'],'UNSUPPORTED_STACK_WIDTH')

    def test_pop_rsp_fails_closed(self):
        r=self.module().walk(bytes.fromhex('505ce800000000'),0x1000,{})
        self.assertEqual(r['stop'],'UNSUPPORTED_STACK_DESTINATION')

    def test_new_callable_is_not_known_signal_or_registration(self):
        c=self.module().classify_edge({'kind':'tail','target':'0xdd8df0'})
        self.assertFalse(c['connection_proven'])
        self.assertEqual(c['next_endpoint_identity'],'UNKNOWN')

if __name__=='__main__':
    unittest.main()
