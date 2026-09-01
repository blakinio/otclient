from __future__ import annotations

import binascii
import hashlib
import json
import re
import struct
import threading
import zlib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.tibia_re_vision.capture_edge import (
    CaptureEdgeError,
    FrameSource,
    PixelRegion,
    RuntimeBinding,
    WindowGeometry,
    _crop_rgb,
    _encode_rgb_png,
    _mask_rgb,
    _require_region,
    _require_rgb,
    _snapshot_binding,
)

from .agent_edge_bridge import AgentEdgeBridge, ReviewedRuntimeAuthorityConfiguration
from .agent_edge_transport import EdgeReplayLedger, EdgeTransportVerifier, VerifiedEdgeFrame
from .agent_protocol import AgentProvenance
from .agent_vision import SecretSafeCapture
from .canonical import jcs_dumps
from .control_domain import ControlDomainService
from .model import ValidationError, validate_opaque_id

_SHA256 = re.compile(r"[0-9a-f]{64}")
_POLICY_ID = re.compile(r"[A-Za-z0-9_.:-]{1,80}")
_REPLAY_META_PREFIX = "vision-p2-edge-replay:"
_CAPTURE_ROOT_NAME = "vision-p2-captures"


@dataclass(frozen=True, slots=True)
class ReviewedCapturePolicy:
    """Reviewed mask data. Trust comes from application composition, never object provenance."""

    policy_id: str
    expected_width: int
    expected_height: int
    secret_regions: tuple[PixelRegion, ...]

    def __post_init__(self) -> None:
        if type(self.policy_id) is not str or _POLICY_ID.fullmatch(self.policy_id) is None:
            raise ValueError("reviewed capture policy id invalid")
        if (
            type(self.expected_width) is not int
            or type(self.expected_height) is not int
            or self.expected_width <= 0
            or self.expected_height <= 0
        ):
            raise ValueError("reviewed capture geometry invalid")
        if (
            type(self.secret_regions) is not tuple
            or not self.secret_regions
            or any(type(region) is not PixelRegion for region in self.secret_regions)
        ):
            raise ValueError("reviewed capture secret regions invalid")
        geometry = WindowGeometry(0, 0, self.expected_width, self.expected_height)
        for region in self.secret_regions:
            _require_region(region, geometry)

    @property
    def policy_ref(self) -> str:
        regions = sorted(
            (region.x, region.y, region.width, region.height)
            for region in self.secret_regions
        )
        canonical = "|".join(
            [
                "vision-p2-reviewed-mask-v1",
                self.policy_id,
                str(self.expected_width),
                str(self.expected_height),
                *(f"{x},{y},{width},{height}" for x, y, width, height in regions),
            ]
        ).encode("ascii")
        return f"secret-mask:{hashlib.sha256(canonical).hexdigest()}"


@dataclass(frozen=True, slots=True)
class TrustedCaptureArtifact:
    path: Path
    sha256: str
    region: PixelRegion | None = None
    parent_full_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class TrustedCaptureEvidence:
    """Authority-neutral capture metadata. It intentionally has no secret_safe field."""

    run_id: str
    runtime_binding: RuntimeBinding
    geometry: WindowGeometry
    source_monotonic_ns: int
    acquisition_completed_ns: int
    full_frame: TrustedCaptureArtifact
    secret_policy_ref: str
    is_blank: bool
    is_black: bool
    changed_from_previous: bool | None
    crop: TrustedCaptureArtifact | None = None


@dataclass(frozen=True, slots=True)
class VisionP2TrustedComposition:
    """Process-composition configuration. Task/API/MCP/transport payloads never select it."""

    runtime_authority_configuration: ReviewedRuntimeAuthorityConfiguration | None = None
    capture_policy: ReviewedCapturePolicy | None = None

    def __post_init__(self) -> None:
        if (
            self.runtime_authority_configuration is not None
            and type(self.runtime_authority_configuration) is not ReviewedRuntimeAuthorityConfiguration
        ):
            raise TypeError("runtime authority configuration invalid")
        if self.capture_policy is not None and type(self.capture_policy) is not ReviewedCapturePolicy:
            raise TypeError("reviewed capture policy invalid")

    def attach(self, service: ControlDomainService) -> TrustedVisionP2Runtime:
        return TrustedVisionP2Runtime(service, self)


