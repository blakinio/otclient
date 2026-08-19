---
task_id: OTC-20260818-track-a-monster-spawn-mechanics-design
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation
phase: coordinator-promotion
source_pr: 540
source_branch: docs/OTC-20260818-track-a-monster-spawn-mechanics-design
source_head: 3fea6bb6c674b36fb66e3b07de9f85f50b3fa562
source_disposition: close_unmerged_after_promotion
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
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
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
ownership_released: false
---

# Monster spawn/mechanics research design — coordinator archive checkpoint

## Disposition

Source #540 is accepted with edits as a documentation/contracts/prompts package. Its observation contract, schema, inference rules and worker prompts are suitable for canonical promotion, but source `current` dependency statements are frozen to the 2026-08-18 design checkpoint and must not be treated as present runtime authority.

Clean promotion adds a coordinator current-state overlay that supersedes those historical `current` statements without rewriting the accepted design semantics.

## What this task completes

This task completes only the **research design layer**:

- `MONSTER_OBSERVATION_V1` semantic evidence contract;
- machine-readable JSON Schema;
- deterministic spawn/respawn inference rules with coverage/censoring controls;
- empirical mechanics inference rules that keep server algorithms UNKNOWN unless directly proven;
- coordinator + observer + spawn-inference + mechanics-inference prompts and alias;
- additive integration into the parent experiment sweep.

## What remains future work

```text
live native-client observer/resolver implementation  NOT IMPLEMENTED
physical spawn sampling                              NOT IMPLEMENTED
authoritative current player XYZ                     NOT PROVEN
server-owned spawn table/home/radius                 UNKNOWN
server AI source/algorithm                           UNKNOWN
Oteryn behavior implementation                       OUT OF SCOPE
```

Future physical work requires a new separately admitted Track A runtime task from then-current trusted `main`. This design does not authorize login, credentials, GUI input, gameplay stimuli or a second logged-in Global session.

## Final schema provenance

The exact source-head schema promoted by the package is blob:

```text
ac7df1cef80c417af6b74d79102c8da074032bed
```

The source task text also records focused validation of earlier blob `2b54ceb...`; that earlier run is preserved as historical validation evidence only and is not mislabeled as validation of final `ac7df1ce...`.

Coordinator re-read of the exact final schema confirmed the fail-closed continuity/create/delete/derived-inference invariants documented in the coordinator audit.

## Current-state correction

At promotion time, unlike the source design checkpoint:

- the exact current official client fence is canonical (`15.32 / 52109920 / ed5469...`);
- #528 native login is terminal/released with causal current-build login-to-world proof and separate later session-retention failure;
- #539 S10 and #536 coverage are terminal;
- current-build creature/combat static evidence exists through #558;
- #302 direct player XYZ remains blocked/non-promotion-ready.

Every future worker must refresh those facts again from live `main`; none is permanent runtime authority.

## Safety

Repository/documentation only, `runtime_access:none`; no official-client execution, credentials, login, GUI input, gameplay, transaction, process-memory access or runtime mutation occurs in this task or closeout.

After clean promotion merge, close source #540 unmerged as superseded and lifecycle-update this archive to `status:completed`, `session_role:released`, final promotion facts and `ownership_released:true`.
