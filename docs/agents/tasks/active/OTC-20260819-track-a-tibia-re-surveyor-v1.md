---
task_id: OTC-20260819-track-a-tibia-re-surveyor-v1
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: research_infrastructure
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
branch: feat/OTC-20260819-track-a-tibia-re-surveyor-v1
base_branch: main
base_sha: 724f020dd33839533c1bcaa2a7102b9d79566431
risk: medium
owned_paths:
  - tools/tibia_re_surveyor/**
  - tests/tools/tibia_re_surveyor/**
  - docs/agents/tasks/active/OTC-20260819-track-a-tibia-re-surveyor-v1.md
  - docs/agents/evidence/OTC-20260819-track-a-tibia-re-surveyor-v1/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - tibia-re-surveyor
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
  - tools/tibia_runtime_bridge/**
depends_on: []
blocks: []
cross_repository_task_ids: []
track_a_runtime_agent_admission_version: 1
execution_class: hybrid
runtime_access: read_only
persistent_session_role: observer
runtime_owner_task: OTC-20260819-track-a-tibia-re-surveyor-v1
runtime_namespace: synology:otclient-track-a-kasmvnc:display-1:client-11365
canonical_registration: ABSENT
canonical_lease_generation: 16
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
owner_current_instruction: build a mass TIBIA-RE surveyor, include approximately ten-minute anti-idle rotation, then run it against the already-running client session
current_client_version_token: "15.32"
current_client_size: 52109920
current_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
invocation_started_at: 2026-08-19T13:45:00+02:00
last_progress_at: 2026-08-19T14:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
current_blocker: current KasmVNC client remains read-only admitted but canonical registration is absent and generation-16 lease is expired; real anti-idle rotation is therefore not currently legal
next_action: complete repository integration/readiness validation on PR #592; real rotation may be exercised only after a separately valid current canonical mutation admission exists
---

# TIBIA-RE Surveyor v1

## Objective

Create a reusable deterministic harness that converts the canonical 169-row full-client RE matrix, existing structured evidence and a bounded current-runtime snapshot into compact machine-readable evidence for later agents.

The harness must reduce repeated manual census work without converting lexical/static presence into semantic proof. It may recommend the next evidence gap, but it never promotes a canonical row to `DONE` by itself.

## Anti-idle boundary

The owner requested an approximately ten-minute turn-in-place keepalive for the already-running research session. Trusted-base governance already defines the shared heartbeat `/tmp/otclient-track-a-last-activity`, shared lock `/tmp/otclient-track-a-gui-input.lock`, an eight-minute trigger threshold and safe rotation as the preferred minimal stimulus.

Implementation preserves that contract and fails closed: an unregistered/read-only target is observable but not mutable. A run without canonical registration, current lease/Gates and GUI authority emits `KEEPALIVE_SKIPPED_UNAUTHORIZED` and sends no keyboard/mouse input. Anti-idle events are explicitly excluded from subsystem semantic proof.

## Acceptance progress

- PASS — parse all 169 canonical coverage IDs and statuses deterministically;
- PASS — index structured task evidence without trusting it as canonical status authority;
- PASS — capture a secret-free current runtime identity/uniqueness/control-plane snapshot;
- PASS — emit compact `coverage.json`, `agent_bundle.json` and human summary;
- PASS — rank next experiments only from explicit canonical status/dependency data;
- PASS — implement shared heartbeat/lock keepalive scheduling with an authority gate and no duplicate input;
- PASS — keep anti-idle events explicitly excluded from subsystem semantic evidence;
- PASS — 13 focused unit tests cover coverage parsing, evidence indexing, runtime normalization and keepalive allow/refuse paths;
- PASS — run the surveyor against the current `otclient-track-a-kasmvnc` session;
- PASS — no login, credential read, transaction, attach/injection or process-memory mutation occurred;
- BLOCKED — real keepalive rotation on the current session, because current canonical mutation admission does not exist.

## Current-session validation checkpoint

```yaml
phase: post_live_current_session_validation
executed_remote_head: 577fc48e123974adca68e06dea48d59aa4d1a127
focused_tests: 13_PASS
remote_diff_check: PASS
canonical_rows: 169
coverage_counts:
  DONE: 14
  PARTIAL: 95
  NOT_STARTED: 56
  BLOCKED: 4
runtime_access_result: READ_ONLY_ADMITTED
target_uniqueness_result: PROVEN
candidate_process_count: 1
client_pid: 11365
client_start_ticks: 74970818
exact_current_fence_match: true
canonical_registration_present: false
canonical_lease_generation: 16
canonical_lease_expired: true
keepalive_due: true
keepalive_result: KEEPALIVE_SKIPPED_UNAUTHORIZED
surveyor_input_sent: false
heartbeat_present_after_run: false
gui_lock_present_after_run: false
rows_with_evidence_mentions: 88
rows_with_current_sha_refs: 64
total_evidence_file_mentions: 272
privacy_secret_scan: PASS
durable_evidence: docs/agents/evidence/OTC-20260819-track-a-tibia-re-surveyor-v1/20260819-current-kasm-live-run.md
next_action: keep PR Draft until repository integration, exact-head CI and required independent audit are complete; do not manufacture registration merely to demonstrate rotation
```
