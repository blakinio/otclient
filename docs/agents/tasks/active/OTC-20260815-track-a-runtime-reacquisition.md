---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: ready
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1529
session_role: researcher
session_rotation_count: 3
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
updated: 2026-08-15T16:09:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as revalidation-required input only
  - PR #283 bridge evidence as read-only reference only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
runtime_code_bearing_head: 3327b8731e7c9babb53e9cc9c0f27428ede8ee5c
invocation_started_at: 2026-08-15T15:29:00+02:00
last_progress_at: 2026-08-15T16:09:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 5
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: anti-stall repair-cycle limit reached for the visible-window/runtime-bootstrap gate after distinct loader, Qt-runtime, renderer, minimal-HOME and Xvfb-profile hypotheses; current exact-head CI also has deterministic actionlint findings requiring a fresh defect-isolation session before another semantic run
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-bundled-qt-loader-shadow.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-software-backend-required.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-x11-home-state-discriminator.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-minimal-home-falsified-xvfb-profile.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xvfb-profile-falsified-rotation.md
next_action: fresh #303 defect-isolation session must first repair only the current workflow actionlint/shellcheck findings without changing runtime semantics, rerun exact-head CI, then resume from the documented canonical-HOME-package launch-path discriminator
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap path in the official native Linux Tibia client. Output remains Draft-only; promotion belongs to coordinator PR #300.

# Exact client and safety fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
task_state: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition
display: ':115'
task_socks_port: 25415
upstream_track_a_socks_port: 25354
concurrency_group: official-client-re-runtime
```

Credentials may exist only in protected login steps. Persistent runtime processes must be credential-variable-free. Track B, shared upstream ownership, movement and irreversible gameplay/economic effects remain out of scope.

# Closed prerequisite gates — FACT

- runner scheduling recovered to proven selector `[otclient, synology]`, runner id `21` / `synology-otclient-01`;
- exact source state `/work/_otclient_tibia_re_state` and exact client fence are reproducible;
- upstream Track A wireproxy/WARP through port `25354` is proven without taking ownership;
- task-local SOCKS relay `25415` is proven with Track/Task/Run/Role and no-secret markers;
- task-local Xvfb launch/XKB/cwd mechanics are proven;
- relay/Xvfb survive workflow-step boundaries with exact ownership/no-secret checks;
- exact existing `libpxbackend-1.0.so` path is proven and the loader repair is effective;
- official bundled Qt 6.9 precedence over toolroot Qt is effective;
- software Qt Quick backend is effective (`QSGSoftwareRenderThread` observed);
- visible-window census proves the failure is not a different title or child-window PID: repeated isolated runs have `visible_window_count=0`;
- bounded minimal launcher HOME reconstruction was executed and is not sufficient;
- historical known-good Xvfb screen/flag profile was reproduced on isolated `:115` and is not sufficient;
- no protected login step executed in runs #18-#24, and no movement/gameplay/economic side effect occurred.

# Current bounded negative results

## Run #18 — loader support repair

Run `31887680537` / job `95019260014` proved the `libpxbackend` path repair and then exposed toolroot Qt shadowing bundled Qt 6.9. Evidence: `20260815-bundled-qt-loader-shadow.md`.

## Run #19 — bundled Qt repair

Run `31887917603` / job `95019811182` removed the Qt_6.9 loader failure and exposed the rendering/window problem. Evidence: `20260815-software-backend-required.md`.

## Run #20 — software backend

Run `31888185244` / job `95020422175` proved software Qt Quick activation but still produced no visible window.

## Run #21 — X11/HOME discriminator

Run `31888421091` / job `95020972569` proved display-wide `visible_window_count=0`, task-local HOME containing only runtime caches, and source HOME containing exactly two known non-package launcher files. Evidence: `20260815-x11-home-state-discriminator.md`.

## Run #22 — minimal non-secret launcher HOME

Run `31888683076` / job `95021585746` reconstructed validated `launchermetadata.json`, a new empty task-local `.running` marker and task-local `packages/Tibia`; it still produced `visible_window_count=0`. Evidence: `20260815-minimal-home-falsified-xvfb-profile.md`.

## Run #23 — harness transformer failure only

Run `31888894069` failed before runtime due a fail-closed stale Xvfb transformation anchor. It did not test the semantic hypothesis and is not a runtime result.

## Run #24 — known-good Xvfb profile

Run `31888992382` / job `95022321212`, exact head `3327b8731e7c9babb53e9cc9c0f27428ede8ee5c`, successfully applied `1920x1080x24 -nolisten tcp -noreset` without the prior GLX/+render flags, passed WARP/relay/Xvfb/exact-client/no-secret launch and still failed at `client_gen_1_window_missing` before login. Artifact `9248039977`, digest `b0babd8bcce36cb0b8cab736723f071968914b97921f13c6b154b8f1c24bcc7a`, records `visible_window_count=0`. Evidence: `20260815-xvfb-profile-falsified-rotation.md`.

# Positive control retained

Historical run `31730884814`, attempt 14, job `94785048338`, is independently terminal `SUCCESS` for this exact client on the same runner. It resolved a visible `^Tibia$` window, submitted the bounded login bootstrap, reached probable world view and proved local SOCKS `7`, direct established `0`, client UDP `0`. The final attempt 15 failed and must not replace attempt-14 evidence.

# Strongest next discriminator

The remaining high-information difference is the package launch path/cwd/argv surface. Attempt 14 executed the client directly from `$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`, whereas the isolated task currently launches the physical task-run-root package and only exposes it into task-local HOME through a symlink.

A fresh session may test only this difference: launch the existing task-owned copied package through the task-local canonical HOME package path/cwd while preserving the exact SHA, bundled Qt, software backend, task-local Xvfb, SOCKS, no-secret and visible-window gates. Do not copy broader persistent HOME or reuse/modify display `:98`.

# Exact-head repository CI

Current exact-head CI run `31888994157` is `FAILURE` because `Fast Checks / Syntax and workflow validation` failed in actionlint/shellcheck after `yamllint` passed. Findings are SC2016, SC2251, SC2015 and SC2318 in the compact workflow shell; they are repository-quality defects, not runtime-semantic evidence.

The next session must repair those deterministic lint findings before launching another semantic runtime run.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] runner/source/WARP/relay/Xvfb prerequisites recovered and independently evidenced;
- [x] loader, bundled Qt, software renderer, visible-window census, minimal-HOME and Xvfb-profile hypotheses discriminated;
- [x] no unauthorized gameplay effect occurred during this rotation;
- [ ] final exact-head CI terminal green before Draft handoff.

# Rotation boundary

Anti-stall repair-cycle limits for the current visible-window/runtime-bootstrap gate are exhausted. This task remains `ready` on the same branch and Draft PR for a fresh defect-isolation session; no further semantic retry is authorized in this session.
