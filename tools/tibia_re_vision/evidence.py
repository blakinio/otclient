from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


SCREEN_CLASSES = {
    "LOGIN_SCREEN",
    "CHARACTER_SELECT",
    "IN_GAME_VISUAL",
    "WORLD_EXIT",
    "OTHER",
    "UNKNOWN",
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
