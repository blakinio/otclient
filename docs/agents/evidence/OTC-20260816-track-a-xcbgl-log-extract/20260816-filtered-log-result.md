# Track A XCB GL completed-log extraction — terminal evidence

## Source fence

Hosted extractor PR #412 consumed only the already-completed governance-compliant #410 physical job:

- source run: `31962559445`
- source job: `95202662909`
- source job status/conclusion: `completed / success`
- source task cleanup: `COMPLETE`
- extractor run: `31963247184`
- extractor job: `95204331959`
- extractor runner: GitHub-hosted Ubuntu 24.04
- physical client execution in this task: `false`
- canonical state access: `none`

The extractor independently fenced source job ID/run ID/status before downloading its Actions log.

## Filtered result

The Actions log yielded 11 retained allowlisted lines. They prove retained observations for:

- bundled `libqwayland-egl.so` metadata and `wayland-egl` key;
- bundled `QXcbIntegrationPlugin` class metadata already recorded by #410;
- successful loading of bundled TLS/QML plugins.

Crucially, **no retained line matched** any of the following xcb-gl-integration-specific terms:

- `xcbglintegrations`
- `libqxcb-glx-integration`
- `libqxcb-egl-integration`
- `xcb_glx`
- `xcb_egl`
- `Xcb GLX gl-integration`
- `Failed to initialize GLX`

## Correct interpretation

This is **not negative runtime proof** that Qt never scanned or loaded an XCB GL integration plugin. The source #410 harness reported `WINDOW_DIAG_CLIENT_LOG_TOTAL_LINES=426`, while the durable Actions output retained only bounded/sanitized portions of that task-owned `client.log`. The xcbglintegration-specific middle lines may therefore have existed in the private ephemeral client log and been omitted before the Actions log was persisted.

Classification:

`PROVEN_RETAINED_ACTIONS_LOG_HAS_NO_XCBGLINTEGRATION_SPECIFIC_OBSERVATION / RUNTIME_DISCOVERY_LOAD_INIT_STILL_UNKNOWN`

This closes the possibility of recovering the missing evidence from the already-retained Actions log without another physical observation. It does not justify a backend assumption or canonical bootstrap retry.

## Primary-source boundary for next evidence

Qt 6.9.3 `QXcbGlIntegrationFactory` constructs `QFactoryLoader` with subdirectory `/xcbglintegrations` and calls `qLoadPlugin` for the requested platform key. Qt 6.9.3 GLX initialization returns false immediately when the X server does not advertise the `xcb_glx` extension; if present, it requires GLX >= 1.3.

Therefore the next separately admitted physical discriminator should preserve the exact isolated startup surface but publish only a compact filtered trace covering:

1. `/xcbglintegrations` directory scan;
2. `xcb_glx` / `xcb_egl` metadata keys and load attempts;
3. GLX integration created/success/failure lines;
4. a read-only extension inventory of the same task-owned Xvfb display proving whether `GLX` is advertised;
5. cleanup completion.

It must not force GLX/EGL/RHI, access canonical state, or retry canonical bootstrap.
