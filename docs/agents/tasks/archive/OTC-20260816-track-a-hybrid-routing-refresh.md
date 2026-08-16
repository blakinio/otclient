---
task_id: OTC-20260816-track-a-hybrid-routing-refresh
status: completed
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-re
task_kind: documentation
phase: archived
base_branch: main
implementation_pr: "343"
implementation_merge_sha: 54e7aa8ce2994238067d39b37d3d807bc10111d3
superseded_pr: "342"
created: 2026-08-16T11:49:00+02:00
completed: 2026-08-16T12:02:14+02:00
risk: medium
execution_mode: github-only
ownership_released: true
owned_paths: []
track_id: official-client-re
runtime_access: none
mutation_authorized: false
---

# Outcome

Track A now has a mandatory post-PR #331 hybrid execution router on `main`:

`docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

Universal Track A entrypoints (`docs/agents/AGENTS.md`, `docs/agents/README.md`) require it at claim/resume/checkpoint.

## Canonical routing

- **GitHub-hosted default:** static/deterministic analysis, workflow/Lua validation, unit/integration tests, Linux builds, `ldd`, real OTClient artifact startup under `Xvfb`, startup logs/evidence, deterministic P2/P0/P1 tooling and coverage/audit work.
- **Synology/self-hosted physical runtime:** the one canonical persistent runtime/session topology, canonical registration/bootstrap/rebind, real display/input, login/relogin, walking/clicking, LAN/runtime integration, long-lived observation, restart/relogin and direct physical gameplay E2E.
- Hosted Xvfb startup/liveness is explicitly not physical gameplay E2E.
- Parallel research does not authorize one logged-in persistent session per researcher or parallel mutation of the one canonical physical runtime.

## Persistent-session boundary

The intended topology is one registered `IDLE_REGISTERED` persistent exact-client runtime reused serially under Gate A / any required rebind / Gate B.

No current live session was fabricated by this task. The preserved non-claims remain until fresh authoritative proof:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Missing registration routes to `canonical_bootstrap`; lease-generation mismatch routes to `canonical_rebind`; manual registration editing remains forbidden.

## Agent dispatch refresh

Coordinator dispatches now additionally require:

```yaml
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted | synology_physical_runtime
RUNTIME_ACCESS: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind
PERSISTENT_SESSION_ROLE: none | consumer_of_runtime_evidence | canonical_runtime_owner
PHYSICAL_E2E_REQUIRED: true | false
```

Any dispatch created before this contract, or lacking these fields, must be refreshed before mutation.

## Validation

Implementation PR #343 exact head:

- head: `7fe47508a77b3fe3c4b65d3681d3a4d6f828dacc`
- `CI / Required`: PASS, run `31940575249`, job `95149047095`;
- Track A `Fresh admission behavior audit`: PASS, run `31940575143`, job `95149012216`;
- Track A `Deterministic admission-policy audit`: PASS, run `31940575143`, job `95149012267`;
- review threads before merge: `0` unresolved;
- protected auto-merge: PASS;
- implementation merged: PR #343 -> `main@54e7aa8ce2994238067d39b37d3d807bc10111d3`.

PR #342 is closed as superseded after its own successful validation because `main` advanced through PR #341 and strict-up-to-date policy required restacking.

Runtime E2E for this documentation task: `NOT_APPLICABLE`; the task neither launched, observed nor mutated a client.

## Final handover

```yaml
STATUS: DONE
IMPLEMENTATION_PR: 343
MAIN_HEAD_AT_IMPLEMENTATION_MERGE: 54e7aa8ce2994238067d39b37d3d807bc10111d3
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
OWNERSHIP_RELEASED: true
RUNTIME_ACCESS: none
DURABLE_STATE:
  - routing contract on main
  - routing evaluation on main
  - mandatory AGENTS/README entrypoints on main
  - this archived task
NEXT_ACTION: coordinator must refetch current main and refresh all pre-upgrade Track A researcher dispatches before researcher mutation
```