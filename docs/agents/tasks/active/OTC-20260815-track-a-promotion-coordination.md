---
task_id: OTC-20260815-track-a-promotion-coordination
status: waiting
agent: unassigned
session_id: null
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
updated: 2026-08-15T21:27:00+02:00
lease_released_at: 2026-08-15T21:27:00+02:00
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
last_progress_at: 2026-08-15T21:27:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-rotation-10-runtime-boundary
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: serial programme rotation into released P2 #308 completion; coordinator ownership released before researcher mutation
last_verified_integration_head: ce933e8fe28ea61669da28ffcc10cf21675a62b0
last_verified_integration_ci_run: 31893876568
last_verified_integration_ci_state: success
last_promotion:
  source_pr: 307
  disposition: ACCEPT_WITH_EDITS
  source_pr_state: closed_unmerged
  canonical_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-loader-diagnostic/20260815-pr307-disposition.md
next_action: complete released #308 researcher handoff from terminal hardened run 31903490468 and CI 31903493799; then reacquire coordinator and review/promote bounded P2 facts
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Research branches remain Draft-only; coordinator owns promotion. Track B remains outside mutation authority.

# Durable programme state

- `main` invocation preflight remained `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- Last verified coordinator integration generation: `ce933e8fe28ea61669da28ffcc10cf21675a62b0`, CI `31893876568` SUCCESS.
- #307: independently reviewed `ACCEPT_WITH_EDITS`, promoted, source Draft closed unmerged.
- #303 cache metadata classifier `31903484499` proves only 3 `.qsb` shader-class files plus one 80-byte gpu/cache-class file, 6937 B total, payload unread in that classifier. Later seed run `31903627907` reached `CACHE_SEEDED` and `CLIENT_RUNNING` but exited `127` before mapped/visible window counts; coordinator classifies it `INCONCLUSIVE_HARNESS_FAILURE`, not cache causality. Further canonical-cache payload reads/copies are returned for evidence; PR comment `5303842133` directs no-payload mapped/unmapped X11 + Qt diagnostics. Canonical evidence: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/runtime-cache-boundary/20260815-pr303-cache-classification-and-harness.md`.
- #308 hardened semantic run `31903490468` on code-bearing head `34f73b0c48198ba452caa505b4c0f3ae7e5b61d7` is terminal SUCCESS; code-bearing CI `31903493799` is terminal SUCCESS. Task is `waiting/unassigned` and explicitly requests a fresh researcher rotation to classify artifact, persist final evidence, then release Draft ready for coordinator.
- #295 remains ownership-lifecycle blocked by merged #291's stale active task record still owning `MAP_OBSERVATION_V1.md`; four material review threads remain unresolved. Canonical audit: `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/map-observation-ownership/20260815-pr295-pr291-lifecycle-blocker.md`.
- #302 remains waiting for a bounded live exact-client in-game observation window; direct player XYZ stays `UNKNOWN/INCONCLUSIVE`.

# Canonical non-completion boundary

```yaml
P2: PARTIAL_hardened_buffer_writer_provenance_success_awaiting_research_handoff_and_promotion
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_static_playerPosition_anchor_plus_structural_world_transition_direct_authoritative_player_state_unknown
RUNTIME: PARTIAL_historical_single_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Remaining programme gates

- complete/promote #308 then continue P2 toward framing/pipeline-order/final-egress/harness;
- recover live RUNTIME restart/relogin and provide bounded P0/P1 observation;
- prove direct P0 reads and live P1 authority/restart stability;
- prove A3/A4 action parity where required;
- close semantic protocol/QMeta coverage and finite P0/P1 denominators;
- repair #295/#291 ownership lifecycle before contract mutation;
- final audit/E2E/exact-head CI/PR hygiene/archive/ownership release.
