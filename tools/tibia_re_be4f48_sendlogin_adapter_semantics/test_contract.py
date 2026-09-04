#!/usr/bin/env python3
"""Original synthetic instructions only; no proprietary fixture bytes."""
import importlib.util
from pathlib import Path
import unittest


class Contract(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name('adapter_semantics.py')
        self.assertTrue(path.exists(), 'bounded adapter analyzer missing before client materialization')
        spec = importlib.util.spec_from_file_location('adapter_semantics', path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_virtual_call_preserves_original_receiver(self):
        # mov rbx,rdi; mov rax,[rdi]; call [rax+0x68]
        result = self.module.trace_block(bytes.fromhex('4889fb488b07ff5068'), 0x1000)
        self.assertEqual(result['calls'][0]['receiver'], 'arg:rdi')
        self.assertEqual(result['calls'][0]['target'], 'load64(add(load64(arg:rdi),0x68))')
        self.assertEqual(result['receiver_identity'], 'UNKNOWN')

    def test_call_clobbers_volatile_receiver(self):
        # call arbitrary external; mov rax,[rdi]; call [rax+0x68]
        result = self.module.trace_block(bytes.fromhex('e800000000488b07ff5068'), 0x1000)
        self.assertEqual(result['calls'][1]['receiver'], 'UNKNOWN')

    def test_branch_cannot_be_read_as_linear_proof(self):
        # je +3; mov rdi,rdx; call rax
        result = self.module.trace_block(bytes.fromhex('74034889d7ffd0'), 0x1000)
        self.assertEqual(result['stop_reason'], 'CONTROL_FLOW_BOUNDARY')
        self.assertEqual(result['calls'], [])

    def test_partial_register_write_kills_pointer_identity(self):
        result = self.module.trace_block(bytes.fromhex('bf01000000488b07ff5068'), 0x1000)
        self.assertNotEqual(result['calls'][0]['receiver'], 'arg:rdi')

    def test_exact_fence_rejects_wrong_input_before_elf_parsing(self):
        with self.assertRaisesRegex(ValueError, 'EXACT_CLIENT_FENCE_MISMATCH'):
            self.module.verify_fence(b'original synthetic test', '15.32.be4f48')

    def test_cfg_visits_both_receiver_branches(self):
        self.assertTrue(callable(getattr(self.module, 'trace_paths', None)), 'CFG traversal missing')
        # je call; mov rdi,rdx; call rax; ret
        result = self.module.trace_paths(bytes.fromhex('74034889d7ffd0c3'), 0x1000)
        self.assertTrue(result['complete'])
        self.assertEqual({c['receiver'] for c in result['calls']}, {'arg:rdi', 'arg:rdx'})

    def test_concrete_operation_prunes_wrong_qslot_branch(self):
        self.assertTrue(callable(getattr(self.module, 'trace_paths', None)), 'CFG traversal missing')
        # cmp edi,1; jne ret; call rax; ret
        code = bytes.fromhex('83ff017502ffd0c3')
        self.assertEqual(self.module.trace_paths(code, 0x1000, {'rdi': 0})['calls'], [])
        self.assertEqual(len(self.module.trace_paths(code, 0x1000, {'rdi': 1})['calls']), 1)

    def test_loop_budget_is_not_a_scientific_blocker(self):
        self.assertTrue(callable(getattr(self.module, 'trace_paths', None)), 'CFG traversal missing')
        result = self.module.trace_paths(bytes.fromhex('ebfe'), 0x1000)
        self.assertFalse(result['complete'])
        self.assertEqual(result['stop_reason'], 'LOOP_OR_PATH_BUDGET')

    def test_vector_copy_preserves_two_member_pointer_words(self):
        # movdqu xmm0,[rsp]; movups [rdi+16],xmm0; mov rax,[rdi+16]; call rax
        result=self.module.trace_block(bytes.fromhex('f30f6f04240f114710488b4710ffd0'),0x1000,
                                      memory={(0,8):0x1230,(8,8):0})
        self.assertEqual(result['calls'][0]['target'],'0x1230')

    def test_memory_partial_overwrite_does_not_preserve_old_pointer(self):
        # mov byte [rdi+17],1; mov rax,[rdi+16]; call rax
        result=self.module.trace_block(bytes.fromhex('c6471101488b4710ffd0'),0x1000,
                                      memory={('add(arg:rdi,0x10)',8):0x1230})
        self.assertNotEqual(result['calls'][0]['target'],'0x1230')

    def test_external_call_invalidates_condition_flags(self):
        # cmp edi,1; call rax; jne ret; call rbx; ret
        result=self.module.trace_paths(bytes.fromhex('83ff01ffd07502ffd3c3'),0x1000,{'rdi':0})
        self.assertEqual({c['site'] for c in result['calls']},{'0x1003','0x1007'})

    def test_adapter_trace_stops_at_first_receiver_edge(self):
        # mov rbx,rdi; mov rax,[rdi]; call [rax+0x68]; mov rdi,rbx; call rax; ret
        code=bytes.fromhex('4889fb488b07ff50684889dfffd0c3')
        result=self.module.trace_paths(code,0x1000,stop_at_receiver=True)
        self.assertEqual(len(result['calls']),1)
        self.assertTrue(result['complete'])

    def test_high_byte_write_cannot_forge_branch_condition(self):
        result=self.module.trace_paths(bytes.fromhex('b40183f8017402ffd3c3'),0x1000,{'rax':0})
        self.assertTrue(result['calls'])

    def test_compare_uses_low32_operand(self):
        result=self.module.trace_paths(bytes.fromhex('83ff017402ffd3c3'),0x1000,{'rdi':0x100000001})
        self.assertEqual(result['calls'],[])

    def test_loop_instruction_fails_closed(self):
        result=self.module.trace_paths(bytes.fromhex('e2feffd0c3'),0x1000)
        self.assertFalse(result['complete'])
        self.assertEqual(result['calls'],[])

    def test_call_invalidates_pointer_memory(self):
        result=self.module.trace_paths(bytes.fromhex('4889fbe8000000004889df488b4710ffd0c3'),0x1000,
                                       memory={('add(arg:rdi,0x10)',8):0x1230})
        self.assertTrue(all(c['target']!='0x1230' for c in result['calls']))

    def test_return_only_path_cannot_prove_total_receiver_invocation(self):
        result=self.module.trace_paths(bytes.fromhex('7402ffd0c3'),0x1000,stop_at_receiver=True)
        self.assertFalse(result.get('all_paths_reach_receiver',True))


if __name__ == '__main__':
    unittest.main()
