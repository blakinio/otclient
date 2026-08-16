# Track A isolated client-window discriminator — final semantic result

## Exact final run

- PR: `#398`
- task: `OTC-20260816-track-a-client-window-ownership-discriminator`
- final-wrapper head: `d65a883baa75e6de7b356c6f66b555b9aeb93a6c`
- workflow run: `31958546334`
- job: `95192878995`
- runner: `synology-otclient-01`
- Track A governance run: `31958546329` = both admission jobs `SUCCESS`
- result: `SUCCESS / PASS_DISCRIMINATOR_CAPTURED`

## Final harness fences

The final run fetched the immutable v3 diagnostic from commit `cb557da12ebb41c597340909b2db717ee59cdfe1`, verified its exact Git blob `1616edcc982be50ef2c95b8077160ec8fe9291fe`, applied exactly one nounset-safe local-declaration repair, then verified the generated shell before execution:

```text
WINDOW_DIAG_FINAL_SOURCE_BLOB=PASS:1616edcc982be50ef2c95b8077160ec8fe9291fe
WINDOW_DIAG_FINAL_PATCH_COUNT=1
WINDOW_DIAG_FINAL_ANCESTRY_ONLY=PASS
WINDOW_DIAG_FINAL_CANONICAL_STATE_ACCESS=NONE
WINDOW_DIAG_FINAL_BASH_N=PASS
```

No broad `/proc` ownership scan, canonical lease/registration/session access, credentials, login or gameplay was permitted by this diagnostic.

## Isolated startup reproduction

The final diagnostic used a run-specific task-owned sandbox and high display:

```text
WINDOW_DIAG_NAMESPACE=.../ephemeral-31958546334-1
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

The optional `launchermetadata.json` source was absent/unsafe, matching the trusted canonical worker's conditional no-copy branch rather than introducing a known fidelity difference.

## Window/process observations

Three bounded snapshots were collected on the task-owned X11 display:

### t+5s

```text
WINDOW_DIAG_CLIENT_ALIVE=true:state=R
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0
```

### t+15s

```text
WINDOW_DIAG_CLIENT_ALIVE=true:state=S
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0
```

### t+35s

```text
WINDOW_DIAG_CLIENT_ALIVE=true:state=S
WINDOW_DIAG_TASK_PROCESS=pid=22224:ppid=1:comm=client:exe=client
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0
```

No marker-verified descendant process was observed in the bounded ancestry snapshots. Therefore the canonical v6 failure was not merely caused by searching for the wrong window title or only the launched PID: in the isolated reproduction there were **zero visible X11 windows of any title/class** at all while the exact client remained alive.

## Sanitized startup-log evidence

The bounded task-owned client log contains, among other non-secret lines:

```text
[proxychains] DLL init: proxychains-ng 4.17
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
failed to acquire GL context to resolve capabilities, using defaults..
Using spritesheet cache size of 910
Asset loading complete
StartDownload: QUrl("https://static.tibia.com/hints.json")
```

Proxychains also successfully reached `static.tibia.com:443` and `www.tibia.com:443`. Audio initialization fell back to the NULL playback device; this is recorded but is not promoted as the window blocker.

A later log line reported a Qt thread-affinity warning involving `QQmlEngine` and `QSGSoftwareRenderThread`. This is evidence of execution reaching Qt Quick rendering work, but by itself does not prove root cause.

## Semantic classification

```text
WINDOW_DIAG_CLASSIFICATION=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
WINDOW_DIAG_RESULT=PASS_DISCRIMINATOR_CAPTURED
WINDOW_DIAG_CLEANUP=COMPLETE
```

Classification: `PROVEN_CLIENT_ALIVE_ZERO_VISIBLE_WINDOWS_WITH_QT_GL_CONTEXT_FAILURES`.

### PROVEN

- exact-client startup reached a live process in the isolated task namespace;
- WARP, Xvfb and VNC startup passed;
- the exact client stayed alive through 35 seconds;
- the task-owned display had zero visible windows at 5, 15 and 35 seconds;
- no marker-verified child process was observed in the bounded ancestry snapshots;
- the client log directly reports XCB/QRhiGles2 failure to create OpenGL/offscreen contexts because neither GLX nor EGL is enabled;
- asset loading completed and HTTPS requests proceeded through the task-owned proxy;
- cleanup completed and no canonical runtime was registered.

### NOT PROVEN / UNKNOWN

- that the GLX/EGL context failure is the sole cause of the missing visible window;
- whether removing `QT_XCB_GL_INTEGRATION=none`, providing a functional GLX/EGL software stack, changing the Qt RHI backend, or another graphics adjustment is the correct production fix;
- whether a canonical client would map a window after such a graphics fix;
- current canonical display/VNC/PID/session identity, which remains unregistered.

## Required next step

Do **not** repeat canonical bootstrap or this discriminator. The next task is GitHub-hosted RUNTIME-INFRA research/fix work that:

1. inventories the trusted worker's graphics environment and the runner/toolroot GLX/EGL/Mesa support;
2. correlates the observed Qt 6.9.3 XCB/QRhiGles2 messages with official Qt behavior using public primary sources where needed;
3. identifies the smallest fail-closed environment/toolroot correction that permits a visible window without weakening client identity or runtime admission rules;
4. validates the correction deterministically/hosted where possible and promotes it to trusted `main` before any new physical canonical bootstrap.
