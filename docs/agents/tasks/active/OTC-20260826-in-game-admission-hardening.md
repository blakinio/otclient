---
task_id: OTC-20260826-in-game-admission-hardening
status: validating
phase: validating
agent: ChatGPT
session_role: owner
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: bugfix
policy_version: 2
branch: fix/OTC-20260826-in-game-admission-hardening
base_branch: main
base_sha: 8a9315e1cd621a5b868010deeec2578266547663
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
repair_status: IMPLEMENTED_AND_HOSTED_GREEN
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
independent_audit: REQUIRED
independent_audit_review: PENDING
exact_final_head: PENDING_BINDING_COMMIT
exact_final_head_causal_timing: REQUIRED
exact_final_head_agent_governance: REQUIRED
exact_final_head_canonical_governance: REQUIRED
exact_final_head_ci: REQUIRED
ownership_released: false
task_archived: false
current_blocker: NONE_AUDIT_CI_ONLY
next_action: freeze this binding head, run fresh independent audit and exact-head hosted checks, merge PR #715, archive task and release ownership
---

# In-game admission hardening

Repository-only repair after RETRY-4 demonstrated that a player-state movement path could treat an adopted runtime with `state=UNKNOWN` as sufficient semantic precondition and reach one irreversible `COMMIT`.

Proven data flow on source main:

1. `tibia-official-client-re-kasm-existing-runtime-probe.py` deliberately emits `UNKNOWN` because bridge object presence is not standalone `IN_GAME` proof.
2. canonical `_guarded_dispatch()` checked registration/probe identity stability but had no movement-specific semantic state gate before emitting `READY`.
3. `tibia-official-client-re-player-state-causal-worker.py::validate_registration()` explicitly required `state == "UNKNOWN"`, so retry-4's preflight accepted the fail-closed state as if it were movement-ready.

Implemented contract: for guarded `kind=move`, current registration and every fresh manifest crossing the guarded-dispatch effect boundary must both be `IN_GAME`; otherwise the request fails closed before `READY` or before the worker effect. Direct worker invocation independently requires `IN_GAME` before any tool/read/dispatch work. This task does not create or infer a new `IN_GAME` proof mechanism.

TDD RED on `9e9a4995c0785617d90967d0ad70cf75c885890e`, run `33014845948`, proved both defects. The minimal repair on `54de1a00b234158a731a30708b3d11d808e0ef55` first passed hosted causal timing run `33015945329`. Strengthened boundary coverage was then added for `UNKNOWN`, `LOGIN`, `CHARACTER_SELECT`, `DISCONNECTED`, post-READY state drift, and a synthetic positive `IN_GAME` path.

The fully strengthened boundary candidate `d2e52ff261805014399c856ce3a024f58fa6cace` passed Track A causal timing `33016340057`, agent runtime governance `33016340032`, canonical live governance `33016340047`, hosted XRes validation `33016340059`, repository CI `33016340233`, and `CI / Required` job `98335600449`. Durable root-cause/repair evidence is stored at `docs/agents/evidence/OTC-20260826-in-game-admission-hardening/root-cause-and-repair.md`.

The task has not proven any current client `IN_GAME`; current adoption semantics remain fail-closed. No future physical action is authorized by this task.
