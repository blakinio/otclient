# Track A isolated QSG / GLX / EGL / RHI discriminator — terminal result

## Exact run

- PR: `#406`
- task: `OTC-20260816-track-a-qsg-glx-egl-rhi-discriminator`
- base: `main@d7a2d4168816cb42267fc7b20aacb88ae1b13b8e`
- workflow run: `31961555061`
- job: `95200193452`
- runner: `synology-otclient-01`
- Track A governance run: `31961554989 = SUCCESS`
- result: `SUCCESS / PASS_DISCRIMINATOR_CAPTURED`

## Harness fences

The one-shot fetched immutable source blob `1616edcc982be50ef2c95b8077160ec8fe9291fe` from commit `cb557da12ebb41c597340909b2db717ee59cdfe1`, applied exactly three predeclared source transformations and passed shell syntax validation:

```text
QSG_DIAG_SOURCE_BLOB=PASS:1616edcc982be50ef2c95b8077160ec8fe9291fe
QSG_DIAG_PATCH_COUNT=3
QSG_DIAG_CANONICAL_STATE_ACCESS=NONE
QSG_DIAG_GRAPHICS_ENV=QT_QUICK_BACKEND_software,QSG_INFO_1
QSG_DIAG_BASH_N=PASS
```

The execution was `ephemeral_isolated`; it did not read/write canonical lease, registration or session state and did not use credentials/login/gameplay.

## Isolated startup

```text
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_DISPLAY=:231
WINDOW_DIAG_VNC_PORT=6200
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_XVFB=PASS
WINDOW_DIAG_VNC=PASS
WINDOW_DIAG_CLIENT_PID=24554
WINDOW_DIAG_CLIENT_PGID=24554
WINDOW_DIAG_CLIENT_START=PASS
```

The exact client remained alive at t+5s, t+15s and t+35s. Each snapshot reported `WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0`. No marker-owned descendant process was observed.

## Graphics/backend evidence

The sanitized `QSG_INFO=1` client log directly proves all of the following in the same run:

- XCB still reports `Cannot create platform OpenGL context, neither GLX nor EGL are enabled`;
- `QRhiGles2` fails temporary/context creation;
- Qt then initializes the **QRhi Vulkan backend**;
- Vulkan instance extensions include `VK_KHR_surface` and `VK_KHR_xcb_surface`;
- physical device 0 is `llvmpipe (LLVM 20.1.2, 128 bits)`, Mesa `25.2.8`, Vulkan API `1.4.318`, and Qt selects it;
- `VK_KHR_swapchain`, `VK_KHR_create_renderpass2`, and `VK_KHR_depth_stencil_resolve` are enabled;
- Qt reports `Using queue family index 0 and queue index 0`;
- Qt Quick reports `Loading backend software` and `Using sg animation driver`;
- later capability probing still reports the same XCB GL-context failure;
- asset loading completes and HTTPS traffic to Tibia endpoints succeeds through the task-owned proxy.

## Classification

`PROVEN_VULKAN_LLVMPIPE_INITIALIZES_WHILE_XCB_GLX_EGL_UNAVAILABLE_AND_NO_VISIBLE_WINDOW`

### PROVEN

- removal of the explicit `QT_XCB_GL_INTEGRATION=none` self-disable is present in the executed harness;
- QSG diagnostics are active;
- QRhi Vulkan initializes successfully on llvmpipe and creates a Vulkan/XCB-capable device path;
- Qt Quick selects the software scenegraph backend;
- XCB platform OpenGL/offscreen context creation still has neither GLX nor EGL available;
- the exact client remains alive for at least 35 seconds;
- the isolated display has zero visible windows at 5/15/35 seconds;
- canonical state was untouched and task-owned cleanup completed.

### FALSIFIED / NARROWED

- the hypothesis that `QT_XCB_GL_INTEGRATION=none` alone caused the missing visible window is falsified for this runner/package state;
- general GPU/Vulkan absence is not the blocker: Vulkan through llvmpipe initializes successfully.

### UNKNOWN

- whether the XCB GLX/EGL integration plugins are absent, not discoverable, fail to load, or fail initialization;
- whether the missing visible window is caused solely by XCB GL integration failure;
- whether forcing a different Qt Quick/RHI backend would be correct or safe;
- whether an XCB plugin-path/library correction is sufficient to map the window.

## Required next step

Do not repeat canonical bootstrap and do not repeat this exact semantic run. The next bounded task should inventory, without canonical mutation, the exact-client/package and trusted toolroot Qt XCB GL integration plugin surfaces and their dynamic dependencies, especially `xcbglintegrations`, `xcb_glx`, `xcb_egl`, Qt plugin search paths and `ldd`/loader availability. If file presence/loading remains ambiguous, a later isolated diagnostic may enable bounded `QT_DEBUG_PLUGINS=1` logging; no backend should be forced before that evidence exists.

Terminal markers:

```text
WINDOW_DIAG_CLASSIFICATION=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
WINDOW_DIAG_RESULT=PASS_DISCRIMINATOR_CAPTURED
WINDOW_DIAG_CLEANUP=COMPLETE
```
