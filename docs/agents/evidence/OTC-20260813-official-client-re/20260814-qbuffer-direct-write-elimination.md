# Track A — QBuffer direct-write family elimination

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Classify the direct `QIODevice::write(QByteArray const&)` candidate at `0xb40630` and determine whether it can serve as the official game-socket write sink.

## Exact experiment — PROVEN

Workflow:

```text
.github/workflows/tibia-official-client-re-writer-family-provenance.yml
```

Run/job:

```yaml
run_id: 31827431247
job_id: 94854741604
head: a55172d55514bfff8b0c44256a984868684d804b
inspect_result: SUCCESS
runner: synology-otclient-01
```

Artifact:

```yaml
name: track-a-writer-family-provenance-31827431247
artifact_id: 9229361853
zip_sha256: 2a59b7cdd12cf90584c19070fb4fd1b956d4e0d870b04c598506175d788707bc
```

## Full relocation classification — PROVEN

The full `.rela.*` view resolves the surrounding table as a QBuffer-derived vtable family. Relevant entries include:

```text
0x3084c58 -> QBuffer::metaObject() const
0x3084c60 -> QBuffer::qt_metacast(char const*)
0x3084c68 -> QBuffer::qt_metacall(...)
0x3084c70 -> 0x7dcbd0
0x3084c78 -> 0x7dcbe0
0x3084c80 -> QObject::event(QEvent*)
0x3084c88 -> QObject::eventFilter(...)
0x3084c90 -> QObject::timerEvent(...)
...
0x3084cb8 -> QIODevice::isSequential() const
0x3084cc0 -> QBuffer::open(...)
0x3084cc8 -> QBuffer::close()
0x3084cd0 -> QBuffer::pos() const
0x3084cd8 -> QBuffer::size() const
0x3084ce0 -> QBuffer::seek(long long)
0x3084ce8 -> QBuffer::atEnd() const
0x3084cf0 -> QIODevice::reset()
0x3084cf8 -> QIODevice::bytesAvailable() const
0x3084d00 -> QIODevice::bytesToWrite() const
0x3084d08 -> QBuffer::canReadLine() const
0x3084d10 -> QIODevice::waitForReadyRead(int)
0x3084d18 -> QIODevice::waitForBytesWritten(int)
0x3084d20 -> QBuffer::readData(char*, long long)
0x3084d28 -> QIODevice::readLineData(char*, long long)
0x3084d30 -> QIODevice::skipData(long long)
0x3084d38 -> QBuffer::writeData(char const*, long long)
0x3084d40 -> 0xb40630
0x3084d48 -> 0xb40690
0x3084d50 -> 0xb40710
```

The earlier arithmetic candidate `0x3084c70` was therefore not the beginning of this QObject/QBuffer virtual table. The functional address point used by the object's virtual dispatch is `0x3084c58`; `0xb40630`, `0xb40690`, and `0xb40710` occur after the inherited QBuffer/QIODevice virtuals at offsets `+0xe8`, `+0xf0`, and `+0xf8` from that address point.

## Destructor proof — PROVEN

Exact FDEs:

```text
0x7dcbd0..0x7dcbdf
0x7dcbe0..0x7dcc01
```

Both explicitly restore the vptr to `0x3084c58` before delegating to the imported `QBuffer` destructor. For example:

```asm
0x7dcbd0: lea rax,[rip+...] # 0x3084c58
0x7dcbd7: mov [rdi],rax
0x7dcbda: jmp QBuffer::~QBuffer()@plt
```

This independently confirms that `0x3084c58` is the relevant QBuffer-derived virtual-dispatch address for this local class/family.

## `0xb40630` semantics — PROVEN

Exact FDE: `0xb40630..0xb4068c`.

Key sequence:

```asm
mov rbx,rdi                 # preserve this
mov rax,[rdi]
call [rax+0x78]
...
mov r13,[rax+0x88]
call QBuffer::buffer()@plt
...
call r13
mov rsi,r12
mov rdi,rbx
call QIODevice::write(QByteArray const&)@plt
...
jmp [vptr+0x88]
```

The `QIODevice::write` receiver is the same `rbx == this` whose vptr belongs to the QBuffer-derived table above. That table inherits `QBuffer::writeData` at `0x3084d38`.

Therefore the direct `QIODevice::write` in `0xb40630` writes through a QBuffer-derived QIODevice, i.e. an in-memory QByteArray buffer path. It is **not** the final network/socket write for the official game connection.

Sibling methods reinforce the same classification:

```text
0xb40690..0xb40703 -> repeatedly uses QBuffer::buffer(), QByteArray::remove(), and seek-like virtual operations
0xb40710..0xb4071e -> QIODevice::readAll() on the same object family
```

## Corrected classification

### FACT

- the `0xb40630` family is QBuffer-derived;
- `0xb40630` invokes `QIODevice::write(QByteArray const&)` on that QBuffer-derived `this` object;
- its inherited virtual writer is `QBuffer::writeData`;
- the family is an in-memory buffer path rather than a concrete network-socket sink.

### DISPROVEN

- `0xb40630` is the official final game `QTcpSocket`/network write sink;
- the table address point relevant to this family begins at `0x3084c70`;
- a direct `QIODevice::write` call is sufficient evidence of a network write without classifying the receiver QIODevice.

### UNKNOWN

- exact local C++ class name of the QBuffer-derived helper (its RTTI object can be decoded separately if useful);
- which of the remaining direct QIODevice-write callers is network-related;
- whether the eventual game-socket writer calls `QIODevice::write(QByteArray const&)` directly or reaches `QAbstractSocket`/`QTcpSocket` through another overload/virtual writeData path;
- exact framing/serializer boundary downstream of canonical `0xb5b880`.

## Next action

Remove `0xb40630` from final-socket candidates. Classify the remaining direct `QIODevice::write(QByteArray const&)` callers `0x7dd3f0`, `0xb46bd0`, and `0xc49ee0` (with `0xd085e0` already excluded as QFile) by receiver type/vtable and caller provenance. In parallel enumerate all imported/relocated Qt network-write surfaces (`QIODevice::write` overloads, `QAbstractSocket`/`QTcpSocket`/`QSslSocket` write-related methods and virtual `writeData`) so the final sink search is not artificially limited to one QByteArray overload.