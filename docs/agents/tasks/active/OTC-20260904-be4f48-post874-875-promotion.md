---
task_id: OTC-20260904-be4f48-post874-875-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260904-be4f48-post874-875-promotion
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
created: 2026-09-04T10:14:00+02:00
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
  - docs/agents/evidence/OTC-20260904-be4f48-post874-875-promotion/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-post874-875-promotion.md
modules_touched: []
reuses:
  - source Draft PR #874 exact-current queue-drain evidence at 369acfb075e8a9d2716dcd73280ca092e0600332
  - source Draft PR #875 exact-current peer-metaowner evidence at final head 9653268fc57e94adcfb41c1f6b1a3e7914f2aa0f
  - merged coordinator promotion #871 and alias registration #873
blocks:
  - Track B PR #284 remains blocked from protocol mutation/E2E
---

# Objective

Promote only independently verified exact-current facts from source Draft PRs #874 and #875, preserve all remaining UNKNOWN boundaries, keep Track B PR #284 untouched, and select the smallest justified next source discriminators.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Acceptance

1. Preserve #874 exact final head/check/artifact identities and promote `QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION=true` plus signal `0xbf` dispatch only.
2. Preserve #875 final PR head, exact analysis head/check/artifact identities and promote only the proven `TLoginProtocolMessageHandler::sendLoginMessage -> QObject::connectImpl -> QSlot(adapter 0xbd3050)` facts.
3. Keep #875 receiver class identity UNKNOWN and do not upgrade `sendlogin_causal_binding_proven` until the receiver endpoint is independently typed.
4. Keep signal `0xbf` receiver/slot/writer UNKNOWN and do not infer a writer from generic Qt/QMeta/socket candidates.
5. Keep Field6 value, complete pre-login sequence and final writer contract UNKNOWN.
6. Do not authorize runtime, OCR/Vision, official-client execution, login, credentials, process-memory access, packet capture or official-service E2E.
7. Keep Track B PR #284 unchanged and `TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN`.
8. Exact-head CI/governance and full diff review must pass before merge.
9. After merge, close source PRs #874 and #875 unmerged as consumed and archive this coordinator lifecycle.
10. Register new aliases only from fresh trusted main after the promotion/lifecycle merge.

# Coordinator result

```text
QUEUE_DRAIN_CAUSAL_CONSUMPTION=true
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_RECEIVER_WRITER=UNKNOWN
SENDLOGIN_SENDER_IDENTITY=tibia::authentication::TLoginProtocolMessageHandler
SENDLOGIN_SIGNAL=sendLoginMessage
SENDLOGIN_CONNECTION_PRIMITIVE=QObject::connectImpl@0x7c6b9f
SENDLOGIN_RECEIVER_PROVENANCE=[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
terminal_result=SOURCE_BLOCKER
```

# Next source boundaries

Exactly two independent follow-ups are justified:

```text
OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY
  resolve only [entry-rdi-derived-rbx+0x88] to an exact receiver class/ownership chain,
  then prove or reject the complete connectImpl sender/receiver pair and sendLogin adapter causality.

OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER
  resolve only the connected receiver/slot/writer for TProtocolMessageQueue signal 0xbf
  carrying the exact queued GameclientMessage pair, following at most one next unique writer edge.
```

They may run in parallel. Neither may broaden into global Qt/socket/writer discovery or modify Track B.

next_action: validate this clean promotion on exact head, squash-merge, close #874/#875 unmerged as consumed, archive lifecycle, then register the two new repository-owned prompts/aliases from fresh trusted main.
