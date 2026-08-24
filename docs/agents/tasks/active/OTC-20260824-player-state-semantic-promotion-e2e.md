---
task_id: OTC-20260824-player-state-semantic-promotion-e2e
status: implementing
agent: ChatGPT
session_role: track_a_runtime_semantic_validator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime_semantic_validation
phase: code_repair
branch: runtime/OTC-20260824-player-state-semantic-promotion-e2e
base_branch: main
base_main: 5d02cf9885ffb00b8a786ba02568cec1919f9cd6
risk: high
updated: 2026-08-24T15:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/tasks/archive/OTC-20260824-player-state-semantic-promotion-e2e.md
  - docs/agents/evidence/OTC-20260824-player-state-semantic-promotion-e2e/**
  - .github/workflows/otc-20260824-player-state-semantic-promotion-e2e.yml
  - .github/scripts/tibia-official-client-re-player-state-semantic-worker.py
  - .github/scripts/test_tibia_official_client_re_player_state_semantic_worker.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - tools/tibia_re_surveyor/player_state.py
  - tests/tools/tibia_re_surveyor/test_player_state.py
modules_touched:
  - tibia_re_surveyor_player_state
  - track_a_canonical_live_transition
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
runtime_access: none_during_code_repair
runtime_owner_task: none
runtime_namespace: track-a-canonical-live
canonical_registration: PRESENT_STALE_LEASE_BINDING
canonical_lease_status: released
canonical_lease_generation: 22
registration_lease_generation: 19
gate_a: RELEASED_AFTER_BLOCKER
generation_rebind: BLOCKED_CODE_REPAIR
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN_BY_GENERATION_22_DIAGNOSTIC
mutation_authorized: false
runtime_helper_cleanup: COMPLETED_ORPHAN_BRIDGE_SOCKET_ONLY
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

## Owner authorization

On 2026-08-24 the owner explicitly stated:

`Zgadzam się na 1 kontrolowany ruch postaci.`

This authorizes exactly one controlled one-tile movement for this semantic causal E2E, and nothing else. It does not authorize login, relogin, credentials, character selection, combat, item use, chat, trade, economy, spells, repeated movement, direct Codex/OpenAI use, or a Package D `turn`.

## Generation-22 admission and infrastructure diagnosis

A direct controller-plane acquisition using the reviewed repository lease implementation produced an active generation-22 lease owned by this task. The generation was persisted before any current-client rebind attempt.

The reviewed Kasm probe then proved:

```yaml
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

The first rebind therefore failed closed with `probe_worker_failed` and did not update the registration.

## Completed bounded helper cleanup

After the no-listener and no-loaded-helper facts were durably recorded, generation 22 remained current. Under the canonical lease `guard-run` supervisor the task revalidated exact client size/SHA, singleton client identity, absence of the bridge library in the current process, and absence of a bridge listener, then removed only the orphaned `bridge.sock` pathname. The guarded command returned zero and revalidated that the pathname no longer existed.

This was helper-infrastructure cleanup only. It performed no keyboard/mouse input, process control, restart, injection, login, credential access, character selection or gameplay action. `physical_action_count` remained 0. `character.sock` was deliberately left untouched because it was not required for Kasm adoption recovery.

The generation-22 lease was then released and its private task-local token removed before code repair began.

## Newly proven code blocker

With the dead bridge socket absent, the Kasm probe would correctly report fail-closed `UNKNOWN / NO_STRUCTURAL_BRIDGE`. The current canonical rebind implementation cannot consume that legitimate transition from the existing `UNKNOWN / BRIDGE_3_OF_3_SEMANTICS_UNPROVEN` registration because `_probe_reg(..., old=True)` calls the full `_match()` before rebind and requires `state_evidence` to be byte-for-byte unchanged. `_rebind()` also does not copy refreshed adoption `state_evidence` into the new registration.

This is a direct task blocker, not a reason to bypass the registration. No other active task in the current checkout declares ownership of `tibia-official-client-re-canonical-live-transition.py`, so this task now owns the transition implementation and focused tests for the narrow repair.

## Repair invariant

The repair may allow an adoption rebind to refresh only fail-closed adoption evidence while preserving exact stable identity:

- old and new semantic state must both remain `UNKNOWN`;
- old/new evidence must be one of `BRIDGE_3_OF_3_SEMANTICS_UNPROVEN` or `NO_STRUCTURAL_BRIDGE`;
- `proof_kind` remains the adoption proof kind;
- boot identity, PID, start ticks, exact client version/size/SHA, display, runtime locator, complete-inventory proof, candidate count/fingerprint and stable window identity base must remain identical;
- any stable identity drift still refuses rebind;
- final post-write probe must exactly match the refreshed registration;
- rollback behavior on post-write failure remains unchanged.

TDD status before implementation:

```yaml
new_test_adoption_rebind_refreshes_fail_closed_state_evidence: RED_expected
observed_error: registered_identity_state_evidence_mismatch
new_test_adoption_rebind_rejects_stable_identity_drift: RED_expected
```

After the local implementation, both focused tests pass. Full existing transition/lease/guard validation and repository CI remain required before the repaired rebind can be used on the physical runtime.

## Required before the authorized movement

1. merge or otherwise place the reviewed rebind repair on trusted `main` before using it as runtime authority;
2. fresh task admission from then-current controller state;
3. Gate A PASS;
4. reviewed generation rebind PASS if required;
5. Gate B PASS with exact singleton target;
6. pre-movement read-only player-state sample AVAILABLE with unique mirrored position;
7. canonical `input.lock` held continuously through final validation, exactly one movement dispatch and immediate reconciliation;
8. exactly one one-tile movement, never retried after COMMIT;
9. post-sample from the same exact process/object with same Z and Manhattan delta exactly 1.

Any UNKNOWN or REQUIRED_NOT_PROVEN required gate refuses the movement.

## Promotion boundary

Only after causal PASS may this task change `tools/tibia_re_surveyor/player_state.py` / focused tests to represent the exact reviewed semantic promotion. Structural bridge 3-of-3 remains insufficient by itself.

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

Commit the tested canonical rebind repair and focused regression tests to PR #688, run exact-head repository/Track A governance checks, and do not reacquire physical runtime until the repair is trusted by repository policy.
