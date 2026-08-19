---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: validating
phase: coordinator-ready-gate
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: cf90b84442dda730bdab93d8aa9f3236b7532ad8
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_role: coordinator
execution_mode: chat_github
execution_reason: independent coordinator audit accepted the bounded slice with one repaired fullscreen-evidence classification; all final exact-head checks now pass
context_pressure: medium
context_growth: stable
estimate_confidence: high
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
final_coordinator_review: 4969851468
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
final_validated_head: 7f4d62be2e788f6e6ac6bf4beb568bc85c350c1e
final_governance_run: 32230632072
final_ci_run: 32230632291
final_static_model_run: 32230632118
final_static_model_job: 95999452908
---

# OTC-20260819 Track A UI/settings coordinator checkpoint

## Accepted delivery

`TIBIA-RE-UI-SETTINGS` has a bounded current-build evidence slice accepted by the coordinator with one corrected negative-control classification.

Accepted scope:

1. dedicated current-public-package static model evidence for H07-H14;
2. exact static `clientoptions.json` xrefs and used `QSettings` callsites;
3. lower-priority current-build refresh signals for selected H02/H04/H05/H06/H15/H18 surfaces;
4. one causal reversible Master Volume persistence experiment in a task-owned `ephemeral_isolated` runtime;
5. bounded negative-control/harness evidence from earlier fullscreen attempts.

The researcher has dropped runtime authority. No further physical operation belongs to this closeout.

## Exact current-build fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

## FACT — static evidence

Final exact-head static run `32230632118`, job `95999452908`, independently reproduced:

```text
UI_SETTINGS_PACKED_SIZE=10214529
UI_SETTINGS_PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
UI_SETTINGS_CLIENT_SIZE=52109920
UI_SETTINGS_CLIENT_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UI_SETTINGS_KEYS_CLIENTOPTIONS_LITERAL_COUNT=1
UI_SETTINGS_KEYS_CLIENTOPTIONS_LITERAL_VA=0x20d2406
UI_SETTINGS_KEYS_QSETTINGS_PLT_COUNT=4
UI_SETTINGS_KEYS_CLIENTOPTIONS_XREF_COUNT=38
UI_SETTINGS_KEYS_QSETTINGS_CALL_COUNT=51
UI_SETTINGS_KEY_ADJACENCY_SCAN=PASS
Build ID=d803d9695868713ef6ab0c3cf65f91212c9c6a62
UI_SETTINGS_PROPRIETARY_BINARY_RETAINED=false
```

The source exact-build package establishes dedicated class/model/controller surfaces for H07-H13, `TClientOptions`, `EClientOption`, one `clientoptions.json` literal with 38 decoded executable references, four used `QSettings` read/write/group PLT targets and 51 direct callsites.

This is dedicated evidence beyond broad capability-name presence but does not by itself establish setting-specific runtime semantics.

## FACT — independently verified Master Volume persistence

Independent coordinator review of primary Remote Desktop Commander command/result history proves the task-owned isolated exact client, shared GUI-input lock, baseline `clientoptions.json`, committed semantic JSON change:

```text
options.soundMasterVolume:    100 -> 43
options.soundMasterVolumeOld: 100 -> 43
```

Both values survived a clean same-HOME restart. The inverse UI commit restored both fields to `100`; a second clean restart retained `100/100`. Terminal cleanup proved zero task-marker processes and removal of the task root/display. No login or credentials were used.

Temporary visual readbacks recorded by the researcher matched the semantic chain, but temporary screenshots were deleted; durable promotion relies on the independently verified semantic JSON/restart/rollback chain plus source observation for UI text.

## Material audit correction

`UISET-AUD-001` — MEDIUM / high confidence.

The source overclaimed `Alt+Return` fullscreen persistence as `DISPROVEN`. Inspection of the pinned experiment code shows v5/v6 removed v2's immediate `await_size_change` effect proof and only scanned candidate files after sending the key.

Accepted terminal classification:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

The corrected durable evidence removes the semantic disproof claim. Open material findings after repair: `0`.

## Coverage disposition

Against PR #536's status definitions, this task supports the following **task-local** delta only:

```text
H07 NOT_STARTED -> PARTIAL
H08 NOT_STARTED -> PARTIAL
H09 NOT_STARTED -> PARTIAL
H10 NOT_STARTED -> PARTIAL
H11 NOT_STARTED -> PARTIAL  (runtime strengthened by Master Volume)
H12 NOT_STARTED -> PARTIAL
H13 NOT_STARTED -> PARTIAL
H14 NOT_STARTED -> PARTIAL  (runtime strengthened by persistence/restart/rollback)
```

No H07-H14 row is `DONE`. PR #536 shared matrix/checklist paths remain untouched.

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- all per-setting persistence sinks and Apply/OK timing;
- character-specific/global option partition;
- profile/migration versioning semantics;
- user-visible `QSettings` versus `clientoptions.json` relationship;
- fullscreen persistence semantics;
- complete H11 audio/music/ambient configuration semantics beyond the proven Master Volume path.

## Final exact-head validation

Final head before Ready transition:

```text
7f4d62be2e788f6e6ac6bf4beb568bc85c350c1e
```

Terminal checks:

```text
Track A agent runtime governance 32230632072 = SUCCESS
CI 32230632291 = SUCCESS
CI / Required = SUCCESS
Track A UI/settings static model 32230632118 = SUCCESS
static-model job 95999452908 = SUCCESS
changed paths = exactly 7 task-owned paths
review threads = 0
final coordinator review = 4969851468
open material findings = 0
```

The final workflow repair removed a GitHub-hosted `apt` infrastructure stall only. It preserved the existing evidence scan logic and pass thresholds, while adding bounded dependency/network setup; generic CI/actionlint and the static producer both passed on the repaired workflow.

## Durable evidence

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md`

## Next action

Coordinator may mark #544 Ready and squash-merge this exact accepted head. After merge, archive this task, release ownership and persist terminal source/merge evidence in a lifecycle-only closeout PR.
