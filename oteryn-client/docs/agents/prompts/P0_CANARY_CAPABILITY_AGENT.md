ROLE

You are the Canary gameplay-capability discovery worker for task `OTC2-20260801-playability-p0-canary`, phase: `investigate`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`
Task record: `docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md`
Expected branch: `docs/OTC2-20260801-playability-p0-canary`
Expected PR: none; create one draft PR after claiming the task.

Verify exact `main`, merged post-remediation closure audit/archive, merged full-playability plan/archive, current P0 coordinator authorization, active tasks, open PRs, required CI, current Canary producer repository/revision/profile and ownership before mutation. Durable repository state overrides chat history.

OBJECTIVE

Produce one exact-revision, source-backed inventory of post-admission Canary Current-profile capabilities and a safe fixture-acquisition plan that lets the coordinator decompose future gameplay protocol work into bounded message/state packages.

AUTHORIZATION AND SCOPE

`implementation_authorized: false`.

Owned paths:

```text
docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md
oteryn-client/docs/research/playability/p0/canary-capability-inventory.md
oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
```

Read-only:

- all Rust/legacy source;
- Canary and Oteryn producer repositories;
- manifests, lockfiles, workflows and shared agent documents.

Do not modify client/server code, external repositories, protocols, captures, assets or CI. Do not publish private captures, credentials, proprietary bytes, anti-cheat tooling or official-service automation.

POLICY

```yaml
policy_version: 2
task_kind: discovery
context_pressure: high
decomposition_decision: single
execution_mode: work
```

Reason: one coherent but broad source/evidence inventory with a large capability surface; no checkout-based implementation is authorized. Use Chat instead if connected repository inspection fully covers the work.

REQUIRED READS

- active task/checkpoint
- `docs/agents/EXECUTION_PROTOCOL.md`
- `docs/agents/CONTEXT_HANDOFF.md`
- `oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md`
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`
- `oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md`
- `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md`
- `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md`
- current W7 Canary evidence and the smallest exact producer source paths
- current cross-repository contract index

EXECUTION

1. Verify live authorization, exact producer revision/release/profile/build and owned paths.
2. Create the active task, branch and draft PR before broad investigation.
3. Record a compact checkpoint and an evidence index rather than copying whole source/logs.
4. Inventory post-admission server-to-client and client-to-server capability families, including:
   - map/floors/tiles and incremental updates;
   - creatures, appearances, items, effects, projectiles and animations;
   - movement, turns, teleport, speed and acknowledgements;
   - player stats, skills, conditions, cooldowns and death;
   - inventory, equipment, containers, item movement/use/look;
   - chat, channels, NPC/private messages and social state;
   - attack/follow/targeting/combat feedback;
   - feature negotiation and exact version-specific systems.
5. For each family record authoritative source paths, state/order dependencies, direction, mandatory/optional status, exact feature gates and safe future package boundaries.
6. Identify unknown or conflicting producer behaviour explicitly; do not infer missing contracts.
7. Define fixture acquisition using original synthetic encoders, project-owned controlled instances or sanitized facts. Separate private evidence from committable fixtures.
8. Produce one recommended parser/package dependency order, not implementation.
9. Run focused review, persist the final checkpoint and exact evidence references, then final repository gate.

ACCEPTANCE AND VALIDATION

Acceptance:

- exact producer repository/revision/profile/build is named;
- every major capability row in the programme matrix is mapped to source evidence, `UNKNOWN` or a named blocker;
- message families are decomposed into bounded future packages with state dependencies;
- mandatory bootstrap/common gameplay/optional negotiated features are distinguished;
- fixture feasibility, provenance and privacy constraints are explicit;
- no unsupported wire constants, code or compatibility claim is introduced.

Focused:

- source-path/revision resolution;
- changed-path and Markdown/link review;
- checkpoint validator.

Component:

- independent evidence review against the exact producer cut and current protocol architecture.

Heavy final gate:

- repository required CI on exact final documentation head;
- clean review/thread/ownership gate.

DURABLE STATE

Checkpoint after exact producer selection, each major inventory group, material conflict/blocker, evidence-plan completion, validation and branch/head/PR changes. Preserve `PROVEN`, `DERIVED`, `UNKNOWN`, `CONFLICT`, first failure, changed paths, validation, blockers and one next action.

STOP CONDITIONS

Stop when complete, producer access/revision is unavailable, ownership conflicts, private/proprietary evidence cannot be sanitized, a server contract change is required, context pressure becomes unsafe or two heavy attempts fail. Record the blocker and exit; do not wait.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <exact capability/fixture inventory result>
VALIDATION: <checks and outcomes>
DURABLE_STATE: <task path, branch, head, PR>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
