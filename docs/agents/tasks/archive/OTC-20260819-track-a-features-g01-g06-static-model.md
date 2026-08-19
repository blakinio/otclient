---
task_id: OTC-20260819-track-a-features-g01-g06-static-model
status: completed
session_role: released
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_capability_census
phase: closed
source_pr: 557
source_branch: research/OTC-20260819-track-a-features-g01-g06-static-model
source_head: 91e2d2bf4e082a9ba487fbc5dc3927faea2f4081
source_disposition: closed_unmerged_superseded
coordinator_review: 4971413034
coordinator_decision: REJECT_SUPERSEDE
open_material_findings_after_review: 0
promotion_pr: NOT_APPLICABLE
promotion_merge: NOT_APPLICABLE
superseding_current_build_source_pr: 560
superseding_current_build_promotion_pr: 564
superseding_current_build_promotion_merge: b239158a609d4b813b3f979580954e5ed28faac8
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gui_input_authorized: false
gameplay_allowed: false
transaction_authorized: false
physical_e2e_required: false
canonical_coverage_modified_by_this_task: false
G01_terminal_status: PARTIAL
G02_terminal_status: PARTIAL
G03_terminal_status: NOT_STARTED
G04_terminal_status: PARTIAL
G05_terminal_status: PARTIAL
G06_terminal_status: PARTIAL
ownership_released: true
---

# TIBIA-RE-FEATURES G01-G06 — terminal superseded archive

## Disposition

The bounded researcher package in source PR #557 is terminal and ownership is released. The source was closed unmerged as superseded after coordinator review `4971413034` classified it `REJECT/SUPERSEDE`.

This disposition does not falsify the retained historical facts in the source package. It means the package should not be promoted as a standalone canonical snapshot because it only re-indexed already-retained primary evidence and its current-build framing became stale before coordinator review.

## Why it is superseded

The source recommended no canonical status change:

```text
G01 keep NOT_STARTED
G02 keep PARTIAL
G03 keep NOT_STARTED
G04 keep NOT_STARTED
G05 keep NOT_STARTED
G06 keep NOT_STARTED
```

After the source was produced, later current-build source #560 was independently audited and cleanly promoted through #564. That canonical current-build result moved:

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

The source package's statement that PR #555 was unmerged/current-build authority unknown is also historical and no longer current.

G02 remains `PARTIAL` from existing structural evidence. G03 remains `NOT_STARTED`; #557 did not establish a concrete dispatch/storage/live/current-build causal edge that would justify changing it.

## Preserved evidence boundary

The source correctly preserved these fail-closed boundaries and they remain valid:

```text
semantic_dispatcher_edge_from_retained_handler_xrefs = NOT_PROVEN
outbound_action_to_wire_serialization = NOT_PROVEN
inbound_message_to_storage_mutation = NOT_PROVEN
storage_to_controller_causality = NOT_PROVEN
live_GUI_semantics = NOT_TESTED
server_acceptance = NOT_TESTED
```

No runtime, credentials, GUI input, gameplay, transaction or client mutation occurred in this task or its closeout.

## Programme effect

This task makes no new shared coverage-matrix edit. Current canonical G01-G06 row statuses must be derived from current promoted evidence on `main`, not from the stale source snapshot.
