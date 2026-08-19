---
task_id: OTC-20260819-track-a-creature-combat-static-g0
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
source_pr: 558
source_branch: research/OTC-20260819-track-a-creature-combat-static-g0
source_head: fa7871e7ee085601ab91a8b695e4db83f06b80e4
source_disposition: close_unmerged_after_promotion
coordinator_review: 4970526774
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: f13179df4aa99a946faf6ec9635d5d40370c6ff3
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
ownership_release_state: effective_on_promotion_merge
---

# TIBIA-RE-CREATURE-COMBAT — bounded current-package static G0 archive

## Accepted scope

This task promotes the bounded current-package static researcher package for D01-D08 and structural C15-C17 creature/combat coverage.

Only two rows change status:

```text
D06 Creature HUD names/icons/status effects      NOT_STARTED -> PARTIAL
D07 Battle-list filters/sorting/secondary lists NOT_STARTED -> PARTIAL
```

Current-package evidence corroborates D01-D05/D08/C15-C17 without changing their existing `PARTIAL` status. No row becomes `DONE`.

## Exact package fence and independent audit

```text
packed SHA-256:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
packed size:      10214529
unpacked SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size:    52109920
```

Coordinator review `4970526774` classified source #558 `ACCEPT`, with zero open material findings.

The producer artifact ZIP independently reproduced GitHub digest:

```text
d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
```

Raw QMeta, protocol-string evidence and producer methodology were independently re-read. The source correctly preserves the distinction between structural QMeta/type/template presence and causal runtime semantics.

## Evidence boundary

**FACT:** dedicated exact-current-package creature HUD and battle-list structural surfaces exist, current creature server-message/template-registration strings persist, and attack/follow generated type/action surfaces persist.

**INFERENCE:** the dedicated D06/D07 static packages satisfy `PARTIAL` under the programme status vocabulary.

**UNKNOWN:** non-QMeta dispatch, handler-to-storage mutation, authoritative live values, HUD status schemas, exact battle-list filter/sort semantics, action-to-wire-to-effect causality, server acceptance, dedicated current-build cancellation semantics and restart/relogin stability.

## Safety

`runtime_access:none`; no client execution, Synology/KasmVNC observation, login, credentials, gameplay, attack/follow input, process-memory access or client mutation. Physical E2E is not applicable to this static package.

## Lifecycle

Source PR #558 remains preserved as researcher provenance and must not merge itself. After clean promotion merges, close #558 unmerged as superseded and finalize this archive to `status: completed`, `session_role: released`, `ownership_released: true` in a lifecycle-only closeout.
