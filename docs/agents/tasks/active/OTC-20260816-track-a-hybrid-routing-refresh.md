---
task_id: OTC-20260816-track-a-hybrid-routing-refresh
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-re
task_kind: documentation
phase: exact-head-validation
branch: docs/OTC-20260816-track-a-hybrid-routing-refresh
base_branch: main
base_head: 9008bb7933db9e96119a61280941e695744e8408
created: 2026-08-16T11:49:00+02:00
updated: 2026-08-16T11:56:00+02:00
risk: medium
execution_mode: github-only
owned_paths:
  - docs/agents/AGENTS.md
  - docs/agents/README.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING_EVAL.md
  - docs/agents/tasks/active/OTC-20260816-track-a-hybrid-routing-refresh.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-hybrid-routing-refresh.md
related_pr: "342"
reuses:
  - PR #331
  - docs/agents/tasks/active/OTC-20260816-linux-ci-hybrid.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - PR #315 historical persistent-display/current-no-client evidence
  - PR #311/#318/#321 canonical-live governance
track_id: official-client-re
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
---

# Goal

Refresh the Track A multi-agent dispatch/routing contract after merged PR #331 so deterministic/disposable work defaults to GitHub-hosted runners while Synology is reserved for the serialized physical persistent runtime lane.

Also make the already-promoted canonical-live design explicit to parallel researchers: the intended topology is one registered idle persistent exact-client runtime on Synology, reused serially under runtime admission, not one independent logged-in session per researcher.

# Source facts

## PR #331 / Linux CI hybrid

Merged PR #331 records the target boundary:

- GitHub-hosted: static/workflow/Lua validation, unit/integration tests, Linux builds, dependency validation, real OTClient artifact startup under Xvfb and startup evidence;
- Synology/self-hosted: persistent OTClient session, real display/input ownership, login/walking/clicking, LAN/runtime integration, long-lived observation and direct physical gameplay evidence;
- hosted startup smoke is not physical gameplay E2E.

## Persistent-session governance

Current trusted-base bootstrap/admission contracts define the target successful initial-creation state as one registered idle persistent exact-client runtime. Later work must use Gate A, any required generation rebind, and Gate B for canonical reuse/mutation.

Current existence must not be fabricated. The authoritative non-claims remain:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

PR #315 is historical evidence that persistent `:98` existed while no exact live client was found during that bounded probe; PR #318 promotes the design target, not proof that a persistent client currently exists.

# Implementation

- Add `OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md` as the normative post-#331 executor router.
- Route P2/P0/P1/COVERAGE deterministic work to GitHub-hosted by default.
- Route physical RUNTIME work to Synology.
- Require one canonical persistent session topology and forbid implicit one-session-per-researcher behavior.
- Preserve bootstrap/rebind/admission fail-closed gates and all current runtime non-claims.
- Add explicit dispatch fields: `EXECUTION_CLASS`, `RUNTIME_ACCESS`, `PERSISTENT_SESSION_ROLE`, `PHYSICAL_E2E_REQUIRED`.
- Add a documented routing regression matrix.
- Update universal Track A agent entrypoints to require this routing document at claim/resume.

# Acceptance inventory

- [x] New routing contract records the PR #331 hosted/Synology boundary.
- [x] Hosted Xvfb smoke is explicitly separated from physical runtime E2E.
- [x] One persistent canonical Synology session is the intended runtime topology.
- [x] Current `:98`/`6082`/PID/session state remains UNKNOWN/NOT_REGISTERED until fresh proof.
- [x] Missing registration routes to canonical bootstrap rather than ordinary launch/reuse.
- [x] Generation mismatch routes to rebind rather than manual registration editing.
- [x] P2/P0/P1/COVERAGE default to GitHub-hosted; RUNTIME owns physical Synology evidence.
- [x] `docs/agents/AGENTS.md` mandates the routing contract.
- [x] `docs/agents/README.md` includes the routing contract in Track A read order.
- [x] Manual routing regression matrix passes.
- [ ] Exact-head repository CI passes.
- [ ] Review has zero unresolved material findings.
- [ ] PR merges through protected main rules.
- [ ] Task is archived and ownership released after merge.

# Validation

- Documentation/prompt-routing change only; live runtime E2E is `NOT_APPLICABLE` because this task neither launches nor observes nor mutates a client.
- Manual scenario matrix: `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING_EVAL.md`.
- PR #342 is the integration PR; exact-head repository CI and review remain mandatory before merge.

# Handover

```yaml
STATUS: validating
BASE_MAIN: 9008bb7933db9e96119a61280941e695744e8408
BRANCH: docs/OTC-20260816-track-a-hybrid-routing-refresh
PR: 342
RUNTIME_ACCESS: none
FACTS:
  - PR #331 merged the hosted Linux build/Xvfb smoke versus Synology physical-runtime boundary.
  - canonical-live governance targets one registered idle persistent runtime.
  - current canonical runtime identity remains UNKNOWN/NOT_REGISTERED without fresh evidence.
  - universal Track A entrypoints now require the hybrid routing contract on this branch.
UNKNOWN:
  - exact live session/display/port identity at current time
  - future bootstrap implementation/live authorization state unless separately proven
NEXT_ACTION: complete exact-head CI/review for PR #342, merge if protected gates pass, then archive this task and release ownership
```