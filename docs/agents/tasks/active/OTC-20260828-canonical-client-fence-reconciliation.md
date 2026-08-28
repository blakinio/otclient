---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: live_admission_pending_current_identity_reconciliation
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: live_admission
branch: docs/OTC-20260828-current-identity-reconciliation-readmit
base_branch: main
base_main: d013efbc3a2df0becca59488a5bb6f4f89cc7bd4
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
  - PR #766 first recovery admission
  - PR #767 merged UNKNOWN remote-mapping repair
  - PR #770 repaired recovery re-admission
  - PR #774 recorded fresh gameWindowState preflight identity mismatch
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Admit exactly one fresh trusted-main metadata-only canonical reconciliation that refreshes the stale exact-current container/PID/start identity proven by gameWindowState preflight run `33204467524` without changing the exact client fence or semantic state.

This checkpoint grants only temporary `canonical_recovery` metadata authority. It grants no client mutation, process-memory observation, GUI/input, login, credential, character-selection, gameplay, process-control, payload-capture or semantic-promotion authority. Live execution still requires a new exact owner trigger after this admission is GREEN and merged to protected `main`.

# Terminal live reconciliation

Fresh owner trigger comment `5456537158` on merged PR #760 created trusted-main workflow run `33201699408`, job `98952477418`, on `synology-otclient-01` at exact head `763806fecc7a0cc1b56fe785dfcadb62ad2dfb9a`.

The live run proved:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PENDING_ADMISSION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PRERUNTIME=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_DECISION=RECONCILE
TRACK_A_CANONICAL_LEASE_GENERATION=41
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS  # three independent guarded probes
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION=41
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION=35
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_TARGET_UNIQUENESS=PROVEN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_MUTATION_AUTHORIZED=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_STATE=UNKNOWN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CLIENT_PROCESS_MUTATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PROCESS_MEMORY_OBSERVATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_SEMANTIC_PROMOTION=false
TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC=0
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_RELEASE=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_CURRENT=PASS
```

The final verification required the canonical registration to be an owner-owned mode-0600 regular file, exact-fenced to:

- version `15.32.75d4a0`;
- size `52105824`;
- SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- `state: UNKNOWN`.

No client process mutation, process-memory observation, GUI/input, login, credential access, gameplay, payload capture or semantic promotion occurred.

The prior failed run `33200286357 / 98947751420` remains historical fail-closed evidence only; it was not replayed. The successful run consumed the new post-repair trigger after #767 and #770.

# Main movement after live PASS

The live workflow twice verified that `main` remained exactly `763806fecc7a0cc1b56fe785dfcadb62ad2dfb9a` before reconciliation authority was exercised. After the workflow completed, unrelated field6 PRs #769 and #771 advanced protected main to `32146659213cba71910cbe8d46aa4c2f6ded607c`. Those later changes do not touch canonical registration/reconciliation owned paths and do not invalidate the already completed guarded live transaction.

# Fresh current-identity recovery admission

The fresh gameWindowState preflight recorded by PR #774 proved the canonical registration fence and ownership were valid, and then proved exactly one exact-fenced official-client target existed but did not match the registered container/PID/start identity (`REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE`). PR #776 merged the TDD repair that routes an exact-current registration through the same cancellation-safe guarded reconciliation transaction.

This admission is intentionally pre-runtime and bounded:

```yaml
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
```

The UNKNOWN generations and target uniqueness grant no write authority. The trusted-main workflow must freshly acquire the canonical lease, prove a controller generation newer than the source registration binding, re-prove the exact-current singleton identity three times under the canonical `guard-run`, atomically refresh only canonical registration metadata, verify `state: UNKNOWN`, and release the lease. Any ambiguity fails closed.

The old successful trigger `5456537158` is consumed and must not be replayed. A new owner comment with exact body `RECONCILE_CANONICAL_CLIENT_FENCE` on merged PR #760 is required only after this admission PR is merged and fresh `main` is revalidated.

# Downstream next action

After one successful same-fence identity reconciliation, persist sanitized durable PASS evidence and return this task to `runtime_access: none` in a separate repository-only closeout PR. Then rerun a new memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. Owner UI remains unauthorized unless that preflight explicitly emits `GAME_WINDOW_STATE_LOGGER_PREFLIGHT=READY`.

next_action: merge this admission after exact-head governance/CI, issue one fresh owner reconciliation trigger on PR #760, verify three-probe exact-current identity refresh and lease release, then close recovery authority before retrying gameWindowState preflight.
