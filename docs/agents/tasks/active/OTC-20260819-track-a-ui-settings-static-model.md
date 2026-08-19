---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: validating
phase: coordinator-current-main-gate
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: 2e572789a2bc4b64c5e906c4515c15c625f6bc9e
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_role: coordinator
execution_mode: chat_github
execution_reason: final accepted evidence is unchanged; current-main revalidation is required because #555 advanced Track A current-client fence and governance after the prior exact-head generation started
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

# OTC-20260819 Track A UI/settings coordinator current-main gate

## Accepted scope

The coordinator accepts the bounded `TIBIA-RE-UI-SETTINGS` evidence slice with one corrected negative-control classification. No further runtime work is authorized or required for this closeout.

Accepted evidence includes:

- dedicated current-build H07-H14 settings/model/controller evidence;
- `clientoptions.json` literal/xrefs and used `QSettings` callsites;
- selected lower-priority H02/H04/H05/H06/H15/H18 static refresh signals;
- one causal reversible Master Volume persistence experiment in a task-owned isolated runtime;
- bounded fullscreen/harness negative-control evidence.

## Exact build fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

The repaired static producer on head `7f4d62be2e788f6e6ac6bf4beb568bc85c350c1e` reproduced this exact package plus:

```text
clientoptions.json literal count = 1 at 0x20d2406
clientoptions executable xrefs = 38
QSettings PLT targets = 4
QSettings direct callsites = 51
UI_SETTINGS_KEY_ADJACENCY_SCAN=PASS
UI_SETTINGS_PROPRIETARY_BINARY_RETAINED=false
```

Runs:

```text
Track A governance 32230632072 = SUCCESS
CI 32230632291 = SUCCESS
Track A UI/settings static model 32230632118 = SUCCESS
static-model job 95999452908 = SUCCESS
```

## Master Volume causal proof

Independent coordinator review of primary Remote Desktop Commander command/result history confirmed:

```text
options.soundMasterVolume:    100 -> 43 -> restart 43 -> rollback 100 -> restart 100
options.soundMasterVolumeOld: 100 -> 43 -> restart 43 -> rollback 100 -> restart 100
```

The task used an isolated exact client/HOME/display, held the shared GUI-input lock, used no login or credentials, and ended with zero task marker processes plus task-root/display cleanup.

## UISET-AUD-001 correction

The source overclaimed the fullscreen/Alt+Return v6 result. Correct terminal classification is:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

Open material findings after repair: `0`.

## Task-local coverage disposition

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

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- complete H11 audio/music/ambient semantics beyond Master Volume;
- all per-setting persistence sinks and Apply/OK timing;
- character/global option partition;
- profile/migration versioning;
- user-visible `QSettings` versus `clientoptions.json` relationship;
- fullscreen persistence semantics.

## Current-main freshness

PR #555 merged after the previous final generation started and advanced `main` to:

```text
2e572789a2bc4b64c5e906c4515c15c625f6bc9e
```

Its 15 paths are disjoint from all 7 paths owned by #544, but #555 changes Track A governance/contracts and advances the current official-client fence. Therefore this checkpoint intentionally retriggers exact-head governance/CI/static-model against the new `main` rather than relying on pre-#555 checks.

No research claim, product code, runtime authority or #536 path changes in this synchronization.

## Durable paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md`

## Next action

Freeze the resulting head. If exact-head governance, CI and static-model all pass against `main@2e572789...`, re-check head/main/review threads and squash-merge #544 with an expected-head guard. Then move this task from active to archive and release ownership in a lifecycle-only PR.
