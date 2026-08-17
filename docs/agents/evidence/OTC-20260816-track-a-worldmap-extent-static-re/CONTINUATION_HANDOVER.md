# Continuation handover — worldmap extent static RE

The STATIC-RE discovery task is complete and coordinator-accepted. Do not reopen the closed exact-static/downstream questions or create another static producer for the same questions without a new discriminator.

```yaml
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
execution_class: github_hosted
runtime_access: none
mutation_authorized: false
owner_funded_ai_api_authorized: false
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
static_patch_graph_ready: true
mutation_design_ready: false
remaining_static_blocker: NONE_FOR_STATIC_DEPENDENCY_DISCOVERY
```

## Canonical producer provenance

Producer #437 is merged canonically:

```text
accepted evidence source head  3e14d079a1e6d09a21c838a4a82c4fc51b7b7e74
strict-main terminal head      8b34175e873ee1a950c3fe21b07f1292696cf309
strict-main terminal CI        32007165687 SUCCESS
canonical merge                f753b5aa94e9aeb6b5554fd5bb827823bda80256
```

Producer #446 is merged canonically:

```text
accepted evidence source head  f7f16af614a88100cc82ff7ecf0b112cb2e0605c
strict-main terminal head      034d2bf5c2c0f3bf40f64889b9e342b61ef61622
strict-main terminal CI        32007282137 SUCCESS
canonical merge                8212765956a9bfafd2d8a7687440c02716c87170
```

## Authoritative final evidence

Read the coordinator closeout first:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-coordinator-producer-acceptance-closeout.md`

Then the final consumer graph checkpoint and report:

- `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-downstream-exact-static-consumption.md`
- `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`

Canonical producer evidence is retained under:

- `docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/`

## Frozen exact graph facts

- exact Handler vptr `0x030871d8`, Storage vptr `0x0308ce70` and Viewport vptr `0x0308c9a8` are proven;
- static packed literal `18/14` at `0x01cdd958` initializes Handler master pair `+0xb0/+0xb4` and the independent Viewport constructor default;
- `0x00bc6350` copies the Handler master pair into snapshot `+0x38`;
- Handler `+0x10` dispatches that snapshot to exact `TWorldMapStorage` slot 12 `0x00cc6cd0`;
- Storage slot 12 copies snapshot `+0x38` to Storage `+0x48/+0x4c` and participates in geometry replacement/out-of-bounds removal;
- Viewport geometry is later recomputed by `0x00cbf700` using fixed-32 arithmetic;
- RenderProvider proves fixed-32 clipping/culling/indexing/iteration dependencies;
- Picker proves fixed-32 screen/world transform and bounds dependencies;
- Camera exact layout and higher-level Viewport/Camera co-ownership are proven;
- all 11 exact Camera-vptr neighborhoods were staged, but no direct Camera-field → Storage/master-extent mutation edge was recovered in those bounded neighborhoods.

## Carried unknowns

These remain explicit constraints and do not reopen completed STATIC-RE discovery by themselves:

- complete post-construction writer census for Handler `+0xb0/+0xb4`;
- exact source member names/units for geometry fields;
- named Camera projection formula or indirect Camera coupling outside the bounded exact-vptr neighborhoods;
- any network/parser extent ceiling not proven by the accepted packages;
- whether the RenderProvider `65535 x 10-byte` allocation represents a semantic world-map ceiling;
- any safe client-byte mutation design.

## Next authorized boundary

No client bytes may be modified under this task. A future mutation-design or physical-validation task requires separate explicit authorization and must consume `STATIC_PATCH_GRAPH_READY=true` plus the carried unknowns above rather than repeating this research.
