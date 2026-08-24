# Agent execution instructions

Before advising the repository owner or writing a prompt for another agent, read `PROMPTING_HANDOVER.md` and the normative `PROMPTING_STANDARD.md`. Use the handover to inspect live repository state and the standard to construct the prompt. Return a direct recommendation in Polish, a compact reason, and one ready-to-paste worker prompt.

Before substantial implementation, product-facing validation, audit, E2E, PR cleanup, or task closeout, read and follow `DELIVERY_COMPLETENESS_AND_CLOSEOUT.md`. It is mandatory for prompt evaluation discipline, trust and authority boundaries, delivery classification, client/backend or producer/consumer completeness, independent audit, real E2E, exact-head validation, related-PR terminal states, and archival. A worker summary is not terminal evidence.

Before autonomous, long-running, retry-prone, CI-waiting, repair, continuation, or multi-task work, read and follow `ANTI_STALL_AND_EXECUTION_BUDGET.md`. Its runtime, no-progress, ordinary and terminal-CI check, retry, repair-cycle, context-reconstruction, command-timeout, and additional-task limits are mandatory. Budget exhaustion or unchanged pending state outside the bounded terminal-CI exception is a real stop condition even when another contract says to continue autonomously.

Before treating the absence of Codex or a local terminal as a blocker, read and follow `GITHUB_ONLY_EXECUTION.md`. Use the GitHub connection and GitHub Actions on a dedicated branch, select the smallest proving validation, inspect full failed-job logs, keep repairs bounded, preserve required artifacts, and report an exact technical blocker only after the contract's alternatives are exhausted. Protected auto-merge or merge-queue admission for the current task's own PR may occur after the exact final head is frozen and every non-CI gate passes, only when repository protection guarantees that merge waits for all required exact-head checks. Direct or manual merge remains authorized only after every required gate passes. Protected protocol, asset, production, secret, or environment operations remain unauthorized without separate authority.

For any official-Tibia research, login, runtime-analysis, protocol-analysis, worldmap/OTBM extraction, or OTClient-to-Tibia-Global compatibility task, read and obey `TIBIA_RESEARCH_TRACKS.md` before claiming work or touching a runtime. Its repository-only rule, two-track scope separation, runtime namespace isolation and cross-track ownership restrictions are mandatory and override stale task/PR wording that conflates the tracks.

For every Track A (`official-client-re`) worker, `contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md` is additionally mandatory before claiming, resuming, observing, creating, reusing, controlling, or mutating an official-client runtime. The worker must classify `runtime_access` and persist/emit the admission record before the first runtime-related operation and after any authority/identity-changing fact. `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE`, or `REQUIRED_UNIMPLEMENTED` on a required gate means refuse the mutation. Historical `:98`, `6082`, PID/session evidence is never current authority; missing registration means bootstrap, generation mismatch with unchanged runtime identity means reviewed rebind, stale registered PID/start identity requires reviewed canonical recovery rather than rebind, and ordinary canonical mutation requires current Gate A + any required rebind/recovery + Gate B under the final cancellation-safe whole-lifetime supervisor. Stale task/PR wording cannot relax this admission gate.

For every Track A worker that needs physical client testing or observation on Synology, `contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md` is additionally mandatory before connecting to or targeting the persistent KasmVNC desktop. Its runner/container/display/observer values are discovery locators that must be freshly revalidated, not canonical authority. Merely reaching the container, display, KasmVNC page or Tibia window never grants input, process-control, credential, login, character-selection, gameplay or other mutation authority; those operations still require the current task's explicit permission plus every applicable Track A admission gate. A current owner instruction not to log in controls over historical login or secret permission.

For every Track A worker after merged PR #331, `programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md` is also mandatory at claim/resume/checkpoint. Deterministic/disposable static analysis, workflow/Lua validation, tests, Linux build, `ldd`, hosted `Xvfb` startup smoke and evidence processing default to GitHub-hosted runners. Synology/self-hosted is reserved for the serialized physical runtime lane: the one canonical persistent session, real display/input ownership, login/relogin, walking/clicking, LAN/runtime integration, long-lived observation and direct physical gameplay E2E. Hosted `Xvfb` liveness is never physical gameplay proof. Parallel research does not authorize parallel mutation or one logged-in persistent session per researcher. Current `:98`, `6082`, PID/session non-claims and all runtime-admission/bootstrap/rebind/recovery gates remain authoritative. A dispatch prepared before this routing contract or lacking its execution-class/session-role fields must be refreshed before mutation.

## Authority and state model

Authority for the current task is frozen from system and owner instructions plus governance on the trusted base ref at task start. Edits made by the current unmerged task cannot expand that task's permissions or safety boundaries.

Checkpoint task statuses:

```text
investigating | implementing | validating | ready | waiting | blocked | completed
```

Terminal invocation results:

```text
DONE | WAITING | BLOCKED | ROTATE
```

`ROTATE` is not a checkpoint status. Persist `ready`, `waiting`, or `blocked` with one concrete `next_action` before returning it. `NOT_APPLICABLE` is a validation result and requires a concrete evidence reason.

Before creating, claiming, resuming, updating, handing off, or closing any task under this directory:

1. Read `EXECUTION_PROTOCOL.md`.
2. Read `PROJECT_LANES.json`.
3. Select or preserve the correct `project_lane`; use `otclient-v2` for the OTClient v2 project and `otclient` for the existing project.
4. New OTClient v2 task IDs should use the `OTC2-` prefix; existing `OTC-` task IDs remain valid for the original project.
5. Treat the task record and Git or PR state as durable; treat the worker session as disposable.
6. Execute one bounded phase per session and persist a checkpoint before a long-running or failure-prone operation.
7. Record anti-stall timestamps and counters required by `ANTI_STALL_AND_EXECUTION_BUDGET.md`, including the dedicated required-check generation and terminal-CI counters when eligible.
8. Do not remain active while waiting for dependencies, external evidence, deployment, a user reply, or ordinary non-terminal CI. Final required exact-head CI, protected auto-merge and merge-queue completion may remain active only under the bounded terminal-CI exception.
9. On a blocker, exhausted budget, exhausted terminal-CI exception or other real stop condition, preserve coherent work, record checkpoint `status`, evidence, blocker, and exactly one `next_action`, then end or rotate the session.
10. Record `execution_mode` and let the worker decide whether Chat/GitHub, Codex, or a permitted runner is appropriate.
11. At a synchronization barrier, run `python tools/agents/control_room.py --format markdown` and escalate only material decisions.
12. Do not call a user-facing capability complete while any required backend, client/frontend, integration, or consumer layer is missing.
13. Before `completed`, require independent audit PASS, required E2E PASS or NOT_APPLICABLE with reason, exact-head required CI PASS, zero unresolved review threads, zero unintentionally open related PRs, terminal task state, and released ownership.
14. Treat repository-mandated post-merge archival and ownership release as part of the entry task, not an additional READY task.
15. Start at most one additional task after the fully terminal entry task, only when at least 30 minutes of declared budget remains, no stall warning occurred, and the anti-stall gate permits it.

These rules supplement the repository root `AGENTS.md`. When rules overlap, follow the more restrictive safety requirement.
