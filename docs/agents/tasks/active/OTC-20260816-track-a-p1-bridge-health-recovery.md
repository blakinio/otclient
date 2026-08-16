---
task_id: OTC-20260816-track-a-p1-bridge-health-recovery
status: implementing
agent: ChatGPT
session_id: chatgpt-p1-20260816-1421
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implement
branch: feat/OTC-20260816-track-a-p1-bridge-health-recovery
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
current_main: b771cf53f01db02a27c9a2a4d9018e7592900111
created: 2026-08-16T13:14:00+02:00
updated: 2026-08-16T14:21:00+02:00
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
  - "RUNTIME for later physical attach/restart/relogin evidence; not mutated by this task"
  - "coordinator serialization before shared MODULE_CATALOG.md / CHANGELOG.md edits"
blocks: []
cross_repository_tasks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: GitHub connector plus GitHub-hosted Actions are sufficient; owner-funded Codex/API use is forbidden
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: phased
decomposition_reason: same task/branch continues through repair, validation, coordinator integration and closeout; no duplicate writer
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
validation_level: component
heavy_validation_runs: 1
session_rotation_count: 1
stale_takeover_count: 1
human_interruptions: 1
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
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
last_progress_at: 2026-08-16T14:21:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: repair-1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Rebuild the coordinator-accepted PR #283 bridge on current Track A and deliver a deterministic fail-closed P1 bridge/API health, reacquisition and recovery layer that is testable on GitHub-hosted runners and consumes only explicit runtime identity supplied by an admitted runtime producer.

P1 must never bootstrap, login, restart, kill, reconfigure, take over, or otherwise mutate the canonical physical runtime. IPC/discovery is read-only; `launcher.py` uses `LD_PRELOAD` process instrumentation and activation remains exclusively RUNTIME-owned under the runtime admission/Gate A/rebind/Gate B/bootstrap contracts.

# Current factual basis

- Canonical P1 PR is #357 on branch `feat/OTC-20260816-track-a-p1-bridge-health-recovery`.
- Previous exact head `edcc3f85bbe084667cb89024b54cd3ab79185809` had Track A governance run `31944372661 = SUCCESS` and repository CI `31944372746 = SUCCESS`.
- Current `main` advanced to `b771cf53f01db02a27c9a2a4d9018e7592900111`; the P1 branch is behind and must be refreshed only after coherent repairs/integration are ready.
- Previous worker checkpoint became stale under the repository 45-minute stale threshold; this replacement session resumes the same task/branch/PR and does not create a duplicate writer.
- Coordinator review on comment `5307270606` returned `ACCEPT_WITH_EDITS`: add same-PR reusable integration records in `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`, and preserve the read-only IPC/discovery vs invasive `LD_PRELOAD` activation authority distinction.
- Those two shared documentation paths are currently also changed by still-open PR #23, so they must not be edited concurrently until coordinator serialization/ownership permits it.
- Fresh P1 semantic audit comment `5307270868` opened two material findings that remain repair requirements for this task:
  1. the Unix socket endpoint is not cryptographically/process-identity bound to the declared `RuntimeIdentity`; same-path replacement can be accepted as healthy;
  2. discovery scan failure (`/proc/self/mem` open/read failure) can collapse into a successful zero-hit result and therefore a false `HEALTHY` state.
- Canonical live state is deliberately not claimed by P1: `:98 = UNKNOWN`, `6082 = UNKNOWN`, PID/session = `NOT_REGISTERED` unless separately proven by the RUNTIME lane.
- No owner-funded Codex/OpenAI API/paid AI quota or owner credentials are authorized.

# Acceptance inventory

