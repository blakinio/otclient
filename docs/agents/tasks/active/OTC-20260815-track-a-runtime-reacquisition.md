---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: active
agent: ChatGPT
session_id: chatgpt-runtime-researcher-20260815-1730
session_role: researcher
session_rotation_count: 5
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
updated: 2026-08-15T17:30:00+02:00
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
execution_reason: exact task-owned physical canonical-HOME package placement discriminator after terminal run 31892440526
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
runtime_code_bearing_head: 3327b8731e7c9babb53e9cc9c0f27428ede8ee5c
workflow_quality_head: 093cd60501e1a60529545e03baf2a73c6eab39ca
invocation_started_at: 2026-08-15T17:30:00+02:00
last_progress_at: 2026-08-15T17:30:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: physical-canonical-home
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: null
active_operation:
  type: physical_task_owned_package_under_canonical_home
  prior_run: 31892440526
  prior_job: 95030622195
  expected_discriminator: TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_READY
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-bundled-qt-loader-shadow.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-software-backend-required.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-x11-home-state-discriminator.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-minimal-home-falsified-xvfb-profile.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-xvfb-profile-falsified-rotation.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
next_action: materialize the copied exact package physically at each task-local HOME packages/Tibia path, launch from that physical cwd/path with every existing exact-client, no-secret, WARP/SOCKS, Xvfb, bundled-Qt, software-renderer and cleanup fence unchanged, then classify the first semantic result
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the existing exact-build structural Worldmap path in the official native Linux Tibia client. Research output remains Draft-only; promotion belongs to coordinator PR #300.

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

Credentials may exist only in protected login steps. Persistent runtime processes must be credential-variable-free. Track B, the shared upstream process, display `:98`, movement and irreversible gameplay/economic effects are out of scope.

# Proven prerequisites — FACT

- `synology-otclient-01`, exact source state, exact client fence, upstream WARP/SOCKS `25354`, task relay `25415`, task-local Xvfb `:115`, process ownership/no-secret checks and cleanup are reproducible;
- `libpxbackend-1.0.so` support loading, bundled Qt 6.9 precedence and software Qt Quick backend have been repaired and independently evidenced;
- minimal launcher metadata/HOME alone is insufficient;
- historical Xvfb screen/flags reproduced on isolated `:115` are insufficient;
- logical canonical task-HOME package pathname via symlink is insufficient;
- repeated isolated failures are genuine `visible_window_count=0`, not a title/PID mismatch;
- historical positive control run `31730884814`, attempt 14, job `94785048338` remains the only accepted successful exact-client login/world-view control on this runner and must not be replaced by failed attempt 15.

# Run #27 terminal classification — FACT

Run `31892440526` / job `95030622195` / head `093cd60501e1a60529545e03baf2a73c6eab39ca` completed with generation-1 setup `FAILURE`, login and generation 2 skipped, evidence snapshot `SUCCESS`, cleanup `SUCCESS`, luacheck `SUCCESS` and cppcheck `SUCCESS`.

It proved:

```text
TRACK_A_RUNTIME_TASK_CRASHDUMP_CLEARED=true prior_entries=0
TRACK_A_RUNTIME_CANONICAL_PACKAGE_LAUNCH generation=1 .../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=4979
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
TRACK_A_RUNTIME_CURRENT_RUN_CLEANUP_COMPLETE=true
```

The copied task-owned crashdump already had zero entries before deletion, so crashdump cleanup is falsified as a causal explanation. No protected login, movement, gameplay or economic effect occurred.

# Positive-control comparison — FACT

Historical successful attempt 14 also used:

```text
QT_QUICK_BACKEND=software
QSG_RENDER_LOOP=basic
QT_XCB_GL_INTEGRATION=none
MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
LIBGL_ALWAYS_SOFTWARE=1
GALLIUM_DRIVER=llvmpipe
```

Therefore the isolated GLX/EGL warnings are not by themselves a sufficient causal explanation. Attempt 14 launched the exact client from the physical package under its persistent canonical HOME and reused a previously live persistent Xvfb `:98`. The current task must never reuse, kill, restart or mutate `:98`.

# Rotation-5 discriminator

Run #26 proved only a logical canonical path backed by a symlink to `runs/<id>/package`. The remaining bounded package-layout difference that can be tested without touching persistent state is physical placement: copy the already task-owned exact package into each fresh `home-gen-N/.local/share/CipSoft GmbH/Tibia/packages/Tibia`, require it to be a real directory rather than a symlink, recheck exact client SHA/size there, and launch with cwd/package paths physically under that task-local HOME.

Change no renderer, Xvfb, networking, login, observer, credential or cleanup semantics in this discriminator.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct client transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] runner/source/WARP/relay/Xvfb/loader/Qt/software-renderer prerequisites are bounded and evidenced;
- [x] canonical symlink path and copied-crashdump hypotheses are falsified;
- [x] no unauthorized gameplay effect occurred in prior runs;
- [ ] final exact-head CI terminal green before Draft handoff.
