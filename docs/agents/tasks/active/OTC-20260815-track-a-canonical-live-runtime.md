---
task_id: OTC-20260815-track-a-canonical-live-runtime
status: implementing
agent: ChatGPT
session_id: automation-20260816-0733-canonical-final
session_role: governance-integrator
session_rotation_count: 5
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: implementation
phase: integrate
branch: docs/OTC-20260815-track-a-canonical-live-runtime
base_branch: main
base_main: b0fd474e34c0252220b773b2304d889821080727
risk: high
related_pr: 311
updated: 2026-08-16T07:33:00+02:00
lease_expires_at: 2026-08-16T08:18:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-live-runtime.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-canonical-live-runtime.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-live-runtime/**
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/CHANGELOG.md
depends_on:
  - final cancellation-safe manager merged by PR #321 as main@8828150617d68247be2074b330f4d954e508307b
  - fresh final manager archive merged by PR #322 as main@b0fd474e34c0252220b773b2304d889821080727
  - bootstrap contract PR #318 merged as 9d3b94d4f06a1eba1dacca91a9dd288e1a8af56a and archived by PR #320
  - PR #303 runtime evidence remains factual input only and its runtime-owned surface must not be touched
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: final governance restack, contract reconciliation, review repair and exact-head GitHub validation require no owner-funded AI or live runtime mutation
run_scope: single_task
continuation_policy: protected_merge_then_archive
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: true
invocation_started_at: 2026-08-16T07:16:27+02:00
last_progress_at: 2026-08-16T07:33:00+02:00
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
validation_level: focused
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
claim_reason: previous task checkpoint was explicitly released with session_id null and lease_expires_at null; no active owner existed, so this is a normal replacement integration session rather than stale takeover
material_review_findings:
  - PRRT_kwDOTVmdjs6ZkaMN: final manager needed cancellation-safe lock ownership; repaired and promoted by PR #321/#322
  - PRRT_kwDOTVmdjs6ZkaMO: sequential reuse needs a dedicated under-lock fail-closed registration generation-rebind transition before Gate B current-generation equality
last_completed_step: manager cancellation P1 is repaired, exact-head validated, protected-merged and freshly archived; current main and both unresolved PR #311 findings were reverified before this claim
next_action: clean-restack PR #311 on current main, reconcile Gate A/bootstrap to PR #321/#322, define fail-closed generation rebinding, then run fresh audit and exact-head CI
---

# Objective

Finish Track A canonical-live runtime governance on the final cancellation-safe manager and bootstrap contracts while preserving strict separation between controller authority, current runtime identity, registration-generation rebinding and initial creation.

# Required final boundary

- Gate A: current authoritative lease plus final cancellation-safe out-of-band supervisor for the entire mutation/process-tree lifetime.
- Registration rebind: when the exact registered runtime survives into a newer controller lease generation, a dedicated under-lock fail-closed metadata transition must freshly prove unchanged exact runtime identity and uniqueness, atomically bind the authoritative registration to the current lease generation, and re-read/revalidate it before Gate B can pass. This transition cannot create or repair a missing/changed runtime and is not an ad-hoc JSON edit.
- Gate B: after any required rebind, current exact-runtime registration/preflight proves PID/process-start identity, exact version/size/SHA, display/window and mutation-relevant state and matches the current validated lease generation.
- Initial creation/bootstrap: separate fail-closed transition; it is not ordinary Gate B reuse or generation rebinding.
- Exact client fence: `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` until direct evidence.
- PR #303 runtime-owned paths/processes and Track B remain untouched.
