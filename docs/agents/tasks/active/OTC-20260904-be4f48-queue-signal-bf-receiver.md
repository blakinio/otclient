---
task_id: OTC-20260904-be4f48-queue-signal-bf-receiver
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
branch: research/OTC-20260904-be4f48-queue-signal-bf-receiver
base_branch: main
base_main: f7a471c2cc7ab7fd53afacc8a7458eeefb96ad97
created: 2026-09-04T10:29:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-receiver.yml
  - tools/tibia_re_be4f48_queue_signal_bf_receiver/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-receiver.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-receiver/**
  - docs/superpowers/plans/2026-09-04-be4f48-queue-signal-bf-receiver.md
modules_touched: []
reuses:
  - merged coordinator promotion #876 / merge 44a35365e38b9483b9c43aff4c36c2379fdbfb3e
  - closed source PR #874 only as discovery input, never as promotion authority
blocks:
  - clean coordinator promotion before any Track B decision
---

# Objective

Resolve only the exact receiver/slot/writer connected to `TProtocolMessageQueue` signal `0xbf`, which is already proven to carry the exact causally consumed queued `GameclientMessage` shared pair. Follow at most one uniquely identity-preserving next writer edge.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal source result

```text
queue_sender=tibia::protocol::TProtocolMessageQueue
queue_signal_index=0xbf
queue_signal_name=clientMessageReadyToProcess
queue_signal_body=0xbd2190
queue_signal_static_metaobject_argument_proven=true
queue_signal_connectimpl_candidate_count=1
queue_signal_connectimpl_callsite=0xbe2eee
queue_signal_connectimpl_fde=0xbe2a50..0xbe3086
queue_signal_receiver_provenance=ENTRY_ARG:rdi
queue_signal_receiver_identity=UNKNOWN
queue_signal_slot_identity=UNKNOWN
queue_signal_writer_identity=UNKNOWN
next_unique_writer_edge=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=QUEUE_SIGNAL_BF_QSLOT_FUNCTION_NOT_UNIQUELY_PROVEN
```

The earlier whole-executable `exec_refs()` approach was removed after two hosted-runner shutdowns. TDD now forbids whole executable-section Capstone disassembly. The final analyzer uses only exact `.text` RIP-relative LEA byte-prefiltering plus per-candidate FDE validation.

The false intermediate blocker around the static metaobject was also removed with a bounded exact register-chain proof:

```text
0xbd221d: rbp = 0x30b73e0
0xbd22ae: rsi = rbp
0xbd22c2: QMetaObject::activate
```

This proves the signal body and yields one exact `QObject::connectImpl` at `0xbe2eee`. The QSlot function identity remains non-unique/unproven, so this lane stops here.

# TDD / exact-head evidence

Initial repository-only RED run `33853900210` failed before package/client steps. Bounded-xref RED `33855995246` and static-metaobject register-chain RED `33856595302` also failed repository-only before exact-client materialization.

Final exact-current analysis:

```text
SOURCE_ANALYSIS_HEAD=b2dd0fac6c58c325b93566c3f150e86e807ae208
SOURCE_RUN=33856767530 success
SOURCE_JOB=100971771959 success
ARTIFACT_ID=9930504401
ARTIFACT_DIGEST=sha256:0eae231ded57a47aa7ea2dfa37339b2a2e465a0e1b031e618e95dccd04da8f6f
CI_RUN=33856767713 success
GOVERNANCE_RUN=33856767680 success
SELF_HOSTED_BOUNDARY_RUN=33856767493 success
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
track_b_pr_284_modified=false
```

# Anti-loop / next action

Do not extend #880 into another Qt/QSlot/writer discovery loop. Preserve this precise blocker and wait for clean coordinator promotion together with terminal source PR #879. Any later QSlot-function discriminator must be a newly admitted bounded task.

next_action: exact-head validate this terminal evidence; then clean coordinator promotion should consume #879/#880, close both source PRs unmerged as consumed, and admit only the next narrow source boundaries justified by the promoted result.
