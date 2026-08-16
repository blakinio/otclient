# Track A canonical runtime v6 — client window discriminator

## Exact physical run

- PR: `#397`
- branch: `ci/OTC-20260816-track-a-canonical-runtime-e2e-v6`
- workflow head: `29c750adfbfbf0ea4db64005698b456a5b9c92b0`
- workflow run: `31957502867`
- job: `95190252936`
- runner: `synology-otclient-01`
- Track A governance run: `31957502830` = `SUCCESS`
- result: `FAIL_CLOSED / client_window_missing`

## Fresh admission

The job fenced exact trusted base `main@9e3634c1d822ffc6e74d8e42da63a4e8c60ea3e1`, re-proved the bounded-window worker contract, support root and exact system xkbcomp, then read current canonical lease state:

```text
RUNTIME_TRUSTED_WORKER_WAIT_CONTRACT=PASS
RUNTIME_SUPPORT_ROOT_PREFLIGHT=PASS
RUNTIME_SYSTEM_XKBCOMP_PREFLIGHT=PASS
pre-admission lease status=released generation=4
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=5
```

No pre-existing authoritative registration/session forced reclassification.

## Trusted bootstrap stage progression

The new non-secret stage markers prove the worker advanced through all support stages before failing at the bounded client-window discriminator:

```text
TRACK_A_CANONICAL_STAGE=warp_start
TRACK_A_CANONICAL_STAGE=wireproxy_configtest_start
TRACK_A_CANONICAL_STAGE=wireproxy_configtest_pass
TRACK_A_CANONICAL_STAGE=warp_egress_probe_start
TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass
TRACK_A_CANONICAL_STAGE=warp_pass
TRACK_A_CANONICAL_STAGE=xvfb_start
TRACK_A_CANONICAL_STAGE=xvfb_pass
TRACK_A_CANONICAL_STAGE=vnc_start
TRACK_A_CANONICAL_STAGE=vnc_pass
TRACK_A_CANONICAL_STAGE=client_start
TRACK_A_CANONICAL_STAGE=client_window_wait_start
TRACK_A_CANONICAL_SESSION_ERROR=client_window_missing
TRACK_A_CANONICAL_TRANSITION_ERROR=bootstrap_worker_failed
```

The wait ran for approximately the intended 30-second production budget. Because `window()` checks client liveness on every poll and returned the missing-window class rather than `client_exited`, the exact launched client PID remained alive through the bounded window observation.

## Failure boundary

- canonical lease generation acquired: `5`;
- exact support/X11/VNC prerequisites: passed;
- canonical WARP egress: passed;
- official exact-client launch stage: reached;
- exact client process remained alive during the 30-second window wait;
- visible `^Tibia$` window owned by that PID: not found within the bounded wait;
- authoritative registration: not published;
- Gate B: not reached;
- account credentials/login/gameplay: not used;
- transition failure path: fail-closed bootstrap rollback; controller lease released by workflow cleanup.

Current PID/session/display/VNC therefore remain unregistered/unclaimed after this attempt.

## Classification

`NEW_PHYSICAL_DISCRIMINATOR / CLIENT_ALIVE_NO_MATCHING_PID_OWNED_VISIBLE_TIBIA_WINDOW`

This result does not prove that the X11 desktop had no visible windows at all, nor that no related child process owned a relevant window. The current worker searches only visible windows matching `^Tibia$` for the exact launched client PID. A bounded follow-up must distinguish:

1. no mapped/visible client-related X11 window exists;
2. a visible relevant window exists but has a different title;
3. a visible Tibia/relevant window is owned by a child/other exact-runtime process rather than the launched PID;
4. the client is alive but blocked before mapping a window, with a bounded non-secret startup log discriminator.

No blind canonical bootstrap retry is justified before that bounded discriminator.

## Next evidence request

Use a separately admitted `ephemeral_isolated` RUNTIME diagnostic with no credentials/login and no canonical registration mutation. Reproduce only the already-proven startup environment on a high task-owned display, then collect a bounded sanitized inventory of:

- launched PID liveness/state;
- visible X11 window IDs/titles/classes/geometries and `_NET_WM_PID`/xdotool PID where available;
- whether any relevant visible window belongs to the launched PID or an owned child;
- a bounded, secret-filtered prefix/tail of the task-owned client startup log;
- task-owned process tree identity only as needed to associate X11 ownership.

Clean every diagnostic process/display/WARP helper afterward. Do not register a canonical runtime from the diagnostic.
