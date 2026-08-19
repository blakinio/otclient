---
task_id: OTC-20260819-track-a-features-static-g0
status: completed
session_role: released
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: closed
source_pr: 560
source_branch: research/OTC-20260819-track-a-features-static-model
source_head: 2822de1bc916a581de5aa3eb0601c1708c468b39
source_disposition: closed_unmerged_superseded
coordinator_review: 4970396563
coordinator_decision: ACCEPT_WITH_EDITS
material_finding: FEATURE-AUD-001
open_material_findings_after_repair: 0
promotion_base: 08c0b6f89ffddd4c75b8f60060ce3b2a62195d95
promotion_pr: 564
promotion_head: 9b8ef32d6c263607bc2472a7526b3d614ca0d9be
promotion_merge: b239158a609d4b813b3f979580954e5ed28faac8
promotion_merge_method: squash
promotion_changed_paths: 4
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32235952137
promotion_ci_result: SUCCESS
promotion_review: 4970434583
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
e2e_reason: static GitHub-hosted documentation/evidence promotion; no official-client runtime operation was part of this bounded task
ownership_released: true
---

# TIBIA-RE-FEATURES — terminal bounded current-package static G0 archive

## Terminal disposition

The bounded `TIBIA-RE-FEATURES` current-package static G0 slice is completed and ownership is released.

Source researcher PR #560 is preserved as provenance and was closed unmerged as superseded after coordinator promotion. Clean promotion PR #564 squash-merged to `main` as:

```text
b239158a609d4b813b3f979580954e5ed28faac8
```

The complete alias (`G01-G23` plus `G32-G41`) remains unfinished; only the four rows below were part of this task.

## Accepted scope

```text
G01 Cyclopedia shell/request-cache model
G04 Bestiary kills/unlocks/loot/progress
G05 Charms selection/assignment
G06 Monster Bonus Effects
```

Accepted task-local status delta:

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

No row is `DONE`. PR #536 shared matrix/checklist paths were not modified.

## Exact package fence

```text
packed SHA-256:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size:    52109920
unpacked SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

Current trusted fence authority is PR #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus lifecycle closeout #561. `FEATURE-AUD-001` corrected the source task's mistaken dependency pointer to PR #551; #551 is the world/minimap promotion and is not current-client fence authority.

## Independent audit and provenance

Coordinator source review `4970396563` classified #560 `ACCEPT_WITH_EDITS`.

The raw producer artifact `9356800104` from run/job `32229656311 / 95996576897` was downloaded independently. Its ZIP SHA-256 reproduced GitHub metadata exactly:

```text
779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
```

All four inner evidence hashes also reproduced exactly. Raw QMeta/protocol text and the producer workflow were independently re-read. The methodology establishes Qt metaobject/static-metacall ownership plus method/property/enum names; it does not manufacture per-method native targets or semantic dispatcher edges.

Promotion PR #564 was a clean one-commit current-main restack:

```text
base:          08c0b6f89ffddd4c75b8f60060ce3b2a62195d95
head:          9b8ef32d6c263607bc2472a7526b3d614ca0d9be
ahead_by:      1
behind_by:     0
changed paths: 4
CI:            32235952137 = SUCCESS
review:        4970434583 = PASS
threads open:  0
merge:         b239158a609d4b813b3f979580954e5ed28faac8
```

Open material findings after repair: `0`.

## Evidence boundary

**FACT:** dedicated exact-package Qt model/controller/protocol-type surfaces exist for G01/G04/G05/G06 and the raw evidence matches the promoted package fence.

**INFERENCE:** those dedicated structural surfaces satisfy `PARTIAL` under the programme status vocabulary.

**UNKNOWN:** generated request/response field schemas; handler-to-storage/controller causal writes; G01 cache ownership/lifetime/invalidation; Bestiary authoritative field ownership and tracker constraints; charm assignment/clearing validation/formulas/persistence; Monster Bonus Effect variants/resource-cost formulas/server validation/persistence; live success/error transitions, reconnect/character-switch behavior and runtime causality.

## Safety and E2E

No Synology/KasmVNC access, official-client execution, login, credentials, gameplay, resource spending, reroll, Forge/Imbuement commit, GUI input, process mutation or client-byte mutation was performed by the coordinator promotion/closeout.

Physical E2E is `NOT_APPLICABLE` because this task is a static GitHub-hosted evidence/documentation promotion.

## Lifecycle

```text
source #560:    CLOSED UNMERGED / SUPERSEDED
promotion #564: MERGED
ownership:      RELEASED
runtime_access: none
```
