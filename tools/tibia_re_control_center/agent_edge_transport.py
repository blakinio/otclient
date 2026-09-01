"""Authenticated, authority-neutral Phase 2 runtime-edge transport primitives."""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import math
import re
import secrets
import socket
import struct
import threading
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any

from .canonical import jcs_dumps
from .model import (
    MAX_SAFE_INTEGER,
    ValidationError,
    checked_non_negative,
    require_exact_keys,
    validate_opaque_id,
)
from .privacy import ensure_no_secret_material

EDGE_TRANSPORT_SCHEMA = "otclient.local-agent.edge-transport.v1"
EDGE_TRANSPORT_PROTOCOL_MAJOR = 1
EDGE_ARTIFACT_SCHEMA = "otclient.local-agent.artifact-ref.v1"
MIN_AUTH_KEY_BYTES = 32
DEFAULT_MAX_AGE_MS = 30_000
DEFAULT_MAX_FUTURE_SKEW_MS = 5_000
MAX_METADATA_FRAME_BYTES = 262_144
MAX_ARTIFACT_BYTES = 32 * 1024 * 1024
MAX_PAYLOAD_DEPTH = 16
MAX_PAYLOAD_ITEMS = 4096
_MEDIA_TYPE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,63}/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,63}$")
_FORBIDDEN_CONTROL_KEYS = frozenset({
    "command", "commands", "shell", "shell_command", "argv", "exec", "executable",
    "process_control", "process_signal", "signal", "kill", "restart",
    "keypress", "keystroke", "mouse", "click", "coordinates", "gui_control",
    "raw_gui", "type_text", "text_entry", "get_secret", "secret_capability_ref",
})


_LOCAL_IPV4_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in ("127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "169.254.0.0/16")
)
_LOCAL_IPV6_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in ("::1/128", "fc00::/7", "fe80::/10")
)


def _is_local_address(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    networks = _LOCAL_IPV4_NETWORKS if address.version == 4 else _LOCAL_IPV6_NETWORKS
    return any(address in network for network in networks)


def resolve_edge_endpoint(host: str, port: int) -> str:
    if not isinstance(host, str) or not host or len(host.encode("utf-8")) > 255:
        raise ValidationError("EDGE_ENDPOINT_INVALID", "edge transport host is invalid")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValidationError("EDGE_ENDPOINT_INVALID", "edge transport port is invalid")
    try:
        literal = str(ipaddress.ip_address(host))
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        except OSError as exc:
            raise ValidationError(
                "EDGE_ENDPOINT_RESOLUTION_FAILED",
                "edge transport endpoint resolution failed safely",
            ) from exc
        resolved: list[str] = []
        for info in infos:
            address = str(ipaddress.ip_address(info[4][0]))
            if address not in resolved:
                resolved.append(address)
        if not resolved:
            raise ValidationError(
                "EDGE_ENDPOINT_RESOLUTION_FAILED",
                "edge transport endpoint resolution returned no addresses",
            )
        if any(not _is_local_address(address) for address in resolved):
            raise ValidationError(
                "EDGE_ENDPOINT_PUBLIC_REJECTED",
                "edge transport endpoint must resolve only to local/private addresses",
            )
        return resolved[0]
    if not _is_local_address(literal):
        raise ValidationError(
            "EDGE_ENDPOINT_PUBLIC_REJECTED",
            "edge transport endpoint must be local/private",
        )
    return literal


def _validate_media_type(value: Any) -> str:
    if not isinstance(value, str) or not _MEDIA_TYPE_RE.fullmatch(value):
        raise ValidationError(
            "EDGE_ARTIFACT_MEDIA_TYPE_INVALID",
            "artifact media type must be a plain type/subtype token",
        )
    return value


def _snapshot_payload(value: Any, *, depth: int = 0, counter: list[int] | None = None) -> Any:
    if depth > MAX_PAYLOAD_DEPTH:
        raise ValidationError("EDGE_PAYLOAD_TOO_DEEP", "edge payload nesting exceeds the admitted bound")
    if counter is None:
        counter = [0]
    counter[0] += 1
    if counter[0] > MAX_PAYLOAD_ITEMS:
        raise ValidationError("EDGE_PAYLOAD_TOO_LARGE", "edge payload item count exceeds the admitted bound")
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload keys must be strings")
            try:
                encoded = key.encode("utf-8", "strict")
            except UnicodeEncodeError as exc:
                raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload key is not valid UTF-8") from exc
            if len(encoded) > MAX_METADATA_FRAME_BYTES:
                raise ValidationError("EDGE_PAYLOAD_TOO_LARGE", "edge payload key exceeds the admitted bound")
            result[key] = _snapshot_payload(child, depth=depth + 1, counter=counter)
        return result
    if isinstance(value, (list, tuple)):
        return [_snapshot_payload(child, depth=depth + 1, counter=counter) for child in value]
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload integer exceeds the safe range")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload float must be finite")
        return value
    if isinstance(value, str):
        try:
            encoded = value.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload string is not valid UTF-8") from exc
        if len(encoded) > MAX_METADATA_FRAME_BYTES:
            raise ValidationError("EDGE_PAYLOAD_TOO_LARGE", "edge payload string exceeds the admitted bound")
        return value
    raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload contains an unsupported value")


