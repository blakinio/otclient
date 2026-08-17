# Track A P2 — `0x4dd250` / QIODevice provenance

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-4dd250-qiodevice-provenance`  
Research status: **DRAFT / NOT PROMOTED — READY FOR COORDINATOR REVIEW AFTER FINAL CI**

## Exact-client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

All new source generations re-fenced the retained regular exact client before reading bounded file-backed bytes. Source-side work performed no disassembly or semantic classification, accessed no client process/process memory/canonical runtime, executed or mutated no client, and uploaded no raw executable/package. Semantic decoding ran on GitHub-hosted Ubuntu. World-map evidence was not used.

## Canonical input

Coordinator promotion #489 establishes the strongest accepted edge before this task:

```text
canonical same message
 -> 0xf50090
 -> field decomposition
 -> writer vslot +0x58 guard == 0xcb2960
 -> payload pointer from canonical message+0x10
 -> payload length from canonical message+0x18
 -> underlying receiver at writer+0x18
 -> exact target 0x4dd250
```

Canonical #489 intentionally left these identities `UNKNOWN`:

```text
writer exact dynamic type
underlying receiver exact dynamic type
semantic role of 0x4dd250
whether 0x4dd250 is the final binary socket boundary
final socket ownership
```

## Accepted exact-SHA predecessor evidence

### PR #308 — writer / QDataStream identities

Accepted exact-SHA artifact `9251725866`, digest:

```text
sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
```

was independently re-read. It establishes:

```text
0x1960340
 -> installs TIODeviceWriter vtable AP 0x2f69d48
 -> RTTI 0x3080718 = TIODeviceWriter
 -> retains supplied QIODevice shared pair at writer+0x08/+0x10
 -> constructs QDataStream(QIODevice*)
 -> retains QDataStream shared pair at writer+0x18/+0x20
```

and exact PLT identity:

```text
0x4dd250 = QDataStream::writeRawData(char const*, qint64)
```

### PR #299 — TCPConnection / QTcpSocket member identity

Merged PR #299 (`8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`) is canonical exact-client evidence for:

```text
TGameserverTCPConnection vtable AP 0x3084b38
AP-0x08 -> RTTI 0x3080630
RTTI name -> tibia::network::TGameserverTCPConnection
```

and for both exact constructors:

```text
0x196ff2a  QTcpSocket constructor path
0x19702c7  QTcpSocket constructor path
```

The corresponding socket member stores are instruction-proven:

```text
path 1 socket store 0x196ff90
path 2 socket store 0x197033d
```

Because the `TGameserverTCPConnection` subobject starts at allocation `+0x10`, both stores are its member `this+0x10`. Thus:

```yaml
TGameserverTCPConnection_this_plus_0x10: FACT:concrete_QTcpSocket_pointer
```

## New evidence generations

### Generation 1 — direct constructor callers

```text
run         32038672531 = SUCCESS
source job  95413976848 = SUCCESS
hosted job  95414062445 = SUCCESS
```

The exact executable contains exactly two direct calls to `0xb4aea0`:

```text
0x1970285
0x1970608
```

The initial RTTI substring scanner did not recover type candidates; that methodological gap was not interpreted semantically and was repaired in generation 2.

### Generation 2 — exact TCPConnection RTTI and expanded callers

```text
run         32038917855 = SUCCESS
source job  95414621259 = SUCCESS
hosted job  95414649302 = SUCCESS
bundle sha  3fa3b3118c0a988000de6c77fc9c52514f9670f9f3d7b52f2d07f63ba53071b7
```

Fixed structural evidence resolves:

```text
known AP        0x3084b38
AP typeinfo     0x3080630
RTTI name       N5tibia7network24TGameserverTCPConnectionE
```

Both callers construct/source an object whose subobject vptr is exactly that address point before passing it to `0xb4aea0`.

Caller 1:

```text
196ff02: alloc 0x20
196ff18: r12 = allocation+0x10
196ff20: rdi = r12
196ff2a: call 0x4ddbc0              # canonical #299 QTcpSocket ctor
...
196ff89: lea rax,0x3084b38
196ff90: mov [rbx+0x20],r12         # TCPConnection this+0x10 socket
196ff98: mov [rbx+0x10],rax         # TCPConnection vptr
...
1970234: rax = [rbp-0x1a8]          # TCPConnection object
1970252: [rbp-0x190] = rax
1970274: rsi = &pair
1970285: call 0xb4aea0
```

Caller 2:

```text
19702c7: call 0x4ddbc0              # canonical #299 QTcpSocket ctor
...
197031b: lea rax,0x3084b38
197032e: mov [rbx+0x10],rax         # TCPConnection vptr
197033d: mov [rbx+0x20],rax         # TCPConnection this+0x10 socket
...
19705d5: [rbp-0x170] = r13          # TCPConnection object
19705f7: rsi = &pair
1970608: call 0xb4aea0
```

Therefore both exact `TGameserverNetworkPacketConnection` constructions reached by these calls are sourced by `TGameserverTCPConnection` objects, not inferred from address adjacency or class names alone.

### Generation 3 — TCPConnection socket pair into current TIODeviceWriter

```text
run         32039061786 = SUCCESS
source job  95415015967 = SUCCESS
hosted job  95415041166 = SUCCESS
window      0xb4ae90..0xb4b290
window sha  4bc45e68bc7c1530579860dfb7769d48e162a82f80fad17a098d2a695760f596
```

The exact bridge begins by copying the supplied `TGameserverTCPConnection` shared pair into `TGameserverNetworkPacketConnection this+0x10/+0x18`:

```text
b4aece: movdqu xmm1,[r15]
b4aed3: movaps [rbp-0x90],xmm1
b4aee1: movups [rbx+0x10],xmm1
```

Later, the exact source object is dereferenced:

```text
b4b1ee: mov rax,[rbx+0x10]          # TGameserverTCPConnection object
b4b1f2: mov rcx,[rax+0x10]          # TCPConnection this+0x10 QTcpSocket pointer
b4b1f6: mov r15,[rax+0x18]          # shared control pointer
b4b1fa: mov [rbp-0xb0],rcx
```

The same two qwords are then rebuilt as a shared pair:

```text
b4b230: movq xmm0,[rbp-0xb0]        # QTcpSocket pointer
b4b238: movq xmm6,r15               # shared control
b4b24f: punpcklqdq xmm0,xmm6
...
b4b26f: movaps [rbp-0x40],xmm0     # exact pair
b4b273: call 0x1960340               # TIODeviceWriter helper
```

The argument to `0x1960340` at `b4b273` is therefore exactly the `TGameserverTCPConnection +0x10/+0x18` QTcpSocket shared pair.

Combining generation 3 with canonical #299 and accepted #308 gives the complete static ownership chain:

```text
TGameserverTCPConnection
 -> this+0x10 concrete QTcpSocket
 -> QTcpSocket shared pair copied by b4aea0
 -> supplied to helper 0x1960340
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream(QIODevice*) constructed on that QTcpSocket
 -> QDataStream object at writer+0x18
 -> canonical payload pointer/length
 -> QDataStream::writeRawData@0x4dd250
