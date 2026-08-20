from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import http.client
import json
from typing import Any, Iterator, Mapping
from urllib import parse

_MAX_BYTES = 2 * 1024 * 1024


class OllamaError(RuntimeError):
    pass


class OllamaTransportError(OllamaError):
    pass


class OllamaProtocolError(OllamaError):
    pass


class OllamaModelError(OllamaError):
    pass


@dataclass(frozen=True)
class InferenceOptions:
    temperature: float = 0.0
    seed: int = 42
    num_ctx: int = 4096
    num_predict: int = 1024
    connect_timeout_s: float = 3.0
    inference_timeout_s: float = 120.0
    keep_alive_s: int = 15

    def validate(self) -> None:
        if self.temperature != 0:
            raise ValueError("temperature must be 0")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool):
            raise ValueError("seed must be integer")
        if not 256 <= self.num_ctx <= 262_144:
            raise ValueError("num_ctx outside bounded range")
        if not 32 <= self.num_predict <= 4096:
            raise ValueError("num_predict outside bounded range")
        if not 0 < self.connect_timeout_s <= 30 or not 0 < self.inference_timeout_s <= 300:
            raise ValueError("timeout outside bounded range")
        if (
            not isinstance(self.keep_alive_s, int)
            or isinstance(self.keep_alive_s, bool)
            or not 0 <= self.keep_alive_s <= 60
        ):
            raise ValueError("keep_alive_s outside bounded range")


@dataclass(frozen=True)
class ModelInfo:
    tag: str
    digest: str
    context_length: int | None


@dataclass(frozen=True)
class Generation:
    response: str
    response_sha256: str
    done_reason: str
    total_duration_ns: int | None
    load_duration_ns: int | None
    prompt_eval_count: int | None
    prompt_eval_duration_ns: int | None
    eval_count: int | None
    eval_duration_ns: int | None


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


