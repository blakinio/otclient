# Track A — outgoing payload consumer provenance correction

## Experiment

- workflow: `Track A outgoing payload consumer provenance`
- workflow path: `.github/workflows/tibia-official-client-re-outgoing-payload-consumers.yml`
- head: `c15899ebef7cadb7ce6f4a302a28dff064f6b537`
- run: `31815819731`
- job: `94817115581`
- result: `SUCCESS`
- runner: `synology-otclient-01`
- artifact id: `9225203231`
- artifact name: `track-a-outgoing-payload-consumers-31815819731`
- artifact digest: `sha256:e0ca5a278d7235e1755105775ed235a4f5ee501db2e5cb473b6d008e8f9831a3`
- exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

The report completed with `TRACK_A_OUTGOING_PAYLOAD_CONSUMERS_COMPLETE=true`.

## New facts

The exact binary contains no literal occurrence of:

```text
OutGoingMessagePayload
OutgoingMessagePayload
MessageBody
SerializeWithCachedSizesToArray
SerializeToArray
ByteSizeLong
```

A previously mentioned `OutGoingMessagePayload`-named envelope is therefore **not** independently reproduced for this exact build.

GDB exposed:

```text
QIODevice::write(QByteArray const&)@plt = 0x4de370
QTcpSocket::QTcpSocket(QObject*)@plt = 0x4ddbc0
```

The experiment did not prove that the queue receiver reaches either symbol.

## Correction of the inherited vtable chain

The experiment carried `0x308c408`, `0x8409d0`, `0x2f66288`, and `0xb5b880` as **input hypotheses**. Their labels in the report are not independent proof.

Exact aligned disassembly at `0x8409d0` begins:

```text
0x8409d0  push rbp
0x8409d1  push rbx
0x8409d2  mov  rbx,rdi
0x8409d5  sub  rsp,0x28
0x8409d9  mov  rdi,[rdi+0x118]
0x8409e0  mov  rax,[rdi]
0x8409e3  call [rax+0x60]
0x8409e6  mov  rdi,[rbx+0x118]
0x8409ed  mov  esi,[rbx+0xa50]
0x8409f3  mov  rax,[rdi]
0x8409f6  call [rax+0x68]
```

**FACT:** code at `0x8409d0` is a non-trivial routine and is not a simple `owner+0x88 -> vslot+0xb8` forwarding thunk.

The broad GDB range used for the alleged `0xb5b880` target started at `0xb5b700`. Under that captured decode, instruction `0xb5b87c` spans through byte `0xb5b880` and the next instruction begins at `0xb5b881`; no exact instruction boundary is shown at `0xb5b880`.

**CONFLICT:** the inherited claim that a valid vtable slot points to exact function entry `0xb5b880` requires re-derivation before reuse.

The workflow's raw `0xe8` census scanned bytes rather than decoded instruction boundaries and produced non-executable nonsense targets. Those raw hits are not promoted. Only exact decoded instructions may support subsequent structural claims.

## What remains proven

Independent queue-handoff evidence remains:

```text
TProtocolMessageQueue::clientMessageReadyToProcess
  -> QObject::connectImpl at 0x7e7470
  -> receiver = containing owner object
  -> encoded pointer-to-member 0x91
  -> receiver virtual slot offset +0x90
```

The same setup family constructs a `QTcpSocket`.

The **concrete function occupying receiver slot `+0x90` is UNKNOWN** until the receiver primary vptr is re-derived from setup/constructor provenance. Serializer, framing and final socket-write sites remain UNKNOWN.

## Next experiment

Reconstruct the concrete receiver target from the proven connect-site:

1. exact disassembly around `0x7e7470` and slot-object callable `0x2a73200`;
2. enumerate read-only address points referenced by the containing setup region;
3. score only address points whose function slots are executable and read exact `+0x90` qwords;
4. directly verify old `0x308c408:+0x90` and `0x2f66288:+0xb8` table values;
5. exact-entry disassemble every surviving target;
6. only then continue toward framing and `QIODevice`/`QTcpSocket` write.
