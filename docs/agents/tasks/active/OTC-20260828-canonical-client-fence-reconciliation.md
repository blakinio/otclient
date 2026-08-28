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
branch: docs/OTC-20260828-canonical-client-fence-reconciliation-readmit
base_branch: main
base_main: 65ec156124458e595ddbc808930116dd89c3c973
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
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Re-admit exactly one reviewed, metadata-only canonical registration reconciliation after the fail-closed first attempt exposed and PR #767 repaired the `remote_view_mapping: UNKNOWN` source-schema overconstraint.

This checkpoint changes only repository admission state. It performs no live action by itself and grants no client mutation, process-memory, GUI/input, login, credential, gameplay, process-control or payload-capture authority.

# Prior live attempt and material repair

The first admitted live attempt was run `33200286357`, job `98947751420`, on trusted main. It passed pre-runtime admission, bounded `RECONCILE`, lease validation and Gate A, then failed before any registration commit with:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_ERROR=source_registration_remote_mapping_invalid
```

PR #767 proved this was an implementation-only overconstraint. The canonical transition schema, historical predecessor Kasm adoption probe and current exact Kasm adoption probe all allow/use a stable `remote_view_mapping: UNKNOWN`; the v1 contract requires equality/continuity rather than `PROVEN` specifically.

TDD repair evidence:

- RED `9c0505ce184ebca402e94d0e6caef2bb7036974a`, run/job `33200847818 / 98949632562`: exactly the stable UNKNOWN regression failed with the live error code;
- minimal production change accepts only canonical `{PROVEN, UNKNOWN}` while the existing source/fresh equality check still rejects mapping drift;
- final restacked repair head `1cf1e302baed42c6a8522e6f2b8e089eb64eb9b6` passed reconciliation run `33201399426`, both governance audits `33201399384`, and CI run `33201399606` including `CI / Required` job `98951644968`;
- PR #767 squash-merged as `65ec156124458e595ddbc808930116dd89c3c973`.

Durable repair evidence is `docs/agents/evidence/OTC-20260828-canonical-client-fence-reconciliation/20260828-unknown-remote-mapping-repair.md`.

# Pending live admission

This is the same narrow pre-Gate-A admission shape already reviewed and tested:

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

The UNKNOWN generations and target uniqueness grant no write authority. The trusted-main live workflow must freshly acquire and validate the canonical lease, prove a controller generation newer than the source binding, validate the closed predecessor fence, prove the exact-current singleton target three times under the canonical guard, and only then atomically reconcile metadata.

# Safety and retry rule

The failed trigger from run `33200286357` is consumed and must not be replayed. This admission PR itself must keep the live workflow skipped. Only after this exact checkpoint is GREEN and merged to protected `main` may one **new** repository-owner comment `RECONCILE_CANONICAL_CLIENT_FENCE` be posted on merged PR #760.

The next live run must accept only:

- `ALREADY_CURRENT` with exact-current fail-closed registration verification;
- complete approved predecessor reconciliation PASS; or
- a new precise fail-closed blocker.

No manual editing of `runtime-registration.json` is permitted.

# Downstream boundary

After successful exact-current registration verification, this recovery authority must be released back to `runtime_access: none`. Then rerun `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. No owner login, character selection, world entry or other GUI action is requested until that memory-free preflight explicitly reports logger readiness.

next_action: obtain fresh exact-head reconciliation/governance/CI GREEN for this single-file re-admission, verify protected-main freshness, safe-squash-merge it, then post one fresh exact `RECONCILE_CANONICAL_CLIENT_FENCE` trigger on #760 and classify the trusted-main result.
