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
updated: 2026-08-15T21:31:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-classification.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window-replay.yml
  - .github/workflows/tibia-official-client-re-runtime-xdotool-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - PR #290 historical login procedure as revalidation-required input only
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
runtime_code_bearing_head: 1147062b1f91298055f8623043457298c5797600
workflow_quality_head: 20229fc50efc57116dfb72be36744f053fa1c704
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:31:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: xdotool_repaired_full_reacquisition
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
stop_reason: null
active_operation:
  type: full_gen1_gen2_reacquisition_with_xdotool_loader_repaired
  no_cache_control_run: 31903986899
  no_cache_control_job: 95058901925
next_action: execute the established #303 gen1-login-verify-stop-gen2-login-verify-compare contract with no cache seed and no client behavior change, but rewrite only effective-helper xdotool invocations to use toolroot loader libraries; preserve protected secrets, exact SHA, WARP/SOCKS, GDB observer, restart and cleanup semantics
---

# Objective

Prove restart/relogin/reacquisition stability for official native Linux Tibia and hand promotable evidence to coordinator PR #300. Final completion additionally requires the original structural position/record-format/privacy/network/live-session gates.

# Exact fence

`15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, runner `synology-otclient-01`, task display `:115`, task SOCKS `25415` -> Track-A WARP SOCKS `25354`.

# Accepted controls

- world/login run `31730884814`, successful attempt-13 `94716022704` and attempt-14 `94785048338`: world transition, local SOCKS only, direct TCP `0`, UDP `0`, session left running;
- structural run `31806312967` / `94785974126`: real `(x,y,z,order)` records, strip counts `0,33,88`, reversible `Up` then `Down`; `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is DERIVED only;
- direct authoritative P0 XYZ remains UNKNOWN.

# Corrected root cause — FACT

Runs #26-#30 reported `client_gen_1_window_missing`, but the helper's `resolve_window()` and login path invoke private toolroot `xdotool` without toolroot `LD_LIBRARY_PATH`, while errors are redirected and converted to empty search results. Independent cache-window run `31903627907` exposed the same tool failure as shell exit `127`.

Run `31903793288` / job `95058443760` added xdotool loader support and showed 4 PID windows / 2 visible windows with a cache-seeded HOME. That result was initially confounded by the cache seed.

The required no-cache control run `31903986899` / job `95058901925` removed the cache seed while retaining the xdotool loader repair and completed SUCCESS:

```text
TRACK_A_NO_CACHE_CONTROL=true
TRACK_A_CACHE_WINDOW_EXACT_CLIENT_VERIFIED=true
TRACK_A_CACHE_WINDOW_UPSTREAM_WARP_VERIFIED=true
TRACK_A_CACHE_WINDOW_TASK_RELAY_VERIFIED=true
TRACK_A_CACHE_WINDOW_XVFB_VERIFIED=true
TRACK_A_CACHE_WINDOW_CLIENT_RUNNING=true pid=15240
TRACK_A_CACHE_WINDOW_ALL_PID_WINDOWS=4
TRACK_A_CACHE_WINDOW_VISIBLE_PID_WINDOWS=2
TRACK_A_CACHE_WINDOW_ID=2097162
X=0 Y=0 WIDTH=1020 HEIGHT=650
```

Therefore the canonical shader/GPU cache is **not required for the visible-window gate**. The actual proven blocker was the X11 observer/control tool loader. The cache must not be added to the full reacquisition path.

# Remaining action

Run full two-generation reacquisition with only effective-helper `xdotool` invocations wrapped in the toolroot loader environment. If gen1/gen2 succeed structurally, proceed to a final live-session run rather than stopping at GUI proof.

# Acceptance

- [ ] two successful reacquired live generations with exact SHA/size;
- [ ] fresh PID/PIE after clean restart;
- [ ] WARP/SOCKS confinement, direct TCP `0`, UDP `0`;
- [ ] structural `IN_GAME` on both generations and structural reacquisition after restart;
- [ ] accepted final position proof and original literal `REC x=... y=... z=... order=... raw28=... raw30=...` boundary;
- [ ] privacy-safe screenshot;
- [ ] final accepted session intentionally left logged in after observer detach;
- [x] no-cache visible-window gate proven;
- [ ] final exact-head CI green.
