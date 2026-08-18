---
task_id: OTC-20260818-track-a-persistent-viewer-handoff
track_id: official-client-re
status: waiting
agent: ChatGPT
session_id: chatgpt-persistent-viewer-handoff-20260818-1641
session_role: implementer
project_lane: otclient
lane: RUNTIME
task_kind: implementation
phase: physical-e2e-wait
branch: fix/OTC-20260818-track-a-persistent-viewer-handoff
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
pull_request: 541
risk: high
updated: 2026-08-18T17:30:49+02:00
policy_version: 2
execution_mode: github_only
execution_reason: repository implementation and deterministic validation are complete enough for review; physical Synology E2E is blocked by the active native-login runtime owner and absence of a current canonical registered client
validation_level: heavy
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive Track A controller/viewer lifecycle change, with repository implementation first and physical consumer validation only after the existing native-login runtime owner provides a current canonical registered exact client
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
  - .github/scripts/tibia-official-client-re-canonical-live-xres-probe.py
  - .github/scripts/tibia-official-client-re-persistent-viewer.py
  - .github/scripts/tibia-official-client-re-persistent-viewer-controller.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_handoff.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_resume.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_xres_probe.py
  - .github/scripts/test_tibia_official_client_re_persistent_viewer.py
  - .github/scripts/test_tibia_official_client_re_persistent_viewer_controller.py
  - .github/workflows/tibia-official-client-re-persistent-viewer-validation.yml
  - docs/agents/AGENTS.md
  - docs/agents/contracts/TRACK_A_CONTROLLER_HANDOFF_AND_VIEWER_V1.md
  - docs/agents/decisions/ADR-0002-track-a-persistent-viewer-handoff.md
modules_touched:
  - track-a-canonical-controller-lease
  - track-a-canonical-live-runtime
  - track-a-remote-view
acceptance:
  - replacement controller sessions can transfer same-task canonical authority without reusing a historical session_id, while rotating the capability and advancing the lease generation
  - old controller capability is invalid immediately after a successful handoff and cross-task handoff is refused
  - canonical reuse/rebind/Gate B window identity is resolved by raw XRes PID ownership rather than xdotool --pid
  - supported viewer start performs Gate B with the raw-XRes canonical probe before creating persistent observer processes
  - browser presentation uses a fixed runner backend on 6081 and a fixed user-facing endpoint on synology:6082, with an identity document proving end-to-end mapping to the exact backend
  - runtime health and viewer health are reported independently; viewer failure never authorizes a Tibia client restart
  - current login/auth/session secrets are never read, printed, persisted, committed, or passed to viewer processes
  - PR #528 remains the current physical native-login/package owner and is not mutated or preempted by this task
integration_dependency: PR #528 must first produce a current admitted canonical registered exact client and release or explicitly reconcile the required runtime surface; only then may this task perform its serialized physical viewer/controller handoff E2E
repository_implementation_head_before_wait_checkpoint: 65e96d7110215ed6a49d391a2d466824fb8ea509
repository_validation_previous_head: 9f37981f1b74b5568588cd48e4a16baa06cc1ef0
repository_validation_previous_head_result: PASS
repository_validation_previous_head_runs:
  - Track A agent runtime governance 32153925510 PASS
  - Track A persistent viewer validation 32153925542 PASS
  - CI 32153925771 PASS
fresh_audit_head: 65e96d7110215ed6a49d391a2d466824fb8ea509
fresh_audit_runs_started:
  - Track A persistent viewer validation 32154852910
  - Track A agent runtime governance 32154852832
  - CI 32154853493
