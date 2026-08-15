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
updated: 2026-08-15T21:18:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-classification.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-window.yml
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
runtime_code_bearing_head: 1147062b1f91298055f8623043457298c5797600
workflow_quality_head: a14e27a6e7f52c031fb31c86e1a86acfb09e6e42
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:18:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: task_local_cache_window_discriminator
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
stop_reason: null
active_operation:
  type: task_local_shader_gpu_cache_seed_window_test
  prior_run: 31903484499
  prior_job: 95057696652
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-physical-canonical-home-falsified.md
next_action: run one no-login task-local visible-window discriminator that differs from run 31903196011 only by seeding the previously classified non-account shader/GPU cache into fresh HOME; do not mutate canonical cache; if it fails, stop treating cache as causal and move to mapped/unmapped X11 state
---

# Objective

Prove restart/relogin/reacquisition stability for the exact official native Linux Tibia client and feed final Track A completion evidence to coordinator PR #300. Research remains Draft-only until promoted by the coordinator.

# Exact client fence

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

Credentials are restricted to protected login steps. Persistent child environments must be credential-variable-free. Track B, persistent display `:98`, unrelated gameplay, irreversible/economic actions and owner-funded AI/API usage are out of scope.

# Previously proven positive controls

- Exact-build software world-login run `31730884814`, successful attempt 13 job `94716022704` and attempt 14 job `94785048338`: world-view transition, SOCKS-only network confinement, direct TCP `0`, UDP `0`, session left running.
- Accepted exact-build structural Worldmap run `31806312967` / job `94785974126`: real structural `(x,y,z,order)` records, strip counts `0,33,88`, and one reversible `Up` / `Down` action with structural before/after behavior.
- Direct authoritative P0 player XYZ remains UNKNOWN; movement geometry `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is DERIVED only.

# Reacquisition negative state

Runs #26-#29 failed before protected login with `client_gen_1_window_missing`. Falsified unchanged hypotheses: minimal launcher HOME, historical Xvfb screen/flags alone, canonical package symlink, task crashdump residue, physical canonical task-HOME package placement and historical private-Xvfb cwd.

PR #307 proved the current bundled-Qt/libproxy loader fence is correct (`RC=0`), qxcb/GLX plugin dependencies resolve, and the historical literal loader path is not valid against today's toolroot.

# Rotation 6 run #30 — FACT

Commit `1147062b1f91298055f8623043457298c5797600` added only `QT_DEBUG_PLUGINS=1`. Run `31903196011` / job `95056995695` again failed before login with exact SHA, WARP, task relay/Xvfb and credential-free child environment all verified. Sanitized artifact `9251658726`, digest `sha256:6438b06010def0d66f4bf5753a44cdd05ad11f75723dfa25e66c16ec8573575b`, records `visible_window_count=0`.

Its log proves bundled QML/image/TLS plugins load, asset loading completes, Tibia HTTPS requests pass through SOCKS, and `QSGSoftwareRenderThread` is active. The `QXcbIntegration` GLX/EGL warning is not causal by itself because accepted positive-control job `94716022704` used the same `QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none` pair and successfully displayed/login/world-entered. Exact-head CI `31903198315` completed SUCCESS.

# Canonical cache classification — FACT

Run `31903484499` / job `95057696652` completed SUCCESS without reading cache payloads. The only known canonical HOME difference is exactly:

- three shader-cache files with `.qsb` suffix, sizes `2309`, `2162`, `2386` bytes;
- one `gpu+generic_cache` file, size `80` bytes;
- total 4 files / 6937 bytes;
- zero path keyword hits for cookie/password/credential/token/email/account/session/auth;
- exact client fence verified.

Therefore the cache is a bounded shader/GPU-state candidate rather than identified account/session state. The next test may copy this exact 6937-byte classified cache only into task-local fresh HOME after an automated non-output sensitive-string rejection; canonical cache itself remains read-only and unchanged.

# Acceptance gate

- [ ] exact client SHA/size rechecked on two successful reacquired generations;
- [ ] fresh PID/PIE proven after clean restart;
- [ ] WARP/SOCKS confinement with direct TCP `0` and UDP `0` on reacquired world sessions;
- [ ] structural `IN_GAME` independently proved on reacquired sessions;
- [ ] structural read reacquired after clean restart/relogin;
- [ ] final direct/accepted position evidence according to coordinator claim boundary;
- [ ] final privacy-safe screenshot evidence;
- [ ] final accepted session intentionally left running after bounded observers detach;
- [x] negative discriminator evidence and no-secret/no-gameplay safety preserved;
- [ ] final exact-head CI terminal green before Draft handoff.
