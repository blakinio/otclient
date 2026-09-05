import unittest
from callflow import selected_inputs


class InputContract(unittest.TestCase):
    def project(self, prefix='', **kw):
        data = bytes.fromhex(prefix)
        site = 0x1000 + len(data)
        return selected_inputs(data + bytes.fromhex('e800000000c3'), 0x1000, site, site + 5, **kw)

    def test_capture_before_selected_call_clobber(self):
        p = self.project()['selected_call']
        self.assertTrue(p['captured'])
        self.assertEqual(p['registers']['rcx'], {'base': 'entry:rcx', 'offset': 0})
        self.assertEqual(p['receiver_carriers'], ['rcx'])

    def test_moved_receiver_is_an_exact_register_carrier(self):
        self.assertIn('rdi', self.project('4889cf')['selected_call']['receiver_carriers'])

    def test_prior_call_clobbers_volatile_receiver(self):
        self.assertEqual(self.project('e800000000')['selected_call']['receiver_carriers'], [])

    def test_saved_receiver_survives_prior_call_conditionally(self):
        p = self.project('4889cbe8000000004889df')['selected_call']
        self.assertEqual(p['receiver_carriers'], ['rdi'])

    def test_outgoing_stack_slots_map_to_precall_rsp(self):
        p = self.project('4883ec1848890c2448894c240848894c241031c9')['selected_call']
        self.assertEqual(p['receiver_carriers'], ['stack+0', 'stack+8', 'stack+16'])
        self.assertEqual(len(p['stack_slots']), 3)

    def test_partial_stack_overwrite_loses_only_overlapped_value(self):
        p = self.project('4883ec1048890c24c64424040031c9')['selected_call']
        self.assertEqual(p['receiver_carriers'], [])

    def test_movq_write_cannot_leave_stale_receiver_stack_argument(self):
        p = self.project('4883ec1048890c24660fd6042431c9')['selected_call']
        self.assertEqual(p['receiver_carriers'], [])

    def test_cmpxchg_possible_write_cannot_leave_must_receiver_argument(self):
        p = self.project('4883ec1048890c244831c0480fb1142431c9')['selected_call']
        self.assertEqual(p['receiver_carriers'], [])

    def test_cmpxchg_implicit_rax_write_cannot_preserve_receiver(self):
        p = self.project('4889c8480fb1d74889c631c9')['selected_call']
        self.assertEqual(p['receiver_carriers'], [])

    def test_conflicting_branch_join_loses_receiver(self):
        self.assertEqual(self.project('85c0740231c9')['selected_call']['receiver_carriers'], [])

    def test_branch_successors_do_not_replace_selected_call_target(self):
        p = self.project('85c0740231c9')['selected_call']
        self.assertEqual(p['target'], '0x100b')

    def test_partial_register_write_is_unknown(self):
        self.assertEqual(self.project('b101')['selected_call']['registers']['rcx'], 'UNKNOWN')

    def test_unknown_target_is_rejected(self):
        with self.assertRaises(ValueError):
            selected_inputs(bytes.fromhex('e800000000c3'), 0x1000, 0x1000, 0x2000)

    def test_unreachable_selected_call_is_not_captured(self):
        p = selected_inputs(bytes.fromhex('eb05e800000000c3'), 0x1000, 0x1002, 0x1007)
        self.assertFalse(p['selected_call']['captured'])
        self.assertEqual(p['selected_call']['receiver_carriers'], [])

    def test_bnd_jump_cannot_invent_call_reachability(self):
        p = selected_inputs(bytes.fromhex('f2eb05e800000000c3'), 0x1000, 0x1003, 0x1008)
        self.assertFalse(p['selected_call']['captured'])

    def test_implicit_stack_write_stops_before_selected_call(self):
        self.assertFalse(self.project('488d5c24f848890b9c')['selected_call']['captured'])

    def test_privileged_resume_stops_before_selected_call(self):
        self.assertFalse(self.project('0faa')['selected_call']['captured'])

    def test_segmented_stack_load_cannot_be_receiver_register(self):
        p = self.project('4883ec1048890c2464488b3c2431c9')['selected_call']
        self.assertEqual(p['registers']['rdi'], 'UNKNOWN')

    def test_address_size_override_cannot_load_full_stack_token(self):
        p = self.project('4883ec1048890c2467488b3c2431c9')['selected_call']
        self.assertEqual(p['registers']['rdi'], 'UNKNOWN')

    def test_unknown_call_result_is_provenance_not_receiver(self):
        p = self.project('e8000000004889c7')['selected_call']
        self.assertEqual(p['registers']['rdi'], {'base': 'call_return:0x1000', 'offset': 0})
        self.assertEqual(p['receiver_carriers'], [])

    def test_resource_cap_cannot_emit_transient_input(self):
        p = self.project('90', max_updates=1)
        self.assertTrue(p['resource_limit_hit'])
        self.assertFalse(p['selected_call']['captured'])

    def test_no_storage_scan_output(self):
        self.assertNotIn('receiver_stores', self.project())


if __name__ == '__main__':
    unittest.main()
