---
task_id: OTC-20260819-track-a-creature-combat-static-g0
status: validating
agent: chatgpt-gpt-5.6-sol
session_id: 20260819-creature-combat-g0
session_role: researcher
project_lane: otclient
lane: P0-STATE
task_kind: discovery
phase: final-draft-validation
branch: research/OTC-20260819-track-a-creature-combat-static-g0
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
current_main_observed: cf90b84442dda730bdab93d8aa9f3236b7532ad8
created: 2026-08-19T09:35:00+02:00
updated: 2026-08-19T09:58:00+02:00
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
  - docs/agents/reports/OTCLIENT-20260818-track-a-s8-creature-inbound-static.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md
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
  - 558
---

# Track A creature/combat static G0

## Objective

Execute owner alias `TIBIA-RE-CREATURE-COMBAT` as one bounded current-package static research slice for primary coverage `D01-D08` and structural leads relevant to `C15-C17`, without taking over the shared physical runtime, canonical coverage files, S10 action-protocol ownership, or spawn/mechanics work.

## Authority and isolation

```yaml
runtime_access: none
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

No Synology/KasmVNC/client runtime was observed or controlled. The public official Linux package existed only inside disposable GitHub-hosted producer jobs and was deleted before compact text evidence upload.

## Producer generations

### Generation 1 — infrastructure cancellation

```text
run/job: 32228647135 / 95993567735
result: CANCELLED
failure_boundary: apt-get dependency installation exceeded job timeout
current_package_fetched: false
raw_client_retained: false
```

The retry was not blind: the producer was changed to dependency-light hosted setup using preinstalled `curl`/`strings` plus `pip pyelftools`.

### Generation 2 — bounded pipeline defect

```text
run/job: 32230003488 / 95997593305
result: FAILURE
PYELFTOOLS_IMPORT=PASS
CURRENT_PACKAGE_FENCE=PASS
QMETA_ENUMERATION=PASS
failure_boundary: sort -u | head under pipefail reported expected truncation SIGPIPE as failure
cleanup: PASS
raw_client_retained: false
```

The second repair removed the truncating pipeline shape without changing research filters or semantic classification rules.

### Generation 3 — successful producer

```text
producer_head: bb0dc3a44a6e5daca2f81817696f91043f8c03d5
run/job: 32230171183 / 95998084380
result: SUCCESS
artifact: 9356949168
artifact_digest: sha256:d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
packed_size: 10214529
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size: 52109920
current_package_fence: PASS
raw_client_retained: false
```

The downloaded artifact ZIP was independently hashed and exactly matched GitHub metadata. It contains only four text files: QMeta, fence, protocol strings and neutral semantic strings.

The temporary producer workflow was deleted after successful artifact verification and is absent from the intended final PR diff.

## Research result

The predeclared row rules were applied without widening them after reading the artifact.

```text
D01 PARTIAL -> PARTIAL
D02 PARTIAL -> PARTIAL
D03 PARTIAL -> PARTIAL
D04 PARTIAL -> PARTIAL
D05 PARTIAL -> PARTIAL
D06 NOT_STARTED -> PARTIAL
D07 NOT_STARTED -> PARTIAL
D08 PARTIAL -> PARTIAL
C15 PARTIAL -> PARTIAL
C16 PARTIAL -> PARTIAL
C17 PARTIAL -> PARTIAL
```

### D06 dedicated current-build proof

Current `TCreatureHUDQmlRenderInfo` exposes exact QMeta ownership for creature name, health, mana/mana-shield bars, horizontal/vertical icons, player states, special conditions and `statusEffectsChanged`; `TCreatureHUDOverlayController` exposes HUD refresh/update.

This closes the `NOT_STARTED` dedicated-evidence gap but not authoritative storage/schema/runtime semantics, so `D06` is only `PARTIAL`.

### D07 dedicated current-build proof

Current `TBattleListController` exposes filter state/toggling and secondary-list creation; `TBattleListGameActionHandler` exposes first/next/previous target actions plus `filterDrawCommands` and `sortDrawCommands`; current neutral types include the battle-list sort/filter proxy and secondary-list action.

This closes the `NOT_STARTED` dedicated-evidence gap but not exact filter/sort/live-membership semantics, so `D07` is only `PARTIAL`.

### Existing partial rows

Current exact-package evidence revalidates `TCreature`, `TCreatureStorage`, `TCreatureProtocolMessageHandler`, `TCreaturesGameActionHandler`, creature server-message families, target-selection structure, `sendAttack`, `sendFollow`, `GameclientMessageAttack` and `GameclientMessageFollow`.

It does not close queue -> non-QMeta handler, handler -> model mutation, authoritative live state, target/action -> protocol -> effect causality, or server acceptance. No dedicated current-build cancel-attack/follow name was recovered; absence is not negative proof and `C17` receives no new semantic promotion.

## Acceptance inventory

- [x] Fresh current public Linux package fetched in a GitHub-hosted ephemeral job and exact packed/unpacked identity fenced.
- [x] Creature/battle/combat QMeta class/method ownership enumerated without the rejected per-method jump-target heuristic.
- [x] Relevant generated protobuf/message and neutral string surfaces enumerated.
- [x] D01-D08 and C15-C17 findings classified as FACT / INFERENCE / UNKNOWN without runtime overclaim.
- [x] Negative scope control proves no credentials, login, gameplay, runtime observation, client execution, client mutation or raw-client artifact retention.
- [x] Temporary producer workflow removed before final research head.
- [x] Task-owned report and evidence paths are sufficient for a fresh coordinator without chat history.
- [ ] Exact-head repository checks on the final Draft checkpoint head.
- [ ] Coordinator independent review/promotion decision; researcher has no promotion/merge authority.

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
implementation_status: researcher_package_complete_validating
physical_e2e: NOT_APPLICABLE
physical_e2e_reason: static reverse-engineering evidence package with runtime_access none
canonical_promotion: NOT_PERFORMED
```

## Durable outputs

- `docs/agents/reports/OTCLIENT-20260819-track-a-creature-combat-static-g0.md`
- `docs/agents/evidence/OTC-20260819-track-a-creature-combat-static-g0/20260819-current-package-creature-combat.md`
- Draft PR #558

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 4
  session_id: 20260819-creature-combat-g0
  session_started_at: 2026-08-19T09:35:00+02:00
  checkpointed_at: 2026-08-19T09:58:00+02:00
  last_progress_at: 2026-08-19T09:58:00+02:00
  phase: final-draft-validation
  exact_head: checkpoint-commit-created-by-this-update
  pull_request: 558
  active_operation: exact-head-ci-observation
  external_run_ids:
    - 32230171183
  operation_started_at: 2026-08-19T09:58:00+02:00
  wait_deadline_at: null
  check_generation: final-draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: final Draft head has terminal repository checks
  next_action: Verify the complete PR diff, exact-head CI/governance, review threads and current main. If clean, write the terminal researcher-ready checkpoint and leave Draft PR #558 for coordinator independent review without merging or canonical promotion.
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T09:52:00+02:00
last_progress_at: 2026-08-19T09:58:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
```
