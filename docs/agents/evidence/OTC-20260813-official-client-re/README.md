# Track A official Linux client RE — evidence index

Repository: `blakinio/otclient`
Track: Track A / `official-client-re`

Read these checkpoints chronologically and treat newer directly verified evidence as superseding older hypotheses:

1. `20260813-canonical-artifact-correction.md`
   - corrects the original false-positive world-entry claim;
   - records the launcher/package-state recovery;
   - records the first visually verified real world entry;
   - contains the reproducible canonical login recipe.

2. `20260814-map-observation-and-dynamic-provenance-checkpoint.md`
   - records post-login structural map observation;
   - proves current-floor aware range `18x14` versus visible viewport `15x11`;
   - records structured `(x,y,z,stack,type_id)` extraction without OCR;
   - proves `+0x19a8ea3` is insufficient for dynamic changes on already-aware tiles;
   - records the BattlEye/early-GDB boundary and OTBM provenance requirements.

3. `20260814-dynamic-map-callback-live-discrimination.md`
   - records live discrimination of dynamic map callback candidates;
   - preserves the exact-version boundary for the promoted dynamic observer.

4. `20260814-official-client-protocol-surface-inventory.md`
   - exact-binary inventory of 47 `ProtocolMessageHandler` classes, 146 `handle*Message` names, 189 inbound and 160 outbound protocol message names;
   - establishes broad structural coverage without claiming opcodes/layouts from names alone.

5. `20260814-protocol-handler-qmeta-neighborhoods.md`
   - records early compact class-local method-name clusters and the stripped-symbol negative result;
   - treat its unresolved Creature/Player statements as historical: later relocation-backed QMeta evidence supersedes them where applicable.

6. `20260814-capability-observation-matrix.md`
   - conservative capability matrix separating presence, dispatch proof, layout proof and runtime proof.

7. `20260814-protobuf-descriptor-census-and-xref-gate.md`
   - recovers `Coordinate.x/y/z = fields 1/2/3 uint32`;
   - records seven embedded `FileDescriptorProto` files;
   - closes direct literal-qword/direct-RIP xref hypotheses and establishes the ELF-relocation route.

8. `20260814-qmeta-relocation-record-layout.md`
   - reconstructs the relocation-backed 0x40-byte QMeta record family;
   - calibrates `+0x18` as the static-metacall field using independently known Worldmap dispatch;
   - recovers exact static-metacall entries for Worldmap, Chat, GameEvent, Effect and Container-family candidates.

9. `20260814-qmeta-string-and-method-table-decode.md`
   - decodes QMeta `(offset,length)` stringdata tables and revision-13 metadata headers;
   - proves the real Container record and `static_metacall=+0xd1e000`;
   - recovers exact method ordering for the calibrated handlers.

10. `20260814-qmeta-handler-census-and-dispatch-map.md`
   - complete relocation-backed census recovers all 47 protocol-handler QMeta records;
   - proves `TPlayerProtocolMessageHandler static_metacall=+0xd1a920` with 22 movement/path/rotation/world-entry methods;
   - proves `TCreatureProtocolMessageHandler` has a valid record but zero own QMeta methods;
   - maps exact Chat and Container QMeta method indices to executable case entries and bounded direct-tail targets;
   - fixes the first jump-tail scanner's cross-case false-positive risk.

11. `20260814-gameaction-qmeta-dispatch-map.md`
   - recovers the exact QMeta method counts/indices and dispatch forms for high-value outbound GameAction handlers;
   - proves executable case entries for Attack, Follow, Talk, Container/WorldMap MoveObject and TradeObject;
   - records and rejects the superseded mapper that used incorrect hard-coded jump tables.

12. `20260814-high-value-outbound-signal-disassembly.md`
   - proves the six mapped `send*` cases are Qt signal-emission wrappers calling `QMetaObject::activate`, not direct protocol serializers;
   - records their exact static metaobjects and signal indices;
   - corrects the prior Player `+0xd1abc0` sender hypothesis: it is only a shared epilogue/return point;
   - redirects the next RE gate to signal-to-receiver connection recovery.

13. `20260814-qt-connect-callsite-census.md`
   - enumerates 2,184 direct calls to three exact Qt connect/disconnect PLT targets;
   - separates 2,078 `connectImpl`, 41 legacy string-based `connect`, and 65 `disconnectImpl` calls;
   - preserves the boundary that callsites alone do not identify semantic signal/slot edges;
   - selects the bounded 41-call legacy neighborhood reconstruction as the next experiment.

14. `20260814-gameaction-connectimpl-arguments.md`
   - corrects the effective ABI for the hidden `QMetaObject::Connection` return pointer;
   - reconstructs argument-source patterns for all 31 tightly correlated `connectImpl` sites;
   - proves 29 nearby GameAction metaobjects are actual sender metaobjects and retains two explicit exceptions.

15. `20260814-gameaction-slot-provenance.md`
   - resolves the QSlotObject invoke-function address for all 29 proven sender sites;
   - proves the selected invoke functions are generic operation/pointer-to-member dispatchers rather than receiver serializers;
   - redirects concrete receiver recovery to the two-word slot payload.

16. `20260814-protocol-queue-action-builders.md`
   - identifies `TProtocolMessageQueue`, its 355-method QMeta table and exact selected method indices;
   - maps movement, MoveObject, Talk, Attack, Follow and TradeObject case entries to concrete builder bodies;
   - recovers exact internal message discriminators while retaining the wire-byte boundary until serializer convergence.

17. `20260814-live-structural-world-and-reversible-movement.md`
   - correlates the owned exact-client world session with decoded map-strip execution;
   - proves one north step and inverse south step, with the derived path `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)`;
   - preserves the boundary between authoritative strip coordinates and the viewport-center-derived player coordinate.

18. `20260814-protocol-queue-network-handoff.md`
   - proves `clientMessageReadyToProcess` hands the queue to its containing owner through virtual slot `+0x90`;
   - ties the containing-owner setup path to `QTcpSocket` construction;
   - retains the exact serializer/framing function and final wire bytes as unknown pending concrete-slot recovery.

Current continuation rule:

```text
Verify actual in-world state first before any live-world mutation experiment.
If logged out/server-save/crashed, use the canonical full restart/login recipe.
Do not use pre-world GDB attach or bypass BattlEye.
Post-login, preserve the promoted dynamic-map observer until a controlled mutation is available.
For protocol/action RE, prefer the exact relocation-backed QMeta records, metadata method indices and bounded case entries over string proximity.
TCreatureProtocolMessageHandler has zero own QMeta methods in this exact version; recover creature routing through the actual upstream/base/direct protocol path rather than inventing handler cases.
Treat GameAction `send*` QMeta cases as signal emitters until their connected receiver/slot is directly recovered; do not label their shared epilogues as serializers.
Do not promote message names as wire opcodes or field layouts.
Do not write every observed world object directly into canonical OTBM.
```
