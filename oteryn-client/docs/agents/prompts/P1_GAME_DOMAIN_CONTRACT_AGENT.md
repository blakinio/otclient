ROLE

You are the sole game-domain public-contract producer for task `OTC2-20260801-playability-p1-game-domain-contract`, phase: `implementation-and-validation`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`  
Project lane: `otclient-v2`  
Expected task: `docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md`  
Expected branch: `feat/OTC2-20260801-playability-p1-game-domain-contract`  
Expected PR: none until you create a draft PR.

Before mutation, verify exact current `main`, merged P0 aggregation and archive, active tasks/checkpoints, open PRs/reviews, required CI, architecture policy and path ownership. Durable repository state overrides chat history. Do not start if another task owns `crates/game-domain/**` or the shared integration lease.

OBJECTIVE

Create the one canonical, protocol-neutral gameplay contract crate that owns session-scoped identifiers plus closed/versioned `GameEvent` and `GameCommand` envelopes required by the minimum M2 spine, without implementing simulation or Canary wire mapping.

AUTHORIZATION AND SCOPE

Implementation is authorized only within:

```text
oteryn-client/crates/game-domain/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
```

After exclusive-path focused/component validation, the coordinator may grant a temporary shared integration lease for:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Do not edit shared paths before the lease is durably recorded. Do not touch `apps/client/**`, workflows, PR #23-owned shared catalogues, protocol crates, renderer, UI, assets, legacy source or producer repositories.

The crate must not contain Canary opcodes/layouts, socket ownership, mutable world state, render snapshots, widgets, platform types or app composition.

POLICY

```yaml
policy_version: 2
task_kind: implementation
context_pressure: high
decomposition_decision: single
execution_mode: codex
```

REQUIRED READS

- the active task/checkpoint and live PR/CI;
- `docs/agents/EXECUTION_PROTOCOL.md`;
- `docs/agents/CONTEXT_HANDOFF.md`;
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`;
- `oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md` game-domain rows;
- `oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md` package A;
- existing `foundation`, `protocol-core`, `game-session` and architecture policy only where needed.

OBJECT MODEL

Produce the smallest coherent public contract including:

- a session generation/token that makes stale identifiers rejectable;
- canonical strongly typed IDs/handles for entity/creature, item, container and tile/position concepts needed by M2/M3 seams;
- bounded position/floor and stack/order primitives without renderer policy;
- bounded text/value payload types where envelopes require external text;
- closed `GameEvent` variants for minimum bootstrap/map/entity/movement/player/item/container/session lifecycle semantics;
- closed `GameCommand` variants for minimum movement/look/use/move-item/target/session semantics, only where shared now;
- explicit envelope versioning/extension policy;
- stable typed errors and redacted/debug-safe output.

Prefer fewer well-owned variants over speculative feature coverage. Optional economy/social/modern systems remain later extensions.

EXECUTION

1. Verify live state, exact ownership and accepted next action.
2. Create/repair the task and draft PR before substantive work.
3. Inspect current foundation/generation/error conventions and architecture categories.
4. Design the minimum public API and record rejected alternatives in the checkpoint.
5. Implement the crate without external dependencies unless evidence proves one is required.
6. Add focused tests for equality/order/hash semantics, bounds, invalid combinations, stale generations, redaction and envelope version behavior.
7. Run package formatting, strict Clippy and tests before requesting the shared lease.
8. Obtain the integration lease, restack on exact `main`, add workspace/category/docs integration and regenerate `Cargo.lock` only with pinned Cargo.
9. Run component and heavy final validation on the exact integrated head.
10. Update the checkpoint after material decisions, first failure, validation, head/PR changes and before session rotation.
11. Merge only through the repository gate and archive the task in a separate PR.

ACCEPTANCE AND VALIDATION

Acceptance:

- exactly one canonical ID/handle family and one `GameEvent`/`GameCommand` producer;
- no protocol/profile/UI/renderer/simulation dependency leakage;
- all externally sourced values are bounded and checked;
- stale-session identifiers fail deterministically;
- public Debug/errors expose no raw external text beyond accepted bounded/redacted fields;
- architecture edges are explicit and complete;
- downstream producers can consume the crate without private substitute types.

Focused:

- `cargo fmt --check -p oteryn-game-domain`;
- strict package Clippy with pinned toolchain;
- package tests including malformed/boundary/stale-generation cases;
- public API and owned-path review.

Component:

- direct fixture tests with `foundation`, `protocol-core`-neutral builders and test-support as permitted;
- architecture checker for new category/edges;
- deterministic teardown/no-panic review.

Heavy final after integration lease:

- locked workspace metadata;
- full Windows workspace rustfmt, strict Clippy and tests;
- architecture policy validation;
- cargo-deny Supply Chain;
- repository `CI / Required` on exact final head;
- clean comments/reviews/threads and exact changed-path gate.

After a heavy failure, isolate the first relevant error cheaply before another full attempt. Do not exceed two heavy attempts in one session.

DURABLE STATE

Checkpoint `PROVEN`, `DERIVED`, `UNKNOWN`, `CONFLICT`, rejected hypotheses, first failure, exact branch/head/PR, changed paths, validation, blockers, lease state and exactly one `next_action`.

STOP CONDITIONS

Stop and checkpoint when complete, blocked, waiting for the shared lease, ownership conflict, material architecture change, owner authorization requirement, unsafe context pressure or two failed heavy attempts. Never remain active merely to poll.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <contract implemented or exact blocker>
VALIDATION: <focused/component/heavy outcomes>
DURABLE_STATE: <task path, branch, head, PR, lease state>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
