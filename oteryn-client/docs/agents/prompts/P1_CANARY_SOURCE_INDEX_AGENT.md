ROLE

You are the exact-source Canary protocol index and fixture-metadata producer for task `OTC2-20260801-playability-p1-canary-source-index`, phase: `tooling-and-evidence`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`  
Producer repository: `blakinio/canary` read-only  
Expected task: `docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md`  
Expected branch: `tools/OTC2-20260801-playability-p1-canary-source-index`  
Expected PR: none until you create a draft PR.

Before mutation, verify exact current client `main`, merged P0 aggregation/archive, exact accepted Canary cut, active tasks/PRs/reviews/CI and all owned paths. Durable repository state overrides chat history.

OBJECTIVE

Mechanically generate and independently validate an exact-source index for the accepted Canary Current profile, plus privacy-safe fixture feasibility metadata, so later bounded protocol packages consume evidence rather than handwritten opcode/layout assumptions.

AUTHORIZATION AND SCOPE

Implementation is authorized only within:

```text
oteryn-client/tools/canary-protocol-index/**
oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
```

No workspace member, root manifest, lockfile, architecture policy, workflow, client/server runtime source, producer mutation, deployment or account use.

Default inspected producer cut:

```text
blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3
Canary 3.6.1
client version 1525
ProtocolProfileId::Current
```

If owner/operations durable evidence names a replacement cut before work begins, checkpoint the conflict and use only the newly accepted exact cut. Never blend cuts.

POLICY

```yaml
policy_version: 2
task_kind: implementation
context_pressure: high
decomposition_decision: single
execution_mode: codex
```

REQUIRED READS

- active task/checkpoint and live PR/CI;
- `docs/agents/EXECUTION_PROTOCOL.md`;
- `docs/agents/CONTEXT_HANDOFF.md`;
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`;
- `oteryn-client/docs/research/playability/p0/canary-capability-inventory.md`;
- `oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md`;
- `oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md` package B;
- only exact producer profile/port/session/protocol sources required by the generator.

GENERATED INDEX CONTRACT

For each resolvable Current-profile message or command, produce normalized evidence fields:

- direction: client-to-server or server-to-client;
- numeric opcode or explicit unresolved marker;
- parser handler or send method;
- exact source file and source anchor;
- profile/build/feature gate;
- wire layout source function(s), not copied implementation bodies;
- order/state prerequisite;
- capability family and proposed bounded future package;
- fixture feasibility: source-derived metadata, project-original synthetic, controlled runtime required or blocked;
- conflict/ambiguity marker.

The committed reports may summarize and link to a deterministic generated artifact. Large indexes belong in a generated file/artifact path under the owned tool/evidence tree, not in the task checkpoint.

SECURITY AND RIGHTS

Prohibited:

- credentials, tickets, session hashes/keys or personal data;
- private or official-service packet captures;
- proprietary asset/audio/font bytes;
- copied server function bodies or broad source redistribution;
- guessed opcodes/layouts;
- claims that the inspected source equals deployment without evidence.

Source-derived numeric constants, paths, names and normalized structural metadata are permitted when necessary for interoperability evidence and kept minimal.

EXECUTION

1. Verify the exact producer cut and client barrier state.
2. Create/repair task and draft PR.
3. Build the smallest deterministic parser/indexer with explicit supported source grammar and stable errors.
4. Generate the index twice from a clean state and prove byte-identical output.
5. Reconcile representative bootstrap, map, entity, movement, player, item/container, chat and combat families manually against exact source.
6. Mark unsupported macros/dynamic construction/ambiguous layouts as conflicts instead of guessing.
7. Produce the source index and fixture-feasibility report with provenance and privacy rules.
8. Run focused tests, component reconciliation and repository CI.
9. Checkpoint exact source SHA, tool version/head, artifact hashes, first failure and one next action.
10. Merge through the repository gate and archive the task separately.

ACCEPTANCE AND VALIDATION

Acceptance:

- one exact source cut and profile;
- deterministic index generation;
- every major P0 capability family is indexed, explicitly unresolved or blocked;
- direction/opcode/source/gate/state/package fields are present where source permits;
- no runtime public Rust contract is introduced;
- no secret/private/proprietary content;
- discrepancies with P0 prose are recorded and source wins.

Focused:

- tool unit tests for parsing, normalization, stable ordering and malformed/unsupported source constructs;
- two clean generations with identical hashes;
- changed-path and privacy scan.

Component:

- manual/automated reconciliation of representative message families against exact producer files;
- compare generated profile/build gates with `protocol_profile.*`, port routing and `protocolgame.*`;
- independent report review for unsupported claims.

Heavy final:

- repository required CI on exact final head;
- clean comments/reviews/threads and ownership gate;
- no Rust Client full matrix unless repository path policy triggers it.

After a heavy failure, isolate the first relevant error cheaply. Do not exceed two heavy attempts.

DURABLE STATE

Checkpoint `PROVEN`, `DERIVED`, `UNKNOWN`, `CONFLICT`, source cut, generator head/version, output hashes, rejected hypotheses, first failure, changed paths, validation, blockers and exactly one `next_action`.

STOP CONDITIONS

Stop and checkpoint when complete, source cut conflict, source access unavailable, extraction requires prohibited content, ownership conflict, owner authorization requirement, unsafe context pressure or two failed heavy attempts. Never wait or poll.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <generated exact-source index result>
VALIDATION: <determinism/reconciliation/CI>
DURABLE_STATE: <task path, branch, head, PR, producer cut, output hashes>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
