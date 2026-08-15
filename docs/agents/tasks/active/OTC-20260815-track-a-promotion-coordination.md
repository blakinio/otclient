---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
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
updated: 2026-08-15T23:24:00+02:00
lease_released_at: 2026-08-15T23:24:00+02:00
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
last_progress_at: 2026-08-15T23:24:00+02:00
ci_check_generation: coordinator-rotation-13-novnc-classification
context_reconstruction_attempts: 1
stop_reason: PR309 bounded classification promoted and source closed unmerged; coordinator ownership released while PR311 protection gate and RUNTIME proceed independently
last_promotion:
  source_pr: 309
  source_pr_state: closed_unmerged
  disposition: ACCEPT_WITH_EDITS
  source_head: 717a23092e0cb43c04fd71b3471bf3eaee81b6f1
  semantic_run: 31904709435
  semantic_job: 95060619492
  source_ci_run: 31909081449
  source_ci_required_job: 95071474364
  review_threads: 0
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-display-candidate/20260815-pr309-disposition.md
next_action: once PR311 auto-merge completes, open a disjoint read-only canonical-runtime registration task that consumes merged lease governance and this bounded display-candidate evidence; do not declare :98 canonical without new identity/provenance proof and do not collide with active PR303 runtime ownership
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research Drafts are promoted only after independent coordinator review. Track B remains outside mutation authority.

# Rotation 13 result — PR #309

`ACCEPT_WITH_EDITS`; source Draft closed unmerged.

Promoted FACT:

```yaml
gateway_6082_novnc_websockify_rfb: true
rfb_protocol_version: "003.008"
rfb_framebuffer: "1920x1080"
persistent_x11_socket_set:
  - ":98"
direct_rfb_5988: CONNECTION_REFUSED
direct_rfb_5998: CONNECTION_REFUSED
direct_rfb_6015: CONNECTION_REFUSED
historical_working_track_a_display: ":98"
```

Promoted INFERENCE:

```yaml
display_98_is_strongest_persistent_backend_candidate: HIGH_CONFIDENCE
```

Preserved UNKNOWN / NOT_PROVEN:

```yaml
exact_websockify_6082_backend_display: UNKNOWN
exact_websockify_backend_transport: UNKNOWN
current_canonical_live_pid: UNKNOWN
current_canonical_live_session_state: UNKNOWN
display_98_is_canonical: NOT_PROVEN
```

The direct-port probe is complete and must not be repeated unchanged. Future canonical-runtime registration must use a different read-only discriminator or authoritative host-side service metadata.

# Current programme boundary

- #312 canonical-live lease manager is merged on main as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`.
- #311 governance is Ready, material review thread resolved, and protected auto-merge is enabled; final required CI is externally delayed by GitHub-hosted LuaJIT setup on the current ready-generation.
- #303 RUNTIME has corrected the old no-window diagnosis; current blocker is a Yama-compatible structural observer model, not GUI creation.
- a current valid lease grants mutation authority only, not concrete runtime identity.
- `:98` remains candidate only until a separate registration/provenance proof.

Track A remains incomplete.
