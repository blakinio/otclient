# Track A P2 — outbound transform semantics

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-raw-transform-semantics`  
Role: researcher; coordinator-only promotion  
Exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Verdict

For the already-canonical official-Linux outbound path:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10 @ 0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10 @ 0xb47130
 -> same-message DualConnection / NetworkPacketProcessor chain
 -> framing writer
 -> QDataStream::writeRawData @ 0x4dd250
 -> QTcpSocket owned by TGameserverTCPConnection
```

this researcher frontier supports:

```text
FRAMING=PROVEN
SEQUENCE=PROVEN
ENCRYPTION=PROVEN
COMPRESSION=DISPROVEN_ON_PROVEN_OUTBOUND_PATH
FINAL_BINARY_EGRESS=PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
LINUX_SOCKET_SYSCALL=UNKNOWN_OPTIONAL
```

The compression result is deliberately scoped. It does not claim that compression is absent from inbound traffic, unrelated client subsystems, or any path outside the canonical outbound chain above.

## Encryption: direct receiver and transform evidence

Hosted exact-byte run `32046592885` independently decoded the concrete member vtable and transform:

- vtable address point: `0x2f63148`;
- typeinfo: `0x3077800`;
- RTTI name: `N6shared11TXteaHelperE` (`shared::TXteaHelper`);
- slot `+0x20`: `0xf85eb0`;
- slot `+0x28`: `0xf861e0`;
- exact transform window: `0xf861e0..0xf864c0`, SHA-256 `f45afa6aaf3337850d4d892692d533140f896444e4a1342c83f73cb7053de3be`.

The classification is not based on the RTTI name alone. At `0xf861e0` the concrete slot takes the source byte container, pads the source to the required 8-byte boundary using the helper state, invokes the helper's keyed transform path, and returns a replacement byte container. `RawDataProcessor` calls this exact member slot only on the `message+0x28 == 2` branch and then moves the returned QByteArray into the same outbound message.

The later backend trace (`32046849472`) is retained as supporting control-flow evidence only. Its bounded windows are:

- `0x196cdf0..0x196d180`, SHA-256 `cc358f4b322493ca83402309f88eebef2d2613362b7cc2c4e16cc7387fffc7a7`;
- `0x1943ae0..0x1943e80`, SHA-256 `78120e7a2984277385ace93de2b7ed3c4c84fbb8bcfd0c22037c02fcda1ec5df`.

Those callees contain additional type-erased/backend machinery. This task therefore does **not** promote an independently rederived XTEA round core or exact round constants. That lower-level algorithm reconstruction is unnecessary for the narrower claim that the canonical outbound stage performs encryption through the concrete `shared::TXteaHelper` transform.

## Compression: bounded falsification on the canonical outbound path

Run `32059752436` regenerated and GitHub-hosted-decoded both byte-changing local stages from the exact client:

- `TProtocolClientMessageProcessor+0x10`: `0xc2df80..0xc2e500`, SHA-256 `00cea4d539c6f4ac8695ae908535b88af7af849f27f4f69578e20cc6f49557b9`;
- `TGameserverNetworkPacketRawDataProcessor+0x10`: `0xb47130..0xb47440`, SHA-256 `d0cd15d635e9452788f628f0d61d26025665d859eb6315b1c188a97d6795f993`.

Canonical coordinator evidence already proves that the persistent QBuffer is consumed by `0xc2df80`, and that the resulting same message reaches `0xb47130` and then the downstream DualConnection/NetworkPacketProcessor/framing/QTcpSocket path.

### `0xc2df80`

The persistent-QBuffer read anchors remain `0xc2dfa5`, `0xc2dfd5`, `0xc2dfeb`, `0xc2e012`. The decoded body reads/copies the QByteArray into the outgoing message and selects mode metadata in `message+0x28` and `message+0x34`. No compressor-like replacement or size-changing byte transform exists between the accepted QBuffer read and the returned network message.

### `0xb47130`

The complete local byte-changing sequence is directly visible:

1. insert a one-byte prefix at `0xb47189`;
2. obtain/append bytes until the container length is divisible by eight (`0xb471f8..0xb47214`);
3. compute appended-byte count and store it into the first byte at `0xb47285`;
4. if `message+0x28 == 2`, invoke the concrete member slot `+0x28` at `0xb472b4`, now resolved to `shared::TXteaHelper` transform `0xf861e0`;
5. assign the resulting QByteArray back into the same message at `0xb47300`.

There is no separate compression stage in this complete RawDataProcessor body.

### Downstream closure

Previously promoted coordinator evidence proves same-message reachability through the DualConnection/NetworkPacketProcessor chain, framing at `0xf50090`, `TIODeviceWriter`, `QDataStream::writeRawData@0x4dd250`, and the QTcpSocket owned by `TGameserverTCPConnection`. No intervening payload replacement/compression transform was promoted on that same-message chain.

Therefore compression is falsified **for this proven outbound path**. The classification is not generalized to inbound or unrelated code.

## Rejected shortcuts and negative controls

The following were explicitly not used as proof:

- class name `TXteaHelper` without transform dataflow;
- 8-byte alignment by itself;
- expected Tibia/Canary protocol behavior;
- generic Qt/socket census;
- address adjacency or vtable adjacency as temporal order;
- the historically disproven `0xb4066b` final-egress interpretation;
- `TConnectionMultiplexer` or `TGameserverTCPConnection::write@0xb40a10` chains;
- runtime/login/process-memory evidence;
- full executable upload;
- owner-funded AI/API.

## Promotion boundary

This is researcher evidence only. The researcher does not self-promote. Coordinator review must independently re-check the exact run/job logs, current canonical main, final source diff, reviews/threads and CI before promoting `ENCRYPTION=PROVEN` and scoped `COMPRESSION=DISPROVEN_ON_PROVEN_OUTBOUND_PATH`.
