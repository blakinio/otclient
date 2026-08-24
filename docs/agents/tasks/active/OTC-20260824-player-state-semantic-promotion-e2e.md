---
task_id: OTC-20260824-player-state-semantic-promotion-e2e
status: implementing
agent: ChatGPT
session_role: track_a_runtime_semantic_validator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime_semantic_validation
phase: runtime_infra_repair
branch: runtime/OTC-20260824-player-state-semantic-promotion-e2e
base_branch: main
base_main: 5d02cf9885ffb00b8a786ba02568cec1919f9cd6
risk: high
updated: 2026-08-24T15:42:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/tasks/archive/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/evidence/OTC-20260824-player-state-semantic-promotion-e2e/**
  - .github/workflows/otc-20260824-player-state-semantic-promotion-e2e.yml
  - .github/scripts/tibia-official-client-re-player-state-semantic-worker.py
  - .github/scripts/test_tibia_official_client_re_player_state_semantic_worker.py
  - tools/tibia_re_surveyor/player_state.py
  - tests/tools/tibia_re_surveyor/test_player_state.py
modules_touched:
  - tibia_re_surveyor_player_state
reuses:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-input-lock.py
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
canonical_registration: PRESENT
canonical_lease_status: active
canonical_lease_generation: 22
registration_lease_generation: 19
gate_a: PASS
generation_rebind: BLOCKED_STALE_BRIDGE_SOCKET
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN_BY_CURRENT_PROBE_DIAGNOSTIC
mutation_authorized: false
runtime_helper_cleanup: ORPHAN_BRIDGE_SOCKET_ONLY
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

## Fresh controller-plane checkpoint

The first persisted discovery, before any live-client observation by this task, found a released generation-19 lease and a generation-19 exact-build registration. Two temporary workflow-triggered controller generations later returned to `released`; they are not accepted as this task's admission evidence because this task requires a durable persist barrier after acquisition and before rebind.

A new direct controller-plane acquisition using the reviewed repository lease implementation then produced:

```yaml
lease_status: active
lease_generation: 22
lease_owner_matches_task: true
canonical_registration: PRESENT
registration_lease_generation: 19
gate_a: PASS
generation_rebind_required: true
physical_action_count: 0
```

Generation 22 is the authoritative admission generation. The raw capability token remains mode-0600 in the task-local state path and was neither printed nor read by the agent.

## Rebind blocker and bounded infrastructure repair

The reviewed Kasm probe was executed only after generation 22 had been persisted. The rebind failed closed before changing the registration:

```yaml
rebind: FAIL
transition_error: probe_worker_failed
official_client_exact_candidate_count: 1
exact_client_fence: PASS
window_proof: PASS
structural_bridge_transport: FAIL
bridge_socket_path_present: true
bridge_listener_present: false
bridge_library_loaded_in_current_client: false
character_socket_path_present: true
character_listener_present: false
auth_socket_path_present: false
physical_action_count: 0
```

This proves the `bridge.sock` pathname is an orphaned helper artifact rather than a live peer endpoint for the current client. The only infrastructure mutation admitted before rebind is therefore a guarded removal of exactly that orphaned `bridge.sock` path, after revalidating immediately inside the guarded command that the current client has no bridge library loaded and that the socket has no listener. This cleanup does not authorize or perform client input, process control, login, restart, injection, helper activation, credential access, or gameplay mutation. `character.sock` is not removed by this repair because it is not required to restore the Kasm adoption probe.

If either no-listener or no-loaded-helper proof changes, cleanup is refused.

## Required before live mutation

1. current Gate A PASS under the authoritative lease and canonical supervisor;
2. authoritative registration PRESENT and exact current client fence PASS;
3. reviewed generation rebind after the bounded orphan-socket repair;
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

## Next action

Under the still-current generation-22 lease, use the reviewed lease `guard-run` supervisor to revalidate and remove only the proven orphan `bridge.sock`. Re-run the Kasm probe afterward; if it reports the socket absent and current target remains unique/exact, retry the reviewed rebind once. No movement is permitted in this repair/rebind step.
