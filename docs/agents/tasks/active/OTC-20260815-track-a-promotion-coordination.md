---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-track-a-coordinator-20260815-2122
session_role: coordinator
session_rotation_count: 10
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
updated: 2026-08-15T21:22:00+02:00
lease_expires_at: 2026-08-15T22:07:00+02:00
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
invocation_started_at: 2026-08-15T21:06:00+02:00
last_progress_at: 2026-08-15T21:22:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-10-ownership-audit
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: null
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
last_promotion:
  source_pr: 307
  disposition: ACCEPT_WITH_EDITS
  source_head: 229d4bdb4051ab707f436f3c1e1602712e76ecb5
  source_exact_head_ci_run: 31894342104
  source_exact_head_ci_state: success
  source_pr_state: closed_unmerged
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-loader-diagnostic/20260815-pr307-disposition.md
active_operation:
  - persist PR 295 / PR 291 ownership-lifecycle blocker without mutating either overlapping contract task
  - inspect released results from active PR 308 and PR 303 only after material progress, without polling loops
next_action: record #295/#291 lifecycle defect under coordinator-owned evidence; then re-evaluate active P2/RUNTIME lanes once after other progress and promote only released evidence
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; coordinator owns promotion. Track B remains outside mutation authority.

# Durable programme state

- `main` invocation preflight: `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- Last verified coordinator integration generation: `ce933e8fe28ea61669da28ffcc10cf21675a62b0`, CI `31893876568` SUCCESS.
- #307: `ACCEPT_WITH_EDITS`, promoted, source Draft closed unmerged. Current loader/plugin dependency resolution is not the demonstrated RUNTIME blocker; canonical HOME cache remains metadata-only `UNKNOWN` and must not be copied/read as a shortcut.
- #308: independently active researcher rotation 2 is strengthening the successful `BUFFER_DATAFLOW_PROVEN` artifact with persistent retained-writer provenance; coordinator does not mutate it while owned.
- #303: independently active researcher rotation 6. Run #30 adds sanitized `QT_DEBUG_PLUGINS=1`; coordinator does not mutate it while owned.
- #302: waiting on a bounded live exact-client in-game process; direct player XYZ remains `UNKNOWN/INCONCLUSIVE`.

# #295 / #291 lifecycle audit

- #295 remains open, non-Draft and has four unresolved material review threads: duplicate contract ownership, missing separate-authorization qualification for Atlas consumption, weakened raw-packet prohibition, and dropped non-negative integer constraint for `producer.protocol_version`.
- #291 is already merged as `005158b5b9bf25fe77bd5fc10813a6388a072836`, but `docs/agents/tasks/active/OTC-20260813-map-observation-export.md` remains on `main` with `status: blocked` and still declares ownership of `docs/agents/contracts/MAP_OBSERVATION_V1.md`.
- #295's correction task also declares that contract. Therefore the overlap is real even though #291 is merged. Coordinator must not edit the contract through #295 until the stale merged-task lifecycle is formally archived/superseded under a correctly owned task.
- Current disposition stays `RETURN_FOR_EVIDENCE / OWNERSHIP_LIFECYCLE_BLOCKED`; no Track B mutation or external Oteryn dependency is authorized.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_writer_retention_intermediate_type_and_qdatastream_serialization_proven_pipeline_order_final_egress_harness_open
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Remaining programme gates

- finish P2 buffer/framing/pipeline-order/final-egress/harness evidence;
- recover live RUNTIME restart/relogin and provide bounded P0/P1 observation;
- prove direct P0 reads and live P1 authority/restart stability;
- prove A3/A4 action parity where required;
- close semantic protocol/QMeta coverage and finite P0/P1 denominators;
- repair #295/#291 ownership lifecycle before contract mutation;
- final audit/E2E/exact-head CI/PR hygiene/archive/ownership release.
