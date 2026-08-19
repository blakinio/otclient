---
task_id: OTC-20260819-track-a-features-static-g0
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
source_pr: 560
source_branch: research/OTC-20260819-track-a-features-static-model
source_head: 2822de1bc916a581de5aa3eb0601c1708c468b39
source_disposition: close_unmerged_after_promotion
coordinator_review: 4970396563
coordinator_decision: ACCEPT_WITH_EDITS
material_finding: FEATURE-AUD-001
open_material_findings_after_repair: 0
promotion_base: 08c0b6f89ffddd4c75b8f60060ce3b2a62195d95
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

# TIBIA-RE-FEATURES — bounded current-package static G0 archive

## Accepted scope

This task promotes one bounded current-public-package structural slice of the wider `TIBIA-RE-FEATURES` alias:

```text
G01 Cyclopedia shell/request-cache model
G04 Bestiary kills/unlocks/loot/progress
G05 Charms selection/assignment
G06 Monster Bonus Effects
```

The complete alias (`G01-G23` plus `G32-G41`) remains unfinished.

## Exact package fence

```text
packed SHA-256:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size:    52109920
unpacked SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

Current trusted fence authority is PR #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus lifecycle closeout #561. The source task's reference to PR #551 as the public-package-fingerprint dependency was incorrect and is superseded by this archive.

## Independent audit

Coordinator review `4970396563` classified source #560 `ACCEPT_WITH_EDITS`.

The raw GitHub Actions artifact was independently downloaded and its ZIP SHA-256 reproduced exactly as GitHub metadata:

```text
779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
```

The four inner evidence hashes also reproduced exactly. The QMeta producer methodology was independently reviewed and does not promote heuristic per-method targets or semantic dispatcher edges.

Open material findings after the provenance repair: `0`.

## Accepted task-local coverage

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

No row is `DONE`. The canonical shared coverage matrix in PR #536 is not modified by this task.

## Evidence boundary

FACT: dedicated exact-package Qt model/controller/protocol-type surfaces exist for the four rows.

INFERENCE: those dedicated surfaces satisfy a structural `PARTIAL` threshold under the current programme status vocabulary.

UNKNOWN: generated field schemas, handler-to-storage causality, cache lifetime/invalidation, resource/cost formulas, server validation, persistence and live transitions.

## Safety

`runtime_access:none`; no official-client execution, login, credentials, gameplay, resource spending, GUI input, process mutation or irreversible action was performed. Physical E2E is not applicable to this static package.

## Source and promotion lifecycle

Source PR #560 remains researcher provenance and must not merge itself. Once the clean promotion merges, close #560 unmerged as superseded and set this archive to `status: completed`, `session_role: released`, `ownership_released: true` in a lifecycle-only closeout.
