from __future__ import annotations

import binascii
import hashlib
import re
import struct
import subprocess
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from weakref import WeakValueDictionary

from tools.tibia_re_control_center.agent_vision import SecretSafeCapture


class CaptureEdgeError(RuntimeError):
    """Fail-closed capture error with a non-secret reason code."""


@dataclass(frozen=True)
class WindowGeometry:
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if any(type(value) is not int for value in (self.x, self.y, self.width, self.height)):
            raise ValueError("geometry values must be integers")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("geometry dimensions must be positive")


@dataclass(frozen=True)
class PixelRegion:
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if any(type(value) is not int for value in (self.x, self.y, self.width, self.height)):
            raise ValueError("pixel region values must be integers")
        if self.x < 0 or self.y < 0 or self.width <= 0 or self.height <= 0:
            raise ValueError("pixel region invalid")


@dataclass(frozen=True)
class RuntimeBinding:
    provenance_ref: str
    runtime_id: str
    target_container: str
    display: str
    pid: int
    process_start_ticks: int
    xid: int
    client_version: str
    client_size: int
    client_sha256: str
    observed_monotonic_ns: int
    runtime_access: str
    target_uniqueness: str

    def __post_init__(self) -> None:
        strings = (
            self.provenance_ref,
            self.runtime_id,
            self.target_container,
            self.display,
            self.client_version,
        )
        if any(type(value) is not str or not value for value in strings):
            raise ValueError("runtime binding string invalid")
        integers = (
            self.pid,
            self.process_start_ticks,
            self.xid,
            self.client_size,
            self.observed_monotonic_ns,
        )
        if any(type(value) is not int or value <= 0 for value in integers):
            raise ValueError("runtime binding integer invalid")
        if self.runtime_access != "read_only" or self.target_uniqueness != "PROVEN":
            raise ValueError("runtime binding is not read-only admitted")
        digest = self.client_sha256
        if type(digest) is not str or len(digest) != 64 or any(
            char not in "0123456789abcdef" for char in digest.lower()
        ):
            raise ValueError("client sha256 invalid")


class ReviewedSecretMaskPolicy:
    """A policy can only be created by its trusted composition-time resolver."""

    __slots__ = ("_issuer", "_sealed", "expected_height", "expected_width", "policy_id", "secret_regions")

    def __init__(self, *args, **kwargs) -> None:
        raise TypeError("ReviewedSecretMaskPolicy is resolver-issued")

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("ReviewedSecretMaskPolicy is immutable")
        object.__setattr__(self, name, value)

    @classmethod
    def _issue(
        cls,
        issuer: ReviewedSecretMaskPolicyResolver,
        issuance_token: object,
        *,
        policy_id: str,
        expected_width: int,
        expected_height: int,
        secret_regions: tuple[PixelRegion, ...],
    ) -> ReviewedSecretMaskPolicy:
        if issuance_token is not _SECRET_POLICY_ISSUANCE_TOKEN:
            raise TypeError("ReviewedSecretMaskPolicy is resolver-issued")
        if type(policy_id) is not str or re.fullmatch(r"[A-Za-z0-9_.:-]{1,80}", policy_id) is None:
            raise ValueError("reviewed secret policy id invalid")
        if (
            type(expected_width) is not int
            or type(expected_height) is not int
            or expected_width <= 0
            or expected_height <= 0
        ):
            raise ValueError("reviewed secret geometry invalid")
        if (
            type(secret_regions) is not tuple
            or not secret_regions
            or any(type(region) is not PixelRegion for region in secret_regions)
        ):
            raise ValueError("reviewed secret regions invalid")
        geometry = WindowGeometry(0, 0, expected_width, expected_height)
        for region in secret_regions:
            if region.x + region.width > geometry.width or region.y + region.height > geometry.height:
                raise ValueError("reviewed secret regions invalid")
        policy = object.__new__(cls)
        policy.policy_id = policy_id
        policy.expected_width = expected_width
        policy.expected_height = expected_height
        policy.secret_regions = secret_regions
        policy._issuer = issuer
        policy._sealed = True
        return policy

    @property
    def policy_ref(self) -> str:
        regions = sorted(
            (region.x, region.y, region.width, region.height)
            for region in self.secret_regions
        )
        canonical = "|".join(
            [
                "reviewed-secret-mask-v1",
                self.policy_id,
                str(self.expected_width),
                str(self.expected_height),
                *(f"{x},{y},{width},{height}" for x, y, width, height in regions),
            ]
        ).encode("ascii")
        return f"secret-mask:{hashlib.sha256(canonical).hexdigest()}"


