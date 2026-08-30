"""Bounded local Qwen vision observations with no semantic authority."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from tools.tibia_re_vision.evidence import (
    ensure_secret_safe,
    validate_input_manifest,
    validate_model_observation,
    validate_visual_evidence,
)
from tools.tibia_re_vision.ollama import admit_residency

from .agent_protocol import AgentVisualState


QWEN_VISION_MODEL = "qwen3-vl:4b-instruct-q4_K_M"
QWEN_VISION_DIGEST = "ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b"
QWEN_VISION_PROFILE_ID = f"ollama:{QWEN_VISION_MODEL}@sha256:{QWEN_VISION_DIGEST}"
QWEN_NUM_CTX = 4096
QWEN_NUM_PREDICT = 256
QWEN_TEMPERATURE = 0


class ModelSlotUnavailable(RuntimeError):
    """The sole local-model slot cannot safely be used by this scheduler."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class SecretSafeCapture:
    run_id: str
    evidence_ref: str
    path: Path
    sha256: str
    secret_safe: bool
    source_monotonic_ns: int | None


@dataclass(frozen=True)
class VisionObservation:
    screen_class: str
    visible_text: tuple[str, ...]
    confidence: float | None
    model_profile_id: str
    evidence_ref: str
    capture_sha256: str
    visual_only: bool = True
    structural_authority: bool = False


_Ps = Callable[[], list[str] | None]
_Digest = Callable[[str], str]
_Infer = Callable[..., Any]
_Unload = Callable[[str], Any]
_VISUAL_MAP = {
    "LOGIN_SCREEN": AgentVisualState.LOGIN_SCREEN.value,
    "CHARACTER_SELECT": AgentVisualState.CHARACTER_SELECT.value,
    "IN_GAME_VISUAL": AgentVisualState.WORLD_VISUAL.value,
    "WORLD_EXIT": AgentVisualState.WORLD_EXIT_VISUAL.value,
    "OTHER": AgentVisualState.UNKNOWN.value,
    "UNKNOWN": AgentVisualState.UNKNOWN.value,
}
_VISION_PROMPT = (
    "Return only the strict visual observation JSON schema. "
    "Describe pixels only; do not infer runtime state, authority, or actions."
)


class ModelSlotScheduler:
    """Serializes a single model slot and never evicts a model it does not own."""

    def __init__(self, *, ps: _Ps, digest: _Digest, infer: _Infer, unload: _Unload) -> None:
        self._ps = ps
        self._digest = digest
        self._infer = infer
        self._unload = unload
        self._owned_model: str | None = None

    def owns(self, model: str) -> bool:
        return self._owned_model == model

    def _residency(self) -> list[str] | None:
        try:
            resident = self._ps()
        except Exception:
            return None
        if resident is None or not isinstance(resident, list) or not all(isinstance(item, str) and item for item in resident):
            return None
        return resident

    def _verify_digest(self, model: str, expected_digest: str) -> None:
        try:
            actual = self._digest(model)
        except Exception as exc:
            raise ModelSlotUnavailable("MODEL_DIGEST_UNAVAILABLE") from exc
        if not isinstance(actual, str) or actual.lower() != expected_digest.lower():
            raise ModelSlotUnavailable("MODEL_DIGEST_MISMATCH")

    def _unload_owned_and_verify_empty(self, model: str) -> None:
        try:
            self._unload(model)
        except Exception as exc:
            raise ModelSlotUnavailable("MODEL_UNLOAD_FAILED") from exc
        if self._residency() != []:
            raise ModelSlotUnavailable("MODEL_UNLOAD_NOT_VERIFIED")
        self._owned_model = None

    def _admit(self, model: str, expected_digest: str) -> None:
        resident = self._residency()
        if resident is None:
            raise ModelSlotUnavailable("RESIDENCY_UNKNOWN")
        if resident == []:
            self._owned_model = None
            self._verify_digest(model, expected_digest)
            self._owned_model = model
            return

        if len(resident) > 1:
            _, code = admit_residency(resident, model)
            raise ModelSlotUnavailable(code)

        active = resident[0]
        if active == model:
            if self._owned_model != model:
                raise ModelSlotUnavailable("TARGET_NOT_OWNED")
            self._verify_digest(model, expected_digest)
            return

        if active != self._owned_model:
            _, code = admit_residency(resident, model)
            raise ModelSlotUnavailable(code)

        # A switch is possible only from the exact scheduler-owned resident model.
        self._verify_digest(model, expected_digest)
        self._unload_owned_and_verify_empty(active)
        self._owned_model = model

    def infer(self, *, model: str, expected_digest: str, **kwargs: Any) -> Any:
        """Admit ``model`` and call the injected provider once.

        The injected provider is the only load/inference path.  It receives the
        admitted model and can load it as part of its bounded request.
        """
        self._admit(model, expected_digest)
        return self._infer(model=model, **kwargs)

    def release(self) -> None:
        """Unload only the exact model this scheduler previously acquired."""
        owned = self._owned_model
        if owned is None:
            return
        resident = self._residency()
        if resident is None:
            raise ModelSlotUnavailable("RESIDENCY_UNKNOWN")
        if resident == []:
            self._owned_model = None
            return
        if resident != [owned]:
            raise ModelSlotUnavailable("MODEL_SLOT_NOT_OWNED")
        self._unload_owned_and_verify_empty(owned)


