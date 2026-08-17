---
task_id: OTC-20260817-track-a-p2-dual-precondition-egress
status: investigating
agent: ChatGPT
session_id: chatgpt-p2-egress-20260817-1141
session_role: draft_researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260817-track-a-p2-dual-precondition-egress
worktree: github-only-ref:research/OTC-20260817-track-a-p2-dual-precondition-egress
base_branch: main
base_main: 60ab740872d52f3f7c4802d49fd5275a9968d085
risk: medium
created: 2026-08-17T11:41:00+02:00
updated: 2026-08-17T11:41:00+02:00
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
last_progress_at: 2026-08-17T11:41:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
additional_task_allowance_consumed: false
---

# Track A P2 — DualConnection precondition / egress discriminator

## Objective

Resolve the first still-UNKNOWN transport boundary immediately downstream of the promoted P2 chain by recovering exact-client dataflow around `TGameserverDualConnection` precondition `+0x90 @ 0xb40370`, especially the `QIODevice::write(QByteArray const&)` call observed at `0xb4066b` in accepted non-quarantined artifact `9252025461`.

The task must determine, from exact fenced native-Linux client bytes, whether that write is causally tied to the same post-`TGameserverNetworkPacketRawDataProcessor` gameplay message and what concrete QIODevice/object owns the destination. It may narrow framing/sequence/compression/encryption ordering only when direct instruction/dataflow evidence supports the claim.

## Current canonical boundary consumed

Coordinator promotion PR #450 established:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

`protocol_stage_order = PROVEN_PARTIAL`.

Still canonical `UNKNOWN` at task start:

- framing;
- sequence;
- compression;
- encryption;
- final binary egress;
- final socket ownership;
- complete transport ordering beyond the recovered processor chain.

## Fresh admission / ownership / uniqueness / drift preflight

- `main@60ab740872d52f3f7c4802d49fd5275a9968d085` verified at dispatch.
- No open `P2-NETWORK` PR and no active branch/task matching this responsibility was found.
- Existing open Track A work is disjoint: RUNTIME discriminator PR #457 and P0 PR #302 do not own these task/evidence/workflow/script paths.
- Old P2 source PRs #301/#308/#310/#368/#449 are closed; #450 is the accepted canonical dependency.
- This worker owns only the four path classes declared in front matter.
- Parallel-research contract applies: researcher output remains Draft-only; coordinator alone may promote/merge semantic conclusions.

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

If exact executable bytes are required, the only permitted non-hosted step is the previously accepted #449-style source-staging boundary: verify the retained regular file against exact size/SHA and copy narrowly enumerated file-byte windows as small UTF-8 hex/metadata. That source step performs no disassembly or semantic classification and uploads no raw executable/package. All disassembly and semantic decisions occur on GitHub-hosted runners.

## Primary hypothesis

`H1`: the call at `0xb4066b` is part of the concrete binary gameplay egress path reachable after the promoted same-message handoff into `TGameserverDualConnection`, and exact dataflow can identify the QIODevice receiver and its relation to the proven `TGameserverTCPConnection::QTcpSocket*` ownership graph.

This hypothesis may be accepted, narrowed or disproven. A successful workflow alone is not semantic evidence.

## Initial discriminator window

Recover exact bytes sufficient to decode at least:

- `0xb40370..0xb40880` (the full known precondition FDE/window);
- exact `TGameserverDualConnection` vtable words needed to revalidate `+0x78`, `+0x80`, `+0x90` dispatch identity;
- only additional bounded code/data windows that are directly required to resolve a concrete receiver/callee discovered from the first window.

At minimum classify the dataflow around:

- indirect `+0x78` call near `0xb40643`;
- `QBuffer::buffer` near `0xb40656`;
- indirect/helper call near `0xb40662`;
- `QIODevice::write(QByteArray const&)` at `0xb4066b`;
- later `QBuffer::buffer`, `QByteArray::remove`, `QIODevice::readAll` and virtual `+0x10` sequence through roughly `0xb40735`.

## Acceptance inventory

- [ ] Exact client size/SHA is reverified before any source bytes are staged.
- [ ] Source staging is file-only, non-semantic, bounded, UTF-8-safe and contains no raw ELF/package.
- [ ] Hosted validation independently disassembles the staged bytes and records exact instruction/dataflow evidence.
- [ ] The QIODevice receiver at `0xb4066b` is classified as `FACT`, `INFERENCE`, `UNKNOWN` or `DISPROVEN` with exact evidence.
- [ ] Relationship of the written QByteArray to the promoted same-message path is classified without using names/vtable adjacency as proof.
- [ ] Final socket ownership is promoted in the Draft only if exact object/dataflow proves it; otherwise remains `UNKNOWN`.
- [ ] Framing, sequence, compression and encryption are each classified separately and remain `UNKNOWN` unless directly evidenced.
- [ ] Negative controls preserve `0xb46bd0` as a proven QString/newline QTcpSocket write but DISPROVEN as gameplay-binary proof, `0xc33259` as QMatrix4x4/non-network, and `0xb5b880` as SUPERSEDED.
- [ ] No quarantined run `31944051248` is used as current proof.
- [ ] No live runtime, process memory, credentials, login, gameplay or owner-funded AI quota is used.
- [ ] Draft PR records raw run/artifact IDs and enough primary evidence for an independent coordinator review.

## Validation / E2E boundary

Focused validation is deterministic parser/disassembly/dataflow checking on GitHub-hosted Linux. Repository governance/CI applies to the exact Draft head.

Physical/runtime E2E is `NOT_APPLICABLE` for this static research producer because it changes no client/runtime behavior and claims no live transport observation. Any future causal live validation belongs to separately admitted RUNTIME work.

## Negative controls

Do not use as proof:

- generic `QIODevice::write` enumeration;
- symbol/type naming without concrete dataflow;
- vtable adjacency as temporal/ownership proof;
- old final-socket candidate `0xc33259`;
- old endpoint `0xb5b880`;
- text/newline writer `0xb46bd0` as gameplay-binary sink;
- quarantined Synology static-analysis run `31944051248`;
- workflow success or generated `result.json` without primary byte/disassembly review.

## Stop conditions

Stop only for a real ownership/safety conflict, inability to obtain the narrowly required exact-fenced file bytes under the permitted staging boundary, exhausted bounded repair budget, or a Draft result that is complete enough for coordinator review.

## Current checkpoint

```yaml
proven:
  - PR #450 promoted the persistent-QBuffer -> ClientMessageProcessor -> RawDataProcessor -> DualConnection same-message chain.
  - Accepted non-quarantined artifact 9252025461 contains a QIODevice::write(QByteArray) call at 0xb4066b inside dual_precondition@0xb40370.
  - Current canonical evidence proves TGameserverTCPConnection owns a concrete QTcpSocket at +0x10, but 0xb46bd0 is text/newline output and not gameplay-binary proof.
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
last_completed_step: fresh trusted-base, admission, ownership, uniqueness and P2 barrier preflight; unique task/branch claimed
next_action: add one-shot exact-file bounded source slicer plus GitHub-hosted decoder for the 0xb40370 discriminator and run it once
```