- [x] Rebuild the exact coordinator-accepted PR #283 bridge/tool/test baseline before extension.
- [x] Preserve exact profile/hash fencing, owner-only local IPC, bounded request framing, read-only discovery and derived `session-status` semantics.
- [x] Add an explicit runtime identity model suitable for RUNTIME-produced registration evidence without discovering or mutating canonical runtime state from P1.
- [x] Add fail-closed bridge health classification for absent/invalid identity, stale generations, transport/protocol errors and identity changes.
- [x] Add deterministic reacquisition/recovery that consumes only explicit fresh bindings and never launches/logs in/restarts/signals/kills the official client.
- [x] Preserve `session-status` evidence level `DERIVED_UNTIL_LIVE_CORRELATION`.
- [ ] Bind every accepted IPC interaction to the registered exact runtime identity so a same-path endpoint replacement cannot pass health/reacquisition. On Linux, peer PID verification (`SO_PEERCRED`) plus process-start/exact-profile identity proof in the protocol is acceptable; equivalent fail-closed proof is acceptable.
- [ ] Add deterministic regression coverage for same-path endpoint replacement / peer identity mismatch and prove it fails closed.
- [ ] Distinguish successful discovery with zero hits from discovery mechanism failure; `/proc/self/mem` open/read failure must propagate as typed/non-healthy state rather than `ok:true` zero hits.
- [ ] Add deterministic regression coverage for successful zero-hit scan versus scan unavailable/read failure.
- [ ] Re-run focused Python tests and standalone Qt bridge build after semantic repairs.
- [ ] Perform a fresh exact-head semantic audit after repairs with zero open material findings.
- [ ] Reconcile the durable task acceptance/checkpoint with final exact-head CI evidence.
- [ ] Add required reusable-system integration records to `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` only after shared-path ownership is serialized; do not race PR #23.
- [ ] Ensure README/task wording explicitly distinguishes read-only IPC/discovery from RUNTIME-owned `LD_PRELOAD` activation.
- [ ] Refresh/integrate current `main` without overwriting other Track A work and obtain fresh exact-head required governance + repository CI.
- [ ] Leave physical runtime proof to RUNTIME; P1 E2E remains `NOT_APPLICABLE` because this is a GitHub-hosted internal producer with `runtime_access: none`.
- [ ] Coordinator makes the final promotion/merge decision; researcher/implementer does not silently bypass coordinator ownership or shared-index serialization.

# Evidence boundary

`session-status` is a structural candidate only and remains `DERIVED_UNTIL_LIVE_CORRELATION`. This task proves hosted bridge/API/lifecycle behavior and standalone helper buildability. It does not prove physical attach, canonical runtime existence, persistent-session reacquisition, restart/relogin stability, current `IN_GAME`, authoritative player position, VNC/display state, or gameplay actions.

# Prior validation evidence

- Accepted baseline reconstruction commit: `a96ba77e4cdbb51dd5257ff45e32c057a04c5772`.
- Full hosted component run: `31944059279`, job `95157324527` = `SUCCESS`.
- Implementation hosted run: `31944224720`, job `95157714206` = focused suite/dependency/blob-fence success on implementation head.
- Previous exact-head Track A governance: `31944372661 = SUCCESS` on `edcc3f85bbe084667cb89024b54cd3ab79185809`.
- Previous exact-head repository CI: `31944372746 = SUCCESS` on the same head.
- These runs predate the two material findings and do not close them.

# Audit result

```yaml
auditor_mode: independent_semantic_review_from_p1_continuation
material_findings_fixed: 0
material_findings_open: 2
coordinator_edits_open: 2
runtime_nonclaims_preserved: true
gameplay_mutation_added: false
owner_funded_ai_used: false
```

# Checkpoint

```yaml
status: implementing
result: IN_PROGRESS
last_completed_step: resumed stale canonical P1 task on the existing branch and persisted coordinator plus semantic repair requirements
blockers:
  - shared MODULE_CATALOG.md and CHANGELOG.md integration edits require coordinator serialization while PR #23 remains an overlapping writer
next_action: repair the two owned-path semantic findings with deterministic regression tests, then run focused/component validation before shared-index integration
```
