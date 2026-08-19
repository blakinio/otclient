---
task_id: OTC-20260819-track-a-creature-combat-static-g0
status: completed
session_role: released
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: closed
source_pr: 558
source_branch: research/OTC-20260819-track-a-creature-combat-static-g0
source_head: fa7871e7ee085601ab91a8b695e4db83f06b80e4
source_disposition: closed_unmerged_superseded
coordinator_review: 4970526774
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: f13179df4aa99a946faf6ec9635d5d40370c6ff3
promotion_pr: 566
promotion_head: e567f5b1e44dff7a6d7764e2a5df3ba626d812ad
promotion_merge: 7213237fbd43d973f967c04d0df54a4fde08674d
promotion_merge_method: squash
promotion_changed_paths: 4
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32237054074
promotion_ci_result: SUCCESS
promotion_review: 4970547715
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: static GitHub-hosted documentation/evidence promotion with no physical official-client runtime operation
ownership_released: true
---

# TIBIA-RE-CREATURE-COMBAT — terminal bounded current-package static G0 archive

## Terminal disposition

The bounded current-package creature/combat static G0 task is completed and ownership is released.

Source researcher PR #558 was preserved as provenance and closed unmerged as superseded. Clean coordinator promotion PR #566 squash-merged to `main` as:

```text
7213237fbd43d973f967c04d0df54a4fde08674d
```

## Accepted task-local coverage

Only two rows change status:

```text
D06 Creature HUD names/icons/status effects      NOT_STARTED -> PARTIAL
D07 Battle-list filters/sorting/secondary lists NOT_STARTED -> PARTIAL
```

Current-package evidence corroborates D01-D05/D08/C15-C17 without changing their existing `PARTIAL` status. No row becomes `DONE`. PR #536 shared coverage files are untouched.

## Exact package fence and independent audit

```text
packed SHA-256:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
packed size:      10214529
unpacked SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size:    52109920
```

Coordinator source review `4970526774` classified #558 `ACCEPT`, with zero open material findings.

Producer artifact `9356949168` was independently downloaded. Its ZIP SHA-256 exactly reproduced GitHub metadata:

```text
d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
```

The archive contains exactly four compact text evidence files and no client bytes. Raw QMeta/protocol evidence and the producer methodology were independently re-read.

The producer establishes QMeta/static-metacall ownership and method names only; it does not recover per-method native targets. Current creature `registerServerMessage<...>` observations are retained as template/string-presence facts, not final runtime-dispatch proof.

## Promotion validation

Promotion #566 was a clean one-commit current-main restack:

```text
base:          f13179df4aa99a946faf6ec9635d5d40370c6ff3
head:          e567f5b1e44dff7a6d7764e2a5df3ba626d812ad
ahead_by:      1
behind_by:     0
changed paths: 4
CI:            32237054074 = SUCCESS
review:        4970547715 = PASS
threads open:  0
merge:         7213237fbd43d973f967c04d0df54a4fde08674d
```

## Evidence boundary

**FACT:** dedicated exact-current-package creature HUD and battle-list structural surfaces exist; current creature server-message/template-registration strings persist; current attack/follow generated type/action surfaces persist.

**INFERENCE:** the dedicated D06/D07 static packages satisfy `PARTIAL` under the programme status vocabulary.

**UNKNOWN:** non-QMeta dispatch; handler-to-storage mutation; authoritative live values; HUD status/icon schemas; exact battle-list filter/sort semantics and persistence; action-to-wire-to-effect causality; server acceptance; dedicated current-build cancellation semantics; restart/relogin stability.

## Safety / E2E

No client execution, Synology/KasmVNC observation, login, credentials, gameplay, keyboard/mouse input, process-memory access or client mutation was performed by the coordinator promotion/closeout.

Physical E2E is `NOT_APPLICABLE` because this task is static documentation/evidence promotion.

## Lifecycle

```text
source #558:    CLOSED UNMERGED / SUPERSEDED
promotion #566: MERGED
ownership:      RELEASED
runtime_access: none
```
