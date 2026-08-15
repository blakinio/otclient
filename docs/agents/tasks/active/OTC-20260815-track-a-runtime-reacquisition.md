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
updated: 2026-08-15T21:22:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-classification.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window-replay.yml
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
workflow_quality_head: 3c3ba863c51c63ec977207224551e874411d57cc
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:22:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: cache_window_probe_tool_repair
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
stop_reason: null
active_operation:
  type: replay_identical_cache_window_probe_with_xdotool_loader_only_repaired
  prior_run: 31903627907
  prior_job: 95058043269
next_action: replay the exact cache-window shell body with only toolroot LD_LIBRARY_PATH exported for xdotool; classify actual all/visible PID window counts; do not change client/cache/Xvfb/proxy/login behavior
---

# Objective

Prove restart/relogin/reacquisition stability for official native Linux Tibia and hand promotable evidence to coordinator PR #300. Final completion still requires structural world proof, authoritative/accepted position proof, one reversible move, privacy-safe screenshot, network confinement and a final live session intentionally left running.

# Exact client fence

- version mapping: `15.32.df7b29`
- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- runner: `synology-otclient-01`
- task display: `:115`
- task SOCKS: `25415` -> upstream WARP SOCKS `25354`

# Accepted positive controls

- world/login exact-build run `31730884814`, successful attempt-13 job `94716022704` and attempt-14 job `94785048338`: world transition, SOCKS-only transport, direct TCP `0`, UDP `0`, session left running;
- structural Worldmap run `31806312967` / job `94785974126`: real `(x,y,z,order)` records, strip counts `0,33,88`, reversible `Up` then `Down`; geometry `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is DERIVED, not direct TPlayerData position;
- direct authoritative P0 player XYZ remains UNKNOWN.

# Falsified reacquisition hypotheses

Do not retry unchanged: minimal launcher HOME; historical Xvfb screen/flags alone; canonical package symlink; task crashdump residue; physical canonical package placement; historical private-Xvfb cwd. PR #307 also disproved base ELF/qxcb/GLX dependency failure and disproved reverting bundled-Qt/libproxy precedence.

# Rotation 6 diagnostics

## Qt runtime diagnostic

Commit `1147062b1f91298055f8623043457298c5797600`, run `31903196011` / job `95056995695`, added only `QT_DEBUG_PLUGINS=1`. Exact SHA, WARP, task relay/Xvfb and no-secret child gates passed, then `client_gen_1_window_missing`. Artifact `9251658726`, digest `sha256:6438b06010def0d66f4bf5753a44cdd05ad11f75723dfa25e66c16ec8573575b`, records `visible_window_count=0`. QML/image/TLS plugins load, assets complete, HTTPS uses SOCKS and `QSGSoftwareRenderThread` is alive. The GLX/EGL warning is not sufficient cause because accepted positive control `94716022704` used the same `QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none`. Exact-head CI `31903198315` succeeded.

## Canonical cache classification

Run `31903484499` / job `95057696652` succeeded. Canonical `~/.cache/CipSoft GmbH` is exactly three `.qsb` shader cache files (`2309`, `2162`, `2386` bytes) plus one 80-byte GPU/generic cache file, total `4` files / `6937` bytes, with zero sensitive path keyword hits. Payloads were not read in that run.

## Cache-window causal discriminator

Run `31903627907` / job `95058043269` seeded only the classified cache into fresh task-local HOME after a non-output sensitive-marker scan, verified exact SHA/WARP/task relay/Xvfb/no-secret client and launched PID `12468`. It then exited `127` before emitting window counts because the X11 probe invoked toolroot `xdotool` without toolroot `LD_LIBRARY_PATH`. This is a diagnostic-tool failure and does NOT prove or disprove the cache hypothesis. Client behavior must remain unchanged for the replay.

# Acceptance

- [ ] two successful reacquired live generations with exact SHA/size;
- [ ] fresh PID/PIE after clean restart;
- [ ] direct TCP `0`, UDP `0`, WARP/SOCKS confinement on reacquired world sessions;
- [ ] structural `IN_GAME` and Worldmap records on reacquired sessions;
- [ ] structural reacquisition after clean restart/relogin;
- [ ] final accepted player position proof within coordinator claim boundary;
- [ ] final literal record format required by original prompt (`REC x=... y=... z=... order=... raw28=... raw30=...`) or explicit blocker if raw fields cannot be justified;
- [ ] privacy-safe screenshot;
- [ ] final session intentionally left logged in after bounded observer detach;
- [x] all failed discriminators avoided credential use/gameplay effects and cleaned only exact task-owned runtime;
- [ ] final exact-head CI green.
