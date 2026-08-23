---
task_id: OTC-20260823-tibia-re-control-center-package-b
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P2-CONTROL-API
track_id: official-client-re
task_kind: implementation
phase: design
risk: medium
branch: feat/OTC-20260823-tibia-re-control-center-package-b
base_branch: main
base_sha: 63100340f0dbe1aba16a20bc7febc8613291583d
created: 2026-08-23T12:42:22+02:00
updated: 2026-08-23T12:42:22+02:00
execution_mode: remote_desktop+github_connector+github_actions
execution_budget_minutes: 120
execution_budget_reason: cohesive Package B full-stack slice requires persistent safety/request storage, secured loopback HTTP transport, browser+CLI integration, restart E2E, fresh audit, exact-head CI, merge and mandatory archive closeout
invocation_started_at: 2026-08-23T12:34:00+02:00
last_progress_at: 2026-08-23T12:42:22+02:00
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: Package B is one coupled transport/persistence/domain/UI idempotency boundary; parallel edits would race shared RequestLedger and API semantics
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
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
transaction_authorized: false
network_listener_allowed: loopback_control_api_only
control_api_listener: loopback_only
official_client_access: false
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
feature_scope:
  type: full_stack
  user_facing: true
  backend_required: true
  frontend_required: true
  integration_required: true
  e2e_required: true
  completion_claim: complete_feature
complete_control_center_programme: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-b.md
  - docs/agents/tasks/archive/OTC-20260823-tibia-re-control-center-package-b.md
  - docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-b/**
  - tools/tibia_re_control_center/persistent_store.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/control_api.py
  - tools/tibia_re_control_center/control_cli.py
  - tools/tibia_re_control_center/control_ui.py
  - tests/tools/tibia_re_control_center/test_package_b.py
  - tests/tools/tibia_re_control_center/audit_package_b.py
  - .github/workflows/tibia-re-control-center-package-b.yml
read_only_paths:
  - tools/tibia_re_surveyor/**
  - tests/tools/tibia_re_surveyor/**
  - tools/tibia_runtime_bridge/**
  - Package C task/evidence/branch paths
  - Package D task/evidence/branch paths
  - existing Package A core files unless a narrowly required compatibility repair is proven and ownership remains free
depends_on:
  - Package A terminal merge 13b3f02a07a176662d766352d9af39619775a73d
  - Control Center contracts and lifecycle closeout on current main
blocks: []
ownership_released: false
next_action: implement durable RequestLedger/store and secured Control API domain path
---

# Control Center Package B — local Control API, browser, CLI and persistence

## Objective

Implement the complete Package B slice over merged Package A: persistent backend-global RequestLedger/ControlState and per-run safety state, exact loopback-only Control API v1, thin same-backend browser and CLI clients, fake-adapter one-step experiments, STOP/reset/restart safety, truthful status views and real local E2E. Official Tibia access and mutation remain forbidden.

## Preflight evidence

Fresh fetch on `main@63100340f0dbe1aba16a20bc7febc8613291583d` verified Package A is terminally merged (`#628`, merge `13b3f02a07a176662d766352d9af39619775a73d`). Package C is concurrently active in its own `surveyor_provider.py`/test/task/evidence paths; Package B owns only the paths declared above. No Package B task/branch/PR existed at claim time.

## Acceptance inventory

- [ ] 01 exact IPv4 loopback bind; wildcard/non-loopback refused
- [ ] 02 fresh >=256-bit nonce per backend epoch; never URL/log/artifact/argv
- [ ] 03 every `/v1/*` request authenticated by nonce
- [ ] 04 exact Host allowlist and exact same-origin Origin enforcement
- [ ] 05 no permissive CORS or cookie ambient authentication
- [ ] 06 bounded body/header/page/event/subscriber/backpressure behavior
- [ ] 07 stable non-secret ControlApiError envelope
- [ ] 08 durable backend-global RequestLedger with canonical request hash
- [ ] 09 every POST persists ACCEPTED + final resource identity before domain execution
- [ ] 10 domain uses exactly reserved resource/control-transition identity
- [ ] 11 STOP/reset uses reserved transition id as ControlState.transition_id
- [ ] 12 same request id/body replays same resource/result across restart
- [ ] 13 same request id/different body conflicts before domain work
- [ ] 14 FAILED request replays same failed logical request
- [ ] 15 ACCEPTED-before-domain and resource-before-COMPLETED crash windows do not duplicate work
- [ ] 16 delayed STOP/reset replay never mutates newer ControlState
- [ ] 17 graceful shutdown flushes global/per-run safety state before clean marker and invalidates nonce
- [ ] 18 restart preserves original run activation/deadline and Action/Budget safety truth
- [ ] 19 browser and CLI use the same HTTP/domain operations
- [ ] 20 browser reload/new tab cannot duplicate active work
- [ ] 21 UI separates runtime/client/recorder/authority/capability/evidence/freshness/session
- [ ] 22 UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN remain explicit
- [ ] 23 MUTATION_ALLOWED cannot be granted locally
- [ ] 24 mutation-capable controls execute only against explicit FAKE_TEST adapter
- [ ] 25 no official-client/raw/debug/concrete-adapter bypass exists
- [ ] 26 Package A full regression suite remains green
- [ ] 27 persisted artifacts/store and generated evidence contain no nonce/secret
- [ ] 28 actual backend + CLI + browser Package B E2E passes on final head
- [ ] 29 fresh independent Package B falsification audit passes
- [ ] 30 exact-head CI, PR terminal state, task archive and ownership release complete

## Validation evidence

Pending implementation. `OFFICIAL_CLIENT_ACCESS=NONE` for the full task lifetime.
