# Track A RUNTIME Xvfb bootstrap-exit evidence

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Execution head: `22885f000370fc3e1543e71795101d4a763871f3`
Run: `31884912160`
Job: `95012697134`
Runner: `synology-otclient-01`, id `21`
Conclusion: `FAILURE`
Artifact id: `9247009047`
Artifact ZIP SHA-256: `1e0390c04fc219d33130f5affb137f3995b4dc6294f6867a8f9eeaee57104edb`

## FACT — residue recovery succeeded

The run first recovered only residue attributable to failed run `31884531727`. Exact task/run path, task process markers, old Xvfb PID, X11 lock/socket activity and task SOCKS port were checked fail-closed before removal. The step completed with:

```text
TRACK_A_RUNTIME_FAILED_RUN_RESIDUE_RECOVERED=true
```

This closes the specific stale-residue concern from run #8.

## FACT — source/upstream/relay remained healthy

Bootstrap again proved:

```text
TRACK_A_RUNTIME_SOURCE_STATE=/work/_otclient_tibia_re_state
TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=16739 source_state=/work/_otclient_tibia_re_state
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=socks-relay pid=22453
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415 pid=22453
```

The effective helper contained the bounded `setsid` lifecycle transform and had SHA-256:

```text
f95dab73ce110629dff117600798d7787487036cb1c1b82716a4d4eb74935432
```

## FACT — new failure occurs inside `start_xvfb`

Unlike run #8, the run never reached a successful Xvfb ownership marker. Bootstrap failed directly with:

```text
TRACK_A_RUNTIME_ERROR=xvfb_exited
```

Therefore `setsid` did not merely fail the later cross-step ownership check: the Xvfb process itself exited during the bounded startup loop. Generation 1, login, client and GDB observer were never started.

## Cleanup

Final generation stop calls executed, but the helper cleanup again returned non-zero before full task/X11 cleanup markers. Run #9 task-local residue is therefore retained as diagnostic evidence until it can be inspected read-only and then recovered under exact ownership fences.

No protected credential value was printed. No login, movement or gameplay/economic action occurred.

## Classification

### FACT

- runner selector is healthy;
- exact source client and WARP are healthy;
- task-local SOCKS relay is healthy under the lifecycle transform;
- failed-run #8 residue was recovered safely;
- Xvfb exits during startup in run #9;
- the next useful evidence is the task-owned `runtime/xvfb.log`, not another identical bootstrap retry.

### INFERENCE

The previous run #8 `xvfb_not_owned` and current `xvfb_exited` may share an Xvfb startup/runtime cause rather than being purely GitHub Actions shell-boundary cleanup. The exact Xvfb log is required to discriminate command/loader/display/XKB/GLX failures.

### UNKNOWN

- the exact Xvfb stderr cause;
- whether the source Xvfb binary/dependencies are currently executable in the run environment;
- whether `setsid` itself changes process startup semantics materially;
- generation-1/2 runtime semantics and direct P0 handoff remain untested.

## Diagnostic run

Workflow head `4999b050ff83b8734528949e53ae4abad2728b1c` temporarily performs only read-only inspection of exact run `31884912160` residue and sanitizes the Xvfb log. Diagnostic run `31885018787` / job `95012954293` is the sole active operation at this checkpoint. It does not start/stop a client, Xvfb, relay or shared upstream process and does not mutate residue.
