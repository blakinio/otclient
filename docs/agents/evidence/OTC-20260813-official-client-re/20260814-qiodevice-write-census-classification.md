# Track A — direct `QIODevice::write(QByteArray)` census classification

Date: 2026-08-14
Track: `official-client-re`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

Source runs:

- `31820898528` / artifact `9226904862`
- `31821085647` / artifact `9226966960`

The second run fixed the GDB environment and provides the authoritative disassembly neighborhoods used below.

## FACT — exact direct-call census for one overload

The exact ELF has five direct calls to the imported overload:

`QIODevice::write(QByteArray const&) @ 0x4de370`

Callsites:

- `0x7dd563`
- `0xb4066b`
- `0xb46c75`
- `0xc4a848`
- `0xd08642`

This census applies only to that specific `QByteArray const&` overload. It is not a census of every possible device/socket write path.

## FACT — `0xb46c75` is a text-line writer, not binary gameplay framing

The containing function begins at `0xb46bd0`. Before the write it:

1. accesses a QIODevice-like object at `[this+0x10]`;
2. uses Qt property/meta calls through that object;
3. emits `QMetaObject::activate` using metaobject `0x30b7d00`;
4. converts a `QString` held at `[this+0x28]/[this+0x30]` with `QString::toLocal8Bit_helper`;
5. appends byte `0x0a` (`'\n'`) to the resulting `QByteArray`;
6. calls `QIODevice::write(QByteArray const&)` at `0xb46c75`.

Therefore the payload passed at `0xb46c75` is a newline-terminated local-8-bit text representation of a QString. This does not match the already recovered binary GameclientMessage / packet transformation path and must not be promoted as the gameplay socket write.

The concrete class name of the containing object is not claimed here without RTTI/vtable provenance.

## FACT — other already-classified direct calls

- `0xb4066b` belongs to `tibia::network::TUnencryptedRawMessageStream::+0xe8 @ 0xb40630`, a `QBuffer`-derived in-memory raw-message stream operation.
- `0x7dd563` belongs to the server/read-side transport cluster and is not the corrected outbound `clientMessageReadyToProcess` path.
- `0xc4a848` and `0xd08642` were classified by their surrounding disassembly as file-oriented I/O rather than gameplay socket output.

## DERIVED

All five direct calls to the **specific** `QIODevice::write(QByteArray const&)` import now have evidence against treating them as the final outbound gameplay socket write.

This strongly suggests that the final network send uses one of the following instead:

- another QIODevice write overload, such as raw pointer + length;
- a concrete/virtual `writeData` path on `QAbstractSocket`/`QTcpSocket`;
- a helper that reaches the socket through a virtual device interface without a direct call to the `QByteArray` overload.

This is a search-direction conclusion, not proof of which alternative is used.

## Next action

Resolve `tibia::network::TGameserverTCPConnection` and the writer/device types traversed from `TGameserverDualConnection`, then inventory **all** imported QIODevice/QAbstractSocket write-related methods and concrete virtual write targets. Follow the object identity, not the previously incomplete single-overload census.
