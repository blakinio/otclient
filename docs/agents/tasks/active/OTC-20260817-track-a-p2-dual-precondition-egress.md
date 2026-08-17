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
base_main: 8a52fe4af6a03fca29a831ae4fae4c3936cf025c
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-dual-precondition-egress.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/**
modules_touched: []
depends_on:
  - PR #450 merged as cbc6388e8607bb92120281a9a15148577994d3a6
  - docs/agents/evidence/OTC-20260816-track-a-promotion-coordination/20260817-p2-network-barrier-update.md
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md
  - PR #310 artifact 9252025461 as accepted exact-SHA symbol-identity cross-check only
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
decomposition_reason: one bounded discriminator around historical 0xb4066b egress candidate
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
branch_tree_repair:
  current_main: 8a52fe4af6a03fca29a831ae4fae4c3936cf025c
  current_main_tree: 58ca558dcade168eb823d4b43eca53a7890988c6
  rebuilt_tree: 2ce1f7e039e090f44eb97d4e34b4e25efd512a3b
  rebuild_commit: 8f412a73845ab4e37296612dc6106a3173b70eae
  ancestry_bind_commit: 3600f6c8927484c30b4a7c97ef411ab0c0ce0fae
  changed_file_inventory_after_repair: EXACTLY_THREE_P2_FILES
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

## Objective and disposition

Test historical `0xb4066b` `QIODevice::write(QByteArray const&)` as the next concrete gameplay egress candidate downstream of the promoted P2 chain.

Researcher disposition: **DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW**. Per Track A parallel-research governance, this researcher does not self-promote or self-merge semantic conclusions.

## Promoted input boundary

PR #450 promoted:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

At task start framing, sequence, compression, encryption, final binary egress and final socket ownership were `UNKNOWN`.

## Evidence generation

Exactly one bounded generation ran:

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

Source staging verified the exact regular-file size/SHA and copied three explicit executable-file windows totalling 3616 bytes. Source staging did no disassembly/semantic classification, did not access or execute a client process, and uploaded no raw executable/package. Semantic disassembly ran on GitHub-hosted Ubuntu.

Accepted non-quarantined #310 artifact `9252025461` was re-hashed to canonical digest `sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991` and used only to cross-check exact-SHA PLT identities:

```text
0x4dac00 = QBuffer::buffer()
0x4de370 = QIODevice::write(QByteArray const&)
```

Quarantined run `31944051248` was not used as proof.

## Primary result

Fresh exact bytes prove historical broad-window wording overreached the function boundary: `0xb40370` returns on visible paths by `0xb40421`; `0xb40630` is a separate function entry. Therefore `0xb4066b` is **not** inside the `0xb40370` / DualConnection `+0x90` function.

Inside `0xb40630`, exact register dataflow is:

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

Classifications:

```yaml
b4066b_inside_b40370_plus_0x90_function: DISPROVEN
b40630_distinct_function_entry: FACT
b4066b_qiodevice_write_callsite: FACT
b4066b_receiver: FACT:b40630_this_rbx_QBuffer_QIODevice_compatible
b4066b_receiver_exact_concrete_dynamic_type: UNKNOWN
b4066b_payload: FACT:original_b40630_second_argument_rsi
b4066b_direct_qtcpsocket_sink: DISPROVEN
payload_relationship_to_promoted_same_message: UNKNOWN
b40630_reachability_from_promoted_dualconnection_plus_0x78_or_plus_0x80: UNKNOWN
```

The direct receiver is the same `this` used for `QBuffer::buffer()`, not the separately proven `TGameserverTCPConnection +0x10 -> QTcpSocket*` member. This rejects `0xb4066b` as a direct QTcpSocket sink but does not prove what an unknown subclass may do internally and does not identify the global final socket sink.

Fresh `+0x78`/`+0x80` windows contain no direct call to `0xb40630`. Nested indirect `+0x10` calls at `0xb56c93` and `0xb57042` remain untyped by this bounded evidence, so no reachability/same-message edge is inferred.

Initial H1 — that `0xb4066b` is the concrete binary gameplay egress candidate reachable after the promoted same-message handoff — is `DISPROVEN_IN_STATED_FORM`.

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

No replacement sink is invented.

## Negative controls

- `0xb46bd0`: FACT QString/local-8-bit + newline write through `TGameserverTCPConnection::QTcpSocket*`; DISPROVEN as binary gameplay-frame proof.
- `0xc33259`: DISPROVEN QMatrix4x4/non-network candidate.
- `0xb5b880`: SUPERSEDED endpoint model.
- vtable adjacency/source-range proximity/workflow success are not reachability or semantic proof.

## Durable evidence and cleanup

Durable evidence:

- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/20260817-dual-egress-discriminator.md`
- `docs/agents/evidence/OTC-20260817-track-a-p2-dual-precondition-egress/result.json`
- source artifact `9283851546`
- hosted final artifact `9283858910`

The one-shot workflow and slicer ran exactly once and were removed after evidence consumption. They are not part of the final Draft diff.

A flawed intermediate restack had retained old branch-tree copies of unrelated XRes/RUNTIME paths. Final tree repair rebuilt the branch from current `main@8a52fe4af6a03fca29a831ae4fae4c3936cf025c` plus only the three P2 files, then bound ancestry to that exact main. Live PR changed-file inventory after `3600f6c8927484c30b4a7c97ef411ab0c0ce0fae` is exactly:

1. this task record;
2. `20260817-dual-egress-discriminator.md`;
3. `result.json`.

## Validation / E2E

- exact client/source-fence and bounded-file safety: PASS, run `32016842999`;
- hosted disassembly/anchor reconstruction: PASS, job `95348295109`;
- experiment-head Track A governance: PASS, run `32016848906`;
- independent primary-disassembly/dataflow review: PASS for the bounded classifications above;
- physical/runtime E2E: `NOT_APPLICABLE` — static file-byte/disassembly research only; no live runtime/network state changed or observed;
- final exact-head governance/repository CI: to be verified on the checkpoint commit produced by this update.

## Acceptance inventory

- [x] exact client size/SHA verified before staging;
- [x] source staging file-only/non-semantic/bounded; no raw ELF/package;
- [x] hosted validation independently disassembled exact bytes;
- [x] receiver and payload at `0xb4066b` classified from exact register dataflow;
- [x] historical function-boundary overclaim corrected;
- [x] direct QTcpSocket sink hypothesis rejected without inventing replacement egress;
- [x] same-message relationship retained as UNKNOWN absent an exact edge;
- [x] framing/sequence/compression/encryption kept independently UNKNOWN;
- [x] negative/quarantined evidence boundaries preserved;
- [x] no runtime/process-memory/login/gameplay/credentials/owner-funded AI used;
- [x] one-shot workflow/script retired;
- [x] durable Markdown and machine-readable result persisted;
- [x] final PR changed-file inventory reduced to exactly three P2 files;
- [ ] final exact-head required governance/CI and review hygiene verified.

## Handover

```yaml
researcher_status: READY_FOR_COORDINATOR_REVIEW_AFTER_FINAL_CI
research_output: DRAFT_NOT_PROMOTED
material_researcher_findings_open: 0
coordinator_review_required: true
coordinator_may_promote_without_independent_primary_review: false
blocker: final exact-head governance/CI and review hygiene only
next_action: after final exact-head checks pass, coordinator independently review Draft #458 artifacts 9283851546/9283858910 and classify ACCEPT, ACCEPT_WITH_EDITS, RETURN_FOR_EVIDENCE, or REJECT/SUPERSEDE
```