def _clock_sample(clock: Callable[[], int]) -> int:
    value = clock()
    if type(value) is not int or value <= 0:
        raise CaptureEdgeError("CAPTURE_CLOCK_INVALID")
    return value


def _require_current(binding: RuntimeBinding, now_ns: int, max_age_ns: int) -> None:
    if type(now_ns) is not int or now_ns <= 0 or type(max_age_ns) is not int or max_age_ns < 0:
        raise CaptureEdgeError("CAPTURE_CLOCK_INVALID")
    age = now_ns - binding.observed_monotonic_ns
    if age < 0 or age > max_age_ns:
        raise CaptureEdgeError("RUNTIME_BINDING_STALE")


def _prepare_capture_root(parent: Path) -> Path:
    parent = Path(parent)
    try:
        parent_resolved = parent.resolve(strict=True)
    except OSError:
        raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID") from None
    if parent.is_symlink() or not parent_resolved.is_dir():
        raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID")
    root = parent_resolved / _CAPTURE_ROOT_NAME
    if root.exists():
        if root.is_symlink() or not root.is_dir():
            raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID")
    else:
        try:
            root.mkdir(mode=0o700)
        except OSError:
            raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID") from None
    try:
        resolved = root.resolve(strict=True)
    except OSError:
        raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID") from None
    if root.is_symlink() or resolved.parent != parent_resolved or resolved.name != _CAPTURE_ROOT_NAME:
        raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID")
    return resolved


def _persist_png(
    root: Path,
    payload: bytes,
    *,
    region: PixelRegion | None = None,
    parent_sha: str | None = None,
) -> TrustedCaptureArtifact:
    if root.is_symlink() or not root.is_dir():
        raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID")
    digest = hashlib.sha256(payload).hexdigest()
    path = root / f"{digest}.png"
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise CaptureEdgeError("CAPTURE_EVIDENCE_ROOT_INVALID")
        try:
            existing = path.read_bytes()
        except OSError:
            raise CaptureEdgeError("CAPTURE_PERSIST_FAILED") from None
        if existing != payload:
            raise CaptureEdgeError("CONTENT_ADDRESS_COLLISION")
    else:
        try:
            path.write_bytes(payload)
        except OSError:
            raise CaptureEdgeError("CAPTURE_PERSIST_FAILED") from None
    return TrustedCaptureArtifact(
        path=path,
        sha256=digest,
        region=region,
        parent_full_sha256=parent_sha,
    )


def _decode_rgb_png(payload: bytes) -> tuple[int, int, bytes]:
    if type(payload) is not bytes or not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    offset = 8
    width = height = None
    compressed = bytearray()
    saw_iend = False
    while offset < len(payload):
        if offset + 12 > len(payload):
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        size = struct.unpack(">I", payload[offset : offset + 4])[0]
        kind = payload[offset + 4 : offset + 8]
        body_end = offset + 8 + size
        crc_end = body_end + 4
        if crc_end > len(payload):
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        body = payload[offset + 8 : body_end]
        crc = struct.unpack(">I", payload[body_end:crc_end])[0]
        if crc != (binascii.crc32(kind + body) & 0xFFFFFFFF):
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        if kind == b"IHDR":
            if width is not None or len(body) != 13:
                raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
                ">IIBBBBB", body
            )
            if (
                not width
                or not height
                or (bit_depth, color_type, compression, filter_method, interlace) != (8, 2, 0, 0, 0)
            ):
                raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        elif kind == b"IDAT":
            compressed.extend(body)
        elif kind == b"IEND":
            if body:
                raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
            saw_iend = True
            offset = crc_end
            break
        offset = crc_end
    if width is None or height is None or not saw_iend or offset != len(payload):
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    try:
        raw = zlib.decompress(bytes(compressed))
    except zlib.error:
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID") from None
    stride = width * 3
    if len(raw) != height * (stride + 1):
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    pixels = bytearray()
    for row in range(height):
        start = row * (stride + 1)
        if raw[start] != 0:
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        pixels.extend(raw[start + 1 : start + 1 + stride])
    return width, height, bytes(pixels)