```

## Promoted-candidate classifications

```yaml
current_writer_exact_dynamic_type: FACT:TIODeviceWriter
current_writer_vtable_ap: FACT:0x2f69d48
current_writer_qiodevice_shared_pair: FACT:TGameserverTCPConnection_this_plus_0x10_plus_0x18
current_writer_qiodevice_concrete_type: FACT:QTcpSocket
current_writer_qiodevice_owner: FACT:TGameserverTCPConnection
current_writer_qdatastream_member: FACT:TIODeviceWriter_plus_0x18
0x4dd250_identity: FACT:QDataStream::writeRawData_char_const_ptr_qint64
canonical_payload_pointer_to_0x4dd250: FACT
canonical_payload_length_to_0x4dd250: FACT
qdatastream_bound_device: FACT:QTcpSocket
qt_qtcpsocket_bound_binary_serialization_boundary: PROVEN
final_socket_owner: FACT:TGameserverTCPConnection
```

This is the first exact same-message path that binds the canonical binary payload to a concrete QTcpSocket-backed QDataStream.

## Egress terminology boundary

The evidence proves the binary gameplay payload reaches `QDataStream::writeRawData` on a `QDataStream` constructed with the concrete `TGameserverTCPConnection::QTcpSocket*`. That is a proven **Qt QTcpSocket-bound binary serialization/write boundary**.

It does not inspect Qt's internal implementation below `QDataStream/QTcpSocket` and therefore does not prove the final operating-system `send`/`write` syscall or kernel socket descriptor transition.

Use precise classifications:

```yaml
FINAL_BINARY_EGRESS_AT_QT_QTCPSOCKET_BOUNDARY: PROVEN
FINAL_SOCKET_OWNER: FACT:TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL: UNKNOWN
FRAMING: UNKNOWN
SEQUENCE: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
```

The legacy undifferentiated phrase `FINAL_BINARY_EGRESS` should not be used to imply an OS syscall. If retained for compatibility, qualify it as `PROVEN_AT_QT_QTCPSOCKET_BOUNDARY` rather than claiming kernel egress.

## Negative controls

- `0xb4066b` direct QIODevice write remains outside this canonical same-message branch and is not the final sink.
- `0xb46bd0` is a separately proven QTcpSocket QString/local8bit/newline path, not gameplay binary proof.
- `0xc33259` remains non-network/QMatrix4x4.
- `0xb5b880` remains superseded.
- no generic Qt write census, class-name-only inference, vtable adjacency or mere socket possession is used as proof.

## Next frontier

The Qt QTcpSocket boundary is now statically proven. Remaining transport research should be treated independently:

1. inspect framing/sequence/compression/encryption ordering before this boundary if required;
2. only if OS-level final egress is specifically required, trace the Qt QTcpSocket implementation/import path below the proven boundary.

Do not start a new frontier from this task before coordinator promotion/closeout.

E2E: `NOT_APPLICABLE` — exact static file/disassembly evidence only.
