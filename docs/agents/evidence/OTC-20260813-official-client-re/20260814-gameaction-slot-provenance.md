# GameAction QSlotObject provenance

## Scope

- Official Linux client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Provenance run `31801723690`, job `94771021150`, on `synology-otclient-01`.
- Invoker disassembly run `31801845276`, job `94771408713`.
- Input was restricted to the 29 `connectImpl` sites where the GameAction metaobject is proven to be stack argument 9.

## Provenance result

All `29/29` sites have a bounded, mechanically recovered `QSlotObject` invoke-function address. There are 24 unique addresses:

- `0x6b10d0` is shared by five sites whose sender families are Creatures, PlayerTrade, Player, Chat and Container.
- `0x7d1780` is shared by two Player sites.
- The remaining 22 sites each use a distinct invoke-function address.
- No invoke-function address remains unresolved after a 4096-byte backward provenance window.

Selected high-value mappings:

| Connect call | Sender family | QSlotObject invoke address |
| --- | --- | --- |
| `0x7d6876` | Creatures | `0x7d31e0` |
| `0x7d7857` | WorldMap | `0x7d23d0` |
| `0x7d8b66` | PlayerTrade | `0x7d1300` |
| `0x7ff2c3` | Creatures | `0x6b10d0` |
| `0x7ff3e1` | PlayerTrade | `0x6b10d0` |
| `0x7ff58e` | Chat | `0x6b10d0` |
| `0x7ffb24` | Container | `0x6b10d0` |

## Invoker semantics

Disassembly proves that `0x6b10d0`, `0x7d31e0`, `0x7d23d0`, and `0x7d1300` are structurally equivalent `QtPrivate::QSlotObjectBase` operation dispatchers, not action-specific receiver functions:

- operation `0` deletes the 32-byte slot object;
- operation `2` performs comparison support;
- operation `1` loads the stored pointer-to-member target from slot-object offsets `+0x10/+0x18`, adjusts the receiver, optionally resolves a virtual member, and tail-jumps through the recovered target register;
- the argument payload is forwarded from the Qt activation argument array.

Therefore the invoke-function address is a template/trampoline identity. Sharing `0x6b10d0` does not prove a shared receiver object, action handler, serializer, message builder or wire path. The concrete executable receiver is encoded in the slot object's two-word payload and must be reconstructed from the writes later copied to offsets `+0x10/+0x18`.

## Preserved source expressions

The provenance run also records, for every site, the final sender, signal-storage, receiver, slot-storage and slot-object register/frame expressions. These expressions are structural evidence but are not promoted to concrete class identities without constructor or RTTI provenance.

## Next boundary

Recover the two-word slot payload for the high-value sender sites. Resolve a direct first word as the concrete receiver target; when its low bit marks a virtual member, recover the vtable entry after applying the stored receiver adjustment. Only then follow the receiver toward builder/serializer/network convergence.