class TrustedCaptureEdge:
    __slots__ = ("_binding_reader", "_frame_source", "_monotonic_ns", "_policy", "_root")

    def __init__(
        self,
        *,
        binding_reader: Callable[[], RuntimeBinding],
        frame_source: FrameSource,
        monotonic_ns: Callable[[], int],
        policy: ReviewedCapturePolicy,
        root: Path,
    ) -> None:
        if type(policy) is not ReviewedCapturePolicy:
            raise CaptureEdgeError("CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED")
        self._binding_reader = binding_reader
        self._frame_source = frame_source
        self._monotonic_ns = monotonic_ns
        self._policy = policy
        self._root = root

    def capture(
        self,
        *,
        run_id: str,
        max_binding_age_ns: int,
        crop: PixelRegion | None = None,
        previous_full_sha256: str | None = None,
    ) -> TrustedCaptureEvidence:
        if type(run_id) is not str or not run_id:
            raise ValueError("run_id invalid")
        if crop is not None and type(crop) is not PixelRegion:
            raise ValueError("crop invalid")
        if previous_full_sha256 is not None and (
            type(previous_full_sha256) is not str
            or _SHA256.fullmatch(previous_full_sha256.lower()) is None
        ):
            raise ValueError("previous full sha256 invalid")
        before = _snapshot_binding(self._binding_reader())
        checked_ns = _clock_sample(self._monotonic_ns)
        _require_current(before, checked_ns, max_binding_age_ns)
        geometry = self._frame_source.geometry(before)
        if type(geometry) is not WindowGeometry:
            raise CaptureEdgeError("CAPTURE_GEOMETRY_INVALID")
        if (geometry.width, geometry.height) != (
            self._policy.expected_width,
            self._policy.expected_height,
        ):
            raise CaptureEdgeError("CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH")
        for region in self._policy.secret_regions:
            _require_region(region, geometry)
        if crop is not None:
            _require_region(crop, geometry)
        started_ns = _clock_sample(self._monotonic_ns)
        if started_ns < checked_ns:
            raise CaptureEdgeError("CAPTURE_CLOCK_INVALID")
        raw_pixels = self._frame_source.capture_rgb(before, geometry)
        completed_ns = _clock_sample(self._monotonic_ns)
        if completed_ns < started_ns:
            raise CaptureEdgeError("CAPTURE_CLOCK_INVALID")
        _require_rgb(geometry, raw_pixels)
        safe_pixels = _mask_rgb(raw_pixels, geometry, self._policy.secret_regions)
        first_pixel = safe_pixels[:3]
        is_blank = all(
            safe_pixels[offset : offset + 3] == first_pixel
            for offset in range(0, len(safe_pixels), 3)
        )
        is_black = max(safe_pixels, default=0) <= 4
        crop_pixels = None if crop is None else _crop_rgb(safe_pixels, geometry, crop)
        after = _snapshot_binding(self._binding_reader())
        if after != before:
            raise CaptureEdgeError("RUNTIME_BINDING_CHANGED")
        after_geometry = self._frame_source.geometry(after)
        if type(after_geometry) is not WindowGeometry or after_geometry != geometry:
            raise CaptureEdgeError("CAPTURE_GEOMETRY_CHANGED")
        final = _snapshot_binding(self._binding_reader())
        if final != before:
            raise CaptureEdgeError("RUNTIME_BINDING_CHANGED")
        final_ns = _clock_sample(self._monotonic_ns)
        if final_ns < completed_ns:
            raise CaptureEdgeError("CAPTURE_CLOCK_INVALID")
        _require_current(final, final_ns, max_binding_age_ns)
        root = _prepare_capture_root(self._root.parent)
        full = _persist_png(
            root,
            _encode_rgb_png(geometry.width, geometry.height, safe_pixels),
        )
        changed = (
            None
            if previous_full_sha256 is None
            else full.sha256 != previous_full_sha256.lower()
        )
        crop_artifact = None
        if crop is not None and crop_pixels is not None:
            crop_artifact = _persist_png(
                root,
                _encode_rgb_png(crop.width, crop.height, crop_pixels),
                region=crop,
                parent_sha=full.sha256,
            )
        return TrustedCaptureEvidence(
            run_id=run_id,
            runtime_binding=before,
            geometry=geometry,
            source_monotonic_ns=started_ns,
            acquisition_completed_ns=completed_ns,
            full_frame=full,
            secret_policy_ref=self._policy.policy_ref,
            is_blank=is_blank,
            is_black=is_black,
            changed_from_previous=changed,
            crop=crop_artifact,
        )


