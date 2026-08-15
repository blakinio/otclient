---
task_id: OTC-20260815-track-a-novnc-display-diagnostic
status: ready
agent: unassigned
session_id: null
session_role: researcher
session_rotation_count: 3
project_lane: otclient
lane: RUNTIME-DIAGNOSTIC
track_id: official-client-re
task_kind: discovery
phase: classified-handoff
branch: research/OTC-20260815-track-a-novnc-display-diagnostic
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-novnc-display-diagnostic
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 309
updated: 2026-08-15T23:18:00+02:00
lease_released_at: 2026-08-15T23:18:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-novnc-display-diagnostic.md
  - docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/**
  - .github/workflows/tibia-official-client-re-novnc-display-diagnostic.yml
depends_on:
  - PR #303 runtime state as read-only comparison input
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
last_progress_at: 2026-08-15T23:18:00+02:00
semantic_run: 31904709435
semantic_job: 95060619492
semantic_state: success
semantic_result: DIRECT_RFB_PORT_MAPPING_INCONCLUSIVE
proposed_disposition: ACCEPT_WITH_EDITS
next_action: coordinator may promote only the bounded FACT/INFERENCE/UNKNOWN classification; do not merge or claim exact 6082-to-98 mapping; future canonical-runtime registration must use a different read-only discriminator
---

# Objective

Classify the completed read-only noVNC/display diagnostic and hand conservative evidence to the Track A coordinator.

# Final FACT

Run `31904709435`, job `95060619492` completed SUCCESS and proved:

```text
DOCKER_GATEWAY_WEBSOCKIFY_RFB_COMPLETE=true
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_FRAMEBUFFER=1920x1080
DIRECT_RFB_DISPLAY_88_REACHABLE=false
DIRECT_RFB_DISPLAY_98_REACHABLE=false
DIRECT_RFB_DISPLAY_115_REACHABLE=false
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
TRACK_A_NOVNC_DIRECT_RFB_FINGERPRINT_PROBE_COMPLETE=true
```

# Final boundary

```yaml
gateway_6082_novnc_rfb: FACT
persistent_x11_socket_98_only: FACT
historical_working_track_a_display_98: FACT
direct_rfb_5988_5998_6015: CONNECTION_REFUSED
exact_6082_backend_display: UNKNOWN
display_98_is_strongest_candidate: INFERENCE_HIGH_CONFIDENCE
display_98_is_canonical: NOT_PROVEN
```

Connection refusal on the conventional direct RFB ports is not evidence against an internal/Unix-socket websockify mapping. The exact backend remains unknown.

Durable evidence:
`docs/agents/evidence/OTC-20260815-track-a-novnc-display-diagnostic/20260815-direct-rfb-final-classification.md`

No semantic rerun was performed, no framebuffer payload was exported and no runtime was mutated.
