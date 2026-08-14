# OTC-20260814 — official-client capability experiment research design

```yaml
task_id: OTC-20260814-official-client-capability-experiment-sweep
programme: OTCLIENT-TIBIA-RE
track: official-client-re
status: completed
repository: blakinio/otclient
task_kind: research_design
completion_scope: research_design_only
merged_design_pr: 293
merged_design_commit: 42226155ee3afdcef380f6400a2fefc52061ada3
archive_pr: 294
runtime_claims_by_this_task: none
runtime_e2e: NOT_APPLICABLE_WITH_REASON
ownership_release_state: released
archive_closeout_state: pending_archive_pr_merge
```

## Result

The Track A official native-Linux Tibia capability experiment design was finalized, exact-head validated and merged through PR #293. This task is a **research-design deliverable only**; it does not claim that the 75-family runtime capability sweep has already been executed.

The canonical programme remains:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
```

Future runtime work must execute bounded hypotheses/phases against the exact current official Linux client and persist evidence according to the merged execution model.

## Durable design set

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
```

## PR #293 acceptance evidence

- exact final PR head before merge: `cbd10b0627299f54ad1f8250d138c851f5658ac5`;
- CI run `31782867711` (`CI` #2668);
- `Detect Build Scope`: `success`;
- `Lua Syntax / Check Lua Syntax`: `success`;
- `Fast Checks / Syntax and workflow validation`: `success`;
- `Fast Checks / Informational static analysis`: `success`;
- `Build - Windows`: `skipped` because compile scope was false for the documentation-only diff;
- `CI / Required` job `94712726508`: `success`;
- no blocking review or unresolved review thread existed at PR #293 merge;
- PR #293 was squash-merged to `main` as `42226155ee3afdcef380f6400a2fefc52061ada3`.

Runtime E2E is `NOT_APPLICABLE_WITH_REASON`: live runtime proof belongs to subsequent bounded `OTCLIENT-TIBIA-RE` execution work, not to this documentation/research-contract task.

## Independent closeout audit

A fresh independent GitHub review was performed on archive PR #294 by:

```yaml
validator: chatgpt-codex-connector
review_id: PRR_kwDOTVmdjs8AAAABJipsBA
reviewed_head: 40f8268196d07db2b883b93e4832b0e16abc0a98
initial_result: findings
material_findings: 2
```

The independent audit found exactly these material closeout gaps:

1. `P1`: the archived record did not persist the independent-audit identity/result before declaring completion;
2. `P2`: the archived record did not explicitly prove release of the seven formerly owned paths.

Both findings are remediated by this archive-record revision. The audit is therefore recorded as:

```yaml
audit_status: findings_remediated
open_material_findings_after_remediation: 0
follow_up_requirement: exact-head CI plus resolution of both review threads before archive PR merge
```

The original design-review report remains design rationale; it is **not** being misrepresented as the independent post-implementation audit. The independent audit evidence is the PR #294 review above.

## Ownership release

The design task no longer owns any implementation/research path. The following former advisory locks are explicitly released for future correctly claimed Track A tasks after this archive PR merges:

```yaml
former_owned_paths:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
  - docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
  - docs/agents/tasks/active/OTC-20260814-official-client-capability-experiment-sweep.md
ownership:
  state: released
  reason: research-design PR 293 merged; future runtime work belongs to bounded OTCLIENT-TIBIA-RE execution tasks
  released_effective_on: merge of archive PR 294
```

No future worker may treat this archived task as an active ownership claim.

## Durable methodology delivered

The merged research design establishes:

- offline `S0/S1/S2` identity, exhaustive census and graph/probe planning before unnecessary login;
- live `L0-L6` execution only after structural `IN_GAME`;
- competing inbound/outbound topology hypotheses rather than assuming one common bus;
- causal recorder plus no-stimulus noise baseline;
- independent read gates `R0-R4` and action gates `A0-A4`;
- normal-client reference-path parity before semantic action promotion;
- explicit abort/recovery and side-effect budgets;
- full generated-message schema extraction where possible;
- runtime graph `message -> queue -> handler -> storage -> controller/model`;
- machine-readable capability/protocol/runtime/experiment registries;
- measurable coverage gates;
- fresh PID/PIE validation for important promotions;
- rare-event evidence states and privacy minimization;
- first-class World/Server Event Intelligence;
- E51-E75 coverage including party/shared experience, player trade, NPC trade, Wheel, Forge, Bestiary/Bosstiary, Prey, Taskboard/Soul Seals, Houses, Imbuements, Weapon Proficiency, Quick Loot, analyzers, Friends/VIP, Quest, Reward Wall, network/latency, server modal/death/disconnect and unclassified features.

## Historical evidence boundary

The design preserves version-fenced static evidence from official Linux client `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, including retained inventories for 349 generated protocol messages and QMeta/action/state subsystem leads. Static presence is not a current live API until revalidated on the exact current binary.

## Post-archive programme continuation

Exact next programme action:

```text
Resolve the current official Linux client version/SHA, execute the exhaustive unfiltered S1 protocol/QMeta/runtime census, build the S2 dependency graph and machine-readable registries, rank P0 probes by information gain, then resolve the approved live login/recovery path, structurally prove IN_GAME, and begin L1 causal inbound/outbound topology correlation before promoting position/HP/mana/map/creature/inventory/container/chat/world-event reads.
```

No further action belongs to this archived design task after PR #294 merges and its review threads are resolved.