def _read_capture_artifact(
    root: Path,
    artifact: TrustedCaptureArtifact,
) -> tuple[int, int, bytes]:
    if type(artifact) is not TrustedCaptureArtifact:
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    path = Path(artifact.path)
    try:
        if (
            path.is_symlink()
            or path.parent.resolve(strict=True) != root
            or path.name != f"{artifact.sha256}.png"
        ):
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        payload = path.read_bytes()
    except OSError:
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID") from None
    if hashlib.sha256(payload).hexdigest() != artifact.sha256:
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    return _decode_rgb_png(payload)


def validate_trusted_capture(
    evidence: TrustedCaptureEvidence,
    *,
    policy: ReviewedCapturePolicy,
    capture_parent: Path,
    current_binding: RuntimeBinding,
    now_ns: int,
    max_age_ns: int,
) -> SecretSafeCapture:
    if type(evidence) is not TrustedCaptureEvidence or type(policy) is not ReviewedCapturePolicy:
        raise CaptureEdgeError("CAPTURE_EVIDENCE_INVALID")
    current = _snapshot_binding(current_binding)
    _require_current(current, now_ns, max_age_ns)
    if current != evidence.runtime_binding:
        raise CaptureEdgeError("CAPTURE_RUNTIME_BINDING_MISMATCH")
    if (
        type(evidence.source_monotonic_ns) is not int
        or evidence.source_monotonic_ns <= 0
        or type(evidence.acquisition_completed_ns) is not int
        or evidence.acquisition_completed_ns < evidence.source_monotonic_ns
        or now_ns < evidence.acquisition_completed_ns
        or now_ns - evidence.source_monotonic_ns > max_age_ns
    ):
        raise CaptureEdgeError("CAPTURE_EVIDENCE_STALE")
    if evidence.secret_policy_ref != policy.policy_ref:
        raise CaptureEdgeError("CAPTURE_SECRET_POLICY_MISMATCH")
    if (evidence.geometry.width, evidence.geometry.height) != (
        policy.expected_width,
        policy.expected_height,
    ):
        raise CaptureEdgeError("CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH")
    root = _prepare_capture_root(capture_parent)
    width, height, pixels = _read_capture_artifact(root, evidence.full_frame)
    if (width, height) != (evidence.geometry.width, evidence.geometry.height):
        raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
    stride = width * 3
    for region in policy.secret_regions:
        _require_region(region, evidence.geometry)
        for row in range(region.y, region.y + region.height):
            start = row * stride + region.x * 3
            end = start + region.width * 3
            if any(pixels[start:end]):
                raise CaptureEdgeError("CAPTURE_SECRET_MASK_INVALID")
    artifact = evidence.full_frame
    if evidence.crop is not None:
        crop = evidence.crop
        if crop.region is None or crop.parent_full_sha256 != evidence.full_frame.sha256:
            raise CaptureEdgeError("CAPTURE_PARENT_BINDING_INVALID")
        crop_width, crop_height, crop_pixels = _read_capture_artifact(root, crop)
        if (crop_width, crop_height) != (crop.region.width, crop.region.height):
            raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        if crop_pixels != _crop_rgb(pixels, evidence.geometry, crop.region):
            raise CaptureEdgeError("CAPTURE_PARENT_BINDING_INVALID")
        artifact = crop
    return SecretSafeCapture(
        run_id=evidence.run_id,
        evidence_ref=f"capture:{artifact.sha256}",
        path=artifact.path,
        sha256=artifact.sha256,
        secret_safe=True,
        source_monotonic_ns=evidence.source_monotonic_ns,
    )


