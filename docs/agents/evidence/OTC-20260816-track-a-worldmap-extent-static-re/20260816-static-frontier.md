# OTC-20260816-track-a-worldmap-extent-static-re — static frontier evidence

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
track: official-client-re
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
execution_class: github_hosted
runtime_access: none
client_mutation: false
owner_funded_ai_api_authorized: false
final_static_classification: BLOCKED
blocker_class: INPUT_BLOCKED
```

This evidence file contains only compact structural metadata and repository/run identifiers. It contains no Tibia executable bytes, assets, credentials, authenticated captures or live process state.

## Governance and ownership preflight

FACT:

- current `main` was rechecked immediately before this checkpoint and had advanced to `dbd9520e2f8cc5a26f556bffaae2a83e139615f9` via coordinator-only shared-index serialization (`#370`);
- PR `#325` is closed/unmerged as superseded; its accepted feasibility content was replayed and merged by PR `#365`;
- PR `#366` archived the completed feasibility task and released its ownership;
- PR `#363` still owns only the viewport-continuation prompt/task paths and was treated read-only;
- PR `#310` remains the canonical P2 hosted-input-staging blocker and was treated read-only;
- this task owns only its task record, analyzer path, evidence path and report path;
- the current coordinator classifies P2 as `BLOCKED_INPUT_STAGING` with the next dependency being a legally and technically compliant GitHub-hosted-readable exact-client source and explicitly says `no Synology fallback`.

No live observation or mutation was performed by this task. `Gate A`, generation rebind, `Gate B`, bootstrap and target uniqueness therefore remained `NOT_APPLICABLE` rather than being bypassed.

## Exact client fence

All exact-client structural claims remain fenced to:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

## Historical exact-binary artifact reused read-only

