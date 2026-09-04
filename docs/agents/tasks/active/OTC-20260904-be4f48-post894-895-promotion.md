---
task_id: OTC-20260904-be4f48-post894-895-promotion
status: active
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: integrate
branch: docs/OTC-20260904-be4f48-post894-895-promotion
base_branch: main
base_main: 7e67c67783b19575ec7f378c7be49cb69d87f1ce
created: 2026-09-04T16:32:00+02:00
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
source_prs: [894, 895]
owned_paths:
  - docs/agents/tasks/active/OTC-20260904-be4f48-post894-895-promotion.md
  - docs/agents/evidence/OTC-20260904-be4f48-post894-895-promotion/**
last_completed_step: independently falsified both terminal exact-current source blockers and selected proof-mode-changing bounded successors
next_action: open docs-only promotion PR; require exact-head CI/governance and clean review hygiene before expected-head squash merge
---

# Objective

Clean coordinator promotion for terminal exact-current source-only PRs #894 and #895.

Exact fence:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No runtime, official-client execution, login, credentials/session access, process memory, packet capture, OCR/Vision, official-service E2E, Field6 runtime observation, or Track B PR #284 mutation is authorized.

# Source #894

```text
PR_HEAD=2e8f797ad0230b9a4338bd44ff98fc562010e422
SCIENTIFIC_HEAD=9c68d92657100b054c6d5006ab46ddc5303112ee
terminal_result=SOURCE_BLOCKER
OWNER_EDGE=0x7c67b8->0x7e8f30
CALLEE_FDE=0x7e8f30..0x7f06d6
OWNER_OBJECT_IDENTITY=UNKNOWN
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
FIRST_MISSING_BOUNDARY=CALLEE_INTERNAL_IDENTITY_EDGE_NOT_FOUND
```

Independent coordinator readback confirms the analyzer inspects only the promoted callee FDE for carried `ENTRY_ARG:rdi`, object-tied vptr/RTTI, same-object external calls, and at most one unique same-object internal edge. It found no such internal candidate and does not justify a positive owner type.

Exact-head checks:

```text
FOCUSED_RUN=33881287522 success
CI_RUN=33881287951 success
GOVERNANCE_RUN=33881287474 success
SELF_HOSTED_BOUNDARY_RUN=33881287646 success
```

# Source #895

```text
PR_HEAD=6e853a400831431ad3c3489828b34441dab86636
SCIENTIFIC_HEAD=88e8c05babc856d89892226ad3cd27d6739997ce
terminal_result=SOURCE_BLOCKER
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_RECEIVER=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
SELF_RELAY_CONNECTIMPL=0xbe2eee
QSLOT_FUNCTION_TARGET=0xbd2190
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
FIRST_MISSING_BOUNDARY=NO_NEXT_CLIENTMESSAGEREADYTOPROCESS_SOURCE_CONNECTION_IN_BOUNDED_QUEUE_CONSTRUCTOR_FDE
```

Independent coordinator readback confirms the analyzer enumerates exactly the direct `QObject::connectImpl` calls in queue-constructor FDE `0xbe2a50..0xbe3086`: `0xbe2e54` and the promoted self-relay `0xbe2eee`. There are zero post-self-relay connects and zero additional exact-signal identity-preserving candidates. It does not justify a downstream endpoint or writer claim.

Exact-head checks:

```text
FOCUSED_RUN=33881260048 success
CI_RUN=33881260365 success
GOVERNANCE_RUN=33881260072 success
SELF_HOSTED_BOUNDARY_RUN=33881260116 success
```

# Integration decision

```text
terminal_result=SOURCE_BLOCKER
integration_status=BLOCKED_NO_IMPLEMENTABLE_WIRE_DELTA
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_QUEUE_WRITER=UNKNOWN
FINAL_TCP_WRITER=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

No Track B implementation or official-service E2E is unlocked.

# Next bounded source boundaries

Register only after promotion + archive:

1. `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS`
   - change proof mode away from owner type discovery;
   - start only from promoted receiver provenance `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]` at the exact sendLogin `connectImpl` context;
   - trace the loaded field object's immediate bounded uses/ABI role and at most one object-tied vptr/QMeta/type edge;
   - do not rerun #884/#889/#894 owner/caller/callee identity scans and do not globally census `+0x88` fields.

2. `OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE`
   - change proof mode away from exhausted constructor-local connect enumeration;
   - start only from exact signal body `0xbd2190`, exact queue static-metaobject/signal identity, and `connectImpl` semantics;
   - admit only exact-signal reference sites that can be causally tied to one `QObject::connectImpl` setup, then classify at most one unique downstream endpoint;
   - no generic/global QObject/QSlot/socket/writer census and no redo of #885/#890/#895.

These source-only tasks are independent and may run in parallel.