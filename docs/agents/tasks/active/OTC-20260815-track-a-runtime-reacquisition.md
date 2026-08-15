---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-2105
session_role: researcher
session_rotation_count: 6
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime-research
phase: restart-relogin-reacquisition
branch: research/OTC-20260815-track-a-runtime-reacquisition
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 303
updated: 2026-08-15T21:05:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as revalidation-required input only
  - PR #283 bridge evidence as read-only reference only
  - PR #307 bounded read-only loader/Qt/support-state diagnostics
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
runtime_code_bearing_head: 4cb98e0b149a5eae21261be468618ec269a8a976
workflow_quality_head: 4cb98e0b149a5eae21261be468618ec269a8a976
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:05:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: qt-runtime-x11-diagnostic
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
stop_reason: null
active_operation:
  type: sanitized_qt_debug_plugins_and_x11_census
  prior_run: 31893122418
  prior_job: 95032257726
  diagnostic_pr: 307
  diagnostic_loader_run: 31893811826
  diagnostic_qt_plugin_run: 31893939190
  diagnostic_support_state_run: 31894272272
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-physical-canonical-home-falsified.md
next_action: add only sanitized QT_DEBUG_PLUGINS plus mapped/unmapped X11 window and extension diagnostics to the existing task-owned generation-1 launch; preserve exact SHA, display :115, WARP/SOCKS, bundled Qt/libproxy precedence, renderer, fresh HOME, no-secret child environment, login guard, observer and cleanup semantics; classify the first causal runtime difference before any further launch tweak
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the exact-build structural Worldmap path in the official native Linux Tibia client. Research output remains Draft-only; promotion belongs to coordinator PR #300.

# Exact fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runner: synology-otclient-01
task_display: ':115'
task_socks_port: 25415
upstream_track_a_socks_port: 25354
concurrency_group: official-client-re-runtime
```

Credentials are restricted to protected login steps. Persistent child environments must be credential-variable-free. Track B, shared upstream ownership, persistent display `:98`, movement and irreversible gameplay/economic effects are out of scope.

# Rotation 6 stale takeover — FACT

At takeover, `main` remains `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`, PR #303 remains Draft/open and its branch remains `4cb98e0b149a5eae21261be468618ec269a8a976`. The previous task checkpoint was last updated at `2026-08-15T17:36:00+02:00`, exceeding the repository 45-minute lease/stale interval by hours. No newer code-bearing #303 commit exists. Later PR #303 comments are read-only diagnostics from PR #307 and do not claim runtime ownership. Rotation 6 therefore takes over the same task/branch without parallel ownership.

# Bounded runtime state — FACT

The lane has independently recovered runner scheduling, exact source state, exact client fence, upstream WARP/SOCKS, task relay, task Xvfb isolation, no-secret child checks, loader support, bundled Qt 6.9 precedence, software Qt Quick backend, visible-window census and cleanup.

The following isolated hypotheses are falsified and must not be retried unchanged:

- minimal launcher metadata/HOME reconstruction;
- historical Xvfb screen/flag profile alone on fresh task-owned `:115`;
- canonical task-HOME package path via symlink;
- copied task crashdump cleanup (`prior_entries=0`);
- physical canonical task-HOME package placement;
- historical private-Xvfb cwd as sufficient to recover the visible client window.

Runs #26-#29 failed before protected login with `client_gen_1_window_missing` and `visible_window_count=0`; cleanup succeeded and no gameplay side effect occurred. Run `31893122418` / job `95032257726` is the latest completed runtime discriminator and falsifies Xvfb cwd as sufficient.

# PR #307 bounded diagnostics — FACT

Read-only PR #307 did not launch the client or use credentials. It proved:

- run `31893811826` / job `95033921299`: exact client `RUNPATH $ORIGIN/lib`; current #303 loader search path resolves completely (`RC=0`) with bundled client Qt and toolroot libproxy/EGL/GLX/X11; reverting to the literal historical loader path is disproven because today's mutable toolroot would fail on `libpxbackend-1.0.so`;
- run `31893939190` / job `95034223662`: `bin/qt.conf` has `Prefix=.`, `plugins/platforms/libqxcb.so` and `plugins/xcbglintegrations/libqxcb-glx-integration.so` exist, and both dependency chains resolve `RC=0`; missing base qxcb/GLX plugin bytes or dependencies are disproven;
- run `31894272272` / job `95035023704`: canonical HOME has no `.config`, but does have `.cache/CipSoft GmbH` with 4 files / 6937 aggregate bytes. Contents were neither read nor copied, so purpose/sensitivity remain UNKNOWN and this cache is only a candidate, not authorized input.

# Current discriminator

Instrument the existing task-owned generation-1 launch only. Enable `QT_DEBUG_PLUGINS=1` for the client and, on window timeout, capture a sanitized diagnostic containing:

- all X11 top-level windows on task-owned `:115`, including mapped/unmapped state, PID when available, geometry and title/class metadata;
- X server extension inventory relevant to X11/GLX/RENDER/XInput without touching persistent `:98`;
- filtered Qt plugin-loader messages limited to plugin paths, plugin keys, load success/failure, platform integration selection and non-sensitive error text.

Do not print environment variables, URLs carrying tokens, cookies, account/session values, login text, or cache contents. Do not change loader paths, renderer, HOME/package placement, proxy, login procedure, structural observer or cleanup in the same run.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] isolated prerequisite and negative-discriminator evidence preserved;
- [x] no unauthorized gameplay effect occurred in failed discriminator runs;
- [ ] exact final-head CI terminal green before Draft handoff.
