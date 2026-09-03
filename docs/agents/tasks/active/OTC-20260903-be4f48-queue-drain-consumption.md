---
task_id: OTC-20260903-be4f48-queue-drain-consumption
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: source_terminal
branch: research/OTC-20260903-be4f48-queue-drain-consumption
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
pr: 874
created: 2026-09-03T19:02:00+02:00
updated_at: 2026-09-03T19:25:00+02:00
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
decomposition_decision: phased
validation_level: focused
heavy_validation_runs: 1
invocation_started_at: 2026-09-03T19:02:00+02:00
last_progress_at: 2026-09-03T19:25:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: source_terminal_checkpoint
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
  - clean coordinator promotion of this source result before any Track B decision
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

# Source terminal result

```text
EXACT_CLIENT_FENCE_PROVEN=true
SERIALIZED_QUEUE_OBJECT_IDENTITY_PROVEN=true
OWNED_DRAIN_CALLBACK=0xbd2190
QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION=true
NEXT_UNIQUE_WRITER_EDGE=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_PR_284_MODIFIED=false
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TERMINAL_RESULT=QUEUE_DRAIN_CONSUMPTION_PROVEN
FIRST_MISSING_BOUNDARY=TProtocolMessageQueue signal 0xbf carrying the exact queued GameclientMessage shared_ptr -> unique connected receiver/writer edge
NEXT_ACTION=clean coordinator promotion from fresh trusted main; do not broaden source PR #874 into global Qt/writer discovery
```

## Evidence

Repository-only TDD RED:

```text
head=2136730313912c7e025f0bc063cf42f18aa836c9
workflow_run=33783273236
job=100741848377
error=AssertionError: drain_consumption.py is missing: expected RED before client materialization
client metadata step=skipped
client materialization step=skipped
artifact upload step=skipped
```

Exact-current source proof:

```text
source_head=4471ccf1e396794ae0d2ce3de97d0474284e6fee
workflow_run=33783945122
job=100744062650
artifact_id=9904688934
artifact_digest=sha256:7d707d2820a891c6d91f974b305d657227587c65aeac2d7ba8557dd04cab4778
result_json_sha256=47ac0c9f8dc79d024a8eaa484474bd8e33bf9cf2407458c2a2bc8256211ddb70
PUBLIC_CURRENT_EXACT_FENCE=PASS
CURRENT_CLIENT_EXACT_FENCE=PASS
BE4F48_QUEUE_DRAIN_CONSUMPTION_CONTRACT=PASS
BE4F48_QUEUE_DRAIN_CONSUMPTION_ANALYSIS=PASS
RAW_CLIENT_RETAINED=false
```

Durable sanitized evidence:

- `docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/result.json`
- `docs/agents/evidence/OTC-20260903-be4f48-queue-drain-consumption/20260903-source-result.md`

## Causal proof summary

The new analyzer independently re-proved the producer identity and queue insertion, then restricted new analysis to the owned callback FDE:

1. adapter builds `{object=allocation+0x10, owner=allocation}` and queue vslot `+0x68` resolves to `0xbd24a0`;
2. insertion copies all 16 bytes into queue storage and advances queue end by `0x10`;
3. callback `0xbd2190` loads queue begin `this+0x70`, copies exactly one 16-byte element to `rsp+0x10`, and separately refcounts the copied owner;
4. it retires the original queue entry and advances queue begin by exactly `0x10`;
5. it passes `rsp+0x10` as Qt `argv[1]` to direct call `0xbd22c2 -> 0x4d7dc0`, promoted as `QMetaObject::activate`, with `TProtocolMessageQueue this`, metaobject `0x30b73e0` and signal index `0xbf`;
6. it reloads the copied owner after dispatch, so the owner lifetime independently spans the semantic consumer call.

This proves causal queue consumption of the exact shared-pointer identity. The next receiver/writer remains deliberately withheld because `QMetaObject::activate` does not statically bind a unique connected receiver in this FDE and this task forbids a broad Qt/socket/TCP search.

## Safety

```text
runtime_access=none
official_client_execution=false
login_performed=false
credential_access=false
process_memory_access=false
packet_capture=false
ocr_vision_used=false
official_service_e2e_count=0
raw_client_uploaded=false
track_b_pr_284_modified=false
field6_value=UNKNOWN
```

A single non-semantic repair restored mandatory source-only Track A admission keys after governance run `33783950469`/job `100744081081` detected their accidental omission. The repaired admission check passed on run `33784080581`; analyzer semantics did not change.

E2E: `NOT_APPLICABLE` because this source-only alias forbids official-client execution and official-service E2E.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-03T19:25:00+02:00
head_before_terminal_checkpoint: c0fa61b5e02eb8827cab684a2cb181b34ec878ee
branch: research/OTC-20260903-be4f48-queue-drain-consumption
pr: 874
status: ready
proven:
  - exact public current client fence is unchanged and passed both metadata and transient-static-byte verification
  - exact 16-byte GameclientMessage object/owner pair and queue insertion are independently re-proved
  - owned callback 0xbd2190 causally consumes the exact queued pair and emits it through QMetaObject::activate signal 0xbf
  - no unique next receiver/writer edge is proved and no final queue/TCP writer is claimed
  - runtime access and official-service E2E remain zero; raw client bytes were removed before artifact upload
  - Track B PR #284 was not modified by this source task
unknown:
  - unique connected receiver/writer edge after signal 0xbf
  - final queue writer
  - final TCP writer
  - final writer contract
conflicts:
  - none
first_failure:
  marker: expected repository-only TDD RED
  evidence: run 33783273236 / job 100741848377
repair_history:
  - run 33783950469 exposed seven omitted source-only admission keys; restored as NOT_APPLICABLE; run 33784080581 passed
validation:
  - command: exact-current source workflow / 33783945122
    result: PASS
    evidence: contract, public fence, transient exact fence, analyzer, sanitized artifact and raw-client cleanup all passed
  - command: Track A runtime governance / 33784080581
    result: PASS
    evidence: repaired source-only admission fields accepted
  - command: Track A self-hosted PR boundary / 33784080524
    result: PASS
    evidence: repaired head accepted
  - command: official-service E2E
    result: NOT_APPLICABLE
    evidence: source-only task forbids official-client execution/service E2E
blockers:
  - source PR lifecycle intentionally awaits independent clean coordinator promotion
next_action: validate this terminal checkpoint exact head through focused workflow plus CI/governance/boundary checks, update Draft PR #874 with exact final IDs, then hand off sanitized facts to a clean coordinator promotion from fresh trusted main
```
