# P0 Full-Playability Discovery Wave

Status: launch plan only after all gates below pass  
Wave ID: `OTERYN-PLAYABILITY-P0-DISCOVERY`  
Task shape: `split` independent discovery outputs plus one aggregation barrier  
Implementation authorized: **false**

## 1. Launch gates

No P0 worker may start until:

1. post-remediation closure audit PR #133 and its separate lifecycle archive are merged;
2. full-playability programme planning PR and its separate lifecycle archive are merged;
3. exact `main`, active tasks, open PRs, review state and required CI are rechecked;
4. no existing task/PR owns a P0 output path;
5. each worker creates one active task, one branch and one draft PR;
6. coordinator records the exact worker set and confirms no source/shared-path lease is granted.

If any gate is missing, the coordinator records `WAITING` and exits. It does not keep polling.

## 2. Wave topology

```text
                         P0-C coordinator
                               |
       +-----------------------+-----------------------+
       |                       |                       |
 P0-CANARY               P0-LEGACY               P0-ASSET
       |                       |                       |
       +---------------+-------+-------+---------------+
                       |               |
                    P0-UX         P0-RELEASE
                       |               |
                       +-------+-------+
                               |
                        P0 aggregation
                               |
        update capability matrix + accept smallest P1 plan
```

Maximum active sessions: one coordinator plus five workers. All workers are docs/evidence-only and independent.

## 3. P0-C — Coordinator and aggregation

Prompt:

```text
oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
```

Coordinator responsibilities:

- verify launch gates and current ownership;
- create or verify exact worker tasks/branches/draft PRs;
- prohibit source/manifests/workflows/shared catalogue edits;
- avoid answering each worker's technical questions unless a true cross-contract decision exists;
- close its launch session after durable dispatch rather than waiting;
- at the barrier, verify merged/archived worker evidence;
- normalize findings into `CAPABILITY_MATRIX.md` using `PROVEN/PARTIAL/SYNTHETIC_ONLY/UNKNOWN/BLOCKED/ABSENT/DEFERRED`;
- classify every capability as release-required, later, or owner-decision-needed;
- identify sole P1 contract producers and exact merge order;
- publish one bounded P1 plan and prompts; no gameplay implementation in the barrier task;
- archive the barrier task separately.

The coordinator must not rewrite worker reports into unsupported conclusions.

## 4. P0-CANARY — Exact server capability and fixture inventory

Prompt:

```text
oteryn-client/docs/agents/prompts/P0_CANARY_CAPABILITY_AGENT.md
```

Proposed task:

```text
OTC2-20260801-playability-p0-canary
```

Exclusive output paths:

```text
oteryn-client/docs/research/playability/p0/canary-capability-inventory.md
oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md
```

Objective:

Produce an exact-revision, source-backed inventory of all post-admission Canary Current-profile capabilities required for client gameplay, including message families, ordering/state dependencies, server feature gates, command/event direction and sanitized fixture feasibility.

Required result:

- exact repository/revision/release/profile/build evidence;
- authoritative source paths for map, movement, creatures, items/effects, player state, inventory/containers, chat, combat and version-specific features;
- distinction between mandatory login/world bootstrap, common gameplay and optional negotiated features;
- packet/state families grouped into bounded future parser packages, not one mega-parser;
- private/synthetic fixture acquisition plan with provenance and no secrets/proprietary bytes;
- blockers requiring producer changes or controlled runtime capture;
- no client or server implementation.

## 5. P0-LEGACY — User workflow and compatibility inventory

Prompt:

```text
oteryn-client/docs/agents/prompts/P0_LEGACY_PARITY_AGENT.md
```

Proposed task:

```text
OTC2-20260801-playability-p0-legacy
```

Exclusive output paths:

```text
oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md
oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md
docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md
```

Objective:

Inventory player-visible workflows and compatibility behaviour from the repository's legacy client and approved original-client evidence, without treating legacy implementation structure as the new architecture.

Required result:

- workflows from login through normal play, error recovery and logout;
- feature/user-story catalogue with preconditions, actions and observable outcomes;
- distinction between core playability, daily-product expectations and version-specific parity;
- exact legacy modules/source paths as evidence;
- gaps or behaviours that should intentionally not be copied;
- no source changes, proprietary asset extraction or official-service automation.

## 6. P0-ASSET — Asset source, importer and runtime decision inventory

Prompt:

```text
oteryn-client/docs/agents/prompts/P0_ASSET_PIPELINE_AGENT.md
```

Proposed task:

```text
OTC2-20260801-playability-p0-assets
```

Exclusive output paths:

