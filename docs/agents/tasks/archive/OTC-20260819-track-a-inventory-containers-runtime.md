---
task_id: OTC-20260819-track-a-inventory-containers-runtime
status: completed
session_role: released
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: closed
source_pr: 559
source_branch: research/OTC-20260819-track-a-inventory-containers-runtime
source_head: e6bbe595e27f4b96386987f2a5610beaaeceed55
source_disposition: closed_unmerged_superseded
coordinator_review: 4970813830
coordinator_decision: ACCEPT_WITH_EDIT
material_finding: INV-AUD-001
material_finding_disposition: resolved_by_clean_current_main_promotion_without_merging_source_history
open_material_findings: 0
superseded_promotion_pr: 573
superseded_promotion_disposition: closed_unmerged_stale_base
promotion_base: 501d4493c15a59b841ac1811823845da8d88ddbc
promotion_pr: 574
promotion_head: 03defe56368d710a5492873809404cc0c33b06ad
promotion_merge: 11c01a8b7ff2179b264b04ce6f3401be532f4e9c
promotion_merge_method: squash
promotion_changed_paths: 11
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32241741642
promotion_ci_result: SUCCESS
promotion_review: 4971013704
promotion_review_result: PASS
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: bounded reverse-engineering documentation/evidence promotion; no product feature or authorized state-changing live journey is delivered by this task
current_client_version_token: '15.32'
current_client_size: 52109920
current_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_client_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
selected_rows: D09-D22
accepted_status: 14_PARTIAL_0_DONE
ownership_released: true
stale_branches_reconciled: true
---

# TIBIA-RE-INVENTORY-CONTAINERS — terminal bounded current-build evidence archive

## Terminal disposition

The bounded `TIBIA-RE-INVENTORY-CONTAINERS` D09-D22 research task is complete and ownership is released.

Source researcher PR #559 is preserved as provenance and was closed unmerged as superseded. The first promotion attempt #573 was also closed unmerged when `main` advanced during its creation. Clean promotion PR #574 was built one commit ahead / zero behind fresh trusted `main`, passed exact-head validation, and squash-merged as:

```text
11c01a8b7ff2179b264b04ce6f3401be532f4e9c
```

## Accepted bounded result

The promoted package proves current-build structural and causal routing for D09-D22 while preserving authenticated/live and stability gaps as unresolved. No row is promoted to `DONE`.

Accepted current-build facts include:

- 14/14 selected D09-D22 anchor sets revalidated;
- 21/21 selected current QMeta types recovered;
- direct protocol queue → container handler routing for the documented families;
- open/close/create/change/delete handler → `TContainerStorage` mutation and storage signal emission;
- direct `TContainerStorage` → `TContainerStorageController` connections for update/remove/manual-sort;
- Set/DeleteInventory → `TInventoryContainer::inventoryChanged`;
- direct `inventoryChanged` → `TPlayerInventoryAndStatusController::onInventoryChanged`.

The exact client fence is `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, ELF Build ID `d803d9695868713ef6ab0c3cf65f91212c9c6a62`.

## Independent audit and final promotion validation

Source review `4970813830` classified #559 `ACCEPT_WITH_EDIT`. The only material finding, `INV-AUD-001`, concerned stale/diverged source history rather than evidence semantics and was resolved by the clean promotion instead of merging that history.

Fresh exact-promotion-head validator `inventory-containers-promotion-validator-v2b` verified on `03defe56368d710a5492873809404cc0c33b06ad`:

```text
git diff --check = PASS
changed path ownership = PASS
JSON parse = PASS
source manifest hashes = 8/8 PASS
Track A agent runtime governance = PASS
text-only promotion = PASS
archive base fence = PASS
AUDIT_RESULT = PASS
```

GitHub CI run `32241741642` completed `SUCCESS`. Promotion review `4971013704` records exact-head PASS with zero open material findings. PR #574 then squash-merged to `main` as `11c01a8b7ff2179b264b04ce6f3401be532f4e9c`.

## Runtime / E2E / safety

A prior separately admitted read-only observation found the exact-current client at the login screen; inventory/container state was not visible. No credentials, login, GUI input, gameplay, process mutation, debugger/injection or item/container stimulus was performed by the promotion or closeout.

E2E is `NOT_APPLICABLE` for this bounded documentation/evidence task. Raw client bytes and passive captures are not retained or promoted.

## Remaining programme gaps

Authenticated live values, full `PlayerInventory` bulk normalization, exact subtype/charge/duration semantics, per-action serialization/server acknowledgements, and restart/relogin stability remain explicit `UNKNOWN` / `NOT_OBSERVED` programme gaps. The terminal task state does not reinterpret those rows as semantically complete.

## Lifecycle

```text
source #559:              CLOSED UNMERGED / SUPERSEDED
promotion attempt #573:   CLOSED UNMERGED / SUPERSEDED STALE BASE
promotion #574:           MERGED
promotion merge:          11c01a8b7ff2179b264b04ce6f3401be532f4e9c
open material findings:   0
accepted D09-D22 status:  14 PARTIAL / 0 DONE
runtime authority:        NONE
ownership:                RELEASED
```