class _TrustedAgentEdgeBridge(AgentEdgeBridge):
    """Bridge variant used only by the trusted composition root."""

    def accept(
        self,
        value: Mapping[str, Any],
        *,
        now_epoch_ms: int,
        expected_session_id: str,
        expected_run_id: str,
        previous_observed_epoch_ms: int | None = None,
    ):
        if not isinstance(value, Mapping) or value.get("capture") is not None:
            raise ValidationError(
                "EDGE_CAPTURE_TRUSTED_EVIDENCE_REQUIRED",
                "raw edge capture cannot self-assert secret safety",
            )
        return super().accept(
            value,
            now_epoch_ms=now_epoch_ms,
            expected_session_id=expected_session_id,
            expected_run_id=expected_run_id,
            previous_observed_epoch_ms=previous_observed_epoch_ms,
        )

    def current_admission(
        self,
        *,
        session_id: str,
        task_id: str | None,
        current_run_id: str | None,
        runtime_access: str,
        task_deadline_epoch_ms: int | None,
        now_epoch_ms: int,
    ):
        status = self._authority_status(
            session_id=session_id,
            task_id=task_id,
            current_run_id=current_run_id,
            runtime_access=runtime_access,
            task_deadline_epoch_ms=task_deadline_epoch_ms,
            now_epoch_ms=now_epoch_ms,
        )
        if status.get("current") is not True:
            raise ValidationError(
                str(status.get("reason", "RUNTIME_ADMISSION_REQUIRED")),
                "current read-only runtime admission is required",
            )
        authority = self._runtime_authorities.get(session_id)
        if authority is None:
            raise ValidationError(
                "RUNTIME_ADMISSION_REQUIRED",
                "current read-only runtime admission is required",
            )
        return authority.admission

    def status(
        self,
        *,
        session_id: str,
        task_id: str | None,
        current_run_id: str | None,
        runtime_access: str,
        task_deadline_epoch_ms: int | None,
        heartbeat_epoch_ms: int | None,
        events: Sequence[Mapping[str, Any]],
        now_epoch_ms: int,
    ) -> dict[str, object]:
        result = super().status(
            session_id=session_id,
            task_id=task_id,
            current_run_id=current_run_id,
            runtime_access=runtime_access,
            task_deadline_epoch_ms=task_deadline_epoch_ms,
            heartbeat_epoch_ms=heartbeat_epoch_ms,
            events=events,
            now_epoch_ms=now_epoch_ms,
        )
        result["capture"] = self._empty_capture()
        event = self._latest_event(events, "EDGE_CAPTURE_VALIDATED")
        if event is None or not isinstance(event.get("payload"), Mapping):
            return result
        payload = event["payload"]
        capture = payload.get("capture")
        if not isinstance(capture, Mapping):
            return result
        value = dict(capture)
        observed = value.get("observed_epoch_ms")
        value["current"] = bool(
            result.get("current") is True
            and event.get("run_id") == current_run_id
            and payload.get("edge_instance_id") == result.get("edge_instance_id")
            and value.get("status") == "AVAILABLE"
            and value.get("secret_safe") is True
            and type(observed) is int
            and observed <= now_epoch_ms
            and now_epoch_ms - observed <= self.heartbeat_timeout_ms
        )
        result["capture"] = value
        return result


def _binding_matches_admission(binding: RuntimeBinding, admission: Any) -> bool:
    locator = admission.locator
    process = admission.process
    window = admission.window
    return bool(
        binding.runtime_id == admission.runtime_namespace
        and binding.target_container == locator.get("container")
        and binding.display == locator.get("display")
        and binding.display == process.get("display")
        and binding.display == window.get("display")
        and binding.pid == process.get("pid")
        and binding.process_start_ticks == process.get("process_start_ticks")
        and binding.xid == window.get("xid")
        and binding.pid == window.get("pid")
        and binding.client_version == process.get("client_version")
        and binding.client_size == process.get("client_size")
        and binding.client_sha256.lower() == str(process.get("client_sha256", "")).lower()
        and binding.target_uniqueness == admission.target_uniqueness
    )


def _replay_meta_key(session_id: str, run_id: str, peer_id: str) -> str:
    session_id = validate_opaque_id(session_id, field_name="session_id")
    run_id = validate_opaque_id(run_id, field_name="run_id")
    peer_id = validate_opaque_id(peer_id, field_name="peer_id")
    digest = hashlib.sha256(f"{session_id}\0{run_id}\0{peer_id}".encode("utf-8")).hexdigest()
    return f"{_REPLAY_META_PREFIX}{digest}"


def _load_replay_ledger(service: ControlDomainService, key: str) -> EdgeReplayLedger:
    raw = service.store._meta(key)
    if raw is None:
        return EdgeReplayLedger()
    try:
        value = json.loads(raw)
    except (TypeError, ValueError):
        raise ValidationError(
            "EDGE_REPLAY_STATE_INVALID",
            "persisted edge replay state is invalid",
        ) from None
    return EdgeReplayLedger.from_snapshot(value)


