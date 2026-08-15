---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
session_role: coordinator
session_rotation_count: 9
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
updated: 2026-08-15T21:20:00+02:00
lease_released_at: 2026-08-15T21:20:00+02:00
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
last_progress_at: 2026-08-15T21:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-9-loader-promotion
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: serial programme rotation into released P2 task #308; coordinator ownership deliberately released before researcher mutation
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
pending_integration_head: a0b79c17d802bf4a26be0e178e4f08bb5aefff4f
pending_integration_ci_run: not_checked_yet
last_promotion:
  source_pr: 307
  disposition: ACCEPT_WITH_EDITS
  source_head: 229d4bdb4051ab707f436f3c1e1602712e76ecb5
  source_exact_head_ci_run: 31894342104
  source_exact_head_ci_state: success
  source_pr_state: closed_unmerged
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-loader-diagnostic/20260815-pr307-disposition.md
next_action: after P2 #308 completes its released worker handoff, reacquire coordinator, review/promote only the bounded QBuffer/QDataStream facts, then reconcile stale RUNTIME #303 using the promoted #307 next discriminator
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; coordinator owns promotion. Track B remains outside mutation authority.

# Rotation-9 durable progress

- `main` preflight remained `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- Prior coordinator CI `31893876568` on `ce933e8fe28ea61669da28ffcc10cf21675a62b0` is terminal `SUCCESS` and is the last verified coordinator integration generation.
- PR #307 was independently reviewed from workflow source and raw logs, classified `ACCEPT_WITH_EDITS`, promoted into coordinator-owned evidence, and closed unmerged. Promoted facts: current exact-client bundled-Qt/libproxy/toolroot dependency graph resolves; literal historical loader replay is not a current positive oracle; qxcb and xcb-GLX plugin files/chains resolve. Persistent HOME `.cache/CipSoft GmbH` remains metadata-only `UNKNOWN`, with no payload read/copy authorization.
- PR #303 run `31893122418` reproduced the historical patched-Xvfb cwd on isolated task-owned `:115` but still failed before login with `client_gen_1_window_missing`; cleanup succeeded. Xvfb cwd is therefore rejected as an isolated cause. #303 remains read-only until stale takeover is revalidated.
- PR #308 semantic run `31903141897` on code-bearing head `5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2` and code-bearing CI `31903144036` are `SUCCESS`. Artifact `9251635451`, digest `sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32`, independently shows a QBuffer allocation and direct QBuffer-as-QIODevice binding into a local QDataStream before local serialization. Source task is still waiting/unassigned and requires its own artifact classification/final handoff before coordinator promotion.
- PR #302 still has no bounded live exact-client in-game observation window; direct player XYZ remains `UNKNOWN/INCONCLUSIVE`.

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
- reconcile #295/#291 ownership lifecycle without Track B contamination;
- final audit/E2E/exact-head CI/PR hygiene/archive/ownership release.
