# Track A isolated client-window discriminator — first-run harness failure

## Exact run

- PR: `#398`
- task: `OTC-20260816-track-a-client-window-ownership-discriminator`
- workflow run: `31957940075`
- job: `95191373266`
- runner: `synology-otclient-01`
- result: `FAIL_CLOSED / DIAGNOSTIC_HARNESS_DEFECT_BEFORE_OBSERVATION`

## Admission and isolation facts

The task had fresh Track A admission as `ephemeral_isolated`, with both governance jobs in run `31957846249` passing. The physical run created only its task-owned namespace and selected fresh high-display/loopback resources:

```text
WINDOW_DIAG_NAMESPACE=/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260816-track-a-client-window-ownership-discriminator/ephemeral-31957940075-1
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_DISPLAY=:231
WINDOW_DIAG_VNC_PORT=6200
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_XVFB=PASS
WINDOW_DIAG_VNC=PASS
```

No canonical lease/registration/session state was read or written by the diagnostic.

## Harness defect

The first workflow launched the copied exact client through a background subshell containing `setsid`, then assumed the shell job PID would necessarily be the new process-group ID. The actual observation was:

```text
WINDOW_DIAG_REFUSED=CLIENT_NOT_ISOLATED_GROUP:pid=17676:pgid=64
```

The workflow stopped immediately at that harness assertion, before any 5/15/35-second X11 window snapshot or sanitized client-startup-log discriminator ran. Therefore this run provides **no evidence** about client window title, visibility, ownership, or startup state.

The isolation objective does not require a private process group: the admission contract requires a unique task-owned sandbox, and process mutation/cleanup can be bounded by the task marker plus the launched PID and marker-verified descendants. Requiring `PGID == PID` was an unnecessary harness assumption.

## Cleanup

The exit trap completed:

```text
WINDOW_DIAG_CLEANUP=COMPLETE
```

No canonical registration was published, no credentials/login/gameplay were used, and no client-window conclusion is promoted from this run.

## Fidelity correction required before one repaired run

A repaired run is evidence-based, not a blind retry. Before it may execute:

1. remove the `PGID == PID` prerequisite and never use process-group cleanup;
2. identify/terminate only the launched task-marker PID plus marker-verified descendants discovered through that known ancestry;
3. verify the launched PID actually resolves to the copied exact client and carries the task marker before observation;
4. mirror the trusted worker's conditional `launchermetadata.json` copy exactly, so a negative window result cannot be blamed on a known startup-environment difference;
5. retain the same high-display/task-root/loopback WARP/VNC isolation, bounded 35-second observation, sanitized log boundary, no-login/no-credentials rule and full cleanup.

Classification: `HARNESS_REPAIR_AUTHORIZED / ONE_REPAIRED_PHYSICAL_DISCRIMINATOR_ALLOWED`.
