---
task_id: OTC-20260819-track-a-inventory-containers-runtime
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: source_ready_for_independent_audit_and_clean_promotion
branch: research/OTC-20260819-track-a-inventory-containers-runtime
base_branch: main
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-inventory-containers-runtime.md
  - docs/agents/evidence/OTC-20260819-track-a-inventory-containers-runtime/**
modules_touched:
  - track-a-research-evidence
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s5-container-inbound-static/result.json
  - docs/agents/evidence/OTC-20260818-track-a-s7-inventory-equipment-static/result.json
  - docs/agents/evidence/OTC-20260818-track-a-s9-action-control-static-census/result.json
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_type_semantics.jsonl
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
track_a_runtime_agent_admission_version: 1
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
owner_funded_ai_api_authorized: false
fence_merge_pr: 555
fence_merge_commit: 2e572789a2bc4b64c5e906c4515c15c625f6bc9e
current_client_version_token: '15.32'
current_client_size: 52109920
current_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_client_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
current_selected_static_rows_passed: 14/14
current_selected_qmeta_types_recovered: 21/21
current_queue_handler_routing: FACT_LISTED_FAMILIES
current_handler_storage_routing: FACT_OPEN_CLOSE_CREATE_CHANGE_DELETE
current_storage_controller_routing: FACT_UPDATED_REMOVED_MANUAL_SORT
current_inventory_status_routing: FACT_SET_DELETE_AND_INVENTORY_CHANGED_CONTROLLER_CONNECT
passive_runtime_observation: LOGIN_SCREEN_NO_INVENTORY_STATE_VISIBLE
raw_proprietary_client_retained: false
raw_runtime_capture_retained: false
e2e_result: NOT_APPLICABLE
e2e_reason: bounded reverse-engineering evidence task; no product feature or authorized state-changing live journey is delivered by this task; authenticated live semantics remain explicitly outside the bounded result
invocation_started_at: 2026-08-19T10:45:00+02:00
last_progress_at: 2026-08-19T11:25:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: source-audit
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
current_blocker: INDEPENDENT_AUDIT_AND_CLEAN_PROMOTION_NOT_YET_COMPLETE
next_action: run a fresh validator-role audit from primary exact-build evidence, then promote accepted task-owned blobs on a one-commit current-main branch
---

# TIBIA-RE-INVENTORY-CONTAINERS

## Bounded acceptance

This task owns D09-D22 inventory/equipment/container research evidence. Its bounded completion criterion is a current-build, evidence-separated structural/causal checkpoint; it does not redefine the broader programme's authenticated live-value, serialization or restart-stability acceptance criteria.

Source researcher PR: #559.

## Implementation result

Current exact client:

```text
version token: 15.32
size:          52109920
sha256:        ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID:  d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Completed source evidence now proves:

- 14/14 selected D09-D22 current-build anchor sets;
- 21/21 selected current QMeta types independently recovered;
- direct current queue→container-handler routing for the documented inventory/container/stash/depot/managed families;
- container open/close/create/change/delete handler→`TContainerStorage` mutations and storage signal emissions;
- direct `TContainerStorage`→`TContainerStorageController` connections for update/remove/manual-sort;
- Set/DeleteInventory→`TInventoryContainer::inventoryChanged`;
- direct `inventoryChanged`→`TPlayerInventoryAndStatusController::onInventoryChanged`.

All fourteen rows remain recommended `PARTIAL`; no row is `DONE`.

Primary final result:

- `docs/agents/evidence/OTC-20260819-track-a-inventory-containers-runtime/result.md`
- `docs/agents/evidence/OTC-20260819-track-a-inventory-containers-runtime/result.json`
- `docs/agents/evidence/OTC-20260819-track-a-inventory-containers-runtime/20260819-current-state-propagation-routing.md`
- `docs/agents/evidence/OTC-20260819-track-a-inventory-containers-runtime/current_state_propagation_routing.json`

## Passive runtime phase

A fresh later invocation successfully persisted `runtime_access: read_only`, proved one unique exact-current client on `otclient-track-a-kasmvnc / DISPLAY=:1`, and captured one passive X11 frame. The client was at the login screen, so no D09-D22 state was visible.

No GUI input, credentials, login, gameplay, process mutation, debugger/injection or item/container stimulus was performed. Raw screenshots and task-local raw current-client copies were deleted and cleanup was verified.

The task has now reduced itself back to `runtime_access: none`; no runtime ownership remains claimed.

## Remaining programme work, not hidden by this closeout

The bounded result does not prove authenticated live inventory/container values, full `PlayerInventory` bulk normalization, exact subtype/charge/duration semantics, per-action serialization/server acknowledgements, or restart/relogin stability. These remain explicit programme-level live/stability gaps and are not grounds to falsify this bounded static/causal research checkpoint as `DONE`.

## Closeout path

Source implementation is coherent. Before `completed`, repository policy still requires:

1. fresh independent validator-role audit of the exact source evidence/diff;
2. clean one-commit promotion from current `main` containing only accepted task-owned evidence/archive paths;
3. exact-head CI and zero unresolved review threads;
4. source #559 closed superseded after successful promotion;
5. lifecycle-only archive/ownership release if the promotion record cannot contain terminal merge facts.
