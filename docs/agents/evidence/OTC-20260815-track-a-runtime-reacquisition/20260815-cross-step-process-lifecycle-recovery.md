# Track A RUNTIME cross-step process lifecycle recovery

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Base main: `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Evidence from run #8

Execution head: `972936ffef081318b6103a6c799feeb3ce36fc92`
Run: `31884531727`
Job: `95011797563`
Runner: `synology-otclient-01`, id `21`
Conclusion: `FAILURE`
Artifact id: `9246917300`
Artifact ZIP SHA-256: `420ef5f216ee12db9a63c7c0f3fd13da7a9195622cae8b3e3885a904b055ad25`

### FACT — bootstrap succeeded

The runner-layout compatibility helper was materialized successfully, then bootstrap proved all prerequisites below:

```text
TRACK_A_RUNTIME_SOURCE_STATE=/work/_otclient_tibia_re_state
TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=16739 source_state=/work/_otclient_tibia_re_state
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=socks-relay pid=21755
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415 pid=21755
TRACK_A_CREDENTIAL_ENV_CLEAR role=xvfb pid=21792
TRACK_A_TASK_XVFB_VERIFIED=true display=:115 pid=21792
TRACK_A_RUNTIME_NAMESPACE_READY=true root=/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition/runs/31884531727 display=:115 socks=25415
```

No credentials were printed. No login or gameplay action occurred.

### FACT — ownership was lost across the workflow-step boundary

The next step reverified the exact client and then failed before launching generation 1:

```text
TRACK_A_RUNTIME_ERROR=xvfb_not_owned
```

`xvfb` PID `21792` had therefore passed exact Track/Task/Role ownership and no-secret checks during bootstrap, but the following workflow step could no longer prove that same process as task-owned. The generation-1 client and GDB observer were never launched.

### FACT — cleanup exposed stale X11 lifecycle residue

The final cleanup stopped both generation slots but exited non-zero before the task-process/X11 cleanup terminal markers. The failed run can therefore leave task-local PID files and/or `:115` lock/socket residue that a future run must not delete unless ownership can be established.

## Lifecycle repair

Workflow head `22885f000370fc3e1543e71795101d4a763871f3` keeps the exact repository helper hash-fenced and applies bounded task-local compatibility transformations at execution time.

The repair adds:

1. `setsid` around each process intended to persist across GitHub Actions shell-step boundaries:
   - task-local SOCKS relay;
   - task-local Xvfb;
   - generation client;
   - generation GDB observer.
2. a pre-bootstrap residue recovery fenced to exact failed run `31884531727`;
3. termination only for PIDs whose `/proc/<pid>/environ` proves exact Track, Task and expected Role markers;
4. fail-closed refusal to terminate an alive PID whose ownership cannot be proven;
5. X11 lock removal only when its PID matches the failed run's recorded Xvfb PID and that PID is dead;
6. X11 socket removal only after the old Xvfb is dead and `/proc/net/unix` does not report the socket active;
7. task SOCKS port `25415` must be free after residue recovery;
8. a separate post-bootstrap workflow step that requires the relay and Xvfb PIDs to still be alive, exact-task-owned and credential-variable-free after crossing the workflow-step boundary, before any client is launched.

The already-retired stale selector run no longer requires an Actions-write cancellation preflight. The workflow now needs only `contents: read`, while the actual RUNTIME job alone retains `official-client-re-runtime` concurrency.

## Safety classification

### FACT

- the repair does not touch the separately owned upstream wireproxy PID/process;
- it does not weaken exact client, WARP, role, credential or transport fences;
- it does not launch a game client until the new persistence gate succeeds;
- failed-run cleanup can act only on the exact canonical task/run namespace and exact owned process markers;
- no gameplay/movement/economic effect is introduced.

### INFERENCE

The short interval between successful Xvfb ownership verification and `xvfb_not_owned` makes workflow-step process lifecycle the narrowest evidence-backed failure domain. `setsid` plus a cross-step persistence gate tests that hypothesis directly without weakening semantic acceptance.

### UNKNOWN pending run #9

Run `31884912160` / job `95012697134` at head `22885f000370fc3e1543e71795101d4a763871f3` is the single active test of this repair. At this checkpoint it is assigned to runner id `21`; semantic results are not yet classified.
