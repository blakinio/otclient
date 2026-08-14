# Track A — protocol queue to network handoff

## Result

Exact-binary Qt connection reconstruction closes the outbound chain from the already recovered action builders to the transport-owner processing handoff.

Run `31805205225` proved that `TProtocolMessageQueue::clientMessageReadyToProcess` is QMeta method index `191`, emitted by wrapper `+0xde91b0`, and connects through a virtual pointer-to-member encoded as `0x91`, i.e. receiver vtable slot `+0x90`. Run `31805264031` proved the sender is the queue stored at `[owner+0x88]` and the receiver is the containing owner object. The same setup path constructs a `QTcpSocket` at `+0x196fee0`, so this receiver belongs to the network/transport owner rather than an internal GameAction re-emitter.

The queue action bodies remain:

| Action | Builder body | Internal discriminator |
|---|---:|---:|
| movement north | `+0xbc7ed0` | `0x65` |
| GoPath | `+0xbd3330` | `0x64` |
| MoveObject | `+0xbd3be0` | `0x78` |
| TradeObject | `+0xbcfff0` | `0x7d` |
| Talk | `+0xbd5530` | `0x96` |
| Attack | `+0xbcc510` | `0xa1` |
| Follow | `+0xbcc6d0` | `0xa2` |

`TProtocolMessageQueue::sendMessage` at `+0xde6de0` is a signal wrapper and is not mislabeled as a serializer. The next proven downstream processing entry is the transport owner's virtual slot `+0x90`, reached by `clientMessageReadyToProcess`; its concrete function and exact serializer/framing role are separately probed by the live-owner workflow.

Run `31806620571`, job `94786993940`, also falsified an adjacency hypothesis: static metaobject `0x3085ba0` is `tibia::creatures::TCreatureStorage` (`playerAdded`, `creatureUpdated`, `creatureAppearanceUpdated`), not the transport owner.

## Confidence boundary

- **FACT:** all requested action builder entry points and their internal discriminators.
- **FACT:** queue-to-containing-network-owner handoff and downstream virtual entry slot `+0x90`.
- **FACT:** the owner setup creates a `QTcpSocket`.
- **UNKNOWN:** the concrete slot function and the exact point at which framing bytes are serialized.
- **UNKNOWN:** internal discriminators are not promoted to final wire bytes without framing-byte capture.
