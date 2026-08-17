# Track A P2 outbound framing — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-f50090-framing`  
Source Draft: PR #493  
Final reviewed source head: `6d01a7eb22548256e0d4f5aff9a6d13f95f84c19`  
Trusted integration base: `main@c1adcf491580e28d40f215356a9e559af2ccadc4`  
Disposition: **ACCEPT_WITH_EDITS**

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

Static/artifact review only: `runtime_access:none`. No live client, process memory, login/gameplay, world-map, raw executable upload or owner-funded AI/API was used.

## Independent verification

The coordinator did not treat the researcher summary as proof. Primary current-main evidence and exact hosted disassembly output were independently checked.

Source Draft exact-head validation:

```text
Track A governance 32042849047 = SUCCESS
CI                 32042849245 = SUCCESS after one infrastructure-only retry
CI / Required      95429351299 = SUCCESS
changed files      exactly 3 P2 task/evidence files
reviews/threads    0/0
```

The first CI attempt failed before checkout/path evaluation because `dorny/paths-filter` downloads returned HTTP 429/502/429. One allowed retry succeeded without repository changes.

Load-bearing exact hosted evidence:

```text
run 32037533068
hosted job 95410901806
window 0xf50040..0xf50480
sha256 1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
```

Accepted predecessor evidence:

```text
run 32005141186
source artifact 9279753620
source sha256 6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32
hosted artifact 9279759553
hosted sha256 8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528

artifact 9251725866
sha256 f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
```

Current main / PR #492 already canonically binds the same outbound message to `TIODeviceWriter`, its `QDataStream`, the concrete `TGameserverTCPConnection`-owned `QTcpSocket`, and `QDataStream::writeRawData@0x4dd250`.

## Exact pre-payload ordering at `0xf50090`

The canonical message is retained in `rbp`; its payload length comes from `message+0x18`.

For a nonnegative payload length, the first scalar source is computed as `ceil(payload_length/8)` and its low 16 bits are forwarded through the current writer scalar path:

```text
f500c6  lea   rsi,[rax+0xe]
f500ca  add   rax,0x7
f500d5  cmovns rsi,rax
f500dc  sar   rsi,0x3
f500f1  movsx esi,si
f500f7  call  0x4dc3d0
```

The next scalar source is a DWORD from the same original message at `+0`:

```text
f50107  mov   esi,DWORD PTR [rbp+0x0]
f5011a  mov   rdi,[rdi+0x18]
f50121  call  0x4daaf0
```

Only afterwards is the canonical raw payload pointer/length forwarded to the underlying QDataStream:

```text
f5013d  mov   rsi,[rsp+0x8]
f50142  mov   rdi,[rdi+0x18]
f50146  mov   rdx,[rsp+0x10]
f50153  call  0x4dd250
```

The accepted wrapper at `0xcb2960` independently preserves the same pointer/length/QDataStream forwarding into `0x4dd250`.

Because PR #492 already proves this writer/QDataStream is bound to the concrete outbound `QTcpSocket`, the deterministic scalar-before-raw ordering is a real outbound framing boundary rather than a local-only byte-container observation.

Classification:

```text
FRAMING=PROVEN
```

This promotion does **not** assign semantic names to either scalar and does not infer sequence, compression or encryption from their width or position.

## Earlier RawDataProcessor envelope transform

Exact hosted bytes at `TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130` independently prove:

```text
prepend one zero byte
 -> append helper-produced bytes until QByteArray length % 8 == 0
 -> first byte = number of bytes appended after the prefix
 -> if message+0x28 == 2, invoke a separate member-object virtual transform
 -> assign resulting QByteArray back to the same message
```

The padding-byte helper and conditional transform are not semantically named by this promotion. In particular, the 8-byte alignment is not itself proof of encryption.

## Canonical stage order after promotion

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message after proven alignment-envelope transform
 -> TGameserverDualConnection+0x78@0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090 structured message decomposition
 -> scalar A source = low16(ceil(payload_length/8))
 -> scalar B source = DWORD(message+0), semantics UNKNOWN
 -> raw payload pointer/length
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream bound to TGameserverTCPConnection-owned QTcpSocket
 -> QDataStream::writeRawData@0x4dd250
 -> Qt/QTcpSocket-bound binary boundary
```

Promoted terminal classifications:

```yaml
DUALCONNECTION_TO_BINARY_EGRESS: PROVEN
FINAL_BINARY_EGRESS: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER: FACT:TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL: UNKNOWN
FRAMING: PROVEN
SEQUENCE: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
```

## Negative controls

- `0xb40630/0xb4066b` remains disproven as this DualConnection egress branch.
- `0xb57042` remains disproven as the same-message continuation.
- `0xb46bd0` remains a QString/local8bit/newline path, not binary gameplay proof.
- `0xc33259` remains non-network/QMatrix4x4.
- `0xb5b880` remains superseded.
- generic Qt write census, class names without dataflow, vtable adjacency and mere QTcpSocket ownership are not used as proof.

## Continuation

Fresh coordinator audit: `PASS_BOUNDED`; material findings open: `0`.

E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.

Next smallest falsifiable frontier is the exact producer/update provenance of `DWORD(message+0)` reaching `f50107`, specifically testing whether it is connection-scoped monotonic sequence state. `SEQUENCE` must remain `UNKNOWN` until that edge is proven or disproven.
