ROLE

You are the user-workflow and legacy-parity discovery worker for task `OTC2-20260801-playability-p0-legacy`, phase: `investigate`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`
Task record: `docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md`
Expected branch: `docs/OTC2-20260801-playability-p0-legacy`
Expected PR: none; create one draft PR after claiming the task.

Verify exact `main`, merged closure audit/archive, merged full-playability plan/archive, P0 coordinator authorization, active tasks, open PRs/reviews, required CI and ownership. Durable repository state overrides chat history.

OBJECTIVE

Produce one evidence-backed catalogue of player-visible workflows and functional parity scenarios from the repository's legacy client and approved original-client evidence, while keeping the new Rust architecture independent from legacy implementation structure.

AUTHORIZATION AND SCOPE

`implementation_authorized: false`.

Owned paths:

```text
docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md
oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md
oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md
```

Read-only:

- legacy `src/**`, `modules/**`, `mods/**`, tests and documentation;
- approved official-client static/behavioural evidence already available to the project;
- all Rust source, manifests, lockfiles, workflows and shared agent files.

Do not modify legacy or Rust code. Do not extract or commit proprietary assets/binaries, automate official services, reverse anti-cheat, or treat legacy architecture as normative.

POLICY

```yaml
policy_version: 2
task_kind: discovery
context_pressure: high
decomposition_decision: single
execution_mode: work
```

Reason: one broad but cohesive behavioural inventory across many modules and user journeys; no implementation is authorized. Use Chat if repository inspection alone is sufficient.

REQUIRED READS

- active task/checkpoint
- `docs/agents/EXECUTION_PROTOCOL.md`
- `docs/agents/CONTEXT_HANDOFF.md`
- `oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md`
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`
- `oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md`
- current legacy task/PR ownership, especially PR #23 and operational asset work
- the smallest relevant legacy modules/tests per workflow

EXECUTION

1. Verify live authorization and create one task, branch and draft PR.
2. Record exact legacy evidence cuts and a compact checkpoint.
3. Inventory user journeys from installation/start through authentication, selection, gameplay, failure recovery, relog and exit.
4. Catalogue observable workflows for:
   - viewport/camera/movement;
   - HUD, stats, skills and status;
   - creatures, targeting, combat and death;
   - items, inventory, equipment and containers;
   - chat, NPC, private/social channels;
   - minimap, hotkeys/action bars and settings;
   - trade, depot, market and version-specific feature panels when present;
   - update/asset repair/error/reconnect behaviours.
5. For each scenario record preconditions, player actions, observable outcomes, failure/recovery expectations, exact evidence paths and whether it is core, daily-product, version-specific or intentionally excluded.
6. Separate server-required behaviour, presentation preference and legacy implementation accident.
7. Record behaviours that should not be copied because they conflict with security, architecture, accessibility, legal or product goals.
8. Map scenarios to M1-M6 and to capability matrix rows; do not choose implementation libraries or public contracts.
9. Run focused review, persist final checkpoint/evidence references and final repository gate.

ACCEPTANCE AND VALIDATION

Acceptance:

- all major player workflows have evidence paths and observable acceptance;
- core playability, daily-product and version-specific parity are separated;
- server capability dependencies and unknowns are explicit;
- legacy behaviour is translated into user outcomes, not copied class/module design;
- intentional non-parity decisions are recommendations, not silent omissions;
- no source/assets/binaries or proprietary material are added.

Focused:

- exact evidence path resolution;
- changed-path and Markdown/link review;
- checkpoint validator.

Component:

- independent review against representative legacy modules/tests and the programme milestone definitions.

Heavy final gate:

- repository required CI on exact final documentation head;
- clean review/thread/ownership gate.

DURABLE STATE

Checkpoint after each major workflow group, material conflict/unknown, scenario catalogue completion, validation and branch/head/PR changes. Externalize large inventories into the two owned reports. Preserve one exact next action.

STOP CONDITIONS

Stop when complete, ownership conflicts, required evidence is unavailable or proprietary, a product decision is required, context pressure becomes unsafe or two heavy attempts fail. Record the blocker and exit; do not wait.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <workflow/parity inventory result>
VALIDATION: <checks and outcomes>
DURABLE_STATE: <task path, branch, head, PR>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
