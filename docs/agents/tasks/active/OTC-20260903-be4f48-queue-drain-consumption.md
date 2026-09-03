---
task_id: OTC-20260903-be4f48-queue-drain-consumption
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: claimed
branch: research/OTC-20260903-be4f48-queue-drain-consumption
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
pr: none
created: 2026-09-03T19:02:00+02:00
updated_at: 2026-09-03T19:02:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: Work-mode handoff was declined; repository GitHub-only governance permits an isolated branch plus hosted Actions
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
worktree_state: UNAVAILABLE_GITHUB_ONLY
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one bounded source-only queue-consumption discriminator with RED/GREEN/static-evidence/closeout phases
validation_level: focused
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-09-03T19:02:00+02:00
last_progress_at: 2026-09-03T19:02:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: none
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-drain-consumption.yml
  - tools/tibia_re_be4f48_queue_drain_consumption/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md
  - docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/**
  - docs/superpowers/plans/2026-09-03-be4f48-queue-drain-consumption.md
modules_touched: []
reuses:
  - merged coordinator promotion PR #871 / merge 18700fcf98478c83e19187a9eb169d087f592ba3
  - merged alias registration PR #873 / merge 446eb643d6ef24dc996a410df812393e19800973
  - sanitized source blocker facts from PR #870 only as bounded discovery input, never by reopening its analyzer family
depends_on:
  - PR #871 merged promotion
  - PR #873 merged alias registration
blocks:
  - later clean coordinator promotion of this source result before any Track B decision
---

# Objective

Resolve only the exact-current static boundary:

```text
proved 16-byte queued GameclientMessage identity
-> owned TProtocolMessageQueue callback 0xbd2190
-> causal consumption of that exact queued object
-> at most the next uniquely bound writer edge while identity remains intact
```

Exact official native Linux client fence:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Safety / admission

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
ocr_vision=false
official_service_e2e=false
raw_client_upload=false
track_b_pr_284_modified=false
```

The exact client may exist only transiently as static bytes inside the bounded GitHub-hosted analyzer job after the repository-only contract is GREEN. It must never execute and must be deleted before sanitized artifact upload.

# Live preflight

- trusted `main` at claim: `446eb643d6ef24dc996a410df812393e19800973`;
- exact-current fence matches `docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json`;
- coordinator promotion #871 fixes the first missing boundary at owned queue callback `0xbd2190` -> causal consumption of the exact queued `GameclientMessage`;
- source PR #870 is closed unmerged and consumed; its analyzer/workflow family will not be reopened;
- no open PR or branch was found owning this alias at claim;
- Track B PR #284 is outside owned paths and must remain unchanged;
- sibling alias `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER` is intentionally parallel and owns a disjoint source boundary.

# Promoted exact-current anchors

```text
sendLogin_adapter_target=0xbd3050
serialized_queue_object_identity=16-byte pair {object=allocation+0x10, owner=allocation}
queue_insert_vslot_target=0xbd24a0
queue_vtable_address_point=0x30ed588
owned_drain_candidate_count=1
owned_drain_candidate=0xbd2190
owned_drain_fde=0xbd2190..0xbd2495
queued_gameclientmessage_causal_consumption=NOT_PROVEN
final_queue_writer=UNKNOWN
final_tcp_writer=UNKNOWN
final_writer_contract=UNKNOWN
```

These are bounded starting anchors. The new analyzer must independently re-derive the exact 16-byte pair and queue insertion before using `0xbd2190` as its consumer seed.

# Acceptance inventory

1. Repository-only TDD RED occurs before any current-client metadata or byte materialization.
2. Exact version/size/SHA mismatch fails closed.
3. Analyzer independently re-proves the adapter-built 16-byte object/owner pair and unchanged queue insertion.
4. Analysis is restricted to `0xbd2190`, proven queue members/storage and only a uniquely identity-preserving next writer edge.
5. `QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION=true` requires explicit exact object/owner identity propagation (or a unique identity-preserving derivative) into a semantic consumer.
6. `FINAL_QUEUE_WRITER_IDENTIFIED=true` additionally requires exactly one next writer edge plus a second independent vtable/ownership/caller cross-check.
7. Any identity fork, nonunique callback target or indistinguishable writer edge terminates as `SOURCE_BLOCKER` without a global socket/QMeta/TCP scan.
8. Sanitized deterministic JSON only; no proprietary bytes, secrets, packet captures or runtime artifacts persist.
9. Track B PR #284 remains untouched and official-service E2E count remains zero.
10. Final exact-head focused workflow, repository CI/governance checks and independent falsification are recorded before terminal disposition.

E2E: `NOT_APPLICABLE` because this exact task is source-only and official-client execution/service E2E is forbidden by its prompt.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-03T19:02:00+02:00
head: UNKNOWN_AFTER_TASK_CLAIM_COMMIT
branch: research/OTC-20260903-be4f48-queue-drain-consumption
pr: none
status: investigating
context_routes:
  - docs/agents/prompts/OTC_BE4F48_QUEUE_DRAIN_CONSUMPTION.md
  - docs/agents/evidence/OTC-20260903-be4f48-post869-870-promotion/result.json
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-drain-consumption.yml
  - tools/tibia_re_be4f48_queue_drain_consumption/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md
  - docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/**
  - docs/superpowers/plans/2026-09-03-be4f48-queue-drain-consumption.md
proven:
  - main exact fence is 15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
  - coordinator promotion #871 records exact queue item pair, insertion 0xbd24a0 and unique owned drain candidate 0xbd2190
  - no open PR or matching queue-drain branch owned this alias at claim
  - runtime_access is none and Track B #284 is outside scope
derived:
  - the smallest admissible experiment is an exact-fenced hosted static analyzer focused on 0xbd2190 after independently re-proving queue identity
unknown:
  - whether 0xbd2190 causally consumes the exact queued GameclientMessage identity
  - next unique writer edge
  - final queue writer
  - final TCP writer
  - final writer contract
conflicts:
  - none
first_failure:
  marker: repository-only RED not yet executed
  evidence: none
rejected_hypotheses:
  - broad global socket/QMeta/TCP discovery: forbidden by task prompt and unnecessary to test the first missing boundary
changed_paths:
  - docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md
validation:
  - command: live alias/PR/branch/fence preflight
    result: PASS
    evidence: main 446eb643d6ef24dc996a410df812393e19800973; no open BE4F48 PR; no be4f48-queue branch; fence manifest matches prompt
  - command: official-service E2E
    result: NOT_APPLICABLE
    evidence: source-only prompt forbids official-client execution and official-service E2E
blockers:
  - none
next_action: open the Draft PR, persist the implementation plan, then add only the repository-only failing contract/workflow and verify RED before production analyzer code
```
