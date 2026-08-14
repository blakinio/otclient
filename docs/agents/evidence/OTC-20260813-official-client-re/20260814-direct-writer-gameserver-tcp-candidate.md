# Track A — direct writer Gameserver TCP candidate

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Preserve the exact evidence that changed the classification of the last unexcluded direct `QIODevice::write(QByteArray const&)` caller (`0xb46bd0`). Earlier structural shape suggested a generic newline-oriented text writer; the QMeta/stringdata provenance makes that heuristic insufficient and elevates the function to a high-priority gameserver network candidate until its concrete socket member is resolved.

## Exact experiment — PROVEN

Workflow:

```text
.github/workflows/tibia-official-client-re-text-writer-provenance.yml
```

Run/job:

```yaml
run_id: 31827951737
job_id: 94856503248
head: 9e11f3a7f7712df7f9de28221b84437ee1b4def1
result: SUCCESS
runner: synology-otclient-01
```

Artifact:

```yaml
name: track-a-text-writer-provenance-31827951737
artifact_id: 9229547119
zip_sha256: 64b3bc0cb6d1682bbc0e80b2f2be98e6217beb2dc1b0c9a92b220551cf133b59
```

## QMetaObject structure at `0x30b7d00` — PROVEN

The exact relocation window proves that `0x30b7d00` begins a local QObject-derived QMetaObject:

```text
0x30b7d00 R_X86_64_64 QObject::staticMetaObject@Qt_6
0x30b7d08 R_X86_64_RELATIVE 0x1d4d2b0
0x30b7d10 R_X86_64_RELATIVE 0x1d4d1a0
0x30b7d18 R_X86_64_RELATIVE 0xdd1cc0
0x30b7d28 R_X86_64_RELATIVE 0x30b7720
```

Under the Qt 6 QMetaObject data layout this is structurally consistent with:

```text
superdata          -> QObject::staticMetaObject
stringdata         -> 0x1d4d2b0
metadata           -> 0x1d4d1a0
static_metacall    -> 0xdd1cc0
related/meta-types -> local table 0x30b7720
```

The final semantic class identity is being independently revalidated by a dedicated follow-up experiment before promotion as an exact decoded QMeta class.

## Stringdata neighborhood — PROVEN

The bounded exact-client stringdata region contains the following coherent gameserver networking vocabulary adjacent to the QMeta pointers:

```text
tibia::network::TGameserverNetworkPacketConnection
connected
disconnected
error
ErrorDescription
packetReceived
TGameserverNetworkPacket
NetworkPacket
onConnected
onDisconnected
onError
onPacketReceived
QAbstractSocket::SocketError
tibia::network::TGameserverTCPConnection
connected
disconnected
error
ErrorDescription
readyRead
onConnected
onError
QAbstractSocket::SocketError
SocketError
onReadyRead
```

This is not a generic global string search: the strings occur in the bounded region surrounding the exact QMeta stringdata/data pointers used by `0x30b7d00`.

## Candidate writer path — PROVEN

Exact FDE:

```text
0xb46bd0..0xb46cce
```

Key behavior:

```asm
r12 = [this+0x10]
call [r12->vtable+0x120] using QVariant(0)
call [r12->vtable+0x120] using QVariant(1)
QMetaObject::activate(this, metaobject=0x30b7d00, signal_index=0, ...)
QString::toLocal8Bit_helper([this+0x28], [this+0x30])
QByteArray::append('\n')
rdi = [this+0x10]
rsi = generated QByteArray
call QIODevice::write(QByteArray const&)@plt at 0xb46c75
```

The exact writer therefore uses the same QObject instance that activates signal index 0 on QMetaObject `0x30b7d00`, and writes the generated QByteArray through a QIODevice pointer stored at member `+0x10`.

## Classification correction

### FACT

- run `31827951737` succeeded on the exact client;
- the QMetaObject used by `0xb46bd0` is QObject-derived and points into a gameserver-networking stringdata/metadata region;
- that region explicitly contains `tibia::network::TGameserverTCPConnection`, QAbstractSocket error type information, and TCP-style signals/slots including `readyRead`;
- `0xb46bd0` writes directly through the member at `[this+0x10]` using `QIODevice::write(QByteArray const&)`.

### SUPERSEDED INFERENCE

The earlier inference that `0xb46bd0` is probably only a logger/console writer because it converts QString to local8bit and appends newline is no longer sufficient. It must not be used to eliminate this candidate.

### UNKNOWN

- exact decoded class name corresponding specifically to QMetaObject `0x30b7d00` rather than its neighboring string tables;
- whether member `[this+0x10]` is exactly a `QTcpSocket*`, another QAbstractSocket/QIODevice subclass, or a wrapper;
- semantic meaning of the newline-terminated payload emitted by `0xb46bd0`;
- whether `0xb46bd0` itself transmits Tibia game-protocol frames or is a connection-control/proxy/handshake path on the same gameserver TCP class;
- relation of this function to canonical outbound subobject target `0xb5b880`.

## Next action

Decode `0x30b7d00` and its `qt_static_metacall @ 0xdd1cc0` as a single QMeta record, enumerate every direct `QTcpSocket::QTcpSocket(QObject*)@plt` callsite, and recover the constructor/member assignment that initializes `[this+0x10]`. Only after proving the concrete member type should `0xb46bd0` be promoted as a gameserver socket writer or split into a connection-control/text subpath. Then connect that socket owner back to the canonical Track A outbound owner/subobject path and locate the binary frame write that carries the actual game-login message.