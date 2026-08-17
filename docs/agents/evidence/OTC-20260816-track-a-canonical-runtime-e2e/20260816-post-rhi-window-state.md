# Track A post-RHI X11 window-state result

## Execution

Task: `OTC-20260816-track-a-canonical-runtime-e2e`  
Source Draft: `#438`  
Semantic head: `8e9cc81011383922cf6bad75ca7207deb749fffb`  
Trusted base: `b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`  
Workflow run: `31972261899`  
Hosted preflight: `95226378236 = SUCCESS`  
Physical job: `95226396914 = SUCCESS` on `synology-otclient-01`  
Cleanup: `COMPLETE`  
Canonical state access: `NONE`

The one-shot workflow and both temporary transformer files were removed immediately after the valid discriminator. No second physical run is authorized by this result.

## Fences

The physical job passed same-generation Track A admission and exact base/source/support fences. The exact official client remained fenced to size `51965216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Contained Xvfb graphics state remained healthy:

- X11 extension count: `23`
- GLX: `true`, opcode `150`
- RENDER: `true`, opcode `139`

## Raw X11 tree

### t+05 — FACT

Client alive. Raw X11 contained one non-root window:

- XID `12582917` (`0x00c00005`)
- map state `UNMAPPED`
- geometry `3x3+0+0`
- PID unavailable through the available property query
- empty name/class

Counts: `total=1`, `viewable=0`, `unmapped=1`.

### t+15 — FACT

Client alive. Raw X11 contained three non-root windows:

- `12582917` (`0x00c00005`) — `UNMAPPED`, `3x3`
- `12582931` (`0x00c00013`) — `UNMAPPED`, `1x1`
- `12582929` (`0x00c00011`) — **`VIEWABLE`, `1920x1080+0+0`**

Available PID/name/class queries did not identify these XIDs. Counts: `total=3`, `viewable=1`, `unmapped=2`.

### t+35 — FACT

The same three-XID shape persisted, including the same **VIEWABLE 1920x1080** XID `0x00c00011`. The exact client remained alive.

The historical xdotool named-visible search still returned `0` at all snapshots.

## Observation correction — FACT

The earlier phrase "zero visible windows" was too strong when based only on the xdotool named-window search. Raw `XGetWindowAttributes` directly proves that a non-root **VIEWABLE** full-display X11 window exists from t+15 onward. The previous search did not see it because usable name/PID/class metadata was not available through that query path.

## XID grouping — INFERENCE

The three XIDs share the `0x00c00000` resource-base region. This is consistent with one X client connection owning the resources, but it is not direct process-identity proof. No XRes client-ID proof was captured in this run.

## Thread progression — FACT

The exact client progressed from 3 threads at t+05 to 32 at t+15 and 38 at t+35. Observed runtime threads included:

- `QXcbEventQueue`
- `llvmpipe-0..3`
- `QQmlThread`
- `QSGSoftwareRend`
- multiple Qt pooled workers
- `QNetworkAccessM`
- `QQuickPixmapRea`

This confirms substantial graphics/QML/network initialization rather than an early graphics-loader exit.

## Broader client log — FACT

Complete local client log: `415` lines. Broader redacted filter: `121` matches.

Load-bearing observations:

- xcb platform plugin loaded;
- xcb GLX integration loaded;
- OpenGL 4.5 context successfully created;
- renderer is Mesa llvmpipe;
- Vulkan library loaded and QRhi Vulkan initialized;
- XCB surface and swapchain support present;
- QtQuick.Window and QtQuick Controls related modules loaded.

A warning appears after QML/QtQuick initialization: QObject reports an attempt to create children for a parent in a different thread; the parent is `QQmlEngine` and the current thread is `QSGSoftwareRenderThread`.

The warning is a discriminator, not proven causal.

## Classification

Primary bounded classification:

`PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX`

Generated-harness classification:

`NONROOT_X11_WINDOWS_PRESENT_NONE_TASK_PID_BOUND`

The second classification means only that the available PID property path did not bind the XIDs to the task PID. It does not prove the viewable window is foreign.

## Current unknowns

1. Whether XID `0x00c00011` is the intended official-client top-level window, an internal/backing Qt window, or another task-display resource.
2. Why PID/name/class metadata is absent through the current property-query path.
3. Whether the QQmlEngine/QSGSoftwareRenderThread warning contributes to the missing top-level identity or is incidental.

## Consequence

The canonical worker currently requires a visible window bound to the exact PID and named `Tibia`. The current evidence proves a viewable X window exists but does not yet prove that identity contract. Relaxing the worker to accept any full-screen viewable XID would therefore be unsafe.

Canonical bootstrap remained intentionally unattempted in this discriminator. The next causal step is direct X resource/PID identity proof before any canonical retry or window-identity relaxation.
