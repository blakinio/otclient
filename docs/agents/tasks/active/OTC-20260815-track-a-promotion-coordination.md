---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-2320
session_role: coordinator
session_rotation_count: 13
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 3575cc0c0a0b4efbcd9fc860d3226002fe40e70f
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T23:20:00+02:00
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
last_progress_at: 2026-08-15T23:20:00+02:00
ci_check_generation: coordinator-rotation-13-novnc-classification
context_reconstruction_attempts: 1
stop_reason: null
last_promotion:
  source_pr: 312
  source_pr_state: merged
  disposition: ACCEPT_WITH_EDITS
  merged_main_commit: 3575cc0c0a0b4efbcd9fc860d3226002fe40e70f
active_review:
  source_pr: 309
  source_head: 717a23092e0cb43c04fd71b3471bf3eaee81b6f1
  semantic_run: 31904709435
  semantic_job: 95060619492
  source_ci_run: 31909081449
  source_ci_required_job: 95071474364
  review_threads: 0
  proposed_disposition: ACCEPT_WITH_EDITS
next_action: independently promote only the bounded PR309 FACT/INFERENCE/UNKNOWN display/noVNC classification into coordinator evidence, close source Draft unmerged after exact-head validation, then return to PR311 protected merge and canonical-runtime registration planning without declaring :98 canonical
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research Drafts are promoted only after independent coordinator review. Track B remains outside mutation authority.

# Rotation 13 — PR #309 noVNC/display classification review

Source semantic run `31904709435` / job `95060619492` is SUCCESS and was independently inspected. Exact facts:

```yaml
gateway_6082_novnc_websockify_rfb: FACT
rfb_protocol_version: 003.008
rfb_framebuffer: 1920x1080
persistent_x11_socket_set: [":98"]
direct_rfb_5988: CONNECTION_REFUSED
direct_rfb_5998: CONNECTION_REFUSED
direct_rfb_6015: CONNECTION_REFUSED
```

Historical accepted Track A evidence used display `:98` successfully. Combined with it being the only persistent X11 socket, `:98` is the strongest backend/runtime-display candidate. This remains an inference, not canonical registration.

The direct-port discriminator cannot prove or disprove `6082 -> :98` because websockify may use a Unix socket/internal endpoint. Exact backend mapping remains UNKNOWN. `:98` canonical status remains NOT_PROVEN.

Source head `717a23092e0cb43c04fd71b3471bf3eaee81b6f1` has repository CI `31909081449`, including `CI / Required` job `95071474364`, SUCCESS and zero review threads.

# Current programme boundary

- #312 canonical-live lease manager is merged on main as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`.
- #311 governance is Ready with material lease thread resolved; final protection CI is externally delayed by GitHub-hosted LuaJIT setup.
- #303 RUNTIME now has visible-window root cause repaired; current blocker is safe Yama-compatible structural observer ownership, not GUI creation.
- `:98` remains candidate only; a separate read-only canonical-runtime registration must prove concrete runtime identity before live reuse/mutation.

Track A remains incomplete.