The continuation prompt points to historical run `31892019505`, artifact `9248797952` (`track-a-p0-static-elf-31892019505`, digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`). Its `static-elf-re.txt` proves:

```text
TRACK_A_P0_EXACT_CLIENT_FENCE=true
TRACK_A_P0_CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_P0_CLIENT_SIZE=51965216
```

The corresponding historical job is `95029600292` (`static-elf-re`). Repository Actions metadata shows it ran on `synology-otclient-01`, labels `[otclient, synology]`.

Claim boundary:

```yaml
historical_exact_binary_evidence_reused: true
current_exact_binary_reexecution: NOT_PERFORMED
current_exact_binary_provenance_upgraded: false
new_synology_static_execution_by_this_task: false
```

The historical sanitized evidence is valid input because it was already retained and explicitly referenced by the continuation, but it is not represented as a fresh GitHub-hosted exact-binary run.

## Exact semantic/type inventory recovered from retained artifact

### TWorldMapExtent

PROVEN exact semantic names:

```text
0x1c8fee0  N5tibia8worldmap15TWorldMapExtentE
0x1cd9ad7  tibia::worldmap::TWorldMapExtentX
```

UNKNOWN: constructor/destructor, typeinfo object address, vtable address/slots, object size, width/height/edge field offsets, default writers, material readers.

### TWorldMapSubfieldExtent

PROVEN exact semantic name:

```text
0x1c9fe20  N5tibia8worldmap23TWorldMapSubfieldExtentE
```

UNKNOWN: constructor/destructor, typeinfo/vtable, object size, subfield dimensions/edges, all writers/readers.

### TWorldMapViewport

PROVEN exact semantic names:

```text
0x1cabb60  St23_Sp_counted_ptr_inplaceIN5tibia8worldmap17TWorldMapViewport...
0x1ce1b60  N5tibia8worldmap17TWorldMapViewportE
```

PROVEN relocation metadata from retained `player-position-graph.txt`:

```text
0x308b598 -> 0x1ce1b60  .rela.dyn  owner=.data.rel.ro
```

This proves a relocated pointer to the RTTI-name string, not by itself a vtable or complete typeinfo object.

INFERENCE / ABI hypothesis only: under the usual Itanium C++ ABI typeinfo shape, `0x308b590` is a candidate object start because the name pointer is commonly stored at `+8`. The retained artifact does not preserve enough adjacent qwords/consumer evidence to promote that candidate.

UNKNOWN: vtable, constructors, dimension/edge fields, viewport clipping rectangle, writers/readers.

### TWorldMapStorage

PROVEN exact semantic names:

```text
0x1ca9180  St23_Sp_counted_ptr_inplaceIN5tibia8worldmap16TWorldMapStorage...
0x1ce1c00  N5tibia8worldmap16TWorldMapStorageE
```

UNKNOWN: storage object layout, backing container/capacity, subfield allocation policy, eviction/retention policy, indexing/coordinate packing, allocation limits and all extent-dependent readers.

### TWorldmapProtocolMessageHandler

PROVEN exact semantic names:

```text
0x1cd59a0  N5tibia8worldmap31TWorldmapProtocolMessageHandlerE
0x1cd67a0  tibia::worldmap::TWorldmapProtocolMessageHandler
0x1cd8bb4  tibia::worldmap::TWorldmapProtocolMessageHandler
0x1cdba40  St23_Sp_counted_ptr_inplaceIN5tibia8worldmap31TWorldmapProtocolMessageHandler...
```

Additional PROVEN semantic lead:

```text
0x1cb3ae1  handleAddBeneathMiddleWorldmapMessageGameAction
```

UNKNOWN: handler vtable, message parser entry points, row/column/floor loop bounds, fixed packet/map allocations, strip dimensions, inclusive/exclusive edge math and storage write path.

### TWorldMapRenderProvider

PROVEN exact semantic names:

```text
0x1cdb580  St23_Sp_counted_ptr_inplaceIN5tibia8worldmap23TWorldMapRenderProvider...
0x1cddd20  N5tibia8worldmap23TWorldMapRenderProviderE
```

PROVEN relocation metadata:

```text
0x3089b78 -> 0x1cddd20  .rela.dyn  owner=.data.rel.ro
```

This is a pointer to the RTTI-name string, not standalone proof of a vtable/typeinfo object.

INFERENCE / ABI hypothesis only: `0x3089b70` is a candidate typeinfo-object start under the common Itanium layout; adjacent structural evidence is not preserved strongly enough to promote it.

UNKNOWN: vtable, render-loop bounds, visible tile iteration, clipping/culling, batching/allocation limits and exact dependency on viewport/extent/storage.

### TWorldMapCamera

PROVEN exact semantic names:

```text
0x1cabce0  N5tibia8renderer15TWorldMapCameraE
0x1cabd20  St23_Sp_counted_ptr_inplaceIN5tibia8renderer15TWorldMapCamera...
```

UNKNOWN: camera object layout, viewport projection fields, clipping dimensions, zoom/scale coupling and consumers.

### TWorldMapPicker

PROVEN exact semantic names:

```text
0x1cdb600  N5tibia8worldmap15TWorldMapPickerE
0x1cdb640  St23_Sp_counted_ptr_inplaceIN5tibia8worldmap15TWorldMapPicker...
```

UNKNOWN: picker object layout, screen-to-world bounds, clipping/selection iteration and larger-extent assumptions.

## Cross-surface semantic leads retained on main

The merged feasibility evidence additionally records these exact-artifact local strings:

```text
0x1d2a48a  onCameraViewportChanged
0x1d2a4f5  onPlayerPositionChanged
0x1d2a95d  tibia::worldmap::TWorldMapCoordinate
0x1d2a9ae  TMapScaleFactor
0x1d2a9be  MapScaleFactor
```

PROVEN: the names are present in the exact retained artifact.

NOT_PROVEN: any specific call edge between those names and the eight target classes. A semantic-name neighborhood is not promoted into a call/dependency edge without disassembly/xref evidence.

## Historical geometry evidence boundary

The merged feasibility checkpoint preserves an `18 x 14` baseline interpretation only as:

```yaml
classification: DERIVED_FROM_OBSERVED_JOB_LOG
confidence: high
raw_rows_preserved_in_consumed_artifact: false
```

`33` and `88` are cumulative strip counts, not dimensions. Candidate `26x20`, `32x24` and `36x28` sizes remain test targets only.

No static claim in this task treats literal `18` or `14` as a dimension field/patch site.

## GitHub-hosted exact-input staging frontier

### Prior P2 attempts (read-only reuse)

PR `#310` already records:

1. `download.tibia.com` attempt -> DNS resolution failure;
2. plain automated `static.tibia.com/download/tibia.x64.tar.gz` attempt -> HTTP 403.

Those attempts were not repeated blindly.

### This task's one materially different hosted attempt

Workflow run `31947523640`, head `7aee21b5659026b7b025b377e0d07ce478b968c2`, job `95165795953`, runner `ubuntu-latest` / GitHub Actions:

```yaml
Verify GitHub-hosted no-runtime boundary: SUCCESS
Materialize exact official Linux client with referer-aware request: FAILURE
Install static analyzer dependencies: SKIPPED
Recover worldmap extent dependency graph: SKIPPED
Remove proprietary input before evidence upload: SUCCESS
Upload sanitized static evidence only: SUCCESS
```

Artifact `9263709952`, `track-a-worldmap-extent-static-31947523640`, digest `sha256:87315733a626bd0d2f8540bc05b0aa5bcd1fcd33d78764be6dc0243a30ae837f`, contains exactly the classification:

```text
WORLDMAP_STATIC_INPUT_STATUS=INPUT_BLOCKED
WORLDMAP_STATIC_INPUT_REASON=referer_aware_official_archive_download_failed
WORLDMAP_STATIC_INPUT_URL=https://static.tibia.com/download/tibia.x64.tar.gz
WORLDMAP_STATIC_INPUT_STRATEGY=official_static_tibia_same_url_referer_compressed
```

No exact-client analysis step ran in this attempt.

### Independent P0 corroboration

Run `31947502633`, job `95165743019` (`hosted-static-position-re`) ran independently on `ubuntu-latest` and also failed only at `Materialize exact official client read-only`; its analysis step was skipped, cleanup succeeded and sanitized upload succeeded.

Artifact `9263704543` contains:

```text
P0_HOSTED_INPUT_STATUS=INPUT_BLOCKED
P0_HOSTED_INPUT_REASON=official_archive_download_failed_with_same_url_referer
P0_HOSTED_INPUT_URL=https://static.tibia.com/download/tibia.x64.tar.gz
```

This corroborates the hosted input blocker without creating another request from this task.

### Public GitHub source inspection

The GitHub-release source already used by PR `#97` (`dudantas/tibia-client`) was inspected as an alternative staging source. Its published original-Linux release inventory inspected during this task did not expose the exact `15.32.df7b29` build. Repository/global GitHub search for the exact version/SHA did not yield an acceptable `blakinio/otclient`-policy-compliant exact binary source.

UNKNOWN: whether a compliant exact archive exists elsewhere but is not indexed/accessible by the available repository tooling.

## Required patch/dependency graph — current evidence matrix

| Graph element | Current status | Evidence / missing proof |
|---|---|---|
| extent/subfield/viewport semantic ownership | PROVEN_PARTIAL | exact names above |
| typeinfo/vtables | UNKNOWN / candidates only | two RTTI-name relocation leads; no complete ABI structure/vtable slots preserved |
| dimension/edge fields | UNKNOWN | exact disassembly/xrefs unavailable on permitted hosted surface |
| constructor/default writers | UNKNOWN | same blocker |
| all material writers/readers | UNKNOWN | same blocker |
| fixed arrays / capacities / allocation formulas | UNKNOWN | same blocker |
| loop bounds / masks / bit widths | UNKNOWN | same blocker |
| protocol row/column/floor parser assumptions | UNKNOWN | same blocker |
| storage indexing/eviction/cache limits | UNKNOWN | same blocker |
| render iteration / clipping / culling | UNKNOWN | same blocker |
| camera projection / scale coupling | UNKNOWN | same blocker |
| picker bounds / coordinate transforms | UNKNOWN | same blocker |
| movement/floor-change strip dependency | UNKNOWN | semantic/historical leads exist; no material static call/data graph |
| isolated-change consequence | UNKNOWN | cannot be reasoned safely before writers/readers/allocation dependencies are recovered |
| concrete patch sites | UNKNOWN | no mutation design is authorized or evidence-backed yet |

## Static classification

```yaml
STATIC_PATCH_GRAPH_READY: false
MORE_STATIC_RE_NEEDED: true_in_principle_but_not_currently_executable_on_allowed_input_surface
RUNTIME_DISCRIMINATOR_REQUIRED: false
BLOCKED: true
blocker_class: INPUT_BLOCKED
```

Why `BLOCKED`, not `RUNTIME_DISCRIMINATOR_REQUIRED`:

- the missing evidence is still fundamentally static (object layouts, xrefs, disassembly, fields, allocations, loops and parser/render consumers);
- no result currently requires live behavior to distinguish two static hypotheses;
- escalating to GUI/runtime would not solve the missing hosted exact-binary input and would violate the user's requested static-first phase.

## Required unblocker / next action

Provide a legally and technically compliant **GitHub-hosted-readable** staging source for the exact fenced official native-Linux `15.32.df7b29` client, without committing the executable to the repository and without using Synology as a static-analysis fallback. Then:

1. verify size and SHA before any claim;
2. run the retained analyzer/hardened successor on GitHub-hosted only;
3. recover full typeinfo/vtable/constructor/destructor/xref evidence;
4. trace candidate dimension fields through protocol/storage/render/camera/picker;
5. audit fixed allocations, loop bounds, parser assumptions and clipping/culling;
6. publish the complete patch/dependency graph;
7. only after that graph is coherent consider a separate mutation task under then-current runtime governance.

Until that unblocker exists, no new X11/VNC/login/session, no Synology static fallback and no client-byte mutation are justified.
