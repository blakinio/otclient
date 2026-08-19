---
task_id: OTC-20260819-track-a-ui-settings-static-model
status: completed_bounded_scope
session_role: released_on_promotion_merge
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
source_pr: 544
source_branch: docs/OTC-20260819-track-a-ui-settings-static-model
source_final_head: 8f3caaf1e2655937c4dd0de69c9973a51e155bd1
source_researcher_head: 7861752c312f77fad0cde28c44c8745aa2806909
source_disposition: close_unmerged_after_promotion
coordinator_audit_review: 4969134238
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
promotion_pr: pending
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

# TIBIA-RE-UI-SETTINGS — terminal bounded-scope archive

## Accepted result

The coordinator accepts the bounded UI/settings package with one material correction (`UISET-AUD-001`). The accepted exact current official Linux client fence is:

```text
packed size:    10214529
packed SHA-256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client size:    52109920
client SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID:   d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Final source workflow generations reproduced one `clientoptions.json` literal at `0x20d2406`, 38 executable xrefs, four used `QSettings` PLT targets, 51 direct `QSettings` callsites, `UI_SETTINGS_KEY_ADJACENCY_SCAN=PASS`, and `UI_SETTINGS_PROPRIETARY_BINARY_RETAINED=false`.

## Causal Master Volume proof

Independent coordinator review of primary Remote Desktop Commander command/result history confirmed the task-owned isolated exact-client experiment:

```text
options.soundMasterVolume:    100 -> 43 -> restart 43 -> rollback 100 -> restart 100
options.soundMasterVolumeOld: 100 -> 43 -> restart 43 -> rollback 100 -> restart 100
```

The experiment held the shared GUI-input lock, used no login or credentials, and ended with zero task-marker processes plus task-root/display cleanup. Temporary visual readbacks were source observations only because their image files were deleted during cleanup.

## Material audit correction

`UISET-AUD-001` corrected the earlier fullscreen/Alt+Return interpretation. The v5/v6 observer sent `Alt+Return` and observed no non-cache candidate-file delta, but it did not retain v2's immediate window-size effect proof. Terminal classification is therefore:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

## Task-local coverage consequence

Under PR #536 status semantics, this bounded package supports:

```text
H07 NOT_STARTED -> PARTIAL
H08 NOT_STARTED -> PARTIAL
H09 NOT_STARTED -> PARTIAL
H10 NOT_STARTED -> PARTIAL
H11 NOT_STARTED -> PARTIAL  (causal Master Volume strengthening)
H12 NOT_STARTED -> PARTIAL
H13 NOT_STARTED -> PARTIAL
H14 NOT_STARTED -> PARTIAL  (causal persistence/restart/rollback strengthening)
```

No H07-H14 row is `DONE`. PR #536 shared matrix/checklist paths are not modified by this task.

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- complete H11 audio/music/ambient semantics beyond Master Volume;
- all per-setting persistence sinks and Apply/OK timing;
- character-specific versus global option partition;
- profile/migration versioning semantics;
- user-visible `QSettings` versus `clientoptions.json` relationship;
- fullscreen persistence semantics.

## Source validation and promotion rationale

The source Draft accumulated 43 commits from old base `a1368bb...` and was 10 commits behind trusted `main`, causing repository rules requiring an up-to-date branch to reject merge despite green required checks. Rather than force-rewrite researcher history, coordinator promotion restacks only the six accepted durable workflow/evidence blobs plus this archive record onto current trusted `main` as a clean one-commit promotion.

Source evidence remains auditable in PR #544 and source review `4969134238`. Ownership release becomes effective only when the clean promotion merges. A lifecycle-only follow-up may replace the pending promotion PR/merge placeholders with terminal facts.