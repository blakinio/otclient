# Repository-native Agent Orchestrator

Status: experimental orchestrator with a fail-closed real-worker adapter for `blakinio/otclient`.

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

The repository default still invokes **no AI/model service**. `docs/agents/AGENT_ORCHESTRATOR.json` keeps `mode: dry_run` and `real_model_executor_enabled: false`. The repository now also contains `tools/agents/orchestrator_executor.py`, a provider-neutral external-process adapter that can execute a trusted fixed argv worker in an isolated detached worktree when a separately authorized provider configuration enables it. Deterministic fixtures prove the executor plumbing without consuming model quota.

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

Default policy:

- `low` -> dispatch is allowed when every other gate passes;
- `medium` + stable/falling growth -> dispatch is allowed;
- `medium` + rising/rapid growth -> checkpoint and rotate the same task before dispatch;
- `high` or `unbounded` -> checkpoint and rotate the same task before dispatch;
- missing context classification -> hold rather than guess;
- if an enabled executor provides a **verified** remaining-context ratio, `<= 0.20` also triggers rotation. This signal is optional and is never fabricated.

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

The result contains the score, pressure band, `dispatch|rotate|hold` action and reasons. It also emits `exact_remaining_tokens_known: false`; provider-specific remaining-context data is carried only in worker results when it is independently verified.

### Why this reduces coordinator context pressure

The coordinator does not ingest worker transcripts. A selected worker receives a compact continuation entry point:

```text
python tools/agents/resume.py --task <task-path>
```

The real-worker adapter renders that durable bundle into the worker request. The worker returns only a standardized result containing task/branch/base/head identity, changed paths, validation/evidence references, context state, status and one next action while incomplete. Large logs remain workflow/repository artifacts.

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

## External real-worker execution

`tools/agents/orchestrator_executor.py` is the provider-neutral adapter. The CLI entry point is:

```bash
python tools/agents/orchestrator.py \
  --config <authorized-executor-config.json> \
  execute \
  --plan /tmp/agent-wave.json \
  --results-dir /tmp/worker-results \
  --output /tmp/executor-summary.json
```

Enablement is fail-closed. The executor requires all of:

- `mode: external_process`;
- `real_model_executor_enabled: true`;
- a concrete `provider` identifier;
- a fixed non-empty `command` argv list owned by trusted configuration, never task prose;
- `owner_funded_ai_allowed: true` when that provider is classified `requires_owner_funded_ai: true`;
- a finite timeout and bounded worker count.

The worker receives one JSON request on stdin containing the compact `resume.py` prompt, exact task/branch/base identity, owned paths, isolated workspace and `worker-result-v1` contract. The subprocess runs with `shell=False` and an allowlisted environment. `HOME` is deliberately absent from the built-in environment because credential/config material commonly lives below it; a provider may receive `HOME` or another credential-bearing variable only when the authorized provider configuration names it explicitly in `pass_env`.

For each selected task the adapter:

1. rediscovers the current task inventory and recomputes the selected wave so dependency, context, branch/head and ownership changes invalidate a stale plan before worker launch;
2. verifies current task/dispatch branch and exact base SHA, rejecting `main`/`master` and invalid branch names;
3. creates a unique detached Git worktree at that exact base;
4. launches one external worker process with a finite timeout;
5. requires structured `worker-result-v1` JSON on stdout;
6. rejects non-zero exit, malformed JSON or dirty/uncommitted worktree state;
7. verifies the actual worktree `HEAD` descends from the dispatch base and equals returned `head_sha`;
8. derives changed paths from `git diff <base>...HEAD` and requires an exact match with the worker result;
9. applies the existing task/branch/base/path/evidence/context result validation;
10. for a worker with any changed path, requires `publish_results: true` and publishes the result commit to the task branch using a normal non-force push only when the remote branch is absent or still equals the dispatch base;
11. verifies the published branch points at the accepted worker head, then removes the isolated worktree.

A failed worker produces no accepted result file. A writer whose commit is not durably published also fails closed; `publish_results: false` is valid only for a no-change/read-only worker. The barrier therefore cannot promote a failed, mismatched or unreachable writer result as `DONE`.

The repository default configuration intentionally keeps this path disabled. A task command such as `next_action` is never converted into executable shell syntax.

