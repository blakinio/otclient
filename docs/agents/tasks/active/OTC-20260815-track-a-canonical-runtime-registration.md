---
task_id: OTC-20260815-track-a-canonical-runtime-registration
status: ready
agent: unassigned
session_id: null
session_role: researcher
session_rotation_count: 0
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: discovery
phase: final-read-only-handoff
branch: research/OTC-20260815-track-a-canonical-runtime-registration
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-canonical-runtime-registration
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 315
updated: 2026-08-15T23:47:00+02:00
lease_released_at: 2026-08-15T23:47:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-runtime-registration.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-runtime-registration/**
  - .github/scripts/tibia-official-client-re-canonical-runtime-registration.py
  - .github/workflows/tibia-official-client-re-canonical-runtime-registration.yml
depends_on:
  - merged PR #312 canonical-live lease manager
  - merged PR #313 lease concurrency remediation
  - PR #311 policy v4 as pending governance dependency
  - coordinator-promoted PR #309 display-candidate evidence as bounded read-only input
blocks: []
policy_version: 4
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
last_progress_at: 2026-08-15T23:47:00+02:00
semantic_code_head: 60c19331703d68fa455b14227c8a9aad8a76d26f
semantic_run: 31910131938
semantic_job: 95073832354
semantic_state: success
semantic_result: PERSISTENT_DISPLAY_NO_LIVE_CLIENT
first_pass_run: 31909992524
first_pass_state: superseded_overclaim_corrected
proposed_disposition: ACCEPT_WITH_EDITS
next_action: coordinator may promote the bounded current-state FACT/INFERENCE/UNKNOWN result; do not merge research source or declare :98 canonical; after lease supervisor/governance is promoted, create/reacquire one canonical persistent live session under lease and perform fresh identity registration before mutation/reuse
---

# Objective

Determine whether persistent display candidate `:98` currently hosts a live exact-fenced official Linux Tibia client suitable for canonical runtime registration, using read-only evidence only.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Final result — FACT

Final semantic code head `60c19331703d68fa455b14227c8a9aad8a76d26f`, run `31910131938`, job `95073832354` completed SUCCESS on `synology-otclient-01`.

```yaml
semantic_result: PERSISTENT_DISPLAY_NO_LIVE_CLIENT
persistent_x11_displays:
  - ":98"
display_98_present: true
tibia_window_count_all: 0
tibia_window_count_visible: 0
global_exact_client_process_count: 0
exact_window_candidate_count: 0
rfb_6082_reachable: true
rfb_desktop_name_supports_display_98: true
exact_6082_backend_display: UNKNOWN
display_98_is_canonical: false
```

The global exact-process census used only `/proc/<pid>/exe`, executable stat/SHA and process-start metadata; it did not read process environments or command lines. X11 queries did not send input/focus actions. RFB handling stopped at sanitized ServerInit metadata/desktop-name classification and did not request/export framebuffer contents.

# Interpretation

The historical successful `:98` login/world evidence remains valid, but that live process/session is no longer present now. At observation time there was no exact fenced client process anywhere on the runner, not merely no visible window.

The RFB desktop name explicitly referencing display 98 strengthens the inference that `6082` fronts `:98`, but descriptive desktop-name text is not authoritative backend configuration, so exact mapping remains UNKNOWN.

# Superseded first pass

Run `31909992524` correctly found no visible Tibia window but overclaimed exact `6082 -> :98` mapping from RFB desktop-name text and did not census hidden windows/global exact processes. That interpretation is rejected. Final run `31910131938` is authoritative for this task.

# Safety

- no client launch/stop/restart/login/logout;
- no keyboard/mouse/focus input;
- no ptrace/GDB/LD_PRELOAD;
- no signals;
- no credentials/session/process-environment/cmdline reads;
- no framebuffer/screenshot export;
- no VNC input/password;
- no Docker/host control;
- no mutation of `:98` or PR #303 `:115`;
- no Track B access.

Durable evidence:
`docs/agents/evidence/OTC-20260815-track-a-canonical-runtime-registration/20260815-final-registration-result.md`
