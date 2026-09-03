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
updated_at: 2026-09-03T19:22:00+02:00
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
heavy_validation_runs: 0
invocation_started_at: 2026-09-03T19:02:00+02:00
last_progress_at: 2026-09-03T19:22:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: implementation
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

Exact current official Linux client fence:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Safety

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

The client may exist only transiently as static bytes inside the bounded GitHub-hosted analyzer job after repository-only GREEN. It is never executed and must be removed before sanitized artifact upload.

# Promoted starting anchors

```text
sendLogin_adapter_target=0xbd3050
serialized_queue_object_identity=16-byte pair {object=allocation+0x10, owner=allocation}
queue_insert_vslot_target=0xbd24a0
queue_vtable_address_point=0x30ed588
owned_drain_candidate=0xbd2190
owned_drain_fde=0xbd2190..0xbd2495
queued_gameclientmessage_causal_consumption=NOT_PROVEN
final_queue_writer=UNKNOWN
final_tcp_writer=UNKNOWN
final_writer_contract=UNKNOWN
```

The new analyzer independently re-proves the exact pair and insertion before using `0xbd2190` as the only consumer seed. It may follow at most one identity-preserving next edge and must stop instead of performing global Qt/socket/TCP discovery.

# TDD evidence

Repository-only RED is proven on exact source head `2136730313912c7e025f0bc063cf42f18aa836c9`:

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

Production analyzer implementation was added only after this RED.

# Current implementation

`tools/tibia_re_be4f48_queue_drain_consumption/drain_consumption.py` now:

1. fails closed on exact version/size/SHA;
2. re-proves adapter allocation/object/owner pair, `GameclientMessage` RTTI, queue RTTI and vslot `+0x68 -> 0xbd24a0`;
3. re-proves the 16-byte insertion and end advance by `0x10`;
4. inspects only FDE `0xbd2190..0xbd2495` for the queue-begin 16-byte copy, owner refcount lifetime, one-element begin advance and exact semantic dispatch;
5. withholds any next writer identity unless a unique identity-preserving edge and independent ownership cross-check are available.

A governance run on implementation head `4471ccf1e396794ae0d2ce3de97d0474284e6fee` exposed a task-record defect, not an analyzer defect: admission fields required even for `runtime_access:none` had been accidentally omitted during checkpoint compaction. Run `33783950469`, job `100744081081` reported exactly:

```text
missing admission fields ['canonical_lease_generation', 'registration_lease_generation', 'gate_a', 'generation_rebind', 'gate_b', 'bootstrap', 'target_uniqueness']
```

This commit restores all seven as `NOT_APPLICABLE`; no runtime authority or canonical namespace is claimed.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-03T19:22:00+02:00
head: 4471ccf1e396794ae0d2ce3de97d0474284e6fee
branch: research/OTC-20260903-be4f48-queue-drain-consumption
pr: 874
status: implementing
proven:
  - exact fence and promoted queue/drain anchors are fixed by main at claim
  - Draft PR #874 owns this alias on an isolated branch
  - repository-only TDD RED run 33783273236 job 100741848377 occurred before any package/client access
  - production analyzer was added after RED
  - repository-only contract passed on implementation workflow run 33783945122 before WARP metadata preparation began
  - Track A self-hosted PR boundary run 33783950324 passed on implementation head
  - deterministic governance failure on 33783950469 was solely missing source-only admission keys and is repaired here
unknown:
  - final exact-current analyzer result
  - next unique receiver/writer edge after bounded queue callback
  - final queue writer
  - final TCP writer
  - final writer contract
first_failure:
  marker: deterministic governance task-record schema failure on implementation head
  evidence: run 33783950469 / job 100744081081 / seven missing admission fields
rejected_hypotheses:
  - global Qt/socket/TCP writer discovery: forbidden by source prompt
  - treating governance failure as analyzer evidence: rejected because the failing job never evaluated exact-client source semantics
validation:
  - command: repository-only TDD RED / run 33783273236 job 100741848377
    result: PASS
    evidence: expected missing-analyzer failure; client steps skipped
  - command: implementation repository contract / run 33783945122
    result: PASS
    evidence: Validate repository contract completed successfully before WARP step
  - command: Track A self-hosted PR boundary / run 33783950324
    result: PASS
    evidence: exact implementation head
  - command: official-service E2E
    result: NOT_APPLICABLE
    evidence: source prompt forbids official-client execution/service E2E
blockers:
  - none
next_action: require the repaired exact head to pass governance and the bounded exact-current static workflow, then inspect only the sanitized result artifact
```
