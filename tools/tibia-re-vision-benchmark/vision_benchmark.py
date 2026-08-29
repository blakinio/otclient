from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

SCREEN_CLASSES = {
    "LOGIN_SCREEN",
    "CHARACTER_SELECT",
    "IN_GAME_VISUAL",
    "WORLD_EXIT",
    "OTHER",
    "UNKNOWN",
}

WEIGHTS = {
    "semantic_correctness": 0.30,
    "hallucination_resistance": 0.25,
    "ocr_exact_match": 0.20,
    "repeatability": 0.10,
    "latency_efficiency": 0.10,
    "memory_efficiency": 0.05,
}


def _is_str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_object_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, dict) for item in value)


def validate_visual_evidence(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be object"]
    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    capture = payload.get("capture")
    if not isinstance(capture, dict):
        capture = {}
        errors.append("capture must be object")
    if not isinstance(capture.get("evidence_ref"), str) or not capture.get("evidence_ref"):
        errors.append("capture.evidence_ref invalid")
    digest = capture.get("sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
        errors.append("capture.sha256 invalid")
    monotonic = capture.get("source_monotonic_ns")
    if monotonic is not None and (not isinstance(monotonic, int) or isinstance(monotonic, bool)):
        errors.append("capture.source_monotonic_ns invalid")

    model = payload.get("model")
    if not isinstance(model, dict):
        model = {}
        errors.append("model must be object")
    if not isinstance(model.get("model_profile_id"), str) or not model.get("model_profile_id"):
        errors.append("model.model_profile_id invalid")

    observation = payload.get("observation")
    if not isinstance(observation, dict):
        observation = {}
        errors.append("observation must be object")
    if observation.get("screen_class") not in SCREEN_CLASSES:
        errors.append("observation.screen_class invalid")
    if not _is_str_list(observation.get("visible_text")):
        errors.append("observation.visible_text invalid")
    for key in ("ui_objects", "appeared", "disappeared", "changed"):
        if not _is_object_list(observation.get(key)):
            errors.append(f"observation.{key} invalid")

    quality = payload.get("quality")
    if not isinstance(quality, dict):
        quality = {}
        errors.append("quality must be object")
    if quality.get("schema_valid") is not True:
        errors.append("quality.schema_valid must be true")
    if quality.get("visual_only") is not True:
        errors.append("quality.visual_only must be true")
    if quality.get("structural_authority") is not False:
        errors.append("quality.structural_authority must be false")
    if not _is_str_list(quality.get("unknown_fields")):
        errors.append("quality.unknown_fields invalid")
    return errors



def validate_model_observation(observation: Any) -> list[str]:
    errors: list[str] = []
    required = {"screen_class", "visible_text", "ui_objects", "appeared", "disappeared", "changed"}
    if not isinstance(observation, dict):
        return ["model observation must be object"]
    if set(observation) != required:
        errors.append("model observation keys invalid")
    if observation.get("screen_class") not in SCREEN_CLASSES:
        errors.append("model observation screen_class invalid")
    if not _is_str_list(observation.get("visible_text")):
        errors.append("model observation visible_text invalid")
    for key in ("ui_objects", "appeared", "disappeared", "changed"):
        if not _is_object_list(observation.get(key)):
            errors.append(f"model observation {key} invalid")
    return errors


def normalize_ocr_transcription(
    raw_text: str,
    *,
    evidence_ref: str,
    capture_sha256: str,
    model_profile_id: str,
    source_monotonic_ns: int | None = None,
) -> dict[str, Any]:
    if not isinstance(raw_text, str):
        raise ValueError("raw_text must be string")
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
    visible_text = [line.strip() for line in raw_text.splitlines() if line.strip()]
    result = {
        "schema_version": 1,
        "capture": {
            "evidence_ref": evidence_ref,
            "sha256": capture_sha256.lower(),
            "source_monotonic_ns": source_monotonic_ns,
        },
        "model": {"model_profile_id": model_profile_id},
        "observation": {
            "screen_class": "UNKNOWN",
            "visible_text": visible_text,
            "ui_objects": [],
            "appeared": [],
            "disappeared": [],
            "changed": [],
        },
        "quality": {
            "schema_valid": True,
            "visual_only": True,
            "structural_authority": False,
            "unknown_fields": ["observation.screen_class"],
        },
    }
    errors = validate_visual_evidence(result)
    if errors:
        raise ValueError("normalized OCR VisualEvidence invalid: " + "; ".join(errors))
    return result

def evaluate_hard_gates(trials: Iterable[dict[str, Any]]) -> dict[str, Any]:
    trials = list(trials)
    if not trials:
        return {
            "schema_valid_100_percent": False,
            "zero_secret_leakage": False,
            "zero_false_in_game_on_login_or_character_select": False,
            "zero_runtime_action_authority": False,
            "zero_model_authored_executable_action_parameters": False,
            "single_model_residency_preserved": False,
            "zero_silent_cloud_fallback": False,
            "required_provenance_complete": False,
            "eligible": False,
            "failure_reasons": ["no_trials"],
        }
    gates = {
        "schema_valid_100_percent": all(not validate_visual_evidence(t.get("visual_evidence")) for t in trials),
        "zero_secret_leakage": all(t.get("secret_leakage") is False for t in trials),
        "zero_false_in_game_on_login_or_character_select": all(
            not (
                t.get("ground_truth_screen_class") in {"LOGIN_SCREEN", "CHARACTER_SELECT"}
                and isinstance(t.get("visual_evidence"), dict)
                and t["visual_evidence"].get("observation", {}).get("screen_class") == "IN_GAME_VISUAL"
            )
            for t in trials
        ),
        "zero_runtime_action_authority": all(t.get("runtime_action_authority") is False for t in trials),
        "zero_model_authored_executable_action_parameters": all(
            t.get("model_authored_executable_action_parameters") is False for t in trials
        ),
        "single_model_residency_preserved": all(t.get("single_model_residency_violation") is False for t in trials),
        "zero_silent_cloud_fallback": all(t.get("silent_cloud_fallback") is False for t in trials),
        "required_provenance_complete": all(t.get("provenance_complete") is True for t in trials),
    }
    failed = [name for name, passed in gates.items() if not passed]
    gates["eligible"] = not failed
    gates["failure_reasons"] = failed
    return gates


def score_profile(metrics: dict[str, float]) -> float:
    missing = set(WEIGHTS) - set(metrics)
    extra = set(metrics) - set(WEIGHTS)
    if missing or extra:
        raise ValueError(f"metrics keys mismatch: missing={sorted(missing)} extra={sorted(extra)}")
    total = 0.0
    for name, weight in WEIGHTS.items():
        value = metrics[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"metric {name} out of range")
        total += float(value) * weight
    return round(total * 100.0, 6)


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


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class UnsafeInputError(ValueError):
    pass


def ensure_secret_safe(metadata: Any) -> bool:
    if not isinstance(metadata, dict) or metadata.get("secret_safe") is not True:
        reason = metadata.get("reason") if isinstance(metadata, dict) else "metadata_invalid"
        raise UnsafeInputError(f"SECRET_INPUT_REJECTED:{reason}")
    return True


def validate_input_manifest(metadata: Any, image_path: str | Path) -> str:
    ensure_secret_safe(metadata)
    digest = metadata.get("sha256") if isinstance(metadata, dict) else None
    if not isinstance(digest, str) or len(digest) != 64 or any(
        c not in "0123456789abcdefABCDEF" for c in digest
    ):
        raise ValueError("manifest sha256 invalid")
    actual = sha256_file(image_path)
    if actual.lower() != digest.lower():
        raise ValueError("manifest sha256 does not match image bytes")
    return actual


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