class OllamaClient:
    """Loopback-only local client. It intentionally has no pull/cloud method."""

    def __init__(self, endpoint: str = "http://127.0.0.1:11434") -> None:
        parsed = parse.urlparse(endpoint)
        if parsed.scheme != "http" or parsed.username or parsed.password:
            raise ValueError("endpoint must be unauthenticated loopback HTTP")
        if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("endpoint must be loopback-only")
        if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
            raise ValueError("endpoint must not contain path/query/fragment")
        self.endpoint = endpoint.rstrip("/")
        self._host = parsed.hostname
        self._port = parsed.port or 80

    def _json(
        self,
        path: str,
        *,
        payload: Mapping[str, Any] | None = None,
        connect_timeout: float,
        timeout: float,
    ) -> Mapping[str, Any]:
        data = None
        headers = {"Accept": "application/json"}
        method = "GET"
        if payload is not None:
            data = json.dumps(payload, separators=(",", ":")).encode()
            headers["Content-Type"] = "application/json"
            method = "POST"
        connection = http.client.HTTPConnection(
            self._host, self._port, timeout=connect_timeout
        )
        try:
            connection.connect()
            if connection.sock is None:
                raise OllamaTransportError("Ollama connection has no socket")
            connection.sock.settimeout(timeout)
            connection.request(method, path, body=data, headers=headers)
            response = connection.getresponse()
            status = response.status
            raw = response.read(_MAX_BYTES + 1)
        except OllamaTransportError:
            raise
        except (http.client.HTTPException, TimeoutError, OSError) as exc:
            raise OllamaTransportError(f"Ollama request failed: {exc}") from exc
        finally:
            connection.close()
        if not 200 <= status < 300:
            raise OllamaProtocolError(f"Ollama HTTP status {status}")
        if len(raw) > _MAX_BYTES:
            raise OllamaProtocolError("Ollama response too large")
        try:
            doc = json.loads(raw.decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise OllamaProtocolError("Ollama returned invalid JSON") from exc
        if not isinstance(doc, Mapping):
            raise OllamaProtocolError("Ollama response must be an object")
        if doc.get("error"):
            raise OllamaProtocolError("Ollama returned an error")
        return doc

    def version(self, *, timeout: float = 3.0) -> str:
        value = self._json("/api/version", connect_timeout=timeout, timeout=timeout).get("version")
        if not isinstance(value, str) or not value:
            raise OllamaProtocolError("malformed version response")
        return value

    def models(self, *, timeout: float = 3.0) -> tuple[ModelInfo, ...]:
        raw = self._json("/api/tags", connect_timeout=timeout, timeout=timeout).get("models")
        if not isinstance(raw, list):
            raise OllamaProtocolError("malformed tags response")
        result: list[ModelInfo] = []
        for item in raw:
            if not isinstance(item, Mapping):
                raise OllamaProtocolError("malformed model entry")
            tag, digest = item.get("name"), item.get("digest")
            details = item.get("details")
            context = details.get("context_length") if isinstance(details, Mapping) else None
            if not isinstance(tag, str) or not isinstance(digest, str):
                raise OllamaProtocolError("malformed model identity")
            result.append(ModelInfo(tag, digest, _int(context)))
        return tuple(result)

    def loaded_models(self, *, timeout: float = 3.0) -> tuple[str, ...]:
        raw = self._json("/api/ps", connect_timeout=timeout, timeout=timeout).get("models")
        if not isinstance(raw, list):
            raise OllamaProtocolError("malformed ps response")
        names: list[str] = []
        for item in raw:
            if not isinstance(item, Mapping):
                raise OllamaProtocolError("malformed loaded-model entry")
            name = item.get("name") or item.get("model")
            if not isinstance(name, str) or not name:
                raise OllamaProtocolError("malformed loaded-model identity")
            names.append(name)
        return tuple(names)

    def assert_single_model_slot(self, tag: str, *, timeout: float = 3.0) -> None:
        loaded = self.loaded_models(timeout=timeout)
        if len(loaded) > 1 or any(name != tag for name in loaded):
            raise OllamaModelError(
                "another local model is already loaded; refusing concurrent model load"
            )

    def unload_model(self, tag: str, *, timeout: float = 5.0) -> None:
        self._json(
            "/api/generate",
            payload={"model": tag, "keep_alive": 0},
            connect_timeout=timeout,
            timeout=timeout,
        )

    @contextmanager
    def model_session(self, tag: str, *, timeout: float = 3.0) -> Iterator["OllamaClient"]:
        self.assert_single_model_slot(tag, timeout=timeout)
        try:
            yield self
        finally:
            loaded = self.loaded_models(timeout=timeout)
            if tag in loaded:
                self.unload_model(tag, timeout=max(timeout, 5.0))

    def require_model(
        self,
        tag: str,
        *,
        expected_digest: str | None = None,
        timeout: float = 3.0,
    ) -> ModelInfo:
        matches = [model for model in self.models(timeout=timeout) if model.tag == tag]
        if len(matches) != 1:
            raise OllamaModelError(f"required local model {tag!r} is not uniquely installed")
        model = matches[0]
        if expected_digest is not None and model.digest != expected_digest:
            raise OllamaModelError("local model digest mismatch")
        return model

    def generate(
        self,
        tag: str,
        prompt: str,
        *,
        options: InferenceOptions = InferenceOptions(),
    ) -> Generation:
        options.validate()
        self.assert_single_model_slot(tag, timeout=options.connect_timeout_s)
        if not isinstance(prompt, str) or not prompt:
            raise ValueError("prompt must be non-empty")
        payload = {
            "model": tag,
            "prompt": prompt,
            "stream": False,
            "keep_alive": f"{options.keep_alive_s}s",
            "options": {
                "temperature": options.temperature,
                "seed": options.seed,
                "num_ctx": options.num_ctx,
                "num_predict": options.num_predict,
            },
        }
        doc = self._json(
            "/api/generate",
            payload=payload,
            connect_timeout=options.connect_timeout_s,
            timeout=options.inference_timeout_s,
        )
        if doc.get("done") is not True:
            raise OllamaProtocolError("generation did not complete")
        reason = doc.get("done_reason")
        if not isinstance(reason, str):
            raise OllamaProtocolError("generation lacks done_reason")
        if reason == "length":
            raise OllamaProtocolError("generation hit output limit")
        response = doc.get("response")
        if not isinstance(response, str) or not response:
            raise OllamaProtocolError("generation returned empty response")
        returned_model = doc.get("model")
        if isinstance(returned_model, str) and returned_model and returned_model != tag:
            raise OllamaProtocolError("unexpected model in response")
        # `thinking` is deliberately ignored and can never leave this method.
        return Generation(
            response=response,
            response_sha256=hashlib.sha256(response.encode()).hexdigest(),
            done_reason=reason,
            total_duration_ns=_int(doc.get("total_duration")),
            load_duration_ns=_int(doc.get("load_duration")),
            prompt_eval_count=_int(doc.get("prompt_eval_count")),
            prompt_eval_duration_ns=_int(doc.get("prompt_eval_duration")),
            eval_count=_int(doc.get("eval_count")),
            eval_duration_ns=_int(doc.get("eval_duration")),
        )
