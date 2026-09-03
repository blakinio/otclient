---
task_id: OTC-20260903-be4f48-final-login-writer
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: implementation
phase: red
branch: research/OTC-20260903-be4f48-final-login-writer
base_branch: main
base_main: a35bbacd475a31ce52736ccbc3b5e837626def66
created: 2026-09-03T18:03:00+02:00
updated_at: 2026-09-03T18:03:00+02:00
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
last_progress_at: 2026-09-03T18:03:00+02:00
ci_checks_for_current_head: 0
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
  - promoted exact-current source blocker evidence from merged PR #866
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

Resolve only the exact-current `15.32.be4f48` boundary:

```text
sendLogin serialized queue object -> final queue/TCP writer contract
```

Do not reopen source PR #865, do not work on sender/peer ownership from PR #869, and do not modify Track B PR #284.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

The trusted-base fence contract `docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json` agrees at claim time. The hosted workflow must additionally re-read the public current package before client materialization and fail closed if it moved.

# Admission / safety

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

The official client may be materialized only transiently as bytes for static ELF/disassembly analysis inside a GitHub-hosted disposable job after the RED repository contract is GREEN. It must never execute, and raw client bytes must be deleted before sanitized artifact upload.

# Live ownership / dependency preflight

Trusted `main` at claim is `a35bbacd475a31ce52736ccbc3b5e837626def66`. Source PR #865 is closed unmerged and consumed by merged promotion #866. Track B PR #284 is open Draft and read-only for this lane. Open PR #869 owns only the independent sender/peer discriminator paths; its changed-file set does not overlap the writer paths declared here. No existing branch or open PR claims `OTC-BE4F48-FINAL-LOGIN-WRITER`.

A local worktree is unavailable because the connected Remote Desktop endpoint reports no device. The dedicated GitHub branch is the isolation boundary under `docs/agents/GITHUB_ONLY_EXECUTION.md`.

# Promoted / revalidated starting facts

```text
sendLogin_qmeta_target=0xde82a2
sendLogin_external_tail=0xde82ae -> 0xbd3050
sendLogin_adapter_fde=0xbd3050..0xbd34dd
queue_vtable_address_point=0x30ed588
queue_vslot_0x68=0xbd24a0
final_frame_candidate=0xf4edd0..0xf4ef15
packet_processor_vslot_0x68=0xf4eca0
final_writer_contract=UNKNOWN
```

The current artifact `9886703883` independently re-proves these addresses against the `be4f48` SHA. It also shows the adapter constructs a 16-byte pair on stack and calls queue vslot `+0x68`; the queue vslot copies the same 16-byte pair into its internal queue. This is discovery evidence to be independently reproduced by the bounded discriminator before promotion.

# TDD / bounded discriminator

1. RED: repository-only contract must fail because the analyzer is absent; failure must occur before any network/package/client step.
2. GREEN-1: add the smallest exact-fenced analyzer that proves adapter-created queue-item identity, queue insertion, queue-drain ownership, and only the next uniquely bound writer transition.
3. Run once against the exact public client on GitHub-hosted Linux.
4. If sanitized evidence gives one mechanically testable continuation toward the packet/frame writer, allow one narrow evidence-derived correction or discriminator. Otherwise stop as `SOURCE_BLOCKER` at the first missing object/ownership edge.
5. No whole-binary TCP/QMeta sweep, generic socket xref ranking, proximity/adjacency inference, runtime observation, OCR/Vision, sender/peer work, Field6 guessing, or Track B mutation.

# Acceptance

A positive source result requires exact current fence plus a unique causal object/buffer chain from the adapter-built queue item through the concrete queue writer to final TCP/socket egress or an equivalent unique final wire-writer contract, with a second independent ownership/caller/vtable cross-check. If any required ownership/dataflow edge is not unique, the scientific terminal result is `SOURCE_BLOCKER`.

E2E is `NOT_APPLICABLE` because this is explicitly static/source-only; a live official-service run is forbidden for this task.

# Current state

```text
trusted_main=a35bbacd475a31ce52736ccbc3b5e837626def66
phase=RED_SETUP
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=PENDING
```

next_action: add the repository-only failing contract, minimal hosted workflow, and early Draft PR; verify RED fails before any current-client package request.