---
task_id: OTC-20260819-track-a-existing-runtime-adoption
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_infrastructure
phase: ready_exact_head_ci
branch: fix/OTC-20260819-track-a-existing-runtime-adoption
base_branch: main
base_sha: 3e3b3a731cb21d775ae686c65991e90969bb86fb
risk: high
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - .github/workflows/track-a-canonical-live-governance.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260819-track-a-existing-runtime-adoption.md
  - docs/agents/evidence/OTC-20260819-track-a-existing-runtime-adoption/**
modules_touched:
  - canonical-live-transition
  - track-a-runtime-admission
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
depends_on:
  - OTC-20260819-track-a-inventory-containers-live-e2e
blocks:
  - future authenticated D09-D22 reversible GUI validation on the existing logged-in Kasm runtime
track_a_runtime_agent_admission_version: 1
execution_class: github_hosted
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-08-19T14:58:00+02:00
last_progress_at: 2026-08-19T15:44:00+02:00
foreground_budget_minutes: 60
foreground_budget_state: FINAL_READY_SYNC_RESTACK
ci_checks_for_current_head: 0
ci_check_generation: ready
terminal_ci_wait_started_at: 2026-08-19T15:44:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
falsification_findings_resolved:
  - title_derived_ingame_removed_structural_bridge_required
  - docker_runtime_identity_and_adoption_provenance_persisted
focused_transition_tests: 17_OF_17_PASS
focused_kasm_probe_tests: 6_OF_6_PASS
focused_track_a_governance: PASS
focused_py_compile: PASS
focused_workflow_yaml_parse: PASS
focused_git_diff_check: PASS
independent_audit_validator: existing-runtime-adoption-final-validator-v3
independent_audit_result: PASS
independent_audit_open_material_findings: 0
source_audit_review: 4972749177
repaired_source_commit: 2a82d7a0f646ac6c640b791730fb2d0edc984a6f
current_blocker: NONE
next_action: run exact-head required CI on this Ready-state current-main restack; if green, squash-merge PR #596 and complete mandatory lifecycle archive and ownership release; do not use adoption on the live client in this invocation
---

# Track A existing unregistered runtime adoption

## Objective

Implement the missing controller-plane transition identified by the authenticated inventory live task: when authoritative `runtime-registration.json` is absent but exactly one already-running exact official client is proven, allow a reviewed metadata-only adoption transaction to create the canonical registration without launching, logging in, restarting, signalling, injecting into, or otherwise mutating the client.

## Frozen authority boundary

This implementation task has `runtime_access: none`. Its changes do not authorize this invocation to adopt or mutate the currently logged-in client. A later invocation may consume the transition only after the implementation is trusted on `main` and performs fresh Track A admission.

## Acceptance and repaired proof model

Adoption requires current authoritative lease plus canonical flock, absent registration, exactly one exact-fenced target, repeated stable boot/PID/start/size/SHA/display/X11-window/provenance proof and atomic registration. Structural exact-peer `BRIDGE_3_OF_3` is required for `IN_GAME`; title-only evidence remains `UNKNOWN`. The registration persists `runtime_locator`, candidate fingerprint and state-evidence provenance for later Gate B reproduction. Adoption never launches, logs in, stops, signals, attaches to, injects into or otherwise mutates the client, and failures roll back only task-created registration metadata.

The repaired implementation passed 17/17 transition tests and 6/6 Kasm probe tests plus Track A governance, Python compilation, workflow YAML parsing and `git diff --check`. Fresh independent validator `existing-runtime-adoption-final-validator-v3` passed the previous exact implementation tree with zero material findings; the only subsequent change is this task checkpoint and clean no-conflict restack over unrelated Control Center documentation merged to `main`. Final Ready-state exact-head CI is now the remaining implementation-PR gate.
