---
task_id: OTC-20260819-track-a-creature-combat-static-g0
status: ready
agent: null
session_id: null
session_role: researcher
project_lane: otclient
lane: P0-STATE
task_kind: discovery
phase: coordinator-handoff
branch: research/OTC-20260819-track-a-creature-combat-static-g0
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
current_main_observed: cf90b84442dda730bdab93d8aa9f3236b7532ad8
created: 2026-08-19T09:35:00+02:00
updated: 2026-08-19T10:00:00+02:00
risk: low
execution_mode: github_only
execution_reason: deterministic current-package static census and evidence processing; physical session was not required
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

Execute owner alias `TIBIA-RE-CREATURE-COMBAT` as a bounded current-package static research slice for primary coverage `D01-D08` and structural leads relevant to `C15-C17`, without taking over the shared physical runtime, canonical coverage files, S10 action-protocol ownership, or spawn/mechanics work.

## Terminal researcher result

```yaml
STATUS: DRAFT_NOT_PROMOTED
DRAFT_PR: 558
RUNTIME_ACCESS: none
PHYSICAL_E2E_REQUIRED: false
canonical_promotion: NOT_PERFORMED
merge_performed: false
```

The successful current-package producer independently fenced the public native-Linux package and retained only compact text evidence.

```text
producer_head: bb0dc3a44a6e5daca2f81817696f91043f8c03d5
run/job: 32230171183 / 95998084380
artifact: 9356949168
artifact_sha256: d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
packed_size: 10214529
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size: 52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

The downloaded artifact ZIP was independently hashed and matched GitHub metadata. It contains only `creature-combat-qmeta.txt`, `fence.txt`, `protocol-strings.txt`, and `semantic-strings.txt`.

## Findings

The predeclared status rules were applied unchanged after artifact inspection:

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

### D06

Current `TCreatureHUDQmlRenderInfo` directly exposes QMeta change surfaces for name, health, mana/mana-shield bars, horizontal/vertical icons, player states, special conditions and `statusEffectsChanged`; `TCreatureHUDOverlayController` exposes refresh/update.

This is dedicated exact-current-build evidence beyond broad lexical presence, so `D06` may be promoted by the coordinator from `NOT_STARTED` to `PARTIAL`. Authoritative provider/schema/runtime semantics remain `UNKNOWN`.

### D07

Current `TBattleListController` exposes filter state/toggling and secondary-list requests. `TBattleListGameActionHandler` exposes first/next/previous target actions, `filterDrawCommands` and `sortDrawCommands`; current neutral types include a battle-list sort/filter proxy and a secondary-list game-action type.

This is dedicated exact-current-build evidence beyond broad lexical presence, so `D07` may be promoted by the coordinator from `NOT_STARTED` to `PARTIAL`. Exact filter/sort/live-membership semantics remain `UNKNOWN`.

### Existing partial rows

Current-build evidence revalidates `TCreature`, `TCreatureStorage`, `TCreatureProtocolMessageHandler`, `TCreaturesGameActionHandler`, creature server-message families, target-selection structure, `sendAttack`, `sendFollow`, `GameclientMessageAttack` and `GameclientMessageFollow`.

It does not close queue -> non-QMeta handler, handler -> model mutation, authoritative live state, target/action -> protocol -> effect causality or server acceptance. No dedicated current-build cancel-attack/follow structural name was recovered; absence is not negative proof and `C17` receives no new semantic promotion.

## Producer repair history

```text
32228647135 / 95993567735 = CANCELLED at apt dependency install; no current package fetched
32230003488 / 95997593305 = QMeta/fence PASS, then pipefail SIGPIPE in intentional sort|head truncation; cleanup PASS
32230171183 / 95998084380 = SUCCESS after dependency-light + non-SIGPIPE repairs
```

The two failures were repaired by distinct evidence-based hypotheses; no identical failure was blindly rerun.

## Acceptance inventory

- [x] Fresh current public Linux package fetched in a GitHub-hosted ephemeral job and exact packed/unpacked identity fenced.
- [x] Creature/battle/combat QMeta ownership enumerated without the rejected per-method jump-target heuristic.
- [x] Relevant generated protobuf/message and neutral string surfaces enumerated.
- [x] D01-D08 and C15-C17 findings classified with FACT / INFERENCE / UNKNOWN boundaries.
- [x] No credentials, login, gameplay, runtime observation, client execution, client mutation or raw-client artifact retention.
- [x] Temporary producer workflow removed from the final PR diff.
- [x] Task-owned report and evidence are sufficient for a fresh coordinator without chat history.
- [x] Pre-handoff exact-head CI `32230564131` / `CI / Required` = SUCCESS on `ca41c1043116442d4c0041e39cc71d65ede96797`.
- [x] Pre-handoff Track A governance `32230563911`: deterministic admission-policy audit = SUCCESS; fresh admission behavior audit = SUCCESS.
- [x] PR diff before terminal handoff contains exactly three task-owned documentation/evidence paths.
- [x] Review threads = 0; submitted reviews = 0 before terminal handoff.
- [ ] Final exact-head checks after this terminal task-state commit; no further branch mutation is intended.
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
implementation_status: researcher_package_complete
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
  generation: 5
  session_id: null
  session_started_at: 2026-08-19T09:35:00+02:00
  checkpointed_at: 2026-08-19T10:00:00+02:00
  last_progress_at: 2026-08-19T10:00:00+02:00
  phase: coordinator-handoff
  exact_head: terminal-task-state-commit-created-by-this-update
  pull_request: 558
  active_operation: final-exact-head-checks
  external_run_ids:
    - 32230171183
    - 32230564131
    - 32230563911
  operation_started_at: 2026-08-19T10:00:00+02:00
  wait_deadline_at: null
  check_generation: terminal-researcher-draft
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: coordinator can independently review exact Draft PR #558 head and retained artifact/evidence
  next_action: Independently audit Draft PR #558 and artifact/evidence; classify ACCEPT, ACCEPT_WITH_EDITS, RETURN_FOR_EVIDENCE, or REJECT/SUPERSEDE. Only the coordinator may promote accepted row deltas into canonical coverage or integrate/merge.
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T09:52:00+02:00
last_progress_at: 2026-08-19T10:00:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: terminal-researcher-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
```
