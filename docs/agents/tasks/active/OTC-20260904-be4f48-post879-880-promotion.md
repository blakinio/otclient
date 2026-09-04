---
task_id: OTC-20260904-be4f48-post879-880-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260904-be4f48-post879-880-promotion
base_branch: main
base_main: f7a471c2cc7ab7fd53afacc8a7458eeefb96ad97
created: 2026-09-04T11:10:00+02:00
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
implementation_authorized: false
owned_paths:
  - docs/agents/evidence/OTC-20260904-be4f48-post879-880-promotion/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-post879-880-promotion.md
modules_touched: []
reuses:
  - source Draft PR #879 final head 7bbbc1f1e5c02f31a71999333ba5423649e3d94a
  - source Draft PR #880 final head 2b640340864c599851c07f9e31564a5644b8628d
  - merged coordinator promotion #876 and alias registration #878
blocks:
  - Track B PR #284 remains blocked from protocol mutation/E2E
---

# Objective

Promote only independently verified exact-current facts from source Draft PRs #879 and #880, preserve all remaining UNKNOWN boundaries, keep Track B PR #284 untouched, and select the smallest justified next source discriminators.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Coordinator result

```text
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_FIELD_READS_IN_SELECTED_FDE=165
SENDLOGIN_RECEIVER_FIELD_WRITES_IN_SELECTED_FDE=0
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_STATIC_METAOBJECT=0x30b73e0
QUEUE_SIGNAL_CONNECTIMPL_CANDIDATE_COUNT=1
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QUEUE_SIGNAL_QSLOT_FUNCTION=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
terminal_result=SOURCE_BLOCKER
integration_status=BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA
```

# Acceptance

1. Promote only sanitized source facts from #879/#880 and preserve exact source heads/runs/artifacts/checks.
2. Do not promote source analyzers/workflows.
3. Keep receiver class identity UNKNOWN until `[rbx+0x88]` initializer/owner is independently typed.
4. Keep queue QSlot function/writer UNKNOWN until the unique `connectImpl@0xbe2eee` slot-object construction is independently resolved.
5. Keep Field6 value, complete pre-login sequence and final writer contract UNKNOWN.
6. Keep `TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN`; do not mutate #284.
7. Do not authorize runtime, OCR/Vision, official-client execution, login, credentials, process-memory access, packet capture or official-service E2E.
8. Exact-head CI/governance and full diff review must pass before merge.
9. After merge, close source PRs #879/#880 unmerged as consumed and archive this coordinator lifecycle.
10. Register new aliases only from fresh trusted main after promotion/lifecycle merge.

# Next source boundaries

Exactly two independent follow-ups are justified:

```text
OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER
  resolve only the initializer/ownership chain for [entry-rdi-derived-rbx+0x88],
  stopping at the first non-unique owner/constructor edge.

OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY
  resolve only the QSlot object/function for unique connectImpl@0xbe2eee
  from call-return boundary 0xbe2eb1, then follow at most one unique writer edge.
```

They may run in parallel. Neither may broaden into global constructor/Qt/socket/writer discovery or modify Track B.

next_action: validate this clean promotion on exact head, squash-merge, close #879/#880 unmerged as consumed, archive lifecycle, then register the two new repository-owned prompts/aliases from fresh trusted main.
