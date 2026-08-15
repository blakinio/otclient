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
updated: 2026-08-15T17:36:00+02:00
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
workflow_quality_head: 093cd60501e1a60529545e03baf2a73c6eab39ca
invocation_started_at: 2026-08-15T17:30:00+02:00
last_progress_at: 2026-08-15T17:36:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: xvfb-cwd-provenance
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
stop_reason: null
active_operation:
  type: clone_historical_private_xvfb_cwd_on_task_owned_display
  prior_run: 31892698773
  prior_job: 95031249885
  historical_launch_commit: f392d76bcaa016cccb7e07012311880f5bf3aa3f
  historical_launch_workflow: .github/workflows/tibia-official-client-re-launch.yml
  historical_positive_run: 31730884814
  historical_positive_attempts: [13, 14]
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-physical-canonical-home-falsified.md
next_action: change only effective task-owned Xvfb launch cwd to the historically proven toolroot/usr/bin cwd required by the private Xvfb /usr/bin-to-dot binary patch; keep display :115 and every other runtime/login/network/renderer/cleanup gate unchanged
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

# Bounded runtime state — FACT

The lane has independently recovered runner scheduling, exact source state, exact client fence, upstream WARP/SOCKS, task relay, task Xvfb isolation, no-secret child checks, loader support, bundled Qt 6.9 precedence, software Qt Quick backend, visible-window census and cleanup.

The following isolated hypotheses are now falsified and must not be retried unchanged:

- minimal launcher metadata/HOME reconstruction;
- historical Xvfb screen/flag profile alone on fresh task-owned `:115`;
- canonical task-HOME package path via symlink;
- copied task crashdump cleanup (`prior_entries=0`);
- physical canonical task-HOME package placement.

Runs #26-#28 all failed before protected login with `client_gen_1_window_missing` and `visible_window_count=0`; cleanup succeeded and no gameplay side effect occurred.

# Run #28 — FACT

Run `31892698773` / job `95031249885` / head `4b2653990c400f5011dcff38ce75af946d858db3` proved:

```text
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_READY generation=1 .../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_LAUNCH generation=1 .../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=10826
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
```

Artifact `9248979348` digest `21f8432108aa47d8a3def26ada56f088a86566606340a80c29b71c20f8731dc2e` records `visible_window_count=0`. Login and generation 2 were skipped. Durable evidence: `20260815-physical-canonical-home-falsified.md`.

# Historical positive controls — FACT

Run `31730884814` attempt 13 / job `94716022704` completed SUCCESS and independently proved `TRACK_A_POST_LOGIN_CHANGED_PIXELS=320319`, `TRACK_A_WORLD_CHANGED_PIXELS=660118`, local SOCKS `7`, direct established `0`, UDP `0`, probable world view and session left running. Attempt 14 / job `94785048338` is another accepted successful exact-client world-view control. Failed attempt 15 must not supersede them.

Both successful attempts reused a previously live persistent Xvfb `:98`; they did not create it.

# Xvfb provenance — FACT

Historical commit `f392d76bcaa016cccb7e07012311880f5bf3aa3f`, workflow `.github/workflows/tibia-official-client-re-launch.yml`, records the persistent `:98` provisioner. It copied toolroot Xvfb into state and patched every hardcoded `/usr/bin\0` occurrence to `.\0`, then when `:98` did not exist it executed:

```text
cd "$toolroot/usr/bin"
XKB_CONFIG_ROOT="$toolroot/usr/share/X11/xkb"
private-Xvfb :98 -screen 0 1920x1080x24 -xkbdir "$toolroot/usr/share/X11/xkb" -nolisten tcp -noreset
```

The current task helper starts its private/task-selected Xvfb without first changing cwd to `$toolroot/usr/bin`. Because the historical binary patch intentionally changes executable-directory resolution to `.`, cwd is a concrete semantic difference, not a speculative renderer tweak.

# Next discriminator

Clone only the historical Xvfb cwd onto task-owned display `:115`: make the effective helper `cd "$toolroot/usr/bin"` immediately before launching Xvfb. Do not reuse, kill, restart or mutate persistent `:98`. Do not change Xvfb flags, screen size, renderer, HOME/package, proxy, login, observer or cleanup semantics in the same experiment.

# Acceptance gate

- [ ] exact client SHA/size rechecked on both successful live generations;
- [ ] fresh PID/PIE proven after restart;
- [ ] WARP/SOCKS confinement proved with no forbidden direct transport;
- [ ] structural `IN_GAME` proved independently of GUI/network liveness;
- [ ] structural read reacquired after clean restart/relogin;
- [x] isolated prerequisite and negative-discriminator evidence preserved;
- [x] no unauthorized gameplay effect occurred in failed discriminator runs;
- [ ] exact final-head CI terminal green before Draft handoff.
