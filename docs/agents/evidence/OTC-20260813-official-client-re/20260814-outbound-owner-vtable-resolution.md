# Track A — outbound owner vtable resolution

Date: 2026-08-14
Track: `official-client-re`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
Recovery branch: `ci/OTC-20260814-track-a-chatgpt-framing-recovery`
Source run: `31824546383`
Source job: `94845451981`
Source result: `SUCCESS`
Source head: `e5a64bde7d0b3b1fb158886f21940d0536f32127`
Artifact: `track-a-outbound-owner-vtables-31824546383` / id `9228275973` / sha256 `beb0fc79cb9eb75922e46c33d02cc096cb0c56706d8f7f7ac7efa46d8a12d998`

## FACT — corrected outbound QSlot path

The real `clientMessageReadyToProcess` connection is the custom Qt slot object invoker at `0x7dd630`. The previously claimed pointer-to-member `{0x91,0}` / owner virtual `+0x90` model is superseded and disproven by direct connectImpl argument reconstruction.

The exact executable calls made by `0x7dd630` are now resolved through RTTI-backed owner fields:

```text
clientMessageReadyToProcess
  -> QSlotObject invoker 0x7dd630
  -> owner+0xc18 : tibia::network::TGameserverDualConnection
       slot +0x90 -> 0xb40370   (precondition/state result; zero aborts the path)
  -> owner+0xa00 : tibia::protocol::TProtocolClientMessageProcessor
       slot +0x10 -> 0xc2df80
  -> owner+0xa10 : tibia::network::TGameserverNetworkPacketRawDataProcessor
       slot +0x10 -> 0xb47130
  -> owner+0xc18 : tibia::network::TGameserverDualConnection
       slot +0x80 -> 0xb56d60
       slot +0x78 -> 0xb56970
```

All listed virtual targets are executable in the exact pinned ELF.

## FACT — `TProtocolClientMessageProcessor::slot+0x10 @ 0xc2df80`

`0xc2df80` is a concrete outbound processing stage. Its disassembly:

- invokes a virtual on the processor dependency at `[rsi+0x8]`;
- operates on the stream/object at `[rsi+0x18]`;
- obtains bytes through the QIODevice path (`QIODevice::readAll` when the concrete fast-path matches `0xb40710`);
- invokes the stream virtual at `+0xf0` after extraction;
- returns a structured QByteArray/result object to the caller.

This is evidence of client-message transformation/serialization into a byte-oriented buffer, but the exact wire framing boundary is not yet fully named.

## FACT — `TGameserverNetworkPacketRawDataProcessor::slot+0x10 @ 0xb47130`

`0xb47130` consumes the QByteArray-like output from the client-message processor and performs packet-level transformation:

- prepends one byte using `QByteArray::insert`;
- calls a dependency virtual through the raw-data processor;
- appends bytes in a bounded loop;
- writes a computed byte into the first byte of the resulting array;
- conditionally invokes another dependency virtual before returning the transformed QByteArray.

This is structurally downstream of `0xc2df80` on the proven `0x7dd630` path.

## FACT — `TGameserverDualConnection`

RTTI-backed vtable address point: `0x30b7b68`.
Relevant exact virtual targets:

- `+0x78 -> 0xb56970`
- `+0x80 -> 0xb56d60`
- `+0x90 -> 0xb40370`

`0xb56d60` and `0xb56970` inspect contained connection objects and call `QAbstractSocket::state`, including explicit comparison with state value `3` (Qt connected state at the API level). They therefore converge on concrete socket-bearing connection state rather than a purely logical protocol object.

## FACT — inbound/outbound correction

The earlier transport cluster `0x7dd3f0 -> 0x7dd563` is not promoted as the outbound final-write path. Owner-field provenance shows that cluster uses the server/read-side processor/raw-stream chain. It must be kept separate from the proven outbound QSlot path above.

## UNKNOWN

Still not proven:

- exact `TGameserverTCPConnection` vtable and the concrete function that performs the outbound device write;
- whether direct `QIODevice::write` callsite `0xb46c75` is the final gameplay socket write or a writer/helper stage;
- exact framing boundary between `0xc2df80`, `0xb47130`, `TGameserverDualConnection`, and the final socket;
- encryption/compression/sequence details on the selected outbound path;
- exact relationship between internal GameclientMessage discriminators and final wire bytes.

## Next action

Resolve RTTI/vtables and constructor provenance for:

- `tibia::shared::TIODeviceWriter` (RTTI observed at `0x3080718`), and
- `tibia::network::TGameserverTCPConnection` (RTTI observed at `0x3080630`).

Then correlate their virtual targets with the remaining direct `QIODevice::write(QByteArray const&)` callsite at `0xb46c75` and with the connection objects traversed by `0xb56d60/0xb56970`. Promote a final write only after the object identity and call edge are both structural facts.
