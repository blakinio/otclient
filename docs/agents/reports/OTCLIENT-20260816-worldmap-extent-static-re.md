# OTCLIENT-TIBIA-RE — worldmap extent static dependency recovery

```yaml
report_date: 2026-08-17
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
subject: official native Linux Tibia client only
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
implementation_status: NOT_IMPLEMENTED
client_byte_mutation: NOT_PERFORMED
runtime_used_by_this_task: false
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
static_patch_graph_ready: true
mutation_design_ready: false
remaining_blocker: NONE_FOR_STATIC_DEPENDENCY_DISCOVERY
```

## Result

The original exact-static input blocker was resolved by producer PR #437. The remaining upstream/downstream blocker is now resolved by new producer Draft PR #446 (`OTC-20260817-track-a-worldmap-downstream-exact-static-evidence`) at exact evidence head `f7f16af614a88100cc82ff7ecf0b112cb2e0605c`.

Producer #446 exact-head validation passed:

```text
Track A governance run  32003664983  SUCCESS
repository CI run        32003665239  SUCCESS
CI / Required job        95309109578  SUCCESS
```

No raw client was uploaded, no live client process/runtime state was used, and no client bytes were modified.

Final durable consumer evidence:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-downstream-exact-static-consumption.md`

## Exact geometry source chain

The `18/14` pair is no longer an unexplained Storage runtime value.

```text
static packed 18/14 @ 0x01cdd958
 -> Handler constructor default at Handler+0xb0/+0xb4
 -> 0x00bc6350 geometry snapshot +0x38
 -> 0x00cdb770 Handler+0x10 virtual slot +0x60
 -> exact TWorldMapStorage slot 12 0x00cc6cd0
 -> Storage+0x48/+0x4c
```

The exact Handler constructor is anchored by vptr `0x030871d8`; the exact Storage object is vptr `0x0308ce70`. Storage slot 12 reads snapshot QWORD `+0x38` and writes it to Storage `+0x48`, covering both DWORDs `+0x48/+0x4c`.

Classification:

```yaml
Handler master pair:
  constructor_default: hardcoded 18/14
  complete_later_writer_census: UNKNOWN
TWorldMapViewport:
  constructor_default: hardcoded 18/14
  later_recomputation: PROVEN
TWorldMapStorage:
  constructor_default: zero
  runtime_update: mutable/copy-driven via slot 12
```

## Storage dependency

Exact Storage evidence remains authoritative:

- lower XYZ `+0x18/+0x1c/+0x20` and upper XYZ `+0x30/+0x34/+0x38` are half-open bounds;
- `+0x48/+0x4c` are payload DWORDs of embedded exact `TWorldMapExtent` at Storage `+0x40`;
- slot 12 replaces geometry and removes nodes outside the resulting bounds;
- `Storage+0x88` is live collection-count/size state;
- no fixed maximum cache capacity is proven;
- Storage traversal is extent/coordinate driven rather than a literal fixed 18×14 allocation.

## Viewport dependency

Exact Viewport vptr `0x0308c9a8`, constructor `0x00cbf680`, and geometry recompute `0x00cbf700` are proven.

The constructor consumes the same packed `18/14` default at `0x01cdd958`, but `0x00cbf700` later recomputes the extent from Viewport state, consumes packed `15/11` delta state and applies signed shift-by-5 / divide-by-32-family arithmetic.

Viewport is therefore a computed geometry dependency, not a second immutable literal-only surface.

## RenderProvider dependency

Exact `TWorldMapRenderProvider` vptr `0x02f6c258` / typeinfo `0x03089b70` has curated primary slots `0..21`.

Load-bearing exact paths prove:

- fixed-size record iteration (`0x20` and `0x30` surfaces depending on path);
- `&0x1f`, shift-by-5 and 32-cell/chunk arithmetic;
- explicit negative/out-of-range coordinate rejection;
- linearized `y*width+x`-style indexing with indexed/vector bounds checks;
- exact `TWorldMapExtent` / `TWorldMapSubfieldExtent`-related construction.

RenderProvider is a direct clipping/culling/indexing/iteration dependency for any future extent change.

## Picker dependency

Exact `TWorldMapPicker` vptr `0x02f6b7c8` / typeinfo `0x03086888` has curated primary slots `0..7`.

Primary paths prove packed coordinate conversions and range traversal using shift-by-5, `0x1f` floor/sign correction and `0x20` stepping. Picker is therefore a direct fixed-32 screen/world transform and bounds dependency.

## Camera dependency

Exact `TWorldMapCamera` vptr `0x03083968` / typeinfo `0x03080500` is proven. Camera constructors initialize vector-state blocks, embedded address points and scalar `1.0` transform-like state.

A dedicated producer pass enumerated all 11 exact Camera-vptr xrefs, staged 11 bounded neighborhoods (225,280 source bytes) and hosted-disassembled 37,325 unique instructions. One exact higher-level construction path co-owns/coordinates a Viewport-compatible object at owner `+0xa8` and counted Camera at owner `+0xc8/+0xd0`, then calls exact Viewport recompute `0x00cbf700`.

No type-anchored Camera-field chain to Storage slot 12, Handler master `18/14`, or Storage `+0x48/+0x4c` was recovered in those exact-vptr neighborhoods. This is a bounded negative result, not a global absence proof.

For the static graph, Camera is a co-owned transform/post-change validation dependency; no Camera mutation site or named projection formula is invented.

## Fixed representation dependencies

Recovered exact/static representation surfaces include:

```text
18/14 packed default  0x01cdd958
Viewport delta         15/11 @ 0x01d63cd0
32-cell scale          shift 5
floor/chunk mask       0x1f
record/allocation      0x18, 0x20, 0x28, 0x30 on different consumers
```

These are dependency constraints, not a proposed patch list.

## Final graph disposition

```yaml
protocol_handler_identity: PROVEN
storage_identity_and_bounds: PROVEN
upstream_storage_extent_source: PROVEN
viewport_default_and_recompute: PROVEN
storage_extent_driven_eviction: PROVEN
render_clipping_culling_iteration: PROVEN
picker_screen_world_transform: PROVEN
camera_layout_and_viewport_coownership: PROVEN
camera_direct_extent_mutation_edge_in_exact_vptr_neighborhoods: NOT_RECOVERED_BOUNDED
fixed_allocation_mask_packing_dependencies: PROVEN
complete_handler_master_later_writer_census: UNKNOWN
named_camera_projection_formula: UNKNOWN
static_patch_graph_ready: true
mutation_design_ready: false
client_byte_mutation_authorized: false
```

The discovery task has enough exact evidence to freeze the dependency graph. The explicit remaining unknowns must be carried into a separately authorized mutation-design and physical-validation phase; they are not grounds to invent additional static patch sites.
