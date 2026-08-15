# Track A RUNTIME runner-selector recovery

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Track: `official-client-re`
Base main: `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Problem classification

### FACT — stale run before repair

RUNTIME run `31883846172` / job `95010096196` was created from execution head `950ce8f5f7cf22b457e82cdb20e9eec285438d9c` with requested labels:

```text
[self-hosted, otclient, synology]
```

The job remained queued with zero steps and `runner_id=0`.

### FACT — independent runner reachability proof

During the same external-state interval, independently owned P0 run `31883967070` / job `95010405800` requested:

```text
[otclient, synology]
```

and was assigned to runner id `21`, `synology-otclient-01`, where it completed `SUCCESS`. Earlier P0 job `95008500800` had also executed on that same runner with the two-label selector.

Therefore the RUNTIME queue was not correctly attributable to an unavailable runner.

## Repair

Workflow commit `4f5314cfefa4dfeb150f4e5d912ef4180c4efc67` changed only scheduling/recovery mechanics around the existing runtime hypothesis:

- `runs-on` changed from `[self-hosted, otclient, synology]` to the proven `[otclient, synology]`;
- the exact old run is fenced by id `31883846172`, head `950ce8f5f7cf22b457e82cdb20e9eec285438d9c`, workflow name, branch and path before cancellation is allowed;
- the GitHub-hosted preflight is outside `official-client-re-runtime` so the stale top-level concurrency holder can be retired;
- the actual `reacquire` job alone owns `official-client-re-runtime` and starts only after the preflight permits it;
- if the old run were already executing, the preflight would suppress the new runtime job rather than cancel a live semantic experiment;
- exact helper blob, run-request, repository/branch/runner-name, client SHA/size, credential-environment and cleanup gates remain unchanged.

No login, movement, game action or process-memory effect occurs in the preflight.

## Result — FACT

The preflight job `95010928093` in new run `31884181155` completed `SUCCESS` and retired only the exact stale run. Old run `31883846172` became terminal `cancelled`.

New `reacquire` job `95010941902` requested `[otclient, synology]` and was immediately assigned to:

```text
runner_id: 21
runner_name: synology-otclient-01
runner_group: Default
```

This closes the scheduling/selector blocker.

## Remaining semantic gate

At this checkpoint `reacquire` is executing its runner setup. No generation-1/2 semantic result is classified yet. The next accepted evidence must come from the existing run `31884181155`; no conceptual duplicate should be dispatched while it is active.

### UNKNOWN pending run

- protected login-secret availability/acceptance;
- exact generation-1 `IN_GAME` structural records;
- clean generation-1 stop;
- fresh generation-2 PID/PIE;
- generation-2 structural reacquisition;
- task-local SOCKS confinement / forbidden direct-transport result;
- persistent child credential-environment assertions;
- final cleanup result.
