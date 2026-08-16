# Track A canonical client-window bounded-wait fix — hosted validation

## Source failure

Physical RUNTIME v5 PR #393, run `31956030015`, job `95186692121`, passed the trusted support-root/xkbcomp preflight and acquired canonical lease generation `4`, then stopped fail-closed at `TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout` before registration or Gate B.

Source review proved the trusted worker's `window()` helper already polls up to `120 * 0.25s` (~30 s), while `bootstrap()` wrapped that helper in a second 100-iteration loop. The nominal missing-window path could therefore take roughly 3025 seconds, exceeding the transition worker timeout of 300 seconds and masking the intended `client_window_missing` discriminator.

## Fix

Validated source head: `7cc7c64aa40b6662973dbc2f059a099a89a184c6` on PR #394.

The change:
- checks client liveness inside each bounded `window()` poll and returns code `2` for a dead PID;
- removes the 100-iteration outer `bootstrap()` multiplier;
- performs exactly one bounded window search;
- maps dead PID to `client_exited` and exhausted live-PID search to `client_window_missing`;
- aligns `probe()` with the same failure distinction;
- adds non-secret stage markers for WARP, Xvfb, VNC, client start and client-window readiness.

## Hosted validator

- workflow run: `31956703737`
- job: `95188323165`
- runner: GitHub-hosted Ubuntu 24.04
- result: `SUCCESS`
- physical runtime access: `none`

Validation results:
- `bash -n` canonical session worker: PASS;
- canonical session tests: 9 PASS;
- canonical transition tests: 9 PASS;
- canonical guard tests: 3 PASS;
- canonical lease tests: 14 PASS;
- explicit bounded-window structural validator: `TRACK_A_BOUNDED_WINDOW_WAIT_VALIDATION=PASS`.

The validator ran against the GitHub pull-request merge ref containing current main `ffe954be315ee29825c726b996a30fea8475a0f3` plus source head #394, so the fix was tested together with the terminal v5 runtime checkpoint now on main.

## Classification

`PASS / HOSTED_BOUNDED_WAIT_DEFECT_REPAIRED`

No Synology/client/X11/VNC/WARP/login/credentials/canonical registration was accessed by this fix validation. Before promotion the temporary validator workflow is removed. Because source branch #394 was created one commit before the v5 terminal checkpoint landed on main, final promotion should use a fresh-main exact-blob replay rather than merging the diverged source history.
