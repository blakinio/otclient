---
task_id: OTC-20260816-track-a-canonical-bootstrap-implementation
status: validating
agent: ChatGPT
session_id: chatgpt-runtime-bootstrap-v2-20260816-1503
session_role: implementation_worker
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: final-no-temp-workflow-validation
branch: ci/OTC-20260816-track-a-canonical-bootstrap-implementation-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
risk: high
updated: 2026-08-16T15:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - historical PR 48 userspace-WARP recipe as implementation provenance only
supersedes_pr: 360
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic transition/session implementation and tests on GitHub-hosted infrastructure; no physical runtime execution is authorized from this branch
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: repair four coordinator findings plus two fail-closed audit hardenings, validate, independently review, then promote before physical runtime reuse
validation_level: heavy
track_a_runtime_agent_admission_version: 1
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
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_findings:
  - {id: TACOORD-360-001, severity: HIGH, implementation_status: REMEDIATED, remediation: exact previous registration is restored and revalidated after every post-publication rebind failure}
  - {id: TACOORD-360-002, severity: HIGH, implementation_status: REMEDIATED, remediation: transition and real shell-worker argv are aligned and regression-tested}
  - {id: TACOORD-360-003, severity: HIGH, implementation_status: REMEDIATED, remediation: account login and credential typing are absent from this infrastructure worker}
  - {id: TACOORD-360-004, severity: MEDIUM, implementation_status: REMEDIATED, remediation: historical shared wireproxy PID/port dependency is removed in favor of canonical-owned pinned userspace WARP}
audit_hardenings:
  - {id: TACBOOT-V2-AUD-001, severity: HIGH, implementation_status: REMEDIATED, finding: incomplete same-runner-UID process inventory must block bootstrap, remediation: unreadable live same-UID inventory now fails closed}
  - {id: TACBOOT-V2-AUD-002, severity: HIGH, implementation_status: REMEDIATED, finding: safe detach must exclude untracked bootstrap descendants, remediation: exact client/xvfb/vnc/wireproxy PID set must equal live bootstrap PGID membership}
acceptance:
  - canonical flock remains held across absence proof, launch, registration publication, post-probe and detach decision
  - bootstrap refuses an existing registration, detected official-client candidate, or incomplete same-runner-UID process inventory
  - client identity is fenced by boot/PID/start/executable size/SHA plus display/window and uniqueness
  - registration is atomic mode-0600 and lease-generation-bound
  - persistent descendants receive no lease capability/fd or account credential environment
  - failed bootstrap terminates only its own process group and leaves no success registration
  - failed post-publication rebind restores and revalidates the previous authoritative registration
  - shell worker argv is regression-tested against the real parser
  - canonical-owned WARP helper uses version/hash-pinned inputs and no PR #303 PID/port authority
  - safe detach and Gate B reject any extra live member of the bootstrap process group
  - physical runtime execution remains forbidden until this implementation is promoted to trusted main
validation:
  semantic_and_deterministic_validation_head: 8f3874286a925a70ecd381d85204caae21b1e91c
  transition_validator_run: 31950552377
  transition_validator_result: SUCCESS
  track_a_governance_run: 31950552351
  track_a_governance_result: SUCCESS
  repository_ci_run: 31950552420
  repository_ci_result: SUCCESS
  implementation_audit: PASS_MATERIAL_FINDINGS_0_AFTER_TWO_ADDITIONAL_HARDENINGS
  temporary_validator_workflow: REMOVE_BEFORE_FINAL_HEAD
  final_no_temp_workflow_governance: PENDING
  final_no_temp_workflow_repository_ci: PENDING
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: no-runtime infrastructure producer; physical bootstrap/login E2E belongs to RUNTIME after trusted-main promotion
last_completed_step: exact-head transition validator, Track A governance and repository CI all passed on 8f387428 after remediation and workflow-lint repair
next_action: remove temporary validator workflow, obtain fresh final exact-head governance/repository CI, then coordinator-review and promote if main remains fresh
---

# Canonical live bootstrap/rebind implementation v2

Fresh-current-main replacement for stale PR #360. It implements only the reviewed canonical bootstrap/rebind/Gate-B authority and persistent-session plumbing. It does not execute the official client or access Synology while unmerged.

Current physical runtime remains unregistered and unclaimed. No historical display, VNC port, PID, session, wireproxy PID or SOCKS port is promoted as current truth. Login is deliberately absent from this infrastructure worker and remains a later serialized RUNTIME operation after trusted-main promotion and fresh admission.
