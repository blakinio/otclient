---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
session_role: coordinator
session_rotation_count: 12
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
updated: 2026-08-15T22:56:00+02:00
lease_released_at: 2026-08-15T22:56:00+02:00
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
last_progress_at: 2026-08-15T22:56:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-12-live-lease-promotion
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: accepted corrected PR312 with bounded edits; MODULE_CATALOG.md and CHANGELOG.md ownership delegated exclusively to source promotion slice before coordinator release
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
last_promotion:
  source_pr: 312
  source_pr_state: open_draft_pending_catalog_changelog_and_final_ci
  disposition: ACCEPT_WITH_EDITS
  corrected_code_head: e368173086ba8bb1235218b3ec11e046e2c909cb
  custom_run: 31907695244
  custom_unit_job: 95067968895
  custom_selfhosted_job: 95067968820
  repository_ci_run: 31907697738
  repository_ci_required_job: 95068323632
  prior_disposition: RETURN_FOR_EVIDENCE
  prior_material_finding: expired release bypassed explicit stale-takeover reason path
  repaired: true
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
delegated_paths:
  target_pr: 312
  purpose: required same-PR reusable-tool discovery metadata before merge
  paths:
    - docs/agents/MODULE_CATALOG.md
    - docs/agents/CHANGELOG.md
next_action: PR #312 promotion worker may claim exactly the delegated discovery paths, add bounded catalogue/changelog entries, pass final exact-head custom validation and CI / Required, then protected-merge #312; afterward coordinator must re-evaluate PR #311 without declaring :98 canonical
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers/implementation workers remain Draft-only. Coordinator owns promotion/integration. Track B remains outside mutation authority.

# Rotation 12 disposition — PR #312

`ACCEPT_WITH_EDITS`

PR #311 policy v3 intentionally disables canonical-live mutation/reuse until `main` contains a reviewed authoritative serialized lease primitive. PR #312 is the implementation candidate.

Independent coordinator source review of #312's first handoff found one material defect: an expired holder could call `release` and then reacquire normally, bypassing the explicit stale-takeover reason/audit path. The source was returned for evidence instead of being promoted merely because CI was green.

Corrected source head `e368173086ba8bb1235218b3ec11e046e2c909cb` rejects expired release with `lease_expired`, preserves active/expired state until explicit takeover, and proves on Synology that a takeover reason is required before generation 2 can be acquired. Corrected custom workflow `31907695244` and repository CI `31907697738` including `CI / Required` job `95068323632` are SUCCESS.

No further material semantic defect was found in the corrected bounded lease manager. Accepted scope is cooperative same-UID programme governance only; it is not a hostile-local-user security boundary and it does not establish a canonical Tibia PID/display/session by itself.

## Required edits before merge

Repository discovery policy requires reusable tooling to update `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` in the same promotion PR. Coordinator ownership of exactly those two paths is therefore released and explicitly delegated to PR #312. No other coordinator path is delegated.

PR #312 must pass exact final-head custom validation and repository `CI / Required` after those edits before protected merge.

# Current promoted P2 boundary

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> retained helper 0x1960340 / TIODeviceWriter AP 0x2f69d48
  -> retained QDataStream serialization
  -> persistent QBuffer-backed QIODevice byte container
```

Still UNKNOWN: first downstream consumer/transform of the retained byte container; overall protocol-stage order; framing; sequence; compression; encryption; final binary egress/socket ownership; causal local harness.

# Other durable boundaries

- #303 RUNTIME remains separately owned; do not mutate it while owned.
- #302 P0 waits on live exact-client in-game RUNTIME observation; direct player XYZ remains `UNKNOWN/INCONCLUSIVE`.
- #295 remains ownership-lifecycle blocked by merged #291 stale active contract ownership.
- #311 remains Draft/policy-v3 and must stay fail-closed until an accepted lease manager is on `main`.
- `:98` remains only the strongest historical/persistent display candidate; canonical registration is a separate read-only proof step.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_retained_qdatastream_to_persistent_qbuffer_backed_byte_container_proven_protocol_stage_order_framing_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```
