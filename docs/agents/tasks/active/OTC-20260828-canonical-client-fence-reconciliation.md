---
task_id: OTC-20260828-canonical-client-fence-reconciliation
status: live_admission_pending_current_identity_reconciliation_retry
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: live_admission
branch: docs/OTC-20260828-current-identity-reconciliation-readmit-2
base_branch: main
base_main: 12721d07ee435e57ec0b169687890c357078d863
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
  - PR #776 exact-current identity reconciliation support
  - PR #777 prior exact-current reconciliation admission
  - PR #778 prior reconciliation PASS closeout
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Admit exactly one fresh trusted-main metadata-only canonical reconciliation that refreshes a stale exact-current container/PID/start identity without changing the exact client fence or semantic state.

This checkpoint grants only temporary `canonical_recovery` metadata authority. It grants no client mutation, process-memory observation, GUI/input, login, credential, character-selection, gameplay, process-control, payload-capture or semantic-promotion authority. Live execution still requires a new exact owner trigger after this admission is GREEN and merged to protected `main`.

# Why this retry admission is required

Fresh memory-free gameWindowState preflight run `33209672873`, job `98979530228`, at exact `main@12721d07ee435e57ec0b169687890c357078d863` passed trusted-main checkpoint, current-fence validation, command validation and canonical registration ownership. Its global inventory then found exactly one exact-fenced official-client candidate but refused admission with `REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE`.

The canonical registration still named container `otclient-track-a-kasmvnc`, container id prefix `1af4af4d67f5`, PID `13947`, start ticks `51652120`; the unique exact-fenced live candidate no longer matched that registered identity. No process-memory observation or owner UI occurred. This is a new runtime-identity drift after the prior successful reconciliation, not evidence that the previous guarded transaction failed.

# Prior terminal live reconciliation

Fresh owner trigger comment `5456537158` on merged PR #760 created trusted-main workflow run `33201699408`, job `98952477418`, on `synology-otclient-01` at exact head `763806fecc7a0cc1b56fe785dfcadb62ad2dfb9a`.

The live run proved a guarded metadata-only exact-client reconciliation with no client mutation or process-memory observation. The later exact-current refresh described below superseded its runtime identity.

# Prior exact-current identity refresh — PASS

Fresh owner trigger comment `5457186114` on merged PR #760 created trusted-main workflow run `33206484746`, job `98968734937`, on `synology-otclient-01` at exact `main@7edf5bc44c08b762be7ac34104e840b391747fd6`.

The transaction emitted:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PENDING_ADMISSION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PRERUNTIME=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_DECISION=RECONCILE_CURRENT_IDENTITY
TRACK_A_CANONICAL_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS  # three guarded probes
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION=41
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

That source registration was exact-current and fail-closed. The guarded transaction refreshed only canonical runtime identity from three stable exact-current singleton probes under a strictly newer canonical lease generation (`42 > 41`). Final verification retained exact fence and `state: UNKNOWN`; no client process mutation, process-memory observation, GUI/input, login, credentials, character selection, gameplay, packet/payload capture or semantic promotion occurred. The lease was explicitly released.

Durable evidence: `docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/20260828-current-identity-reconciliation-pass.md`.

# Retry authority boundary

This retry admission is intentionally bounded to the same metadata-only contract:

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
```

next_action: after exact-head GREEN and merge, issue one new `RECONCILE_CANONICAL_CLIENT_FENCE` owner trigger, verify the metadata-only transaction and lease release, close authority again, then immediately re-run memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. Owner UI remains unauthorized until that preflight explicitly reports `GAME_WINDOW_STATE_LOGGER_PREFLIGHT=READY`.
