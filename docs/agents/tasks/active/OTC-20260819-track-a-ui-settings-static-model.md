---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: implementing
phase: runtime-persistence-proof
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: e2c1fa0af020c83a992652a50391d48b85aa111e
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-002
session_role: runtime_researcher
execution_mode: github_actions_synology
execution_reason: owner requested completion; static research is complete and the remaining H10/H14 acceptance discriminator is one bounded reversible UI persistence experiment
decomposition_decision: phased
decomposition_reason: v1 failed before client identity; v2 fixed identity and proved a real current-client window but xdotool failed to load libxdo before any key event; v3 repairs only that loader boundary
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
invocation_started_at: 2026-08-19T07:19:00+02:00
updated_at: 2026-08-19T07:45:00+02:00
last_progress_at: 2026-08-19T07:45:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime_persistence_probe_v3
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 1
heavy_validation_runs: 5
stale_takeover_count: 0
human_interruptions: 0
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260819-track-a-ui-settings-static-model
runtime_namespace: ui-settings-persistence-ephemeral
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
persistent_session_role: none
physical_e2e_required: true
owner_authorization_source: "owner continuation instruction on 2026-08-19: dokoncz zadanie"
---

# OTC-20260819 Track A UI/settings model and persistence proof

## Authority and current main

The owner invoked `TIBIA-RE-UI-SETTINGS` and then requested `dokoncz zadanie`. The alias package is canonical after #543. Current trusted base for this continuation is `main@e2c1fa0af020c83a992652a50391d48b85aa111e`; the advance from `f41102ca88f152d6e0bc502d72455354db536334` is #547's independently promoted economy-panel static census and does not overlap this task's settings/runtime paths or authority.

The promoted UI-settings mission requires settings recovery through reversible write and reload/restart persistence where authority permits, with exact before/after, shared input serialization and rollback. This researcher remains Draft-only and cannot self-promote or merge.

## Runtime admission

```yaml
EXECUTION_CLASS: synology_physical_runtime
RUNTIME_ACCESS: ephemeral_isolated
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: true
runtime_owner_task: OTC-20260819-track-a-ui-settings-static-model
runtime_namespace: ui-settings-persistence-ephemeral
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
```

No canonical registration/lease/Kasm session/login/gameplay state may be read or mutated. Runtime children unset `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. No login, character selection, gameplay, purchase, transfer, shared-package mutation or network-setting mutation is authorized. Any GUI stimulus must hold `/tmp/otclient-track-a-gui-input.lock`.

## Exact current-client fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

Only a source package matching the exact current client size/SHA may be copied read-only into the task-owned HOME.

## Causal experiment

Selected setting: current-build default action `Alt+Return` / `ToggleFullscreen`. It requires no account/login state and has an exact inverse. Acceptance is:

```text
empty isolated display
-> unique exact client identity
-> baseline window size
-> shared input lock + one Alt+Return
-> changed window size readback
-> restart same isolated HOME
-> toggled size reproduced
-> shared lock + inverse Alt+Return
-> baseline size restored
-> second restart
-> baseline size reproduced
-> task-owned cleanup
```

Candidate config files may be compared by path/size/hash only; contents are not emitted.

## Physical attempt v1 — harness failure before semantic stimulus

Run `32219692697`, admission job `95967731308` SUCCESS, physical job `95967768412` FAILURE. Exact current source package, WARP, copied-client fence and empty isolated Xvfb display all passed; cleanup completed. The harness assumed the launcher-returned PID was the durable client and failed before proving a client window. No input marker was reached.

## Physical attempt v2 — client/window proved, input not sent

Run `32220128284`, admission job `95968925444` SUCCESS, physical job `95968964315` FAILURE. Direct verified facts:

```text
UI_SETTINGS_V2_LIVE_MAIN=f41102ca88f152d6e0bc502d72455354db536334
UI_SETTINGS_V2_RUNTIME_ACCESS=ephemeral_isolated
UI_SETTINGS_V2_CANONICAL_STATE_ACCESS=NONE
UI_SETTINGS_V2_CREDENTIALS_USED=false
UI_SETTINGS_V2_LOGIN_ATTEMPTED=false
UI_SETTINGS_V2_GAMEPLAY_ATTEMPTED=false
UI_SETTINGS_V2_CURRENT_EXACT_SOURCE_PACKAGE=PASS
UI_SETTINGS_V2_WARP=PASS
UI_SETTINGS_V2_COPIED_CLIENT_FENCE=PASS
UI_SETTINGS_V2_XVFB_EMPTY_DISPLAY=PASS
UI_SETTINGS_V2_CLIENT_START_1=PASS;PID=15458;START_TICKS=73673731
UI_SETTINGS_V2_BASELINE_WINDOW_SIZE=1020x650
```

The intended input command then failed twice before key injection because `/work/_otclient_tibia_re_state/toolroot/usr/bin/xdotool` could not load `libxdo.so.3`. The later `FULLSCREEN_TOGGLE_NO_OBSERVABLE_SIZE_CHANGE` refusal is therefore a harness consequence, not a semantic result. Cleanup completed. **No setting was changed in v2.**

Repair v3: require `libxdo.so.3` inside the contained toolroot, export its resolved directory plus contained library directories to `LD_LIBRARY_PATH`, prove `xdotool version` before launching the experiment, then execute the already-pinned v2 physical body. No other causal logic is changed.

The first v3 admission run `32220443981` failed closed before runtime because `main` advanced from `f41102ca...` to `e2c1fa0a...` via non-overlapping #547. This task record refreshes the base; that admission failure performed no physical job.

## Completed static phase

Durable evidence:

- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`

