---
task_id: OTC-20260821-surveyor-next-nonoverlap-gap
status: validating
phase: auditing
agent: ChatGPT
project_lane: otclient
lane: P0-SURVEYOR
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
branch: fix/OTC-20260821-surveyor-ui-settings-physical
base_main: 1cb56f652784ca1baeaf59a777e4c0b5b8ab312e
execution_mode: chat
execution_reason: physical failure is isolated and repaired; exact-head deterministic validation/audit is repository-hosted until post-merge trusted-main reacceptance
execution_class: github_hosted
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: true
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260821-surveyor-next-nonoverlap-gap.md
  - docs/agents/tasks/archive/OTC-20260821-surveyor-next-nonoverlap-gap.md
  - docs/agents/evidence/OTC-20260821-surveyor-next-nonoverlap-gap/**
  - .github/workflows/track-a-surveyor-tests.yml
  - tools/tibia_re_surveyor/ui_settings.py
  - tools/tibia_re_surveyor/reader_registry.py
  - tools/tibia_re_surveyor/README.md
  - tests/tools/tibia_re_surveyor/test_ui_settings.py
  - tests/tools/tibia_re_surveyor/test_survey.py
modules_touched:
  - tibia_re_surveyor
depends_on:
  - OTC-20260821-surveyor-action-protocol-reader
blocks: []
feature_scope:
  type: backend_only
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: discovery selected one non-overlapping reader; the same task now owns implementation through validation, physical acceptance and closeout
invocation_started_at: 2026-08-21T22:05:00+02:00
last_progress_at: 2026-08-21T22:36:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: repair_exact_head
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
next_action: obtain fresh independent exact-head audit plus CI/governance PASS for repair #659, merge if clean, then rerun trusted-main read-only physical acceptance
---

# Surveyor v2 next non-overlap typed-reader slice

## Goal

Continue Surveyor v2 from current `main` after terminal `OTC-20260821-surveyor-action-protocol-reader`. Select the highest-value current P0/P1 typed-reader gap that is safe and non-overlapping, then complete that reader through implementation, validation, audit, protected merge, trusted-main read-only physical E2E, durable evidence and terminal archival.

## Frozen owner authority

The current owner request authorizes the bounded Surveyor continuation and read-only physical acceptance. It explicitly forbids gameplay input, relogin, client restart and process-memory writes. No credential use, character selection, process-control, injection, network mutation or transaction/economy action is authorized.

## Discovery acceptance

- Current `main` is the source of truth; historical gap counts and runtime IDs are discovery evidence only.
- Run repository-only `--collect-all` first under `runtime_access: none`.
- Inspect live open PRs and active task ownership before selecting a reader.
- Exclude `world_minimap_typed_reader` while #475/#593 or successor ownership overlaps remain active.
- Rank by canonical P0/P1 blocker impact, downstream rows, exact-current-build evidence, bounded read-only discrimination feasibility, implementation size and non-overlap.
- Update this task to `implementation` and extend `owned_paths` only after the selected slice is proven non-conflicting.

## Selected slice

Fresh repository-only collect-all on exact starting `main@dce8bbd0e78ceea3681a1fe1dab40d3c19ed7458` produced 169 rows, 12 aliases, 8 missing typed readers and privacy `PASS`. `world_minimap_typed_reader` ranked first at score 125 but is excluded by still-open overlapping PRs #475 and #593. `ui_settings_typed_reader` ranked second at score 65 and is the highest-ranked non-overlapping gap. Its prior exact-build UI/settings discovery task `OTC-20260819-track-a-ui-settings-static-model` is terminally archived with ownership released and no open UI/settings PR exists.

The implementation is deliberately bounded to the exact-build `tibia::config::TClientOptions` compiled model plus the two previously causally proven Master Volume fields in `clientoptions.json`; the physical repair later binds the current file specifically as `conf/clientoptions.json` under the exact executable package root. The reader does not claim complete settings semantics, live UI application state, `TClientOptions -> clientoptions.json` linkage, or QSettings linkage. It uses no process-memory access.

## Implementer falsification checkpoint

SELF-658-001 (pre-audit, not an independent finding): the first wrapper revision checked the embedded probe state/type but did not independently validate every bounded payload field before semantic wrapping. The final candidate now fail-closes on malformed static type/literal counts, reader identity, both Master Volume integer ranges, fixed relative persistence path, read-only filesystem marker, and no-process-memory marker. Two negative tests were added. Final local validation after this repair: focused UI/settings 6/6 PASS; all Surveyor tests 57/57 PASS; collect-all 169 rows / 12 aliases / 7 missing readers / privacy PASS; Track A runtime governance PASS; git diff --check PASS.

## Pre-audit exact code-head validation

Code candidate 15398146d7fd46cf047aba1f3aa7317990092b84 passed all applicable GitHub gates before this metadata-only audit checkpoint: repository CI run 32520242535, Track A Surveyor tests run 32520242610, and Track A agent runtime governance run 32520242396, all success. Implementer falsification immediately after this checkpoint found that the outer UI/settings wrapper validated only probe `state`/type and not the full bounded payload. That candidate is superseded by a fail-closed payload-shape validation repair before independent audit.

## Runtime boundary

No official-client runtime may be observed under this checkpoint. Before any later physical read-only observation, re-admit this task with an explicit non-conflicting runtime namespace and fresh `target_uniqueness: PROVEN`. Mutation remains false throughout this task.

## Terminal acceptance

The selected slice is complete only after focused/static validation, exact-current-build resolver, collect-all/privacy PASS, fresh independent audit, required exact-head CI/governance, implementation merge, trusted-main read-only physical E2E, durable evidence, intentional terminal state for all related PRs, archival/removal of the active task record and released ownership.
## Independent audit remediation

Fresh validator review `PRR_kwDOTVmdjs8AAAABKddk8A` on head `e91504bb8dcfcb7d582baf122710981e76c957e0` opened two findings: `AUD-658-001` P1 (unexpected probe fields could escape the telemetry allowlist) and `AUD-658-002` P2 (pre-open `resolve()` weakened fixed-path symlink protection).

Both are repaired in the current working candidate. Accepted static/live probe payloads now require exact key sets and are rebuilt from allowlisted scalar values. The settings file is opened by no-follow directory descriptors from passwd home through the fixed path, then validated as a regular file owned by the target uid. Post-repair focused tests are 8/8 PASS; all Surveyor tests 59/59 PASS; compileall, collect-all 169/12/7, privacy, Track A governance and `git diff --check` are PASS.

The original review is not reused as a passing audit because code changed. Fresh exact-head re-audit is mandatory before merge.

## First trusted-main physical acceptance ? repair required

Implementation PR #658 merged as `1cb56f652784ca1baeaf59a777e4c0b5b8ab312e`. Trusted-main workflow run `32523208150`, job `96899728966`, re-proved one exact client PID `19590`, start ticks `76611792`, exact size/SHA, one matching X11 window, canonical registration generation `2`, lease generation `19`, `runtime_access=read_only`, target uniqueness `PROVEN`, and `mutation_authorized=false`.

The workflow itself completed successfully and the sanitized artifact `9461336737` (digest `sha256:e10a836244c454056e09202f5f179c16852b743db9016e30c004b1fa3d19690f`) passed privacy with 169 rows / 12 aliases / 7 missing reader implementations. However, task-level E2E is **not PASS**: `ui_settings_typed_reader` returned `UNAVAILABLE / LIVE_SETTINGS_READ_FAILED:CLIENTOPTIONS_PARENT_OPEN_FAILED`. Static `TClientOptions` evidence remained AVAILABLE. No gameplay input, relogin, restart, process control, process-memory write, credential access, network mutation or economy action occurred.

This is physical repair cycle 1. The current read-only admission is persisted only to inspect the fixed-path filesystem metadata needed to explain that fail-closed result; mutation remains forbidden.

## Physical repair diagnosis

Read-only metadata isolated the failure without reading config contents. The persistent Kasm runtime does not store current settings under the prior isolated-HOME path. A bounded filename census found four historical package roots, so home scanning is intentionally rejected as ambiguous. The exact live executable is `/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client`; its own package-root sibling `conf/clientoptions.json` exists, is regular, non-symlink and owned by the target UID.

Repair #659 therefore anchors the file only to the already exact-fenced executable's package root (`exe.parent.parent`), requires `.../bin/client`, and opens package root -> `conf` -> `clientoptions.json` with mandatory `O_DIRECTORY/O_NOFOLLOW`, regular-file and UID checks. It performs no HOME scan and preserves the exact output allowlists from `AUD-658-001`. Durable diagnosis: `docs/agents/evidence/OTC-20260821-surveyor-next-nonoverlap-gap/20260821-physical-read-path-repair.md`.
