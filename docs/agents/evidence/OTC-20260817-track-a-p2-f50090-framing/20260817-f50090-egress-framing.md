# P2 outbound framing at `0xf50090`

Status: `DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW`  
Task: `OTC-20260817-track-a-p2-f50090-framing`  
Base: `main@c1adcf491580e28d40f215356a9e559af2ccadc4`  
Exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Execution used existing exact-client bounded artifacts only: `runtime_access: none`; no new source run, runtime/login, world-map, raw executable upload or owner-funded AI.

## Canonical boundary reused

PR #492/current main already proves:

```text
same outbound message
 -> TGameserverDualConnection +0x78
 -> virtual +0x30 @ 0xb56c93
 -> TConnectionMultiplexer::write @ 0xf50040
 -> second virtual +0x30 @ 0xf50090
 -> TGameserverTCPConnection::write @ 0xb40a10
 -> concrete TGameserverTCPConnection-owned QTcpSocket
 -> QDataStream
 -> QDataStream::writeRawData @ 0x4dd250
```

This task does not reopen reachability.

## Primary exact evidence

- run `32037533068`, hosted job `95410901806`, exact window `0xf50040..0xf50480`, SHA-256 `1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea`;
- run `31904696996`, artifact `9252025461`, digest `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991`;
- run `32005141186`, artifacts `9279753620` / `9279759553`, digests `sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32` / `sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`;
- accepted helper artifact `9251725866`, digest `sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`.

## FACT — two pre-payload scalar writes

`0xf50090` preserves the canonical message in `rbp` and loads payload length from `message+0x18`:

```text
f50093 mov rbp,rsi
f500a3 mov rax,[rsi+0x18]
```

First scalar source for nonnegative lengths is `ceil(payload_length/8)`; its low 16-bit value is forwarded:

```text
f500c6 lea rsi,[rax+0xe]
f500ca add rax,0x7
f500d5 cmovns rsi,rax
f500dc sar rsi,0x3
f500f1 movsx esi,si
f500f7 call 0x4dc3d0
```

The next scalar is loaded as a DWORD from the original message at `+0`:

```text
f50107 mov esi,DWORD PTR [rbp+0x0]
f5011a mov rdi,[rdi+0x18]
f50121 call 0x4daaf0
```

Only afterwards is the raw payload written:

```text
f5013d mov rsi,[rsp+0x8]      # payload pointer
f50142 mov rdi,[rdi+0x18]     # underlying QDataStream
f50146 mov rdx,[rsp+0x10]     # payload length
f50153 call 0x4dd250           # QDataStream::writeRawData
```

Wrapper `0xcb2960` independently preserves the same pointer/length/QDataStream forwarding into `0x4dd250`.

Combined with PR #492 QTcpSocket provenance, these are deterministic pre-payload writes on the concrete outbound wire-bound serialization path. Therefore `FRAMING=PROVEN`. The semantic name and encoded byte-order/width of the scalar operators beyond the directly observed source widths are not overclaimed.

## FACT — earlier RawDataProcessor envelope transform

Exact bytes at `TGameserverNetworkPacketRawDataProcessor @ 0xb47130` show:

```text
prepend one byte
 -> append helper-produced bytes until total QByteArray length % 8 == 0
 -> first byte = number of bytes appended after the prefix
 -> assign transformed QByteArray back to the same message
```

Key calls/edges: `b47189 -> QByteArray::insert`, `b47206 -> QByteArray::append(char)`, loop `b47210/b47214`, count store `b4725f/b47285`, assignment `b47300 -> QByteArray::operator=`.

The padding-byte helper and optional later indirect transform are not semantically typed. This task does not label them encryption.

## Terminal researcher classification

```text
DUALCONNECTION_TO_BINARY_EGRESS=PROVEN
FINAL_BINARY_EGRESS=QDataStream::writeRawData@0x4dd250_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER=TGameserverTCPConnection
FRAMING=PROVEN
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
LINUX_SOCKET_SYSCALL=UNKNOWN
```

## Proven stage order

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10 @ 0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10 @ 0xb47130
 -> same message after proven 8-byte-alignment envelope transform
 -> TGameserverDualConnection +0x80/+0x78
 -> virtual +0x30 @ 0xb56c93
 -> TConnectionMultiplexer::write @ 0xf50040
 -> second virtual +0x30 / serialization @ 0xf50090
 -> scalar A = low16(ceil(payload_length/8))
 -> scalar B = DWORD(message+0), semantics UNKNOWN
 -> raw payload
 -> TGameserverTCPConnection::write @ 0xb40a10
 -> owned QTcpSocket / QDataStream
 -> QDataStream::writeRawData @ 0x4dd250
 -> Linux socket syscall UNKNOWN
```

## Rejected / controlled historical candidates

- `0xb40630/0xb4066b`: `DISPROVEN` as this DualConnection egress branch. `0xb4066b` remains a real QIODevice write inside distinct `0xb40630`, but canonical dataflow resolves elsewhere.
- `0xb46bd0`: QString/local8bit/newline negative control; not used as gameplay-binary proof.
- `0xc33259`: QMatrix4x4/non-network negative control; not used.
- `0xb5b880`: superseded historical sink candidate; not used.
- generic Qt write census, names without dataflow, vtable adjacency and mere QTcpSocket ownership remain inadmissible proof.

## Remaining UNKNOWN and next frontier

`DWORD(message+0)` has no proven semantic identity yet. `SEQUENCE`, `COMPRESSION`, `ENCRYPTION` and Linux syscall boundary remain `UNKNOWN`.

Next smallest falsifiable frontier: trace the exact producer/update provenance of `DWORD(message+0)` that reaches `f50107`; prove or disprove connection-scoped monotonic sequence semantics from a concrete assignment/update edge. Width, position or names alone are insufficient.

Promotion authority: coordinator only.