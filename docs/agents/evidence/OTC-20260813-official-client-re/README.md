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

Current continuation rule:

```text
Verify actual in-world state first before any live-world mutation experiment.
If logged out/server-save/crashed, use the canonical full restart/login recipe.
Do not use pre-world GDB attach or bypass BattlEye.
Post-login, preserve the promoted dynamic-map observer until a controlled mutation is available.
For protocol/action RE, prefer the exact relocation-backed QMeta records, metadata method indices and bounded case entries over string proximity.
TCreatureProtocolMessageHandler has zero own QMeta methods in this exact version; recover creature routing through the actual upstream/base/direct protocol path rather than inventing handler cases.
Do not promote message names as wire opcodes or field layouts.
Do not write every observed world object directly into canonical OTBM.
```