def _save_replay_ledger(
    service: ControlDomainService,
    key: str,
    ledger: EdgeReplayLedger,
) -> None:
    value = ledger.snapshot()
    EdgeReplayLedger.from_snapshot(value)
    encoded = jcs_dumps(value)
    with service.store._transaction("vision_p2_edge_replay"):
        service.store._db.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
            (key, encoded),
        )


class DurableEdgeTransportVerifier:
    """Verify against durable replay state and persist it before returning accepted data."""

    def __init__(
        self,
        runtime: TrustedVisionP2Runtime,
        *,
        session_id: str,
        run_id: str,
        expected_peer_id: str,
        expected_peer_auth_key: bytes,
        expected_connection_id: str,
    ) -> None:
        self._runtime = runtime
        self._session_id = validate_opaque_id(session_id, field_name="session_id")
        self._run_id = validate_opaque_id(run_id, field_name="run_id")
        self._peer_id = validate_opaque_id(expected_peer_id, field_name="expected_peer_id")
        self._auth_key = bytes(expected_peer_auth_key)
        if len(self._auth_key) < 32:
            raise ValidationError(
                "EDGE_AUTH_KEY_INVALID",
                "edge authentication key is invalid",
            )
        self._connection_id = validate_opaque_id(
            expected_connection_id,
            field_name="expected_connection_id",
        )
        self._meta_key = _replay_meta_key(
            self._session_id,
            self._run_id,
            self._peer_id,
        )
        self._lock = threading.RLock()
        self._failed = False

    def verify(self, packet: bytes, *, now_epoch_ms: int) -> VerifiedEdgeFrame:
        with self._lock:
            if self._failed:
                raise ValidationError(
                    "EDGE_REPLAY_PERSISTENCE_FAILED",
                    "durable edge verifier is fail-closed",
                )
            ledger = _load_replay_ledger(self._runtime.service, self._meta_key)
            verifier = EdgeTransportVerifier(
                expected_peer_id=self._peer_id,
                expected_peer_auth_key=self._auth_key,
                replay_ledger=ledger,
                expected_connection_id=self._connection_id,
            )
            frame = verifier.verify(packet, now_epoch_ms=now_epoch_ms)
            if frame.session_id != self._session_id or frame.run_id != self._run_id:
                raise ValidationError(
                    "EDGE_SESSION_RUN_REJECTED",
                    "edge frame belongs to another session or run",
                )
            try:
                _save_replay_ledger(self._runtime.service, self._meta_key, ledger)
            except Exception:
                self._failed = True
                raise
            return frame


