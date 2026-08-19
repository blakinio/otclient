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
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-002
session_role: runtime_researcher
execution_mode: github_actions_synology
execution_reason: owner requested completion of the same UI/settings task; the remaining acceptance gate requires one bounded real-input persistence proof on a task-owned isolated Synology display
decomposition_decision: phased
decomposition_reason: static discovery is complete; this continuation executes the smallest causal runtime persistence discriminator without using or mutating the canonical session
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
invocation_started_at: 2026-08-19T07:19:00+02:00
updated_at: 2026-08-19T07:26:00+02:00
last_progress_at: 2026-08-19T07:26:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: runtime_persistence_probe
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 1
heavy_validation_runs: 3
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

## Current objective

Continue the owner-invoked `TIBIA-RE-UI-SETTINGS` task through the remaining causal acceptance boundary. The static discovery phase is already complete. This phase is limited to one task-owned, reversible settings persistence experiment:

```text
safe read
-> reversible fullscreen toggle
-> immediate readback
-> client restart using the same isolated HOME
-> persisted-state readback
-> exact inverse toggle
-> second restart
-> restored-state readback
-> complete task-owned cleanup
```

The selected stimulus is the current-build global `Alt+Return` / `ToggleFullscreen` action recovered by the static phase. It does not require account login, character selection, world entry, gameplay, credentials, network-setting mutation, purchase, transfer or mutation of the canonical Track A runtime.

## Authority and runtime boundary

The current owner instruction explicitly requests completion of this same task. It authorizes the smallest reversible runtime action required by the task objective, subject to all trusted-base Track A safety rules.

Runtime classification for this phase:

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

The experiment MUST use a run-specific task-owned namespace, display and HOME. The physical runner must be exactly `synology-otclient-01`. No canonical lease, registration, Kasm desktop session or canonical display may be read or written. No login or secret access is allowed. The workflow unsets `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` before every child process launch.

The experiment may only **copy** a current exact official-client package from one of the trusted source-package locations into its task-owned sandbox. It MUST fail closed if the source-package `bin/client` is not the exact current package already established by static evidence:

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

The trusted-base canonical exact-client fence remains unchanged and is not reinterpreted by this task. This experiment makes no canonical identity, bootstrap or rebind claim.

## Owned paths

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `.github/workflows/tibia-official-client-re-ui-settings-persistence.yml` (one-shot physical discriminator; remove after terminal evidence capture)
- `docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**`

Existing #528 native-login, #539 action-protocol, #475 worldmap, #302 player-position, #536 coverage-matrix and #543 prompt-package paths remain non-owned and must not be edited.

## Runtime acceptance contract

The one-shot discriminator must prove all of the following or fail closed:

1. exact runner/repository/base-head admission;
2. unique task-owned namespace and initially empty selected X11 display;
3. current exact source-package client SHA/size before any copy;
4. exact copied client SHA/size inside the task sandbox;
5. task-owned WARP/SOCKS, Xvfb and contained DRI/toolroot startup without credentials;
6. exact client starts and one causally attributable large VIEWABLE window appears on the previously empty isolated display;
7. baseline window size is read before input;
8. one `Alt+Return` stimulus changes the real window size and immediate readback observes the change;
9. after terminating only the task-owned client and restarting it with the same isolated HOME, the toggled window size is reproduced;
10. one inverse `Alt+Return` restores the original window size;
11. after a second terminate/restart using the same HOME, the original window size is reproduced again;
12. bounded settings/config candidate file paths and hashes may be compared, but file contents must not be printed;
13. no credentials/login/gameplay/canonical state access occurs;
14. all task-owned client/Xvfb/WARP processes and the task namespace are cleaned on every exit path.

A failure to find a current exact source package is a **real environment blocker**, not permission to patch a shared package, mix old resources with a new binary, or use the obsolete trusted canonical binary as a substitute.

## Completed static phase

Durable evidence already present:

- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`

Verified static facts for the current package include dedicated H07-H13 action-bar/hotkey/multi-action/cooldown/graphics/sound/interface/gameplay models, `TClientOptions`/`EClientOption`, one `clientoptions.json` literal with 38 decoded code references, four used `QSettings` read/write/group PLT targets and 51 direct callsites. The static phase did not prove the high-level store relation and did not recover authoritative `QSettings` group/key names.

Static exact-head validation before this continuation was green on PR #544 head `6bf84d06e17d8838ed5ebcfbe2758499eef89171`:

- Track A governance `32195086192` = SUCCESS;
- UI/settings static model `32195086252` / `95897323380` = SUCCESS;
- repository CI `32195086335`, `CI / Required` = SUCCESS.

## Current checkpoint

```yaml
STATUS: RUNTIME_PROOF_ADMITTED_NOT_YET_EXECUTED
ALIAS: TIBIA-RE-UI-SETTINGS
TASK_ID: OTC-20260819-track-a-ui-settings-static-model
DRAFT_PR: 544
BASE_MAIN: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
STATIC_HEAD: 6bf84d06e17d8838ed5ebcfbe2758499eef89171
CURRENT_RUNTIME_ACCESS: ephemeral_isolated
CANONICAL_STATE_ACCESS: NONE
LOGIN_ALLOWED: false
CREDENTIALS_ALLOWED: false
GAMEPLAY_ALLOWED: false
SHARED_SOURCE_PACKAGE_MUTATION_ALLOWED: false
RUNTIME_STIMULUS: Alt+Return ToggleFullscreen exactly once, then exact inverse after persistence proof
RESTORE_REQUIREMENT: original window mode must survive the final restart before cleanup
BLOCKERS: []
NEXT_ACTION: add and execute the one-shot Synology UI-settings persistence discriminator on this branch; if the exact current source package is unavailable or the self-hosted runner cannot execute, persist that exact blocker without weakening the test
```
