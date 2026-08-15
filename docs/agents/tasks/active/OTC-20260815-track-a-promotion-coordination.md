---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-2352
session_role: coordinator
session_rotation_count: 14
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T23:52:00+02:00
lease_released_at: null
risk: medium
related_pr: 300
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
  - tools/tibia_worldmap_reconstruction/**
  - tests/tools/tibia_worldmap_reconstruction/**
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
last_progress_at: 2026-08-15T23:52:00+02:00
ci_check_generation: coordinator-rotation-14-runtime-registration
context_reconstruction_attempts: 1
stop_reason: null
last_promotion:
  source_pr: 309
  source_pr_state: closed_unmerged
  disposition: ACCEPT_WITH_EDITS
active_review:
  source_pr: 315
  source_final_head: 129b440195439e7fd813e548d55c76a23ede88a7
  semantic_code_head: 60c19331703d68fa455b14227c8a9aad8a76d26f
  semantic_run: 31910131938
  semantic_job: 95073832354
  repository_ci_run: 31910340819
  repository_ci_required_job: 95074702295
  review_threads: 0
  proposed_disposition: ACCEPT_WITH_EDITS
next_action: independently promote bounded PR315 current-state registration result, close source unmerged, then continue only disjoint planning while PR316 remains actively owned; PR311 stays fail-closed Draft until PR316 plus bootstrap-boundary reconciliation
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research Drafts are promoted only after independent coordinator review. Track B remains outside mutation authority.

# Rotation 14 — PR #315 registration review

Source final handoff head `129b440195439e7fd813e548d55c76a23ede88a7` has repository CI `31910340819`, including `CI / Required` job `95074702295`, SUCCESS and zero review threads.

Final semantic code head `60c19331703d68fa455b14227c8a9aad8a76d26f`, run `31910131938`, job `95073832354`, SUCCESS on `synology-otclient-01`.

Independent review rejects the first-pass overclaim that RFB desktop-name text proves exact backend mapping. Final source correctly performs visible+hidden X11 window census plus global exact-client `/proc/*/exe` size/SHA census without environ/cmdline/ptrace/input/framebuffer export.

Promotable FACT:

```yaml
semantic_result: PERSISTENT_DISPLAY_NO_LIVE_CLIENT
persistent_x11_socket_set:
  - ":98"
display_98_present: true
tibia_window_count_all: 0
tibia_window_count_visible: 0
global_exact_client_process_count: 0
exact_window_candidate_count: 0
rfb_6082_reachable: true
rfb_protocol_version: "003.008"
rfb_framebuffer: "1920x1080"
rfb_desktop_name_supports_display_98: true
```

Promotable interpretation:
- historical successful `:98` login/world evidence remains valid;
- that historical exact-client process/session is not running now;
- there is no current exact-fenced client process anywhere on the runner at observation time.

Preserved boundary:

```yaml
exact_6082_backend_display: UNKNOWN
display_98_is_canonical: false
current_canonical_live_pid: none_observed
current_live_world_session: none_observed
```

The desktop name supporting `98` strengthens the mapping inference only; it is not authoritative backend configuration.

Programme consequence: there is currently no live runtime to register/reuse. Initial canonical-session creation is therefore a distinct future mutation transition and must not be smuggled through the reuse gate. PR #311 remains Draft while that bootstrap boundary and active PR #316 supervisor remediation are unresolved.
