---
task_id: OTC-20260819-track-a-creature-combat-static-g0
status: investigating
agent: chatgpt-gpt-5.6-sol
session_id: 20260819-creature-combat-g0
session_role: researcher
project_lane: otclient
lane: P0-STATE
task_kind: discovery
phase: investigate
branch: research/OTC-20260819-track-a-creature-combat-static-g0
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
created: 2026-08-19T09:35:00+02:00
updated: 2026-08-19T09:35:00+02:00
risk: low
execution_mode: github_only
execution_reason: deterministic current-package static census and evidence processing; physical session is not required
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: consumer_of_runtime_evidence
PHYSICAL_E2E_REQUIRED: false
track_id: official-client-re
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
implementation_authorized: true
e2e_required: false
decomposition_decision: single
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-creature-combat-static-g0.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-creature-combat-static-g0.md
  - docs/agents/evidence/OTC-20260819-track-a-creature-combat-static-g0/**
  - .github/workflows/track-a-creature-combat-static-g0.yml
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
depends_on:
  - PR #536 coverage matrix as read-only status vocabulary
  - PR #539/S10 action-protocol evidence as read-only overlap boundary
  - PR #555 current-client-fence advance as read-only provenance context only
blocks: []
related_prs:
  - 528
  - 536
  - 539
  - 540
  - 550
  - 555
---

# Track A creature/combat static G0

## Objective

Execute owner alias `TIBIA-RE-CREATURE-COMBAT` as one bounded current-package static research slice for primary coverage `D01-D08` and structural leads relevant to `C15-C17`, without taking over the shared physical runtime or S10 action-protocol ownership.

Research targets:

- creature-family inbound dispatch and registry/lifecycle names;
- creature health/outfit/speed/skull/party/marks/light/type/unpass state surfaces;
- creature HUD/status-effect surfaces;
- battle-list models, filtering, sorting and secondary lists;
- target selection plus attack/follow/cancel structural action/state surfaces;
- current-package generated-message/protocol names relevant to those families.

Runtime combat causality remains `UNKNOWN` unless separately proven by an admitted physical-runtime task. This G0 task must not initiate combat or send game input.

## Authority and isolation

```yaml
runtime_access: none
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

The official Linux client may be fetched and decompressed only inside an ephemeral GitHub-hosted static-analysis job. It must never be executed, logged into, mutated, committed, or uploaded. Only compact sanitized text evidence may be retained, and raw package/client bytes must be deleted before artifact upload.

Shared canonical coverage/knowledge files, PR #536 paths, PR #539/S10 paths, PR #528/#550 runtime state, and PR #540 spawn/mechanics paths are read-only dependencies and not owned by this researcher.

## Acceptance inventory

- [ ] Fresh current public Linux package is fetched in a GitHub-hosted ephemeral job and exact packed/unpacked identity is fenced.
- [ ] Creature/battle/combat QMeta class/method ownership is enumerated without relying on the disproven per-method jump-target heuristic from world/minimap G0.
- [ ] Relevant generated protobuf/message and neutral string surfaces are enumerated.
- [ ] D01-D08 and C15-C17 findings are classified as FACT / INFERENCE / UNKNOWN without runtime overclaim.
- [ ] Negative scope control proves no credentials, login, gameplay, runtime observation, client execution, client mutation, or raw-client artifact retention.
- [ ] Temporary producer workflow is removed before the final research head.
- [ ] Task-owned report/evidence paths contain enough information for a fresh coordinator to audit without chat history.
- [ ] Exact-head repository checks are recorded for the final Draft head.

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
implementation_status: research_in_progress
physical_e2e: NOT_APPLICABLE
physical_e2e_reason: static reverse-engineering evidence package with runtime_access none
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: 20260819-creature-combat-g0
  session_started_at: 2026-08-19T09:35:00+02:00
  checkpointed_at: 2026-08-19T09:35:00+02:00
  last_progress_at: 2026-08-19T09:35:00+02:00
  phase: investigate
  exact_head: task-claim-commit
  pull_request: none
  active_operation: none
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: null
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: branch and owned paths remain non-overlapping
  next_action: Open the Draft PR, then add and run the bounded GitHub-hosted current-package creature/combat static producer.
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T09:35:00+02:00
last_progress_at: 2026-08-19T09:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```
