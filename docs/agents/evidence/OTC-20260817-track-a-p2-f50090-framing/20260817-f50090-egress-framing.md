# P2 outbound framing at `0xf50090`

Status: `DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW`  
Task: `OTC-20260817-track-a-p2-f50090-framing`  
Base: `main@c1adcf491580e28d40f215356a9e559af2ccadc4`  
Exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Execution used existing exact-client bounded artifacts only: `runtime_access: none`; no new source run, runtime/login, world-map, raw executable upload or owner-funded AI.

## Canonical boundary reused

Current main / PR #492 already proves:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10 @ 0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10 @ 0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection+0x78 @ 0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> exact target 0xf50090
 -> structured message field decomposition
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream bound to TGameserverTCPConnection-owned QTcpSocket
 -> QDataStream::writeRawData @ 0x4dd250
 -> Qt/QTcpSocket-bound binary boundary
```

This task does not reopen reachability, writer identity or QTcpSocket ownership.

## Primary exact evidence

- run `32037533068`, hosted job `95410901806`, exact window `0xf50040..0xf50480`, SHA-256 `1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea`;
- run `31904696996`, artifact `9252025461`, digest `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991`;
- run `32005141186`, artifacts `9279753620` / `9279759553`, digests `sha256:6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32` / `sha256:8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`;
- accepted TIODeviceWriter/QDataStream helper artifact `9251725866`, digest `sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`;
- canonical current-main QTcpSocket promotion `docs/agents/evidence/OTC-20260817-track-a-p2-qtcpsocket-boundary-promotion/result.json`, blob `8a489244f59d3f4a7f5bb753629b85b5a47b10da`.

## FACT — ordered pre-payload scalar operations

`0xf50090` preserves the canonical message in `rbp` and loads payload length from `message+0x18`:

```text
f50093 mov rbp,rsi
f500a3 mov rax,[rsi+0x18]
```

For nonnegative payload lengths the first scalar source is `ceil(payload_length/8)` and its low 16-bit value is forwarded through a TIODeviceWriter scalar operation:

```text
f500c6 lea rsi,[rax+0xe]
f500ca add rax,0x7
f500d5 cmovns rsi,rax
f500dc sar rsi,0x3
f500f1 movsx esi,si
f500f7 call 0x4dc3d0
```

The next scalar source is a DWORD loaded from the original message at `+0` and forwarded through the next writer scalar operation:

```text
f50107 mov esi,DWORD PTR [rbp+0x0]
f5011a mov rdi,[rdi+0x18]
f50121 call 0x4daaf0
```

Only after those two scalar operations is the raw payload forwarded:

```text
f5013d mov rsi,[rsp+0x8]      # payload pointer
f50142 mov rdi,[rdi+0x18]     # underlying QDataStream
f50146 mov rdx,[rsp+0x10]     # payload length
f50153 call 0x4dd250           # QDataStream::writeRawData
```

Exact wrapper `0xcb2960` independently preserves the same payload-pointer/length/QDataStream forwarding contract:

```text
cb2960 mov rdx,[rsi+0x10]
cb2964 mov rsi,[rsi+0x8]
cb2968 mov rdi,[rdi+0x18]
cb2971 jmp 0x4dd250
```

PR #492 independently proves the dynamic writer is `TIODeviceWriter` and that this underlying QDataStream is bound to the concrete `TGameserverTCPConnection`-owned QTcpSocket. Therefore the two deterministic scalar operations precede the raw payload on the already-proven QTcpSocket-bound outbound serialization path.

This is sufficient for researcher classification `FRAMING=PROVEN`. The semantic name of either scalar, the exact scalar operator semantic names and encoded byte order are not promoted by this task.

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
 -> TGameserverDualConnection+0x78 @ 0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090 structured message field decomposition
 -> scalar A source = low16(ceil(payload_length/8))
 -> scalar B source = DWORD(message+0), semantics UNKNOWN
 -> raw payload pointer/length
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream bound to TGameserverTCPConnection-owned QTcpSocket
 -> QDataStream::writeRawData @ 0x4dd250
 -> Qt/QTcpSocket-bound binary boundary
 -> Linux socket syscall UNKNOWN
```

## Rejected / controlled historical candidates

- `0xb40630/0xb4066b`: `DISPROVEN` as this DualConnection egress branch. `0xb4066b` remains a real QIODevice write inside distinct `0xb40630`, but canonical receiver-vtable/dataflow resolves to `0xf50090` instead.
- `0xb57042` same-message continuation: `DISPROVEN` by the accepted #487 bounded receiver-path work.
- `0xb46bd0`: QString/local8bit/newline negative control; not used as gameplay-binary proof.
- `0xc33259`: QMatrix4x4/non-network negative control; not used.
- `0xb5b880`: superseded historical sink candidate; not used.
- generic Qt write census, class names without dataflow, vtable adjacency and mere QTcpSocket ownership remain inadmissible proof methods.

## Remaining UNKNOWN and next frontier

`DWORD(message+0)` has no proven semantic identity. In particular, it is not called a sequence number from width or position alone.

Remaining independent classifications:

```text
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
LINUX_SOCKET_SYSCALL=UNKNOWN
```

Next smallest falsifiable frontier: trace the exact producer/update provenance of `DWORD(message+0)` that reaches `f50107`; prove or disprove connection-scoped monotonic sequence semantics from a concrete assignment/update edge. Width, position or class naming are insufficient.

Promotion authority remains coordinator-only.
