from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

from .evidence import sha256_file, validate_model_observation, validate_visual_evidence


def admit_residency(resident_models: list[str] | None, target: str) -> tuple[bool, str]:
    if resident_models is None:
        return False, "RESIDENCY_UNKNOWN"
    if not resident_models:
        return True, "EMPTY_SLOT"
    if len(resident_models) == 1 and resident_models[0] == target:
        return True, "EXACT_TARGET_ONLY"
    if len(resident_models) > 1:
        return False, "MULTIPLE_RESIDENT_MODELS"
    return False, "DIFFERENT_RESIDENT_MODEL"


def _loopback_base(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("local model endpoint must be loopback HTTP")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("local model endpoint must not include credentials/query/fragment")
    return endpoint.rstrip("/")


def _local_json_request(endpoint: str, path: str, payload: dict[str, Any] | None = None, timeout: float = 30.0) -> dict[str, Any]:
    base = _loopback_base(endpoint)
    data = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request = Request(base + path, data=data, headers={"Content-Type": "application/json"})
    opener = build_opener(ProxyHandler({}))
    with opener.open(request, timeout=timeout) as response:
        raw = response.read()
    decoded = json.loads(raw.decode("utf-8"))
    if not isinstance(decoded, dict):
        raise ValueError("provider response must be a JSON object")
    return decoded


def query_ollama_ps(endpoint: str = "http://127.0.0.1:11434", timeout: float = 5.0) -> list[str]:
    response = _local_json_request(endpoint, "/api/ps", timeout=timeout)
    models = response.get("models")
    if not isinstance(models, list):
        raise ValueError("Ollama /api/ps models missing")
    names: list[str] = []
    for entry in models:
        if not isinstance(entry, dict):
            raise ValueError("Ollama /api/ps model entry invalid")
        name = entry.get("name") or entry.get("model")
        if not isinstance(name, str) or not name:
            raise ValueError("Ollama /api/ps model name invalid")
        names.append(name)
    return names


def query_ollama_model_digest(
    endpoint: str, model: str, timeout: float = 5.0
) -> str:
    if not isinstance(model, str) or not model:
        raise ValueError("model invalid")
    response = _local_json_request(endpoint, "/api/tags", timeout=timeout)
    models = response.get("models")
    if not isinstance(models, list):
        raise ValueError("Ollama /api/tags models missing")
    matches = []
    for entry in models:
        if not isinstance(entry, dict):
            raise ValueError("Ollama /api/tags model entry invalid")
        name = entry.get("name") or entry.get("model")
        if name == model:
            matches.append(entry)
    if len(matches) != 1:
        raise ValueError(f"installed model identity not unique: {model}")
    digest = matches[0].get("digest")
    if not isinstance(digest, str) or len(digest) != 64 or any(
        c not in "0123456789abcdefABCDEF" for c in digest
    ):
        raise ValueError("installed model digest invalid")
    return digest.lower()


def unload_ollama_model(
    endpoint: str, model: str, timeout: float = 30.0
) -> list[str]:
    if not isinstance(model, str) or not model:
        raise ValueError("model invalid")
    _local_json_request(
        endpoint,
        "/api/generate",
        payload={"model": model, "stream": False, "keep_alive": 0},
        timeout=timeout,
    )
    resident = query_ollama_ps(endpoint, timeout=min(timeout, 5.0))
    if resident:
        raise RuntimeError(f"MODEL_UNLOAD_NOT_VERIFIED:{resident}")
    return resident


def release_ollama_model_if_owned(
    endpoint: str, model: str, timeout: float = 30.0
) -> list[str]:
    resident = query_ollama_ps(endpoint, timeout=min(timeout, 5.0))
    if not resident:
        return []
    if resident != [model]:
        raise RuntimeError(f"MODEL_SLOT_NOT_EXCLUSIVE_AT_CLEANUP:{resident}")
    return unload_ollama_model(endpoint, model, timeout=timeout)


def run_ollama_trial(
    endpoint: str,
    model: str,
    image_path: str | Path,
    prompt: str,
    *,
    evidence_ref: str,
    capture_sha256: str,
    model_profile_id: str,
    source_monotonic_ns: int | None = None,
    keep_alive: str = "0s",
    num_ctx: int = 4096,
    num_predict: int = 256,
    timeout: float = 120.0,
) -> dict[str, Any]:
    resident = query_ollama_ps(endpoint)
    admitted, reason = admit_residency(resident, model)
    if not admitted:
        raise RuntimeError(f"MODEL_SLOT_NOT_EXCLUSIVE:{reason}:{resident}")
    if not isinstance(evidence_ref, str) or not evidence_ref:
        raise ValueError("evidence_ref invalid")
    if not isinstance(capture_sha256, str) or len(capture_sha256) != 64 or any(
        c not in "0123456789abcdefABCDEF" for c in capture_sha256
    ):
        raise ValueError("capture_sha256 invalid")
    if not isinstance(model_profile_id, str) or not model_profile_id:
        raise ValueError("model_profile_id invalid")
    if source_monotonic_ns is not None and (
        not isinstance(source_monotonic_ns, int) or isinstance(source_monotonic_ns, bool)
    ):
        raise ValueError("source_monotonic_ns invalid")
    if not isinstance(num_ctx, int) or isinstance(num_ctx, bool) or num_ctx <= 0:
        raise ValueError("num_ctx invalid")
    if not isinstance(num_predict, int) or isinstance(num_predict, bool) or num_predict <= 0:
        raise ValueError("num_predict invalid")

    image = Path(image_path)
    actual_sha256 = sha256_file(image)
    if actual_sha256.lower() != capture_sha256.lower():
        raise ValueError("capture_sha256 does not match image bytes")
    encoded = base64.b64encode(image.read_bytes()).decode("ascii")
    request = {
        "model": model,
        "messages": [{"role": "user", "content": prompt, "images": [encoded]}],
        "format": "json",
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"temperature": 0, "num_ctx": num_ctx, "num_predict": num_predict},
    }
    response = _local_json_request(endpoint, "/api/chat", payload=request, timeout=timeout)
    message = response.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("Ollama response message.content missing")
    try:
        observation = json.loads(message["content"])
    except json.JSONDecodeError as exc:
        raise ValueError("model output is not strict JSON") from exc
    observation_errors = validate_model_observation(observation)
    if observation_errors:
        raise ValueError("model observation invalid: " + "; ".join(observation_errors))

    visual_evidence = {
        "schema_version": 1,
        "capture": {
            "evidence_ref": evidence_ref,
            "sha256": capture_sha256.lower(),
            "source_monotonic_ns": source_monotonic_ns,
        },
        "model": {"model_profile_id": model_profile_id},
        "observation": observation,
        "quality": {
            "schema_valid": True,
            "visual_only": True,
            "structural_authority": False,
            "unknown_fields": [],
        },
    }
    schema_errors = validate_visual_evidence(visual_evidence)
    telemetry = {
        key: response.get(key)
        for key in (
            "total_duration",
            "load_duration",
            "prompt_eval_duration",
            "eval_duration",
            "prompt_eval_count",
            "eval_count",
        )
    }
    return {
        "visual_evidence": visual_evidence,
        "schema_errors": schema_errors,
        "telemetry": telemetry,
        "residency_admission": reason,
    }
