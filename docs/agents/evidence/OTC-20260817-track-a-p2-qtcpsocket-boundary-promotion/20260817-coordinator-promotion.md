# Track A P2 QTcpSocket-bound binary boundary — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-4dd250-qiodevice-provenance`  
Source Draft: PR #490  
Final reviewed source head: `6d6211b89c802600ab7e749d3b08ba3f7a60840f`  
Trusted integration base: `main@c1ddb0e0a8a6a1634668f025837aab72d20af64e`  
Disposition: **ACCEPT_WITH_EDITS**

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

This promotion is static exact-file/disassembly evidence only. No live client process, process memory, canonical runtime, login/gameplay or world-map evidence was used. No owner-funded AI/API was used.

## Independent verification

The coordinator did not use the researcher summary as proof. The final three-file source diff, exact source/hosted logs and accepted predecessor evidence were independently checked.

New generation evidence:

```text
run 32038672531 = SUCCESS
  source 95413976848
  hosted 95414062445
  direct calls to 0xb4aea0: 0x1970285, 0x1970608

run 32038917855 = SUCCESS
  source 95414621259
  hosted 95414649302
  bundle sha256 3fa3b3118c0a988000de6c77fc9c52514f9670f9f3d7b52f2d07f63ba53071b7
  AP 0x3084b38
  typeinfo 0x3080630
  RTTI name N5tibia7network24TGameserverTCPConnectionE

run 32039061786 = SUCCESS
  source 95415015967
  hosted 95415041166
  bridge 0xb4ae90..0xb4b290
  bridge sha256 4bc45e68bc7c1530579860dfb7769d48e162a82f80fad17a098d2a695760f596
```

All source stages re-fenced the exact retained regular ELF and performed only bounded file-byte mapping / structural indexing. Source-side disassembly, semantic classification, runtime/process access, client execution/mutation and raw executable upload were absent. Semantic decode ran on GitHub-hosted Ubuntu.

Final researcher head validation:

```text
Track A governance 32039404811 = SUCCESS
CI                 32039405213 = SUCCESS
CI / Required      95416178014 = SUCCESS
changed files      exactly 3 durable P2 files
reviews/threads    0/0 before coordinator disposition
one-shot workflow  absent from final diff
```

The initial CI failure on the final head was an external `codeload.github.com` HTTP 429 while downloading `dorny/paths-filter`; one evidence-based job retry succeeded without repository changes.

## Accepted predecessor identities

### TIODeviceWriter / QDataStream

Accepted exact-SHA PR #308 artifact:

```text
artifact 9251725866
sha256   f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
```

independently establishes:

```text
helper 0x1960340
 -> TIODeviceWriter AP 0x2f69d48
 -> RTTI 0x3080718
 -> supplied QIODevice shared pair retained at writer+0x08/+0x10
 -> QDataStream(QIODevice*) constructed
 -> QDataStream shared pair retained at writer+0x18/+0x20

0x4dd250 = QDataStream::writeRawData(char const*, qint64)
```

Current canonical main also contains the final `0xf50090` writer-type reconciliation, so this promotion does not depend on historical researcher narrative alone.

### TGameserverTCPConnection / QTcpSocket

Merged PR #299 (`8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`) canonically establishes:

```text
TGameserverTCPConnection AP 0x3084b38
RTTI 0x3080630
exact QTcpSocket constructor paths 0x196ff2a and 0x19702c7
concrete QTcpSocket member TGameserverTCPConnection this+0x10
```

## New exact ownership bridge

Generation 2 independently re-resolves the actual objects supplied to both direct `0xb4aea0` callers as `TGameserverTCPConnection` by exact vptr/RTTI evidence.

Generation 3 proves the load-bearing QTcpSocket shared-pair flow:

```text
b4b1ee: mov rax,[rbx+0x10]   # source TGameserverTCPConnection
b4b1f2: mov rcx,[rax+0x10]   # TCPConnection this+0x10 concrete QTcpSocket*
b4b1f6: mov r15,[rax+0x18]   # shared control
b4b1fa: mov [rbp-0xb0],rcx
...
b4b230: movq xmm0,[rbp-0xb0]
b4b238: movq xmm6,r15
b4b24f: punpcklqdq xmm0,xmm6
...
b4b26f: movaps [rbp-0x40],xmm0
b4b273: call 0x1960340        # TIODeviceWriter helper
```

Thus the QIODevice shared pair supplied to the current TIODeviceWriter is exactly the `TGameserverTCPConnection +0x10/+0x18` QTcpSocket shared pair.

## Canonical P2 binary path after this promotion

Combining canonical #450/#481/#487/#489/current-main evidence with the newly accepted ownership bridge gives:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection+0x78@0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090
 -> structured message field decomposition
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream constructed on TGameserverTCPConnection::QTcpSocket*
 -> canonical payload pointer/length
 -> QDataStream::writeRawData(char const*, qint64) @ 0x4dd250
 -> Qt QTcpSocket-bound binary boundary
```

Promoted classifications:

```yaml
CURRENT_WRITER_TYPE: FACT:TIODeviceWriter
CURRENT_QIODEVICE_TYPE: FACT:QTcpSocket
CURRENT_QIODEVICE_OWNER: FACT:TGameserverTCPConnection
TARGET_0x4DD250: FACT:QDataStream::writeRawData(char const*, qint64)
CANONICAL_PAYLOAD_POINTER_TO_0x4DD250: FACT
CANONICAL_PAYLOAD_LENGTH_TO_0x4DD250: FACT
QT_QTCPSOCKET_BOUND_BINARY_BOUNDARY: PROVEN
FINAL_BINARY_EGRESS: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER: FACT:TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL: UNKNOWN
FRAMING: UNKNOWN
SEQUENCE: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
```

This is the first canonical exact same-message chain that binds the gameplay binary payload to a concrete QTcpSocket-backed QDataStream.

## Terminology boundary

`FINAL_BINARY_EGRESS=PROVEN_AT_QT_QTCPSOCKET_BOUNDARY` is an abstraction-level statement. It proves the binary payload is written through `QDataStream::writeRawData` on a QDataStream constructed on the concrete `TGameserverTCPConnection::QTcpSocket*`.

It does **not** prove a specific Linux `send`/`write` syscall, file descriptor or kernel socket transition. Those remain `FINAL_OS_SOCKET_SYSCALL=UNKNOWN` unless a future separately authorized static frontier traces below Qt.

Framing, sequence, compression and encryption remain independent `UNKNOWN` classifications; no transport-layer semantic is inferred merely because the QTcpSocket boundary is now proven.

## Negative controls

- `0xb4066b` remains outside the canonical same-message path and is not the final gameplay sink.
- `0xb46bd0` remains a separately proven QTcpSocket QString/local8bit/newline path, not gameplay binary proof.
- `0xc33259` remains QMatrix4x4/non-network.
- `0xb5b880` remains superseded.
- no generic Qt write census, class-name-only inference, vtable adjacency or socket possession alone is used as proof.

## Audit / E2E / continuation

Fresh coordinator audit: `PASS_BOUNDED`; material findings open: `0`.

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.

This was the final additional research task allowed by the current autonomous invocation. This closeout intentionally creates **no new active research task**. Future independent frontiers, for a later owner invocation, are:

1. optional OS-level Qt/QTcpSocket -> Linux syscall/kernel transition;
2. framing;
3. sequence;
4. compression;
5. encryption ordering before the proven QTcpSocket boundary.
