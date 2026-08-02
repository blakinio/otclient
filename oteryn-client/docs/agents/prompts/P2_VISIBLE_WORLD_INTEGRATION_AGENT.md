# P2 Visible World Integration Worker

## Role and phase

You are the one serialized P2 synthetic visible-world composition owner in `blakinio/otclient`, lane `otclient-v2`.

## Repository and live state

Start only after all five prerequisite producers are merged and separately archived:

- SIMULATION-SNAPSHOT;
- CANARY-WORLD-PROTOCOL;
- ASSET-DECODE;
- RENDERER-RESOURCE;
- INPUT-PLATFORM.

Verify live `main`, P2 wave/barrier, producer APIs and evidence, tasks, PRs, reviews, shared leases and exact CI.

Create:

```text
docs/agents/tasks/active/OTC2-<date>-playability-p2-visible-world-integration.md
feat/OTC2-<date>-playability-p2-visible-world-integration
```

## Objective

Compose the merged P2 producers into one bounded original synthetic visible-world client loop that renders a world snapshot, maps semantic movement/logout actions to `GameCommand`, applies reconciliation events and shuts down safely.

## Authorization and scope

Exclusive paths:

```text
oteryn-client/crates/world-renderer/**
oteryn-client/apps/client/**
oteryn-client/tests/integration/visible-world/**
oteryn-client/docs/evidence/playability/p2/synthetic-visible-world.md
docs/agents/tasks/active/OTC2-<date>-playability-p2-visible-world-integration.md
```

This worker is the only P2 holder of the final `apps/client/**` composition lease. Exact root workspace/lockfile/architecture/document paths require the recorded shared lease.

Forbidden:

- new gameplay IDs/events/commands or alternate snapshots/resource handles;
- protocol layout changes, simulation mutation outside its producer or asset decode/resource duplication;
- broad UI framework, inventory/chat/combat/settings/audio/minimap work;
- production assets, credentials, private captures or deployment activation;
- claiming controlled Canary compatibility or M2 completion from synthetic fixtures.

## Trust and context

Trusted: repository governance, architecture, merged P2 wave and exact producer contracts. Fixture protocol bytes, assets and runtime logs are untrusted data; use only original sanitized fixtures with explicit provenance.

Minimum reads:

```text
docs/agents/EXECUTION_PROTOCOL.md
docs/agents/CONTEXT_HANDOFF.md
docs/agents/END_TO_END_FEATURE_COMPLETENESS.md
docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
<merged producer public APIs and archive checkpoints only>
```

## Policy

```yaml
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
context_pressure: high
decomposition_decision: phased
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
```

## Feature scope

```yaml
feature_scope:
  type: full_stack
  user_facing: true
  backend_required: true
  frontend_required: true
  integration_required: true
  e2e_required: true
  completion_claim: partial_consumer
```

The required E2E for this task is an original synthetic fixture journey. Controlled real M2 acceptance is a separate task and remains mandatory before any playable/M2 claim.

## Acceptance inventory

- world-renderer consumes immutable `RenderSnapshot` values and renderer-resource handles only;
- deterministic draw extraction/order covers bounded floors, tiles, items, local player and basic entities/effects required by the accepted synthetic fixture;
- no renderer path mutates simulation or interprets Canary fields;
- original synthetic RGBA assets are loaded through asset-runtime -> asset-decode -> renderer-resource, never loose paths;
- product M2 binding map lives outside input-actions and maps normalized semantic movement/camera/logout actions deliberately;
- semantic movement/logout actions create validated session-fenced `GameCommandEnvelope` values;
- fixture protocol events update simulation and publish new snapshots, including movement reconciliation;
- app/event thread remains nonblocking for network, filesystem, decode and worker shutdown;
- resize, suspend, focus/capture loss, device loss, session end and close paths are deterministic;
- one repeatable synthetic E2E proves launch -> visible world -> movement command -> reconciliation -> logout -> terminal cleanup;
- evidence records exact build, fixture provenance, visible-state assertions and teardown results without credentials/private/proprietary data;
- audit classifies output `SYNTHETIC_ONLY` and `partial_consumer`; no M2/playable claim;
- exact-head Windows workspace, architecture, Supply Chain, repository CI and review hygiene pass;
- implementation merges, archives separately and releases final P2 composition lease.

## Execution

1. Verify all producer merges/archives and exact public APIs; reject stale or substitute contracts.
2. Create task/branch/draft PR and record the final composition lease boundaries.
3. Implement the smallest world-renderer and binding map needed by the accepted synthetic journey.
4. Compose producer lifecycles in `apps/client` without blocking the event/frame path.
5. Add deterministic integration fixtures and assertions at each boundary.
6. Run focused world-renderer/binding tests, component producer-chain tests and the full synthetic E2E.
7. Verify user-observable frame/state transitions and persistent evidence, not only worker claims.
8. Perform a fresh architecture, threading, hot-path, trust, teardown and feature-completeness audit; repair findings.
9. Restack on exact current `main`, run full exact-head Windows, architecture, Supply Chain and repository CI.
10. Close all temporary/diagnostic PRs and review threads, protected-merge, separately archive and release ownership.
11. Refresh P2 barrier. Launch controlled M2 acceptance only when its named owner inputs are present; otherwise persist exact blockers and continue any other independent READY programme work.

## Outcome verification

Record exact producer SHAs, fixture hashes/provenance, screenshots or frame assertions where policy permits, input-to-command and event-to-snapshot evidence, teardown results, job IDs, changed paths, audit findings, merge and archive SHAs.

## Stop conditions

Stop for missing producer/archive, incompatible public contracts, required architecture change, ownership conflict, unsafe context/tool limit, two investigated heavy failures or no READY work. Missing staging/production inputs do not justify weakening the synthetic claim or calling M2 complete.

## Final response

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE | PRODUCER_COMPLETE
RESULT: <synthetic visible-world composition outcome>
VALIDATION: <focused/component/synthetic E2E/audit/exact-head CI>
DURABLE_STATE: <task, branch, head, PR, archive and producer SHAs>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <controlled M2 acceptance or one other READY action>
```
