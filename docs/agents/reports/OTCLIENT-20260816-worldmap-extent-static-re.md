# OTCLIENT-TIBIA-RE — worldmap extent static dependency recovery

```yaml
report_date: 2026-08-16
repository: blakinio/otclient
track: official-client-re
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
subject: official native Linux Tibia client only
implementation_status: NOT_IMPLEMENTED
client_byte_mutation: NOT_PERFORMED
live_runtime_access: NOT_PERFORMED
final_static_classification: BLOCKED
blocker_class: INPUT_BLOCKED
```

## Result

The requested full patch/dependency graph could **not** be completed in this phase because the exact fenced executable cannot currently be staged on the required GitHub-hosted analysis surface.

This is an input/infrastructure blocker, not evidence that runtime observation is required.

The task did recover and normalize the maximum safe static frontier available from already-retained exact-client evidence, identified two structural RTTI-name relocation leads, preserved every unresolved graph edge explicitly as `UNKNOWN`, and performed one materially different GitHub-hosted staging experiment. That experiment failed before analyzer installation/execution and before any client-byte analysis.

```yaml
FACT:
  - the exact historical artifact proves all eight requested semantic/type surfaces exist in client 15.32.df7b29
  - retained relocation metadata links .data.rel.ro locations 0x3089b78 and 0x308b598 to the TWorldMapRenderProvider and TWorldMapViewport RTTI-name strings respectively
  - current GitHub-hosted staging remains unavailable after prior DNS/HTTP-403 evidence plus an independent same-URL-Referer failure
  - no new static analysis ran on Synology
  - no live client, X11, VNC, login/session or runtime mutation was used
  - no client bytes were modified
INFERENCE:
  - 0x3089b70 and 0x308b590 are ABI-shaped candidate typeinfo-object starts only; they are not proven typeinfo/vtable addresses
UNKNOWN:
  - exact extent/subfield/viewport dimension fields
  - constructor/default writers and all material readers/writers
  - fixed allocations/capacities and loop bounds
  - protocol row/column/floor parser assumptions
  - storage indexing/eviction limits
  - render clipping/culling/iteration limits
  - camera projection/scale coupling
  - picker bounds/coordinate-transform limits
  - concrete patch sites and isolated-change consequences
NOT_PROVEN:
  - that 18/14 are literal static dimension constants
  - that one constant or one object field controls the map size
  - that 26x20, 32x24 or 36x28 is safe/supported
  - that the official server supplies a larger live-awareness area
```

## Exact evidence boundary

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

The accepted feasibility checkpoint is on `main` in:

- `docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md`;
- `docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/20260816-evidence.md`.

This continuation's detailed static frontier is in:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-static-frontier.md`.

## Partial target graph

| Target | Proven structural surface | Remaining graph status |
|---|---|---|
| `TWorldMapExtent` | exact RTTI-name string `0x1c8fee0`; `TWorldMapExtentX` semantic string `0x1cd9ad7` | fields/writers/readers/vtable UNKNOWN |
| `TWorldMapSubfieldExtent` | exact RTTI-name string `0x1c9fe20` | fields/writers/readers/vtable UNKNOWN |
| `TWorldMapViewport` | exact names `0x1cabb60`, `0x1ce1b60`; relocation `0x308b598 -> 0x1ce1b60` | typeinfo candidate only; fields/writers/readers/clipping UNKNOWN |
| `TWorldMapStorage` | exact names `0x1ca9180`, `0x1ce1c00` | layout/capacity/index/cache/consumers UNKNOWN |
| `TWorldmapProtocolMessageHandler` | exact/plain/shared ownership names `0x1cd59a0`, `0x1cd67a0`, `0x1cd8bb4`, `0x1cdba40` | parser loops/floor-row-column assumptions/storage writes UNKNOWN |
| `TWorldMapRenderProvider` | exact names `0x1cdb580`, `0x1cddd20`; relocation `0x3089b78 -> 0x1cddd20` | typeinfo candidate only; render loops/clipping/culling UNKNOWN |
| `TWorldMapCamera` | exact names `0x1cabce0`, `0x1cabd20` | layout/projection/viewport dependency UNKNOWN |
| `TWorldMapPicker` | exact names `0x1cdb600`, `0x1cdb640` | bounds/picking transform/extent dependency UNKNOWN |

Additional retained semantic leads include `onCameraViewportChanged`, `onPlayerPositionChanged`, `TWorldMapCoordinate`, `TMapScaleFactor` and `MapScaleFactor`. They remain names, not promoted call edges.

