---
task_id: OTC-20260826-in-game-admission-hardening
status: implementing
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
tdd_red_head: 9e9a4995c0785617d90967d0ad70cf75c885890e
tdd_red_run: 33014845948
tdd_green_head: 54de1a00b234158a731a30708b3d11d808e0ef55
tdd_green_run: 33015945329
tdd_green: PASS
current_blocker: NONE_VALIDATION_ONLY
next_action: obtain clean governance and repository CI on the current head, record durable evidence, run independent exact-head audit, merge and archive
---

# In-game admission hardening

Repository-only repair after RETRY-4 demonstrated that a player-state movement path could treat an adopted runtime with `state=UNKNOWN` as sufficient semantic precondition and reach one irreversible `COMMIT`.

Proven data flow on source main:

1. `tibia-official-client-re-kasm-existing-runtime-probe.py` deliberately emits `UNKNOWN` because bridge object presence is not standalone `IN_GAME` proof.
2. canonical `_guarded_dispatch()` checked registration/probe identity stability but had no movement-specific semantic state gate before emitting `READY`.
3. `tibia-official-client-re-player-state-causal-worker.py::validate_registration()` explicitly required `state == "UNKNOWN"`, so retry-4's preflight accepted the fail-closed state as if it were movement-ready.

Implemented contract: for guarded `kind=move`, current registration and every fresh manifest crossing the guarded-dispatch effect boundary must both be `IN_GAME`; otherwise the request fails closed before `READY` or before the worker effect. Direct worker invocation independently requires `IN_GAME` before any tool/read/dispatch work. This task does not create or infer a new `IN_GAME` proof mechanism.

TDD RED on `9e9a4995c0785617d90967d0ad70cf75c885890e`, run `33014845948`, proved both defects: canonical emitted READY instead of raising the new semantic admission refusal, and the worker returned post-dispatch `AMBIGUOUS` instead of pre-dispatch `REFUSED` for an UNKNOWN registration. The minimal repair on `54de1a00b234158a731a30708b3d11d808e0ef55` passed hosted causal timing run `33015945329`.
