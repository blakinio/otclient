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
   - records the controlled second-player item provenance experiments;
   - proves `+0x19a8ea3` is insufficient for dynamic changes on already-aware tiles;
   - records the BattlEye/early-GDB boundary;
   - records binary-analysis progress and current dynamic mutation candidates `+0xcecc70` and `+0xcecf40`;
   - defines the provenance architecture required before writing canonical OTBM;
   - defines the exact next controlled experiment.

3. `20260814-dynamic-map-callback-live-discrimination.md`
   - records live discrimination of dynamic map callback candidates;
   - preserves the exact-version boundary for the promoted dynamic observer.

4. `20260814-official-client-protocol-surface-inventory.md`
   - exact-binary inventory of `ProtocolMessageHandler`, `handle*Message`, inbound `GameserverMessage*` and outbound `GameclientMessage*` surfaces;
   - establishes broad structural coverage for map, creature, player, inventory/container, chat, party, trade, market, quest, effects and native actions;
   - does not claim opcodes, layouts or callable offsets from names alone.

5. `20260814-protocol-handler-qmeta-neighborhoods.md`
   - maps compact class-local method-name clusters for Chat, Container, Effect, Market, NPC Trade, Player Trade, Quest and Game Event;
   - records that stripped symbols do not expose `qt_static_metacall` / `staticMetaObject` directly;
   - keeps Creature/Player handler ownership unresolved where proximity is ambiguous.

6. `20260814-capability-observation-matrix.md`
   - converts the proven exact-binary surfaces into a conservative observation/action capability matrix;
   - separates `present`/`clustered` evidence from still-unknown executable offsets, field layouts and runtime invocation proof;
   - prioritizes MoveCreature/player state/chat/container and movement/MoveObject/Attack/Follow/Trade builder gates.

7. `20260814-protobuf-descriptor-census-and-xref-gate.md`
   - records the successful revision-2 census of embedded `FileDescriptorProto` records;
   - directly recovers `Coordinate.x/y/z` as fields `1/2/3`, all `uint32`;
   - proves selected game protocol message schemas are not present in the seven embedded file descriptors and must be recovered from generated C++ metadata/accessors/disassembly;
   - records the completed-output/cancelled-job boundary of xref v1 and rejects the tested literal-string absolute-qword route;
   - introduces the linear xref-v2 replacement gate.

Current continuation rule:

```text
Verify actual in-world state first before any live-world mutation experiment.
If logged out/server-save/crashed, use the canonical full restart/login recipe.
Do not use pre-world GDB attach or bypass BattlEye.
Post-login, preserve the promoted dynamic-map observer until a controlled mutation is available.
For protocol/action RE, prefer exact-binary static metadata/xref mapping before any invasive runtime action.
Do not promote string offsets as function offsets and do not promote message names as wire opcodes or field layouts.
Do not write every observed world object directly into canonical OTBM.
```
