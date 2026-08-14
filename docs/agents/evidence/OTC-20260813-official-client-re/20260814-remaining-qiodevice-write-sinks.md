# Track A — remaining direct QIODevice write sinks

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Classify the remaining exact-client direct calls to `QIODevice::write(QByteArray const&)@plt` after the QBuffer helper at `0xb40630` and QFile path at `0xd085e0` were excluded from final game-socket sink candidates.

## Exact run — PROVEN

Workflow:

```text
.github/workflows/tibia-official-client-re-remaining-write-sinks.yml
```

Run/job:

```yaml
run_id: 31827692106
job_id: 94855632121
head: 6bc1c54650fc41c36587bb83705076ac90fc485e
result: SUCCESS
runner: synology-otclient-01
```

Artifact:

```yaml
name: track-a-remaining-write-sinks-31827692106
artifact_id: 9229441999
zip_sha256: a4ca736215b6c8a8377ffd335cdb2916b526be5d41483e7bb68617ff31a3fe29
```

## Imported Qt write/network surface — PROVEN

The full relocation/PLT inventory found these directly imported socket/write-relevant Qt surfaces:

```text
QAbstractSocket::errorOccurred(QAbstractSocket::SocketError)
QAbstractSocket::staticMetaObject
QAbstractSocket::connected()
QAbstractSocket::disconnected()
QTcpSocket::QTcpSocket(QObject*)@plt = 0x4ddbc0
QIODevice::write(QByteArray const&)@plt = 0x4de370
QAbstractSocket::state() const@plt = 0x4def50
```

No separately imported `QAbstractSocket::writeData`, `QTcpSocket` write overload, or `QSslSocket` write surface was emitted by this exact scan. This is a bounded import-surface fact; local wrappers and indirect virtual dispatch remain possible.

## Candidate A — QBuffer-family path — DISPROVEN AS FINAL SOCKET SINK

FDE:

```text
0x7dd3f0..0x7dd62d
```

Exact sequence identifies the same QBuffer-derived object family already proven around `0xb40630`:

```asm
0x7dd500  mov rdx,[r12]
0x7dd504  mov rdx,[rdx+0xe8]
0x7dd51e  lea rax,[rip+...]      # 0xb40630
0x7dd525  cmp rdx,rax
0x7dd53a  call [vptr+0x78]
0x7dd54e  call QBuffer::buffer()@plt
0x7dd55a  call [vptr+0x88]
0x7dd560  mov rdi,r12
0x7dd563  call QIODevice::write(QByteArray const&)@plt
0x7dd572  call [vptr+0x88]
```

The independently proven QBuffer-derived table has `+0xe8 -> 0xb40630`. Candidate A explicitly checks for that exact slot and calls `QBuffer::buffer()` before the direct QIODevice write. Therefore Candidate A is another operation on the in-memory QBuffer-derived family, not the final game socket writer.

## Candidate D — QNetworkReply-to-file path — DISPROVEN AS FINAL SOCKET SINK

FDE:

```text
0xc49ee0..0xc4a9e5
```

Exact disassembly shows an HTTP/network-reply consumption/download path:

```text
[this+0x220] -> QNetworkReply/QIODevice
QNetworkReply::error()
QNetworkReply::isFinished()
QIODevice::read(...)
```

When response bytes are available the function writes them to the embedded device at `[this+0x328]` and immediately flushes it:

```asm
0xc4a83b  lea rbp,[rbx+0x328]
0xc4a842  mov rsi,r12             # QByteArray read from QNetworkReply
0xc4a845  mov rdi,rbp
0xc4a848  call QIODevice::write(QByteArray const&)@plt
0xc4a84d  mov rdi,rbp
0xc4a850  call QFileDevice::flush()@plt
```

The same function is rich in `QDateTime`, `QLocale`, `QString`, `QMessageLogger`, timer, and QNetworkReply operations. The direct write is therefore a network-download/read-to-file-device path, not an outbound game socket write.

## Candidate C — only remaining direct-write candidate — ROLE UNKNOWN

FDE:

```text
0xb46bd0..0xb46cce
```

Exact sequence:

```asm
r12 = [this+0x10]
call [r12->vtable+0x120] with QVariant(0)
call [r12->vtable+0x120] with QVariant(1)
QMetaObject::activate(this, metaobject=0x30b7d00, signal_index=0, ...)
QString::toLocal8Bit_helper([this+0x28], [this+0x30])
QByteArray::append('\n')
rdi = [this+0x10]
rsi = generated QByteArray
call QIODevice::write(QByteArray const&)@plt at 0xb46c75
```

This is structurally a newline-terminated text emitter to a QIODevice stored at `[this+0x10]`. That shape is inconsistent with an obvious binary game packet writer, but that semantic exclusion is not yet proven. The exact QObject/QMeta class at `0x30b7d00` and the concrete device type stored at `[this+0x10]` must be recovered before Candidate C is eliminated.

## Direct-write survivor set

After the exact classifications now available:

```yaml
0x7dd3f0: DISPROVEN_FINAL_SOCKET_SINK   # QBuffer family
0xb40630: DISPROVEN_FINAL_SOCKET_SINK   # QBuffer-derived helper
0xb46bd0: UNKNOWN                       # newline text emitter, device unresolved
0xc49ee0: DISPROVEN_FINAL_SOCKET_SINK   # QNetworkReply -> QFileDevice flush
0xd085e0: DISPROVEN_FINAL_SOCKET_SINK   # explicit QFile path
```

Thus `0xb46bd0` is the only direct `QIODevice::write(QByteArray const&)` function not yet excluded.

## Proof boundary

### FACT

- Candidate A belongs to the same QBuffer-derived family as `0xb40630` and is not the final game socket sink.
- Candidate D reads from a QNetworkReply and writes/flushed data through a QFileDevice path; it is not the final outbound game socket sink.
- Candidate C converts QString to local 8-bit text, appends newline, emits a Qt signal, and writes the result to `[this+0x10]`.
- Candidate C is the sole unclassified direct callsite family remaining from the exact five-site `QIODevice::write(QByteArray const&)` census.

### UNKNOWN

- QObject/QMeta class represented by `0x30b7d00`;
- concrete QIODevice class stored at Candidate C `[this+0x10]`;
- whether Candidate C is logging/console/process text or any network-facing text protocol;
- whether the official game socket uses the imported QByteArray write directly at all;
- indirect socket writer/framing target downstream of the canonical Track A owner/subobject path.

## Next action

Perform one exact-SHA static classification of Candidate C: decode the QMeta object/string table around `0x30b7d00`, enumerate its relocation references and methods/signals, recover constructor/destructor provenance for the object around `0xb46bd0`, and trace all writes/initialization of member `[this+0x10]`. If that device is proven to be a file/console/log/process/text sink, eliminate Candidate C and promote the conclusion that none of the five direct `QIODevice::write(QByteArray const&)` callsite families is the final game socket writer. Then pivot to `QTcpSocket::QTcpSocket(QObject*)@plt` object provenance and indirect virtual write dispatch on the canonical game-session/network-owner path.