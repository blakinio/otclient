# OTC-20260814 — official-client capability experiment research design

```yaml
task_id: OTC-20260814-official-client-capability-experiment-sweep
programme: OTCLIENT-TIBIA-RE
track: official-client-re
status: completed
repository: blakinio/otclient
base_branch: main
merged_pr: 293
merged_commit: 42226155ee3afdcef380f6400a2fefc52061ada3
task_kind: research_design
completion_scope: research_design_only
runtime_claims_by_this_task: none
runtime_e2e: NOT_APPLICABLE_WITH_REASON
```

## Result

The Track A official native-Linux Tibia capability experiment design was finalized, validated and merged through PR #293.

The merged design set is:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
```

This task intentionally does **not** claim that the 75-family runtime capability sweep has already been executed. The canonical programme remains `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md`; future workers execute bounded hypotheses/phases against the exact current official Linux client and persist evidence according to the merged execution model.

## Acceptance evidence

- PR #293 exact final head before merge: `cbd10b0627299f54ad1f8250d138c851f5658ac5`.
- Exact-head CI run: `31782867711` (`CI` #2668).
- `Detect Build Scope`: success.
- `Lua Syntax / Check Lua Syntax`: success.
- `Fast Checks / Syntax and workflow validation`: success.
- `Fast Checks / Informational static analysis`: success.
- `Build - Windows`: skipped because the documentation-only diff did not require compile scope.
- `CI / Required` job `94712726508`: success.
- PR had no blocking reviews or unresolved review threads at merge.
- PR #293 was squash-merged to `main` as `42226155ee3afdcef380f6400a2fefc52061ada3`.
- Runtime E2E is `NOT_APPLICABLE_WITH_REASON`: this task is a documentation/research-contract deliverable; live runtime proof belongs to subsequent bounded `OTCLIENT-TIBIA-RE` experiments.

## Durable methodology delivered

The merged design establishes:

- offline `S0/S1/S2` identity, exhaustive census and graph/probe planning before unnecessary login;
- live `L0-L6` execution after structural `IN_GAME`;
- competing inbound/outbound topology hypotheses instead of assuming one common bus;
- causal recorder plus no-stimulus noise baseline;
- independent read gates `R0-R4` and action gates `A0-A4`;
- normal-client reference-path parity before semantic action promotion;
- explicit abort/recovery and side-effect budgets;
- full generated-message schema extraction where possible;
- runtime graph `message -> queue -> handler -> storage -> controller/model`;
- machine-readable capability/protocol/runtime/experiment registries;
- measurable coverage gates;
- independent fresh PID/PIE validation for important promotions;
- rare-event evidence states and privacy minimization;
- first-class World/Server Event Intelligence;
- exhaustive E51-E75 census/feature extension including party, player trade, NPC trade, Wheel, Forge, Bestiary/Bosstiary, Prey, Taskboard/Soul Seals, Houses, Imbuements, Weapon Proficiency, Quick Loot, analyzers, Friends/VIP, Quest, Reward Wall, network/latency, server modal/death/disconnect and unclassified features.

## Historical evidence boundary

The design preserves version-fenced static evidence from official Linux client `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, including the retained inventories for 349 generated protocol messages, QMeta/action/state surfaces and subsystem leads. Static presence is not promoted to a current live API without revalidation.

## Post-archive programme continuation

Exact next programme action:

```text
Resolve the current official Linux client version/SHA, execute the exhaustive unfiltered S1 protocol/QMeta/runtime census, build the S2 dependency graph and machine-readable registries, rank P0 probes by information gain, then resolve the approved live login/recovery path, structurally prove IN_GAME, and begin L1 causal inbound/outbound topology correlation before promoting position/HP/mana/map/creature/inventory/container/chat/world-event reads.
```

No further action belongs to this archived design task.
