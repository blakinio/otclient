"""Bounded local Qwen vision observations with no semantic authority."""

from __future__ import annotations

import hashlib
import os
import stat
import tempfile
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Protocol

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
_UNSET = object()
_MODEL_SLOT_ERROR_CODES = frozenset({
    "DIFFERENT_RESIDENT_MODEL",
    "MODEL_DIGEST_MISMATCH",
    "MODEL_DIGEST_UNAVAILABLE",
    "MODEL_INFERENCE_FAILED",
    "MODEL_SLOT_NOT_OWNED",
    "MODEL_SLOT_REENTRANT",
    "MODEL_UNLOAD_FAILED",
    "MODEL_UNLOAD_NOT_VERIFIED",
    "MULTIPLE_RESIDENT_MODELS",
    "RESIDENCY_UNKNOWN",
    "TARGET_NOT_OWNED",
})


class ModelSlotUnavailable(RuntimeError):
    """The sole local-model slot cannot safely be used by this scheduler."""

    def __init__(self, code: str) -> None:
        if code not in _MODEL_SLOT_ERROR_CODES:
            raise ValueError("model slot error code invalid")
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
_Unload = Callable[[str], Any]


class _Infer(Protocol):
    """Exact endpoint-bound ``run_ollama_trial`` provider shape."""

    def __call__(
        self,
        model: str,
        image_path: str | Path,
        prompt: str,
        *,
        evidence_ref: str,
        capture_sha256: str,
        model_profile_id: str,
        source_monotonic_ns: int | None,
        keep_alive: str,
        num_ctx: int,
        num_predict: int,
    ) -> Any: ...


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
    """Serialize the complete lifecycle of the one repository-owned model slot."""

    def __init__(self, *, ps: _Ps, digest: _Digest, infer: _Infer, unload: _Unload) -> None:
        self._ps = ps
        self._digest = digest
        self._infer = infer
        self._unload = unload
        self._owned_model: str | None = None
        self._lock = threading.RLock()
        self._transition_thread: int | None = None

    def owns(self, model: str) -> bool:
        with self._lock:
            return self._owned_model == model

    def _residency(self) -> list[str] | None:
        try:
            resident = self._ps()
        except Exception:
            return None
        if (
            resident is None
            or not isinstance(resident, list)
            or not all(isinstance(item, str) and item for item in resident)
        ):
            return None
        return resident

    def _verify_digest(self, model: str, expected_digest: str) -> None:
        actual: object = _UNSET
        try:
            actual = self._digest(model)
        except Exception:
            pass
        if actual is _UNSET:
            raise ModelSlotUnavailable("MODEL_DIGEST_UNAVAILABLE")
        if not isinstance(actual, str) or actual.lower() != expected_digest.lower():
            raise ModelSlotUnavailable("MODEL_DIGEST_MISMATCH")

    @staticmethod
    def _residency_failure(resident: list[str] | None, model: str) -> ModelSlotUnavailable:
        if resident is None:
            return ModelSlotUnavailable("RESIDENCY_UNKNOWN")
        _, code = admit_residency(resident, model)
        return ModelSlotUnavailable(code)

    def _unload_owned_and_verify_empty(self, model: str) -> None:
        unload_failed = False
        try:
            self._unload(model)
        except Exception:
            unload_failed = True

        # Classify the one post-effect observation identically whether the
        # provider returned or raised.  Only exact continuity proves that the
        # old ownership claim remains valid; every other state loses the claim
        # so a later same-name foreign resident can never be unloaded.
        resident = self._residency()
        if resident != [model]:
            self._owned_model = None
        if unload_failed:
            raise ModelSlotUnavailable("MODEL_UNLOAD_FAILED")
        if resident != []:
            raise ModelSlotUnavailable("MODEL_UNLOAD_NOT_VERIFIED")

    def _admit(self, model: str, expected_digest: str) -> None:
        resident = self._residency()
        if resident is None:
            raise ModelSlotUnavailable("RESIDENCY_UNKNOWN")
        if resident == []:
            self._owned_model = None
            self._verify_digest(model, expected_digest)
            return
        if len(resident) > 1:
            raise self._residency_failure(resident, model)

        active = resident[0]
        if active == model:
            if self._owned_model != model:
                raise ModelSlotUnavailable("TARGET_NOT_OWNED")
            self._verify_digest(model, expected_digest)
            return
        if active != self._owned_model:
            raise self._residency_failure(resident, model)

        # Verify the next exact identity before disturbing the currently owned
        # resident.  The target remains unowned until post-provider residency.
        self._verify_digest(model, expected_digest)
        self._unload_owned_and_verify_empty(active)

    def _reconcile_provider_residency(self, model: str) -> None:
        resident = self._residency()
        if resident == []:
            self._owned_model = None
            return
        if resident == [model]:
            # This exact target appeared during the serialized acquisition.
            self._owned_model = model
            return
        self._owned_model = None
        raise self._residency_failure(resident, model)

    def infer(
        self,
        *,
        model: str,
        expected_digest: str,
        image_path: str | Path,
        evidence_ref: str,
        capture_sha256: str,
        model_profile_id: str,
        source_monotonic_ns: int | None,
        keep_alive: str,
        num_ctx: int,
        num_predict: int,
    ) -> Any:
        """Run one exact provider call while holding the sole logical slot."""
        with self._lock:
            thread_id = threading.get_ident()
            if self._transition_thread == thread_id:
                raise ModelSlotUnavailable("MODEL_SLOT_REENTRANT")
            self._transition_thread = thread_id
            try:
                self._admit(model, expected_digest)
                response: object = _UNSET
                provider_failed = False
                try:
                    response = self._infer(
                        model,
                        image_path,
                        _VISION_PROMPT,
                        evidence_ref=evidence_ref,
                        capture_sha256=capture_sha256,
                        model_profile_id=model_profile_id,
                        source_monotonic_ns=source_monotonic_ns,
                        keep_alive=keep_alive,
                        num_ctx=num_ctx,
                        num_predict=num_predict,
                    )
                except Exception:
                    provider_failed = True

                # Reconcile outside the provider handler so untrusted provider
                # exception objects cannot become an implicit context.  A
                # residency safety failure remains primary over inference.
                residency_failure: str | None = None
                try:
                    self._reconcile_provider_residency(model)
                except ModelSlotUnavailable as error:
                    residency_failure = error.code
                if residency_failure is not None:
                    raise ModelSlotUnavailable(residency_failure)
                if provider_failed:
                    raise ModelSlotUnavailable("MODEL_INFERENCE_FAILED")
                if response is _UNSET:
                    raise AssertionError("provider response state invalid")
                return response
            finally:
                self._transition_thread = None

    def release(self) -> None:
        """Unload only an exact target acquired by this scheduler."""
        with self._lock:
            thread_id = threading.get_ident()
            if self._transition_thread == thread_id:
                raise ModelSlotUnavailable("MODEL_SLOT_REENTRANT")
            self._transition_thread = thread_id
            try:
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
            finally:
                self._transition_thread = None


