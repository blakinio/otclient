---
task_id: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
source_pr: 539
source_branch: docs/OTC-20260818-track-a-s10-action-protocol-code-window-harvest
source_head: ac34c2f906e834ace414f8c8d8fa75a150b4b65a
source_disposition: close_unmerged_after_promotion
coordinator_review: 4970899448
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: 5ce628b7e565eb17876b76305af6a6086ed7f258
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
ownership_release_state: pending_promotion_merge
---

# Track A S10 — action/protocol retained-evidence archive checkpoint

## Coordinator disposition

Source PR #539 is accepted as a bounded historical retained-evidence result. Its terminal classification remains deliberately partial:

```yaml
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
S10_RESULT: BLOCKED_MISSING_RETAINED_CODE_WINDOW
H1_MOVEOBJECT_SENDER: PROVEN_HISTORICAL_EXACT_BUILD
H2_ACTION_SPECIFIC_CONNECT_EDGE: UNKNOWN
H3_PROTOCOL_OWNER_AND_MOVEOBJECT_BUILDER: PROVEN_HISTORICAL_EXACT_BUILD
CURRENT_BUILD_OFFSETS: UNKNOWN
RUNTIME_EFFECT_BY_S10: NOT_OBSERVED
```

The blocker means the retained corpus is insufficient to prove the specific action-identity-preserving connect edge; it does not disprove that the connection exists.

## Historical exact-build fence

All executable addresses in this package are valid only for:

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

They must not be reused as current-client offsets. Current trusted executable identity is independently governed by the later `52109920 / ed5469...` fence.

## Accepted direct evidence

```text
TContainerGameActionHandler::sendMoveObject
  signal index 1 / signal-emission wrapper                    PROVEN historical

TContainerGameActionHandler::<some signal>
  -> TInternalGameActionRouter 0x8332d0                      PROVEN historical

TProtocolMessageQueue::sendMoveObject
  QMeta index 218
  -> case 0xdf6d58
  -> builder 0xbd3be0
  -> internal GameclientMessage discriminator 0x78           PROVEN historical
```

`0x78` is not a final wire opcode/byte.

The corrected retained `connectImpl` evidence does not establish the pointer-to-member signal index at the proven Container sender-metaobject site. Therefore the following remains `UNKNOWN`:

```text
TContainerGameActionHandler::sendMoveObject signal index 1
  -> exact connect receiver/member preserving action identity
  -> TProtocolMessageQueue::sendMoveObject
```

## Independent audit

Coordinator review `4970899448` re-read the original retained H1/H2/H3 evidence on the historical branch and found zero material issues. The source exact head has green CI/governance and zero review threads.

Because source #539 is 19 commits behind current main, accepted material is promoted through a clean current-main branch rather than by merging researcher history.

## Safety

`runtime_access:none`; no client execution, new client-byte acquisition, credentials, login, gameplay, process-memory access, GUI input or runtime mutation occurred in S10 coordinator review/promotion. Physical E2E is not applicable.

## Lifecycle

After the clean promotion merges, source #539 must be closed unmerged as superseded and this archive finalized to `status: completed`, `session_role: released`, `ownership_released: true` in a lifecycle-only closeout.
