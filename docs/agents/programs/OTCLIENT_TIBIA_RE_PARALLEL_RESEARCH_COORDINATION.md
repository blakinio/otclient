# OTCLIENT-TIBIA-RE parallel research coordination

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
status: operational_coordination_addendum
promotion_authority: coordinator_only
research_worker_output: draft_only
prompt_contract_version: 1.0.1
prompt_eval: docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_AGENT_PROMPT_EVAL.md
```

## Authority and scope

This document defines how remaining Track A research may be executed in parallel. It is subordinate to, and must not weaken, current repository governance, especially:

- `AGENTS.md` and `docs/agents/AGENTS.md`;
- `docs/agents/PROMPTING_STANDARD.md` and `docs/agents/PROMPT_EVAL_STANDARD.md`;
- `docs/agents/PROMPTING_HANDOVER.md`;
- `docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md`;
- `docs/agents/EXECUTION_PROTOCOL.md` and `docs/agents/PROJECT_LANES.json`;
- `docs/agents/TRUST_AND_CONTEXT_BOUNDARIES.md`;
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`;
- the current canonical `OTCLIENT-TIBIA-RE` programme, knowledge, task, evidence and closeout rules.

Track B (`blakinio/otclient -> Tibia Global compatibility`) is outside this coordination model and must not be modified by Track A workers.

## Decision

### RECOMMENDATION — adopted operating model

Use parallel **draft-only research workers** with one **promotion/integration coordinator**.

Researchers remain autonomous investigators. Within assigned authority they may inspect the repository, design bounded hypotheses, implement probes/workflows/tools, run experiments, consume artifacts, falsify hypotheses and persist durable evidence. The restriction is on **promotion**, not investigation.

A research worker's repository delivery stops at a **Draft PR**. It must not merge its own work and must not promote its conclusions into canonical programme knowledge as established fact.

The coordinator is the campaign promotion/integration authority, subject to higher repository/owner authority. It reviews each Draft PR and raw evidence, independently checks high-impact claims, corrects classifications where necessary, resolves conflicts, and integrates only accepted, current, bounded slices.

```text
research observation / experiment
        -> worker draft evidence
        -> Draft PR
        -> coordinator review
        -> ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE
        -> canonical promotion / integration / merge
```

## Why this fits Track A

Track A contains workstreams that can progress independently: outbound protocol/network ownership, P0 game-state reads, P1 bridge engineering, live causal/restart validation, and quantitative coverage/audit work. Serializing all investigation through one worker wastes independent research capacity.

The programme has also produced plausible hypotheses that were later disproven. Parallel investigation without a promotion gate therefore risks contaminating canonical knowledge with stale or conflicting claims.

The coordinator must be a **quality and integration gate, not a research bottleneck**. A well-supported, low-risk draft may be accepted unchanged after proportionate verification. Independent reproduction effort should scale with claim impact, ambiguity and downstream blast radius rather than be repeated mechanically for every observation.

## Recommended lanes

Run up to five draft-only research lanes concurrently only when live task/path ownership is non-overlapping:

| Lane | Primary responsibility | Promotion boundary |
|---|---|---|
| P2-NETWORK | final gameplay egress, writer ownership, serialization/framing/compression/encryption/sequence, connection state | Draft PR only |
| P0-STATE | player/world/UI-backed semantic reads and direct runtime storage | Draft PR only |
| P1-BRIDGE | stable read-only bridge/API, identity/readiness/health/recovery | Draft PR only |
| RUNTIME | login/session causal validation, negative controls, restart/relogin stability, safe action evidence | Draft PR only |
| COVERAGE-AUDIT | protocol/QMeta/P0 census, evidence gaps, conflict/supersession audit | Draft PR only |

The coordinator owns canonical promotion, cross-lane reconciliation, global coverage state, final programme/task/handover state and closeout.

A lane may be split further only when the coordinator can assign disjoint task and path ownership. Do not create workers that merely duplicate the same queued experiment.

## Mandatory dispatch preflight

**Lane names are not locks.** Before any researcher may mutate repository state, the coordinator/dispatcher must resolve and provide all of the following from live repository state:

