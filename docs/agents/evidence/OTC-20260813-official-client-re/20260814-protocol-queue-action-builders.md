# TProtocolMessageQueue action builders

## Scope

- Official Linux client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- QMeta decode run `31802808290`, job `94774542787`.
- Dispatch run `31802935253`, job `94774953120`; convergence run `31803088165`, job `94775445667`.
- Builder disassembly run `31803012968`, job `94775199763`.

## Queue identity and surface

Static metaobject `0x3085b60` is exactly `tibia::protocol::TProtocolMessageQueue`. Its relocation-backed QMeta table has 355 methods. Relevant exact indices include:

| Index | Method |
| --- | --- |
| 0 | `sendMessage` |
| 191 | `clientMessageReadyToProcess` |
| 192 | `fireEmitSignalForNewProtocolMessage` |
| 193 | `fireEmitSignalForNewClientProtocolMessage` |
| 194 | `prepareAndEnqueueGameclientMessage` |
| 195 | `handleGameAction` |
| 201–204 | cardinal movement |
| 209–212 | diagonal movement |
| 213 | `sendGoPath` |
| 218 | `sendMoveObject` |
| 237 | `sendTalkMessage` |
| 247 | `sendAttack` |
| 248 | `sendFollow` |
| 283 | `sendTradeObject` |

The exact static metacall is `0xdf5fe0` and uses a 355-entry relative jump table at `0x1d8bd6c`.

## Exact method entry mapping

Selected QMeta case entries tail-dispatch to concrete method bodies:

| Method | Case entry | Body |
| --- | --- | --- |
| `sendGoNorth` | `0xdf6c37` | `0xbc7ed0` |
| `sendGoEast` | `0xdf6c48` | `0xbc81e0` |
| `sendGoSouth` | `0xdf6c59` | `0xbc84f0` |
| `sendGoWest` | `0xdf6c6a` | `0xbc8800` |
| `sendGoNorthEast` | `0xdf6cbf` | `0xbc94f0` |
| `sendGoSouthEast` | `0xdf6cd0` | `0xbc9800` |
| `sendGoSouthWest` | `0xdf6ce1` | `0xbc9b10` |
| `sendGoNorthWest` | `0xdf6cf2` | `0xbc9e20` |
| `sendGoPath` | `0xdf6d03` | `0xbd3330` |
| `sendMoveObject` | `0xdf6d58` | `0xbd3be0` |
| `sendTalkMessage` | `0xdf7f4e` | `0xbd5530` |
| `sendAttack` | `0xdf7ff8` | `0xbcc510` |
| `sendFollow` | `0xdf8009` | `0xbcc6d0` |
| `sendTradeObject` | `0xdf7b5c` | `0xbcfff0` |

## Builder structure and discriminators

These bodies allocate and initialise an 0x50-byte polymorphic message object, initialise common message storage through `0x1aaa530`, select/construct typed payload storage through `0x1ab2600`, copy action parameters, and submit the owning message through a queue/interface virtual method or shared helper `0xbc6e20`.

Exact discriminator constants written before submission are:

| Action | Constant | Write form |
| --- | --- | --- |
| `sendGoPath` | `0x64` | message offset `+0x48` |
| `sendGoNorth` | `0x65` | message offset `+0x48` |
| `sendMoveObject` | `0x78` | message offset `+0x48` |
| `sendTradeObject` | `0x7d` | helper `0xbc6e20` writes offset `+0x38` |
| `sendTalkMessage` | `0x96` | message offset `+0x48` |
| `sendAttack` | `0xa1` | helper `0xbc6e20` writes offset `+0x38` |
| `sendFollow` | `0xa2` | helper `0xbc6e20` writes offset `+0x38` |

`0xbc6e20` sets the message presence/dirty flag at `+0x28`, stores the supplied discriminator at `+0x38`, then invokes the receiver/interface virtual method at vtable offset `+0x68` with the owning message pair.

These constants are proven internal `GameclientMessage` discriminators. They are not yet promoted to final wire bytes because the exact serializer framing/encoding path downstream of `sendMessage` has not been structurally closed.

## Send convergence

QMeta index 0 (`sendMessage`) enters at `0xdf7930` and calls body `0xde6de0`. Index 194 (`prepareAndEnqueueGameclientMessage`) enters at `0xdf6b99`, copies the owning message and calls `0xbc6e20`. Indices 191–193 converge on queue-processing helpers `0xde91b0`, `0xbc6f00`, and `0xbc6750` respectively. These are the next exact serializer/network convergence targets.
