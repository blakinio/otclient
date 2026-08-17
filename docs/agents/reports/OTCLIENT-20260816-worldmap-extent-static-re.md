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

## Coordinator disposition

The static dependency result is accepted after canonical promotion of both exact-client producers.

Producer #437 (`OTC-20260816-track-a-worldmap-exact-static-evidence`):

```text
accepted evidence source head  3e14d079a1e6d09a21c838a4a82c4fc51b7b7e74
final cross-check run          32004839610
strict-main terminal head      8b34175e873ee1a950c3fe21b07f1292696cf309
strict-main CI                 32007165687 SUCCESS
canonical squash merge         f753b5aa94e9aeb6b5554fd5bb827823bda80256
```

Producer #446 (`OTC-20260817-track-a-worldmap-downstream-exact-static-evidence`):

```text
accepted evidence source head  f7f16af614a88100cc82ff7ecf0b112cb2e0605c
broad / targeted / Camera runs 32001356705 / 32002326947 / 32003150333
strict-main terminal head      034d2bf5c2c0f3bf40f64889b9e342b61ef61622
strict-main CI                 32007282137 SUCCESS
canonical squash merge         8212765956a9bfafd2d8a7687440c02716c87170
```

Canonical evidence lives under:

- `docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/`
- `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-coordinator-producer-acceptance-closeout.md`

No raw client was promoted, no live client process/runtime state was used by this consumer, and no client bytes were modified.

## Exact geometry source chain

The upstream source of the retained Storage pair is proven:

```text
hardcoded packed 18/14 @ 0x01cdd958
 -> exact TWorldmapProtocolMessageHandler constructor
 -> Handler+0xb0/+0xb4 constructor default
 -> 0x00bc6350 geometry snapshot +0x38
 -> Handler+0x10 exact TWorldMapStorage virtual dispatch
 -> exact TWorldMapStorage slot 12 0x00cc6cd0
 -> Storage+0x48/+0x4c
```

Exact identities include Handler vptr `0x030871d8`, Storage vptr `0x0308ce70` and Viewport vptr `0x0308c9a8`.

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

Accepted exact evidence proves:

- lower XYZ `+0x18/+0x1c/+0x20` and upper XYZ `+0x30/+0x34/+0x38` participate in half-open bounds;
- `+0x48/+0x4c` are payload DWORDs of embedded exact `TWorldMapExtent` at `Storage+0x40`;
- slot 12 replaces geometry and drives out-of-bounds removal;
- `Storage+0x88` participates in live collection-count state;
- no fixed maximum Storage/cache capacity is proven;
- Storage traversal is extent/coordinate driven rather than a literal fixed 18×14 allocation.

## Viewport dependency

Viewport constructor `0x00cbf680` consumes the same packed `18/14` default. Exact recompute `0x00cbf700` later derives geometry from Viewport state, consumes packed `15/11` delta state, and uses signed shift-by-5 / divide-by-32-family arithmetic. Viewport is therefore a computed geometry dependency, not an immutable literal-only surface.

## RenderProvider dependency

Exact `TWorldMapRenderProvider` vptr `0x02f6c258` / typeinfo `0x03089b70` is proven. Its accepted primary paths establish fixed-32 clipping/culling/indexing/iteration dependencies including `&0x1f`, shift-by-5, explicit coordinate bounds checks, linearized indexing and extent/subfield-extent state.

## Picker dependency

Exact `TWorldMapPicker` vptr `0x02f6b7c8` / typeinfo `0x03086888` is proven. Accepted primary paths establish fixed-32 screen/world conversion and bounds traversal using shift-by-5, `0x1f` correction and `0x20` stepping.

## Camera dependency

Exact `TWorldMapCamera` vptr `0x03083968` / typeinfo `0x03080500` is proven. A higher-level world-map owner co-owns/coordinates a Viewport-compatible object at owner `+0xa8` and counted Camera at owner `+0xc8/+0xd0`, then invokes exact Viewport recompute `0x00cbf700`.

All 11 exact Camera-vptr neighborhoods were staged and hosted-disassembled. No type-anchored Camera-field chain to Storage slot 12, Handler master `18/14`, or Storage `+0x48/+0x4c` was recovered in those bounded neighborhoods. This is a bounded negative result, not a global absence proof. No Camera mutation site or named projection formula is invented.

## Fixed representation dependencies

Recovered representation constraints include:

```text
18/14 packed default  0x01cdd958
Viewport delta         15/11 @ 0x01d63cd0
32-cell scale          shift 5
floor/chunk mask       0x1f
record/allocation      0x18, 0x20, 0x28, 0x30 on different consumers
```

They are dependencies to preserve/revalidate, not a proposed patch list.

## Final disposition

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
network_or_parser_extent_ceiling: UNKNOWN
safe_client_byte_mutation_design: UNKNOWN
static_patch_graph_ready: true
mutation_design_ready: false
client_byte_mutation_authorized: false
```

The static graph is sufficiently recovered to close discovery. A separately authorized mutation-design/physical-validation task may consume this graph, but must carry every explicit unknown above and must not infer additional patch sites from them.
