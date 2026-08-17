# Track A canonical graphics integration fix — hosted source evidence

## Triggering physical evidence

Terminal discriminator PR #398 / run `31958546334` / job `95192878995` proved the exact `15.32.df7b29` client remained alive through 35 seconds while the task-owned X11 display had zero visible windows at t+5/t+15/t+35. The sanitized client log directly recorded:

```text
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
```

That evidence did **not** prove the graphics error was the sole root cause, but selected graphics-stack compatibility as the next hosted-only boundary.

## Trusted-worker source state

Before this fix the canonical worker launched the exact client with both:

```text
QT_QUICK_BACKEND=software
QT_XCB_GL_INTEGRATION=none
```

## Qt 6.9.3 primary-source proof

Upstream repository: `qt/qtbase`
Tag: `v6.9.3`
Path: `src/plugins/platforms/xcb/qxcbconnection.cpp`
Exact inspected blob: `e6d232d0ef95023e8b1586b706743fc7f01c3711`

`QXcbConnection::glIntegration()` initializes the default candidate list in order as `xcb_glx`, then `xcb_egl`. It reads `QT_XCB_GL_INTEGRATION`; when the value equals `none`, it clears the candidate list. If candidates remain, Qt tries them in priority order and keeps the first integration whose initialization succeeds.

Therefore the trusted worker's explicit `QT_XCB_GL_INTEGRATION=none` deterministically prevents Qt XCB from selecting either GLX or EGL integration. This source behavior directly matches the observed wording that neither GLX nor EGL is enabled.

## Minimal correction

The worker client environment is changed only from:

```text
QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none
```

to:

```text
QT_QUICK_BACKEND=software QSG_INFO=1
```

Properties:

- `QT_QUICK_BACKEND=software` remains unchanged;
- the explicit XCB GL integration disablement is removed, allowing Qt's own GLX/EGL selection logic to run;
- `QSG_INFO=1` adds non-secret Qt Quick scenegraph initialization diagnostics for the later physical validation;
- no `QSG_RHI_BACKEND` is forced, because evidence does not yet justify selecting a specific renderer/API;
- exact-client identity/fence, WARP, X11/VNC, lease, registration, Gate B, rollback and credential boundaries are unchanged.

## Hosted contract test

`.github/scripts/test_tibia_official_client_re_canonical_live_session.py` requires the canonical client launch block to contain:

- `QT_QUICK_BACKEND=software`;
- `QSG_INFO=1`;
- no `QT_XCB_GL_INTEGRATION=none` anywhere in the worker;
- no forced `QSG_RHI_BACKEND=` in the launch block.

## Exact hosted validation

Temporary GitHub-hosted validator:

- workflow run: `31959453898`
- job: `95195086514`
- runner: `ubuntu-24.04`
- result: `SUCCESS`
- runtime access: `none`
- physical E2E: `false`

Exact suite results:

```text
canonical session tests: 11 PASS
canonical transition tests: 9 PASS
canonical guard tests: 3 PASS
canonical lease tests: 14 PASS
TRACK_A_CANONICAL_GRAPHICS_INTEGRATION_CONTRACT=PASS
TRACK_A_RUNTIME_ACCESS=none
TRACK_A_PHYSICAL_E2E=false
```

The validator also ran `bash -n` against the worker. The session suite includes the new graphics-environment contract and retained bounded-window/toolroot tests; transition, guard and lease suites remained green without physical runtime access.

The temporary validator workflow is task-owned and is removed before promotion.

## Classification

`PASS / HOSTED_GRAPHICS_INTEGRATION_SOURCE_FIX_PROVEN / PHYSICAL_RESULT_UNKNOWN`

This task does not claim that GLX/EGL libraries/plugins are present and functional on `synology-otclient-01`, nor that a visible Tibia window will map after the change. A fresh physical canonical bootstrap is allowed only after this fix reaches trusted `main` and must independently re-prove all admission/support/identity gates.
