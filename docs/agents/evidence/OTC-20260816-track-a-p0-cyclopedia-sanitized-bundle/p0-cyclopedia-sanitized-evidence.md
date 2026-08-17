# P0 Cyclopedia sanitized exact-client evidence

Task: `OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle`  
Consumer: PR #302 / `OTC-20260815-track-a-p0-direct-position`  
Producer: PR #435  
Final producer source run: `32000921225`  
Producer source head: `40b5efd2f6371b8f5c0a00036084960ab66eefd0`  
Consumer-facing artifact: `9278368790` / `track-a-p0-cyclopedia-sanitized-32000921225`  
Artifact ZIP digest: `sha256:49f48d4283e63dd613b32a99300dc86eb98d68d7d7f640ec621c72e854c30c87`

## Boundary and exact fence

This is bounded static evidence staging only. The source stage read one already-retained exact official Linux client file; it did not launch the client, inspect process memory, consume canonical runtime state, log in, perform gameplay, or upload the raw client. GitHub-hosted validation rendered only the bounded code windows exported by the source stage.

Exact fence:

- version: `15.32.df7b29`
- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- hosted validation: `PASS`
- runtime access: `none`
- client executed: `false`
- process memory accessed: `false`
- canonical runtime accessed: `false`
- network accessed: `false`
- raw client uploaded: `false`
- semantic player XYZ proven: `false`
- physical confirmation owner: `RUNTIME`

The final artifact contains exactly four unique RIP-relative xrefs and four hosted disassembly windows. Run #6 (`31973213388`) is superseded because its scanner counted a REX-prefixed `LEA` twice; final run #7 deduplicates the prefixed instruction and is the only accepted bundle.

## Facts recovered from the exact client

All nine requested target labels are present. Relevant exact string virtual addresses include:

| Target | Exact-client virtual address(es) |
|---|---|
| `N5tibia10cyclopedia21TCyclopediaMapStorageE` | `0x1cdda40` |
| `tibia::cyclopedia::TCyclopediaMapStorage` | `0x1d2a580`, `0x1d2a8d8` |
| `onPlayerCreatureAddedToGameSession` | `0x1d2aa4a`, `0x1d70542` |
| `std::weak_ptr<tibia::creatures::TCreature>` | includes `0x1d2aa6d` |
| `pPlayer` | includes `0x1d2aa98` |
| `onPlayerPositionWasUpdated` | `0x1d2aaa0` |
| `playerPositionChanged` | `0x1d2a937` |
| `tibia::worldmap::TWorldMapCoordinate` | includes `0x1d2a95d` |
| `onPlayerPositionChanged` | includes `0x1d2a4f5` |

The compact `0x1d2a8d8`–`0x1d2aaa0` metadata/string neighborhood therefore contains, in order, `TCyclopediaMapStorage`, `playerPositionChanged`, `TWorldMapCoordinate`, `onPlayerCreatureAddedToGameSession`, the weak-player type, `pPlayer`, and `onPlayerPositionWasUpdated`. This is a static metadata-neighborhood fact; it is not by itself an object-layout or callback-implementation proof.

Four exact `.rela.dyn` references were recovered:

- `0x3089a58 -> 0x1cdda40` — `TCyclopediaMapStorage` RTTI name.
- `0x3138ef8 -> 0x1c91120` — `TWorldMapCoordinate` string instance.
- `0x31393f8 -> 0x1c93260` — `weak_ptr<TCreature>` string instance.
- `0x31516b8 -> 0x1d2a580` — `TCyclopediaMapStorage` metadata string instance.

RTTI graph recovery derives:

- typeinfo candidate: `0x3089a50`
- vtable address point: `0x3089db0`
- typeinfo relocation slot for that vtable: `0x3089da8`

Four unique code xrefs were recovered:

- `0x812952 -> 0x3089db0`
- `0x812e12 -> 0x3089db0`
- `0xd299ed -> 0x1d2a8d8`
- `0xeb0ea2 -> 0x3089db0`

At `0x812952`, code loads `0x3089db0` and stores it at the object base (`[rdi-0x418]` after `rdi += 0x418`). A second structurally similar path exists at `0x812e12`.

At `0xeb0ea2`, code loads `0x3089db0`, immediately stores it to `[rbx]`, then initializes a long sequence of member-relative pointer pairs (`+0x38/+0x40`, `+0x68/+0x70`, `+0x98/+0xa0`, and onward). This is strong structural evidence for an object initialization path associated with the recovered `TCyclopediaMapStorage` vtable address point. It does not establish player-position semantics by itself.

At `0xd299ed`, code loads the exact `TCyclopediaMapStorage` metadata address `0x1d2a8d8` and passes it into a nearby helper call. This is a direct executable reference to that metadata instance.

## Classification for P0

**FACT:** the requested player/Cyclopedia strings, RTTI name, typeinfo candidate, vtable address point, relocations, and four unique code xrefs above are present in the exact fenced client.

**STRUCTURAL_DERIVATION:** the `0xeb0ea2` path is an object initializer associated with the recovered `TCyclopediaMapStorage` vtable graph; the two `0x8129xx/0x812exx` paths also install the same vtable address point while operating on a large object.

**UNKNOWN:** this bundle does not prove which exact executable functions implement `onPlayerPositionWasUpdated`, `playerPositionChanged`, `onPlayerPositionChanged`, `pPlayer`, or `onPlayerCreatureAddedToGameSession`. Direct code xrefs to those specific strings were not recovered by the bounded scanner. Their co-location in metadata is a route for further static analysis, not semantic proof.

**UNKNOWN / RUNTIME-owned:** semantic player XYZ values, their in-process storage, world-coordinate correlation, negative controls, repeatability, and fresh-PID/relogin stability. Only the RUNTIME lane may promote those physical claims.

## Consumer handoff

P0 #302 can now consume this bundle as exact-client structural evidence and continue from the `TCyclopediaMapStorage` RTTI/vtable/object-initialization graph plus the compact player-position metadata neighborhood. It must keep physical XYZ claims separate until RUNTIME supplies independent physical confirmation.

## File integrity

- `bundle-summary.txt`: `sha256:af1f307660bb18f6529dfc2919feba27f2b516e0b7556e6caa5152053e8b7653`
- `bundle.json`: `sha256:a537891368c0bb8888ed8caeca3bbfc9fc910d9c37bc2a1e852188eb4671b4a6`
- `cyclopedia-code-windows.txt`: `sha256:f660005cc2a8fef15ac35ba891430cb67157ee45f5a282d05ad884ae60368002`
- `hosted-validation.json`: `sha256:103c0d092fbf650b849205d4e648636ba5010706a4eeacf61810415a6dfe7591`
- `hosted-validation.txt`: `sha256:49ddc67ae0d175e56e2dd256c06d04e983f31dfbc323e879fca7257f150eded6`

## Closeout audit

Fresh coordinator audit reviewed the final consumer artifact itself, the final source/hosted run, and the intended producer diff. No blocking material finding remains after the REX-prefix duplicate-xref correction. The one-shot source workflow is not part of the terminal tree. This task is static evidence staging, so user-facing runtime E2E is `NOT_APPLICABLE_WITH_REASON`; physical XYZ E2E is a separate RUNTIME-owned acceptance surface rather than an unexecuted requirement of this producer.
