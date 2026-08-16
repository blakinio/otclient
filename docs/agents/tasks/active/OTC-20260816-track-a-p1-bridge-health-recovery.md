---
task_id: OTC-20260816-track-a-p1-bridge-health-recovery
status: implementing
agent: ChatGPT
session_id: agent-20260816-p1-bridge-001
session_role: researcher
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: bridge-health-recovery
branch: feat/OTC-20260816-track-a-p1-bridge-health-recovery
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
created: 2026-08-16T13:14:00+02:00
updated: 2026-08-16T13:14:00+02:00
risk: medium
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-p1-bridge-health-recovery.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
modules_touched:
  - Track A official-client runtime bridge tooling
reuses:
  - "PR #283 accepted bounded read-only bridge source/evidence (closed unmerged)"
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P1_BRIDGE_ALIAS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
depends_on:
  - "PR #283 historical accepted source; blobs are reused only after exact comparison"
  - "PR #303 / RUNTIME only for later physical attach/restart/relogin evidence; not mutated by this task"
blocks: []
cross_repository_tasks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub connector plus GitHub-hosted Actions are sufficient; owner-funded Codex/API use is forbidden
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
decomposition_decision: single
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
stale_takeover_count: 0
human_interruptions: 0
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
track_a_runtime_admission:
  track_id: official-client-re
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
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-08-16T13:10:00+02:00
last_progress_at: 2026-08-16T13:14:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Rebuild the coordinator-accepted PR #283 read-only runtime bridge on current `main`, then add a deterministic fail-closed P1 health/reacquisition/recovery layer that is testable on GitHub-hosted runners and consumes only explicit runtime identity supplied by an admitted runtime producer.

The P1 layer must never bootstrap, launch, login, restart, kill, attach to, reconfigure, or guess the canonical physical runtime. Real attach/reacquisition/restart/relogin proof remains RUNTIME-owned.

# Current factual basis

- Current dispatch base is `main@0d7b2607912552599ae501891491aab439cfde7b`.
- PR #283 is closed unmerged, but its bounded read-only bridge implementation was explicitly accepted by the coordinator; its source/test blobs are not present on current `main`.
- No open PR currently owns `tools/tibia_runtime_bridge/**` or `tests/tools/tibia_runtime_bridge/**`.
- PR #303 owns separate runtime surfaces; this task consumes only durable evidence and performs no live observation or mutation.
- Current canonical runtime identity remains unclaimed here: `:98 = UNKNOWN`, `6082 = UNKNOWN`, PID/session = `NOT_REGISTERED`.

# Acceptance inventory

- [ ] Rebuild the exact accepted PR #283 bridge/tool/test baseline on this current-main branch and prove the reused blobs match the accepted source.
- [ ] Preserve exact profile/hash fencing, owner-only local IPC, bounded request framing, read-only discovery and derived `session-status` semantics.
- [ ] Add an explicit runtime identity model suitable for RUNTIME-produced registrations/evidence without reading or mutating the canonical runtime from P1.
- [ ] Add fail-closed bridge health classification that distinguishes ready/not-ready, unreachable, malformed response and stale/changed identity without promoting `session-status` to authoritative `IN_GAME`.
- [ ] Add deterministic reacquisition that binds only to a fresh explicit identity/endpoint, rejects absent identity, exact-fence mismatch, generation regression/change during probe and process identity change, and drops stale cached channels.
- [ ] Add bounded recovery semantics that may retry/reacquire a newly supplied identity but never starts/restarts/logs in a client or invents PID/display/socket data.
- [ ] Cover healthy, unavailable, malformed, identity-change race, stale generation, replacement endpoint, retry exhaustion and recovery-success paths with deterministic tests.
- [ ] Keep all prior #283 focused tests passing.
- [ ] Run proportional GitHub-hosted focused/component validation and exact-head repository CI required for this Draft head.
- [ ] Perform a fresh post-implementation audit with zero open material findings before handoff.
- [ ] Leave the result as `DRAFT_NOT_PROMOTED`; do not merge or promote P1 conclusions.

# Evidence boundary

`session-status` remains a structural candidate with evidence level `DERIVED_UNTIL_LIVE_CORRELATION`. This task may prove API/lifecycle behavior under deterministic hosted simulation; it cannot prove physical attach, real restart/relogin stability, canonical session readiness, authoritative player position or gameplay actions.

# Checkpoint

```yaml
status: implementing
last_completed_step: claimed current-main P1 lane with runtime_access none and non-overlapping bridge paths
blockers: []
next_action: reconstruct the accepted PR #283 bridge baseline exactly, inspect its public Python API, then implement the smallest fail-closed health/reacquisition/recovery layer with deterministic tests
```
