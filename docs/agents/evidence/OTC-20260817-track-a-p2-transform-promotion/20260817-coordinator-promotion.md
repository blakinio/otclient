# Track A P2 outbound transforms — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-raw-transform-semantics`  
Source Draft: PR #497  
Source final head: `b2a3f6ee9cbc785c20df429b5a482d6ffc92b0d9`  
Integration base: `main@8a5fcfd72f2554261eef91a2129c9cc076e730ea`  
Decision: **ACCEPT_WITH_EDITS**

Exact client: `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Source closeout checks

The final researcher head was independently checked before promotion:

```text
Track A governance 32060048976 = SUCCESS
CI                 32060049189 = SUCCESS
CI / Required      95479139576 = SUCCESS
changed files      3
reviews/threads    0/0
one-shot workflow  removed
```

The final source diff contains only the researcher task and two durable evidence files. No runtime/login/world-map/process-memory/full executable upload/owner-funded AI was used.

## Independent encryption verification

The coordinator rechecked hosted exact-byte run `32046592885`, source job `95435821666`, hosted job `95435860761`.

Concrete type/dispatch evidence:

```text
vtable AP        0x2f63148
typeinfo         0x3077800
RTTI             N6shared11TXteaHelperE  (shared::TXteaHelper)
vslot +0x20      0xf85eb0
vslot +0x28      0xf861e0
```

The exact `0xf861e0..0xf864c0` transform window has SHA-256 `f45afa6aaf3337850d4d892692d533140f896444e4a1342c83f73cb7053de3be` and the vtable window `0x2f63138..0x2f63188` has SHA-256 `a2c5fbc512e3510ac14f876e840e9ec02dfbb1b13db6620a63b4e6ba02399e64`.

This is not a class-name-only classification. On the canonical RawDataProcessor path, mode `message+0x28 == 2` invokes the concrete member vslot `+0x28`; the slot receives the padded byte container and produces the replacement QByteArray that is moved back into the same outgoing message. Exact receiver provenance plus the byte-container transform is sufficient to promote the stage role as encryption.

The deeper type-erased backend trace from run `32046849472` is retained only as supporting control flow. The coordinator does **not** promote an independently rederived XTEA round core, exact round count, or constants from that trace. Those details remain outside the accepted claim.

Promoted encryption classification:

```yaml
ENCRYPTION: PROVEN
ENCRYPTION_GATE: FACT:message_plus_0x28_equals_2
ENCRYPTION_RECEIVER: FACT:shared::TXteaHelper
ENCRYPTION_VTABLE_AP: FACT:0x2f63148
ENCRYPTION_TRANSFORM_SLOT: FACT:vslot_plus_0x28_at_0xf861e0
XTEA_ROUND_CORE: UNKNOWN_NOT_REQUIRED_FOR_ENCRYPTION_ROLE_CLASSIFICATION
```

## Independent compression falsification

The coordinator independently checked run `32059752436`, source job `95478101478`, hosted job `95478152304`:

- `TProtocolClientMessageProcessor+0x10`: `0xc2df80..0xc2e500`, SHA-256 `00cea4d539c6f4ac8695ae908535b88af7af849f27f4f69578e20cc6f49557b9`;
- `TGameserverNetworkPacketRawDataProcessor+0x10`: `0xb47130..0xb47440`, SHA-256 `d0cd15d635e9452788f628f0d61d26025665d859eb6315b1c188a97d6795f993`.

Previously promoted coordinator evidence independently establishes the path:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same outgoing message
 -> DualConnection / NetworkPacketProcessor
 -> 0xf50090 framing
 -> TIODeviceWriter / QDataStream::writeRawData@0x4dd250
 -> TGameserverTCPConnection-owned QTcpSocket
```

`0xc2df80` reads/copies the persistent-QBuffer data into the outgoing network message and selects mode metadata. The complete `0xb47130` byte-changing body then performs:

1. one-byte prefix insertion;
2. padding until length is divisible by eight;
3. padding-count store into the first byte;
4. conditional concrete `shared::TXteaHelper` transform for mode 2;
5. assignment of the result back to the same outgoing message.

No separate compression transform occurs in these complete local byte-changing stages, and the already-canonical downstream same-message chain has no intervening payload replacement/compressor before framing/QTcpSocket.

Therefore compression is **disproven on the proven outbound path**. This is intentionally not globalized to inbound traffic, unrelated client code, or unproven alternative paths.

Promoted compression classification:

```yaml
COMPRESSION: DISPROVEN_ON_PROVEN_OUTBOUND_PATH
COMPRESSION_OUTSIDE_PROVEN_OUTBOUND_PATH: UNKNOWN
```

## Final P2 outbound protocol classification

```yaml
FRAMING: PROVEN
SEQUENCE: PROVEN
ENCRYPTION: PROVEN
COMPRESSION: DISPROVEN_ON_PROVEN_OUTBOUND_PATH
FINAL_BINARY_EGRESS: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER: FACT:TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL: UNKNOWN_OPTIONAL
```

This closes the non-optional P2 outbound protocol-semantic reconstruction at the Qt/QTcpSocket boundary. Linux syscall tracing below that already-proven boundary remains optional because it does not change the reconstructed application-layer outbound protocol.

## Negative controls

The promotion does not rely on RTTI naming alone, 8-byte alignment alone, Canary/OT expectations, generic Qt census, vtable adjacency as temporal ordering, or runtime behavior. The historically disproven `0xb4066b` final-egress interpretation and the erroneous `TConnectionMultiplexer` / `TGameserverTCPConnection::write@0xb40a10` chain remain rejected.

Audit: `PASS_BOUNDED`, material findings open `0`. E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
