# OTC-20260812 — worldmap reconstruction evidence pipeline

## Status

`IMPLEMENTED_TOOLING / REAL_CAPTURE_PENDING`

Repository: `blakinio/otclient`

Archived task: `docs/agents/tasks/archive/OTC-20260812-worldmap-reconstruction.md`

Tool: `tools/tibia_worldmap_reconstruction/`

Source research PR: `#279`, exact source head `04356aa9c042ce19d9d8431b91f18567e410a5e5`, closed unmerged after coordinator disposition `ACCEPT_WITH_EDITS`.

Current-main integration authority: `OTC-20260815-track-a-promotion-coordination` / PR `#300`.

## Goal

Provide a durable neutral pipeline that converts separately authorized decoded official-client tile observations into normalized reconstruction state, compares that state with normalized references and emits an OTBM-ready static-tile plan without guessing missing semantics.

## Accepted implementation boundary

The accepted implementation provides:

- exact client-version and target OTB-version fencing;
- mandatory observation provenance (`source`, `capture_id`);
- deterministic repeated-observation merge;
- explicit `CONFLICT` instead of silently picking one tile variant;
- evidence-backed appearance-role classification;
- explicit client appearance ID -> OTB/server ID mapping;
- no assumed identity mapping;
- structural snapshot validation before compare/plan operations;
- fail-closed ground, unknown-role and unmapped-ID handling;
- separation of dynamic entities from static OTBM output;
- source-specific reference comparison;
- neutral OTBM-ready static plan rather than guessed binary OTBM generation;
- relative-path/containment validation for file inputs and atomic output replacement where applicable.

Implemented files:

```text
tools/tibia_worldmap_reconstruction/__init__.py
tools/tibia_worldmap_reconstruction/README.md
tools/tibia_worldmap_reconstruction/cli.py
tools/tibia_worldmap_reconstruction/pipeline.py
tests/tools/tibia_worldmap_reconstruction/test_pipeline.py
```

## Evidence-authoritative path

```text
trusted observations
+ verified appearance catalog
+ verified client->OTB mapping
-> reconstruct()
-> structurally validated snapshot
-> compare() / plan-otbm
```

`validate_snapshot()` proves schema/internal consistency. It does **not** cryptographically authenticate an arbitrary self-consistent supplied snapshot and does not independently prove that OTB IDs came from an authoritative mapping. If snapshots cross an untrusted handoff, authentication or revalidation against original catalog/mapping inputs is still required.

## Static versus dynamic policy

A proven tile role may be classified as:

```text
ground
border
static
dynamic
creature
npc
unknown
```

Dynamic/creature/NPC presence is not converted into a static OTBM object by default. Observed presence or movement also does not prove a spawn definition. Spawn origin/radius/count/respawn timing require separate repeated evidence.

## Reference comparison policy

References are normalized independently and retain source identity. No reference wins by default. Expected comparison states include:

```text
MATCH
NOT_OBSERVED
REFERENCE_MISSING
GROUND_MISMATCH
CONTENT_MISMATCH
STACK_ORDER_MISMATCH
UNMAPPED_ID
UNKNOWN_ROLE
GROUND_UNRESOLVED
CONFLICT
```

Unresolved structural state propagates before equality comparisons.

## OTBM plan boundary

The accepted tool emits a neutral static plan containing only validated information such as:

```text
client_version
otb_version
position
ground_otb_id
ordered static_otb_ids
```

A later binary OTBM writer is a mechanical consumer of that validated plan. It must not become the place where missing ground, appearance-role or mapping semantics are guessed.

## Source validation and audit

### OTC279-AUD-001

The first fresh audit found that caller-supplied snapshots were insufficiently validated before compare/plan operations. The source task added strict type/range/status and internal-consistency validation plus regression coverage.

Recorded source validation:

```yaml
run: 31653654639
job: 94303192632
focused_tests: 19/19 PASS
python_syntax: PASS
synthetic_e2e: PASS
```

### OTC279-AUD-002

A later closeout audit found that an `OK` snapshot could still contradict its own `observed_variants` through independently changed ground/static/dynamic projections. Source repairs bound an `OK` projection back to the recorded observed variant and added regression coverage.

Recorded repaired validation:

```yaml
run: 31681045961
job: 94386320196
focused_tests: 23/23 PASS
python_syntax: PASS
synthetic_reconstruct_compare_plan: PASS
```

The temporary source validation workflow was removed before the final source head.

Final source repository CI on exact head `04356aa9c042ce19d9d8431b91f18567e410a5e5` was independently verified by the coordinator as run `31681889560`, conclusion `success`, with no unresolved PR review threads.

## Current-main integration

The coordinator did not merge the stale 27-commit source branch wholesale. After closing #279 and releasing its ownership, PR #300 rebuilt the accepted immutable source blobs on `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`, then reconciled shared catalogue/changelog/lifecycle state separately.

This preserves a bounded auditable integration and avoids reviving stale branch history.

## Security/licensing boundary

Do not commit through this pipeline:

- official client binaries;
- proprietary appearance/sprite/sound/map asset bytes without confirmed rights;
- credentials/session material;
- account/character identity;
- authenticated screenshots;
- raw private captures containing protected data.

Neutralized IDs/coordinates and original/synthetic fixtures are acceptable only within the governing evidence/privacy rules.

## UNKNOWN / not delivered by this tooling

- semantic classification of arbitrary live appearance IDs unless separately proven;
- exact current appearance flags/roles for all objects;
- complete current client appearance ID -> OTB/server ID mapping;
- complete real official-client world capture;
- authoritative monster/NPC spawn definitions;
- complete binary OTBM output;
- proof that any particular external reference is globally complete/correct.

Those remain separate Track A evidence tasks and are not upgraded by the existence of this pipeline.
