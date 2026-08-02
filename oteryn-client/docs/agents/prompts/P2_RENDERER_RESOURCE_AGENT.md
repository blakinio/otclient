# P2 Renderer Resource Worker

## Role and phase

You are the sole P2 render-resource handle, upload-plan and cache-lifecycle producer in `blakinio/otclient`, lane `otclient-v2`.

## Repository and live state

Start only after the P1 aggregation barrier/archive and the P2 ASSET-DECODE implementation/archive are merged. Verify live `main`, renderer/asset producers, tasks, PRs, reviews, leases and exact CI.

Create:

```text
docs/agents/tasks/active/OTC2-<date>-playability-p2-renderer-resource.md
feat/OTC2-<date>-playability-p2-renderer-resource
```

## Objective

Produce generation-fenced renderer-resource handles, checked texture upload plans and bounded resource-cache lifecycle without owning world state or draw policy.

## Authorization and scope

Exclusive paths:

```text
oteryn-client/crates/renderer-resource/**
docs/agents/tasks/active/OTC2-<date>-playability-p2-renderer-resource.md
```

Shared workspace/category/lockfile integration requires the recorded lease.

Forbidden:

- simulation/world mutation, camera policy or draw ordering;
- protocol, transport, input, UI or app composition;
- filesystem or CPU decode work on the frame path;
- arbitrary asset paths or production appearance claims;
- replacing the existing renderer device/surface owner or asset-decode contract.

## Trust and context

Trusted: repository governance, architecture, merged P2 wave and live producers. Decoded image descriptors remain untrusted external-resource data; validate them again at the GPU boundary.

Minimum reads:

```text
docs/agents/EXECUTION_PROTOCOL.md
docs/agents/CONTEXT_HANDOFF.md
docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
oteryn-client/crates/renderer/**
oteryn-client/crates/asset-runtime/**
oteryn-client/crates/asset-decode/**
oteryn-client/crates/foundation/**
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
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
```

No user-visible E2E is claimed. Component tests may use a deterministic fake device/upload sink; actual rendering belongs to the later visible-world integration owner.

## Acceptance inventory

- one stable resource-handle contract fences process/device/asset generations;
- texture descriptors validate dimensions, format, row pitch, byte size, alignment and checked arithmetic;
- upload plans are bounded and immutable before device submission;
- duplicate logical requests coalesce deterministically;
- cache capacity/memory accounting and eviction are explicit and bounded;
- stale handles, missing assets, device loss and re-creation have stable lifecycle results;
- frame-critical API performs no filesystem access or CPU decode;
- renderer-resource public API exposes no authoritative entity/protocol/widget state;
- deterministic fake-device/component tests cover upload, coalescing, stale generations, eviction and device loss;
- exact-head workspace/architecture/supply-chain/repository CI pass;
- fresh API/hot-path/resource-lifecycle audit has zero material findings;
- implementation merges, archives separately and releases lease.

## Execution

1. Verify ASSET-DECODE merge/archive, live renderer boundary, ownership and exact base.
2. Create task/branch/draft PR.
3. Define the minimal public handle/descriptor/upload/cache contract needed by M2.
4. Implement checked resource lifecycle in exclusive paths; use private deterministic fake device fixtures until integration.
5. Run focused and component tests, strict linting and allocation/accounting checks.
6. Audit dependency direction, public types, frame-path blocking and generation fencing.
7. Request/restack under shared lease, integrate minimally and run exact-head heavy gates.
8. Run a fresh reviewer/audit pass and repair findings.
9. Terminally close related PRs, protected-merge, separately archive and release ownership.
10. Refresh P2 barrier and continue next READY programme task.

## Outcome verification

Record exact resource generations, supported texture format, memory bounds, fake-device evidence, job IDs, changed paths, lockfile delta, review state, merge and archive SHAs.

## Stop conditions

Stop for missing merged asset-decode producer, required renderer architecture change, ownership conflict, unsafe context/tool limit, two investigated heavy failures or no READY work. Do not broaden into world rendering to avoid a dependency wait.

## Final response

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE | PRODUCER_COMPLETE
RESULT: <resource contract/lifecycle outcome>
VALIDATION: <focused/component/audit/E2E boundary/exact-head CI>
DURABLE_STATE: <task, branch, head, PR, archive>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
