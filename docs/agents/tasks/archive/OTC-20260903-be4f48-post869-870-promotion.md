---
task_id: OTC-20260903-be4f48-post869-870-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: close
branch: docs/archive-OTC-20260903-be4f48-post869-870-promotion
base_branch: main
base_main: 18700fcf98478c83e19187a9eb169d087f592ba3
created: 2026-09-03T18:43:00+02:00
completed: 2026-09-03T18:52:00+02:00
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
  - docs/agents/evidence/OTC-20260903-be4f48-post869-870-promotion/**
  - docs/agents/tasks/archive/OTC-20260903-be4f48-post869-870-promotion.md
modules_touched: []
reuses:
  - source Draft PR #869 exact-current sender-peer evidence at cce4f0dc4f34eecb069f326681958e58a8e6585c
  - source Draft PR #870 exact-current final-writer evidence at a87904047032fcc8c20b7ac7c1aac6c43d805207
  - merged promotion #866 and lifecycle #867
blocks:
  - Track B PR #284 remains blocked from protocol mutation/E2E
---

# Objective

Promote only the independently verified exact-current facts from source Draft PRs #869 and #870, correct the previously promoted `0x4d8670` helper interpretation, preserve all UNKNOWN boundaries, select the smallest justified next source discriminators, close the consumed source lanes, and archive the lifecycle without modifying Track B PR #284.

# Completion

Coordinator promotion PR #871 was rebuilt cleanly from trusted `main@a35bbacd475a31ce52736ccbc3b5e837626def66`, validated and squash-merged:

```text
promotion PR          #871
promotion final head  4f704cc289989103bfb8835f067cd84dc3cc1f68
promotion CI          33781043365 = SUCCESS
promotion governance  33781041411 = SUCCESS
promotion merge       18700fcf98478c83e19187a9eb169d087f592ba3
changed files         3 docs-only
review submissions    0
review threads        0
material comments     0
```

Source Draft PRs were then closed **unmerged as consumed**:

```text
#869 head cce4f0dc4f34eecb069f326681958e58a8e6585c = CLOSED_UNMERGED
#870 head a87904047032fcc8c20b7ac7c1aac6c43d805207 = CLOSED_UNMERGED
```

# Promoted result

```text
terminal_result=SOURCE_BLOCKER
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

Accepted source advances:

```text
0xd052a0 = Qt signal body calling QMetaObject::activate
peer_static_metaobject_argument=0x30b68a0
peer_signal_index_argument=0
0x4d8670 = operator new(unsigned long), not Qt connection primitive
serialized queue object = exact 16-byte GameclientMessage pair
queue insertion target=0xbd24a0
unique owned drain candidate=0xbd2190
```

Withheld boundaries remain:

```text
peer class owner=UNKNOWN
actual Qt connection primitive=UNKNOWN
sender/receiver direction=UNKNOWN
causal signal -> sendLogin binding=NOT_PROVEN
0xbd2190 causal consumption of exact queued GameclientMessage=NOT_PROVEN
final queue/TCP writer=UNKNOWN
```

# Next source tasks

Exactly two independent source-only discriminators are justified and may run in parallel:

```text
OTC-BE4F48-SENDLOGIN-PEER-METAOWNER
OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION
```

Neither may touch Track B PR #284 or use runtime, OCR/Vision, credentials, packet capture, official-client execution or official-service E2E.

next_action: register the two repository-owned prompts/aliases from fresh trusted main, then allow separate agents to claim them independently.