```text
oteryn-client/docs/research/playability/p0/asset-source-and-rights-matrix.md
oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md
docs/agents/tasks/active/OTC2-20260801-playability-p0-assets.md
```

Objective:

Define the smallest legally and technically safe path from approved source inputs to runtime-visible sprites, text and audio, building on the existing synthetic schema/compiler without claiming production rights or format support.

Required result:

- source categories and rights/provenance status;
- local-import versus redistribution boundaries;
- exact required appearance/sprite/font/audio metadata for M2-M5;
- importer and runtime threat boundaries;
- proposed bounded package order: pack open/verify/index, decode, logical handles, upload/streaming, importer families and signing;
- test fixture strategy using original synthetic or approved inputs;
- explicit owner decisions/blockers;
- no asset bytes, importer/runtime code or pack schema changes.

## 7. P0-UX — Windows UI, input, audio and accessibility inventory

Prompt:

```text
oteryn-client/docs/agents/prompts/P0_UX_INPUT_AUDIO_AGENT.md
```

Proposed task:

```text
OTC2-20260801-playability-p0-ux
```

Exclusive output paths:

```text
oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md
oteryn-client/docs/research/playability/p0/ui-feature-decomposition.md
docs/agents/tasks/active/OTC2-20260801-playability-p0-ux.md
```

Objective:

Define native Windows presentation, semantic input and audio capability requirements and decompose them into architecture-safe core versus feature packages.

Required result:

- login/selection/game HUD/panels/modal/error workflows;
- retained UI core primitives and concrete feature separation;
- DPI, focus, IME, clipboard, drag/drop, mouse capture, keyboard navigation and accessibility acceptance;
- input actions/contexts/hotkeys/conflict rules;
- audio backend/device/category/positional/UI requirements;
- dependency order and synthetic test harnesses;
- no library selection or implementation unless the evidence is required only as a recommendation;
- no UI cloning or proprietary visual extraction.

## 8. P0-RELEASE — Controlled E2E, performance and product delivery inventory

Prompt:

```text
oteryn-client/docs/agents/prompts/P0_RELEASE_E2E_AGENT.md
```

Proposed task:

```text
OTC2-20260801-playability-p0-release
```

Exclusive output paths:

```text
oteryn-client/docs/research/playability/p0/staging-e2e-and-release-plan.md
oteryn-client/docs/research/playability/p0/performance-reliability-acceptance.md
docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md
```

Objective:

Define exact controlled-environment, Windows runtime, E2E, performance, soak, packaging, updater and release evidence required for M1-M6.

Required result:

- real technical-login staging prerequisites and evidence capture rules;
- scenario ladder from M1 admission through M5 parity;
- Windows/driver/hardware support matrix candidates;
- frame-time, memory, network, startup and asset-load budget methodology without inventing final numbers;
- network-loss, device-loss, crash, update rollback and multi-hour soak scenarios;
- artifact/privacy/secret handling;
- launcher/update/signing/packaging dependency map;
- owner/deployment decisions and external blockers;
- no deployment, credential use, workflow or implementation.

## 9. Worker validation

Focused validation for every P0 worker:

- exact changed paths match declared ownership;
- cited source/revision/PR evidence is resolvable;
- no secret, private capture, proprietary binary or unsupported claim appears;
- task checkpoint validates with `tools/agents/checkpoint.py`;
- Markdown/path/link review passes.

Component validation:

- fresh independent review of the worker report against its stated sources;
- contradictions and `UNKNOWN` items are explicit.

Heavy final gate:

- repository required CI on exact final documentation head;
- clean review/thread/ownership gate.

No Rust Client heavy matrix is required solely for docs unless path scope or repository policy triggers it.

## 10. Merge and barrier order

The five worker outputs are independent and may merge in any order after validation. Each receives a separate lifecycle archive PR.

After all are merged/archived or durably blocked:

1. coordinator opens one aggregation task/branch/draft PR;
2. restacks on exact current `main`;
3. updates programme capability matrix and dependency graph only from accepted evidence;
4. resolves duplicate or conflicting feature names/requirements;
5. records owner decisions separately from technical facts;
6. accepts the smallest P1 package set with exact sole producers, owned paths and validation;
7. prepares only the prompts for that P1 wave;
8. merges and separately archives the aggregation task.

## 11. P0 completion rule

P0 is complete when:

- all five reports are merged and archived or explicitly blocked with one next action;
- every major `UNKNOWN` in the current matrix is either evidenced, narrowed or assigned a named blocker;
- the coordinator publishes one normalized release-required capability set;
- exact sole producers and dependency order for P1 are accepted;
- no P0 task, branch lease or unarchived worker remains;
- no implementation was smuggled into discovery.
