---
task_id: OTC-20260818-track-a-persistent-viewer-handoff
track_id: official-client-re
status: implementing
agent: ChatGPT
session_id: chatgpt-track-a-kasmvnc-20260818-1735
session_role: implementer
project_lane: otclient
lane: RUNTIME
task_kind: implementation
phase: kasmvnc-physical-deploy
branch: fix/OTC-20260818-track-a-persistent-viewer-handoff
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
pull_request: 541
risk: high
updated: 2026-08-18T17:35:00+02:00
policy_version: 2
execution_mode: github-orchestrated-synology
execution_reason: deploy a real persistent KasmVNC desktop on synology-otclient-01, isolated from the active native-login runtime, so browser desktop identity no longer depends on noVNC or an agent session
validation_level: heavy
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: preserve the validated controller-handoff work, replace the presentation implementation with a task-owned persistent KasmVNC desktop, then integrate the official client into that desktop only after the current native-login owner releases or explicitly reconciles its client runtime surface
feature_scope:
  type: infrastructure
  user_facing: true
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: ephemeral_isolated
persistent_session_role: none
physical_e2e_required: true
runtime_owner_task: OTC-20260818-track-a-persistent-viewer-handoff
runtime_namespace: track-a-kasmvnc-desktop
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
live_runtime_authorization_source: owner explicitly requested replacement of noVNC with KasmVNC and physical deployment on 2026-08-18; authorization covers only the isolated KasmVNC desktop and excludes the official client, credentials, login and gameplay
kasm_container: otclient-track-a-kasmvnc
kasm_image: kasmweb/ubuntu-noble-desktop:1.17.0
kasm_state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260818-track-a-persistent-viewer-handoff/kasmvnc
kasm_host_port: 6901
kasm_container_port: 6901
kasm_internal_display: ':1'
kasm_public_url: https://192.168.1.2:6901/
kasm_restart_policy: unless-stopped
protected_concurrent_owner_task: OTC-20260818-native-login-to-ingame-e2e
protected_concurrent_owner_pr: 528
protected_concurrent_display: ':99'
protected_concurrent_url: http://192.168.1.2:6083/
protected_concurrent_canonical_lease: untouched
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-track-a-persistent-viewer-handoff.md
  - docs/agents/evidence/OTC-20260818-track-a-persistent-viewer-handoff/**
  - .github/workflows/tibia-official-client-re-kasmvnc-deploy.yml
  - .github/scripts/tibia-official-client-re-canonical-live-handoff.py
  - .github/scripts/tibia-official-client-re-canonical-live-resume.py
  - .github/scripts/tibia-official-client-re-canonical-live-xres-probe.py
  - .github/workflows/tibia-official-client-re-persistent-viewer-validation.yml
  - docs/agents/contracts/TRACK_A_CONTROLLER_HANDOFF_AND_VIEWER_V1.md
  - docs/agents/decisions/ADR-0002-track-a-persistent-viewer-handoff.md
modules_touched:
  - track-a-controller-handoff
  - track-a-kasmvnc-desktop
  - track-a-runtime-presentation
acceptance:
  - KasmVNC is the actual persistent browser desktop provider; no x11vnc/websockify/noVNC chain is used for the new desktop
  - one task-owned Docker container named otclient-track-a-kasmvnc remains alive after the GitHub Actions deployment job exits
  - the stable LAN endpoint is https://192.168.1.2:6901/ and returns the KasmVNC web application
  - the Kasm desktop has its own isolated display and namespace and does not attach to, stop, reconfigure or replace PR #528 display :99 or port 6083
  - no TIBIA_TEST_EMAIL, TIBIA_TEST_PASSWORD, canonical lease capability or official-client session material is passed to the Kasm container
  - replacement agent sessions do not create a new Kasm desktop; they reuse the same container and endpoint
  - existing same-task controller handoff remains fail-closed and does not use historical session_id as runtime identity
  - an official Tibia client is not started inside the new Kasm desktop until the active native-login owner releases or explicitly reconciles that client runtime surface
integration_dependency: KasmVNC desktop deployment itself is independent and may proceed now in the isolated track-a-kasmvnc-desktop namespace; migration of the official client into Kasm waits for PR #528 runtime ownership reconciliation
invocation_started_at: 2026-08-18T17:35:00+02:00
last_progress_at: 2026-08-18T17:35:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: deploy the isolated KasmVNC Docker desktop on synology-otclient-01 at HTTPS port 6901 and prove the endpoint and container persistence without touching PR #528 state
recovery:
  policy_version: 1
  generation: 4
  session_id: chatgpt-track-a-kasmvnc-20260818-1735
  session_started_at: 2026-08-18T17:35:00+02:00
  checkpointed_at: 2026-08-18T17:35:00+02:00
  last_progress_at: 2026-08-18T17:35:00+02:00
  phase: kasmvnc-physical-deploy
  exact_head: admission-update
  pull_request: 541
  active_operation: create isolated KasmVNC deployment workflow
  external_run_ids: []
  operation_started_at: 2026-08-18T17:35:00+02:00
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: container name otclient-track-a-kasmvnc and host port 6901 remain unowned or owned only by this exact task; PR #528 :99/6083/canonical lease remain untouched
  next_action: execute the task-owned KasmVNC deployment and verify HTTPS 6901 from the Synology runner
---

# Track A persistent KasmVNC desktop and controller handoff

## Objective

Replace the previous noVNC presentation design with a **real persistent KasmVNC desktop** on Synology. KasmVNC owns its own X desktop and browser transport; it is not a viewer attached to the old `Xvfb -> x11vnc -> websockify -> noVNC` chain.

The target user path is:

```text
browser
  -> HTTPS 192.168.1.2:6901
  -> KasmVNC web server / websocket
  -> persistent Kasm desktop DISPLAY=:1 inside task-owned container
```

The Kasm desktop is a durable programme resource. Replacement ChatGPT/GitHub Actions sessions reuse the same container and URL rather than creating a new GUI session.

## Current physical isolation

PR #528 remains the owner of the native-login runtime surface. Its retained legacy observer is `DISPLAY=:99` / `http://192.168.1.2:6083/`, and its canonical registration is currently absent. This task therefore deploys KasmVNC **without launching the official Tibia client** and without touching #528's display, port, processes, canonical lease, state directory or credentials.

The Kasm deployment uses only:

```text
container: otclient-track-a-kasmvnc
host port: 6901
container port: 6901
container display: :1
state: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260818-track-a-persistent-viewer-handoff/kasmvnc
```

## Security boundary

The deployment must not read or reference `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD`. It must not receive a canonical lease token/capability. Its own browser password is generated into the task-private state directory with mode `0600` and is unrelated to Tibia authentication.

## Migration after desktop deployment

Once PR #528 releases or explicitly reconciles the official-client runtime surface, the official native Linux client launch/bootstrap path can be migrated to execute inside this persistent Kasm desktop. Until then, the immediate deliverable is a verified, reachable, persistent KasmVNC desktop that replaces noVNC as the user-facing GUI technology for future Track A runtime work.
