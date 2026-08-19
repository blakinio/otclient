---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: validating
phase: coordinator-required-check-gate
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: 34e41a04d62e642ef0ae67c79354f183473270a3
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_role: coordinator
execution_mode: chat_github
execution_reason: accepted evidence is unchanged; branch protection requires CI / Required on the current merge-ref after lifecycle-only #561 advanced main
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
source_pr: 544
source_researcher_head: 7861752c312f77fad0cde28c44c8745aa2806909
coordinator_review: 4969134238
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
---

# OTC-20260819 Track A UI/settings coordinator required-check gate

## Accepted result

The bounded `TIBIA-RE-UI-SETTINGS` evidence slice remains accepted with one corrected negative-control classification. This synchronization changes only the task checkpoint so GitHub can attach required checks to the current merge-ref. No research conclusion, product code, runtime authority or #536 path is changed.

Accepted evidence:

- dedicated exact-current-build H07-H14 settings/model/controller package;
- one `clientoptions.json` literal plus decoded executable xrefs;
- used `QSettings` read/write/group callsites;
- selected lower-priority H02/H04/H05/H06/H15/H18 static refresh signals;
- one causal reversible Master Volume persistence experiment in a task-owned isolated runtime.

## Exact build fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

Repaired static producer evidence remains:

```text
clientoptions.json literal count = 1 at 0x20d2406
clientoptions executable xrefs = 38
QSettings PLT targets = 4
QSettings direct callsites = 51
UI_SETTINGS_KEY_ADJACENCY_SCAN=PASS
UI_SETTINGS_PROPRIETARY_BINARY_RETAINED=false
```

## Master Volume causal proof

Independent coordinator verification of primary Remote Desktop Commander command/result history confirms:

```text
options.soundMasterVolume:    100 -> 43 -> restart 43 -> rollback 100 -> restart 100
options.soundMasterVolumeOld: 100 -> 43 -> restart 43 -> rollback 100 -> restart 100
```

The isolated exact client/HOME/display used the shared GUI-input lock, no login and no credentials. Terminal cleanup proved zero task marker processes and removal of task root/display.

## UISET-AUD-001

Fullscreen/Alt+Return v6 remains correctly classified:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

Open material findings after repair: `0`.

## Task-local coverage

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

No H07-H14 row is `DONE`. PR #536 shared matrix/checklist paths remain untouched.

## Current-main / required-check state

The source was revalidated after #555 current-client-fence/governance merge on head `7f1c2b6def08546dc3f8e847189c7b10f252c16b`:

```text
Track A governance 32231395685 = SUCCESS
CI 32231395843 / CI Required = SUCCESS
Track A UI/settings static model 32231395688 = SUCCESS
```

After those runs, #561 advanced `main` to `34e41a04d62e642ef0ae67c79354f183473270a3`. #561 changes exactly three current-client-fence lifecycle paths and is semantically disjoint from #544; it does not modify governance/contracts or any #544 path.

An expected-head merge attempt was correctly rejected by repository rules because `CI / Required` was expected for the new merge-ref. This checkpoint is therefore the minimal safe synchronize action to generate required checks against `main@34e41a04...`.

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- complete H11 semantics beyond Master Volume;
- all per-setting persistence sinks and save timing;
- character/global option partition;
- profile/migration versioning;
- QSettings/clientoptions relationship;
- fullscreen persistence semantics.

## Durable paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md`

## Next action

Freeze the resulting head. Wait for exact-head governance, `CI / Required`, and static-model success against `main@34e41a04...`. If all pass and main has no new material governance/overlap change, squash-merge #544 with expected-head guard. Then archive this task and release ownership in a lifecycle-only closeout PR.
