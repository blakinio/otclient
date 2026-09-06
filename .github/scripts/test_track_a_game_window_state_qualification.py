#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import struct
import sys
import unittest

SCRIPT = Path(__file__).with_name('track_a_game_window_state_qualification.py')
if not SCRIPT.is_file():
    raise AssertionError('GAME_WINDOW_STATE_QUALIFICATION_IMPLEMENTATION_MISSING')
spec = importlib.util.spec_from_file_location('game_window_state_qualification', SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class SemanticClassificationTests(unittest.TestCase):
    def test_ingame_is_the_only_positive_known_state(self):
        result = module.classify_qstring_payload(6, 'INGAME'.encode('utf-16-le'))
        self.assertEqual('INGAME', result['semantic_state'])
        self.assertEqual('INGAME', result['known_text'])
        self.assertEqual(6, result['value_length'])
        self.assertEqual(hashlib.sha256(b'INGAME').hexdigest(), result['known_value_sha256'])

    def test_empty_is_known_non_ingame(self):
        result = module.classify_qstring_payload(0, b'')
        self.assertEqual('EMPTY', result['semantic_state'])
        self.assertEqual('', result['known_text'])
        self.assertEqual(hashlib.sha256(b'').hexdigest(), result['known_value_sha256'])

    def test_other_text_is_not_retained(self):
        result = module.classify_qstring_payload(5, 'LOGIN'.encode('utf-16-le'))
        self.assertEqual('OTHER', result['semantic_state'])
        self.assertEqual(5, result['value_length'])
        self.assertIsNone(result['known_text'])
        self.assertIsNone(result['known_value_sha256'])

    def test_invalid_utf16_fails_closed(self):
        with self.assertRaisesRegex(module.QualificationError, 'QSTRING_UTF16_INVALID'):
            module.classify_qstring_payload(1, b'\x00\xd8')


class MappingBoundsTests(unittest.TestCase):
    def setUp(self):
        self.regions = [
            module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]'),
            module.Mapping(0x3000, 0x4000, 'r--p', '/client'),
            module.Mapping(0x5000, 0x6000, 'r--p', '[vvar]'),
        ]

    def test_accepts_fully_bounded_readable_payload(self):
        self.assertTrue(module.payload_range_allowed(self.regions, 0x1100, 12))
        self.assertTrue(module.payload_range_allowed(self.regions, 0x3100, 12))

    def test_rejects_cross_mapping_or_unmapped_payload(self):
        self.assertFalse(module.payload_range_allowed(self.regions, 0x1ffc, 8))
        self.assertFalse(module.payload_range_allowed(self.regions, 0x2500, 2))

    def test_rejects_special_kernel_mapping(self):
        self.assertFalse(module.payload_range_allowed(self.regions, 0x5100, 2))


class MappingBaseTests(unittest.TestCase):
    def test_uses_lowest_executable_mapping_candidate_like_current_snapshot_reader(self):
        exe = Path('/client')
        regions = [
            module.Mapping(0x55555000, 0x55556000, 'r--p', '/client', 0x0),
            module.Mapping(0x55557000, 0x55558000, 'r-xp', '/client', 0x1000),
            module.Mapping(0x70000000, 0x70001000, 'rw-p', '[heap]', 0x0),
        ]
        self.assertEqual(0x55555000, module._mapping_base(regions, exe))