class ReviewedSecretMaskPolicyResolver:
    """Trusted composition root that issues exactly one reviewed deterministic policy."""

    def __init__(
        self,
        *,
        policy_id: str,
        expected_width: int,
        expected_height: int,
        secret_regions: tuple[PixelRegion, ...],
    ) -> None:
        self._policy = ReviewedSecretMaskPolicy._issue(
            self,
            _SECRET_POLICY_ISSUANCE_TOKEN,
            policy_id=policy_id,
            expected_width=expected_width,
            expected_height=expected_height,
            secret_regions=secret_regions,
        )

    @property
    def policy(self) -> ReviewedSecretMaskPolicy:
        return self._policy

    def owns(self, policy: ReviewedSecretMaskPolicy) -> bool:
        return policy is self._policy and policy._issuer is self


class FrameSource(Protocol):
    def geometry(self, binding: RuntimeBinding) -> WindowGeometry: ...

    def capture_rgb(self, binding: RuntimeBinding, geometry: WindowGeometry) -> bytes: ...


class _ProcessRunner(Protocol):
    def run(self, args: tuple[str, ...], *, timeout_s: float): ...


class _SubprocessRunner:
    def run(self, args: tuple[str, ...], *, timeout_s: float):
        try:
            return subprocess.run(
                list(args),
                check=False,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=timeout_s,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise CaptureEdgeError("CAPTURE_COMMAND_FAILED") from None


class KasmX11FfmpegFrameSource:
    """Exact-binding, read-only X11 capture with a fixed command vocabulary."""

    def __init__(self, *, runner: _ProcessRunner | None = None, timeout_s: float = 10.0) -> None:
        if type(timeout_s) not in (int, float) or isinstance(timeout_s, bool) or not 0 < timeout_s <= 30:
            raise ValueError("capture command timeout invalid")
        self._runner = runner or _SubprocessRunner()
        self._timeout_s = float(timeout_s)

    @staticmethod
    def _prefix(binding: RuntimeBinding) -> tuple[str, ...]:
        if re.fullmatch(r"[A-Za-z0-9_.-]+", binding.target_container) is None:
            raise CaptureEdgeError("CAPTURE_BINDING_INVALID")
        if re.fullmatch(r":\d+(?:\.\d+)?", binding.display) is None:
            raise CaptureEdgeError("CAPTURE_BINDING_INVALID")
        return (
            "docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={binding.display}",
            binding.target_container,
        )

    def _run(self, binding: RuntimeBinding, args: tuple[str, ...], error_code: str) -> bytes:
        result = self._runner.run(self._prefix(binding) + args, timeout_s=self._timeout_s)
        returncode = getattr(result, "returncode", None)
        stdout = getattr(result, "stdout", None)
        if type(returncode) is not int or type(stdout) is not bytes:
            raise CaptureEdgeError("CAPTURE_COMMAND_RESULT_INVALID")
        if returncode != 0:
            raise CaptureEdgeError(error_code)
        return stdout

    def geometry(self, binding: RuntimeBinding) -> WindowGeometry:
        raw = self._run(
            binding,
            ("xdotool", "getwindowgeometry", "--shell", str(binding.xid)),
            "CAPTURE_GEOMETRY_FAILED",
        )
        try:
            values = {}
            for line in raw.decode("ascii").splitlines():
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key in {"X", "Y", "WIDTH", "HEIGHT"}:
                    if key in values or not re.fullmatch(r"-?\d+", value):
                        raise ValueError
                    values[key] = int(value)
            if set(values) != {"X", "Y", "WIDTH", "HEIGHT"}:
                raise ValueError
            return WindowGeometry(values["X"], values["Y"], values["WIDTH"], values["HEIGHT"])
        except (UnicodeDecodeError, ValueError):
            raise CaptureEdgeError("CAPTURE_GEOMETRY_INVALID") from None

    def capture_rgb(self, binding: RuntimeBinding, geometry: WindowGeometry) -> bytes:
        if type(geometry) is not WindowGeometry:
            raise ValueError("geometry invalid")
        return self._run(
            binding,
            (
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
                "-f", "x11grab", "-video_size", f"{geometry.width}x{geometry.height}",
                "-i", f"{binding.display}+{geometry.x},{geometry.y}",
                "-frames:v", "1", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1",
            ),
            "CAPTURE_FFMPEG_FAILED",
        )


@dataclass(frozen=True)
class CaptureArtifact:
    path: Path
    sha256: str
    region: PixelRegion | None = None
    parent_full_sha256: str | None = None


class CaptureEvidence:
    """Opaque producer-issued evidence; caller-created instances never reach vision."""

    __slots__ = (
        "__weakref__",
        "_sealed",
        "changed_from_previous",
        "crop",
        "full_frame",
        "geometry",
        "is_black",
        "is_blank",
        "run_id",
        "runtime_binding",
        "secret_policy_ref",
        "secret_safe",
        "source_monotonic_ns",
    )

    def __init__(self, *args, **kwargs) -> None:
        raise TypeError("CaptureEvidence is producer-issued")

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("CaptureEvidence is immutable")
        object.__setattr__(self, name, value)

    @classmethod
    def _issue(
        cls,
        *,
        issuance_token: object,
        run_id: str,
        runtime_binding: RuntimeBinding,
        geometry: WindowGeometry,
        source_monotonic_ns: int,
        full_frame: CaptureArtifact,
        secret_policy_ref: str,
        is_blank: bool,
        is_black: bool,
        changed_from_previous: bool | None,
        crop: CaptureArtifact | None,
    ) -> CaptureEvidence:
        if issuance_token is not _CAPTURE_EVIDENCE_ISSUANCE_TOKEN:
            raise TypeError("CaptureEvidence is producer-issued")
        evidence = object.__new__(cls)
        evidence.run_id = run_id
        evidence.runtime_binding = runtime_binding
        evidence.geometry = geometry
        evidence.source_monotonic_ns = source_monotonic_ns
        evidence.full_frame = full_frame
        evidence.secret_safe = True
        evidence.secret_policy_ref = secret_policy_ref
        evidence.is_blank = is_blank
        evidence.is_black = is_black
        evidence.changed_from_previous = changed_from_previous
        evidence.crop = crop
        evidence._sealed = True
        _ISSUED_EVIDENCE[id(evidence)] = evidence
        return evidence

    def validated_vision_capture(
        self,
        *,
        current_binding: RuntimeBinding,
        now_ns: int,
        max_age_ns: int,
    ) -> SecretSafeCapture:
        if _ISSUED_EVIDENCE.get(id(self)) is not self:
            raise CaptureEdgeError("CAPTURE_EVIDENCE_UNISSUED")
        if type(current_binding) is not RuntimeBinding:
            raise ValueError("current binding invalid")
        if type(now_ns) is not int or type(max_age_ns) is not int or max_age_ns < 0:
            raise ValueError("capture time bound invalid")
        if current_binding != self.runtime_binding:
            raise CaptureEdgeError("CAPTURE_RUNTIME_BINDING_MISMATCH")
        age = now_ns - self.source_monotonic_ns
        if age < 0 or age > max_age_ns:
            raise CaptureEdgeError("CAPTURE_EVIDENCE_STALE")
        if self.secret_safe is not True:
            raise CaptureEdgeError("CAPTURE_NOT_SECRET_SAFE")
        artifacts = (self.full_frame,) if self.crop is None else (self.full_frame, self.crop)
        for artifact in artifacts:
            try:
                actual = hashlib.sha256(artifact.path.read_bytes()).hexdigest()
            except OSError:
                raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID") from None
            if actual != artifact.sha256:
                raise CaptureEdgeError("CAPTURE_ARTIFACT_INTEGRITY_INVALID")
        if self.crop is not None and self.crop.parent_full_sha256 != self.full_frame.sha256:
            raise CaptureEdgeError("CAPTURE_PARENT_BINDING_INVALID")
        artifact = self.crop or self.full_frame
        return SecretSafeCapture(
            run_id=self.run_id,
            evidence_ref=f"capture:{artifact.sha256}",
            path=artifact.path,
            sha256=artifact.sha256,
            secret_safe=self.secret_safe,
            source_monotonic_ns=self.source_monotonic_ns,
        )


_ISSUED_EVIDENCE: WeakValueDictionary[int, CaptureEvidence] = WeakValueDictionary()
_SECRET_POLICY_ISSUANCE_TOKEN = object()
_CAPTURE_EVIDENCE_ISSUANCE_TOKEN = object()


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    crc = binascii.crc32(body) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", crc)


def _require_rgb(geometry: WindowGeometry, pixels: bytes) -> None:
    expected = geometry.width * geometry.height * 3
    if type(pixels) is not bytes or len(pixels) != expected:
        raise CaptureEdgeError("CAPTURE_RGB_LENGTH_INVALID")


def _encode_rgb_png(width: int, height: int, pixels: bytes) -> bytes:
    geometry = WindowGeometry(x=0, y=0, width=width, height=height)
    _require_rgb(geometry, pixels)
    stride = width * 3
    rows = b"".join(
        b"\x00" + pixels[offset : offset + stride]
        for offset in range(0, len(pixels), stride)
    )
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", zlib.compress(rows))
        + _png_chunk(b"IEND", b"")
    )


