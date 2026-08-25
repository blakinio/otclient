# OTCLIENT-TIBIA-RE hybrid execution routing

```yaml
routing_contract_version: 1.0.0
programme: OTCLIENT-TIBIA-RE
track: official-client-re
status: normative_execution_routing
adopted_after_pr: 331
runner_boundary:
  github_hosted: deterministic_disposable_validation
  synology: physical_persistent_runtime
canonical_synology_runner: synology-otclient-01
canonical_state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
```

## Purpose

This document is the mandatory execution-router for Track A after PR #331. It does not replace the runtime-admission, canonical-live, bootstrap, ownership, evidence or anti-stall contracts. It decides **where a task should execute** once those contracts have admitted the task.

Any Track A dispatch/task created before this routing contract reached `main` must be refreshed at the next claim/resume/checkpoint before mutation. A stale dispatch may be reused only after its `BASE_MAIN`, runtime admission, runner class, dependencies and owned paths are revalidated against current `main`.

## Authoritative hybrid boundary

### GitHub-hosted runners — default for deterministic/disposable work

Use GitHub-hosted runners for work that does not require the physical persistent game session or Synology-local physical environment, including:

- repository/source static analysis;
- workflow/actionlint/yamllint validation;
- Lua validation;
- unit tests and bounded integration tests;
- Linux release/test builds;
- `ldd` / shared-library resolution checks for built OTClient artifacts;
- bounded real OTClient artifact startup under `Xvfb`;
- software-rendered/headless startup validation;
- startup/dependency logs and evidence artifacts;
- deterministic parsers, registries, coverage computation, evidence normalization and other disposable tooling;
- P2/P0/P1 static or synthetic/local-harness work that does not need the real persistent Tibia session.

PR #331's `Client Startup Smoke - Linux` is a hosted startup/liveness check only. It must never be promoted as proof of real login, real display/input ownership, LAN behavior, gameplay control, persistent-session stability or physical runtime E2E.

If a deterministic static experiment currently depends on host-local retained material that is not legally/technically available on a GitHub-hosted runner, the worker must record the exact input blocker and ask the coordinator to choose a compliant evidence-staging strategy. It must not silently consume the canonical physical session merely because Synology has the files.

### Synology/self-hosted — only for physical/persistent runtime evidence

Use `synology-otclient-01` for work that genuinely depends on the controlled physical runtime environment, including:

- the one canonical persistent official-client session;
- canonical runtime registration/rebind/bootstrap work;
- real X11 display/window ownership;
- real keyboard/mouse/input injection under an authorized runtime task;
- login, character/world entry and relogin;
- walking, reversible movement, clicking and other authorized physical gameplay stimuli;
- LAN/Synology-specific runtime integration;
- long-lived observations that must survive an individual workflow/job;
- direct physical gameplay evidence;
- restart/relogin causal stability;
- final physical runtime E2E when a gate requires it.

Synology is a scarce serialized runtime resource, not the default static-analysis executor.

## Persistent-session model

The programme target is **one canonical registered idle persistent exact-client runtime**, not one live Tibia session per researcher.

The governing bootstrap contract defines the successful creation transition as:

```text
no registered canonical runtime
 -> authoritative lease + bootstrap supervisor
 -> exact process/display/window/state proof
 -> atomic generation-bound registration
 -> safe detach
 -> IDLE_REGISTERED persistent client
```

After that state exists, future physical experiments should reuse the same canonical session serially through current Gate A / required rebind / Gate B instead of spawning duplicate logged-in sessions.

The persistent client itself must not inherit controller coordination authority, lease capability or credentials. Credentials may exist only in a separately authorized bounded login step and must not persist in the client/helper environment or registration record.

### Current non-claims

The persistent-session **design is authoritative; current existence is not**. Until fresh current evidence proves otherwise, every worker must preserve:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Historical evidence establishes that a persistent X11 display `:98` existed and that RFB metadata supported an association with display 98, but the later bounded registration probe found no exact fenced live client at that time. Historical `:98`, `6082`, PID/session or prior login success is therefore discovery input only.

If the authoritative registration is absent, ordinary runtime reuse MUST NOT launch a replacement client. The worker must classify the runtime request under `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`; initial creation belongs only to `canonical_bootstrap`. If the reviewed bootstrap implementation is unavailable or the required live authorization/gates are not proven, mutation remains refused and the lane continues unrelated safe work or returns the exact blocker.

If an existing registration is bound to an older lease generation and fresh proof shows the same unchanged runtime identity, use reviewed `canonical_rebind`. If both registered PID/start are stale on the same boot while the reviewed probe proves exactly one current same-fence canonical target with the required continuity anchors, route only to reviewed `canonical_recovery`. If the authoritative adoption registration is from a different boot identity than repeated fresh singleton proof, route only to `canonical_boot_epoch_recovery`. Never use rebind to bless identity drift and never edit registration metadata manually.

## Parallel-lane routing

### P2-NETWORK

Default execution: **GitHub-hosted**.

