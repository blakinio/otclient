---
task_id: OTC-20260817-track-a-p2-f50090-downstream
status: waiting
agent: ChatGPT
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-f50090-downstream
base_branch: main
base_main: 696db6ce34acd23a3d0081b9b1b94e1eabbe1cbe
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-f50090-downstream.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-f50090-downstream/**
  - .github/scripts/tibia-official-client-re-p2-f50090-downstream.py
  - .github/workflows/tibia-official-client-re-p2-f50090-downstream.yml
modules_touched: []
depends_on:
  - PR #487 merged as 696db6ce34acd23a3d0081b9b1b94e1eabbe1cbe
  - PR #481 canonical P2 chain
blocks: []
policy_version: 2
prompting_standard_version: 2.1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_mode: github-only
execution_reason: bounded exact-client static dataflow discriminator; no live runtime required
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: coordinator_approved_exact_fenced_file_only_nonsemantic_bridge
source_staging_runner: synology-otclient-01
source_staging_reason: exact retained official-client file is host-local; Synology step may only hash and copy bounded file-backed bytes, while all disassembly and semantic classification run GitHub-hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
promotion_authority: coordinator_only
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: partial_producer
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
accepted_input:
  same_message_to_f50090: FACT
  target: 0xf50090
  final_binary_egress: UNKNOWN
  final_socket_ownership: UNKNOWN
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
source_generation_1:
  producer_head: e7c13ea31f42b9c1e1c08103cd576a56cfadc554
  workflow: Track A P2 f50090 downstream evidence
  run: 32036648847
  source_job: 95408380165
  source_job_state_last_observed: queued
  code_window: 0xf50040..0xf50480
  runner_visibility_probe: FORBIDDEN_BY_INTEGRATION_403
anti_stall:
  invocation_started_at: 2026-08-17T15:40:00+02:00
  last_progress_at: 2026-08-17T15:49:00+02:00
  ci_checks_for_current_head: 0
  ci_check_generation: draft
  terminal_ci_wait_started_at: null
  terminal_ci_checks_for_current_generation: 0
  unchanged_state_checks: 2
  identical_failure_retries: 0
  repair_cycles_for_current_gate: 0
  context_reconstruction_attempts: 1
  stall_warnings: 0
blocker: external source-staging job 95408380165 remains queued on the exact-file Synology runner; GitHub integration cannot inspect self-hosted runner availability (403 Resource not accessible by integration), and anti-stall forbids a third unchanged external-state poll in this invocation
next_action: inspect run 32036648847 after its state changes; if source/hosted jobs succeed, independently review the final artifact disassembly and classify the same-message edge from 0xf50090 before deciding whether one narrower follow-up byte window is required
---

# Track A P2 — `0xf50090` downstream discriminator

## Objective

Continue only the coordinator-promoted same-message branch:

```text
... -> TGameserverDualConnection +0x78
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable 0x2f741d8 +0x10
 -> 0xf50090
```

Recover the smallest exact downstream edge from `0xf50090` while preserving the same input argument.

## Execution boundary

This worker is static-only (`runtime_access:none`). The exact retained client file is not available on GitHub-hosted runners, so the coordinator-selected staging bridge may use `synology-otclient-01` only to locate a regular exact-size/exact-SHA file and copy a bounded file-backed byte window. The source step must not execute/disassemble the client, inspect processes or process memory, read canonical runtime state, perform login/gameplay, or make semantic classifications. Disassembly and all interpretation run on GitHub-hosted Linux from the sanitized bounded artifact. No raw executable/package may be uploaded.

## Acceptance inventory

- [ ] exact client size/SHA fenced before any new bytes are consumed;
- [ ] function boundary and SysV input dataflow for `0xf50090` reconstructed from exact bytes;
- [ ] relationship of the canonical same message to `0xf50090` arguments classified FACT/DISPROVEN/UNKNOWN;
- [ ] first downstream concrete call/virtual target carrying that message resolved when exact evidence permits;
- [ ] if a direct binary-write sink is present, receiver/payload ownership proven from dataflow rather than names;
- [ ] if no sink is present, next exact transform/forward target identified without semantic guessing;
- [ ] framing/sequence/compression/encryption/final socket ownership remain UNKNOWN unless independently proven;
- [ ] no world-map evidence, live runtime, process memory, login/gameplay, OTClient/Canary/CrystalServer behavioral proof or owner-funded AI used;
- [ ] one-shot staging surfaces removed after evidence capture;
- [ ] final Draft exact-head governance/CI/review hygiene green before coordinator review.

## Current external wait

Generation 1 producer run `32036648847` is queued on the file-only source-staging runner. Two unchanged-state observations have already been consumed in this invocation. The repository anti-stall contract requires this worker to stop polling until that external state changes.

## Stop condition

Stop once the same-message path through `0xf50090` has one exact falsifiable downstream classification. Do not broaden into a generic Qt/network census.
