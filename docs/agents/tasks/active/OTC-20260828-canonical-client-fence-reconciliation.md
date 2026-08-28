---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: live_admission_pending
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: live_admission
branch: docs/OTC-20260828-canonical-client-fence-reconciliation-admission
base_branch: main
base_main: 911ba621923513b061ba71f19a2ea281f806cdee
created: 2026-08-28T22:00:00+02:00
risk: high
execution_class: self_hosted
execution_mode: github_actions_metadata_reconciliation
runtime_access: canonical_recovery
runtime_owner_task: OTC-20260828-canonical-client-fence-reconciliation
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
recovery_mode: client_fence_reconciliation_v1
client_fence_reconciliation_contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/decisions/ADR-0002-track-a-canonical-client-fence-reconciliation.md
  - docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/**
  - docs/agents/tasks/active/OTC-20260828-canonical-client-fence-reconciliation.md
modules_touched:
  - track-a-canonical-live-runtime
  - track-a-runtime-agent-admission
reuses:
  - merged canonical lease guard-run supervisor
  - merged current Kasm existing-runtime adoption probe
  - PR #754 trusted exact-current client fence
  - PR #760 gameWindowState preflight blocker evidence
  - PR #763 merged client-fence reconciliation implementation
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Admit exactly one reviewed, metadata-only canonical registration reconciliation for the exact predecessor fence left behind after repository current-client authority advanced in PR #754.

The implementation was squash-merged in PR #763 as `911ba621923513b061ba71f19a2ea281f806cdee`. This checkpoint changes only repository admission state. It performs no live action by itself and grants no client mutation, login, GUI/input, process-memory, process-control, credential, gameplay or network-payload authority.

# Root cause

The gameWindowState memory-free preflight run `33193448068`, job `98924502254`, stopped at canonical registration resolution with `REGISTRATION_CLIENT_VERSION_MISMATCH`. No process-memory observation occurred.

Current transition `_read()` correctly rejects any registration outside the current exact fence. Existing rebind, stale-registration recovery and boot-epoch recovery all begin from that strict read and intentionally do not authorize exact-client fence replacement. Adoption/bootstrap cannot be substituted because the authoritative registration is present.

# Design boundary

The live reconciliation must follow `TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md` and ADR-0002:

- exact source fence only: `15.32 / 52109920 / ed5469b9...`;
- exact target fence only: `15.32.75d4a0 / 52105824 / d1a16819...`;
- source must be fail-closed `existing_runtime_adoption_v1`;
- target must be proven by three stable current Kasm adoption probes;
- same canonical Docker container name/display/remote-view endpoint/mapping;
- current controller generation newer than source registration generation binding;
- atomic `registration_generation + 1` replacement and exact-own-record rollback;
- result forced to `state: UNKNOWN`;
- execution only as a finite child under reviewed canonical lease `guard-run`;
- no client launch/stop/signal/restart/attach/injection/input/login/credentials/gameplay/process-memory observation.

# TDD and implementation evidence

Primary implementation RED was captured at `95a49119f8f8866c9761bcb587ca62719f416dc1`, run `33195284267`, job `98930734507`.

Primary implementation GREEN was established at `fe998516ecfd816fb053e0b56158d6aa7f9466e1`, run `33195900581`, job `98932830802`; same-head Track A governance run `33195900573` passed jobs `98932830815` and `98932831016`.

A separate admission-review RED was captured at `e45da7114663d9276ce9225889ae1aa4ae746dea`, run `33196302067`, job `98934193806`, proving that UNKNOWN generation discovery needed a narrowly named pre-Gate-A recovery mode rather than a global relaxation.

The exact mode-specific governance GREEN was then captured at `3bc47b1442723a9f7e60a5cc5e9c2526ad9550c0`, run `33196798715`, job `98935886243`; legacy canonical recovery remained fail-closed.

Final implementation head `f68c35d5894f254e01dbeda50251a58db3dbd9e5` passed reconciliation, current-client-fence, Track A admission/governance, canonical-live governance and CI Required before PR #763 was squash-merged as `911ba621923513b061ba71f19a2ea281f806cdee`.

# Pending live admission

This checkpoint intentionally uses the only pre-Gate-A admission shape allowed for this reviewed migration:

```yaml
runtime_access: canonical_recovery
recovery_mode: client_fence_reconciliation_v1
client_fence_reconciliation_contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
```

The UNKNOWN generations are deliberate. They are not write authority. The trusted-main live workflow must freshly acquire the canonical lease, prove a strictly newer current controller generation, validate the approved predecessor registration, prove the exact-current singleton target and target uniqueness under the canonical guard, and only then may the reviewed helper atomically reconcile registration metadata.

# Live-use rule

This admission PR itself must not execute the live reconciliation. Only after this exact admission is merged green to protected `main` may the repository owner post the exact trigger `RECONCILE_CANONICAL_CLIENT_FENCE` on #760.

The live workflow must accept only:

- `ALREADY_CURRENT`, if the registration is already exact-current and fail-closed;
- a complete approved predecessor reconciliation PASS; or
- a precise fail-closed blocker.

No owner login/character/world action is requested during reconciliation. After an exact-current `state: UNKNOWN` registration is verified, this recovery authority must be released and the memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION` must be rerun before any owner UI interaction.

# Acceptance

1. This PR changes only the active admission task.
2. Track A runtime governance accepts the exact named recovery mode and exact contract binding.
3. Both generation values remain UNKNOWN before Gate A and target uniqueness remains UNKNOWN.
4. Mutation, login, process control, process memory, GUI/input, gameplay and payload capture remain unauthorized.
5. PR-event live reconciliation stays skipped.
6. Protected-main freshness and exact-head checks are verified before squash merge.
7. After merge, one fresh exact owner-authored reconciliation trigger is consumed and classified.
8. Recovery authority is released after terminal reconciliation result before downstream gameWindowState observation.

next_action: merge this repository-only admission after fresh exact-head governance/CI, then post one fresh exact `RECONCILE_CANONICAL_CLIENT_FENCE` trigger on #760 and classify the trusted-main live result without manually editing canonical registration.
