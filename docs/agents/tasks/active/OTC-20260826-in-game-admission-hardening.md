---
task_id: OTC-20260826-in-game-admission-hardening
status: planned
phase: investigating
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
current_blocker: NONE
next_action: TDD regressions for pre-READY movement admission and worker direct-invocation defense
---

# In-game admission hardening

Repository-only repair after RETRY-4 demonstrated that a player-state movement path could treat an adopted runtime with `state=UNKNOWN` as sufficient semantic precondition and reach one irreversible `COMMIT`.

Proven data flow on current main:

1. `tibia-official-client-re-kasm-existing-runtime-probe.py` deliberately emits `UNKNOWN` because bridge object presence is not standalone `IN_GAME` proof.
2. canonical `_guarded_dispatch()` checks registration/probe identity stability but has no movement-specific semantic state gate before emitting `READY`.
3. `tibia-official-client-re-player-state-causal-worker.py::validate_registration()` explicitly requires `state == "UNKNOWN"`, so retry-4's preflight accepted the fail-closed state as if it were movement-ready.

Goal: for guarded `kind=move`, `UNKNOWN`, `LOGIN`, `CHARACTER_SELECT`, and `DISCONNECTED` must fail before `READY`; direct worker invocation must also reject non-`IN_GAME` before any input/tool/read/dispatch effect. This task does not create or infer a new `IN_GAME` proof mechanism.
