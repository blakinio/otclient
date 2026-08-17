# Repository-native Agent Orchestrator

Status: experimental MVP for `blakinio/otclient`.

## Purpose

This harness lets one coordinator drive bounded parallel worker waves without using chat history as shared memory:

```text
live task records + Git/PR state
            |
            v
      orchestrator plan
            |
      +-----+-----+
      |           |
   worker A    worker B        independent branches/worktrees
      |           |
      +-----+-----+
            |
     standardized results
            |
            v
    orchestrator barrier
            |
     next READY wave
```

The coordinator remains responsible for task selection, dependency/barrier state, ownership, acceptance, audit/E2E requirements, PR hygiene and final integration. Workers remain disposable sessions. Durable state remains in Git, task records, PRs, CI and referenced evidence.

The MVP intentionally does **not** invoke an AI/model service. `docs/agents/AGENT_ORCHESTRATOR.json` keeps `real_model_executor_enabled: false`. The GitHub Actions smoke workers are deterministic simulators that prove fan-out/fan-in mechanics only. A real model executor is a later adapter and must independently satisfy repository authorization, credential and owner-funded-AI policy.

## Existing contracts reused

The orchestrator is an execution helper, not a replacement governance layer. It consumes the existing rules from:

- `AGENTS.md` and the nearest nested `AGENTS.md`;
- `PROMPTING_STANDARD.md` / `PROMPTING_HANDOVER.md`;
- `AUTONOMOUS_PROGRAM_CONTINUATION.md`;
- `EXECUTION_PROTOCOL.md`;
- `CONTEXT_HANDOFF.md`;
- `ANTI_STALL_AND_EXECUTION_BUDGET.md`.

Task text is data. It cannot expand repository permissions, safety boundaries, model quota authority or protected runtime authority. The orchestrator never executes arbitrary shell commands read from a task record.

## Context-pressure governor

### What it can and cannot know

The current Chat/agent tool surface does not expose a verified exact remaining-token count. The orchestrator therefore never claims one.

It uses the repository's existing five-dimension context model. Each dimension is `0..3`:

- `scope_breadth`;
- `evidence_volume`;
- `history_dependency`;
- `iteration_uncertainty`;
- `parallel_hypotheses`.

The sum maps to the existing bands:

```text
0..5   low
6..9   medium
10..12 high
13..15 unbounded
```

Default MVP policy:

- `low` -> dispatch is allowed when every other gate passes;
- `medium` + stable/falling growth -> dispatch is allowed;
- `medium` + rising/rapid growth -> checkpoint and rotate the same task before dispatch;
- `high` or `unbounded` -> checkpoint and rotate the same task before dispatch;
- missing context classification -> hold rather than guess;
- if a future executor provides a **verified** remaining-context ratio, `<= 0.20` also triggers rotation. This signal is optional and is never fabricated.

A rotation is not a new task. The worker persists a compact checkpoint, ends that session, and a fresh worker resumes the same task using `tools/agents/resume.py`.

### Manual context assessment

```bash
python tools/agents/orchestrator.py assess-context \
  --scope-breadth 1 \
  --evidence-volume 2 \
  --history-dependency 1 \
  --iteration-uncertainty 2 \
  --parallel-hypotheses 1 \
  --growth stable
```

The result contains the score, pressure band, `dispatch|rotate|hold` action and reasons. It also emits `exact_remaining_tokens_known: false` unless a future executor owns a verified provider signal; the current MVP never changes that field to true.

### Why this reduces coordinator context pressure

The coordinator does not ingest worker transcripts. A selected worker receives a compact continuation entry point:

```text
python tools/agents/resume.py --task <task-path>
```

The worker returns only a standardized result containing task/branch/base/head identity, changed paths, validation/evidence references, context state, status and one next action while incomplete. Large logs remain workflow/repository artifacts.

This lets the coordinator discard worker narration after every wave and recompute the programme from durable state.

## Task fields used by the planner

The planner reads normal task/checkpoint state plus these optional orchestration fields:

