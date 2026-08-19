---
task_id: OTC-20260818-track-a-monster-spawn-mechanics-design
status: completed
session_role: released
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation
phase: closed
source_pr: 540
source_branch: docs/OTC-20260818-track-a-monster-spawn-mechanics-design
source_head: 3fea6bb6c674b36fb66e3b07de9f85f50b3fa562
source_disposition: closed_unmerged_superseded
coordinator_review: 4971768519
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
source_governance_run: 32151427300
source_governance_result: SUCCESS
source_ci_run: 32151427685
source_ci_result: SUCCESS
promoted_schema_blob: ac7df1cef80c417af6b74d79102c8da074032bed
source_earlier_validated_schema_blob: 2b54cebfb61c6a727f95ce54276418ad4f0fe189
source_earlier_schema_validation_is_final_blob_validation: false
promotion_base: 238b3698447db3a208b7f2b21feffb3d0ec77401
promotion_pr: 594
promotion_head: d4460801692c32f8370f4fda45d3cf37bb0957d6
promotion_merge: f48c58ad1c06de1c95b630acabd8d0dd6939d0bd
promotion_merge_method: squash
promotion_changed_paths: 11
promotion_ahead_by: 3
promotion_behind_by: 0
promotion_ci_run: 32249997448
promotion_ci_result: SUCCESS
promotion_review: 4971797253
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gui_input_authorized: false
gameplay_allowed: false
transaction_authorized: false
physical_e2e_required: false
runtime_recorder_implemented: false
physical_spawn_sampling_completed: false
server_spawn_table_proven: false
server_ai_algorithm_proven: false
ownership_released: true
---

# Monster spawn/mechanics research design — terminal archive

## Terminal disposition

The bounded monster spawn/respawn/observable-mechanics **research design** task is complete and ownership is released. Source PR #540 was closed unmerged as superseded after clean coordinator promotion #594 squash-merged as:

```text
f48c58ad1c06de1c95b630acabd8d0dd6939d0bd
```

## Canonical delivered design

The promoted package defines:

- `MONSTER_OBSERVATION_V1` semantic evidence contract;
- machine-readable JSON Schema;
- deterministic spawn/respawn inference with coverage, epoch and censoring controls;
- empirical mechanics inference with repetitions, negative controls, counterexamples and holdout validation;
- coordinator, observer, spawn-inference and mechanics-inference prompts plus alias;
- an additive child-programme link in the parent experiment sweep;
- a coordinator current-state/provenance overlay.

## Final schema identity and boundary

The promoted exact schema blob is:

```text
ac7df1cef80c417af6b74d79102c8da074032bed
```

The source task also records focused automated validation for earlier blob `2b54ceb...`. That earlier blob is preserved as historical validation provenance only; it is not mislabeled as an automated validation run of final `ac7df1ce...`.

Coordinator re-read of final `ac7df1ce...` confirmed the core fail-closed invariants for continuous coverage, continuous-create classification, creature create/delete requirements, derived/inference provenance and monster semantic-name constraints.

## Current-state correction

Source `current` dependency prose is historical to the 2026-08-18 design checkpoint. The promoted coordinator overlay records the later state at promotion:

- current exact official Linux client fence `15.32 / 52109920 / ed5469...`;
- #528 native-login task terminal/released with causal login-to-world proof and a separate post-handoff session-retention failure;
- #539 S10 terminal with the missing retained action-specific connect window still unproven;
- #536 coverage registry terminal;
- current-build creature/combat static G0 promoted through #558;
- #302 authoritative player XYZ still non-promotion-ready and causally unproven.

Future workers must refresh these facts again from then-current trusted main. This archive is not runtime authority.

## Completion boundary

This design task intentionally does **not** complete the physical research programme:

```text
live native-client recorder/resolver implementation  NOT IMPLEMENTED
physical spawn sampling                              NOT IMPLEMENTED
authoritative current player XYZ                     NOT PROVEN
server-owned spawn table/home/radius                 UNKNOWN
server AI source/algorithm                           UNKNOWN
Oteryn behavior implementation                       OUT OF SCOPE
```

Future physical work requires a new separately admitted Track A task satisfying then-current ownership/lease/registration/admission and exact-client/structural-IN_GAME gates. This design never authorizes a second logged-in Global session merely for sampling throughput.

## Promotion validation

```text
head                     d4460801692c32f8370f4fda45d3cf37bb0957d6
ahead_by                 3
behind_by                0
changed paths            11
CI                        32249997448 = SUCCESS
promotion review          4971797253
review threads            0
merge                     f48c58ad1c06de1c95b630acabd8d0dd6939d0bd
```

## Safety

The source task, coordinator audit, promotion and lifecycle closeout are repository/documentation work only with `runtime_access:none`. No official-client execution, credential use, login, GUI input, gameplay, economy/account transaction, process-memory access or runtime mutation occurred during coordinator work.