class TrustedVisionP2Runtime:
    """One application-owned adapter over the existing ControlDomain/session/store."""

    def __init__(
        self,
        service: ControlDomainService,
        composition: VisionP2TrustedComposition,
    ) -> None:
        if type(service) is not ControlDomainService or type(composition) is not VisionP2TrustedComposition:
            raise TypeError("trusted vision P2 composition inputs invalid")
        if service.agent._tasks or service.agent._sessions:
            raise ValidationError(
                "VISION_P2_COMPOSITION_LATE_ATTACH",
                "trusted vision P2 composition must attach before agent session use",
            )
        service.agent.edge = _TrustedAgentEdgeBridge(
            runtime_authority_configuration=composition.runtime_authority_configuration
        )
        self.service = service
        self.composition = composition
        self._capture_parent = service.store.control_dir

    @property
    def capture_root(self) -> Path:
        return self._capture_parent / _CAPTURE_ROOT_NAME

    def build_capture_edge(
        self,
        *,
        binding_reader: Callable[[], RuntimeBinding],
        frame_source: FrameSource,
        monotonic_ns: Callable[[], int],
    ) -> TrustedCaptureEdge:
        policy = self.composition.capture_policy
        if policy is None:
            raise CaptureEdgeError("CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED")
        root = _prepare_capture_root(self._capture_parent)
        return TrustedCaptureEdge(
            binding_reader=binding_reader,
            frame_source=frame_source,
            monotonic_ns=monotonic_ns,
            policy=policy,
            root=root,
        )

    def validate_capture(
        self,
        evidence: TrustedCaptureEvidence,
        *,
        current_binding: RuntimeBinding,
        now_ns: int,
        max_age_ns: int,
    ) -> SecretSafeCapture:
        policy = self.composition.capture_policy
        if policy is None:
            raise CaptureEdgeError("CAPTURE_TRUSTED_POLICY_CONSUMER_REQUIRED")
        return validate_trusted_capture(
            evidence,
            policy=policy,
            capture_parent=self._capture_parent,
            current_binding=current_binding,
            now_ns=now_ns,
            max_age_ns=max_age_ns,
        )

    def ingest_edge_observation(self, value: Mapping[str, Any]) -> dict[str, object]:
        return self.service.agent.ingest_edge_observation(value)

    def ingest_capture(
        self,
        session_id: str,
        evidence: TrustedCaptureEvidence,
        *,
        current_binding: RuntimeBinding,
        now_ns: int,
        max_age_ns: int,
    ) -> dict[str, object]:
        safe = self.validate_capture(
            evidence,
            current_binding=current_binding,
            now_ns=now_ns,
            max_age_ns=max_age_ns,
        )
        agent = self.service.agent
        with agent._lock:
            session = agent.ensure_session(session_id)
            task = agent._tasks.get(session_id)
            if task is None or task.runtime_access != "read_only":
                raise ValidationError(
                    "EDGE_RUNTIME_NOT_ADMITTED",
                    "validated capture requires a read-only task",
                )
            if session.current_run_id != task.run_id or evidence.run_id != task.run_id:
                raise ValidationError(
                    "EDGE_BINDING_MISMATCH",
                    "validated capture belongs to another run",
                )
            now_epoch_ms = agent._now_epoch_ms()
            if now_epoch_ms >= task.deadline_epoch_ms:
                agent.edge.disconnect(session_id)
                raise ValidationError(
                    "EDGE_TASK_DEADLINE_EXPIRED",
                    "expired task cannot ingest capture",
                )
            edge = agent.snapshot(session_id)["edge"]
            if edge.get("current") is not True or not isinstance(edge.get("edge_instance_id"), str):
                raise ValidationError(
                    str(edge.get("reason", "EDGE_RUNTIME_NOT_ADMITTED")),
                    "validated capture requires the current admitted edge instance",
                )
            admission = agent.edge.current_admission(
                session_id=session_id,
                task_id=task.task_id,
                current_run_id=task.run_id,
                runtime_access=task.runtime_access,
                task_deadline_epoch_ms=task.deadline_epoch_ms,
                now_epoch_ms=now_epoch_ms,
            )
            if not _binding_matches_admission(evidence.runtime_binding, admission):
                raise ValidationError(
                    "CAPTURE_RUNTIME_ADMISSION_MISMATCH",
                    "capture binding does not match the current admitted runtime identity",
                )
            capture_payload = {
                "status": "AVAILABLE",
                "artifact_ref": safe.evidence_ref,
                "sha256": safe.sha256,
                "observed_epoch_ms": now_epoch_ms,
                "secret_safe": True,
            }
            payload = {
                "edge_instance_id": edge["edge_instance_id"],
                "capture": capture_payload,
                "physical_effect": False,
            }
            agent._persist_event(
                session_id,
                provenance=AgentProvenance.RUNTIME,
                kind="EDGE_CAPTURE_VALIDATED",
                artifact_refs=(safe.evidence_ref,),
                payload=payload,
                operation="vision_p2_validated_capture",
            )
            retained = agent._evidence_refs.setdefault(session_id, [])
            if safe.evidence_ref not in retained:
                retained.append(safe.evidence_ref)
            return agent.snapshot(session_id)

    def durable_edge_verifier(
        self,
        *,
        session_id: str,
        run_id: str,
        expected_peer_id: str,
        expected_peer_auth_key: bytes,
        expected_connection_id: str,
    ) -> DurableEdgeTransportVerifier:
        return DurableEdgeTransportVerifier(
            self,
            session_id=session_id,
            run_id=run_id,
            expected_peer_id=expected_peer_id,
            expected_peer_auth_key=expected_peer_auth_key,
            expected_connection_id=expected_connection_id,
        )


__all__ = [
    "DurableEdgeTransportVerifier",
    "ReviewedCapturePolicy",
    "TrustedCaptureArtifact",
    "TrustedCaptureEdge",
    "TrustedCaptureEvidence",
    "TrustedVisionP2Runtime",
    "VisionP2TrustedComposition",
    "validate_trusted_capture",
]