A detached Git worktree is an isolation mechanism for worker files, **not a hostile-worker sandbox**: worktrees share repository Git metadata. Before any concrete AI/model runtime is activated, its trusted wrapper/execution environment must separately bound repository-global Git ref/config mutation, credential access, network/process authority and any other provider-specific capability. The generic adapter does not grant that authority merely because it can launch a process.

## Barrier and iterative replanning

Given a wave plan and a directory of accepted worker result JSON files:

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

`.github/workflows/agent-orchestrator-smoke.yml` proves the control-plane mechanics without an AI service. Its focused suite includes deterministic real-executor integration tests that create temporary Git repositories/worktrees and launch `fake_real_worker.py` as a genuine external process. The fixture proves a successful committed writer is durably published to its task branch and accepted, while malformed JSON, non-zero exit, timeout, dirty worktree, head mismatch, stale plan, protected branch, ownership escape, missing durable publication and a moved remote task branch all fail closed. It also proves unlisted environment data, including `HOME`, is absent unless explicitly allowlisted.

The existing fan-out/fan-in fixture also proves:

```text
plan fixture wave [A, B]
    -> GitHub Actions matrix runs A and B in parallel
    -> each emits worker-result-v1 JSON
    -> barrier validates both
    -> dependencies A+B become DONE in the barrier overlay
    -> second wave contains dependent task C
    -> high-context task D remains held for rotation
```

This is real GitHub-hosted process/worktree and orchestration E2E. It is **not** evidence that an AI/model provider was invoked.

## Provider activation boundary

The adapter is implemented, but a concrete model/provider configuration remains a separate activation decision. Before a provider is enabled, repository policy still requires:

- exact authorization for any owner-funded AI/model/credential use;
- a trusted worker wrapper that accepts the JSON request and emits `worker-result-v1`;
- explicit `pass_env` entries only for the provider environment variables actually authorized;
- one independently isolated worker process per selected task;
- a provider-specific sandbox/capability boundary appropriate to repository-global Git metadata, credentials, network and process access;
- repository-specific runtime/protected-resource admission gates;
- fresh live ownership and dependency checks;
- fresh validator roles where required by the task;
- provider-specific context/retry limits that do not weaken the repository anti-stall budget.

The coordinator may then loop `plan -> execute -> barrier -> plan` until a real stop condition or programme budget is reached.

## Safe rollout for this repository

Use staged proof rather than turning on autonomous model writers immediately:

1. **MVP smoke** — deterministic fixture fan-out/fan-in; no AI.
2. **Live repo plan-only** — run `plan` against active task records; no workers.
3. **External-process fixture** — real detached worktree/process/commit/result validation with deterministic fake workers; no AI.
4. **Read-only provider workers** — after a concrete provider is authorized and configured, use validator/research tasks with no write ownership.
5. **Two disjoint provider writers** — only after read-only evidence is clean; unique branches/worktrees and non-overlapping paths.
6. **Adaptive waves** — enable barrier-driven second/third waves after result contract and context rotation have proved reliable.
7. **Cross-repository port** — copy the small tool/config/workflow surface, then replace repository-specific task-ID patterns, lane rules and governance references rather than copying live OTClient task state.

Do not move to the next stage by weakening a failed gate.

## Porting checklist

For another repository:

- preserve a durable task/checkpoint format with task ID, status, branch, exact head, ownership, dependencies and one next action;
- define repository-specific task-ID patterns if they differ;
- provide a compact resume/handoff generator;
- set path-ownership semantics and maximum worker count;
- map the local context-pressure policy and rotate threshold;
- keep provider credentials and funding authority outside task data;
- create repository-specific workflow fixtures proving dependency, overlap, context, external-process execution and fan-out/fan-in behavior;
- run plan-only against the real task inventory before enabling provider workers;
- keep one coordinator responsible for integration and terminal acceptance.

## Current non-goals

The orchestrator does not:

- estimate exact ChatGPT/model tokens remaining;
- select or authorize a model/provider by itself;
- treat credential availability as permission to consume owner-funded AI quota;
- execute shell commands sourced from task prose;
- provide a hostile-model sandbox merely by using Git worktrees;
- bypass task ownership, runtime admission, audit, E2E, exact-head CI or merge gates;
- claim deterministic fixtures are AI agents;
- make `ACTIVE_WORK.md` a shared lock;
- create one canonical-runtime session per parallel worker.
