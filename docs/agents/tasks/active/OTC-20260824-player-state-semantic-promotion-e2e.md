---
task_id: OTC-20260824-player-state-semantic-promotion-e2e
status: implementing
agent: ChatGPT
session_role: track_a_runtime_semantic_validator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime_semantic_validation
phase: admission
branch: runtime/OTC-20260824-player-state-semantic-promotion-e2e
base_branch: main
base_main: 5d02cf9885ffb00b8a786ba02568cec1919f9cd6
risk: high
updated: 2026-08-24T15:14:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/tasks/archive/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/evidence/OTC-20260824-player-state-semantic-promotion-e2e/**
  - tools/tibia_re_surveyor/player_state.py
  - tests/tools/tibia_re_surveyor/test_player_state.py
modules_touched:
  - tibia_re_surveyor_player_state
reuses:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - tools/tibia_re_surveyor/player_state.py
  - docs/agents/evidence/OTC-20260824-control-center-package-d-physical-retry-3/runtime-admission-terminal.md
depends_on:
  - OTC-20260824-control-center-package-d-physical-retry-3
blocks:
  - future fresh Package D physical turn E2E
cross_repo_tasks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: physical_runtime
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_stop_at_task_boundary
user_communication: low_noise
track_a_runtime_agent_admission_version: 1
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260824-player-state-semantic-promotion-e2e
runtime_namespace: track-a-canonical-live
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: REQUIRED_NOT_PROVEN
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
credentials_allowed: false
login_allowed: false
character_selection_allowed: false
transaction_authorized: false
physical_action_budget: 1
physical_action_kind: one_tile_movement_only
physical_action_count: 0
ready: false
commit: false
possibly_dispatched: false
---

# Goal

Promote or reject the current exact-build `player_state_typed_reader` as a semantic active-world discriminator using one causal owner-authorized movement differential on the already logged-in Official Tibia session.

This task is not Package D retry 4. It must not execute the Package D `turn` action. A future fresh Package D task may consume only durable promoted evidence from this task.

## Current owner authorization

On 2026-08-24 in the current conversation the owner explicitly stated:

`Zgadzam się na 1 kontrolowany ruch postaci.`

This authorizes exactly one controlled one-tile movement for this semantic causal E2E, and nothing else. It does not authorize login, relogin, credentials, character selection, combat, item use, chat, trade, economy, spells, repeated movement, direct Codex/OpenAI use, or a Package D `turn`.

## Admission state before live client observation

The task begins fail-closed. Current controller/registration/lease state must be rediscovered after this record is persisted. No historical PID, XID, display, window, registration generation, lease generation, or semantic state is inherited.

Required before the one physical movement:

1. current Gate A PASS under the authoritative lease and canonical supervisor;
2. authoritative registration PRESENT and exact current client fence PASS;
3. reviewed generation rebind if current registration/controller generations differ;
4. current Gate B PASS including boot/PID/start/exact-SHA/display/window/target uniqueness;
5. canonical `input.lock` held continuously through final validation, the single movement, and immediate reconciliation;
6. a read-only `player_state_typed_reader` sample immediately before movement with a unique object, mirrored position consistency, plausible XYZ and exact-process fence;
7. exactly one semantic movement primitive whose effect bound is one tile and whose target remains the same canonical client;
8. final revalidation immediately before dispatch.

Any UNKNOWN or REQUIRED_NOT_PROVEN required gate refuses the movement.

## Causal acceptance criteria

The movement may be promoted as semantic evidence only when all of the following are observed in the same admitted runtime generation:

- pre-sample `P0=(x0,y0,z0)` is available from the exact current reader;
- exactly one authorized one-tile movement is dispatched once;
- post-sample `P1=(x1,y1,z1)` is available from the same unique typed object and exact process identity;
- `z1 == z0`;
- Manhattan delta is exactly one: `abs(x1-x0)+abs(y1-y0) == 1`;
- mirrored copies remain equal before and after;
- target identity, Gate B and input-lock authority remain valid through reconciliation;
- no second physical action is attempted regardless of ambiguity or failure.

If COMMIT occurs and outcome becomes uncertain, record `AMBIGUOUS_NO_RETRY`; never retry the movement.

## Promotion boundary

Only after causal PASS may this task change `tools/tibia_re_surveyor/player_state.py` / focused tests to represent the exact reviewed semantic promotion. The promotion must stay exact-client-fenced and fail closed on uniqueness, mirror, plausibility, identity or runtime-state failure. Structural bridge 3-of-3 remains insufficient by itself.

If causal proof fails or cannot legally run, keep `semantic_promotion_allowed: false` and close with the exact blocker.

## Safety/nonclaims

- no credentials or 2FA inspection;
- no login/relogin/character selection;
- no second official-client session;
- no combat/economy/item/spell/chat/trade action;
- no Package D turn;
- no raw runtime identifiers or secrets in user-visible/durable evidence;
- no direct Codex/OpenAI/owner-funded AI invocation;
- at most one movement dispatch total.

## Initial next action

Rediscover controller-plane lease/registration state without observing or mutating the Official Tibia client, update this admission record, then proceed only if a legal current canonical admission path exists.