physical_blocker_owner_task: OTC-20260818-native-login-to-ingame-e2e
physical_blocker_owner_pr: 528
physical_blocker_owner_phase: exact-sha-native-route-reproof
physical_blocker_current_exact_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
physical_blocker_current_exact_client_size: 52109920
physical_blocker_canonical_registration_present: false
physical_blocker_canonical_session_present: false
physical_blocker_retained_observer_url: http://192.168.1.2:6083/
physical_blocker_retained_observer_display: ':99'
invocation_started_at: 2026-08-18T16:41:38+02:00
last_progress_at: 2026-08-18T17:30:49+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
last_validation_failure: the first raw-XRes probe run failed only in its new unittest harness; the harness was corrected and the later exact-head persistent-viewer validation passed before the fresh-audit commit
blocker: physical E2E cannot run while PR #528 owns the Synology runtime surface and no current canonical registered exact client exists
next_action: after PR #528 establishes a current admitted canonical registered exact client and releases or reconciles the runtime surface, run the serialized physical controller-handoff plus viewer persistence E2E on Synology; then freeze the final head, require fresh audit and exact-head CI PASS, and merge/archive PR #541
recovery:
  policy_version: 1
  generation: 3
  session_id: chatgpt-persistent-viewer-handoff-20260818-1641
  session_started_at: 2026-08-18T16:41:38+02:00
  checkpointed_at: 2026-08-18T17:30:49+02:00
  last_progress_at: 2026-08-18T17:30:49+02:00
  phase: physical-e2e-wait
  exact_head: waiting-checkpoint-commit
  pull_request: 541
  active_operation: none
  external_run_ids: [32154852910, 32154852832, 32154853493]
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: waiting
  safe_to_resume: true
  resume_condition: PR #528 no longer conflicts with the required canonical runtime surface and a current exact canonical runtime registration exists
  next_action: run the serialized physical controller-handoff and persistent-viewer E2E on the newly registered canonical exact client without creating a second official-client session
---

# Track A persistent viewer and controller handoff

## Objective

Make the canonical official-client runtime a durable programme resource that survives replacement agent/session turnover without making historical `session_id` values part of runtime identity, while preserving exclusive controller authority and fail-closed exact-runtime checks.

The browser observer is a stable presentation path rather than a per-agent endpoint:

```text
canonical X11 display
 -> x11vnc view-only RFB :5901
 -> websockify/noVNC runner backend :6081
 -> host presentation :6082
 -> http://synology:6082/
```

A public `viewer-identity.json` proves that `:6082` reaches the exact current backend and exact immutable runtime binding before viewer health can be `PASS`.

## Verified trigger evidence

PR #528 run/job `32147631742 / 95745198909` started an updater websockify listener on `6082` and then attempted to publish another relay on host `192.168.1.2:6082`; Docker failed with `address already in use`. Earlier gen16 evidence separately proved a healthy client/window/RFB/WebSocket path while the host presentation mapping was wrong.

The design therefore keeps these identities separate:

```text
runtime identity      = registration + boot/PID/start/exact client/display/raw-XRes XID
controller identity   = task + current disposable session + rotated capability + lease generation
viewer identity       = immutable runtime binding + viewer instance + fixed backend/public mapping
```

## Implemented repository slice

The branch contains:

- fail-closed same-task lease handoff that discovers the prior controller session from authoritative lease state, rotates the capability and increments generation;
- high-level resume/release helper that derives a replacement GitHub Actions session id and never needs the historical session id;
- raw-XRes canonical reuse probe for rebind/Gate B, replacing `xdotool --pid` as window ownership authority on the reuse path;
- authority-aware persistent-viewer controller that requires Gate B with the raw-XRes probe before viewer start;
- persistent view-only viewer bound to immutable runtime identity, with fixed `5901 -> 6081 -> public 6082` topology;
- exact `viewer-identity.json`, RFB and WebSocket checks so a stale public presentation path cannot masquerade as the current viewer;
- separate runtime/viewer health classification so viewer failure never authorizes a client restart;
- deterministic tests, a fresh independent validator job, ADR-0002 and the operational handoff/viewer contract.

## Current physical blocker

The current native-login owner, PR #528, has successfully installed the current official Linux client (`sha256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, size `52109920`) and retains an isolated observer at `http://192.168.1.2:6083/` on `DISPLAY=:99`.

It has **not** yet bootstrapped or registered the new exact canonical client. Its task explicitly records `current_registration_present: false` and `current_canonical_session_present: false` while it re-proves the new exact-SHA native auth/character/IN_GAME routes.

Therefore the final #541 physical proof cannot truthfully run yet. Creating another official-client runtime/session or taking over PR #528's namespace would violate the Track A ownership model. The repository implementation remains reviewable, but this task stays `waiting` until the current owner supplies the canonical runtime required by the physical handoff test.

## Physical completion gate

When the current canonical exact client exists and ownership is available, one serialized E2E must prove:

1. controller A passes Gate B;
2. viewer health is PASS through exact public `:6082` identity and WebSocket mapping;
3. controller authority is released/replaced without terminating the client/viewer;
4. controller B gets a fresh session/capability/generation without reusing A's historical `session_id`;
5. required rebind + Gate B pass via raw XRes;
6. the same runtime identity and viewer instance remain healthy;
7. no second official-client login/session is created;
8. no Tibia credential or auth/session secret is accessed by the viewer/handoff test.