def _reject_control_surface(value: Any, *, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValidationError("EDGE_PAYLOAD_INVALID", "edge payload keys must be strings")
            normalized = re.sub(
                r"[^a-z0-9]+",
                "_",
                unicodedata.normalize("NFKC", key).casefold(),
            ).strip("_")
            if normalized in _FORBIDDEN_CONTROL_KEYS:
                raise ValidationError(
                    "EDGE_CONTROL_SURFACE_REJECTED",
                    f"forbidden remote control surface at {path}.{key}",
                )
            _reject_control_surface(child, path=f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_control_surface(child, path=f"{path}[{index}]")


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError("EDGE_FRAME_DUPLICATE_KEY", "duplicate JSON key is forbidden")
        result[key] = value
    return result


class EdgeFrameKind(str, Enum):
    HELLO = "HELLO"
    HELLO_ACK = "HELLO_ACK"
    HEARTBEAT = "HEARTBEAT"
    OBSERVATION = "OBSERVATION"
    ARTIFACT = "ARTIFACT"


def _auth_key(value: bytes, field: str) -> bytes:
    if not isinstance(value, bytes) or len(value) < MIN_AUTH_KEY_BYTES:
        raise ValidationError("EDGE_AUTH_KEY_INVALID", f"{field} must contain at least 32 bytes")
    return bytes(value)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(child) for key, child in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(child) for child in value)
    return value


def _canonical_unsigned(value: Mapping[str, Any]) -> bytes:
    return jcs_dumps(value).encode("utf-8")


@dataclass(frozen=True)
class EdgeArtifactDescriptor:
    ref: str
    sha256: str
    size_bytes: int
    media_type: str

    def as_mapping(self) -> dict[str, Any]:
        return {
            "schema": EDGE_ARTIFACT_SCHEMA,
            "ref": self.ref,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "media_type": self.media_type,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> EdgeArtifactDescriptor:
        if not isinstance(value, Mapping):
            raise ValidationError("EDGE_ARTIFACT_DESCRIPTOR_INVALID", "artifact descriptor must be an object")
        require_exact_keys(value, ("schema", "ref", "sha256", "size_bytes", "media_type"))
        if value["schema"] != EDGE_ARTIFACT_SCHEMA:
            raise ValidationError("EDGE_ARTIFACT_DESCRIPTOR_INVALID", "artifact descriptor schema is not supported")
        digest = value["sha256"]
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValidationError("EDGE_ARTIFACT_DESCRIPTOR_INVALID", "artifact descriptor hash is invalid")
        ref = value["ref"]
        if ref != f"sha256:{digest}":
            raise ValidationError("EDGE_ARTIFACT_DESCRIPTOR_INVALID", "artifact descriptor ref does not match hash")
        size = checked_non_negative(value["size_bytes"], maximum=MAX_SAFE_INTEGER, field_name="size_bytes")
        if size > MAX_ARTIFACT_BYTES:
            raise ValidationError("EDGE_ARTIFACT_TOO_LARGE", "artifact exceeds the admitted size bound")
        try:
            media_type = _validate_media_type(value["media_type"])
        except ValidationError as exc:
            raise ValidationError(
                "EDGE_ARTIFACT_DESCRIPTOR_INVALID",
                "artifact descriptor media type is invalid",
            ) from exc
        return cls(ref=ref, sha256=digest, size_bytes=size, media_type=media_type)


def describe_artifact(data: bytes, *, media_type: str) -> EdgeArtifactDescriptor:
    if not isinstance(data, bytes):
        raise ValidationError("EDGE_ARTIFACT_INVALID", "artifact bytes must be bytes")
    if len(data) > MAX_ARTIFACT_BYTES:
        raise ValidationError("EDGE_ARTIFACT_TOO_LARGE", "artifact exceeds the admitted size bound")
    media_type = _validate_media_type(media_type)
    digest = hashlib.sha256(data).hexdigest()
    return EdgeArtifactDescriptor(
        ref=f"sha256:{digest}",
        sha256=digest,
        size_bytes=len(data),
        media_type=media_type,
    )


def verify_artifact_bytes(descriptor: EdgeArtifactDescriptor, data: bytes) -> bytes:
    if not isinstance(descriptor, EdgeArtifactDescriptor) or not isinstance(data, bytes):
        raise ValidationError("EDGE_ARTIFACT_INVALID", "artifact verification input is invalid")
    if len(data) != descriptor.size_bytes:
        raise ValidationError("EDGE_ARTIFACT_INTEGRITY_FAILED", "artifact size does not match descriptor")
    digest = hashlib.sha256(data).hexdigest()
    if not hmac.compare_digest(digest, descriptor.sha256) or descriptor.ref != f"sha256:{digest}":
        raise ValidationError("EDGE_ARTIFACT_INTEGRITY_FAILED", "artifact hash does not match descriptor")
    return bytes(data)


@dataclass(frozen=True)
class VerifiedEdgeFrame:
    kind: EdgeFrameKind
    sender_peer_id: str
    connection_id: str
    sequence: int
    sent_epoch_ms: int
    payload: Mapping[str, Any]
    peer_authenticated: bool = True
    mutation_authorized: bool = False
    physical_action_budget: int = 0
    evidence_fresh: bool = False
    action_resume_allowed: bool = False


class EdgeTransportSigner:
    def __init__(self, *, local_peer_id: str, local_auth_key: bytes) -> None:
        self.local_peer_id = validate_opaque_id(local_peer_id, field_name="local_peer_id")
        self._auth_key = _auth_key(local_auth_key, "local_auth_key")

    def __repr__(self) -> str:
        return f"EdgeTransportSigner(local_peer_id={self.local_peer_id!r}, auth_key=<redacted>)"

    def seal(
        self,
        *,
        kind: EdgeFrameKind,
        connection_id: str,
        sequence: int,
        sent_epoch_ms: int,
        payload: Mapping[str, Any],
    ) -> bytes:
        try:
            admitted_kind = EdgeFrameKind(kind)
        except (TypeError, ValueError) as exc:
            raise ValidationError("EDGE_KIND_INVALID", "edge frame kind is not admitted") from exc
        connection_id = validate_opaque_id(connection_id, field_name="connection_id")
        sequence = checked_non_negative(sequence, maximum=MAX_SAFE_INTEGER, field_name="sequence")
        if sequence < 1:
            raise ValidationError("EDGE_SEQUENCE_INVALID", "sequence must be at least one")
        sent_epoch_ms = checked_non_negative(sent_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="sent_epoch_ms")
        if not isinstance(payload, Mapping):
            raise ValidationError("EDGE_PAYLOAD_INVALID", "payload must be an object")
        payload_copy = _snapshot_payload(payload)
        _reject_control_surface(payload_copy)
        ensure_no_secret_material(payload_copy, key_path="edge.payload")
        unsigned = {
            "schema": EDGE_TRANSPORT_SCHEMA,
            "protocol_major": EDGE_TRANSPORT_PROTOCOL_MAJOR,
            "sender_peer_id": self.local_peer_id,
            "connection_id": connection_id,
            "sequence": sequence,
            "sent_epoch_ms": sent_epoch_ms,
            "kind": admitted_kind.value,
            "authority_scope": "PEER_IDENTITY_ONLY",
            "mutation_authorized": False,
            "physical_action_budget": 0,
            "evidence_fresh": False,
            "action_resume_allowed": False,
            "payload": payload_copy,
        }
        tag = hmac.new(self._auth_key, _canonical_unsigned(unsigned), hashlib.sha256).hexdigest()
        packet = jcs_dumps({**unsigned, "auth_tag": tag}).encode("utf-8")
        if len(packet) > MAX_METADATA_FRAME_BYTES:
            raise ValidationError("EDGE_FRAME_TOO_LARGE", "edge metadata frame exceeds the admitted size bound")
        return packet


class EdgeTransportVerifier:
    def __init__(
        self,
        *,
        expected_peer_id: str,
        expected_peer_auth_key: bytes,
        expected_connection_id: str | None = None,
        last_accepted_sequence: int = 0,
        max_age_ms: int = DEFAULT_MAX_AGE_MS,
        max_future_skew_ms: int = DEFAULT_MAX_FUTURE_SKEW_MS,
    ) -> None:
        self.expected_peer_id = validate_opaque_id(expected_peer_id, field_name="expected_peer_id")
        self._auth_key = _auth_key(expected_peer_auth_key, "expected_peer_auth_key")
        self._connection_id = (
            None
            if expected_connection_id is None
            else validate_opaque_id(expected_connection_id, field_name="expected_connection_id")
        )
        self._last_sequence = checked_non_negative(last_accepted_sequence, maximum=MAX_SAFE_INTEGER, field_name="last_accepted_sequence")
        self.max_age_ms = checked_non_negative(max_age_ms, maximum=MAX_SAFE_INTEGER, field_name="max_age_ms")
        self.max_future_skew_ms = checked_non_negative(max_future_skew_ms, maximum=MAX_SAFE_INTEGER, field_name="max_future_skew_ms")

    def __repr__(self) -> str:
        return f"EdgeTransportVerifier(expected_peer_id={self.expected_peer_id!r}, auth_key=<redacted>)"

    @property
    def last_accepted_sequence(self) -> int:
        return self._last_sequence

    @property
    def connection_id(self) -> str | None:
        return self._connection_id

    def bind_connection(self, connection_id: str) -> None:
        connection_id = validate_opaque_id(connection_id, field_name="connection_id")
        if self._connection_id == connection_id:
            raise ValidationError(
                "EDGE_CONNECTION_REUSE_REJECTED",
                "reusing a connection id cannot reset the replay window",
            )
        self._connection_id = connection_id
        self._last_sequence = 0

    def verify(self, packet: bytes, *, now_epoch_ms: int) -> VerifiedEdgeFrame:
        if not isinstance(packet, bytes):
            raise ValidationError("EDGE_FRAME_INVALID", "edge frame must be bytes")
        if len(packet) > MAX_METADATA_FRAME_BYTES:
            raise ValidationError("EDGE_FRAME_TOO_LARGE", "edge metadata frame exceeds the admitted size bound")
        try:
            decoded = json.loads(packet.decode("utf-8", "strict"), object_pairs_hook=_no_duplicate_keys)
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
            raise ValidationError("EDGE_FRAME_INVALID", "edge frame must be valid UTF-8 JSON") from exc
        if not isinstance(decoded, dict):
            raise ValidationError("EDGE_FRAME_INVALID", "edge frame must be a JSON object")
        keys = (
            "schema", "protocol_major", "sender_peer_id", "connection_id", "sequence",
            "sent_epoch_ms", "kind", "authority_scope", "mutation_authorized",
            "physical_action_budget", "evidence_fresh", "action_resume_allowed", "payload", "auth_tag",
        )
        require_exact_keys(decoded, keys)
        if (
            decoded["schema"] != EDGE_TRANSPORT_SCHEMA
            or type(decoded["protocol_major"]) is not int
            or decoded["protocol_major"] != EDGE_TRANSPORT_PROTOCOL_MAJOR
        ):
            raise ValidationError("EDGE_VERSION_REJECTED", "edge transport schema/version is not supported")
        if decoded["sender_peer_id"] != self.expected_peer_id:
            raise ValidationError("EDGE_PEER_REJECTED", "edge transport peer identity does not match pairing")
        if (
            decoded["authority_scope"] != "PEER_IDENTITY_ONLY"
            or decoded["mutation_authorized"] is not False
            or type(decoded["physical_action_budget"]) is not int
            or decoded["physical_action_budget"] != 0
            or decoded["evidence_fresh"] is not False
            or decoded["action_resume_allowed"] is not False
        ):
            raise ValidationError("EDGE_AUTHORITY_EXPANSION_REJECTED", "transport frame attempted to expand authority")
        tag = decoded["auth_tag"]
        if not isinstance(tag, str) or len(tag) != 64:
            raise ValidationError("EDGE_AUTHENTICATION_FAILED", "edge transport authentication failed")
        unsigned = dict(decoded)
        unsigned.pop("auth_tag")
        expected = hmac.new(self._auth_key, _canonical_unsigned(unsigned), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(tag, expected):
            raise ValidationError("EDGE_AUTHENTICATION_FAILED", "edge transport authentication failed")
        sequence = checked_non_negative(decoded["sequence"], maximum=MAX_SAFE_INTEGER, field_name="sequence")
        if sequence <= self._last_sequence:
            raise ValidationError("EDGE_REPLAY_REJECTED", "edge frame sequence is not newer than accepted state")
        sent_epoch_ms = checked_non_negative(decoded["sent_epoch_ms"], maximum=MAX_SAFE_INTEGER, field_name="sent_epoch_ms")
        now_epoch_ms = checked_non_negative(now_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="now_epoch_ms")
        if sent_epoch_ms > now_epoch_ms + self.max_future_skew_ms or now_epoch_ms - sent_epoch_ms > self.max_age_ms:
            raise ValidationError("EDGE_STALE_REJECTED", "edge frame timestamp is outside the admitted freshness window")
        try:
            kind = EdgeFrameKind(decoded["kind"])
        except (TypeError, ValueError) as exc:
            raise ValidationError("EDGE_KIND_INVALID", "edge frame kind is not admitted") from exc
        payload = decoded["payload"]
        if not isinstance(payload, dict):
            raise ValidationError("EDGE_PAYLOAD_INVALID", "payload must be an object")
        payload = _snapshot_payload(payload)
        _reject_control_surface(payload)
        ensure_no_secret_material(payload, key_path="edge.payload")
        connection_id = validate_opaque_id(decoded["connection_id"], field_name="connection_id")
        if self._connection_id is None:
            self._connection_id = connection_id
        elif connection_id != self._connection_id:
            raise ValidationError("EDGE_CONNECTION_REJECTED", "edge frame belongs to a different connection")
        self._last_sequence = sequence
        return VerifiedEdgeFrame(
            kind=kind,
            sender_peer_id=self.expected_peer_id,
            connection_id=connection_id,
            sequence=sequence,
            sent_epoch_ms=sent_epoch_ms,
            payload=_freeze(payload),
        )


def _recv_exact(connection: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = connection.recv(remaining)
        if not chunk:
            raise ValidationError("EDGE_CONNECTION_CLOSED", "edge transport connection closed before a complete frame")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _send_framed(connection: socket.socket, packet: bytes) -> None:
    if not isinstance(packet, bytes) or not 1 <= len(packet) <= MAX_METADATA_FRAME_BYTES:
        raise ValidationError("EDGE_FRAME_TOO_LARGE", "edge metadata frame is outside the admitted size bound")
    connection.sendall(struct.pack("!I", len(packet)) + packet)


def _recv_framed(connection: socket.socket) -> bytes:
    header = _recv_exact(connection, 4)
    size = struct.unpack("!I", header)[0]
    if not 1 <= size <= MAX_METADATA_FRAME_BYTES:
        raise ValidationError("EDGE_FRAME_TOO_LARGE", "edge metadata frame is outside the admitted size bound")
    return _recv_exact(connection, size)


def _send_artifact_framed(connection: socket.socket, data: bytes) -> None:
    if not isinstance(data, bytes) or len(data) > MAX_ARTIFACT_BYTES:
        raise ValidationError("EDGE_ARTIFACT_TOO_LARGE", "artifact exceeds the admitted size bound")
    connection.sendall(struct.pack("!I", len(data)) + data)


def receive_artifact_bytes(
    connection: socket.socket,
    descriptor: EdgeArtifactDescriptor,
) -> bytes:
    if not isinstance(descriptor, EdgeArtifactDescriptor):
        raise ValidationError("EDGE_ARTIFACT_INVALID", "artifact descriptor is invalid")
    try:
        header = _recv_exact(connection, 4)
        size = struct.unpack("!I", header)[0]
        if size != descriptor.size_bytes:
            raise ValidationError(
                "EDGE_ARTIFACT_LENGTH_MISMATCH",
                "artifact wire length does not match its signed descriptor",
            )
        if size > MAX_ARTIFACT_BYTES:
            raise ValidationError("EDGE_ARTIFACT_TOO_LARGE", "artifact exceeds the admitted size bound")
        return verify_artifact_bytes(descriptor, _recv_exact(connection, size))
    except OSError as exc:
        raise ValidationError("EDGE_ARTIFACT_RECEIVE_FAILED", "edge artifact receive failed safely") from exc


class EdgeOutboundChannel:
    def __init__(
        self,
        *,
        connection: socket.socket,
        signer: EdgeTransportSigner,
        connection_id: str,
    ) -> None:
        self._connection = connection
        self._signer = signer
        self.connection_id = validate_opaque_id(connection_id, field_name="connection_id")
        self._next_sequence = 2
        self._closed = False
        self._send_lock = threading.RLock()
        self.peer_authenticated = True
        self.mutation_authorized = False
        self.action_resume_allowed = False
        self.evidence_fresh = False

    def send(self, kind: EdgeFrameKind, payload: Mapping[str, Any], *, sent_epoch_ms: int) -> int:
        with self._send_lock:
            if self._closed:
                raise ValidationError("EDGE_CONNECTION_CLOSED", "edge transport channel is closed")
            try:
                admitted_kind = EdgeFrameKind(kind)
            except (TypeError, ValueError) as exc:
                raise ValidationError("EDGE_KIND_INVALID", "edge frame kind is not admitted") from exc
            if admitted_kind not in {EdgeFrameKind.HEARTBEAT, EdgeFrameKind.OBSERVATION}:
                raise ValidationError("EDGE_DIRECTION_REJECTED", "post-handshake edge channel is outbound observation-only")
            sequence = self._next_sequence
            packet = self._signer.seal(
                kind=admitted_kind,
                connection_id=self.connection_id,
                sequence=sequence,
                sent_epoch_ms=sent_epoch_ms,
                payload=payload,
            )
            try:
                _send_framed(self._connection, packet)
            except OSError as exc:
                self.close()
                raise ValidationError("EDGE_SEND_FAILED", "edge transport send failed safely") from exc
            self._next_sequence += 1
            return sequence

    def send_artifact(
        self,
        data: bytes,
        *,
        media_type: str,
        sent_epoch_ms: int,
    ) -> tuple[int, EdgeArtifactDescriptor]:
        descriptor = describe_artifact(data, media_type=media_type)
        with self._send_lock:
            if self._closed:
                raise ValidationError("EDGE_CONNECTION_CLOSED", "edge transport channel is closed")
            sequence = self._next_sequence
            packet = self._signer.seal(
                kind=EdgeFrameKind.ARTIFACT,
                connection_id=self.connection_id,
                sequence=sequence,
                sent_epoch_ms=sent_epoch_ms,
                payload={"artifact": descriptor.as_mapping()},
            )
            try:
                _send_framed(self._connection, packet)
                _send_artifact_framed(self._connection, data)
            except OSError as exc:
                self.close()
                raise ValidationError("EDGE_ARTIFACT_SEND_FAILED", "edge artifact transfer failed safely") from exc
            self._next_sequence += 1
            return sequence, descriptor

    def close(self) -> None:
        with self._send_lock:
            if self._closed:
                return
            self._closed = True
            try:
                self._connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self._connection.close()


class EdgeOutboundClient:
    def __init__(
        self,
        *,
        local_peer_id: str,
        local_auth_key: bytes,
        expected_remote_peer_id: str,
        expected_remote_auth_key: bytes,
        timeout_seconds: float = 5.0,
    ) -> None:
        local_key = _auth_key(local_auth_key, "local_auth_key")
        remote_key = _auth_key(expected_remote_auth_key, "expected_remote_auth_key")
        if hmac.compare_digest(local_key, remote_key):
            raise ValidationError(
                "EDGE_PAIRING_KEY_REUSE_REJECTED",
                "mutual authentication requires distinct directional pairing keys",
            )
        self._signer = EdgeTransportSigner(
            local_peer_id=local_peer_id,
            local_auth_key=local_key,
        )
        self.expected_remote_peer_id = validate_opaque_id(
            expected_remote_peer_id,
            field_name="expected_remote_peer_id",
        )
        self._remote_key = remote_key
        if (
            isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(float(timeout_seconds))
            or timeout_seconds <= 0
            or timeout_seconds > 30
        ):
            raise ValidationError("EDGE_TIMEOUT_INVALID", "edge transport timeout must be in (0, 30] seconds")
        self.timeout_seconds = float(timeout_seconds)

    def __repr__(self) -> str:
        return (
            "EdgeOutboundClient("
            f"local_peer_id={self._signer.local_peer_id!r}, "
            f"expected_remote_peer_id={self.expected_remote_peer_id!r}, auth_keys=<redacted>)"
        )

    def connect(self, host: str, port: int, *, now_epoch_ms: int) -> EdgeOutboundChannel:
        resolved_host = resolve_edge_endpoint(host, port)
        now_epoch_ms = checked_non_negative(now_epoch_ms, maximum=MAX_SAFE_INTEGER, field_name="now_epoch_ms")
        connection_id = f"edge-{secrets.token_hex(16)}"
        try:
            connection = socket.create_connection((resolved_host, port), timeout=self.timeout_seconds)
            connection.settimeout(self.timeout_seconds)
        except OSError as exc:
            raise ValidationError("EDGE_CONNECT_FAILED", "outbound edge transport connection failed safely") from exc
        try:
            hello = self._signer.seal(
                kind=EdgeFrameKind.HELLO,
                connection_id=connection_id,
                sequence=1,
                sent_epoch_ms=now_epoch_ms,
                payload={"transport_mode": "OUTBOUND_ONLY", "role": "RUNTIME_EDGE"},
            )
            _send_framed(connection, hello)
            verifier = EdgeTransportVerifier(
                expected_peer_id=self.expected_remote_peer_id,
                expected_peer_auth_key=self._remote_key,
                expected_connection_id=connection_id,
            )
            acknowledged = verifier.verify(_recv_framed(connection), now_epoch_ms=now_epoch_ms)
            if acknowledged.kind != EdgeFrameKind.HELLO_ACK:
                raise ValidationError("EDGE_HANDSHAKE_REJECTED", "edge transport peer did not return HELLO_ACK")
            payload = acknowledged.payload
            require_exact_keys(payload, ("acknowledged_peer_id", "transport_mode"))
            if payload["acknowledged_peer_id"] != self._signer.local_peer_id or payload["transport_mode"] != "OUTBOUND_ONLY":
                raise ValidationError("EDGE_HANDSHAKE_REJECTED", "edge transport peer acknowledgement does not match pairing")
            return EdgeOutboundChannel(
                connection=connection,
                signer=self._signer,
                connection_id=connection_id,
            )
        except (OSError, ValidationError):
            try:
                connection.close()
            finally:
                pass
            raise
