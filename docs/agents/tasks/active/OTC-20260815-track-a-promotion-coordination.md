---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
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
updated: 2026-08-15T23:53:00+02:00
lease_released_at: 2026-08-15T23:53:00+02:00
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
last_progress_at: 2026-08-15T23:53:00+02:00
ci_check_generation: coordinator-rotation-14-runtime-registration
context_reconstruction_attempts: 1
stop_reason: PR315 current-state result promoted and source closed unmerged; coordinator ownership released while PR316 remains actively owned/validating
last_promotion:
  source_pr: 315
  source_pr_state: closed_unmerged
  disposition: ACCEPT_WITH_EDITS
  source_final_head: 129b440195439e7fd813e548d55c76a23ede88a7
  semantic_code_head: 60c19331703d68fa455b14227c8a9aad8a76d26f
  semantic_run: 31910131938
  semantic_job: 95073832354
  source_ci_run: 31910340819
  source_ci_required_job: 95074702295
  review_threads: 0
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-runtime-registration/20260815-pr315-disposition.md
next_action: when active PR316 releases ownership, independently review/promote the final guard supervisor; PR311 remains Draft and must also reconcile the initial-canonical-session bootstrap deadlock proved by PR315 before merge; do not start/login a canonical session yet
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research Drafts are promoted only after independent coordinator review. Track B remains outside mutation authority.

# Rotation 14 result — PR #315

`ACCEPT_WITH_EDITS`; source Draft closed unmerged.

Promoted current-state FACT:

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

Promoted interpretation:
- historical successful `:98` login/world evidence remains valid;
- that historical exact-client process/session is not running now;
- there is no current exact-fenced official-client process anywhere visible through the runner namespace at observation time.

Preserved boundary:

```yaml
rfb_desktop_name_supports_6082_to_98_mapping: INFERENCE_SUPPORTING_EVIDENCE
exact_6082_backend_display: UNKNOWN
display_98_is_canonical: false
current_canonical_live_pid: none_observed
current_live_world_session: none_observed
```

The final probe covered hidden and visible windows plus a global exact executable size/SHA census. It used no process environment/cmdline, ptrace, framebuffer export, input, signals, login or runtime mutation.

# Programme consequence

There is no live session to reuse right now. Initial canonical-session creation is a separate mutation transition. It remains disabled until Track A has a reviewed bootstrap primitive that can create the exact-fenced process under authoritative lease, prove/register its identity, and transition to an idle persistent session without releasing control while untracked mutation descendants remain.

# Other live gates

- #316 supervisor remediation is actively owned and final `CI / Required` is green, but worker handoff has not yet released ownership; coordinator must not mutate it.
- #311 governance remains Draft; it must consume the final #316 manager state and encode the bootstrap/reuse distinction before merge.
- #314 stale lease-manager closeout is closed/superseded.
- #303 RUNTIME remains separately owned; current blocker concerns Yama-compatible structural observation, not X11 window creation.

Track A remains incomplete.
