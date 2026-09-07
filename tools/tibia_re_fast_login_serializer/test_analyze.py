import unittest
from analyze import unique, mapped_slice, exact_name_offsets, decode_snapshot


class BoundsTests(unittest.TestCase):
    def test_unique_is_not_first_match(self):
        self.assertEqual(unique([17]), 17)
        for rows in ([], [17, 18], [17, 17]):
            with self.assertRaises(ValueError):
                unique(rows)

    def test_mapping_requires_whole_file_backed_span(self):
        self.assertEqual(mapped_slice(b'abcdef', [(100, 1, 4)], 101, 2), b'cd')
        for address, size in ((99, 1), (103, 2), (100, 0), (100, -1)):
            with self.assertRaises(ValueError):
                mapped_slice(b'abcdef', [(100, 1, 4)], address, size)

    def test_overlap_and_truncated_file_rejected(self):
        for segments in ([(100, 0, 4), (100, 0, 4)], [(100, 5, 4)]):
            with self.assertRaises(ValueError):
                mapped_slice(b'abcdef', segments, 100, 2)

    def test_partial_overlapping_segment_rejected(self):
        with self.assertRaises(ValueError):
            mapped_slice(b'abcdef', [(100, 0, 4), (101, 1, 1)], 100, 3)

    def test_complete_nul_delimited_type_name(self):
        self.assertEqual(exact_name_offsets(b'x\0N3FooE\0suffixN3FooE\0N3FooEX\0', 'N3FooE'), [2])
        self.assertEqual(exact_name_offsets(b'N3FooE\0', 'N3FooE'), [0])

    def test_decode_is_lexical_not_reachability_proof(self):
        # UD2 followed by RET is retained lexically, never claimed reachable.
        result = decode_snapshot(bytes.fromhex('0f0bc3'), 0x1000)
        self.assertEqual([r['mnemonic'] for r in result['instructions']], ['ud2', 'ret'])
        self.assertFalse(result['control_flow_proven'])
        self.assertFalse(result['runtime_execution_proven'])
        self.assertNotIn('bytes', result['instructions'][0])

    def test_truncated_decode_rejected(self):
        with self.assertRaises(ValueError):
            decode_snapshot(bytes.fromhex('48'), 0x1000)

    def test_decode_cap_does_not_claim_complete(self):
        with self.assertRaises(ValueError):
            decode_snapshot(bytes.fromhex('9090c3'), 0x1000, cap=2)


if __name__ == '__main__':
    unittest.main()
