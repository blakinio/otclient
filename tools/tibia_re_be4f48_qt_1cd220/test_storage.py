import unittest
from storage import receiver_storage, storage_region


class StorageContract(unittest.TestCase):
    def flow(self, code, **kw):
        return receiver_storage(bytes.fromhex(code), 0x1000, **kw)

    def writes(self, code):
        return [s for s in self.flow(code)['receiver_stores'] if not s['private_stack']]

    def test_direct_receiver_store_has_destination_and_width(self):
        stores = self.writes('48894f28c3')
        self.assertEqual(len(stores), 1)
        self.assertEqual(stores[0]['site'], '0x1000')
        self.assertEqual(stores[0]['width'], 8)
        self.assertEqual(stores[0]['destination'], {'base': 'entry:rdi', 'offset': 40})

    def test_callee_preserved_receiver_can_be_written_to_call_result(self):
        stores = self.writes('4889cbe80000000048895820c3')
        self.assertEqual(stores[0]['destination'], {'base': 'call_return:0x1003', 'offset': 32})
        self.assertEqual(stores[0]['destination_owner'], 'UNKNOWN')

    def test_call_clobbers_volatile_receiver(self):
        self.assertEqual(self.writes('e80000000048894f28c3'), [])

    def test_conflicting_branch_join_loses_receiver(self):
        self.assertEqual(self.writes('85c0740231c948894f28c3'), [])

    def test_partial_register_write_loses_receiver(self):
        self.assertEqual(self.writes('b10148894f28c3'), [])

    def test_partial_store_is_not_receiver_pointer_store(self):
        self.assertEqual(self.writes('894f28c3'), [])

    def test_stack_spill_round_trip(self):
        stores = self.writes('4883ec1048890c24488b04244889074883c410c3')
        self.assertEqual(len(stores), 1)
        self.assertEqual(stores[0]['site'], '0x100c')

    def test_overlapping_partial_stack_write_invalidates_spill(self):
        self.assertEqual(self.writes('4883ec1048890c24c644240400488b0424488907c3'), [])

    def test_segment_override_cannot_read_ordinary_stack_spill(self):
        self.assertEqual(self.writes('4883ec1048890c2464488b0424488907c3'), [])

    def test_segmented_store_is_explicit_unknown_boundary(self):
        p = self.flow('6448890fc3')
        self.assertEqual(p['receiver_stores'], [])
        self.assertIn('SEGMENTED_MEMORY', [x['kind'] for x in p['boundaries']])

    def test_address_size_override_does_not_preserve_64bit_destination(self):
        p = self.flow('6748890fc3')
        self.assertEqual(p['receiver_stores'][0]['destination'], 'UNKNOWN')

    def test_unknown_destination_is_not_a_nonstack_proof(self):
        p = self.flow('48890bc3')
        self.assertEqual(p['receiver_stores'][0]['destination_provenance'], 'UNKNOWN')

    def test_implicit_pushfq_cannot_leave_old_receiver_spill(self):
        self.assertEqual(self.writes('488d5c24f848890b9c488b03488907c3'), [])

    def test_bnd_jump_has_no_unreachable_store_fallthrough(self):
        p = self.flow('f2eb0348890fc3')
        self.assertEqual(p['receiver_stores'], [])
        self.assertEqual(p['cfg']['0x1000'], ['0x1006'])

    def test_privileged_resume_cannot_fall_through_to_store(self):
        p = self.flow('0faa48890fc3')
        self.assertEqual(p['receiver_stores'], [])
        self.assertFalse(p['coverage_complete'])

    def test_unknown_memory_alias_invalidates_stack_spill(self):
        self.assertEqual(self.writes('4883ec1048890c24488916488b0424488907c3'), [])

    def test_call_may_mutate_escaped_stack_spill(self):
        self.assertEqual(self.writes('4883ec1048890c24e800000000488b0424488907c3'), [])

    def test_fixed_point_identity_preserving_loop(self):
        p = self.flow('4889cb85c075fc48891fc3')
        self.assertTrue(p['fixedpoint_reached'])
        self.assertTrue(p['coverage_complete'])
        self.assertEqual(len(p['receiver_stores']), 1)
        self.assertFalse(p['termination_proven'])

    def test_loop_join_does_not_emit_transient_store(self):
        p = self.flow('4889cb48891f85c0740431dbebf5c3')
        self.assertEqual(p['receiver_stores'], [])

    def test_update_budget_does_not_emit_transient_store(self):
        p = self.flow('48894f28c3', max_updates=1)
        self.assertEqual(p['receiver_stores'], [])
        self.assertFalse(p['fixedpoint_reached'])

    def test_instruction_cap_is_not_absence_proof(self):
        p = self.flow('9048894f28c3', max_instructions=1)
        self.assertEqual(p['receiver_stores'], [])
        self.assertTrue(p['resource_limit_hit'])
        self.assertFalse(p['coverage_complete'])

    def test_unsupported_control_stops_path(self):
        p = self.flow('0f0548894f28c3')
        self.assertFalse(p['coverage_complete'])
        self.assertEqual(p['receiver_stores'], [])

    def test_fde_must_be_unique_bounded_and_exact_entry(self):
        self.assertEqual(storage_region([(0x1000, 0x1100)], 0x1000), (0x1000, 0x1100))
        for rows in [[], [(0xff0, 0x1100)], [(0x1000, 0x4001)], [(0x1000, 0x1100)] * 2]:
            with self.assertRaises(ValueError):
                storage_region(rows, 0x1000)


if __name__ == '__main__':
    unittest.main()