Current-build static facts include dedicated H07-H13 action-bar/hotkey/multi-action/cooldown/graphics/sound/interface/gameplay models, `TClientOptions`/`EClientOption`, one `clientoptions.json` literal with 38 decoded code references, four used `QSettings` read/write/group PLT targets and 51 direct callsites. Static evidence alone did not establish high-level persistence semantics.

## Owned paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `.github/workflows/tibia-official-client-re-ui-settings-persistence.yml` (retired v1; temporary)
- `.github/workflows/tibia-official-client-re-ui-settings-persistence-v2.yml` (retired v2; temporary)
- `.github/workflows/tibia-official-client-re-ui-settings-persistence-v3.yml` (active repaired discriminator; temporary)
- `docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**`

Existing native-login/action-protocol/worldmap/player-position/full-client-matrix owned paths remain untouched.

## Checkpoint

```yaml
STATUS: RUNTIME_PROOF_V3_READY
ALIAS: TIBIA-RE-UI-SETTINGS
TASK_ID: OTC-20260819-track-a-ui-settings-static-model
DRAFT_PR: 544
BASE_MAIN: e2c1fa0af020c83a992652a50391d48b85aa111e
V1_RUN: 32219692697
V1_RESULT: HARNESS_FAILURE_BEFORE_CLIENT_IDENTITY
V2_RUN: 32220128284
V2_RESULT: EXACT_CLIENT_AND_BASELINE_PROVEN; XDOTOOL_LOADER_FAILURE_BEFORE_ANY_INPUT
CURRENT_EXACT_SOURCE_ON_SYNOLOGY: PROVEN
CURRENT_RUNTIME_ACCESS: ephemeral_isolated
CANONICAL_STATE_ACCESS: NONE
LOGIN_ALLOWED: false
CREDENTIALS_ALLOWED: false
GAMEPLAY_ALLOWED: false
SHARED_SOURCE_PACKAGE_MUTATION_ALLOWED: false
V3_REPAIR: contained libxdo loader path only; causal experiment unchanged
RESTORE_REQUIREMENT: final restart must reproduce baseline window size before cleanup
BLOCKERS: []
NEXT_ACTION: rerun v3 through pull_request synchronization against current main; persist terminal semantic evidence; never interpret v1/v2 harness failures as settings semantics
```
