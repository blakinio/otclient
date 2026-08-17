---
task_id: OTC-20260817-track-a-p2-dual-precondition-egress
status: ready
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
base_main: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
risk: medium
created: 2026-08-17T11:41:00+02:00
updated: 2026-08-17T12:01:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-precondition-egress.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/**
modules_touched: []
depends_on:
  - PR #450 merged as cbc6388e8607bb92120281a9a15148577994d3a6
  - docs/agents/evidence/OTC-20260816-track-a-promotion-coordination/20260817-p2-network-barrier-update.md
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md
  - PR #310 artifact 9252025461 as accepted symbol-identity cross-check only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: exact-fenced bounded file-byte staging plus GitHub-hosted disassembly; no live official-client runtime
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded discriminator around the historical 0xb4066b egress candidate
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
research_output: DRAFT_NOT_PROMOTED_READY_FOR_COORDINATOR_REVIEW
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
last_progress_at: 2026-08-17T12:01:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final_draft_package
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
additional_task_allowance_consumed: false
---

# Track A P2 — DualConnection egress discriminator

## Research objective

Test the historical `0xb4066b` `QIODevice::write(QByteArray const&)` candidate against the currently promoted P2 same-message chain and determine whether it is a concrete final binary/socket egress boundary.

Researcher output is **Draft-only**. Coordinator review/promotion is mandatory and this task does not self-merge.

## Current promoted input

PR #450 established:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

At task start framing, sequence, compression, encryption, final binary egress and final socket ownership were `UNKNOWN`.

## Admission / scope

```yaml
runtime_access: none
mutation_authorized: false
physical_e2e_required: false
semantic_execution: github_hosted
source_staging: exact-fenced bounded regular-file bytes only; no source-side disassembly/semantics
```

No client process, process memory, canonical runtime, X11/VNC, login/session, gameplay, packet replay, client mutation, credentials or owner-funded AI quota was used.

## Main drift reconciliation

The branch was initially dispatched from `60ab740872d52f3f7c4802d49fd5275a9968d085` and first restacked on disjoint XRes merge `16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc` via merge commit `bc562567f6d0a502323d5f2911db3f94fec82b52`.

During evidence review main advanced again to `1eb4a8edecba3966aa1e6155e241b404eb4d30cb`. Compare from `16c6fb...` showed only XRes helper/tests and RUNTIME/XRes task/archive changes; no P2 path overlap. The branch was restacked without force-push via `e862a7c7e58788c7a8020d43eee3cd4443f52f2b`.

## Evidence generation

One generation only:

```yaml
experiment_head: 37c455f2ab3170457a0d084a7745eaa42e28aff1
run: 32016842999
source_job: 95348018877
hosted_job: 95348295109
source_artifact: 9283851546
source_artifact_digest: sha256:7e03ed66bff463e288b5f2414bad8190a27bf421161ba1218c2a74d7342baeab
final_artifact: 9283858910
final_artifact_digest: sha256:2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
track_a_governance_run: 32016848906
track_a_governance_result: SUCCESS
```

The source artifact contains exactly three bounded file-byte windows totalling 3616 bytes. Hosted validation reconstructed/disassembled those windows on Ubuntu. The accepted non-quarantined #310 artifact `9252025461` was independently re-hashed to its canonical digest `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991` and is used only to cross-check exact-SHA PLT identities:

```text
0x4dac00 = QBuffer::buffer()
0x4de370 = QIODevice::write(QByteArray const&)
```

## Result

### FACT — historical broad-window wording did not describe one function

Fresh exact bytes prove `0xb40370` returns on all visible paths by `0xb40421`. A separate entry begins at `0xb40430`; another distinct prologue begins at `0xb40630`.

Therefore:

```yaml
b4066b_inside_TGameserverDualConnection_plus_0x90_function_b40370: DISPROVEN
```

### FACT — `0xb4066b` receiver and payload dataflow

Inside distinct function `0xb40630`:

```text
b40634: mov r12,rsi     # preserve original second argument
b40639: mov rbx,rdi     # preserve this
...
b40656: call 0x4dac00   # QBuffer::buffer()
...
b40665: mov rsi,r12
b40668: mov rdi,rbx
b4066b: call 0x4de370   # QIODevice::write(QByteArray const&)
```

Thus:

```yaml
qiodevice_write_receiver: FACT:b40630_this_rbx
receiver_structural_base: FACT:QBuffer/QIODevice-compatible at that base address
receiver_exact_concrete_dynamic_type: UNKNOWN
qiodevice_write_payload: FACT:original_b40630_second_argument_rsi
```

The direct receiver is the same `this` used for `QBuffer::buffer()`, not the separately proven `TGameserverTCPConnection +0x10 -> QTcpSocket*` member.

```yaml
b4066b_direct_qtcpsocket_sink: DISPROVEN
```

This does not prove what an unknown subclass may do internally and therefore does not identify the global final socket sink.

### UNKNOWN — no recovered same-message reachability edge

Fresh `TGameserverDualConnection +0x78` and `+0x80` windows contain no direct call to `0xb40630`. They contain nested indirect `+0x10` dispatches at `0xb56c93` and `0xb57042`, but the staged evidence does not type those nested vtables as `0xb40630`.

Therefore:

```yaml
payload_relationship_to_promoted_same_message: UNKNOWN
b40630_reachability_from_promoted_plus_0x78_or_plus_0x80: UNKNOWN
```

No source-range proximity or vtable adjacency is used as reachability proof.

## Hypothesis disposition

```yaml
H1: DISPROVEN_IN_STATED_FORM
statement: 0xb4066b is the concrete binary gameplay egress candidate reachable after the promoted same-message handoff into TGameserverDualConnection
reasons:
  - b4066b is not inside the b40370 +0x90 function
  - direct QIODevice receiver is the b40630 QBuffer-compatible this, not a proven QTcpSocket member
  - no exact edge from promoted +0x78/+0x80 windows to b40630 was recovered
```

## Remaining P2 state

```yaml
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
complete_transport_stage_order_beyond_promoted_chain: UNKNOWN
```

This is a bounded negative result; no replacement sink is invented.

## Negative controls

- `0xb46bd0`: proven QString/local-8-bit + newline write through `TGameserverTCPConnection::QTcpSocket*`, but DISPROVEN as binary gameplay-frame proof.
- `0xc33259`: DISPROVEN QMatrix4x4/non-network candidate.
- `0xb5b880`: SUPERSEDED endpoint model.
- quarantined run `31944051248`: not used as proof.

## Durable evidence

- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/20260817-dual-egress-discriminator.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/result.json`
- source artifact `9283851546`
- final hosted disassembly artifact `9283858910`

One-shot workflow/script were consumed exactly once and then removed from the Draft branch. They are not promotion payload.

## Validation / E2E

- source exact fence + bounded-file safety: PASS in run `32016842999`;
- hosted exact-anchor reconstruction/disassembly: PASS in job `95348295109`;
- experiment-head Track A governance: PASS in run `32016848906`;
- manual primary-disassembly/dataflow review: PASS for the bounded classifications above;
- physical/runtime E2E: `NOT_APPLICABLE` because no live runtime/network state was changed or observed;
- final Draft-package exact-head repository/governance CI: resolve from live GitHub state on the final task checkpoint head.

## Researcher acceptance inventory

- [x] exact client size/SHA verified before staging;
- [x] source staging file-only/non-semantic/bounded; no raw ELF/package;
- [x] hosted validation independently disassembled primary bytes;
- [x] `0xb4066b` receiver and payload classified from exact register dataflow;
- [x] historical `b40370` broad-window overreach corrected;
- [x] direct QTcpSocket sink hypothesis rejected without inventing a replacement;
- [x] same-message relationship remains UNKNOWN because no exact edge was recovered;
- [x] framing/sequence/compression/encryption remain separately UNKNOWN;
- [x] quarantined and superseded candidates excluded;
- [x] no runtime/process-memory/login/gameplay/credentials/owner-funded AI used;
- [x] one-shot workflow/script retired after the one evidence generation;
- [x] durable Markdown + machine-readable result persisted;

## Handover

```yaml
researcher_status: READY_FOR_COORDINATOR_REVIEW
research_output: DRAFT_NOT_PROMOTED
material_researcher_findings_open: 0
coordinator_review_required: true
coordinator_may_promote_without_independent_primary_review: false
last_completed_step: independently reviewed exact source/final artifacts, persisted bounded negative result, restacked on current main and retired consumed one-shot tooling
blocker: none inside researcher scope
next_action: coordinator independently review Draft PR #458 artifacts 9283851546/9283858910 and classify ACCEPT, ACCEPT_WITH_EDITS, RETURN_FOR_EVIDENCE, or REJECT/SUPERSEDE
```
