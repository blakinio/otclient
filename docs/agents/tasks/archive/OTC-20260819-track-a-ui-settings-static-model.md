---
task_id: OTC-20260819-track-a-ui-settings-static-model
status: completed
session_role: released
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
task_kind: discovery
phase: closed
source_pr: 544
source_branch: docs/OTC-20260819-track-a-ui-settings-static-model
source_final_head: 8f3caaf1e2655937c4dd0de69c9973a51e155bd1
source_researcher_head: 7861752c312f77fad0cde28c44c8745aa2806909
source_disposition: closed_unmerged_superseded
coordinator_audit_review: 4969134238
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
promotion_pr: 562
promotion_branch: docs/OTC-20260819-track-a-ui-settings-promotion-v2
promotion_base: 34e41a04d62e642ef0ae67c79354f183473270a3
promotion_head: bff3df609175aa14a55967b6aea6817ecdc32848
promotion_merge: f3df2ee606058ba5ef7bec72b91f77f60eaffb59
promotion_merge_method: squash
promotion_changed_paths: 7
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32232600817
promotion_ci_result: SUCCESS
promotion_static_model_run: 32232600573
promotion_static_model_result: SUCCESS
promotion_review: 4970081454
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
ownership_released: true
---

# TIBIA-RE-UI-SETTINGS — terminal bounded-scope archive

## Terminal repository state

The bounded UI/settings package is complete and promoted.

Source researcher/coordinator PR #544 is **closed unmerged as superseded**. Its historical branch was intentionally preserved for provenance rather than force-rewritten after repository rules revealed that it was 10 commits behind trusted `main`.

Clean promotion PR #562 was created from exact trusted base `34e41a04d62e642ef0ae67c79354f183473270a3` as a one-commit restack containing the six exact coordinator-accepted workflow/evidence blobs plus this archive record.

```text
promotion head:  bff3df609175aa14a55967b6aea6817ecdc32848
ahead_by:        1
behind_by:       0
changed paths:   7
CI:              32232600817 = SUCCESS
static model:    32232600573 = SUCCESS
review:          4970081454
review threads:  0
merge:           f3df2ee606058ba5ef7bec72b91f77f60eaffb59
merge method:    squash
```

No ruleset bypass, force-push, login, credential use, gameplay or additional runtime mutation was used for promotion or closeout.

## Accepted exact-build evidence

The coordinator accepts the exact current official Linux client fence:

```text
packed size:    10214529
packed SHA-256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client size:    52109920
client SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID:   d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Final producer generations reproduced:

```text
clientoptions.json literal count = 1 at 0x20d2406
clientoptions executable xrefs = 38
QSettings PLT targets = 4
QSettings direct callsites = 51
UI_SETTINGS_KEY_ADJACENCY_SCAN = PASS
UI_SETTINGS_PROPRIETARY_BINARY_RETAINED = false
```

## Causal Master Volume proof

Independent coordinator review of primary Remote Desktop Commander command/result history confirmed the task-owned isolated exact-client persistence chain:

```text
options.soundMasterVolume:    100 -> 43 -> restart 43 -> rollback 100 -> restart 100
options.soundMasterVolumeOld: 100 -> 43 -> restart 43 -> rollback 100 -> restart 100
```

The experiment held the shared GUI-input lock, used no login or credentials, and ended with zero task-marker processes plus task-root/display cleanup. Temporary visual readbacks remain source observations only because their image files were deleted during cleanup.

## Material audit correction

`UISET-AUD-001` corrected the earlier fullscreen/Alt+Return interpretation. The v5/v6 observer sent `Alt+Return` and observed no non-cache candidate-file delta, but it did not retain v2's immediate window-size effect proof.

Terminal classification:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

Coordinator source audit review: `4969134238`. Open material findings after repair: `0`.

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

No H07-H14 row is `DONE`. PR #536 shared matrix/checklist paths were not modified.

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- complete H11 audio/music/ambient semantics beyond Master Volume;
- all per-setting persistence sinks and Apply/OK timing;
- character-specific versus global option partition;
- profile/migration versioning semantics;
- user-visible `QSettings` versus `clientoptions.json` relationship;
- fullscreen persistence semantics.

## Ownership release

Task ownership is released. Current task authority is `runtime_access: none` and `mutation_authorized: false`. Any future UI/settings runtime work requires a separately admitted task and fresh trusted-base validation.