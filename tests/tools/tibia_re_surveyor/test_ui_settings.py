import json
import unittest

from tools.tibia_re_surveyor.ui_settings import (
    READ_ONLY_SETTINGS_PROBE,
    READER_ID,
    STATIC_SETTINGS_PROBE,
    TYPE_NAME,
    read_ui_settings,
)


class UiSettingsReaderTests(unittest.TestCase):
    @staticmethod
    def _static():
        return json.dumps(
            {
                "state": "AVAILABLE",
                "type_name": TYPE_NAME,
                "type_string_count": 1,
                "clientoptions_literal_count": 1,
            }
        )

    @staticmethod
    def _live():
        return json.dumps(
            {
                "state": "AVAILABLE",
                "reader_id": READER_ID,
                "master_volume": 100,
                "master_volume_old": 100,
                "persistence_relative_path": "conf/clientoptions.json",
                "filesystem_access": "read_only",
                "process_memory_access": "not_used",
            }
        )

    def test_success_is_bounded_to_master_volume_persistence_snapshot(self):
        calls = []

        def runner(command):
            calls.append(command)
            return self._static() if len(calls) == 1 else self._live()

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("AVAILABLE", doc["state"])
        self.assertEqual("TYPED_UI_SETTINGS_MASTER_VOLUME_FILE_READ_ONLY", doc["semantic_state"])
        self.assertEqual(100, doc["master_volume"])
        self.assertEqual(100, doc["master_volume_old"])
        self.assertEqual("read_only", doc["filesystem_access"])
        self.assertEqual("not_used", doc["process_memory_access"])
        self.assertTrue(doc["settings_model_type_present"])
        self.assertFalse(doc["live_ui_application_state_claimed"])
        self.assertFalse(doc["all_settings_model_claimed"])
        self.assertFalse(doc["qsettings_linkage_claimed"])
        self.assertFalse(doc["client_options_to_file_linkage_claimed"])
        self.assertFalse(doc["semantic_promotion_allowed"])
        self.assertEqual(2, len(calls))
        self.assertEqual("python3", calls[0][3])
        self.assertEqual("python3", calls[1][3])

    def test_static_failure_is_fail_closed_and_secret_free(self):
        def runner(command):
            raise RuntimeError("arbitrary static stderr that must not survive")

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("STATIC_SETTINGS_MODEL_FAILED:RuntimeError", doc["reason"])
        self.assertNotIn("arbitrary", json.dumps(doc))
        self.assertFalse(doc["semantic_promotion_allowed"])

    def test_malformed_static_payload_fails_closed(self):
        def runner(command):
            return json.dumps(
                {
                    "state": "AVAILABLE",
                    "type_name": TYPE_NAME,
                    "type_string_count": 1,
                    "clientoptions_literal_count": 2,
                }
            )

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("STATIC_SETTINGS_MODEL_FAILED:RuntimeError", doc["reason"])

    def test_static_payload_with_extra_field_fails_closed(self):
        payload = json.loads(self._static())
        payload["credential"] = "must-not-survive"

        def runner(command):
            return json.dumps(payload)

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertNotIn("credential", json.dumps(doc))
        self.assertNotIn("must-not-survive", json.dumps(doc))

    def test_live_payload_with_extra_field_fails_closed(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._static()
            payload = json.loads(self._live())
            payload["token"] = "must-not-survive"
            return json.dumps(payload)

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertNotIn("token", json.dumps(doc))
        self.assertNotIn("must-not-survive", json.dumps(doc))

    def test_malformed_live_payload_fails_closed(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._static()
            payload = json.loads(self._live())
            payload["master_volume"] = True
            return json.dumps(payload)

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("LIVE_SETTINGS_READ_FAILED:RuntimeError", doc["reason"])
        self.assertEqual(TYPE_NAME, doc["static_evidence"]["type_name"])

    def test_live_known_failure_is_bounded_and_keeps_static_evidence(self):
        calls = []

        def runner(command):
            calls.append(command)
            if len(calls) == 1:
                return self._static()
            raise RuntimeError("CLIENTOPTIONS_MASTER_VOLUME_INVALID secret-noise")

        doc = read_ui_settings(pid=123, start_ticks=456, runner=runner)
        self.assertEqual("UNAVAILABLE", doc["state"])
        self.assertEqual("LIVE_SETTINGS_READ_FAILED:CLIENTOPTIONS_MASTER_VOLUME_INVALID", doc["reason"])
        self.assertEqual(TYPE_NAME, doc["static_evidence"]["type_name"])
        self.assertNotIn("secret-noise", json.dumps(doc))

    def test_probe_sources_bind_package_root_to_live_executable_descriptor(self):
        self.assertIn('exe_fd=os.open(proc_exe,os.O_RDONLY|os.O_CLOEXEC)', READ_ONLY_SETTINGS_PROBE)
        self.assertIn("exe_st=os.fstat(exe_fd)", READ_ONLY_SETTINGS_PROBE)
        self.assertIn('bin_fd=os.open("bin",dir_flags,dir_fd=root_fd)', READ_ONLY_SETTINGS_PROBE)
        self.assertIn('package_exe_fd=os.open("client",file_flags,dir_fd=bin_fd)', READ_ONLY_SETTINGS_PROBE)
        self.assertIn("package_exe_st=os.fstat(package_exe_fd)", READ_ONLY_SETTINGS_PROBE)
        self.assertIn(
            "(package_exe_st.st_dev,package_exe_st.st_ino)!=(exe_st.st_dev,exe_st.st_ino)",
            READ_ONLY_SETTINGS_PROBE,
        )
        self.assertIn("CLIENT_PACKAGE_EXECUTABLE_IDENTITY_MISMATCH", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("CLIENT_EXE_IDENTITY_CHANGED", READ_ONLY_SETTINGS_PROBE)

    def test_probe_sources_are_read_only_allowlisted_and_do_not_read_process_memory(self):
        self.assertIn("os.O_RDONLY", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("os.O_NOFOLLOW", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("package_root=exe.parent.parent", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("dir_fd=root_fd", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("dir_fd=conf_fd", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("CLIENT_PACKAGE_LAYOUT_INVALID", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("CLIENT_NOFOLLOW_UNAVAILABLE", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("stat.S_ISREG", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("pwd.getpwuid", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("os.walk", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("os.O_RDWR", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("os.O_WRONLY", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn(f"/proc/{{pid}}/mem", READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("environ", READ_ONLY_SETTINGS_PROBE)
        self.assertIn('("soundMasterVolume","soundMasterVolumeOld")', READ_ONLY_SETTINGS_PROBE)
        self.assertNotIn("write(", READ_ONLY_SETTINGS_PROBE)
        self.assertIn("STATIC_EXACT_FENCE_MISMATCH", STATIC_SETTINGS_PROBE)
        self.assertIn("tibia::config::TClientOptions", STATIC_SETTINGS_PROBE)
        self.assertIn("clientoptions.json", STATIC_SETTINGS_PROBE)


if __name__ == "__main__":
    unittest.main()
