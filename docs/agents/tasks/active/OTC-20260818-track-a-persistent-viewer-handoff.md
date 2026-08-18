---
task_id: OTC-20260818-track-a-persistent-viewer-handoff
track_id: official-client-re
status: implementing
agent: ChatGPT
session_id: chatgpt-persistent-viewer-handoff-20260818-1641
session_role: implementer
project_lane: otclient
lane: RUNTIME
task_kind: implementation
phase: validate
branch: fix/OTC-20260818-track-a-persistent-viewer-handoff
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
pull_request: 541
risk: high
updated: 2026-08-18T17:04:00+02:00
policy_version: 2
execution_mode: github_only
execution_reason: repository tooling and deterministic tests are implemented through GitHub; physical Synology validation is deferred until it can be isolated from the active native-login owner
validation_level: heavy
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive Track A controller/viewer lifecycle change, with repository implementation first and physical consumer validation after promotion
feature_scope:
  type: infrastructure
  user_facing: true
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: true
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
gameplay_allowed: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-track-a-persistent-viewer-handoff.md
  - docs/agents/evidence/OTC-20260818-track-a-persistent-viewer-handoff/**
  - .github/scripts/tibia-official-client-re-canonical-live-handoff.py
  - .github/scripts/tibia-official-client-re-canonical-live-resume.py
  - .github/scripts/tibia-official-client-re-persistent-viewer.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_handoff.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_resume.py
  - .github/scripts/test_tibia_official_client_re_persistent_viewer.py
  - docs/agents/decisions/ADR-0002-track-a-persistent-viewer-handoff.md
modules_touched:
  - track-a-canonical-controller-lease
  - track-a-canonical-live-runtime
  - track-a-remote-view
acceptance:
  - replacement controller sessions can transfer same-task canonical authority without reusing a historical session_id, while rotating the capability and advancing the lease generation
  - old controller capability is invalid immediately after a successful handoff and cross-task handoff is refused
  - canonical X11 window identity is resolved by the promoted raw-XRes PID ownership helper rather than xdotool --pid
  - browser presentation uses a fixed runner backend on 6081 and a fixed user-facing endpoint on synology:6082, with an identity document proving end-to-end mapping to the exact backend
  - runtime health and viewer health are reported independently; viewer failure never authorizes a Tibia client restart
  - current login/auth/session secrets are never read, printed, persisted, committed, or passed to viewer processes
  - PR #528 remains the current physical native-login/package owner and is not mutated or preempted by this task
integration_dependency: PR #528 may consume the promoted controller/viewer tooling only after this task is independently audited and merged; this task must not use its unmerged governance/code to touch the live official client
invocation_started_at: 2026-08-18T16:41:38+02:00
last_progress_at: 2026-08-18T17:04:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
last_validation_failure: Track A deterministic admission-policy audit rejected the task because track_id was missing; Fresh admission behavior audit passed
next_action: validate the repaired admission record and run the committed controller handoff/resume/viewer tests on the new exact head
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-persistent-viewer-handoff-20260818-1641
  session_started_at: 2026-08-18T16:41:38+02:00
  checkpointed_at: 2026-08-18T17:04:00+02:00
  last_progress_at: 2026-08-18T17:04:00+02:00
  phase: validate
  exact_head: after-admission-fix
  pull_request: 541
  active_operation: GitHub Actions exact-head validation
  external_run_ids: []
  operation_started_at: 2026-08-18T17:04:00+02:00
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: branch and owned paths remain conflict-free and PR #528 continues to own the physical native-login runtime
  next_action: inspect the first exact-head CI result; repair only evidence-backed failures and do not touch PR #528 runtime
---

# Track A persistent viewer and controller handoff

## Objective

Make the canonical official-client runtime a durable programme resource that can survive agent/session replacement without making historical `session_id` values part of runtime identity, while preserving exclusive controller authority and fail-closed exact-runtime checks.

The browser observer must likewise be a stable presentation path rather than a per-agent endpoint. Its public contract is:

```text
canonical X11 display
 -> x11vnc RFB backend
 -> websockify/noVNC runner backend :6081
 -> existing host presentation :6082
 -> http://synology:6082/
```

A public identity document must prove that `:6082` reaches the exact current backend before the viewer is reported healthy.

## Verified trigger evidence

PR #528 run/job `32147631742 / 95745198909` started the updater websockify listener on `6082` and then attempted to publish another relay on host `192.168.1.2:6082`; Docker failed with `listen: address already in use`. Earlier gen16 evidence also proved a healthy client/window/RFB/WebSocket path while the host `6082 -> runner 6081` mapping was wrong.

The resulting design keeps three identities separate:

```text
runtime identity      = registration + boot/PID/start/exact client/display/XID
controller identity   = task + current disposable session + rotated capability
viewer identity       = runtime registration binding + fixed backend/public mapping
```

## Implemented repository slice

The branch now contains:

- a fail-closed same-task lease handoff that discovers the previous controller session from authoritative state, rotates the capability and increments generation;
- a high-level resume/release helper that derives the replacement GitHub Actions session id, performs handoff only when explicitly requested, then uses the existing canonical rebind and Gate B transitions;
- a persistent view-only viewer bound to immutable runtime identity and raw-XRes-owned XID, with fixed `5901 -> 6081 -> public 6082` topology;
- an exact `viewer-identity.json` check plus RFB/WebSocket checks so a stale public presentation path cannot masquerade as the current viewer;
- separate runtime and viewer health results so viewer failure does not authorize client restart;
- focused deterministic tests and ADR-0002 documenting the transition boundaries.

## Safety boundary

This task is repository implementation only until its changes are independently audited and promoted. It does not observe, start, stop, restart, attach to, log into, or otherwise mutate the official client. It does not consume Tibia credentials or session material. PR #528 remains the current physical native-login/package owner.

Physical E2E is required before the infrastructure can be called fully deployed. If PR #528 still owns the relevant Synology viewer/runtime surface when repository implementation is ready, the task must checkpoint `waiting` rather than interfere with that live owner.
