# Track A final client-window ownership/startup discriminator — 2026-08-16

## Scope

One final `ephemeral_isolated` no-login diagnostic on `synology-otclient-01` after two earlier harness-only failures. The run reproduced the trusted exact-client startup environment in a run-specific high-display sandbox, collected bounded X11/process/startup-log evidence, and cleaned all task-owned state. It did not read or write canonical lease/registration state and did not use account credentials, login input, gameplay input, Track B state, or BattlEye internals.

## Exact final run

- PR: `#398`
- source branch: `ci/OTC-20260816-track-a-client-window-ownership-discriminator`
- semantic wrapper head: `d65a883baa75e6de7b356c6f66b555b9aeb93a6c`
- workflow run: `31958546334`
- job: `95192878995`
- runner: `synology-otclient-01`
- result: `SUCCESS`
- cleanup: `WINDOW_DIAG_CLEANUP=COMPLETE`

The wrapper fetched immutable v3 source commit `cb557da12ebb41c597340909b2db717ee59cdfe1`, required Git blob `1616edcc982be50ef2c95b8077160ec8fe9291fe`, applied exactly one deterministic shell-local repair, passed `bash -n`, and proved the generated script had no canonical runtime-registration/lease surface.

```text
WINDOW_DIAG_FINAL_SOURCE_BLOB=PASS:1616edcc982be50ef2c95b8077160ec8fe9291fe
WINDOW_DIAG_FINAL_PATCH_COUNT=1
WINDOW_DIAG_FINAL_ANCESTRY_ONLY=PASS
WINDOW_DIAG_FINAL_CANONICAL_STATE_ACCESS=NONE
WINDOW_DIAG_FINAL_BASH_N=PASS
```

## Admission and exact-client fence

```text
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_DISPLAY=:231
WINDOW_DIAG_VNC_PORT=6200
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_LAUNCHERMETADATA=SOURCE_ABSENT_OR_UNSAFE
WINDOW_DIAG_XVFB=PASS
WINDOW_DIAG_VNC=PASS
WINDOW_DIAG_CLIENT_PID=22224
WINDOW_DIAG_CLIENT_PGID=22224
WINDOW_DIAG_CLIENT_START=PASS
```

`launchermetadata.json` was absent or unsafe at the trusted conditional source path; the diagnostic therefore followed the same conditional behavior as the canonical worker and did not invent metadata.

The launched process was verified against the copied exact executable fence:

- client version: `15.32.df7b29`
- client size: `51965216`
- client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Bounded X11/process observation

At all three bounded snapshots the exact client remained alive and no visible X11 window existed on the isolated display:

```text
WINDOW_DIAG_SNAPSHOT=t05
WINDOW_DIAG_CLIENT_ALIVE=true:state=R
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0

WINDOW_DIAG_SNAPSHOT=t15
WINDOW_DIAG_CLIENT_ALIVE=true:state=S
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0

WINDOW_DIAG_SNAPSHOT=t35
WINDOW_DIAG_CLIENT_ALIVE=true:state=S
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0
```

No marker-owned descendant process appeared in the bounded ancestry snapshots. Therefore the v6 failure is not explained by a differently titled visible window or a visible child-owned window during this observation window.

## Sanitized startup-log discriminator

The task-owned client log repeatedly recorded the following non-secret startup errors before and during the no-window interval:

```text
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
failed to acquire GL context to resolve capabilities, using defaults..
```

The same process later reached `Asset loading complete` and successfully made proxied HTTPS requests to `static.tibia.com` / `www.tibia.com`, so the evidence does not support a simple early process crash or WARP/network failure. ALSA errors were also present, but the client explicitly selected a null playback device and remained alive.

The log also contained a Qt thread-affinity warning involving `QQmlEngine` and `QSGSoftwareRenderThread`. This is recorded as an observation only; its causal relevance is not proven.

## Classification

`PASS / CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY`

Directly proven:

- exact client process stayed alive through 35 seconds;
- WARP, Xvfb and localhost-only VNC startup passed;
- visible X11 window count on the task-owned display was exactly zero at 5, 15 and 35 seconds;
- no visible differently titled task-owned window and no visible child-owned window existed in those snapshots;
- startup log repeatedly reported missing GLX/EGL OpenGL context and QRhiGles2 context creation failure;
- cleanup completed and no canonical registration was published.

Not proven:

- that the GLX/EGL/QRhi failure is the sole causal reason no window maps;
- that ALSA or the Qt thread-affinity warning is causal;
- that changing any graphics environment variable is safe or sufficient without hosted source/contract analysis and a separately admitted physical validation.

## Disposition

The ownership/title discriminator is complete. The next safe step is a separate GitHub-hosted, `runtime_access: none` analysis/fix task for the canonical client's graphics/render-backend startup contract. It must use this direct runtime evidence plus the trusted worker environment (`QT_QUICK_BACKEND=software`, `QT_XCB_GL_INTEGRATION=none`, contained libraries) to identify a minimal deterministic change and add hosted contract tests before any further physical canonical bootstrap.

No further physical retry is authorized from this discriminator task.
