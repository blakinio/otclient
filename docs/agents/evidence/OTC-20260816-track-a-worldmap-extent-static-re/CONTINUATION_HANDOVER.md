# Continuation handover — worldmap extent static RE

The STATIC-RE discovery task is complete on this branch. Do not reopen the old exact-static/downstream blockers or create another static producer for the same questions without a new discriminator.

```yaml
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
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

## Authoritative final evidence

Read first:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260817-downstream-exact-static-consumption.md`

Then the final report:

`docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`

Producer #446 durable evidence is also retained under:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/`

## Frozen exact graph facts

- exact Handler vptr `0x030871d8` / Storage vptr `0x0308ce70` / Viewport vptr `0x0308c9a8` are proven;
- static packed literal `18/14` at `0x01cdd958` initializes Handler master pair `+0xb0/+0xb4` and Viewport constructor default;
- `0x00bc6350` copies Handler master pair into snapshot `+0x38`;
- `0x00cdb770` dispatches that snapshot through exact Handler `+0x10` Storage slot 12 `0x00cc6cd0`;
- Storage slot 12 copies snapshot `+0x38` to Storage `+0x48/+0x4c`;
- Storage lower/upper XYZ bounds, extent-driven out-of-bounds removal and live collection count relation are proven;
- Viewport geometry is later recomputed by `0x00cbf700` and uses fixed-32 arithmetic;
- RenderProvider primary slots `0..21` prove clipping/culling/indexing/iteration dependencies and 32-cell/chunk representation;
- Picker primary slots `0..7` prove fixed-32 screen/world transform and bounds dependencies;
- Camera exact layout and higher-level Viewport/Camera coownership are proven; all 11 exact Camera-vptr neighborhoods were staged, but no direct Camera-field → Storage/master extent mutation edge was recovered in those bounded neighborhoods.

## Carried unknowns

These do not reopen STATIC-RE discovery by themselves:

- complete post-construction writer census for Handler `+0xb0/+0xb4`;
- exact source member names/units;
- named Camera projection formula or indirect Camera coupling outside the bounded exact-vptr neighborhoods.

They must be explicit constraints in any later mutation-design or physical-validation task.

## Next authorized boundary

No client bytes may be modified under this task. A future mutation-design task requires separate explicit authorization and should consume `STATIC_PATCH_GRAPH_READY=true` rather than repeating this research.