def _require_region(region: PixelRegion, geometry: WindowGeometry) -> None:
    if region.x + region.width > geometry.width or region.y + region.height > geometry.height:
        raise CaptureEdgeError("CAPTURE_REGION_OUT_OF_BOUNDS")


def _mask_rgb(
    pixels: bytes,
    geometry: WindowGeometry,
    regions: tuple[PixelRegion, ...],
) -> bytes:
    _require_rgb(geometry, pixels)
    masked = bytearray(pixels)
    stride = geometry.width * 3
    for region in regions:
        _require_region(region, geometry)
        for row in range(region.y, region.y + region.height):
            start = row * stride + region.x * 3
            end = start + region.width * 3
            masked[start:end] = b"\x00" * (end - start)
    return bytes(masked)


def _crop_rgb(pixels: bytes, geometry: WindowGeometry, region: PixelRegion) -> bytes:
    _require_rgb(geometry, pixels)
    _require_region(region, geometry)
    stride = geometry.width * 3
    cropped = bytearray()
    for row in range(region.y, region.y + region.height):
        start = row * stride + region.x * 3
        cropped.extend(pixels[start : start + region.width * 3])
    return bytes(cropped)


def _persist_png(
    root: Path,
    png: bytes,
    *,
    region: PixelRegion | None = None,
    parent_full_sha256: str | None = None,
) -> CaptureArtifact:
    digest = hashlib.sha256(png).hexdigest()
    path = root / f"{digest}.png"
    if path.exists():
        if path.read_bytes() != png:
            raise CaptureEdgeError("CONTENT_ADDRESS_COLLISION")
    else:
        path.write_bytes(png)
    return CaptureArtifact(
        path=path,
        sha256=digest,
        region=region,
        parent_full_sha256=parent_full_sha256,
    )


