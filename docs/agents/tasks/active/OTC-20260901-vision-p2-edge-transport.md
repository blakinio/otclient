---
task_id: OTC-20260901-vision-p2-edge-transport
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: worker_local_commit_ready_waiting_main
branch: feat/OTC-20260901-vision-p2-edge-transport
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T21:07:53+02:00
risk: high
execution_class: github_hosted
execution_mode: isolated_worker_branch
preferred_execution: codex
run_scope: wave_1_worker
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
worktree: C:/Users/barte/otclient-vision-p2-edge-transport
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
related_prs:
  - PR #829 Wave 1 worker Draft
current_blocker: coordinator runtime-signals promotion PR #839 must merge before final current-main restack/push to avoid a known-stale base
next_action: after PR #839 merges, refresh main, restack this committed edge-transport slice once, rerun exact local gates, then push Draft PR #829 and observe exact-head CI
invocation_started_at: 2026-09-01T17:03:28+02:00
last_progress_at: 2026-09-01T21:07:53+02:00
ci_checks_for_current_head: 0
ci_check_generation: local-replay-race-repaired-30-pass
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# OTC-VISION-P2-EDGE-TRANSPORT

## Mission

Implement a narrow authenticated bounded Synology-to-Molehill edge transport with versioned metadata and content-addressed artifacts, without generic shell, raw GUI control or authority expansion.

## Dispatch boundary

This task is bootstrapped by `OTC-VISION-P2-COORDINATOR`. The worker may mutate repository files only after its own isolated session validates the exact task, branch, worktree and Draft PR and confirms the ownership set below remains non-overlapping. Real Official Tibia runtime observation is **not authorized** by this record. Any later transition from `runtime_access: none` to `read_only` requires a coordinator-assigned single observation window, fresh exact-target proof, and a persisted valid read-only admission record before observation.

## Binding reads

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Owned paths

- `docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md`
- `docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md`
- `tools/tibia_re_control_center/agent_edge_transport.py`
- `tests/tools/tibia_re_control_center/test_agent_edge_transport.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
TASK_ID: OTC-20260901-vision-p2-edge-transport
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
PROJECT_LANE: otclient
BASE_MAIN: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
BRANCH: feat/OTC-20260901-vision-p2-edge-transport
WORKTREE: C:/Users/barte/otclient-vision-p2-edge-transport
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T21:07:53+02:00
head: 9fce716178820920cac1f605fc5402910c1bed6e
head_semantics: local_replay_race_repair_commit_before_docs_checkpoint
branch: feat/OTC-20260901-vision-p2-edge-transport
pr: 829
status: validating
phase: worker_local_commit_ready_waiting_main
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - edge-transport
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
proven:
  - local implementation plus replay-race repair is committed through 9fce716178820920cac1f605fc5402910c1bed6e; branch remains unpushed while coordinator runtime-signals promotion PR #839 is pending.
  - runtime_access remains none; all mutation/runtime-effect authority remains false and physical action count/budget remain 0/0.
  - outbound-only transport mutually authenticates peers with distinct directional HMAC-SHA256 keys and grants no runtime/action authority.
  - signed metadata is bounded, versioned, freshness/connection/replay fenced and recursively rejects generic shell/process/GUI/secret-getter surfaces.
  - artifact descriptors bind SHA-256, exact size and media type; bytes travel separately with exact receiver integrity checks.
  - empirical parser debugging corrected a stale test-only recursion depth assumption without changing production behavior.
  - independent concurrency falsification proved two simultaneous verify calls could both accept the same sequence before atomic replay state commit.
  - RED test test_concurrent_duplicate_receive_advances_replay_window_once reproduced two successful accepts for sequence 1.
  - verifier now validates packet contents first and atomically commits connection/replay state under one RLock; bind_connection uses the same state lock.
  - after repair exactly one concurrent duplicate is accepted and one fails EDGE_REPLAY_REJECTED.
  - fresh focused suite passes 30/30; protocol+transport component suite passes 47/47; Ruff, py_compile, checkpoint validation, Track A governance and git diff --check pass.
derived:
  - repository/static transport producer is locally coherent and replay-safe under concurrent verifier use.
  - transport peer authentication remains authority-neutral and cannot establish Track A admission, semantic state, evidence freshness or action authority.
unknown:
  - exact-head hosted CI/governance after current-main restack and future publication.
  - coordinator independent classification after publication.
  - real Synology/Kasm/Official Tibia transport evidence; none authorized or attempted.
conflicts: []
first_failure:
  marker: CONCURRENT-REPLAY-WINDOW-RACE
  evidence: deterministic barrier test forced two verifier threads past validation before state commit and both accepted sequence 1; atomic replay-state commit repair reduces acceptance to exactly one.
rejected_hypotheses:
  - production JSON recursion handling was broken: rejected; current decoder simply accepts depth 1100 and production correctly catches RecursionError at deeper nesting.
  - GIL alone makes verifier replay updates atomic: rejected by deterministic two-thread falsification.
  - transport authentication grants runtime/action authority: rejected by fixed authority-neutral envelope and tests.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
validation:
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_edge_transport -q
    result: PASS
    evidence: 30 tests, zero failures/errors after replay-race repair.
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol tests.tools.tibia_re_control_center.test_agent_edge_transport -q
    result: PASS
    evidence: 47 tests, zero failures/errors.
  - command: Ruff and py_compile on edge-transport implementation/test
    result: PASS
    evidence: static validation clean.
  - command: checkpoint validator, Track A governance, git diff --check
    result: PASS
    evidence: all local governance/hygiene gates pass.
blockers:
  - wait for coordinator promotion PR #839 to merge before final current-main restack/push.
next_action: after PR #839 merges, restack once onto current main, rerun local gates, push Draft PR #829 and observe exact-head CI.
```
