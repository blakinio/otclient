#!/usr/bin/env python3
"""Pure fail-closed XRes 1.2 wire encoder/parser.

This module intentionally performs no I/O. The caller is responsible for core
QueryExtension discovery, transport, authentication and request sequencing.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

XRES_PROTOCOL_MAJOR = 1
XRES_PROTOCOL_MINOR = 2
XRES_QUERY_VERSION = 0
XRES_QUERY_CLIENT_IDS = 4
XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID = 0x02
X11_REPLY = 1
XRES_QUERY_VERSION_REQUEST_SIZE = 8
XRES_QUERY_VERSION_REPLY_SIZE = 32
XRES_QUERY_CLIENT_IDS_FIXED_REQUEST_SIZE = 8
XRES_QUERY_CLIENT_IDS_REPLY_SIZE = 32
XRES_CLIENT_ID_SPEC_SIZE = 8
XRES_CLIENT_ID_VALUE_FIXED_SIZE = 12
DEFAULT_MAX_REPLY_BYTES = 4096
DEFAULT_MAX_IDS = 64
DEFAULT_MAX_VALUES_PER_ID = 64


class XResWireError(ValueError):
    """Raised when a value or XRes wire message fails strict validation."""


@dataclass(frozen=True)
class QueryVersionReply:
    sequence: int
    server_major: int
    server_minor: int


@dataclass(frozen=True)
class ClientIdValue:
    client: int
    mask: int
    values: tuple[int, ...]


def _endian(byte_order: str) -> str:
    if byte_order == "little":
        return "<"
    if byte_order == "big":
        return ">"
    raise XResWireError(f"unsupported byte order: {byte_order!r}")


def _uint(value: int, bits: int, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise XResWireError(f"{field} must be an integer")
    maximum = (1 << bits) - 1
    if not 0 <= value <= maximum:
        raise XResWireError(f"{field} must fit uint{bits}")
    return value


def _extension_major_opcode(value: int) -> int:
    value = _uint(value, 8, "extension major opcode")
    if value < 128:
        raise XResWireError("extension major opcode must be in the X11 extension range")
    return value


def _expected_sequence(value: int | None) -> int | None:
    if value is None:
        return None
    return _uint(value, 16, "expected sequence")


def encode_query_version(major_opcode: int, byte_order: str) -> bytes:
    """Encode XRes QueryVersion(1, 2), without performing transport I/O."""

    prefix = _endian(byte_order)
    opcode = _extension_major_opcode(major_opcode)
    request = struct.pack(
        prefix + "BBHBBH",
        opcode,
        XRES_QUERY_VERSION,
        XRES_QUERY_VERSION_REQUEST_SIZE // 4,
        XRES_PROTOCOL_MAJOR,
        XRES_PROTOCOL_MINOR,
        0,
    )
    if len(request) != XRES_QUERY_VERSION_REQUEST_SIZE:
        raise AssertionError("internal QueryVersion size mismatch")
    return request


def parse_query_version_reply(
    data: bytes,
    byte_order: str,
    *,
    expected_sequence: int | None = None,
) -> QueryVersionReply:
    """Parse an exact fixed-size XRes QueryVersion reply."""

    prefix = _endian(byte_order)
    expected = _expected_sequence(expected_sequence)
    if not isinstance(data, bytes):
        raise XResWireError("QueryVersion reply must be bytes")
    if len(data) != XRES_QUERY_VERSION_REPLY_SIZE:
        raise XResWireError("QueryVersion reply must be exactly 32 bytes")
    response_type, _pad, sequence, length_words, server_major, server_minor, _padding = (
        struct.unpack(prefix + "BBHIHH20s", data)
    )
    if response_type != X11_REPLY:
        raise XResWireError("QueryVersion response is not an X11 reply")
    if length_words != 0:
        raise XResWireError("QueryVersion reply declared unexpected trailing payload")
    if expected is not None and sequence != expected:
        raise XResWireError("QueryVersion sequence mismatch")
    return QueryVersionReply(sequence, server_major, server_minor)


def require_xres_1_2(reply: QueryVersionReply) -> None:
    """Fail closed unless the server reports XRes >= 1.2."""

    if not isinstance(reply, QueryVersionReply):
        raise XResWireError("expected a QueryVersionReply")
    if (reply.server_major, reply.server_minor) < (
        XRES_PROTOCOL_MAJOR,
        XRES_PROTOCOL_MINOR,
    ):
        raise XResWireError("XRes server version is below 1.2")


def encode_query_client_ids(
    major_opcode: int,
    resource_xid: int,
    byte_order: str,
) -> bytes:
    """Encode one QueryClientIds spec requesting LocalClientPid for an XID."""

    prefix = _endian(byte_order)
    opcode = _extension_major_opcode(major_opcode)
    xid = _uint(resource_xid, 32, "resource XID")
    if xid == 0:
        raise XResWireError("resource XID must be nonzero")
    request = struct.pack(
        prefix + "BBHI",
        opcode,
        XRES_QUERY_CLIENT_IDS,
        (XRES_QUERY_CLIENT_IDS_FIXED_REQUEST_SIZE + XRES_CLIENT_ID_SPEC_SIZE) // 4,
        1,
    ) + struct.pack(prefix + "II", xid, XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID)
    if len(request) != XRES_QUERY_CLIENT_IDS_FIXED_REQUEST_SIZE + XRES_CLIENT_ID_SPEC_SIZE:
        raise AssertionError("internal QueryClientIds size mismatch")
    return request


def parse_query_client_ids_reply(
    data: bytes,
    byte_order: str,
    *,
    expected_sequence: int | None = None,
    max_reply_bytes: int = DEFAULT_MAX_REPLY_BYTES,
    max_ids: int = DEFAULT_MAX_IDS,
    max_values_per_id: int = DEFAULT_MAX_VALUES_PER_ID,
) -> tuple[ClientIdValue, ...]:
    """Parse a bounded XRes QueryClientIds reply into immutable records.

    XRes 1.2's CLIENTIDVALUE.length field is a byte count. In particular,
    LocalClientPid uses length=4 followed by exactly one CARD32 PID. Keep the
    public limit expressed in CARD32 values while validating the wire byte count
    is naturally aligned before unpacking.
    """

    prefix = _endian(byte_order)
    expected = _expected_sequence(expected_sequence)
    if not isinstance(data, bytes):
        raise XResWireError("QueryClientIds reply must be bytes")
    _uint(max_reply_bytes, 32, "max reply bytes")
    _uint(max_ids, 32, "max ids")
    _uint(max_values_per_id, 32, "max values per id")
    if max_reply_bytes < XRES_QUERY_CLIENT_IDS_REPLY_SIZE:
        raise XResWireError("max reply bytes is below fixed reply size")
    if max_ids == 0 or max_values_per_id == 0:
        raise XResWireError("parser limits must be positive")
    if len(data) < XRES_QUERY_CLIENT_IDS_REPLY_SIZE:
        raise XResWireError("QueryClientIds reply is truncated")
    if len(data) > max_reply_bytes:
        raise XResWireError("QueryClientIds reply exceeds configured size cap")

    response_type, _pad, sequence, length_words, num_ids, _padding = struct.unpack_from(
        prefix + "BBHII20s", data, 0
    )
    if response_type != X11_REPLY:
        raise XResWireError("QueryClientIds response is not an X11 reply")
    if expected is not None and sequence != expected:
        raise XResWireError("QueryClientIds sequence mismatch")
    if num_ids > max_ids:
        raise XResWireError("QueryClientIds id count exceeds configured cap")

    declared_size = XRES_QUERY_CLIENT_IDS_REPLY_SIZE + length_words * 4
    if declared_size != len(data):
        raise XResWireError("QueryClientIds declared length does not match bytes received")

    offset = XRES_QUERY_CLIENT_IDS_REPLY_SIZE
    records: list[ClientIdValue] = []
    for _ in range(num_ids):
        if offset + XRES_CLIENT_ID_VALUE_FIXED_SIZE > len(data):
            raise XResWireError("QueryClientIds client-id record is truncated")
        client, mask, value_length_bytes = struct.unpack_from(prefix + "III", data, offset)
        if value_length_bytes % 4 != 0:
            raise XResWireError("QueryClientIds client-id value byte length is not CARD32 aligned")
        value_count = value_length_bytes // 4
        if value_count > max_values_per_id:
            raise XResWireError("QueryClientIds value count exceeds configured cap")
        end = offset + XRES_CLIENT_ID_VALUE_FIXED_SIZE + value_length_bytes
        if end > len(data):
            raise XResWireError("QueryClientIds client-id value payload is truncated")
        values = (
            tuple(struct.unpack_from(prefix + f"{value_count}I", data, offset + 12))
            if value_count
            else ()
        )
        records.append(ClientIdValue(client, mask, values))
        offset = end

    if offset != len(data):
        raise XResWireError("QueryClientIds reply contains unparsed trailing payload")
    return tuple(records)


def extract_local_client_pid(
    records: tuple[ClientIdValue, ...],
    resource_xid: int,
) -> int | None:
    """Return one unambiguous LocalClientPid for the requested one-spec query."""

    xid = _uint(resource_xid, 32, "resource XID")
    if xid == 0:
        raise XResWireError("resource XID must be nonzero")
    if not isinstance(records, tuple) or not all(isinstance(item, ClientIdValue) for item in records):
        raise XResWireError("records must be a tuple of ClientIdValue objects")
    if not records:
        return None
    if len(records) != 1:
        raise XResWireError("one-spec QueryClientIds reply must contain exactly one record")

    record = records[0]
    if record.client != xid:
        raise XResWireError("QueryClientIds reply did not identify the requested resource")
    if record.mask != XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID:
        raise XResWireError("QueryClientIds target record returned an unexpected mask")
    if len(record.values) != 1:
        raise XResWireError("LocalClientPid record must contain exactly one CARD32 value")
    pid = record.values[0]
    if pid == 0:
        raise XResWireError("LocalClientPid must be positive")
    return pid