```yaml
TASK_ID: <required concrete task id>
TASK_RECORD: docs/agents/tasks/active/<required concrete task file>
PROJECT_LANE: otclient
LANE: <P2-NETWORK|P0-STATE|P1-BRIDGE|RUNTIME|COVERAGE-AUDIT>
BASE_MAIN: <exact current main SHA at dispatch>
BRANCH: <unique branch for this task>
WORKTREE: <dedicated worktree or equivalent isolated checkout identifier>
OWNED_PATHS:
  - <exact writable path/glob claim 1>
  - <exact writable path/glob claim 2>
DEPENDENCIES:
  - <task/PR/head or none>
```

Dispatch is **read-only** until every required field is concrete and live-state checks confirm:

1. the task record exists and matches the assigned lane/branch;
2. `owned_paths` are declared in the task record;
3. no active task/PR has an unresolved ownership overlap for those writable paths;
4. branch and worktree are unique to that worker and not shared;
5. current `main`, open PRs and active task records were refreshed after any prior assignment change.

If an experiment later needs a path outside `OWNED_PATHS`, the worker must not silently edit it. Persist the need and obtain/resolve ownership through the coordinator or current repository protocol first.

## Branch and write isolation

Every research worker must:

1. start from the resolved current `main`/base state;
2. use only its assigned unique branch and worktree;
3. remain within the assigned Track A writable paths and experiment namespace;
4. persist evidence under the assigned Track A evidence namespace;
5. mark researcher-authored conclusions `DRAFT / NOT PROMOTED` until coordinator review;
6. open a **Draft PR** targeting `main` early enough for discoverability;
7. never merge, squash, rebase, force-push another worker's branch, update `main`, or share a worktree.

Researchers must not concurrently edit global canonical knowledge/task/handover/coverage files unless the coordinator explicitly assigns exclusive ownership for that exact path. Prefer lane-local evidence and artifacts. The coordinator serializes canonical writes when drafts converge on shared state.

## Evidence vocabulary

Every material claim uses one of:

- `FACT` — directly established by cited evidence under the applicable gate;
- `INFERENCE` — reasoned conclusion supported by facts but not directly proven;
- `ASSUMPTION` — working premise requiring test;
- `RECOMMENDATION` — proposed next step or design choice;
- `UNKNOWN` — unresolved question or missing evidence;
- `DISPROVEN` / `SUPERSEDED` — tested claim rejected or replaced by stronger evidence.

A green workflow is not by itself a `FACT` about Tibia semantics. Technical execution success and semantic proof are separate outcomes.

## Exact-client fence

Unless the current canonical programme intentionally advances to another build, build-specific experiments must verify current official native Linux client identity before analysis/runtime promotion.

Current research fence at adoption time:

