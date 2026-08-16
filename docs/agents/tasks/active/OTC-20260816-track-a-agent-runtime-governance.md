---
task_id: OTC-20260816-track-a-agent-runtime-governance
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260816-0836
session_role: coordinator
session_rotation_count: 1
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: implementation
phase: final-independent-remediation
branch: docs/OTC-20260816-track-a-agent-runtime-governance
base_branch: main
base_main: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
risk: medium
related_pr: 324
created: 2026-08-16T08:05:00+02:00
updated: 2026-08-16T08:36:00+02:00
lease_expires_at: 2026-08-16T09:21:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/README.md
  - docs/agents/AGENTS.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-agent-runtime-governance.yml
  - docs/agents/tasks/active/OTC-20260816-track-a-agent-runtime-governance.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-agent-runtime-governance.md
modules_touched:
  - agent-governance
reuses:
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - final Gate A/rebind/Gate B/bootstrap policy merged by PR #311
  - final cancellation-safe manager merged by PR #321
  - current Track A research isolation contract policy v5
depends_on:
  - main@3a5568f36ebc326afd246d0d2da45b5d8eecabfa
  - coordinator PR #300 remains separately owned/released; this task does not edit its changed CHANGELOG/MODULE_CATALOG paths
  - runtime research PR #303 remains separately owned; this task does not access or mutate its runtime surface
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: narrow repository-governance and deterministic policy-audit changes can be completed through the GitHub connector without live runtime access
run_scope: single_task
continuation_policy: protected_merge_then_archive
task_completion_policy: protected_merge_then_archive
user_communication: milestone_only
implementation_authorized: true
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: high
decomposition_decision: single
validation_level: component
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
runtime_access: none
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
last_progress_at: 2026-08-16T08:36:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-final-admission-remediation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
material_review_findings:
  - PRRT_kwDOTVmdjs6ZlHWz: remediated and verified; authorized canonical mutation requires positive equal lease generations after any rebind
  - PRRT_kwDOTVmdjs6ZlHW1: remediated and verified; canonical access is bound to runtime_owner_task == task_id and canonical namespace
  - PRRT_kwDOTVmdjs6ZlHW2: remediated and verified; ephemeral_isolated rejects canonical namespace and aliases
  - PRRT_kwDOTVmdjs6ZlIVI: remediated and verified; universal mandatory docs/agents/README.md entrypoint is workflow-triggered and statically audited
  - PRRT_kwDOTVmdjs6ZlJ8D: active; read_only must require proven uniqueness/non-conflicting target ownership before live observation
  - PRRT_kwDOTVmdjs6ZlKa_: active; runtime-sensitive diff must bind changed Track A admission task to current PR head branch rather than accept any changed Track A task
  - claim_resume_admission: active; admission record must be persisted at Track A claim/resume/checkpoint (`none` for static), not delayed until first live operation
validation_evidence:
  - implementation_parent_head: 90f31bfe42bbc2e8c178e90b7e04a6d69f64c01e
  - track_a_governance_run: 31931442198 SUCCESS
  - policy_audit_job: 95126785784 SUCCESS
  - fresh_behavior_audit_job: 95126785680 SUCCESS
  - repository_ci_run: 31931442374 SUCCESS
  - required_ci_job: 95127228818 SUCCESS
  - released_checkpoint_head: 11300cae0a2d5cc284c08fef2eb48fc3fbaaf71b
last_completed_step: previous implementer released ownership; coordinator independently claimed after verifying waiting/unassigned state and preserved runtime_access=none
next_action: repair read_only target proof, claim/resume persistence, and branch-bound sensitive-path admission; add deterministic negative cases; rerun exact-head governance + repository CI; resolve only verified findings; release for protected merge and archive
---

# Track A agent runtime-governance enforcement

## Goal

Make the final Track A canonical-live runtime rules unavoidable at the normal agent entrypoints, so every current or future Track A researcher classifies runtime access before work and fails closed instead of treating historical `:98`, `6082`, PID/session evidence as current authority.

## Acceptance criteria

- The universally mandatory `docs/agents/README.md` routes every Track A worker to the admission contract at claim/resume; static workers persist `runtime_access: none` before substantial Track A work.
- Track A nested instructions and canonical wrapper require the same admission and re-admission before live work or after material authority/identity change.
- The contract defines a mandatory admission record for `none`, `read_only`, `ephemeral_isolated`, `canonical_reuse_or_mutation`, `canonical_bootstrap`, and `canonical_rebind`.
- `read_only` requires demonstrably non-invasive observation, a declared non-conflicting target boundary, and `target_uniqueness: PROVEN`; otherwise refuse observation.
- Canonical mutation requires current Gate A + any required rebind + Gate B + current-task ownership + authoritative canonical namespace + target uniqueness + positive equal current/registration lease generations + final whole-lifetime supervisor.
- Missing registration routes only to bootstrap; generation mismatch routes only to reviewed rebind.
- Ephemeral runtimes cannot use/alias canonical namespace.
- Historical `:98`, `6082`, PID/session evidence never satisfies current identity.
- Runtime-sensitive PRs cannot satisfy CI using an unrelated changed Track A task record; admission must be bound to the current PR head branch.
- Track A workers may not mutate PR #303-owned runtime or Track B state.
- Deterministic repository tests prevent regression/bypass of these invariants.
- No live Tibia runtime operation is performed by this task.
- Exact-head CI/review are green before merge; task is archived and ownership released afterward.

## Current safety boundary

This task itself is `runtime_access: none`. No X11/RFB/Tibia process/login/session/credentials/canonical state/PR #303 runtime/Track B runtime is inspected or mutated.

## Promotion boundary

This PR is governance-only. Runtime E2E is `NOT_APPLICABLE_WITH_REASON`: no live runtime is exercised because the deliverable is admission policy and deterministic repository enforcement. The relevant component E2E is policy validator + fresh negative/positive behavior cases + repository CI.
