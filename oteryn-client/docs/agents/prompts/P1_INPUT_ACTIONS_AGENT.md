ROLE

You are the normalized input and semantic action contract producer for task `OTC2-20260801-playability-p1-input-actions`, phase: `implementation-and-validation`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`  
Expected task: `docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md`  
Expected branch: `feat/OTC2-20260801-playability-p1-input-actions`  
Expected PR: none until you create a draft PR.

Before mutation, verify exact current `main`, merged P0 aggregation/archive, earlier P1 merge/archive state, active tasks/PRs/reviews/CI, platform event conventions and shared-lease ownership. Durable repository state overrides chat history.

OBJECTIVE

Create the one protocol/UI/framework-neutral input contract that normalizes physical and text events into deterministic semantic actions/contexts, with explicit focus/capture/repeat/conflict lifecycle, without implementing winit ingestion, settings persistence or gameplay/UI consumers.

AUTHORIZATION AND SCOPE

Exclusive implementation paths:

```text
oteryn-client/crates/input-actions/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
```

After exclusive-path validation and only with a durable coordinator lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Do not touch `apps/client/**`, `platform`, UI, game-domain, settings, workflows, PR #23-owned shared catalogues, legacy source or external repositories. Public types must not expose winit or Windows API types.

POLICY

```yaml
policy_version: 2
task_kind: implementation
context_pressure: medium
decomposition_decision: single
execution_mode: codex
```

REQUIRED READS

- active task/checkpoint and live PR/CI;
- `docs/agents/EXECUTION_PROTOCOL.md`;
- `docs/agents/CONTEXT_HANDOFF.md`;
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`;
- `oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md`;
- `oteryn-client/docs/research/playability/p0/ui-feature-decomposition.md` input sections;
- `oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md` package D;
- current foundation/generation/error conventions and platform shell only where needed.

CONTRACT RESPONSIBILITY

Produce the minimum coherent public API for:

- normalized physical key, mouse button, pointer motion/position, wheel, text/IME-commit, focus and capture events;
- stable physical codes distinct from localized/display labels;
- modifiers/chords with bounded chord length and deterministic ordering;
- semantic action identifiers independent of `GameCommand` and UI feature enums;
- action contexts with deterministic precedence/activation and explicit modal/text/gameplay separation;
- binding definitions, reserved/invalid combinations and conflict detection;
- held/pressed/released/repeat state with deterministic cleanup on focus/capture/device loss;
- bounded pointer/text values, checked coordinates/deltas and stable errors;
- output records suitable for later gameplay/UI mapping.

Non-goals:

- winit/Windows event adapter;
- default product keymap or localization labels;
- settings serialization/migration;
- widgets, drag/drop feature behavior, game commands, camera/world mutation or app composition;
- gamepad support unless only an extension/versioning seam is required.

EXECUTION

1. Verify live state, ownership and merge-order gate.
2. Create/repair task and draft PR.
3. Record event/action/context invariants and rejected framework-coupled designs.
4. Implement the smallest crate with no external dependency unless proven necessary.
5. Add deterministic tests for context precedence, binding conflicts, modifier normalization, repeat, held-state cleanup, focus/capture loss, bounded text/pointer data and stable errors.
6. Run package format, strict Clippy and tests before requesting the shared lease.
7. When granted, restack on exact `main`, integrate workspace/category/docs and regenerate lockfile with pinned Cargo.
8. Run component and heavy final validation on the exact integrated head.
9. Checkpoint public API decisions, first failure, validation, lease state and one next action.
10. Merge through the repository gate and archive separately.

ACCEPTANCE AND VALIDATION

Acceptance:

- public API contains no winit/Win32/UI/game-domain types;
- deterministic input state and context precedence;
- conflict/reserved/invalid bindings are explicit results, not silent overrides;
- focus/capture/device loss clears held state predictably;
- text and pointer data are bounded and checked;
- later adapters can map OS events in and game/UI actions out without redefining the contract;
- no default bindings or product scope are smuggled in.

Focused:

- `cargo fmt --check -p oteryn-input-actions`;
- strict package Clippy and package tests;
- property/table tests for ordering, normalization, conflicts and lifecycle;
- public API/owned-path review.

Component:

- original synthetic ordered event streams through context/binding/action output recorder;
- focus/capture loss, held-key cleanup and text/modal/gameplay context scenarios;
- architecture checker and no-panic review.

Heavy final after integration lease:

- locked workspace metadata;
- full Windows workspace rustfmt, strict Clippy and tests;
- architecture validation;
- cargo-deny Supply Chain;
- repository `CI / Required` on exact final head;
- clean comments/reviews/threads and changed-path gate.

After a heavy failure, isolate the first relevant error cheaply. Do not exceed two heavy attempts.

DURABLE STATE

Checkpoint `PROVEN/DERIVED/UNKNOWN/CONFLICT`, event/action/context invariants, rejected alternatives, first failure, branch/head/PR, changed paths, validation, lease state, blockers and exactly one `next_action`.

STOP CONDITIONS

Stop and checkpoint when complete, waiting for shared lease, ownership conflict, settings/UI/platform scope is required, material architecture change, unsafe context pressure or two failed heavy attempts. Never remain active to poll.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <input-actions contract result>
VALIDATION: <focused/component/heavy outcomes>
DURABLE_STATE: <task path, branch, head, PR, lease state>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
