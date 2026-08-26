---
task_id: OTC-20260826-in-game-admission-hardening
status: completed
result: ROOT_CAUSE_PROVEN_AND_REPAIRED
phase: archived
agent: ChatGPT
session_role: released
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: bugfix
policy_version: 2
branch: docs/OTC-20260826-in-game-admission-hardening-archive
base_branch: main
base_sha: 43653aeffc08a70ecd4a7a53b4be90f528e62b99
risk: high
execution_mode: github_hosted
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
physical_action_budget: 0
physical_action_count: 0
semantic_promotion_performed: false
root_cause_status: PROVEN
repair_status: MERGED
no_new_ingame_producer: true
tdd_red_head: 9e9a4995c0785617d90967d0ad70cf75c885890e
tdd_red_run: 33014845948
tdd_green_head: 54de1a00b234158a731a30708b3d11d808e0ef55
tdd_green_run: 33015945329
boundary_validation_head: d2e52ff261805014399c856ce3a024f58fa6cace
boundary_validation_causal_timing_run: 33016340057
boundary_validation_agent_governance_run: 33016340032
boundary_validation_canonical_governance_run: 33016340047
boundary_validation_xres_run: 33016340059
boundary_validation_ci_run: 33016340233
boundary_validation_required_job: 98335600449
boundary_validation: PASS
durable_evidence: docs/agents/evidence/OTC-20260826-in-game-admission-hardening/root-cause-and-repair.md
implementation_pr: 715
implementation_exact_final_head: ee4adcfee582e53ce8c717d21b1b4caf2203d356
implementation_audit_review: 5035317009
implementation_audit: PASS
implementation_audit_material_findings_open: 0
implementation_causal_timing_run: 33016493691
implementation_causal_timing: PASS
implementation_agent_governance_run: 33016493675
implementation_agent_governance: PASS
implementation_canonical_governance_run: 33016493683
implementation_canonical_governance: PASS
implementation_xres_run: 33016493615
implementation_xres: PASS
implementation_ci_run: 33016493792
implementation_ci: PASS
implementation_required_context: CI / Required
implementation_required_job: 98336204700
implementation_merge_commit: 43653aeffc08a70ecd4a7a53b4be90f528e62b99
ownership_released: true
task_archived: true
archive_pr: 716
archive_independent_audit: REQUIRED
archive_independent_audit_review: PENDING
archive_independent_audit_material_findings_open: UNKNOWN
archive_exact_head_governance: REQUIRED
archive_exact_head_ci: REQUIRED
archive_merged: false
current_blocker: NONE_ARCHIVE_CLOSEOUT_ONLY
next_action: run fresh archive audit and exact-head governance/CI on PR #716, merge, then bind terminal archive metadata
---

# In-game admission hardening — terminal archive

The admission bug is proven and the two-layer repair is merged in PR #715 as `43653aeffc08a70ecd4a7a53b4be90f528e62b99`.

The proven pre-repair composition was: existing-runtime adoption intentionally produced `state=UNKNOWN`; canonical guarded dispatch fenced identity without a movement-specific semantic state gate; and the player-state causal worker explicitly accepted UNKNOWN. This allowed an UNKNOWN runtime to cross the movement READY/COMMIT boundary in RETRY-4.

The merged repair requires both canonical registration and each fresh probe manifest to be exactly `IN_GAME` for guarded `kind=move`, with checks before READY and again before the worker effect. Direct causal-worker invocation independently requires `IN_GAME`. `UNKNOWN`, `LOGIN`, `CHARACTER_SELECT`, and `DISCONNECTED` are covered by permanent fail-closed tests, as is a post-READY drift to UNKNOWN. A synthetic positive IN_GAME path is also covered so the guard is not a blanket movement disable.

No new `IN_GAME` producer was introduced. Current `existing_runtime_adoption_v1` semantics remain deliberately fail-closed; this task does not prove that any current client is logged in or in the game world. A future physical movement attempt therefore remains blocked until a separately trustworthy IN_GAME proof source exists, and any physical action would require separate owner authorization.

The implementation exact final head `ee4adcfee582e53ce8c717d21b1b4caf2203d356` passed validator review `5035317009`, Track A causal timing `33016493691`, agent runtime governance `33016493675`, canonical live governance `33016493683`, hosted XRes `33016493615`, repository CI `33016493792`, and `CI / Required` job `98336204700` before merge.

This lifecycle performed zero runtime/client observations, zero login/relog/restart/character selection, zero gameplay input, zero READY, zero COMMIT, zero physical actions, zero credentials, and zero process-memory writes. Durable evidence remains at `docs/agents/evidence/OTC-20260826-in-game-admission-hardening/root-cause-and-repair.md`.
