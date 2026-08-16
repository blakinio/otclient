---
task_id: OTC-20260816-track-a-canonical-bootstrap-implementation
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-bootstrap-v2-20260816-1503
session_role: implementation_worker
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: remediate-bootstrap-rebind
branch: ci/OTC-20260816-track-a-canonical-bootstrap-implementation-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
risk: high
updated: 2026-08-16T15:03:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/workflows/tibia-official-client-re-canonical-live-transition-v2.yml
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
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: repair four independent audit findings, validate, independently audit, then promote before physical runtime reuse
validation_level: heavy
session_rotation_count: 1
heavy_validation_runs: 0
stale_takeover_count: 1
human_interruptions: 1
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
  - id: TACOORD-360-001
    severity: HIGH
    source_pr: 360
    remediation: restore and revalidate the exact previous authoritative registration on every post-write rebind failure
  - id: TACOORD-360-002
    severity: HIGH
    source_pr: 360
    remediation: align transition and real shell-worker argv contract and regression-test the actual parser
  - id: TACOORD-360-003
    severity: HIGH
    source_pr: 360
    remediation: remove credential/login typing from this infrastructure worker entirely; physical login remains separately RUNTIME-owned
  - id: TACOORD-360-004
    severity: MEDIUM
    source_pr: 360
    remediation: remove historical shared wireproxy PID/25354 dependency and create a canonical-owned pinned userspace-WARP helper inside the bootstrap process group
acceptance:
  - canonical flock is held continuously across under-lock registration/candidate preflight, bootstrap launch, registration publication, post-probe and detach decision
  - bootstrap refuses an existing authoritative registration and any detectable official-client candidate before launch
  - created client is revalidated by boot identity, PID, process start ticks, exact executable size/SHA, display and window before registration success
  - registration is atomic, mode 0600, generation-bound and revalidated after publication
  - persistent descendants receive neither lease capability material nor canonical flock file descriptors
  - bootstrap failure terminates only the bootstrap-owned process group, invokes bounded owned-state rollback and leaves no success registration
  - rebind final-probe or lease/identity failure after publication restores and revalidates the exact previous registration before returning failure
  - transition bootstrap/probe argv is executable against the real shell worker parser; extra arguments fail closed
  - this infrastructure worker contains no account-login credential typing path and strips TIBIA_TEST and lease/capability variables from descendants
  - canonical bootstrap owns its userspace WARP helper and private state; it does not read or reuse historical PR 303 wireproxy PID/port authority
  - WARP helper downloads are version-pinned and archive/binary inputs are hash-verified before use
  - physical runtime, login, X11/VNC mutation and real client E2E remain forbidden on this branch until implementation is independently reviewed and promoted to trusted main
validation:
  local_preflight:
    python_compile: PASS
    shell_syntax: PASS
    deterministic_tests: PASS_7_OF_7
  github_hosted: PENDING
  independent_audit: PENDING
  final_exact_head_ci: PENDING
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: this is a no-runtime infrastructure producer; physical bootstrap/login E2E belongs to RUNTIME only after trusted-main promotion
last_completed_step: created fresh-current-main replacement branch and locally reproduced all four coordinator findings with deterministic remediations
next_action: persist replacement implementation plus hosted validator, open a superseding Draft PR, close stale PR 360, then validate and independently audit the exact head
---

# Canonical live bootstrap/rebind implementation v2

This fresh-current-main continuation replaces stale PR #360 without inheriting its base or its unsafe runtime assumptions. It implements only the reviewed authority/identity transition and persistent-session bootstrap plumbing. It does **not** run the official client or access Synology while unmerged.

## Safety boundary

The physical runtime remains unregistered and unclaimed. No historical display, VNC port, PID, session, wireproxy PID or SOCKS port is promoted as current truth. The replacement specifically removes the historical shared-wireproxy dependency: any future authorized bootstrap must create and own its own pinned userspace-WARP helper under the canonical namespace/process group.

Account login is deliberately absent from this infrastructure worker. A later RUNTIME task may perform a separately reviewed protected login only after this implementation is promoted to trusted `main` and fresh Gate A/bootstrap/Gate B admission permits mutation.