Use hosted/static/synthetic/local-harness experiments for writer ownership, RTTI/vtables, serialization, framing, sequence, compression/encryption ordering, protocol registries and non-physical socket/byte-container proofs whenever possible.

If a P2 claim ultimately requires direct evidence from the real persistent client, request a bounded stimulus/observation from the RUNTIME lane. P2 must not independently take over display/input/login/session ownership.

### P0-STATE

Default execution: **GitHub-hosted** for candidate discovery, resolvers, parsers, state registries and deterministic validation.

Direct semantic/causal validation against the real client is supplied by the RUNTIME lane or by a separately admitted, non-conflicting `read_only` task with `target_uniqueness: PROVEN`. P0 must not create a second logged-in session to validate reads.

### P1-BRIDGE

Default execution: **GitHub-hosted** for bridge implementation, unit/integration tests, lifecycle simulation, stale-state tests, restart logic simulation and headless startup integration.

Real persistent-session attach/reacquisition/liveness validation is coordinated through RUNTIME and the canonical admission model. P1 must fail closed when canonical identity is unavailable; it must not bootstrap or mutate the physical session as an implementation shortcut.

### RUNTIME

Execution: **Synology/self-hosted** for physical runtime work.

RUNTIME is the primary owner/provider of real login/display/input/gameplay/restart-relogin evidence. Its first action at every claim/resume is runtime admission and live ownership reconciliation.

RUNTIME should prefer reuse of the one registered persistent session when Gate A + any required rebind + Gate B pass. It may perform bootstrap only through a reviewed current implementation and separate live authorization. It must never create a second logged-in Global session merely to unblock another lane.

RUNTIME may run supporting deterministic hosted jobs for analysis of its artifacts, but physical state mutation remains on Synology.

### COVERAGE-AUDIT

Execution: **GitHub-hosted**.

Coverage computation, registries, denominator checks, contradiction/supersession audits and evidence indexing should not consume the Synology runtime. Runtime results are inputs from durable artifacts/reports, not a reason to take the live session.

## Coordinator dispatch rules

Before dispatching or refreshing any Track A researcher, the coordinator must add/verify these fields in addition to the existing task/branch/worktree/owned-path contract:

```yaml
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted | synology_physical_runtime
RUNTIME_ACCESS: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind | canonical_recovery | canonical_boot_epoch_recovery
PERSISTENT_SESSION_ROLE: none | consumer_of_runtime_evidence | canonical_runtime_owner
PHYSICAL_E2E_REQUIRED: true | false
```

Rules:

1. `P2-NETWORK`, `P0-STATE`, `P1-BRIDGE` and `COVERAGE-AUDIT` default to `EXECUTION_CLASS: github_hosted` and `RUNTIME_ACCESS: none`.
2. `RUNTIME` uses `EXECUTION_CLASS: synology_physical_runtime` for physical work and must persist the full runtime-admission record.
3. A non-RUNTIME lane may receive `read_only` access only when the admission contract's uniqueness/ownership/non-invasiveness gates are freshly proven and the coordinator can show why RUNTIME-provided durable evidence is insufficient.
4. No lane gets an independent logged-in persistent session by default.
5. Hosted `Xvfb` startup smoke is not physical E2E and cannot satisfy a task whose `PHYSICAL_E2E_REQUIRED` is true.
6. Synology physical operations are serialized through current runtime ownership/lease/registration governance; parallel research does not mean parallel mutation of the one physical session.
7. If a dispatch was prepared from a base before the merged hybrid boundary or lacks the fields above, refresh it before mutation.

## Task refresh matrix

| Lane | Default executor | Persistent session | Physical E2E | Key refresh |
|---|---|---|---|---|
| P2-NETWORK | GitHub-hosted | no ownership | only via RUNTIME if needed | keep static/synthetic work hosted; request bounded real stimulus instead of taking session |
| P0-STATE | GitHub-hosted | evidence consumer | via RUNTIME for causal reads | discover hosted; validate semantics against RUNTIME evidence |
| P1-BRIDGE | GitHub-hosted | evidence consumer | via RUNTIME for reacquisition/restart | build/test hosted; fail closed without canonical identity |
| RUNTIME | Synology | canonical runtime owner/provider | yes | establish/reuse one registered persistent session under admission gates |
| COVERAGE-AUDIT | GitHub-hosted | none | no | consume durable runtime evidence only |

## Evidence boundary

Classify the environment outcome explicitly:

```text
HOSTED_STATIC_OR_TEST
HOSTED_LINUX_BUILD
HOSTED_XVFB_STARTUP_SMOKE
SYNOLOGY_RUNTIME_READ_ONLY
SYNOLOGY_PHYSICAL_RUNTIME_E2E
CANONICAL_PERSISTENT_SESSION_PROOF
```

Do not collapse these categories. A lower class cannot satisfy a higher physical-runtime gate.

## Mandatory related contracts

Every Track A worker must continue to obey current versions of:

- `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`;
- `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`;
- `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`;
- `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md` when parallel research is active;
- current task/PR/ownership state.

Current `main` and these trusted-base contracts override stale PR/task/chat wording.