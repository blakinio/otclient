# P2 Input Platform Worker

## Role and phase

You are the sole Windows/winit physical-event adapter producer for the merged input-actions contract in `blakinio/otclient`, lane `otclient-v2`.

## Repository and live state

Verify live `main`, the merged/archived P1 aggregation barrier, P2 wave, `input-actions`, current platform/app event handling, active tasks, PRs, reviews, leases and CI.

Create:

```text
docs/agents/tasks/active/OTC2-<date>-playability-p2-input-platform.md
feat/OTC2-<date>-playability-p2-input-platform
```

## Objective

Map supported Windows/winit keyboard, mouse, pointer, wheel, text, focus, capture and device lifecycle into framework-neutral `input-actions` physical events without leaking OS/framework types across the adapter boundary.

## Authorization and scope

Exclusive paths:

```text
oteryn-client/crates/input-platform/**
docs/agents/tasks/active/OTC2-<date>-playability-p2-input-platform.md
```

Shared workspace/category/lockfile edits require the recorded integration lease.

Forbidden:

- product default keymap or persisted user settings;
- direct `GameCommand` mapping;
- widget/UI policy, world state or camera behaviour;
- edits to `input-actions` unless a separately accepted producer defect is proven;
- `apps/client/**` composition;
- raw Win32 hooks or unsupported global input capture.

## Trust and context

Trusted instructions are repository governance, architecture, merged P2 wave and live ownership. OS/framework events are untrusted runtime input; normalize and bound them.

Minimum reads:

```text
docs/agents/EXECUTION_PROTOCOL.md
docs/agents/CONTEXT_HANDOFF.md
docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
oteryn-client/crates/input-actions/**
oteryn-client/crates/platform/**
oteryn-client/apps/client/**
```

Application code is read-only evidence for this package.

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
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
```

Interactive Windows E2E belongs to visible-world integration/controlled acceptance. This package proves deterministic adapter behaviour with synthetic framework events.

## Acceptance inventory

- public API accepts adapter-owned values and emits only merged normalized physical events;
- winit/Win32 types do not cross the public output boundary;
- keyboard scan/logical identity, modifiers, mouse buttons, pointer position/delta, wheel, text and focus/capture lifecycle follow explicit mapping rules;
- unsupported/unknown keys or buttons use a bounded explicit policy rather than panic or silent aliasing;
- focus loss, capture loss and device loss trigger the cleanup semantics required by input-actions;
- duplicate/reordered lifecycle events produce deterministic stable outcomes;
- text input is bounded and not confused with key presses;
- no global hooks, background capture, keylogging or raw secret logging;
- no product binding map, gameplay command, UI or app composition enters the crate;
- positive/negative/boundary adapter tests pass;
- exact-head workspace/architecture/supply-chain/repository CI and fresh trust/API audit pass;
- implementation merges and archives separately.

## Execution

1. Verify exact live event-loop/framework version, merged input-actions API and ownership.
2. Open task/branch/draft PR.
3. Define a minimal adapter-private synthetic event model for deterministic tests.
4. Implement explicit mappings in exclusive paths, preserving input-actions lifecycle invariants.
5. Run focused mapping/lifecycle tests and strict linting.
6. Run component integration through `InputRouter` with synthetic focus/capture/device loss.
7. Audit public types, privacy/logging, unsupported-event policy and no hidden global capture.
8. Request/restack under shared lease, integrate minimally and run exact-head heavy gates.
9. Repair audit findings; close related PRs; protected-merge, separately archive and release ownership.
10. Refresh P2 barrier and continue next READY programme work.

## Outcome verification

Record supported event matrix, explicit unsupported policy, lifecycle cleanup evidence, job IDs, changed paths, dependency/lockfile delta, reviews, merge and archive SHAs.

## Stop conditions

Stop for a required framework/architecture decision, input-actions producer defect, ownership conflict, unsafe context/tool limit, two investigated heavy failures or no READY work. Do not edit app composition or invent product bindings to demonstrate usage.

## Final response

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE | PRODUCER_COMPLETE
RESULT: <bounded platform adapter outcome>
VALIDATION: <focused/component/audit/E2E boundary/exact-head CI>
DURABLE_STATE: <task, branch, head, PR, archive>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
