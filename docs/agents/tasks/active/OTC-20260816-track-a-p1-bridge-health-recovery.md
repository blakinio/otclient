---
task_id: OTC-20260816-track-a-p1-bridge-health-recovery
status: ready
agent: ChatGPT
session_id: agent-20260816-p1-bridge-001
session_role: researcher
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: handoff
branch: feat/OTC-20260816-track-a-p1-bridge-health-recovery
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
created: 2026-08-16T13:14:00+02:00
updated: 2026-08-16T13:26:57+02:00
risk: medium
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-p1-bridge-health-recovery.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
  - .github/workflows/track-a-p1-bridge-validation.yml
modules_touched:
  - Track A official-client runtime bridge tooling
reuses:
  - "PR #283 accepted bounded read-only bridge source/evidence (closed unmerged)"
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P1_BRIDGE_ALIAS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
depends_on:
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
estimate_confidence: high
validation_level: component
heavy_validation_runs: 1
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-08-16T13:10:00+02:00
last_progress_at: 2026-08-16T13:26:57+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Rebuild the coordinator-accepted PR #283 read-only runtime bridge on current `main`, then add a deterministic fail-closed P1 health/reacquisition/recovery layer that is testable on GitHub-hosted runners and consumes only explicit runtime identity supplied by an admitted runtime producer.

The P1 layer must never bootstrap, launch, login, restart, kill, attach to, reconfigure, or guess the canonical physical runtime. Real attach/reacquisition/restart/relogin proof remains RUNTIME-owned.

# Current factual basis

- Dispatch base and current `main` are both `0d7b2607912552599ae501891491aab439cfde7b` at handoff preparation.
- PR #283 is closed unmerged, but its bounded read-only bridge implementation was explicitly accepted by the coordinator. The accepted source/test baseline was reconstructed on this branch from its exact blob SHAs before any P1 extension.
- Untouched restored blobs for CMake, `bridge.cpp`, launcher, resolver, profile, `__init__.py` and original focused tests remain byte-identical to the accepted #283 blobs; the temporary hosted workflow asserted these SHAs before tests.
- `ipc_client.py` extends the accepted API compatibly with typed transport/protocol failure subclasses while retaining `BridgeClientError` as their base.
- `health.py` consumes only an explicit exact-fence `BridgeBinding`; it owns no canonical-state discovery and no process-control/launch/login/restart/attach capability.
- PR #303 owns separate physical runtime surfaces; this task neither observed nor mutated that runtime.
- Canonical live identity is deliberately not claimed here: `:98 = UNKNOWN`, `6082 = UNKNOWN`, PID/session = `NOT_REGISTERED`.
- The task-owned temporary workflow `.github/workflows/track-a-p1-bridge-validation.yml` was used only for hosted validation and was removed before this handoff head.
- Final Track A admission fields are persisted at top-level front matter exactly as the deterministic governance parser requires for `runtime_access: none`.

# Acceptance inventory

