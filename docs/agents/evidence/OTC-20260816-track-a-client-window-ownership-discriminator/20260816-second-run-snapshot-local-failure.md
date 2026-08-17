# Track A isolated client-window discriminator — second harness failure

## Exact run

- PR: `#398`
- task: `OTC-20260816-track-a-client-window-ownership-discriminator`
- repaired-generation head: `cb557da12ebb41c597340909b2db717ee59cdfe1`
- workflow run: `31958323922`
- job: `95192357706`
- runner: `synology-otclient-01`
- Track A governance run: `31958324115` = `SUCCESS`
- result: `FAIL_CLOSED / DIAGNOSTIC_SNAPSHOT_HARNESS_DEFECT_BEFORE_WINDOW_CAPTURE`

## Progress beyond the first run

This run fixed the first PGID harness assumption and reproduced substantially more of the trusted startup path:

```text
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_DISPLAY=:231
WINDOW_DIAG_VNC_PORT=6200
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_LAUNCHERMETADATA=SOURCE_ABSENT_OR_UNSAFE
WINDOW_DIAG_XVFB=PASS
WINDOW_DIAG_VNC=PASS
WINDOW_DIAG_CLIENT_PID=20841
WINDOW_DIAG_CLIENT_PGID=20841
WINDOW_DIAG_CLIENT_START=PASS
```

The exact live client PID passed marker/role, executable realpath, exact size and exact SHA checks. The repaired launcher used `subprocess.Popen(..., start_new_session=True)` and observed its real client PID/PGID directly, so the previous `PGID==PID` assumption was no longer a blocker.

The trusted worker's conditional `launchermetadata.json` source path was also mirrored. That optional source did not exist as a safe regular file in this environment, which is equivalent to the canonical worker's no-copy branch and is therefore not a fidelity mismatch.

## Second harness defect

The very first snapshot call stopped immediately under `set -u` with:

```text
line 349: label: unbound variable
```

The cause is deterministic shell evaluation order in this local declaration:

```bash
local label="$1" out="$root/windows-$label.tsv" pids="$root/pids-$label.txt"
```

`$label` is expanded while the same `local` command is being evaluated, before the local `label` assignment is established under nounset. No X11 window inventory, process snapshot or sanitized client-log discriminator was emitted.

This is a one-line harness bug and does not change the physical startup result above.

## Cleanup and safety

The exit trap emitted:

```text
WINDOW_DIAG_CLEANUP=COMPLETE
```

No canonical lease/registration/session state was read or written, no credentials/login/gameplay were used, and no semantic client-window conclusion is promoted from this run.

## Final harness-repair allowance

A final harness repair is evidence-based rather than a blind retry:

```bash
local label="$1"
local out="$root/windows-$label.tsv"
local pids="$root/pids-$label.txt"
```

Before the final physical discriminator executes, its generated shell must pass `bash -n` and an exact source-shape fence proving:

- the three declarations are split;
- the old compound declaration is absent;
- no broad `/proc/*` marker scan is present;
- the exact-client/live-PID fences and conditional launchermetadata fidelity remain present;
- canonical lease/registration paths remain absent from the diagnostic script.

Classification: `FINAL_HARNESS_REPAIR_AUTHORIZED / NO_FURTHER_HARNESS_RETRY_AFTER_THIS`.
