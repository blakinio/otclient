---
task_id: OTC-20260817-track-a-p2-dual-precondition-egress
status: waiting
agent: ChatGPT
session_id: chatgpt-p2-egress-20260817-1141
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260817-track-a-p2-dual-precondition-egress
worktree: github-only-ref:research/OTC-20260817-track-a-p2-dual-precondition-egress
base_branch: main
base_main: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
risk: medium
created: 2026-08-17T11:41:00+02:00
updated: 2026-08-17T11:46:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-precondition-egress.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/**
  - .github/scripts/tibia-official-client-re-p2-dual-precondition-egress.py
  - .github/workflows/tibia-official-client-re-p2-dual-precondition-egress.yml
modules_touched: []
depends_on:
  - PR #450 merged as cbc6388e8607bb92120281a9a15148577994d3a6
  - docs/agents/evidence/OTC-20260816-track-a-promotion-coordination/20260817-p2-network-barrier-update.md
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md
  - PR #310 artifact 9252025461 as discovery input only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded exact-client file-byte staging plus GitHub-hosted disassembly/semantic validation; no live client/runtime access
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded discriminator around the already-known TGameserverDualConnection precondition/write path
validation_level: focused
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
source_staging_class: synology_file_only_exact_fenced_nonsemantic
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
track_a_runtime_agent_admission_version: 1
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
research_output: DRAFT_NOT_PROMOTED
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
invocation_started_at: 2026-08-17T11:36:00+02:00
last_progress_at: 2026-08-17T11:45:40+02:00
ci_checks_for_current_head: 2
ci_check_generation: draft_experiment
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
additional_task_allowance_consumed: false
---

# Track A P2 — DualConnection precondition / egress discriminator

## Objective

Resolve the first still-UNKNOWN transport boundary immediately downstream of the promoted P2 chain by recovering exact-client dataflow around `TGameserverDualConnection` precondition `+0x90 @ 0xb40370`, especially the `QIODevice::write(QByteArray const&)` call observed at `0xb4066b` in accepted non-quarantined artifact `9252025461`.

Bounded question: is that write causally tied to the same post-`TGameserverNetworkPacketRawDataProcessor` gameplay message, and which concrete QIODevice/object owns the destination? Framing, sequence, compression, encryption and final socket ownership must remain `UNKNOWN` unless direct exact-byte dataflow proves them.

## Current canonical boundary consumed

PR #450 promoted exactly:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

`protocol_stage_order = PROVEN_PARTIAL`.

Still canonical `UNKNOWN`: framing, sequence, compression, encryption, final binary egress, final socket ownership and complete transport ordering beyond the recovered processor chain.

## Admission / ownership / uniqueness / drift

- Initial dispatch base: `main@60ab740872d52f3f7c4802d49fd5275a9968d085`.
- Fresh main drift was detected while Draft #458 was opened: `main` advanced by exactly one disjoint RUNTIME/XRes merge to `16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc`.
- `60ab740..16c6fb` changed only `docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/**` and `docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md`; no P2 owned/evidence path overlapped.
- Branch was restacked without force-push through merge commit `bc562567f6d0a502323d5f2911db3f94fec82b52`, preserving the task commit and current main tree.
- No other open `P2-NETWORK` PR or active task owns this responsibility or these paths.
- Old P2 source PRs #301/#308/#310/#368/#449 are closed; #450 is the accepted dependency.
- Draft PR: #458. Researcher output is Draft-only; coordinator alone may promote/merge semantic conclusions.

## Runtime admission

```yaml
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
```

No client process, process memory, canonical state, X11/VNC, login/session, gameplay, packet replay or client-byte mutation is authorized.

The one permitted non-hosted operation follows accepted #449 precedent: verify the retained regular file against exact size/SHA and copy only bounded file-byte windows as small UTF-8 hex/metadata. Source staging performs no disassembly or semantic classification and uploads no raw executable/package. All disassembly/semantic review is GitHub-hosted.

## Experiment generation 1

Draft exact workflow head: `37c455f2ab3170457a0d084a7745eaa42e28aff1`.

Owned one-shot tooling:

- `.github/scripts/tibia-official-client-re-p2-dual-precondition-egress.py`
- `.github/workflows/tibia-official-client-re-p2-dual-precondition-egress.yml`

Exact staged code windows requested, total `0xe20` / 3616 bytes:

- `dual_precondition`: `0xb40370..0xb40880`;
- `dual_entry_78`: `0xb56970..0xb56d60`;
- `dual_entry_80`: `0xb56d60..0xb57280`.

Source side is limited to ELF file VA-to-offset mapping and exact byte copying. Hosted side independently runs `objdump` on reconstructed bounded binary windows and fail-closes on known exact anchors including `0xb4066b -> QIODevice::write(QByteArray)`.

Workflow:

```yaml
run_id: 32016842999
head: 37c455f2ab3170457a0d084a7745eaa42e28aff1
source_job_id: 95348018877
last_observed_status: in_progress
last_observed_step: Set up job
source_runner_contract: [otclient, synology] / synology-otclient-01
semantic_runner: ubuntu-24.04 github-hosted
runtime_access: none
```

Two ordinary state observations on this exact head found the experiment still in progress. Per `ANTI_STALL_AND_EXECUTION_BUDGET.md`, this worker does not poll a third time in the same invocation.

## Acceptance inventory

- [ ] Exact client size/SHA reverified before source bytes are staged.
- [ ] Source staging file-only/non-semantic/bounded; no raw ELF/package.
- [ ] Hosted validation independently disassembles primary bytes and validates exact anchors.
- [ ] `0xb4066b` QIODevice receiver classified from primary disassembly.
- [ ] Payload relationship to promoted same-message path classified from exact dataflow.
- [ ] Final binary egress and final socket ownership promoted only if directly proven; otherwise `UNKNOWN`.
- [ ] Framing, sequence, compression and encryption classified separately without semantic overclaim.
- [x] Negative controls preserve `0xb46bd0` as text/newline QTcpSocket write but not gameplay-binary proof; `0xc33259` DISPROVEN; `0xb5b880` SUPERSEDED.
- [x] Quarantined run `31944051248` is not used as current proof.
- [x] No runtime/process-memory/login/gameplay/credentials/owner-funded AI quota used.
- [x] Draft PR #458 exists and exposes task/owned paths before evidence execution.

## Negative controls

Never use generic `QIODevice::write` enumeration, symbol/type naming alone, vtable adjacency, workflow colour, generated `result.json`, `0xb46bd0`, `0xc33259`, `0xb5b880` or quarantined run `31944051248` as substitute proof of gameplay binary egress.

## Current checkpoint

```yaml
proven:
  - PR #450 promoted the persistent-QBuffer -> ClientMessageProcessor -> RawDataProcessor -> DualConnection same-message chain.
  - Accepted non-quarantined artifact 9252025461 contains QIODevice::write(QByteArray) at 0xb4066b in dual_precondition@0xb40370.
  - Current canonical evidence proves TGameserverTCPConnection owns a concrete QTcpSocket at +0x10, while 0xb46bd0 is not gameplay-binary proof.
  - task ownership/admission/uniqueness are fresh and branch is restacked on main@16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc.
unknown:
  - exact receiver and payload identity at 0xb4066b
  - final binary egress
  - final socket ownership
  - framing
  - sequence
  - compression
  - encryption
conflicts: []
rejected_hypotheses:
  - 0xc33259 as gameplay sink
  - 0xb5b880 as gameplay endpoint
last_completed_step: created Draft #458, one-shot source/hosted tooling and started run 32016842999 on exact head 37c455f2ab3170457a0d084a7745eaa42e28aff1
blocker: experiment run 32016842999 is still in progress after the maximum two ordinary state observations for this exact head
next_action: once run 32016842999 is terminal, consume its source/final artifacts and independently inspect primary hosted disassembly before any semantic classification
```
