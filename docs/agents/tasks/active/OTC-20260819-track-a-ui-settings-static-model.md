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
base_main: f41102ca88f152d6e0bc502d72455354db536334
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-002
session_role: runtime_researcher
execution_mode: github_actions_synology
execution_reason: owner requested completion; static research is complete and the remaining H10/H14 acceptance discriminator is one bounded reversible UI persistence experiment
decomposition_decision: phased
decomposition_reason: run 32219692697 proved current exact source availability and isolated admission but exposed a pre-semantic client-process-selection harness defect; repair only that discriminator before retry
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
invocation_started_at: 2026-08-19T07:19:00+02:00
updated_at: 2026-08-19T07:35:00+02:00
last_progress_at: 2026-08-19T07:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime_persistence_probe_v2
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 1
heavy_validation_runs: 4
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

## Authority and live-state refresh

The owner invoked `TIBIA-RE-UI-SETTINGS` and then explicitly requested `dokoncz zadanie`. The alias package is now promoted on current `main` by merge `b6d4a3276d17c926c5840f82521571fdfaa126a0` (#543); its task archive is current `main@f41102ca88f152d6e0bc502d72455354db536334` (#548). The promoted mission requires settings recovery through reversible write and reload/restart persistence where authority permits, exact before/after and rollback, with shared GUI-input serialization.

This researcher remains Draft-only and does not promote or merge its own claims. The runtime experiment is task-owned `ephemeral_isolated`, not canonical reuse/bootstrap/rebind.

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

No canonical Track A registration, lease, KasmVNC session, login session or gameplay state may be read or mutated. Runtime children must unset `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. No account login, character selection, world entry, purchase, transfer, network-setting mutation or shared-package mutation is authorized.

Any GUI stimulus in the physical retry must hold `/tmp/otclient-track-a-gui-input.lock` for the shortest practical interval even though the target display/HOME are isolated.

## Exact current-client fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

The task may only read and copy a source package matching that exact size/SHA into its run-specific HOME. It must never update or patch the shared source package.

## Causal experiment

Selected setting: promoted current-build default action `Alt+Return` / `ToggleFullscreen`. This is used because it has a direct observable X11 before/after state without login. The experiment has a tested inverse operation and must fail closed unless the final restart returns to the exact baseline window size.

Required chain:

```text
empty isolated display
-> exact current client identity
-> baseline window size
-> acquire shared input lock
-> one Alt+Return
-> changed window size readback
-> release lock
-> restart same isolated HOME
-> toggled size reproduced
-> acquire lock
-> inverse Alt+Return
-> baseline size restored
-> release lock
-> restart same isolated HOME
-> baseline size reproduced
-> task-owned cleanup
```

Config/settings candidate paths may be compared by path/size/hash only; contents are not emitted.

## First physical attempt — negative harness control

Workflow run `32219692697`:

- admission job `95967731308`: **SUCCESS**;
- physical runner: `synology-otclient-01`;
- physical job `95967768412`: **FAILURE before semantic stimulus**;
- cleanup: `UI_SETTINGS_RUNTIME_CLEANUP=COMPLETE`.

Verified facts before that failure:

```text
UI_SETTINGS_RUNTIME_ACCESS=ephemeral_isolated
UI_SETTINGS_CANONICAL_STATE_ACCESS=NONE
UI_SETTINGS_CREDENTIALS_USED=false
UI_SETTINGS_LOGIN_ATTEMPTED=false
UI_SETTINGS_GAMEPLAY_ATTEMPTED=false
UI_SETTINGS_TOOLROOT=/work/_otclient_tibia_re_state/toolroot
UI_SETTINGS_CURRENT_EXACT_SOURCE_PACKAGE=PASS
UI_SETTINGS_WARP=PASS
UI_SETTINGS_COPIED_CLIENT_FENCE=PASS
UI_SETTINGS_XVFB_EMPTY_DISPLAY=PASS
```

No `UI_SETTINGS_CLIENT_START_1=PASS`, baseline window, or input marker was emitted. Therefore the failure is **not** semantic evidence against fullscreen persistence. The v1 harness used the launcher-returned PID as if it were necessarily the durable exact client process and exited under `set -e` before explaining which identity assertion failed.

Repair hypothesis for v2: launch once, then scan only marker-owned processes and select exactly one process whose `/proc/PID/exe`, size and SHA match the copied exact client. Zero or multiple exact candidates fail closed with a sanitized client-log tail. This is a new discriminator, not an identical retry.

## Completed static phase

Durable evidence remains under:

- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`

Current exact-build static facts include dedicated H07-H13 action-bar/hotkey/multi-action/cooldown/graphics/sound/interface/gameplay models, `TClientOptions`/`EClientOption`, one `clientoptions.json` literal with 38 decoded code references, four used `QSettings` read/write/group PLT targets and 51 direct callsites. Static evidence alone did not establish the high-level persistence store relationship.

## Owned paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `.github/workflows/tibia-official-client-re-ui-settings-persistence.yml` (failed v1 discriminator; temporary)
- `.github/workflows/tibia-official-client-re-ui-settings-persistence-v2.yml` (repair discriminator; temporary)
- `docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**`

Existing native-login/action-protocol/worldmap/player-position/full-client-matrix owned paths remain untouched.

## Checkpoint

```yaml
STATUS: RUNTIME_PROOF_REPAIR_READY
ALIAS: TIBIA-RE-UI-SETTINGS
TASK_ID: OTC-20260819-track-a-ui-settings-static-model
DRAFT_PR: 544
BASE_MAIN: f41102ca88f152d6e0bc502d72455354db536334
PREVIOUS_RUNTIME_RUN: 32219692697
PREVIOUS_RUNTIME_RESULT: HARNESS_FAILURE_BEFORE_SEMANTIC_STIMULUS
CURRENT_EXACT_SOURCE_ON_SYNOLOGY: PROVEN
CURRENT_RUNTIME_ACCESS: ephemeral_isolated
CANONICAL_STATE_ACCESS: NONE
LOGIN_ALLOWED: false
CREDENTIALS_ALLOWED: false
GAMEPLAY_ALLOWED: false
SHARED_SOURCE_PACKAGE_MUTATION_ALLOWED: false
REPAIR: select exactly one marker-owned exact-SHA client process instead of assuming launcher PID; serialize each input with shared GUI lock; emit explicit diagnostics on every pre-semantic refusal
RESTORE_REQUIREMENT: final restart must reproduce baseline window size before cleanup
BLOCKERS: []
NEXT_ACTION: run v2 discriminator against current-main freshness; persist terminal positive or negative evidence; do not repeat an unchanged failure
```