class CaptureEdge:
    def __init__(
        self,
        *,
        binding_reader: Callable[[], RuntimeBinding],
        frame_source: FrameSource,
        monotonic_ns: Callable[[], int],
        secret_policy: ReviewedSecretMaskPolicy,
        policy_resolver: ReviewedSecretMaskPolicyResolver | None = None,
    ) -> None:
        resolver = secret_policy._issuer if type(secret_policy) is ReviewedSecretMaskPolicy else None
        if policy_resolver is not None:
            resolver = policy_resolver
        if (
            type(secret_policy) is not ReviewedSecretMaskPolicy
            or type(resolver) is not ReviewedSecretMaskPolicyResolver
            or not resolver.owns(secret_policy)
        ):
            raise ValueError("reviewed secret policy issuer invalid")
        self._binding_reader = binding_reader
        self._frame_source = frame_source
        self._monotonic_ns = monotonic_ns
        self._secret_policy = secret_policy

    @staticmethod
    def _require_current(binding: RuntimeBinding, now_ns: int, max_age_ns: int) -> None:
        if type(now_ns) is not int or type(max_age_ns) is not int or max_age_ns < 0:
            raise ValueError("capture time bound invalid")
        age = now_ns - binding.observed_monotonic_ns
        if age < 0 or age > max_age_ns:
            raise CaptureEdgeError("RUNTIME_BINDING_STALE")

    def capture(
        self,
        *,
        run_id: str,
        evidence_root: Path,
        max_binding_age_ns: int,
        crop: PixelRegion | None = None,
        previous_full_sha256: str | None = None,
    ) -> CaptureEvidence:
        if type(run_id) is not str or not run_id:
            raise ValueError("run_id invalid")
        if crop is not None and type(crop) is not PixelRegion:
            raise ValueError("crop invalid")
        if previous_full_sha256 is not None and (
            type(previous_full_sha256) is not str
            or len(previous_full_sha256) != 64
            or any(c not in "0123456789abcdefABCDEF" for c in previous_full_sha256)
        ):
            raise ValueError("previous full sha256 invalid")
        before = self._binding_reader()
        binding_checked_ns = self._monotonic_ns()
        self._require_current(before, binding_checked_ns, max_binding_age_ns)
        geometry = self._frame_source.geometry(before)
        if type(geometry) is not WindowGeometry:
            raise CaptureEdgeError("CAPTURE_GEOMETRY_INVALID")
        if (
            geometry.width != self._secret_policy.expected_width
            or geometry.height != self._secret_policy.expected_height
        ):
            raise CaptureEdgeError("CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH")
        for region in self._secret_policy.secret_regions:
            _require_region(region, geometry)
        if crop is not None:
            _require_region(crop, geometry)

        acquisition_started_ns = self._monotonic_ns()
        raw_pixels = self._frame_source.capture_rgb(before, geometry)
        _require_rgb(geometry, raw_pixels)
        safe_pixels = _mask_rgb(raw_pixels, geometry, self._secret_policy.secret_regions)
        first_pixel = safe_pixels[:3]
        is_blank = all(safe_pixels[offset : offset + 3] == first_pixel for offset in range(0, len(safe_pixels), 3))
        is_black = max(safe_pixels, default=0) <= 4
        crop_pixels = None if crop is None else _crop_rgb(safe_pixels, geometry, crop)

        after = self._binding_reader()
        if after != before:
            raise CaptureEdgeError("RUNTIME_BINDING_CHANGED")
        after_geometry = self._frame_source.geometry(after)
        if type(after_geometry) is not WindowGeometry:
            raise CaptureEdgeError("CAPTURE_GEOMETRY_INVALID")
        if after_geometry != geometry:
            raise CaptureEdgeError("CAPTURE_GEOMETRY_CHANGED")
        final_binding = self._binding_reader()
        if final_binding != before:
            raise CaptureEdgeError("RUNTIME_BINDING_CHANGED")
        full_png = _encode_rgb_png(geometry.width, geometry.height, safe_pixels)
        crop_png = None if crop is None else _encode_rgb_png(crop.width, crop.height, crop_pixels)
        root = Path(evidence_root)
        root.mkdir(parents=True, exist_ok=True)
        full_artifact = _persist_png(root, full_png)
        changed_from_previous = (
            None
            if previous_full_sha256 is None
            else full_artifact.sha256 != previous_full_sha256.lower()
        )
        crop_artifact = None
        if crop is not None and crop_png is not None:
            crop_artifact = _persist_png(
                root,
                crop_png,
                region=crop,
                parent_full_sha256=full_artifact.sha256,
            )
        return CaptureEvidence._issue(
            issuance_token=_CAPTURE_EVIDENCE_ISSUANCE_TOKEN,
            run_id=run_id,
            runtime_binding=before,
            geometry=geometry,
            source_monotonic_ns=acquisition_started_ns,
            full_frame=full_artifact,
            secret_policy_ref=self._secret_policy.policy_ref,
            is_blank=is_blank,
            is_black=is_black,
            changed_from_previous=changed_from_previous,
            crop=crop_artifact,
        )
