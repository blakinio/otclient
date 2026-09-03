---
task_id: OTC-20260903-be4f48-final-login-writer
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: red_verified
branch: research/OTC-20260903-be4f48-final-login-writer
base_branch: main
base_main: a35bbacd475a31ce52736ccbc3b5e837626def66
pr: 870
created: 2026-09-03T18:03:00+02:00
updated_at: 2026-09-03T18:16:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: no connected local device; GitHub-only contract permits isolated branch plus hosted Actions
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
worktree_state: UNAVAILABLE_CONNECTOR_ONLY_NO_REMOTE_DEVICE
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one bounded source-only writer discriminator with RED/GREEN/static-evidence/closeout phases
validation_level: focused
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-09-03T18:03:00+02:00
last_progress_at: 2026-09-03T18:16:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: draft
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
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-final-login-writer.yml
  - tools/tibia_re_be4f48_final_login_writer/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-final-login-writer.md
  - docs/agents/evidence/OTC-20260903-be4f48-final-login-writer/**
  - docs/superpowers/plans/2026-09-03-be4f48-final-login-writer.md
modules_touched: []
reuses:
  - merged PR #866 exact-current promotion
  - exact-current writer run 32998976901 / artifact 9886703883 as sanitized discovery input only
  - exact-current sendLogin adapter 0xbd3050..0xbd34dd and TProtocolMessageQueue vslot +0x68 target 0xbd24a0 under the be4f48 fence
  - historical writer source commit 3d87d729b73f868aefe1662c72af666a4921b1d8 only for bounded helper patterns, never as cross-build proof
depends_on:
  - PR #866 merged promotion
  - PR #867 archived promotion lifecycle
blocks:
  - clean coordinator promotion combining this independent lane with sender/peer lane PR #869 before any Track B decision
---

# Objective

Resolve only:

```text
sendLogin serialized queue object -> final queue/TCP writer contract
```

for exact official native Linux client `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.

Do not reopen #865, do not enter sender/peer scope from #869, and do not modify Track B PR #284.

# Safety / admission

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
official_service_e2e=false
raw_client_upload=false
track_b_pr_284_modified=false
```

The official client may exist only transiently as static bytes inside the bounded GitHub-hosted job after the repository-only contract is GREEN. It must not execute and must be removed before sanitized artifact upload.

# Live preflight

- trusted main at claim: `a35bbacd475a31ce52736ccbc3b5e837626def66`;
- #865: closed unmerged, consumed by #866;
- #284: open Draft, read-only cross-track hold;
- #869: independent sender/peer lane with non-overlapping paths;
- local worktree: unavailable because the connected Remote Desktop endpoint has no device; dedicated GitHub branch is the isolation boundary.

# Exact-current starting anchors

```text
sendLogin_qmeta_target=0xde82a2
sendLogin_external_tail=0xde82ae -> 0xbd3050
sendLogin_adapter_fde=0xbd3050..0xbd34dd
queue_vtable_address_point=0x30ed588
queue_vslot_0x68=0xbd24a0
packet_processor_vslot_0x68=0xf4eca0
final_frame_candidate=0xf4edd0..0xf4ef15
final_writer_contract=UNKNOWN
```

Artifact `9886703883` independently re-proves those anchors on `be4f48` and shows discovery evidence for the adapter-built 16-byte pair entering queue vslot `+0x68`; the new analyzer must independently reproduce the causal edge before promotion.

# TDD evidence

RED is proven on exact source head `0545bf2f6ce5aea3a037163fe29e12ebbc8a43e5`:

```text
workflow_run=33777551053
job=100722916699
Validate repository contract=failure
first_actionable_error=AssertionError: writer_path.py is missing: expected RED before client materialization
Prepare secret-free current official client metadata through WARP=skipped
Materialize exact client transiently and run bounded static discriminator=skipped
Upload sanitized static evidence only=skipped
```

This is the required RED-before-client-materialization proof. Production analyzer code may now be added.

# Bounded discriminator

1. Independently prove adapter-created 16-byte queue item and queue insertion.
2. Derive the concrete queued-object vtable from the adapter store and decode RTTI without adjacency inference.
3. Inspect only `TProtocolMessageQueue` executable vslots and directly reached bounded callers to find a unique drain of the same 16-byte item.
4. Follow only a uniquely reached queued-object/writer virtual edge toward packet/frame/TCP egress.
5. Positive writer identity requires a second independent ownership/caller/vtable cross-check.
6. At the first non-unique edge, stop as `SOURCE_BLOCKER`; no global TCP/QMeta/socket sweep.

E2E is `NOT_APPLICABLE` because this task is source-only and live official-service execution is forbidden.

# Current state

```text
trusted_main=a35bbacd475a31ce52736ccbc3b5e837626def66
source_head=0545bf2f6ce5aea3a037163fe29e12ebbc8a43e5
phase=RED_VERIFIED
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=PENDING
```

next_action: implement the minimal exact-fenced `writer_path.py`, then require the repository-only contract and `py_compile` to pass before the first exact-client static run.