class QStringMemberTests(unittest.TestCase):
    def test_reads_exact_24_byte_member_and_payload(self):
        regions = [module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]')]
        member = struct.pack('<QQq', 0x1110, 0x1200, 6)
        calls = []
        def read(address, length):
            calls.append((address, length))
            self.assertEqual((0x1200, 12), (address, length))
            return 'INGAME'.encode('utf-16-le')
        result = module.decode_qstring_member(member, regions, read)
        self.assertEqual('INGAME', result['semantic_state'])
        self.assertEqual([(0x1200, 12)], calls)

    def test_empty_member_reads_no_payload(self):
        regions = [module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]')]
        member = struct.pack('<QQq', 0, 0, 0)
        result = module.decode_qstring_member(member, regions, lambda *_: self.fail('payload read not allowed'))
        self.assertEqual('EMPTY', result['semantic_state'])

    def test_rejects_length_over_bound(self):
        regions = [module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]')]
        member = struct.pack('<QQq', 0x1110, 0x1200, module.MAX_QSTRING_CHARS + 1)
        with self.assertRaisesRegex(module.QualificationError, 'QSTRING_LENGTH_OUT_OF_BOUNDS'):
            module.decode_qstring_member(member, regions, lambda *_: b'')

    def test_rejects_payload_pointer_outside_allowed_mapping(self):
        regions = [module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]')]
        member = struct.pack('<QQq', 0x1110, 0x9000, 6)
        with self.assertRaisesRegex(module.QualificationError, 'QSTRING_PAYLOAD_POINTER_OUT_OF_BOUNDS'):
            module.decode_qstring_member(member, regions, lambda *_: b'')

    def test_rejects_short_payload_read(self):
        regions = [module.Mapping(0x1000, 0x2000, 'rw-p', '[heap]')]
        member = struct.pack('<QQq', 0x1110, 0x1200, 6)
        with self.assertRaisesRegex(module.QualificationError, 'QSTRING_PAYLOAD_SHORT_READ'):
            module.decode_qstring_member(member, regions, lambda *_: b'bad')


class ObjectUniquenessTests(unittest.TestCase):
    def test_requires_exactly_one_controller(self):
        self.assertEqual(0x1230, module.select_unique_object([0x1230]))
        with self.assertRaisesRegex(module.QualificationError, 'GAME_WINDOW_CONTROLLER_COUNT=0'):
            module.select_unique_object([])
        with self.assertRaisesRegex(module.QualificationError, 'GAME_WINDOW_CONTROLLER_COUNT=2'):
            module.select_unique_object([0x1230, 0x4560])


class EventSanitizationTests(unittest.TestCase):
    def test_event_never_promotes_and_retains_no_raw_pointer_or_other_text(self):
        event = module.build_event(
            pid=123,
            start_ticks=456,
            uniqueness='PROVEN',
            semantic={'semantic_state': 'OTHER', 'value_length': 4, 'known_text': None, 'known_value_sha256': None},
            event_kind='STATE_CHANGE',
        )
        self.assertFalse(event['in_game_claimed'])
        self.assertFalse(event['semantic_promotion_performed'])
        self.assertEqual('OTHER', event['semantic_state'])
        self.assertNotIn('object_address', event)
        self.assertNotIn('data_pointer', event)
        self.assertNotIn('raw_payload', event)
        self.assertNotIn('value', event)


class StaticAuthorityGuardTests(unittest.TestCase):
    def test_reader_derives_current_binding_and_contains_no_historical_authority(self):
        text = SCRIPT.read_text(encoding='utf-8')
        for forbidden in (
            '0x30c2250', '0x30c3488', '0x30b6ba0', '0xd28890', '0x4d7dc0',
            'CURRENT_VERSION = "15.32.75d4a0"', 'GAME_WINDOW_STATE_MEMBER_OFFSET = 0x60',
            'anchor.EXPECTED_SHA256', 'anchor.EXPECTED_SIZE',
        ):
            self.assertNotIn(forbidden.lower(), text.lower())
        self.assertIn('current_client_fence', text)
        self.assertIn('analyze_game_window_state', text)
        self.assertIn('binding = analyze_game_window_state(exe)', text)
        self.assertIn('binding["read_property"]["backing_member"]', text)
        self.assertIn('binding["rtti"]["vptr_offset"]', text)

    def test_proc_mem_is_read_only_and_forbidden_surfaces_are_absent(self):
        text = SCRIPT.read_text(encoding='utf-8')
        self.assertIn('os.O_RDONLY | os.O_CLOEXEC', text)
        for forbidden in ('ptrace', 'process_vm_writev', '/proc/{pid}/environ', 'gdb', 'uprobe', 'tracefs', 'xdotool', 'pyautogui'):
            self.assertNotIn(forbidden.lower(), text.lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)
