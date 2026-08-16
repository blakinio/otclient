#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import unittest

WORKER = pathlib.Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh')


class CanonicalXcbGlIntegrationTests(unittest.TestCase):
    @staticmethod
    def source() -> str:
        return WORKER.read_text(encoding='utf-8')

    @classmethod
    def bootstrap_body(cls) -> str:
        source = cls.source()
        start = source.index('bootstrap() {')
        end = source.index('\nprobe() {', start)
        return source[start:end]

    def test_production_client_launch_does_not_disable_xcb_gl_integration(self) -> None:
        body = self.bootstrap_body()
        self.assertNotIn('QT_XCB_GL_INTEGRATION=none', body)
        self.assertNotIn('QT_XCB_GL_INTEGRATION=', body)

    def test_software_quick_backend_is_preserved(self) -> None:
        body = self.bootstrap_body()
        self.assertIn('QT_QUICK_BACKEND=software', body)

    def test_no_new_rhi_or_gl_backend_is_forced(self) -> None:
        body = self.bootstrap_body()
        self.assertNotIn('QSG_RHI_BACKEND=', body)
        self.assertNotIn('QT_OPENGL=', body)
        self.assertNotIn('LIBGL_ALWAYS_SOFTWARE=', body)

    def test_identity_network_and_secret_boundaries_are_unchanged(self) -> None:
        source = self.source()
        for needle in (
            'SIZE=51965216',
            'SHA=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
            'env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD',
            'PROXYCHAINS_CONF_FILE="$SESSION/proxychains.conf"',
            'wait_for_window "$pid" "$display" "$xdotool" 120 .25',
            'verify_tracked_group "$pgid"',
        ):
            self.assertIn(needle, source)


if __name__ == '__main__':
    unittest.main()
