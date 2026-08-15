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
updated: 2026-08-15T21:13:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/workflows/tibia-official-client-re-runtime-cache-classification.yml
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
workflow_quality_head: 1147062b1f91298055f8623043457298c5797600
invocation_started_at: 2026-08-15T21:05:00+02:00
last_progress_at: 2026-08-15T21:13:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: support-cache-classification
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
stop_reason: null
active_operation:
  type: metadata_only_canonical_cache_classification
  prior_run: 31903196011
  prior_job: 95056995695
  prior_artifact: 9251658726
  prior_artifact_digest: sha256:6438b06010def0d66f4bf5753a44cdd05ad11f75723dfa25e66c16ec8573575b
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-canonical-package-path-falsified.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/20260815-physical-canonical-home-falsified.md
next_action: classify the only known canonical-HOME difference, ~/.cache/CipSoft GmbH, from path/size metadata only without reading payloads; if it is not a safe causal candidate, instrument mapped/unmapped X11 state on a fresh task-owned run before any further launch tweak
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
- Direct authoritative P0 player XYZ remains UNKNOWN; the movement geometry `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is DERIVED and must not be promoted to direct TPlayerData position.

# Reacquisition negative state

Runs #26-#29 failed before protected login with `client_gen_1_window_missing`. These hypotheses are falsified and must not be retried unchanged:

- minimal launcher metadata/HOME reconstruction alone;
- historical Xvfb screen/flag profile alone on fresh task-owned `:115`;
- canonical task-HOME package path via symlink;
- copied task crashdump cleanup (`prior_entries=0`);
- physical canonical task-HOME package placement;
- historical private-Xvfb cwd as sufficient.

PR #307 independently proved the current loader fence is correct (`RC=0`), bundled Qt/qxcb/GLX plugin bytes and dependency resolution are present, and reverting to the literal historical loader path is invalid on today's mutable toolroot.

# Rotation 6 run #30 — FACT

Commit `1147062b1f91298055f8623043457298c5797600` added only job-level `QT_DEBUG_PLUGINS=1`; loader, HOME, Xvfb, renderer, proxy, login guard, observer and cleanup semantics were unchanged.

Run `31903196011` / job `95056995695` completed FAILURE before login. It proved again:

```text
TRACK_A_UPSTREAM_WARP_VERIFIED=true
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415
TRACK_A_TASK_XVFB_VERIFIED=true display=:115
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
TRACK_A_RUNTIME_CURRENT_RUN_CLEANUP_COMPLETE=true
```

Sanitized artifact `9251658726`, digest `sha256:6438b06010def0d66f4bf5753a44cdd05ad11f75723dfa25e66c16ec8573575b`, records `visible_window_count=0` and a non-secret client log. The log proves numerous bundled QML/image/TLS plugins load successfully, asset loading completes, HTTPS reaches Tibia hosts through `127.0.0.1:25415`, and the software render thread is active. It also prints `QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled`, but this is not causal by itself: accepted positive-control job `94716022704` used the same `QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none` settings and successfully created the Tibia window and entered world.

Exact-head CI `31903198315` for `1147062b...` completed SUCCESS.

# Remaining known HOME difference

Metadata-only PR #307 run `31894272272` found no canonical `~/.config`, but did find canonical `~/.cache/CipSoft GmbH` containing exactly 4 files / 6937 aggregate bytes. No cache content was read or copied. Fresh #303 homes do not intentionally seed this cache. Its purpose and sensitivity are UNKNOWN; it must be classified without exposing or reading payload values before it can be considered a safe discriminator.

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