class AgentVisionSensor:
    """Validates a secret-safe capture before making one local visual request."""

    def __init__(self, scheduler: ModelSlotScheduler, *, prompt: str = _VISION_PROMPT) -> None:
        self._scheduler = scheduler
        self._prompt = prompt
        self._seen_capture_sha256: set[str] = set()

    @staticmethod
    def _capture_bytes(capture: SecretSafeCapture) -> tuple[bytes, str]:
        if not isinstance(capture, SecretSafeCapture):
            raise ValueError("capture invalid")
        ensure_secret_safe({"secret_safe": capture.secret_safe})
        if not isinstance(capture.run_id, str) or not capture.run_id:
            raise ValueError("capture.run_id invalid")
        if not isinstance(capture.evidence_ref, str) or not capture.evidence_ref:
            raise ValueError("capture.evidence_ref invalid")
        if not isinstance(capture.path, Path):
            raise ValueError("capture.path invalid")
        if capture.source_monotonic_ns is not None and (
            not isinstance(capture.source_monotonic_ns, int) or isinstance(capture.source_monotonic_ns, bool)
        ):
            raise ValueError("capture.source_monotonic_ns invalid")
        if not isinstance(capture.sha256, str) or len(capture.sha256) != 64:
            raise ValueError("capture.sha256 invalid")
        try:
            bytes_ = capture.path.read_bytes()
        except OSError as exc:
            raise ValueError("capture bytes unavailable") from exc
        if not bytes_:
            raise ValueError("capture bytes empty")
        actual = hashlib.sha256(bytes_).hexdigest()
        if actual != capture.sha256.lower():
            raise ValueError("capture sha256 does not match bytes")
        # Reuse the manifest validation at the input boundary as a second
        # independent file/hash binding check before provider invocation.
        validate_input_manifest(
            {"secret_safe": capture.secret_safe, "sha256": capture.sha256}, capture.path
        )
        return bytes_, actual

    @staticmethod
    def _strict_evidence(response: Any, capture: SecretSafeCapture) -> Mapping[str, Any]:
        candidate = response.get("visual_evidence") if isinstance(response, Mapping) and "visual_evidence" in response else response
        if not isinstance(candidate, Mapping):
            raise ValueError("provider response is not VisualEvidence")
        payload = dict(candidate)
        errors = validate_visual_evidence(payload)
        required_shapes = {
            "payload": (payload, {"schema_version", "capture", "model", "observation", "quality"}),
            "capture": (payload.get("capture"), {"evidence_ref", "sha256", "source_monotonic_ns"}),
            "model": (payload.get("model"), {"model_profile_id"}),
            "quality": (payload.get("quality"), {"schema_valid", "visual_only", "structural_authority", "unknown_fields"}),
        }
        for name, (value, keys) in required_shapes.items():
            if not isinstance(value, Mapping) or set(value) != keys:
                errors.append(f"{name} keys invalid")
        observation = payload.get("observation")
        if isinstance(observation, Mapping):
            errors.extend(validate_model_observation(dict(observation)))
        if errors:
            raise ValueError("VisualEvidence invalid: " + "; ".join(errors))
        capture_data = payload["capture"]
        model_data = payload["model"]
        quality = payload["quality"]
        if (
            capture_data.get("evidence_ref") != capture.evidence_ref
            or capture_data.get("sha256", "").lower() != capture.sha256.lower()
            or capture_data.get("source_monotonic_ns") != capture.source_monotonic_ns
            or model_data.get("model_profile_id") != QWEN_VISION_PROFILE_ID
            or quality.get("visual_only") is not True
            or quality.get("structural_authority") is not False
        ):
            raise ValueError("VisualEvidence provenance or authority invalid")
        return payload

    def observe(self, capture: SecretSafeCapture) -> VisionObservation:
        _, actual_sha256 = self._capture_bytes(capture)
        if actual_sha256 in self._seen_capture_sha256:
            raise ValueError("DUPLICATE_CAPTURE_SHA256")
        self._seen_capture_sha256.add(actual_sha256)
        response = self._scheduler.infer(
            model=QWEN_VISION_MODEL,
            expected_digest=QWEN_VISION_DIGEST,
            image_path=capture.path,
            prompt=self._prompt,
            evidence_ref=capture.evidence_ref,
            capture_sha256=actual_sha256,
            source_monotonic_ns=capture.source_monotonic_ns,
            model_profile_id=QWEN_VISION_PROFILE_ID,
            keep_alive="0s",
            num_ctx=QWEN_NUM_CTX,
            num_predict=QWEN_NUM_PREDICT,
            temperature=QWEN_TEMPERATURE,
        )
        evidence = self._strict_evidence(response, capture)
        observation = evidence["observation"]
        screen_class = _VISUAL_MAP[observation["screen_class"]]
        return VisionObservation(
            screen_class=screen_class,
            visible_text=tuple(observation["visible_text"]),
            confidence=None,
            model_profile_id=QWEN_VISION_PROFILE_ID,
            evidence_ref=capture.evidence_ref,
            capture_sha256=actual_sha256,
        )
