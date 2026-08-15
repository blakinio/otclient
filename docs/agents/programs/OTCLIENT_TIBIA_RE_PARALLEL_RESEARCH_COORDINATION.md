# OTCLIENT-TIBIA-RE parallel research coordination

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
status: operational_coordination_addendum
promotion_authority: coordinator_only
research_worker_output: draft_only
```

## Authority and scope

This document defines how the remaining Track A research may be executed in parallel. It is subordinate to, and must not weaken, the current repository governance, especially:

- `AGENTS.md` and `docs/agents/AGENTS.md`;
- `docs/agents/PROMPTING_STANDARD.md`;
- `docs/agents/PROMPTING_HANDOVER.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`;
- the current canonical `OTCLIENT-TIBIA-RE` programme, knowledge, task, evidence and closeout rules.

Track B (`blakinio/otclient -> Tibia Global compatibility`) is outside this coordination model and must not be modified by Track A workers.

## Decision

### RECOMMENDATION — adopted operating model

Use parallel **draft-only research workers** with one **promotion/integration coordinator**.

The purpose is not to make researchers passive. Each researcher may independently inspect the repository, design bounded hypotheses, create an isolated branch, implement probes/workflows/tools inside its assigned scope, run experiments, consume artifacts, falsify hypotheses, and persist durable evidence. The restriction is on **promotion**, not investigation.

A research worker must stop its repository delivery at a **Draft PR**. It must not merge its own work and must not promote its conclusions into canonical programme knowledge as established fact.

The coordinator is the sole promotion/integration authority for this campaign. The coordinator reviews each Draft PR and its raw evidence, independently checks high-impact claims, corrects classifications where necessary, resolves conflicts, and merges only accepted, current, auditable slices.

This is intentionally a two-level evidence system:

```text
research observation / experiment
        -> worker draft evidence
        -> Draft PR
        -> coordinator review
        -> ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE
        -> canonical promotion / merge
```

## Why this model fits Track A

Track A contains several workstreams that can proceed independently: outbound protocol/network ownership, P0 game-state reads, P1 bridge engineering, live causal/restart validation, and quantitative coverage/audit work. Serializing all of them through one investigator wastes independent research capacity.

At the same time, this programme has already produced plausible-looking hypotheses that were later disproven. Therefore parallel work without a promotion gate creates a real risk of stale or conflicting claims contaminating canonical knowledge.

The coordinator must be a **quality and integration gate, not a research bottleneck**. A well-supported draft may be accepted unchanged. The coordinator should spend independent verification effort in proportion to claim impact and uncertainty rather than redoing every experiment from scratch.

## Recommended lanes

Run up to five draft-only research lanes concurrently when repository/path ownership is non-overlapping:

| Lane | Primary responsibility | Promotion boundary |
|---|---|---|
| P2-NETWORK | final gameplay egress, writer ownership, serialization/framing/compression/encryption/sequence, connection state | Draft PR only |
| P0-STATE | player/world/UI-backed semantic reads and direct runtime storage | Draft PR only |
| P1-BRIDGE | stable read-only bridge/API, identity/readiness/health/recovery | Draft PR only |
| RUNTIME | login/session causal validation, negative controls, restart/relogin stability, safe action evidence | Draft PR only |
| COVERAGE-AUDIT | protocol/QMeta/P0 census, evidence gaps, conflict/supersession audit | Draft PR only |

The coordinator owns canonical promotion, cross-lane reconciliation, global coverage state, final task/handover state, and closeout.

A lane may be temporarily split further only when the coordinator can give each worker disjoint hypothesis and path ownership. Do not create multiple workers that merely duplicate the same queued experiment.

## Branch and write isolation

Every research worker must:

1. refetch current `main` before starting;
2. create a fresh isolated branch for its bounded research slice;
3. stay inside its assigned Track A path/experiment namespace;
4. persist raw or summarized evidence under the appropriate Track A evidence namespace;
5. mark researcher-authored conclusions as `DRAFT / NOT PROMOTED` until coordinator review;
6. open a **Draft PR** targeting `main`;
7. never merge, squash, rebase, force-push another worker's branch, or update `main` directly.

Researchers must not concurrently edit global canonical knowledge/task/handover files unless the coordinator explicitly assigns exclusive ownership for that exact slice. Prefer lane-local evidence files and artifacts.

The coordinator serializes canonical writes when multiple drafts affect the same knowledge, task, registry, or handover path.

## Evidence vocabulary

Every material claim must use one of these classifications:

- `FACT` — directly established by cited evidence under the applicable gate;
- `INFERENCE` — reasoned conclusion supported by facts but not directly proven;
- `ASSUMPTION` — working premise that still requires testing;
- `RECOMMENDATION` — proposed next step or design choice;
- `UNKNOWN` — unresolved question or missing evidence;
- `DISPROVEN` / `SUPERSEDED` — tested claim rejected or replaced by stronger evidence.

A green workflow is not by itself a `FACT` about Tibia semantics. Technical execution success and semantic proof must be evaluated separately.

## Exact-client fence

Unless the current canonical programme has intentionally advanced to another build, experiments in this campaign must verify the current official native Linux client identity before analysis or runtime promotion.

Current research fence at adoption time:

```text
canonical version mapping: 15.32.df7b29
size:                      51965216
SHA-256:                   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The version text is the repository's canonical mapping for the SHA/size pair; do not misstate it as an embedded exact-version-string proof unless independently demonstrated.

