# Track A XCB GL runtime trace — terminal evidence

## Exact execution

- PR: `#415`
- semantic workflow run: `31964397523`
- physical job: `95207211173`
- governance run on dispatch head: `31964397501 = SUCCESS`
- dispatch head: `8ffc60146573e5fb9ac1b900ff45843af10301dd`
- base: `main@d3f186414256151c9d5e03f34c5a9026b1fba500`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- immutable source harness blob: `1616edcc982be50ef2c95b8077160ec8fe9291fe`
- fenced transformation count: `6`
- exact client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

The run used only the task-owned ephemeral namespace created by the accepted isolated harness. It did not read or write the canonical lease, registration or session state, and it used no account credentials, login, gameplay or Track B surface.

## Task-owned X11 server observation

The accepted harness started its isolated Xvfb successfully on display `:231`. The added read-only core-X11 probe connected only to that task-owned UNIX socket and issued `ListExtensions` plus `QueryExtension` for `GLX` and `RENDER`.

Direct output:

```text
XCBGL_DIAG_X11_EXTENSION_COUNT=22
XCBGL_DIAG_X11_EXTENSIONS=BIG-REQUESTS,Composite,DAMAGE,DOUBLE-BUFFER,Generic Event Extension,MIT-SCREEN-SAVER,MIT-SHM,Present,RANDR,RECORD,RENDER,SECURITY,SHAPE,SYNC,X-Resource,XC-MISC,XFIXES,XINERAMA,XInputExtension,XKEYBOARD,XTEST,XVideo
XCBGL_DIAG_X11_GLX_PRESENT=false
XCBGL_DIAG_X11_GLX_MAJOR_OPCODE=0
XCBGL_DIAG_X11_RENDER_PRESENT=true
XCBGL_DIAG_X11_RENDER_MAJOR_OPCODE=139
```

Therefore the exact task-owned Xvfb display directly **does not advertise the GLX extension**. The immutable accepted harness launch command does not explicitly disable GLX; it starts Xvfb with the screen/XKB/no-listen/noreset arguments only. This evidence is about this exact contained Xvfb/runtime surface and must not be generalized to another X server or image without fresh proof.

## Qt XCB GL integration trace

The workflow scanned all `424` task-owned client-log lines locally and emitted only an allowlisted sanitized subset. `41` lines matched the XCB GL / GLX / EGL / QRhi / library-load filter.

The retained filtered trace directly proves:

```text
... libqxcb.so ... loaded library
checking directory path ".../Tibia/bin/plugins/xcbglintegrations" ...
looking at "libqxcb-glx-integration.so"
Found metadata in lib .../plugins/xcbglintegrations/libqxcb-glx-integration.so
"xcb_glx"
"className": "QXcbGlxIntegrationPlugin"
Got keys from plugin meta data QList("xcb_glx")
.../plugins/xcbglintegrations/libqxcb-glx-integration.so" loaded library
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
"vulkan" loaded library
Initializing QRhi Vulkan backend ...
```

This closes the prior #410/#412 uncertainty for the GLX side: the bundled XCB GL integration directory is scanned, `libqxcb-glx-integration.so` metadata is valid, key `xcb_glx` is obtained, and the library is loaded. The failure occurs after that point while the same X11 display directly reports no GLX extension.

The complete-log filter also included `EGL` and `libqxcb-egl-integration`. No `libqxcb-egl-integration.so` discovery/load line appears in the emitted complete-log match set. This is negative evidence about the exact `QT_DEBUG_PLUGINS` log only; it does **not** prove that an EGL plugin file is absent from the package or that every possible EGL code path is impossible.

## Bounded client/window state

The exact client started as PID/PGID `26073` inside the ephemeral task namespace and remained alive at all bounded snapshots:

```text
t+5s  client_alive=true  visible_window_count=0
t+15s client_alive=true  visible_window_count=0
t+35s client_alive=true  visible_window_count=0
WINDOW_DIAG_CLASSIFICATION=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
WINDOW_DIAG_RESULT=PASS_DISCRIMINATOR_CAPTURED
WINDOW_DIAG_CLEANUP=COMPLETE
```

The PID, display `:231` and VNC port `6200` are historical values of this destroyed ephemeral namespace only. Cleanup completed; none of them is current canonical authority.

## Classification

`PROVEN_TASK_OWNED_XVFB_GLX_ABSENT_QT_XCB_GLX_PLUGIN_DISCOVERED_AND_LOADED_CONTEXT_CREATION_FAILS_NO_GLX_OR_EGL`

Load-bearing facts now proven together:

- the exact task-owned Xvfb advertises no `GLX` extension;
- Qt loads the bundled `xcb` platform plugin;
- Qt scans `xcbglintegrations`;
- Qt discovers and loads `libqxcb-glx-integration.so` with key `xcb_glx`;
- Qt then reports that neither GLX nor EGL is enabled and the GLES2 RHI context path fails;
- Qt subsequently loads/initializes a Vulkan RHI path, but the exact client still has no visible window through 35 seconds.

The absence of GLX is a directly proven graphics prerequisite gap. It is **not yet proven to be the sole cause** of the final no-window state because a Vulkan RHI path also initializes later in the same log.

## Next discriminator

Stop this task without retry. A separately admitted support-only task should determine whether the exact contained Xvfb binary can expose GLX at all, preferably by:

1. read-only inventory of the exact contained Xvfb binary and its GLX-supporting modules/dependencies; and
2. if governance separately admits it, one task-owned Xvfb-only probe using explicit `+extension GLX`, followed by the same core-X11 extension query.

Do not launch the official client in that support probe. Do not retry canonical bootstrap, do not force a client RHI/backend, and do not infer that enabling GLX alone will produce a visible client window.