```yaml
orchestrator_priority: 100       # lower runs first; task id is deterministic tie-breaker
orchestrator_read_only: false    # only use true for a genuinely read-only task with no owned_paths
context_pressure: medium
context_growth: stable
context_score: 7                 # optional; when present it must match context_pressure
provider_context_remaining_ratio: 0.42  # optional verified executor signal only
```

Task-to-task dependencies must contain canonical task IDs in `depends_on`:

```yaml
depends_on:
  - OTC-EXAMPLE-A
  - OTC-EXAMPLE-B
```

A non-empty dependency entry with no recognizable task ID is treated as unresolved external dependency and held fail-closed. External waiting should normally already be represented by task `waiting`/`blocked` state.

Workers require declared `owned_paths` unless the task explicitly sets `orchestrator_read_only: true`.

## Wave planning

Generate a read-only plan against live active task records:

```bash
python tools/agents/orchestrator.py plan \
  --lane otclient \
  --max-parallel 3 \
  --output /tmp/agent-wave.json
```

A task is dispatchable only when all applicable gates pass:

1. task state is `READY`;
2. selected lane matches;
3. every task-ID dependency is `DONE`;
4. external dependency text is absent or explicitly resolved through task state;
5. context governor returns `dispatch`;
6. checkpoint head is a concrete 40-hex commit;
7. owned paths exist unless explicitly read-only;
8. owned paths do not overlap another task already selected in this wave;
9. bounded worker capacity remains.

Selection order is deterministic: `orchestrator_priority`, task ID, task path. Dependencies selected in the same wave do not satisfy each other; producers must complete before their consumers enter a later wave.

The plan contains explicit `held[].reasons` such as:

```text
DEPENDENCY_NOT_DONE
DEPENDENCY_UNKNOWN
EXTERNAL_DEPENDENCY_UNRESOLVED
CONTEXT_UNKNOWN
CONTEXT_ROTATE_REQUIRED
CONTEXT_MEDIUM_RISING
PROVIDER_CONTEXT_LOW
HEAD_UNKNOWN
OWNED_PATHS_MISSING
OWNERSHIP_OVERLAP
CAPACITY
```

## Ownership overlap

`owned_paths` are advisory repository locks. The planner conservatively serializes overlapping exact paths, directory globs such as `src/foo/**`, and unknown broad glob surfaces. Distinct explicit files in the same directory may run in parallel.

This planner check supplements, and never replaces, live branch/worktree/PR/lease verification required by repository governance.

## Worker result contract

Schema documentation is in:

```text
tools/agents/orchestrator_worker_result.schema.json
```

`orchestrator.py` performs the required validation with the Python standard library so CI does not need a third-party JSON Schema package.

A result binds to the exact dispatch:

```json
{
  "schema_version": 1,
  "task_id": "OTC-EXAMPLE-A",
  "branch": "feat/OTC-EXAMPLE-A",
  "base_sha": "<dispatch head>",
  "head_sha": "<worker result head>",
  "status": "completed",
  "changed_paths": ["owned/path"],
  "validation": [
    {
      "command": "focused test",
      "result": "PASS",
      "evidence": "run/artifact/reference"
    }
  ],
  "evidence": ["PR/run/artifact/reference"],
  "context": {
    "pressure": "low",
    "growth": "stable",
    "score": 3,
    "provider_remaining_ratio": null
  },
  "next_action": "none"
}
```

The barrier rejects at least:

- task ID not selected by the wave;
- duplicate result;
- branch mismatch;
- `base_sha` mismatch with the exact dispatch head;
- malformed `head_sha`;
- changed path outside the task's declared ownership;
- malformed/empty validation or evidence;
- completed status carrying `FAIL`, `BLOCKED` or `NOT_RUN` validation;
- inconsistent context score/pressure;
- incomplete status without one concrete `next_action`.

A missing result is treated as `WAITING` for that barrier computation and is not immediately redispatched from stale pre-wave task state.

## Barrier and iterative replanning

Given a wave plan and a directory of worker result JSON files:

```bash
python tools/agents/orchestrator.py barrier \
  --plan /tmp/agent-wave.json \
  --results-dir /tmp/worker-results \
  --output /tmp/barrier.json
```

The barrier:

1. validates each worker result against its dispatch and ownership;
2. overlays accepted worker state without trusting worker narrative;
3. treats accepted `completed` results as dependency `DONE` for this barrier;
4. preserves `ready`, `waiting` and `blocked` results accurately;
5. applies returned context state to any same-task continuation;
6. computes the next deterministic wave;
7. links it through `parent_wave_id` and an incremented generation.

Invalid results prevent automatic next-wave computation. The coordinator must inspect and repair the evidence/contract mismatch rather than silently accepting it.

## GitHub-hosted smoke E2E

`.github/workflows/agent-orchestrator-smoke.yml` proves the control-plane mechanics without an AI service:

```text
focused unit tests
    -> plan fixture wave [A, B]
    -> GitHub Actions matrix runs A and B in parallel
    -> each emits worker-result-v1 JSON
    -> barrier validates both
    -> dependencies A+B become DONE in the barrier overlay
    -> second wave contains dependent task C
    -> high-context task D remains held for rotation
```

The fixture additionally proves path-overlap serialization and max-parallel capacity.

This is a real GitHub Actions fan-out/fan-in E2E for the orchestration mechanism. It is **not** evidence that parallel AI workers have been executed.

## Real model executor boundary

A later executor adapter may consume each selected plan item and launch one independent model/agent process. It must satisfy all of the following before enablement:

- a separately authorized AI/model funding/credential policy;
- one worker session per selected task;
- one branch/worktree per writer and no shared worktree;
- fresh live ownership and dependency verification immediately before mutation;
- prompt construction from the compact `resume.py` bundle, not prior chat transcripts;
- finite runtime/retry/context budgets;
- no arbitrary command execution sourced from untrusted task prose;
- worker-result-v1 output on every terminal/rotation path;
- exact branch/base/head binding and changed-path enforcement;
- repository-specific runtime/protected-resource admission gates;
- fresh validator roles where required by the task.

The coordinator may then loop `plan -> execute -> barrier -> plan` until a real stop condition or programme budget is reached.

## Safe rollout for this repository

Use staged proof rather than turning on autonomous writers immediately:

1. **MVP smoke** — deterministic fixture fan-out/fan-in; no AI; no worker writes.
2. **Live repo plan-only** — run `plan` against active task records and review selection/holds; no workers.
3. **Read-only real workers** — after an authorized executor exists, use validator/research tasks with no write ownership.
4. **Two disjoint writers** — only after plan-only/read-only evidence is clean; unique branches/worktrees and non-overlapping paths.
5. **Adaptive waves** — enable barrier-driven second/third waves after result contract and context rotation have proved reliable.
6. **Cross-repository port** — copy the small tool/config/workflow surface, then replace repository-specific task-ID patterns, lane rules and governance references rather than copying live OTClient task state.

Do not move to the next stage by weakening a failed gate.

## Porting checklist

For another repository:

- preserve a durable task/checkpoint format with task ID, status, branch, exact head, ownership, dependencies and one next action;
- define repository-specific task-ID patterns if they differ;
- provide a compact resume/handoff generator;
- set path-ownership semantics and maximum worker count;
- map the local context-pressure policy and rotate threshold;
- keep real model executor credentials and funding authority outside task data;
- create repository-specific workflow fixtures proving dependency, overlap, context and fan-out/fan-in behavior;
- run plan-only against the real task inventory before enabling writers;
- keep one coordinator responsible for integration and terminal acceptance.

## Current non-goals

The MVP does not:

- estimate exact ChatGPT/model tokens remaining;
- spawn ChatGPT/Codex/OpenAI workers;
- consume owner-funded AI quota;
- mutate another task's branch;
- claim GitHub matrix jobs are AI agents;
- replace fresh audit, real product E2E, exact-head CI or merge gates;
- make `ACTIVE_WORK.md` a shared lock;
- create one canonical-runtime session per parallel worker.