If the official client changes, the worker must record the mismatch and follow current programme update/recovery rules rather than silently applying old offsets to a new build.

## Researcher acceptance package

Every Draft PR must contain or reference enough information for a different agent to review without relying on chat history. At minimum the handover must state:

```yaml
STATUS: DRAFT_NOT_PROMOTED
LANE:
BRANCH:
HEAD:
BASE_MAIN:
CLIENT_IDENTITY:
OBJECTIVE:
HYPOTHESES_TESTED:
EXPERIMENTS_COMPLETED:
WORKFLOW_RUNS:
ARTIFACTS:
FACTS:
INFERENCES:
DISPROVEN_OR_SUPERSEDED:
UNKNOWN:
NEGATIVE_CONTROLS:
REPEATABILITY:
RESTART_OR_RELOGIN_TEST:
FILES_CHANGED:
VALIDATION:
SIDE_EFFECTS:
BLOCKERS:
NEXT_RECOMMENDED_EXPERIMENT:
```

For live experiments, preserve the causal recorder and side-effect requirements from the normative experiment execution model. Do not include secrets or unnecessary personal chat content in artifacts.

## Coordinator review contract

The coordinator must treat every researcher conclusion as untrusted until reviewed. For each Draft PR it must:

1. refetch current `main`, PR head, changed files, discussion and relevant artifacts;
2. verify Track A scope and detect any Track B contamination;
3. verify exact client identity/provenance for build-specific claims;
4. compare findings with current canonical facts plus `DISPROVEN/SUPERSEDED` history;
5. verify that the experiment tests the stated hypothesis rather than merely executing successfully;
6. require negative controls, repeatability, causal evidence and restart/relogin proof where the applicable gate requires them;
7. independently reproduce or cross-check high-impact claims when a false promotion would redirect downstream research;
8. resolve conflicts between lanes using evidence quality, not recency or confidence language;
9. classify the draft outcome;
10. update canonical coverage/task/knowledge/handover only after acceptance;
11. merge only a bounded, reviewable, validated slice.

### Review outcomes

- `ACCEPT` — evidence and implementation meet the gate; coordinator may promote and merge.
- `ACCEPT_WITH_EDITS` — underlying evidence is sound but wording, classification, scope, safety, or integration needs correction before merge.
- `RETURN_FOR_EVIDENCE` — hypothesis remains plausible but required proof is missing; keep Draft PR unmerged.
- `REJECT/SUPERSEDE` — evidence falsifies the claim, the work is stale/duplicated, or a stronger current result replaces it. Preserve useful negative evidence when appropriate.

The coordinator must not turn `RETURN_FOR_EVIDENCE` into a canonical fact and must not use branch age or CI color as a substitute for semantic review.

## Parallelism and dependency rules

Work may proceed concurrently when a lane can make progress without assuming an unresolved result from another lane.

Examples:

- P0 state discovery and P1 bridge architecture may proceed while P2 final egress remains unresolved.
- Runtime can validate already-discovered read candidates while static P2 work continues.
- Coverage/audit can continuously identify missing families but must not self-promote coverage closure.

When one lane depends on another lane's unmerged result, treat that result as `DRAFT` and pin the exact branch/head. Do not copy it into canonical facts before coordinator promotion.

## Anti-stall and duplication control

A queued or blocked workflow does not justify idle time when an independent bounded hypothesis can be tested. Workers should pursue distinct evidence paths allowed by the programme's anti-stall rules.

Before launching an expensive or overlapping experiment, inspect current workflow runs, active Draft PRs and lane handovers. The coordinator resolves duplicate ownership and cancels conceptual duplication by assigning a different hypothesis rather than having multiple workers rediscover the same evidence.

## Campaign success condition

This coordination model does not reduce Track A's completion criteria. Full success still requires all applicable P2, P1, P0, runtime/action, quantitative coverage, validation, canonical-state, handover and closeout gates to be satisfied.

No worker and no coordinator may claim `100%`, `COMPLETE`, or equivalent merely because all Draft PRs are green or merged. Completion is an evidence-gated programme state.
