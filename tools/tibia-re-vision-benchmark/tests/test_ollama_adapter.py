import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vision_benchmark import (  # noqa: E402
    UnsafeInputError,
    ensure_secret_safe,
    query_ollama_ps,
    run_ollama_trial,
)


def model_observation():
    return {
        "screen_class": "LOGIN_SCREEN",
        "visible_text": ["ACCOUNT LOGIN"],
        "ui_objects": [],
        "appeared": [],
        "disappeared": [],
        "changed": [],
    }


class FakeOllamaHandler(BaseHTTPRequestHandler):
    chat_content = json.dumps(model_observation())
    last_chat = None

    def log_message(self, *_args):
        pass

    def do_GET(self):
        if self.path == "/api/ps":
            body = json.dumps({"models": [{"name": "qwen-test"}]}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
            return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length", "0"))
        type(self).last_chat = json.loads(self.rfile.read(length))
        body = json.dumps({
            "message": {"role": "assistant", "content": type(self).chat_content},
            "total_duration": 100,
            "load_duration": 10,
            "prompt_eval_duration": 20,
            "eval_duration": 70,
            "prompt_eval_count": 4,
            "eval_count": 8,
        }).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)


class OllamaAdapterTests(unittest.TestCase):
    def setUp(self):
        FakeOllamaHandler.chat_content = json.dumps(model_observation())
        FakeOllamaHandler.last_chat = None
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllamaHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.endpoint = f"http://127.0.0.1:{self.server.server_port}"
        self.temp = tempfile.TemporaryDirectory()
        self.image = Path(self.temp.name) / "fixture.png"
        self.image.write_bytes(b"not-a-real-image-but-adapter-only")

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.temp.cleanup()

    def test_query_ps_returns_model_names(self):
        self.assertEqual(query_ollama_ps(self.endpoint), ["qwen-test"])

    def test_non_loopback_endpoint_is_rejected(self):
        with self.assertRaises(ValueError):
            query_ollama_ps("http://example.com:11434")

    def test_chat_sends_format_json_and_keepalive_zero(self):
        result = run_ollama_trial(
            self.endpoint,
            "qwen-test",
            self.image,
            "Return JSON",
            evidence_ref="fixture:test",
            capture_sha256="b" * 64,
            model_profile_id="qwen-test-profile",
            keep_alive="0s",
        )
        sent = FakeOllamaHandler.last_chat
        self.assertEqual(sent["format"], "json")
        self.assertEqual(sent["keep_alive"], "0s")
        self.assertFalse(sent["stream"])
        self.assertEqual(sent["options"]["temperature"], 0)
        self.assertTrue(sent["messages"][0]["images"])
        self.assertEqual(result["visual_evidence"]["observation"]["screen_class"], "LOGIN_SCREEN")
        self.assertEqual(result["visual_evidence"]["capture"]["sha256"], "b" * 64)
        self.assertEqual(result["visual_evidence"]["model"]["model_profile_id"], "qwen-test-profile")
        self.assertIs(result["visual_evidence"]["quality"]["structural_authority"], False)
        self.assertEqual(result["telemetry"]["eval_count"], 8)

    def test_invalid_model_json_is_not_repaired(self):
        FakeOllamaHandler.chat_content = "not-json"
        with self.assertRaises(ValueError):
            run_ollama_trial(
                self.endpoint, "qwen-test", self.image, "Return JSON",
                evidence_ref="fixture:test", capture_sha256="b" * 64,
                model_profile_id="qwen-test-profile", keep_alive="0s"
            )


    def test_model_cannot_author_authority_or_provenance_fields(self):
        FakeOllamaHandler.chat_content = json.dumps({
            **model_observation(),
            "quality": {"structural_authority": True},
            "capture": {"sha256": "0" * 64},
        })
        with self.assertRaises(ValueError):
            run_ollama_trial(
                self.endpoint, "qwen-test", self.image, "Return JSON",
                evidence_ref="fixture:test", capture_sha256="b" * 64,
                model_profile_id="qwen-test-profile", keep_alive="0s"
            )

    def test_secret_metadata_is_rejected_before_inference(self):
        with self.assertRaises(UnsafeInputError):
            ensure_secret_safe({"secret_safe": False, "reason": "credentials_possible"})
        self.assertTrue(ensure_secret_safe({"secret_safe": True, "reason": "synthetic_fixture"}))


if __name__ == "__main__":
    unittest.main()
