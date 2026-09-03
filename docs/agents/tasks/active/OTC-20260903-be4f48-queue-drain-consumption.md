---
task_id: OTC-20260903-be4f48-queue-drain-consumption
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: red_verified
branch: research/OTC-20260903-be4f48-queue-drain-consumption
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
pr: 874
created: 2026-09-03T19:02:00+02:00
updated_at: 2026-09-03T19:14:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: Work-mode handoff was declined; repository GitHub-only governance permits an isolated branch plus hosted Actions
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
worktree_state: UNAVAILABLE_GITHUB_ONLY
policy_version: 2
context_pressure: medium
decomposition_decision: phased
validation_level: focused
heavy_validation_runs: 0
invocation_started_at: 2026-09-03T19:02:00+02:00
last_progress_at: 2026-09-03T19:14:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: red
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
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
  - sanitized exact-current facts from consumed source PR #870 only as bounded discovery input, never by reopening its analyzer family
depends_on:
  - PR #871 merged promotion
  - PR #873 merged alias registration
blocks:
  - later clean coordinator promotion of this source result before any Track B decision
---

# Objective

Resolve only:

```text
proved exact queued GameclientMessage 16-byte identity
-> owned TProtocolMessageQueue callback 0xbd2190
-> causal consumption of that exact queued object
-> at most the next uniquely bound writer edge while identity remains intact
```

Exact client fence:

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

The exact client may exist only transiently as static bytes inside the bounded GitHub-hosted analyzer job after repository-only GREEN. It must never execute and must be deleted before sanitized artifact upload.

# Promoted starting anchors

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

The new analyzer must independently re-prove the exact pair and queue insertion before using `0xbd2190` as the consumer seed.

# Acceptance inventory

1. Repository-only TDD RED occurs before current-client metadata or byte materialization.
2. Exact version/size/SHA mismatch fails closed.
3. Analyzer independently re-proves the adapter-built 16-byte object/owner pair and unchanged queue insertion.
4. New analysis is restricted to `0xbd2190`, proven queue storage, and at most one uniquely identity-preserving next writer edge.
5. Causal consumption requires explicit exact object/owner identity propagation into a semantic consumer.
6. Positive final queue-writer identity additionally requires exactly one next writer edge plus an independent ownership/vtable/caller cross-check.
7. Any identity fork or nonunique writer edge stops without a global socket/QMeta/TCP scan.
8. Only sanitized deterministic JSON may persist.
9. Track B PR #284 remains untouched and official-service E2E count remains zero.
10. Final exact-head focused workflow, repository CI/governance checks and a fresh falsification pass are required before terminal disposition.

E2E: `NOT_APPLICABLE` because this source-only task forbids official-client execution and official-service E2E.

# TDD evidence

Repository-only RED is proven on source head `2136730313912c7e025f0bc063cf42f18aa836c9`:

```text
workflow_run=33783273236
job=100741848377
Validate repository contract=failure
first_actionable_error=AssertionError: drain_consumption.py is missing: expected RED before client materialization
Prepare secret-free current official client metadata through WARP=skipped
Materialize exact client transiently and run bounded static discriminator=skipped
Emit sanitized source result=skipped
Upload sanitized static evidence only=skipped
```

This is the required RED-before-client-materialization proof. Production analyzer code may now be added.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-03T19:14:00+02:00
head: 2136730313912c7e025f0bc063cf42f18aa836c9
branch: research/OTC-20260903-be4f48-queue-drain-consumption
pr: 874
status: implementing
context_routes:
  - docs/agents/prompts/OTC_BE4F48_QUEUE_DRAIN_CONSUMPTION.md
  - docs/agents/evidence/OTC-20260903-be4f48-post869-870-promotion/result.json
  - docs/superpowers/plans/2026-09-03-be4f48-queue-drain-consumption.md
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-drain-consumption.yml
  - tools/tibia_re_be4f48_queue_drain_consumption/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md
  - docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/**
  - docs/superpowers/plans/2026-09-03-be4f48-queue-drain-consumption.md
proven:
  - main exact fence is 15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
  - coordinator promotion #871 records the exact queue item pair, insertion 0xbd24a0 and unique owned drain candidate 0xbd2190
  - Draft PR #874 owns this alias on an isolated branch
  - repository-only TDD RED run 33783273236 job 100741848377 failed exactly because drain_consumption.py was absent
  - all client metadata/materialization/artifact steps were skipped on the RED run
  - Track A runtime-governance run 33783279031 and self-hosted PR-boundary run 33783279088 passed on the RED head
  - runtime_access is none and Track B #284 is outside scope
derived:
  - production implementation may now begin under TDD and exact-current fencing
unknown:
  - whether 0xbd2190 causally consumes the exact queued GameclientMessage identity
  - next unique writer edge
  - final queue writer
  - final TCP writer
  - final writer contract
conflicts:
  - none
first_failure:
  marker: expected repository-only TDD RED
  evidence: workflow 33783273236 / job 100741848377 / exact missing-analyzer AssertionError
rejected_hypotheses:
  - broad global socket/QMeta/TCP discovery: forbidden by task prompt and unnecessary to test the first missing boundary
changed_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-drain-consumption.yml
  - tools/tibia_re_be4f48_queue_drain_consumption/test_contract.py
  - docs/agents/tasks/active/OTC-20260903-be4f48-queue-drain-consumption.md
  - docs/superpowers/plans/2026-09-03-be4f48-queue-drain-consumption.md
validation:
  - command: repository-only TDD RED / workflow 33783273236 job 100741848377
    result: PASS
    evidence: expected missing-analyzer failure occurred before WARP/client steps; those steps were skipped
  - command: Track A agent runtime governance / 33783279031
    result: PASS
    evidence: exact RED head 2136730313912c7e025f0bc063cf42f18aa836c9
  - command: Track A self-hosted PR boundary / 33783279088
    result: PASS
    evidence: exact RED head 2136730313912c7e025f0bc063cf42f18aa836c9
  - command: official-service E2E
    result: NOT_APPLICABLE
    evidence: source-only prompt forbids official-client execution and official-service E2E
blockers:
  - none
next_action: implement the minimal exact-fenced drain_consumption.py that independently re-proves the 16-byte queue identity/insertion and tests only callback 0xbd2190 for causal identity-preserving consumption
```
