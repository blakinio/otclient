---
task_id: OTC-20260826-current-game-login-wire-writer
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260826-current-game-login-wire-writer
related_pr: 699
base_branch: main
base_main: 8085b40698d409bbacba3460001e8ddca4f6c84f
current_main_observed: 77a4f63f0caa099635489ad0e5a6efc3042dc12f
created: 2026-08-26T17:12:00+02:00
updated: 2026-08-26T20:36:00+02:00
risk: high
execution_mode: github_actions_hosted
execution_reason: current-build static protocol reconstruction is deterministic/disposable P2 work
execution_class: github_hosted
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
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
promotion_authority: coordinator_only
researcher_delivery: draft_pr_only
policy_version: 2
session_id: chatgpt-20260826-current-login-wire-writer
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one sequential current-build queue-to-TCP writer proof
validation_level: focused
invocation_started_at: 2026-08-26T17:11:00+02:00
last_progress_at: 2026-08-26T20:36:00+02:00
heavy_validation_runs: 4
repair_cycles_for_current_gate: 1
identical_failure_retries: 0
context_reconstruction_attempts: 0
stall_warnings: 0
ci_checks_for_current_head: 2
unchanged_state_checks: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml
  - tools/tibia_re_current_game_login_wire_writer/**
  - docs/agents/evidence/OTC-20260826-current-game-login-wire-writer/**
  - docs/agents/tasks/active/OTC-20260826-current-game-login-wire-writer.md
modules_touched:
  - official-client-re
  - protocol-research
reuses:
  - docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/**
  - docs/agents/evidence/OTC-20260813-tibia-global-login-lab/20260826-current-build-encrypted-handoff-game-0x14.md
depends_on:
  - PR #589 historical native game-login structural promotion on trusted main
  - PR #284 Track B current-build structured 0x14 checkpoint as consumer requirement only
blocks:
  - PR #284 next game-login protocol mutation/retry until coordinator promotion reaches trusted main
cross_repo_tasks: []
implementation_authorized: true
---

# Current-build game-login queue/TCP writer proof

Alias family: `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-WIRE-WRITER`.

## Objective

Recover current-build outbound game-login queue/writer semantics sufficiently to stop protocol guessing after Track B's structured `0x14`, while keeping unsupported semantics explicitly `UNKNOWN`.

## Acceptance inventory

- [x] Current public Linux package independently revalidated through a disposable secret-free hosted producer.
- [x] Current `TProtocolMessageQueue::sendLogin` QMeta case and adapter recovered without reusing historical addresses.
- [x] Current queue vtable `+0x68` target recovered and first remaining asynchronous boundary recorded.
- [x] Current outbound padding, XTEA mode-2 transform, sequence and final block framing recovered.
- [x] Current `QDataStream::writeRawData` / Qt-bound writer construction graph recovered.
- [x] Structural Track B comparison completed without modifying Track B or running login.
- [x] Only sanitized evidence persisted; proprietary raw client and secrets were not uploaded or retained.
- [x] Exact research head `3d87d729b73f868aefe1662c72af666a4921b1d8` passed task producer, repository CI and Track A governance before the docs-only freeze.
- [ ] Fresh coordinator/independent audit and promotion to trusted `main`.

## Exact current client

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

## Final proving generation

```text
research head  3d87d729b73f868aefe1662c72af666a4921b1d8
producer run   32998976901 = SUCCESS
artifact       9617908322
digest         sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
CI             32998977749 = SUCCESS
Track A gov.   32998976855 = SUCCESS
```

Durable evidence:

- `docs/agents/evidence/OTC-20260826-current-game-login-wire-writer/20260826-current-game-login-wire-writer.md`
- `docs/agents/evidence/OTC-20260826-current-game-login-wire-writer/result.json`

## Research classification

```yaml
current_exact_client_fence: PROVEN
current_sendlogin_qmeta_case: PROVEN
current_sendlogin_adapter: PROVEN
current_queue_vslot_plus_0x68_target: PROVEN
current_padding: PROVEN
current_xtea_mode2_transform: PROVEN
current_sequence: PROVEN
current_framing: PROVEN
current_qdatastream_raw_write: PROVEN
current_qt_bound_binary_writer: PROVEN
final_os_socket_syscall: UNKNOWN_OPTIONAL
queue_async_drain_to_client_processor: UNKNOWN
current_generated_login_message_field_schema: UNKNOWN
track_b_outer_transport_shape: STRUCTURALLY_ALIGNED
track_b_next_guess_should_change_outer_framing: REJECTED
```

The current outer transport proof aligns with Track B's existing generic `Protocol::send()` / `OutputMessage` framing. The research therefore rejects another framing/sequence/XTEA feature-toggle guess as the next Track B action. The unresolved login-specific payload representation sits before that generic transport layer.

## Safety / E2E

```yaml
runtime_access: none
official_client_executed: false
login_performed: false
credential_or_session_access: false
raw_client_uploaded: false
raw_client_retained: false
physical_e2e:
  result: NOT_APPLICABLE
  reason: exact-file static protocol reconstruction only
```

## Context checkpoint

```yaml
checkpoint_version: 1
status: ready
phase: validate
branch: research/OTC-20260826-current-game-login-wire-writer
draft_pr: 699
final_research_head: 3d87d729b73f868aefe1662c72af666a4921b1d8
current_main_observed: 77a4f63f0caa099635489ad0e5a6efc3042dc12f
first_unproven_boundary:
  - asynchronous drain from TProtocolMessageQueue +0x68 @ 0xbd24a0 into the recovered client/raw/network processor path
  - exact current generated login-message field schema
rejected_hypotheses:
  - reuse historical df7b29/bf29ac addresses as current proof
  - change generic outer framing after structured 0x14 without current evidence
  - retry Track B login before current evidence promotion
blocker: coordinator promotion required before Track B consumes this as trusted-main evidence
next_action: Coordinator independently audit source PR #699, persist only accepted sanitized evidence on current trusted main, close the researcher PR unmerged, then allow Track B #284 to consume the promoted result.
```
