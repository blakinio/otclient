---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: investigating
phase: researcher-closeout
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: 6071b237d70a11ab10e5050cc23730162b0e7e0b
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-002
session_role: researcher
execution_mode: chat_github
execution_reason: static and causal runtime discovery are complete; runtime authority has been dropped and the Draft is awaiting exact-head checks plus independent coordinator review
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
invocation_started_at: 2026-08-19T07:19:00+02:00
updated_at: 2026-08-19T08:31:00+02:00
last_progress_at: 2026-08-19T08:31:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: researcher_final_closeout
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 1
heavy_validation_runs: 6
stale_takeover_count: 0
human_interruptions: 0
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
owner_authorization_source: "owner continuation instruction on 2026-08-19: dokoncz zadanie"
---

# OTC-20260819 Track A UI/settings research closeout

## Delivery state

```yaml
STATUS: DRAFT_NOT_PROMOTED
ALIAS: TIBIA-RE-UI-SETTINGS
TASK_ID: OTC-20260819-track-a-ui-settings-static-model
DRAFT_PR: 544
BASE_MAIN: 6071b237d70a11ab10e5050cc23730162b0e7e0b
RESEARCHER_RUNTIME_ACCESS: none
RESEARCHER_MUTATION_AUTHORITY: false
E2E: PASS_FOR_MASTER_VOLUME_PERSISTENCE_PATH
CANONICAL_PROMOTION: NOT_PERFORMED
```

The researcher has finished both the static settings model and one full causal reversible persistence experiment. This task remains active only for independent coordinator/fresh-validator review; the researcher must not merge or self-promote the coverage matrix.

## Exact current-client fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

## Completed experiments

1. Current-package static settings census and high-level model recovery.
2. Static `clientoptions.json` and `QSettings` xref/callsite discriminators.
3. Action-bar/hotkey/multi-action/cooldown static refresh for H07-H09.
4. Fullscreen/`Alt+Return` runtime candidate with dynamic cache false-positive rejection.
5. Positive pre-login **Master Volume** causal persistence experiment on a task-owned isolated Synology display/HOME.

## FACTS

Static evidence established dedicated current-build H07-H13 model/controller surfaces, `TClientOptions`, `EClientOption`, one `clientoptions.json` literal with 38 decoded executable references, four used `QSettings` read/write/group targets and 51 direct callsites.

The positive runtime experiment ran against `main@5940913a325288cfd9985be54af1a56b65e5560e` before later non-overlapping minimap promotion #551. It used runner `synology-otclient-01`, machine `bc3917480db1`, a fresh task-owned HOME and display `:271`, no canonical session, no login and no credentials.

Causal sound-setting chain proven:

```text
Options / Sound / Master Volume 100%
-> real slider write 43%
-> immediate UI readback 43%
-> OK commit
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume = 43
-> options.soundMasterVolumeOld = 43
-> clean restart with same HOME
-> UI readback Master Volume 43%
-> inverse slider write 100%
-> OK commit
-> both fields = 100
-> clean second restart
-> final UI readback Master Volume 100%
-> both fields = 100
```

The copied `clientoptions.json` baseline was size 158761 / SHA256 `b545e59f01e908b12c878753b0f49514854c601d5e83159a5da8d0ae8b491251`. The first 43% `OK` commit produced size 158758 / SHA256 `d84081c78d634ca69897dd3eb15a5257f1445b3ba7f034e4fd449275e0538309`. Whole-file hashes later changed because the client performs additional normal bookkeeping; semantic persistence is therefore anchored to the exact option fields plus UI readback rather than whole-file equality.

Final cleanup returned:

```text
UI_SETTINGS_MANUAL_MARKER_PROCESS_COUNT=0
UI_SETTINGS_MANUAL_ROOT_CLEANED=true
UI_SETTINGS_MANUAL_DISPLAY_CLEANED=true
UI_SETTINGS_V2_CLEANUP=COMPLETE
UI_SETTINGS_HOST_SCREENSHOT_TEMP_CLEANUP=COMPLETE
```

Temporary runtime observation images were deleted and are not repository artifacts.

## DISPROVEN OR SUPERSEDED

`Alt+Return`/fullscreen is **DISPROVEN as a persistence discriminator for this pre-login isolated state**. Run `32221978132`, physical job `95974034787`, sent real input against the exact current client but, after excluding `/cache/`, emitted `UI_SETTINGS_V5_POST_STOP_CANDIDATE_DELTA_COUNT=0` and `UI_SETTINGS_V5_SEMANTIC_NEGATIVE=NO_PERSISTENCE_CANDIDATE_DELTA_AFTER_ALT_RETURN_AND_CLIENT_STOP`.

Earlier V5 restart-stable JSON candidates were all dynamic `packages/Tibia/cache/` files and were rejected as false positives. V1/V2/V3/V4 harness failures were pre-semantic or observer defects and are not settings claims. Their temporary workflows have been removed from the branch.

## INFERENCES

The positive Master Volume path is strong runtime evidence for H11 audio settings and H14 options persistence. It proves that `packages/Tibia/conf/clientoptions.json` is a real persistence sink for at least this concrete sound option, resolving that relationship for this setting.

## UNKNOWN

This proof does not establish that all H10-H13 settings use `clientoptions.json`, that all save timing matches `OK`, or the complete profile/migration/character-specific/QSettings relationship. H10/H12/H13 require setting-specific runtime evidence before broad completion claims.

## Durable evidence

- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md`

## Researcher final boundary

No further physical runtime action is authorized from this researcher state. The next action is exact-head CI/governance, then a **fresh coordinator/validator** must independently inspect this Draft, falsify the high-impact H11/H14 claims, decide canonical matrix updates, archive/close the task and merge only through coordinator authority.
