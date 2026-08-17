# Coordinator producer acceptance closeout — PR #367

Date: 2026-08-17

## Decision

```yaml
consumer_task: OTC-20260816-track-a-worldmap-extent-static-re
consumer_pr: 367
coordinator_decision: ACCEPT_WITH_EDITS_COMPLETED
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: false
client_byte_mutation_authorized: false
runtime_access: none
```

The bounded STATIC-RE result is accepted. No additional static producer is required for the questions closed by this task. This closeout consumes the final producer evidence after both producer PRs were terminalized, validated on current-main heads, and merged canonically.

## Exact client fence

```text
version   15.32.df7b29
size      51965216
sha256    e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform  official native Linux only
```

No raw exact game-client executable was committed or uploaded by this coordinator closeout, the exact game client was not executed by this consumer, process memory/canonical runtime state were not accessed, and no client bytes were changed. The separately documented historical owner-supplied launcher/bootstrap archive is not the fenced exact game-client executable and remains historical provenance only.

## Canonical producer #437

Task: `OTC-20260816-track-a-worldmap-exact-static-evidence`

```text
accepted evidence source head  3e14d079a1e6d09a21c838a4a82c4fc51b7b7e74
pre-cleanup governance         32005392491 SUCCESS
pre-cleanup repository CI      32005392636 SUCCESS
final cross-check run          32004839610
source job/artifact            95312106162 / 9279649834 SUCCESS
hosted job/artifact            95312291576 / 9279654629 SUCCESS
final artifact sha256          f4605cc42e032d7ce3ca91bda17aa54dfdb2b8b427d8758fadc30d10748c30b7
terminal cleanup head          3b6942ba543fec499d43c0697debfe80eb19471a
strict-main terminal head      8b34175e873ee1a950c3fe21b07f1292696cf309
strict-main terminal CI        32007165687 SUCCESS
canonical squash merge         f753b5aa94e9aeb6b5554fd5bb827823bda80256
```

Durable canonical evidence is under:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/`

Accepted load-bearing result: hardcoded packed `18/14 @ 0x01cdd958` initializes the exact `TWorldmapProtocolMessageHandler` master pair, which flows through the exact snapshot builder and exact `TWorldMapStorage` slot 12 to `Storage+0x48/+0x4c`. Viewport dynamic geometry, RenderProvider fixed-32 dependencies and Picker fixed-32 dependencies are independently recovered. Producer #437 does not prove a complete later-writer census, a fixed Storage/cache ceiling, a named Camera projection formula, or a safe client mutation.

## Canonical producer #446

Task: `OTC-20260817-track-a-worldmap-downstream-exact-static-evidence`

```text
accepted evidence source head  f7f16af614a88100cc82ff7ecf0b112cb2e0605c
pre-cleanup governance         32003664983 SUCCESS
pre-cleanup repository CI      32003665239 SUCCESS
broad run                      32001356705
broad source/final artifacts   9278519216 / 9278527206
targeted run                   32002326947
targeted source/final artifacts 9278827774 / 9278833445
camera run                     32003150333
camera source/final artifacts  9279105537 / 9279111731
terminal cleanup head          be0149bf59226194001ce24cda2743dbb6492bca
strict-main terminal head      034d2bf5c2c0f3bf40f64889b9e342b61ef61622
strict-main terminal CI        32007282137 SUCCESS
canonical squash merge         8212765956a9bfafd2d8a7687440c02716c87170
```

Durable canonical evidence is under:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/`

Accepted load-bearing result: producer #446 independently corroborates the `18/14 -> Handler -> snapshot -> Storage slot12` chain, proves RenderProvider clipping/indexing and Picker fixed-32 transform dependencies, and proves exact Camera layout plus higher-level Viewport/Camera co-ownership. Its 11 exact Camera-vptr neighborhoods produce a bounded negative result for a direct Camera-field-to-extent mutation edge; this is not a global absence proof and does not identify a Camera patch site.

## Frozen consumer graph

```text
hardcoded packed 18/14 @ 0x01cdd958
  -> Handler+0xb0/+0xb4 constructor default
  -> 0x00bc6350 snapshot+0x38
  -> Handler+0x10 exact TWorldMapStorage vslot12
  -> 0x00cc6cd0
  -> Storage+0x48/+0x4c

Viewport: constructor default 18/14 + later recomputation at 0x00cbf700
RenderProvider: direct fixed-32 clipping/culling/indexing/iteration dependency
Picker: direct fixed-32 screen/world transform and bounds dependency
Camera: exact layout/co-ownership; no direct extent mutation edge recovered in bounded exact-vptr neighborhoods
```

## Carried unknowns

These remain constraints, not reasons to repeat the completed static discovery:

- complete post-construction writer census for Handler `+0xb0/+0xb4`;
- exact source-level member names/units for geometry fields;
- named Camera projection formula or indirect coupling outside the bounded exact-vptr neighborhoods;
- any network/parser extent ceiling not proven by these static packages;
- semantic interpretation of the RenderProvider `65535 x 10-byte` allocation as a world-map ceiling;
- any safe client-byte mutation design.

## Terminal boundary

`STATIC_PATCH_GRAPH_READY=true` means the dependency graph is sufficiently recovered to close this STATIC-RE task. It does not authorize a patch. `MUTATION_DESIGN_READY=false`; any mutation-design and physical validation require a separately authorized task. E2E for this static-evidence closeout is `NOT_APPLICABLE` because no user-facing/live-runtime behavior is changed.