class AgentVisionSensor:
    """Validate one capture snapshot and return only strict visual evidence."""

    def __init__(self, scheduler: ModelSlotScheduler) -> None:
        self._scheduler = scheduler
        self._identity_lock = threading.Lock()
        self._pending_capture_sha256: set[tuple[str, str]] = set()
        self._pending_evidence_refs: dict[tuple[str, str], str] = {}
        self._completed_capture_sha256: set[tuple[str, str]] = set()
        self._evidence_refs: dict[tuple[str, str], str] = {}

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
            not isinstance(capture.source_monotonic_ns, int)
            or isinstance(capture.source_monotonic_ns, bool)
        ):
            raise ValueError("capture.source_monotonic_ns invalid")
        if not isinstance(capture.sha256, str) or len(capture.sha256) != 64:
            raise ValueError("capture.sha256 invalid")
        capture_bytes: object = _UNSET
        try:
            capture_bytes = capture.path.read_bytes()
        except OSError:
            pass
        if capture_bytes is _UNSET:
            raise ValueError("capture bytes unavailable")
        if not isinstance(capture_bytes, bytes):
            raise AssertionError("capture reader returned non-bytes")
        bytes_ = capture_bytes
        if not bytes_:
            raise ValueError("capture bytes empty")
        actual = hashlib.sha256(bytes_).hexdigest()
        if actual != capture.sha256.lower():
            raise ValueError("capture sha256 does not match bytes")
        manifest_unavailable = False
        try:
            validate_input_manifest(
                {"secret_safe": capture.secret_safe, "sha256": capture.sha256},
                capture.path,
            )
        except OSError:
            manifest_unavailable = True
        if manifest_unavailable:
            raise ValueError("capture bytes unavailable")
        return bytes_, actual

    @staticmethod
    def _snapshot_metadata_is_safe(mode: int, *, windows: bool) -> bool:
        if not stat.S_ISREG(mode):
            return False
        permissions = stat.S_IMODE(mode)
        write_bits = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
        if permissions & write_bits:
            return False
        if windows:
            # CPython exposes the Windows read-only attribute through the
            # owner-read/write mode aliases and commonly reports 0444.  This
            # bounded phase relies additionally on the unshared temporary
            # parent; POSIX-looking bits are not treated as a Windows ACL proof.
            return bool(permissions & stat.S_IREAD)
        return bool(permissions & stat.S_IRUSR)

    @classmethod
    def _verify_snapshot(cls, path: Path, expected_sha256: str) -> None:
        metadata: object = _UNSET
        try:
            metadata = path.lstat()
        except OSError:
            pass
        if metadata is _UNSET:
            raise ValueError("capture snapshot integrity invalid")
        if not isinstance(metadata, os.stat_result):
            raise AssertionError("snapshot metadata state invalid")
        if not cls._snapshot_metadata_is_safe(
            metadata.st_mode,
            windows=os.name == "nt",
        ):
            raise ValueError("capture snapshot integrity invalid")
        snapshot_bytes: object = _UNSET
        try:
            snapshot_bytes = path.read_bytes()
        except OSError:
            pass
        if snapshot_bytes is _UNSET:
            raise ValueError("capture snapshot integrity invalid")
        if not isinstance(snapshot_bytes, bytes):
            raise AssertionError("snapshot reader returned non-bytes")
        bytes_ = snapshot_bytes
        if hashlib.sha256(bytes_).hexdigest() != expected_sha256:
            raise ValueError("capture snapshot integrity invalid")

    @classmethod
    @contextmanager
    def _snapshot(
        cls, bytes_: bytes, expected_sha256: str
    ) -> Iterator[Path]:
        with tempfile.TemporaryDirectory(prefix="tibia-re-vision-") as raw:
            path = Path(raw) / "capture.snapshot"
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(path, flags, 0o600)
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    descriptor = -1
                    handle.write(bytes_)
                    handle.flush()
                    os.fsync(handle.fileno())
            finally:
                if descriptor >= 0:
                    os.close(descriptor)
            path.chmod(stat.S_IRUSR)
            cls._verify_snapshot(path, expected_sha256)
            try:
                yield path
            finally:
                cls._verify_snapshot(path, expected_sha256)

    def _reserve_identity(self, capture: SecretSafeCapture, sha256: str) -> None:
        capture_key = (capture.run_id, sha256)
        evidence_key = (capture.run_id, capture.evidence_ref)
        with self._identity_lock:
            committed_sha = self._evidence_refs.get(evidence_key)
            if committed_sha is not None and committed_sha != sha256:
                raise ValueError("EVIDENCE_REF_SHA256_REBIND")
            pending_sha = self._pending_evidence_refs.get(evidence_key)
            if pending_sha is not None and pending_sha != sha256:
                raise ValueError("EVIDENCE_REF_SHA256_REBIND")
            if (
                capture_key in self._completed_capture_sha256
                or capture_key in self._pending_capture_sha256
            ):
                raise ValueError("DUPLICATE_CAPTURE_SHA256")
            self._pending_capture_sha256.add(capture_key)
            self._pending_evidence_refs[evidence_key] = sha256

    def _rollback_identity(self, capture: SecretSafeCapture, sha256: str) -> None:
        capture_key = (capture.run_id, sha256)
        evidence_key = (capture.run_id, capture.evidence_ref)
        with self._identity_lock:
            self._pending_capture_sha256.discard(capture_key)
            if self._pending_evidence_refs.get(evidence_key) == sha256:
                del self._pending_evidence_refs[evidence_key]

    def _commit_identity(self, capture: SecretSafeCapture, sha256: str) -> None:
        capture_key = (capture.run_id, sha256)
        evidence_key = (capture.run_id, capture.evidence_ref)
        with self._identity_lock:
            if (
                capture_key not in self._pending_capture_sha256
                or self._pending_evidence_refs.get(evidence_key) != sha256
            ):
                raise RuntimeError("capture identity reservation lost")
            self._pending_capture_sha256.remove(capture_key)
            del self._pending_evidence_refs[evidence_key]
            self._completed_capture_sha256.add(capture_key)
            self._evidence_refs[evidence_key] = sha256

    @staticmethod
    def _strict_evidence(response: Any, capture: SecretSafeCapture) -> Mapping[str, Any]:
        candidate = (
            response.get("visual_evidence")
            if isinstance(response, Mapping) and "visual_evidence" in response
            else response
        )
        if not isinstance(candidate, Mapping):
            raise ValueError("provider response is not VisualEvidence")
        payload = dict(candidate)
        errors = validate_visual_evidence(payload)
        required_shapes = {
            "payload": (
                payload,
                {"schema_version", "capture", "model", "observation", "quality"},
            ),
            "capture": (
                payload.get("capture"),
                {"evidence_ref", "sha256", "source_monotonic_ns"},
            ),
            "model": (payload.get("model"), {"model_profile_id"}),
            "quality": (
                payload.get("quality"),
                {"schema_valid", "visual_only", "structural_authority", "unknown_fields"},
            ),
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
        bytes_, actual_sha256 = self._capture_bytes(capture)
        self._reserve_identity(capture, actual_sha256)
        observation_complete = False
        try:
            with self._snapshot(bytes_, actual_sha256) as snapshot_path:
                response = self._scheduler.infer(
                    model=QWEN_VISION_MODEL,
                    expected_digest=QWEN_VISION_DIGEST,
                    image_path=snapshot_path,
                    evidence_ref=capture.evidence_ref,
                    capture_sha256=actual_sha256,
                    source_monotonic_ns=capture.source_monotonic_ns,
                    model_profile_id=QWEN_VISION_PROFILE_ID,
                    keep_alive="0s",
                    num_ctx=QWEN_NUM_CTX,
                    num_predict=QWEN_NUM_PREDICT,
                )
                evidence = self._strict_evidence(response, capture)
                observation = evidence["observation"]
                result = VisionObservation(
                    screen_class=_VISUAL_MAP[observation["screen_class"]],
                    visible_text=tuple(observation["visible_text"]),
                    confidence=None,
                    model_profile_id=QWEN_VISION_PROFILE_ID,
                    evidence_ref=capture.evidence_ref,
                    capture_sha256=actual_sha256,
                )
            observation_complete = True
        finally:
            if not observation_complete:
                self._rollback_identity(capture, actual_sha256)
        self._commit_identity(capture, actual_sha256)
        return result