```text
canonical version mapping: 15.32
size:                      52109920
SHA-256:                   ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

The version text is the repository's canonical mapping for the SHA/size pair; do not call it an embedded exact-version-string proof unless independently demonstrated.

If the official client changes, record the mismatch and follow current update/recovery rules instead of applying old offsets to a new build.

## Execution budget and real stops

Parallelism does **not** relax `ANTI_STALL_AND_EXECUTION_BUDGET.md`. Its runtime, no-progress, ordinary/terminal-CI check, retry, repair-cycle, context reconstruction, command-timeout and additional-task limits remain mandatory.

Budget exhaustion, an exhausted bounded terminal-CI exception, unsafe context/tool limits, unresolved ownership, required authority/safety decision, or an unchanged pending state outside the allowed terminal-CI exception are real stop/rotation conditions even when the lane objective is unfinished.

When a worker hits a real stop:

1. preserve coherent work;
2. checkpoint the task as `ready`, `waiting`, or `blocked` as appropriate;
3. record required anti-stall counters/timestamps and evidence;
4. record exactly one `next_action`;
5. leave a Draft PR/handover if a reviewable slice exists;
6. return/rotate rather than polling indefinitely.

If another independent bounded hypothesis is READY and within the same authorized task/budget, the worker may pursue it. A queue alone is not permission to dispatch a conceptual duplicate.

## Researcher acceptance package

Every Draft PR must contain/reference enough information for another agent to review without chat history:

```yaml
STATUS: DRAFT_NOT_PROMOTED | WAITING | BLOCKED | ROTATE
TASK_ID:
TASK_RECORD:
LANE:
BRANCH:
WORKTREE:
HEAD:
BASE_MAIN:
OWNED_PATHS:
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
EXECUTION_BUDGET_STATE:
BLOCKERS:
NEXT_RECOMMENDED_EXPERIMENT:
DRAFT_PR:
```

For live experiments preserve causal-recorder, privacy and side-effect requirements from the normative experiment model. Never persist secrets or unnecessary personal chat content.

## Coordinator review contract

Treat every researcher conclusion as untrusted until reviewed. For each Draft PR the coordinator must:

1. refetch current `main`, exact PR head, task record, owned paths, changed files, discussion, checks and relevant artifacts;
2. verify Track A scope and detect Track B contamination;
3. verify task/branch/worktree/path isolation and resolve overlaps;
4. verify exact client identity/provenance for build-specific claims;
5. compare findings with current canonical facts and `DISPROVEN/SUPERSEDED` history;
6. verify that the experiment discriminates the stated hypothesis rather than merely executes successfully;
7. require negative controls, repeatability, causal evidence and restart/relogin proof where the gate requires them;
8. independently reproduce/cross-check high-impact claims whose false promotion would redirect downstream research;
9. resolve conflicts by evidence quality, not recency or confidence language;
10. classify the draft outcome;
11. update canonical coverage/task/knowledge/handover only after acceptance;
12. integrate and merge only a bounded, reviewable, validated slice under repository closeout rules.

### Review outcomes

- `ACCEPT` — evidence/implementation meet the gate; coordinator may promote and integrate.
- `ACCEPT_WITH_EDITS` — underlying evidence is sound but wording, classification, scope, safety or integration requires correction.
- `RETURN_FOR_EVIDENCE` — hypothesis remains plausible but required proof is missing; keep Draft PR unmerged.
- `REJECT/SUPERSEDE` — evidence falsifies the claim, work is stale/duplicated, or stronger current evidence replaces it; preserve useful negative evidence.

`RETURN_FOR_EVIDENCE` never becomes a canonical fact. CI colour, PR age or worker confidence are never semantic evidence substitutes.

## Parallelism and dependencies

Work may proceed concurrently when a lane can progress without assuming an unresolved result from another lane.

Examples:

- P0 discovery and P1 bridge architecture may proceed while P2 final egress is unresolved.
- Runtime may validate already-discovered read candidates while static P2 work continues.
- Coverage/audit may identify missing families continuously but cannot self-promote closure.

When a lane depends on another unmerged result, pin exact task/branch/head and classify it `DRAFT`. Do not copy it into canonical facts before coordinator promotion.

## Anti-duplication

Before an expensive/overlapping experiment, inspect active task records, open Draft PRs, workflow runs and lane handovers. The coordinator resolves duplicate ownership by assigning a distinct hypothesis or path rather than allowing multiple workers to rediscover the same evidence.

## Prompt-as-code gate

The parallel prompt layer is behavioural code. Its current contract is version `1.0.0` and its documented baseline/candidate/rollback evaluation is:

`docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_AGENT_PROMPT_EVAL.md`

Material changes to researcher/coordinator authority, routing, stop conditions, examples, tools or acceptance must increment/update that contract and rerun the same representative baseline/candidate evaluation under `PROMPT_EVAL_STANDARD.md`. Do not add coordination rules merely because they sound prudent.

## Campaign success condition

This model does not reduce Track A completion criteria. Full success still requires all applicable P2, P1, P0, runtime/action, quantitative coverage, validation, canonical-state, handover and closeout gates.

No worker and no coordinator may claim `100%`, `COMPLETE`, or equivalent merely because Draft PRs are green or merged. Completion remains an evidence-gated programme state.

## 2026-08-19 current-client fence provenance boundary

The current public native-Linux package is fenced by size `52109920` and SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`; `15.32` is an embedded version-family token, not a claim of a more specific suffix. The superseded `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` binary remains admissible only as explicitly historical build-fenced evidence. Historical addresses, offsets, QMeta/vptr assumptions, serializers, helper binaries and runtime-bridge profiles are **not** promoted to the current binary by this identity update.

This fence change grants no login, credential, GUI input, gameplay, process-control, transaction or mutation authority. All ordinary ownership/admission/lease/Gate A/rebind/Gate B/bootstrap requirements remain unchanged.
