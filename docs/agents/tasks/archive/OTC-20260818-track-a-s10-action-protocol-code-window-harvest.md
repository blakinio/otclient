---
task_id: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
status: completed
session_role: released
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
phase: closed
source_pr: 539
source_branch: docs/OTC-20260818-track-a-s10-action-protocol-code-window-harvest
source_head: ac34c2f906e834ace414f8c8d8fa75a150b4b65a
source_disposition: closed_unmerged_superseded
coordinator_review: 4970899448
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: 5ce628b7e565eb17876b76305af6a6086ed7f258
promotion_pr: 571
promotion_head: c4ba046bd9eb3b5999b9fbfba1c722c48eddfbb2
promotion_merge: b63ba927ec341b58c246a4e44ffb6d3cffe23e08
promotion_merge_method: squash
promotion_changed_paths: 3
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32240754268
promotion_ci_result: SUCCESS
promotion_review: 4970916936
promotion_review_threads_open: 0
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: retained historical static evidence only; no official-client runtime operation was part of S10
ownership_released: true
---

# Track A S10 — terminal action/protocol retained-evidence archive

## Terminal disposition

The bounded S10 retained-evidence discriminator is completed and ownership is released.

Source PR #539 was preserved as provenance and closed unmerged as superseded after clean coordinator promotion #571 squash-merged as:

```text
b63ba927ec341b58c246a4e44ffb6d3cffe23e08
```

## Canonical S10 result

```yaml
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
S10_RESULT: BLOCKED_MISSING_RETAINED_CODE_WINDOW
H1_MOVEOBJECT_SENDER: PROVEN_HISTORICAL_EXACT_BUILD
H2_ACTION_SPECIFIC_CONNECT_EDGE: UNKNOWN
H3_PROTOCOL_OWNER_AND_MOVEOBJECT_BUILDER: PROVEN_HISTORICAL_EXACT_BUILD
CURRENT_BUILD_OFFSETS: UNKNOWN
RUNTIME_EFFECT_BY_S10: NOT_OBSERVED
```

The blocker means the retained historical corpus is insufficient to prove the specific action-identity-preserving connect/dataflow edge; it does not disprove that the connection exists.

## Historical exact-build fence

Every executable address in S10 remains valid only for:

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

No S10 address is a current-build offset.

## Accepted evidence boundary

```text
TContainerGameActionHandler::sendMoveObject
  QMeta signal index 1 / signal-emission wrapper              PROVEN historical

TContainerGameActionHandler::<some signal>
  -> TInternalGameActionRouter 0x8332d0                      PROVEN historical

TProtocolMessageQueue::sendMoveObject
  QMeta index 218
  -> case 0xdf6d58
  -> builder 0xbd3be0
  -> internal GameclientMessage discriminator 0x78           PROVEN historical
```

The corrected retained `QObject::connectImpl` reconstruction explicitly does not establish the sender pointer-to-member signal index at the proven Container connection site. Therefore it cannot specifically bind `sendMoveObject` signal index 1 to that router/queue path without inference.

`0x78` remains an internal message discriminator, not a final wire opcode/byte.

## Independent audit and validation

Coordinator review `4970899448` independently re-read the original retained H1/H2/H3 evidence and found zero material issues.

Promotion #571 was a clean one-commit current-main promotion, `ahead_by=1`, `behind_by=0`, with three documentation/evidence/archive paths. It passed exact-head CI `32240754268`, final review `4970916936`, and had zero open review threads before merge.

## Safety / follow-up

No client execution, new client-byte acquisition, credentials, login, gameplay, process-memory access, GUI input or runtime mutation occurred in S10 or coordinator promotion/closeout.

Any future attempt to close the missing edge must use a new task and admissible current-build code/connect/dataflow evidence. Historical offsets above must not be reused as current-build facts.
