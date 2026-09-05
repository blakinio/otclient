import unittest
from construction import construct, qualify_tail


class ConstructionContract(unittest.TestCase):
    PREFIX = '4883ec184889742408488d0c24'

    def p(self, prefix=None, suffix='', **kw):
        return construct(bytes.fromhex((self.PREFIX if prefix is None else prefix) + suffix + 'e800000000c3'), 0x1000, **kw)

    def test_live_cell_and_pointer_escape(self):
        p = self.p()
        self.assertTrue(p['construction_escape_proven'])
        self.assertEqual(p['live_cells'], [{'offset': -16, 'width': 8, 'value': {'kind': 'ENTRY_ARG', 'register': 'rsi'}}])
        self.assertEqual(p['escapes'][0]['register'], 'rcx')
        self.assertEqual(p['escapes'][0]['frame_offset'], -24)
        self.assertEqual(p['escapes'][0]['relative_cell_offsets'], [8])

    def test_frame_identity_is_not_logical_object_identity(self):
        self.assertEqual(self.p()['logical_object_type'], 'UNKNOWN')

    def test_partial_overwrite_invalidates_full_cell(self):
        self.assertFalse(self.p(suffix='c644240900')['construction_escape_proven'])

    def test_unknown_external_alias_invalidates_cells(self):
        self.assertEqual(self.p(suffix='488937')['live_cells'], [])

    def test_deallocation_invalidates_escaped_pointer(self):
        p = self.p(suffix='4883c418')
        self.assertEqual(p['live_cells'], [])
        self.assertEqual(p['escapes'], [])

    def test_caller_stack_is_not_private_frame(self):
        self.assertFalse(self.p('4889742408488d0c24')['construction_escape_proven'])

    def test_unknown_source_has_no_known_cell(self):
        self.assertEqual(self.p('4883ec18488b374889742408488d0c24')['live_cells'], [])

    def test_partial_source_register_loses_entry_pointer(self):
        self.assertEqual(self.p('4883ec1889f64889742408488d0c24')['live_cells'], [])

    def test_constant_zero_cell_is_proven(self):
        p = self.p('4883ec1831f64889742408488d0c24')
        self.assertEqual(p['live_cells'][0]['value'], {'kind': 'CONSTANT', 'value': 0})

    def test_push_constructs_allocated_cell(self):
        p = self.p('564889e1')
        self.assertTrue(p['construction_escape_proven'])
        self.assertEqual(p['live_cells'][0]['offset'], -8)

    def test_pop_releases_cell(self):
        self.assertFalse(self.p('564889e15e')['construction_escape_proven'])

    def test_address_size_override_is_unknown_alias(self):
        self.assertEqual(self.p(suffix='674889742408')['live_cells'], [])

    def test_segmented_write_is_unknown_alias(self):
        self.assertEqual(self.p(suffix='644889742408')['live_cells'], [])

    def test_unknown_implicit_stack_write_stops(self):
        p = self.p(suffix='9c')
        self.assertFalse(p['construction_escape_proven'])
        self.assertEqual(p['boundary']['kind'], 'UNMODELED_INSTRUCTION')

    def test_conditional_branch_is_not_followed(self):
        self.assertFalse(self.p(suffix='7400')['construction_escape_proven'])

    def test_register_pointer_copy_preserves_stack_offset(self):
        p = self.p('4883ec184889e048897424084889c1')
        self.assertEqual(p['escapes'][0]['frame_offset'], -24)

    def test_truncated_stack_rebase_cannot_preserve_frame(self):
        self.assertFalse(self.p(suffix='89e4')['construction_escape_proven'])

    def test_pointer_outside_frame_does_not_escape_constructed_region(self):
        self.assertFalse(self.p('4883ec184889742408488d4c2418')['construction_escape_proven'])

    def test_instruction_cap_drops_escape_claim(self):
        p = self.p(max_instructions=1)
        self.assertTrue(p['resource_limit_hit'])
        self.assertFalse(p['construction_escape_proven'])

    def test_no_activation_or_import_classification(self):
        p = self.p()
        self.assertNotIn('activation', p)
        self.assertNotIn('import', p)

    def test_tail_kind_qualification(self):
        qualify_tail(bytes.fromhex('e900000000'), 0x1000, 0x1005)
        with self.assertRaises(ValueError):
            qualify_tail(bytes.fromhex('e800000000'), 0x1000, 0x1005)


if __name__ == '__main__':
    unittest.main()
