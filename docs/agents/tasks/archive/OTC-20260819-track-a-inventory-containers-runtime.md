---
task_id: OTC-20260819-track-a-inventory-containers-runtime
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
source_pr: 559
source_branch: research/OTC-20260819-track-a-inventory-containers-runtime
source_head: e6bbe595e27f4b96386987f2a5610beaaeceed55
source_disposition: close_unmerged_after_promotion
coordinator_review: 4970813830
coordinator_decision: ACCEPT_WITH_EDIT
material_finding: INV-AUD-001
material_finding_disposition: resolved_by_clean_current_main_promotion_without_merging_source_history
open_material_findings: 0
promotion_base: 5ce628b7e565eb17876b76305af6a6086ed7f258
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: bounded reverse-engineering evidence promotion; no product feature or authorized state-changing live journey is delivered by this task
current_client_version_token: '15.32'
current_client_size: 52109920
current_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_client_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
selected_rows: D09-D22
accepted_status: 14_PARTIAL_0_DONE
ownership_release_state: effective_on_promotion_merge_and_terminal_closeout
---

# TIBIA-RE-INVENTORY-CONTAINERS — bounded current-build evidence archive

## Accepted bounded result

The accepted source package proves current-build structural and causal routing for D09-D22 while preserving authenticated/live and stability gaps as unresolved. No row is promoted to `DONE`.

Accepted current-build facts include:

- 14/14 selected D09-D22 anchor sets revalidated;
- 21/21 selected current QMeta types recovered;
- direct protocol queue → container handler routing for the documented families;
- open/close/create/change/delete handler → `TContainerStorage` mutation and storage signal emission;
- direct `TContainerStorage` → `TContainerStorageController` connections for update/remove/manual-sort;
- Set/DeleteInventory → `TInventoryContainer::inventoryChanged`;
- direct `inventoryChanged` → `TPlayerInventoryAndStatusController::onInventoryChanged`.

The exact client fence is `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, ELF Build ID `d803d9695868713ef6ab0c3cf65f91212c9c6a62`.

## Independent audit

Review `4970813830` classified source #559 `ACCEPT_WITH_EDIT`. The only material finding, `INV-AUD-001`, concerned stale/diverged source-branch history rather than evidence semantics. This promotion resolves that finding by copying only accepted task-owned blobs onto fresh trusted `main`; source #559 remains provenance and is not merged.

Semantic material findings open: `0`.

## Runtime and safety boundary

A prior separately admitted read-only observation found the exact-current client at the login screen; inventory/container state was not visible. No credentials, login, GUI input, gameplay, process mutation, debugger/injection or item/container stimulus is part of this promotion. Raw client bytes and passive captures are not retained or promoted.

## Remaining programme gaps

Authenticated live values, full `PlayerInventory` bulk normalization, exact subtype/charge/duration semantics, per-action serialization/server acknowledgements, and restart/relogin stability remain `UNKNOWN` / `NOT_OBSERVED`. This bounded archive does not hide those gaps.

## Lifecycle

After exact-head validation and promotion merge, close source #559 unmerged as superseded, then finalize this archive with promotion CI/review/merge facts and `ownership_released: true` in the mandatory lifecycle-only closeout.
