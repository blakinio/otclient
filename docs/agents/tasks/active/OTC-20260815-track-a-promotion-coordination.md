---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
session_role: coordinator
session_rotation_count: 11
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T21:39:00+02:00
lease_released_at: 2026-08-15T21:39:00+02:00
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
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
last_progress_at: 2026-08-15T21:39:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-11-post-p2-promotion
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: serial programme rotation into new non-overlapping P2 downstream-consumer research lane; coordinator ownership deliberately released before researcher task initialization
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
last_promotion:
  source_pr: 308
  source_pr_state: closed_unmerged
  disposition: ACCEPT_WITH_EDITS
  source_final_head: 7153ba4f0799a2c6b81eeeb62e4b1320e386c924
  source_release_head_ci_run: 31903882606
  source_release_head_ci_state: success
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-buffer-boundary/20260815-pr308-disposition.md
next_action: initialize and execute isolated P2 task `OTC-20260815-track-a-p2-buffer-downstream-consumer` from exact main, using #308 promoted facts only as pinned unmerged dependency; recover the first exact downstream consumer/transform of the retained QBuffer-backed byte container without generic census or final-socket shortcut
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only. Coordinator owns promotion/integration. Track B remains outside mutation authority.

# Current promoted P2 boundary

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> retained helper 0x1960340 / TIODeviceWriter AP 0x2f69d48
  -> retained QDataStream serialization
  -> persistent QBuffer-backed QIODevice byte container
```

Proven local lifecycle: QBuffer/QDataStream binding exists before serializer use.

Still UNKNOWN: first downstream consumer/transform of the retained byte container; overall protocol-stage order; framing; sequence; compression; encryption; final binary egress/socket ownership; causal local harness.

# Other durable boundaries

- #307 loader/plugin diagnostics promoted and source closed unmerged; cache state remains non-causal/UNKNOWN.
- #303 RUNTIME remains separately owned. Cache-seed run `31903627907` is `INCONCLUSIVE_HARNESS_FAILURE`, and coordinator comment `5303842133` requires no-payload X11/Qt diagnostics. Do not mutate #303 while owned.
- #302 P0 waits on live exact-client in-game RUNTIME observation; direct player XYZ remains `UNKNOWN/INCONCLUSIVE`.
- #295 remains ownership-lifecycle blocked by merged #291 stale active contract ownership; four material review threads remain unresolved.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_retained_qdatastream_to_persistent_qbuffer_backed_byte_container_proven_protocol_stage_order_framing_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```
