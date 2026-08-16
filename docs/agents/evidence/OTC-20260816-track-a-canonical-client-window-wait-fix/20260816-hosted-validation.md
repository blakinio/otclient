# Track A canonical client-window bounded-wait repair — hosted validation

## Source failure

Canonical RUNTIME v5 PR #393, workflow run `31956030015`, job `95186692121`, reached `synology-otclient-01`, passed the trusted support-root and exact `/usr/bin/xkbcomp` preflight, acquired canonical lease generation `4`, generated the canonical WARP profile and then stopped fail-closed at `TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout` before authoritative registration or Gate B.

Trusted-worker source review showed that the prior `window()` helper already had an internal `120 * 0.25s` polling budget (about 30 seconds), while `bootstrap()` wrapped it in another 100-iteration loop. A missing-window path could therefore exceed 3000 seconds and be terminated by the transition's 300-second worker timeout before `client_window_missing` was observable.

## Fresh-main repair

Canonical candidate PR: `#395` from exact base `main@ffe954be315ee29825c726b996a30fea8475a0f3`.

Validated semantic head: `f82c35cba98690d30676fa34997895ba6daf0c82`.

The worker now:

- uses one explicit production window-wait budget: `120 * 0.25s` (~30 seconds);
- checks client liveness on every polling iteration;
- maps a dead PID to `client_exited`;
- maps an exhausted live-PID search to `client_window_missing`;
- reserves unexpected helper status for `client_window_probe_failed`;
- uses the same bounded helper in bootstrap and probe;
- removes the previous outer 100-iteration multiplier;
- adds non-secret stage markers around wireproxy/WARP, Xvfb, VNC, client start and client-window wait progression.

## Hosted semantic validator

- workflow run: `31956997604`
- job: `95189035137`
- runner: GitHub-hosted Ubuntu 24.04
- result: `SUCCESS`
- runtime access: `none`
- physical E2E: `false`

Exact results:

```text
canonical session tests: 10 PASS
canonical transition tests: 9 PASS
canonical guard tests: 3 PASS
canonical lease tests: 14 PASS
TRACK_A_CANONICAL_WINDOW_WAIT_VALIDATION=PASS
TRACK_A_RUNTIME_ACCESS=none
TRACK_A_PHYSICAL_E2E=false
```

The session suite behaviorally exercises:

- a visible matching Tibia window;
- a dead client PID;
- a live client PID with no window;
- the production wait-budget/source-shape invariant.

The validator checked the pull-request merge ref against current main, so the repair was tested together with the terminal v5 RUNTIME checkpoint on `main`.

## Classification

`PASS / HOSTED_BOUNDED_WINDOW_WAIT_REPAIR_PROVEN`

No Synology/client/X11/VNC/WARP/login/credentials/canonical registration were accessed by this repair validation. The temporary semantic workflow is task-owned and must be removed before promotion. A new physical RUNTIME attempt is permitted only after this repair is promoted to trusted `main` and a fresh admission record is created.
