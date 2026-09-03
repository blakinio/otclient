---
task_id: OTC-20260903-be4f48-post869-870-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260903-be4f48-post869-870-promotion
base_branch: main
base_main: a35bbacd475a31ce52736ccbc3b5e837626def66
created: 2026-09-03T18:43:00+02:00
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
  - docs/agents/tasks/active/OTC-20260903-be4f48-post869-870-promotion.md
modules_touched: []
reuses:
  - source Draft PR #869 exact-current sender-peer evidence at cce4f0dc4f34eecb069f326681958e58a8e6585c
  - source Draft PR #870 exact-current final-writer evidence at a87904047032fcc8c20b7ac7c1aac6c43d805207
  - merged promotion #866 and lifecycle #867
blocks:
  - Track B PR #284 remains blocked from protocol mutation/E2E
---

# Objective

Promote only the independently verified exact-current facts from source Draft PRs #869 and #870, correct the previously promoted `0x4d8670` helper interpretation, preserve all UNKNOWN boundaries, and select the smallest justified next source discriminators without modifying Track B PR #284.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Acceptance

1. Revalidate source #869 exact final head/checks and promote only sanitized exact-current facts.
2. Revalidate source #870 exact final head/checks/artifact and promote only sanitized exact-current facts.
3. Correct `0x4d8670` to `operator new(unsigned long)` / `ALLOCATOR_OPERATOR_NEW`; do not retain it as a Qt connection helper.
4. Preserve `0xd052a0` only as a proved Qt signal body calling `QMetaObject::activate`, with static-metaobject argument `0x30b68a0` and signal index `0`; owner/direction remain UNKNOWN.
5. Preserve the proved 16-byte queued `GameclientMessage` identity, queue insertion target `0xbd24a0`, and unique owned drain candidate `0xbd2190`; causal consumption and final writer remain UNKNOWN.
6. Keep Field6 value UNKNOWN, complete pre-login order UNKNOWN and Track B wire delta NOT_PROVEN.
7. Do not authorize runtime, OCR/Vision, official-client execution, login, credentials, process-memory access, packet capture or official-service E2E.
8. Exact-head CI/governance and full diff review must pass before merge.
9. After merge, close source PRs #869 and #870 unmerged as consumed and archive this promotion lifecycle.
10. Register new aliases only after this promotion is on trusted `main`.

# Coordinator result

```text
terminal_result=SOURCE_BLOCKER
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

The two independently justified next source boundaries are:

```text
OTC-BE4F48-SENDLOGIN-PEER-METAOWNER
  0x30b68a0 / signal index 0 -> peer owner + actual bounded Qt connection primitive/direction

OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION
  0xbd2190 -> causal consumption of the exact queued GameclientMessage object
```

They are independent and may run in parallel after this promotion merges. Neither may touch Track B #284 or broaden into runtime/E2E.

next_action: validate this clean promotion on exact head, squash-merge, close #869/#870 unmerged as consumed, archive lifecycle, then register the two new repository-owned aliases/prompts from fresh trusted main.