## Why the graph stops here

The historical exact-binary static artifact `9248797952` was deliberately sanitized for a different P0 question. It preserves exact SHA/size, semantic strings and a small relocation/disassembly neighborhood, but it does **not** contain the worldmap constructors, full vtables, function xrefs or arbitrary `.text/.data.rel.ro` bytes needed to recover this task's object-field and consumer graph.

Its generating job `95029600292` ran historically on `synology-otclient-01`. The user explicitly required new static RE to run GitHub-hosted and forbade using Synology merely because it is available. This task therefore reused the retained artifact read-only and did not rerun/extend static analysis there.

## Hosted input attempts

Prior PR `#310` already established two non-working hosted source paths:

- `download.tibia.com`: DNS failure;
- plain automated `static.tibia.com/download/tibia.x64.tar.gz`: HTTP 403.

This task made exactly one materially different attempt in run `31947523640`, job `95165795953`: compressed transfer with a same-URL Referer. It still classified `INPUT_BLOCKED`; analyzer dependency installation and graph recovery were skipped. Cleanup and sanitized evidence upload succeeded, artifact `9263709952`.

Independent P0 run `31947502633`, job `95165743019`, independently reproduced the same same-URL-Referer input failure on `ubuntu-latest`, artifact `9263704543`.

A public GitHub release source already used by PR `#97` was also inspected, but its published original-Linux inventory did not expose the exact `15.32.df7b29` build. No acceptable exact-version/SHA source was found through the available GitHub repository search.

No further HTTP-variant retry was attempted.

## Current patch/dependency graph status

```text
TWorldMapExtent / TWorldMapSubfieldExtent / TWorldMapViewport
        semantic identity: PROVEN
        concrete dimension fields: UNKNOWN
        default writers: UNKNOWN
        material readers/writers: UNKNOWN
             |
             +--> TWorldMapStorage
             |      object identity: PROVEN
             |      allocation/capacity/indexing/eviction: UNKNOWN
             |
             +--> TWorldmapProtocolMessageHandler
             |      object identity: PROVEN
             |      parser row/column/floor loops and strip assumptions: UNKNOWN
             |
             +--> TWorldMapRenderProvider
             |      object identity + RTTI-name relocation lead: PROVEN_PARTIAL
             |      render loops/clipping/culling/batching: UNKNOWN
             |
             +--> TWorldMapCamera
             |      object identity: PROVEN
             |      projection/scale/viewport dependency: UNKNOWN
             |
             +--> TWorldMapPicker
                    object identity: PROVEN
                    picking bounds/coordinate transforms: UNKNOWN
```

This is deliberately **not** presented as a usable patch graph. A safe mutation cannot be designed from semantic identities alone.

## Classification

Final classification for this task invocation:

```text
BLOCKED
```

Specific blocker:

```text
INPUT_BLOCKED: exact 15.32.df7b29 native-Linux executable is not currently available to GitHub-hosted Actions through a compliant source, while Synology static fallback is forbidden.
```

`RUNTIME_DISCRIMINATOR_REQUIRED` is false at this point. The missing facts are still static facts and should be recovered statically once exact input is available.

## Required unblocker

The smallest correct unblocker is a legally/technically compliant GitHub-hosted-readable source for the exact fenced official client, without committing proprietary bytes and without routing static analysis through Synology.

Once that exists, the next static run should recover, in order:

1. typeinfo/vtable groups and constructor/destructor candidates for extent/subfield/viewport;
2. candidate dimension/edge fields and all writes/reads;
3. storage allocation/index/cache dependencies;
4. protocol parser row/column/floor/strip dependencies;
5. render/camera/picker clipping, culling and transform dependencies;
6. fixed allocations, stack arrays, masks, packing widths and loop bounds;
7. the final table `field/constant -> writers -> readers -> allocations -> protocol -> render -> isolated-change consequence`.

Only after that table is coherent should a separate client-byte mutation task exist.

## Runtime and safety boundary

No GUI/runtime escalation is justified by the present evidence. This task performed none of the following:

- no Synology static RE;
- no new or existing X11 session access;
- no VNC/noVNC access or creation;
- no Tibia login/relogin/session takeover;
- no process inspection of a live client;
- no Gate A/Gate B bypass;
- no client-byte modification;
- no owner Codex/OpenAI API/token/paid AI use.

If a future, genuinely runtime-only discriminator appears after static recovery, it must be a separate governance decision against then-current Track A ownership/admission state and the user's persistent-desktop reuse constraints.
