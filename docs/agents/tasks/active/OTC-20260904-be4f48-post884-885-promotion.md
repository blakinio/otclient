---
task_id: OTC-20260904-be4f48-post884-885-promotion
status: active
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: integrate
branch: docs/OTC-20260904-be4f48-post884-885-promotion
base_branch: main
base_main: e24462d72942d8381e1a468de84f16b60f1aa8c9
created: 2026-09-04T13:47:00+02:00
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: false
source_prs: [884, 885]
owned_paths:
  - docs/agents/tasks/active/OTC-20260904-be4f48-post884-885-promotion.md
  - docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/**
last_completed_step: independent coordinator audit reconstructed exact-current source state for PRs 884 and 885 and found no implementable Track B wire delta; exact-head governance admission metadata repaired after fail-closed validation
next_action: require exact-head CI/governance and clean review hygiene, then squash-merge with expected-head guard before consuming source PRs
---

# Objective

Perform the clean coordinator promotion for the two terminal exact-current source-only Track A PRs:

- #884 `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER`;
- #885 `OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY`.

The coordinator may promote only sanitized exact-current facts for the current official Linux client fence:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No analyzer/workflow is promoted. Track B PR #284 is not modified. No official client is executed and no runtime/login/credentials/process-memory/packet-capture/OCR/Vision/official-service-E2E authority exists in this task.

# Independent coordinator audit

The coordinator independently re-read the exact current source evidence and the bounded analyzer logic at the live PR heads, checked the complete changed-path sets, and revalidated the current exact-head check state.

## Source #884

```text
CURRENT_PR_HEAD=18a0567c61d3f606e4a8d72e4ab832583ca6b429
SCIENTIFIC_SOURCE_HEAD=29d30b7de6a59bfa0a40c619abfbf3f3061692e1
SOURCE_RESULT=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=CONNECTION_OWNER_FDE_DIRECT_CALLER_NOT_UNIQUE
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_FIELD_DEFINITION=UNKNOWN
SENDLOGIN_RECEIVER_OWNER_CHAIN=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

The bounded target-specific direct-caller search preserves zero accepted callers as UNKNOWN. It does not infer a constructor, owner, receiver identity, or causal binding.

Current exact-head qualification on `18a0567...`:

```text
FOCUSED_RUN=33867156653 success
CI_RUN=33867157221 success
GOVERNANCE_RUN=33867156626 success
SELF_HOSTED_BOUNDARY_RUN=33867156624 success
```

## Source #885

```text
CURRENT_PR_HEAD=5fb8be7458fb8ecc12818baab5729681df67ee21
SCIENTIFIC_SOURCE_HEAD=2431ef51a9e3d95365fbae0d1b5d23846b9b1a99
SOURCE_RESULT=QUEUE_SIGNAL_BF_QSLOT_IDENTITY_PROVEN
FIRST_MISSING_BOUNDARY=NEXT_WRITER_EDGE_SEMANTICS_NOT_UNIQUELY_PROVEN
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_CONNECTIMPL_CALLSITE=0xbe2eee
QUEUE_SIGNAL_RECEIVER_PROVENANCE=ENTRY_ARG:rdi
QSLOT_OBJECT_PRODUCER=operator new@0xbe2eb1 size=0x20 -> r9<-rax@0xbe2ec3
QSLOT_DISPATCH_IMPL_TARGET=0xbe4df0
QSLOT_FUNCTION_TARGET=0xbd2190
QSLOT_IDENTITY_PROVEN=true
QUEUE_SIGNAL_WRITER_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

The coordinator independently checked that the exact QSlot object separates dispatcher storage at `+0x08` from callable payload at `+0x10..+0x20`; the callable payload is `(0xbd2190, 0)` and the dispatcher direct-call branch selects `0xbd2190`. This proves QSlot callable identity only. It does not prove writer identity or a TCP boundary.

Current exact-head qualification on `5fb8be7...`:

```text
FOCUSED_RUN=33867557971 success
CI_RUN=33867558234 success
GOVERNANCE_RUN=33867558010 success
SELF_HOSTED_BOUNDARY_RUN=33867557979 success
```

# Integration decision

```text
terminal_result=SOURCE_BLOCKER
integration_status=BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

No source result provides an implementable exact-current Track B mutation. PR #284 therefore remains blocked and unchanged. Runtime Field6 observation remains unjustified because the native pre-success ordering/final writer contract are still not closed.

# Next bounded source boundaries

The coordinator admits two independent follow-ups, each using a new proof mode rather than rerunning a consumed search:

1. `OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE`
   - start only from connection-owner FDE `0x7c6700..0x7cc933`, its `entry-rdi` owner object, and the proved receiver field `[entry-rdi-derived-rbx+0x88]`;
   - resolve only bounded in-FDE/one-edge vtable, RTTI, or QMeta evidence sufficient to type the connection-owner object and, only if uniquely implied, the `+0x88` receiver;
   - do not repeat the zero-result direct-caller search and do not open a global constructor/RTTI/QMeta/QObject census.

2. `OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE`
   - start only from `connectImpl@0xbe2eee`, receiver provenance `ENTRY_ARG:rdi`, exact QSlot callable `0xbd2190`, and the causally carried `GameclientMessage` shared pair;
   - resolve the exact receiver object/class identity and whether this connection is a signal relay;
   - if and only if that identity is unique, follow at most one next identity-preserving `clientMessageReadyToProcess` edge; no global socket/writer census.

These follow-ups may run in parallel after a separate alias-registration lifecycle from fresh trusted main. They authorize no runtime, Track B mutation, or official-service E2E.
