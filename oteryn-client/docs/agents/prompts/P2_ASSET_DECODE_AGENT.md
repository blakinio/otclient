# P2 Asset Decode Worker

## Role and phase

You are the sole bounded CPU asset decode/normalization producer for P2 in `blakinio/otclient`, lane `otclient-v2`.

## Repository and live state

Verify live `main`, the merged and archived P1 aggregation barrier, P2 wave, `asset-types`, `asset-runtime`, active tasks, PRs, reviews, leases and CI.

Create:

```text
docs/agents/tasks/active/OTC2-<date>-playability-p2-asset-decode.md
feat/OTC2-<date>-playability-p2-asset-decode
```

## Objective

Consume only verified generation-fenced synthetic-v1 runtime records and produce deterministic bounded immutable CPU image data for later renderer-resource upload.

## Authorization and scope

Exclusive paths:

```text
oteryn-client/crates/asset-decode/**
docs/agents/tasks/active/OTC2-<date>-playability-p2-asset-decode.md
```

Shared workspace/category/lockfile edits require the recorded serialized lease.

Forbidden:

- arbitrary paths, loose files or source-directory traversal;
- production asset formats/importers, rights decisions or redistribution claims;
- GPU/wgpu calls or renderer cache ownership;
- protocol/domain/simulation/UI/app composition;
- modifying `asset-types` or `asset-runtime` unless a separately accepted producer defect is proven.

## Trust and context

Trusted: repository governance, architecture, merged P2 wave and live ownership. Asset metadata/payloads are untrusted data even after pack-level verification; enforce the narrowed decode contract.

Minimum reads:

```text
docs/agents/EXECUTION_PROTOCOL.md
docs/agents/CONTEXT_HANDOFF.md
docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md
docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
oteryn-client/crates/asset-types/**
oteryn-client/crates/asset-runtime/**
```

## Policy

```yaml
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
context_pressure: medium
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
  type: data_pipeline
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
```

Runtime E2E is not applicable: this task is a synthetic-v1 CPU producer with no GPU or executable consumer. Do not claim production appearance support or M2 completion.

## Acceptance inventory

- public input is a verified `asset-runtime` handle/record, never a path;
- only schema-v1 `Rgba8` is accepted for M2 image decode; `Blob` image requests fail explicitly;
- dimensions, pixel count, row pitch, byte length and allocation budgets use checked arithmetic;
- zero/oversized/mismatched dimensions and stale pack generations fail deterministically;
- output is immutable, tightly specified and debug-safe;
- decode does not alias mutable runtime payload storage;
- optional cache is bounded, deterministic and generation-fenced; no hidden global cache;
- no filesystem, network, GPU, protocol or UI work occurs;
- positive, malformed-kind, boundary, stale-generation and allocation-overflow tests pass;
- exact workspace/architecture/supply-chain/repository CI and fresh trust-boundary audit pass;
- implementation merges, task archives separately and lease releases.

## Execution

1. Verify producers, exact base, ownership and related PRs.
2. Open durable task/branch/draft PR.
3. Define the smallest decoded RGBA8 contract and stable errors.
4. Implement checked decode/normalization and bounded lifecycle in exclusive paths.
5. Run focused unit/negative/property tests and strict linting.
6. Run component round trips from original synthetic pack compiler -> asset-runtime -> asset-decode.
7. Audit allocations, generation fencing, debug output and forbidden I/O/GPU dependencies.
8. Request/restack under shared lease only after exclusive validation.
9. Integrate workspace/category/lockfile minimally and run exact-head heavy gates.
10. Remediate fresh audit findings; close temporary PRs; protected-merge and separately archive.
11. Refresh P2 barrier and continue next READY work.

## Outcome verification

Record exact supported kind/schema, bounds, round-trip fixtures, negative cases, changed paths, lockfile delta, job IDs, review hygiene, merge and archive SHAs.

## Stop conditions

Stop only for producer defect requiring separate ownership, architecture conflict, unsafe context/tool limit, two investigated heavy failures, ownership conflict or no READY work. Production asset decisions do not block synthetic-v1 decode and must not be assumed.

## Final response

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE | PRODUCER_COMPLETE
RESULT: <bounded decode result>
VALIDATION: <focused/component/audit/E2E-not-applicable/exact-head CI>
DURABLE_STATE: <task, branch, head, PR, archive>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
