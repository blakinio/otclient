# Track A isolated DRI-repair client revalidation — terminal evidence

## Exact execution

- PR: `#431`
- trusted base: `main@fa5b66b697d42c60515c5de48ea5e30135eadd0e`
- semantic workflow run: `31970703417`
- semantic job: `95222630271`
- governance run on semantic head: `31970703290 = SUCCESS`
- semantic head: `c5e6328c697a2f02590bc99d082bb340e1405b8d`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- immutable source harness blob: `1616edcc982be50ef2c95b8077160ec8fe9291fe`
- exact client: `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- cleanup: `COMPLETE`

Two earlier workflow invocations never crossed the runtime boundary. Runs `31970618113` / job `95222415652` and `31970677923` / job `95222564029` both refused in the immutable-source transformer with `DRI_REVALIDATION_REFUSED=XVFB_ENV_PATCH_SITE_COUNT:0`. They created no task namespace and started no Xvfb or client, so they are preflight failures rather than semantic physical executions. The transformer anchor was then repaired without changing runtime semantics.

## Admission and support fence

The successful run emitted:

```text
DRI_REVALIDATION_SOURCE_BLOB=PASS:1616edcc982be50ef2c95b8077160ec8fe9291fe
DRI_REVALIDATION_PATCH_COUNT=9
DRI_REVALIDATION_CANONICAL_STATE_ACCESS=NONE
DRI_REVALIDATION_RUNTIME_ACCESS=EPHEMERAL_ISOLATED
DRI_REVALIDATION_XVFB_NEW_INPUT=LIBGL_DRIVERS_PATH_ONLY
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
DRI_REVALIDATION_SUPPORT_FENCE=PASS
DRI_REVALIDATION_DRI_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
DRI_REVALIDATION_SWRAST_REAL=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
```

The generated client launch segment was checked before execution to ensure `LIBGL_DRIVERS_PATH` was absent. No `+extension GLX`, `QSG_RHI_BACKEND`, credentials, canonical registration/lease path or broad process inventory was admitted.

## Task-owned X11 result

The task-owned Xvfb used the accepted canonical-shaped argument list unchanged and received only the contained DRI provider path as the new graphics/provider input. Direct same-display core-X11 output was:

```text
DRI_REVALIDATION_X11_EXTENSION_COUNT=23
DRI_REVALIDATION_X11_GLX_PRESENT=true
DRI_REVALIDATION_X11_GLX_MAJOR_OPCODE=150
DRI_REVALIDATION_X11_RENDER_PRESENT=true
DRI_REVALIDATION_X11_RENDER_MAJOR_OPCODE=139
```

This independently reproduces the promoted support-only proof under the full isolated official-client startup surface: the contained DRI path is sufficient for this exact task-owned Xvfb to advertise GLX without adding `+extension GLX`.

## Exact-client/window result

The exact copied official client passed the executable fence and started in the task-owned namespace. Historical destroyed-namespace identifiers were:

```text
DISPLAY=:231
VNC_PORT=6200
CLIENT_PID=26972
CLIENT_PGID=26972
```

These values are evidence for this completed ephemeral run only; they are not current canonical authority.

Bounded snapshots:

```text
t+5s:  client_alive=true state=D visible_window_count=0
t+15s: client_alive=true state=R visible_window_count=0
t+35s: client_alive=true state=S visible_window_count=0
```

Final classification:

```text
WINDOW_DIAG_CLASSIFICATION=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
WINDOW_DIAG_RESULT=PASS_DISCRIMINATOR_CAPTURED
WINDOW_DIAG_CLEANUP=COMPLETE
```

Therefore the DRI-path repair fixes the directly observed Xvfb GLX prerequisite but does **not** by itself produce a visible official-client window in this bounded isolated startup.

## Qt graphics trace after GLX restoration

The complete `415`-line task-owned client log was scanned locally with an allowlist covering `xcbglintegrations`, `libqxcb-{glx,egl}-integration`, `QXcbIntegration`, `GLX`, `EGL`, `QRhi`, `Vulkan` and library-load failures/successes. `35` lines matched and were emitted in sanitized form.

The emitted trace directly proves:

- `libqxcb.so` loaded;
- the `xcbglintegrations` directory was scanned;
- `libqxcb-glx-integration.so` metadata/key `xcb_glx` was discovered;
- `libqxcb-glx-integration.so` loaded;
- the Vulkan library loaded;
- `Initializing QRhi Vulkan backend ...` occurred;
- numerous Qt Quick/QML libraries then loaded.

Unlike the earlier accepted no-GLX run `31964397523`, the complete allowlisted match set contained **no** `QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled`, no corresponding offscreen-surface failure, and no `QRhiGles2: Failed to create ...` line. This is bounded negative evidence about the complete configured allowlist scan, not proof that every possible GL/EGL context path succeeded.

## Classification

`PROVEN_DRI_PATH_RESTORES_XVFB_GLX_AND_REMOVES_PRIOR_ALLOWLISTED_QXCB_NO_GLX_EGL_FAILURE_BUT_EXACT_CLIENT_REMAINS_ALIVE_WITH_ZERO_VISIBLE_WINDOWS_THROUGH_35S`

Load-bearing conclusions:

1. The trusted contained DRI provider path is a real causal repair for the Xvfb GLX prerequisite.
2. The prior `neither GLX nor EGL are enabled` / GLES2 temporary-context failure signature is no longer present in the complete configured graphics-log match set.
3. The exact client still produces zero visible task-owned windows through 35 seconds while remaining alive.
4. Vulkan RHI initialization still occurs, so the remaining no-window cause lies beyond the already-repaired GLX availability prerequisite.
5. This run grants no canonical identity or mutation authority and does not authorize a canonical bootstrap retry.

## Next boundary

Do not repeat this physical experiment. The next investigation should consume this durable evidence and isolate the post-RHI/no-visible-window path without creating a second logged-in Global session and without treating historical display/PID values as current state. Canonical bootstrap remains governed separately and remains unauthorized by this evidence.