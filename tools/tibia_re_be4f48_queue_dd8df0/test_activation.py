import unittest
from activation import project, qualify_tail, classify, ACTIVATE


class ActivationContract(unittest.TestCase):
    def p(self, prefix='', suffix='e800000000c3', **kw):
        return project(bytes.fromhex(prefix + suffix), 0x1000, **kw)

    def test_tail_accepts_exact_jump(self):
        qualify_tail(bytes.fromhex('e900000000'), 0x1000, 0x1005)

    def test_call_cannot_replace_tail(self):
        with self.assertRaises(ValueError):
            qualify_tail(bytes.fromhex('e800000000'), 0x1000, 0x1005)

    def test_wrong_tail_target_rejected(self):
        with self.assertRaises(ValueError):
            qualify_tail(bytes.fromhex('e900000000'), 0x1000, 0x2000)

    def test_receiver_and_numeric_argument_before_first_call(self):
        p = self.p('babf000000')
        self.assertEqual(p['registers']['rdi'], {'kind': 'ENTRY_RECEIVER'})
        self.assertEqual(p['registers']['rdx'], {'kind': 'CONSTANT', 'value': 191})
        self.assertEqual(p['boundary']['kind'], 'DIRECT_CALL')
        self.assertEqual(p['instructions'], 2)

    def test_rip_lea_is_linktime_static_address(self):
        self.assertEqual(self.p('488d3520000000')['registers']['rsi'],
                         {'kind': 'STATIC_ADDRESS', 'value': 0x1027})

    def test_memory_load_does_not_guess_value(self):
        self.assertEqual(self.p('488b3520000000')['registers']['rsi'], 'UNKNOWN')

    def test_partial_receiver_write_loses_identity(self):
        self.assertEqual(self.p('66bf0000')['registers']['rdi'], 'UNKNOWN')

    def test_truncated_receiver_move_is_unknown(self):
        self.assertEqual(self.p('89ff')['registers']['rdi'], 'UNKNOWN')

    def test_full_width_receiver_move_survives(self):
        self.assertEqual(self.p('4889fe4889f7')['registers']['rdi'], {'kind': 'ENTRY_RECEIVER'})

    def test_zero_xor_has_exact_constant(self):
        self.assertEqual(self.p('31c9')['registers']['rcx'], {'kind': 'CONSTANT', 'value': 0})

    def test_32bit_immediate_zero_extends(self):
        self.assertEqual(self.p('baffffffff')['registers']['rdx'], {'kind': 'CONSTANT', 'value': 0xffffffff})

    def test_segmented_lea_is_not_proven_static_pointer(self):
        self.assertEqual(self.p('64488d3520000000')['registers']['rsi'], 'UNKNOWN')

    def test_unknown_implicit_write_stops(self):
        self.assertEqual(self.p('9c')['boundary']['kind'], 'UNMODELED_INSTRUCTION')

    def test_conditional_branch_is_not_explored(self):
        self.assertEqual(self.p('7400')['boundary']['kind'], 'BRANCH_STOP')

    def test_prefixed_tail_stops_and_cannot_fallthrough(self):
        p = self.p('', 'f2e900010000')
        self.assertEqual(p['boundary']['kind'], 'DIRECT_TAIL')
        self.assertEqual(p['instructions'], 1)

    def test_privileged_control_stops(self):
        self.assertEqual(self.p('0faa')['boundary']['kind'], 'UNMODELED_CONTROL')

    def test_instruction_cap_is_incomplete(self):
        p = self.p('9090', max_instructions=1)
        self.assertTrue(p['resource_limit_hit'])
        self.assertEqual(p['registers']['rdi'], 'UNKNOWN')

    def test_return_is_not_activation(self):
        self.assertEqual(self.p('', 'c3')['boundary']['kind'], 'RETURN')

    def test_activate_requires_exact_import_and_receiver(self):
        p = self.p('488d3520000000babf00000031c9')
        self.assertEqual(classify(p, ACTIVATE)[0], 'POSITIVE_EXACT_ACTIVATION_ARGUMENTS')
        self.assertEqual(classify(p, '_different_activate')[0], 'SOURCE_BLOCKER')
        p['registers']['rdi'] = 'UNKNOWN'
        self.assertEqual(classify(p, ACTIVATE)[0], 'SOURCE_BLOCKER')

    def test_unknown_instruction_cannot_support_activation(self):
        self.assertEqual(classify(self.p('9c'), ACTIVATE)[0], 'SOURCE_BLOCKER')


if __name__ == '__main__':
    unittest.main()