- [x] Rebuild the exact accepted PR #283 bridge/tool/test baseline on this current-main branch from accepted blob SHAs before extension.
- [x] Preserve exact profile/hash fencing, owner-only local IPC, bounded request framing, read-only discovery and derived `session-status` semantics.
- [x] Add an explicit runtime identity model suitable for RUNTIME-produced registrations/evidence without reading or mutating the canonical runtime from P1.
- [x] Add fail-closed bridge health classification for healthy/degraded, unreachable, malformed, absent/invalid identity and stale/changed identity without promoting `session-status` to authoritative `IN_GAME`.
- [x] Add deterministic reacquisition that binds only to a fresh explicit identity/endpoint, rejects absent identity, exact-fence mismatch, registration/lease generation regression, same-generation process/endpoint change and identity changes during probe, and drops stale cached channels.
- [x] Add bounded recovery that retries/reacquires only newly supplied explicit bindings and never starts/restarts/logs in a client or invents PID/display/socket data.
- [x] Cover healthy/unavailable/malformed/identity-change/stale-generation/stale-lease/replacement-endpoint/retry-exhaustion/recovery-success and real Unix-socket transport/protocol classification paths with deterministic tests.
- [x] Keep all prior #283 focused tests passing on the latest implementation code (`31944224720`, job `95157714206`: baseline fence, dependencies, `py_compile`, focused suite all SUCCESS before C++ build step).
- [x] Run proportional GitHub-hosted focused/component validation. Full validation run `31944059279`, job `95157324527`, completed SUCCESS including accepted-blob fence, dependencies, `py_compile`, focused suite and standalone Qt bridge build. Later Python-only audit fixes did not change accepted CMake/`bridge.cpp`; run `31944224720` re-proved their exact blob fence and the complete Python suite on head `7c86acf779a4677715161001ab9315d41afed65d`.
- [x] Diagnose the sole focused-validation failure from evidence: run `31944025412`, job `95157249963` failed only because hosted validation lacked `pyelftools`; dependency installation was added and the next full run succeeded. No identical blind retry was used.
- [x] Perform a fresh post-implementation exact-source audit. Two robustness findings were found and fixed (string-based stale classification; non-object `PING` handling), followed by additional regression/real-IPC tests. Final re-read at `e78fea2e19ad93e1c828cd8f00cd47a23b7a6402` found zero open material code findings. This was a same-invocation validator pass, not an independent external reviewer; coordinator review remains required for promotion.
- [x] Remove the temporary validation workflow before the final Draft handoff head (`e78fea2e19ad93e1c828cd8f00cd47a23b7a6402`).
- [x] Correct the deterministic Track A admission record after exact-head governance exposed nested-vs-top-level parser incompatibility (`31944317814`, job `95157928824`).
- [x] Leave the result `DRAFT_NOT_PROMOTED`; PR #357 remains Draft and the researcher does not merge/promote it.
- [ ] Final exact-head repository CI/checks are intentionally read from PR #357 after this handoff commit; any failure reopens the task before coordinator promotion.

# Evidence boundary

`session-status` remains a structural candidate with evidence level `DERIVED_UNTIL_LIVE_CORRELATION`. This task proves only hosted bridge/API/lifecycle behavior and standalone helper buildability. It does not prove physical attach, canonical runtime existence, persistent-session reacquisition, restart/relogin stability, current `IN_GAME`, authoritative player position or gameplay actions.

# Validation evidence

- Accepted baseline reconstruction commit: `a96ba77e4cdbb51dd5257ff45e32c057a04c5772`.
- Full hosted component run: `31944059279`, job `95157324527` = `SUCCESS`.
- Latest implementation hosted run: `31944224720`, job `95157714206`; accepted baseline fence, dependencies, `py_compile` and complete focused suite = `SUCCESS` before branch cleanup advanced the Draft head.
- Temporary validation workflow removed: `e78fea2e19ad93e1c828cd8f00cd47a23b7a6402`.
- Main freshness recheck at handoff preparation: `main@0d7b2607912552599ae501891491aab439cfde7b`.
- Exact-head governance diagnostic: `31944317814`, job `95157928824` identified only missing top-level admission fields; fresh behavior audit in the same run passed, and the record was flattened without touching bridge code.

# Audit result

```yaml
auditor_mode: fresh_exact_source_same_invocation
material_findings_fixed: 2
material_findings_open: 0
independent_external_audit: coordinator_required_for_promotion
runtime_nonclaims_preserved: true
gameplay_mutation_added: false
owner_funded_ai_used: false
```

# Checkpoint

```yaml
status: ready
result: DRAFT_NOT_PROMOTED
last_completed_step: fixed deterministic admission-record shape after exact-head governance while preserving the frozen P1 bridge implementation
blockers: []
next_action: verify PR #357 final exact-head repository checks, then coordinator reviews/promotes or rejects the Draft P1 package; physical runtime proof remains RUNTIME-owned
```
