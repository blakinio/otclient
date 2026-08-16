# Track A canonical XCB GL integration repair — source correlation

## Physical selector

Canonical RUNTIME v6 and the terminal isolated window discriminator established the following current boundary:

- final isolated run: `31958546334`, job `95192878995`;
- exact client stayed alive for 35 seconds;
- visible X11 windows at t+5/t+15/t+35: `0 / 0 / 0`;
- startup reached asset loading and HTTPS activity;
- sanitized log contained:
  - `QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled`;
  - `QRhiGles2: Failed to create temporary context`;
  - `QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled`;
  - `QRhiGles2: Failed to create context`.

Terminal physical evidence is persisted in:
`docs/agents/evidence/OTC-20260816-track-a-client-window-ownership-discriminator/20260816-final-no-visible-window-gl-context.md`.

## Trusted-worker override

Before this repair, the canonical client launch environment explicitly contained both:

```text
QT_QUICK_BACKEND=software
QT_XCB_GL_INTEGRATION=none
```

The repair removes only `QT_XCB_GL_INTEGRATION=none`. It preserves `QT_QUICK_BACKEND=software` and does not force a replacement XCB integration, RHI backend, OpenGL implementation or new graphics package.

## Official Qt 6.9.3 source correlation

Primary source: official `qt/qtbase` tag `v6.9.3`.

### `src/plugins/platforms/xcb/qxcbconnection.cpp`

Git blob: `e6d232d0ef95023e8b1586b706743fc7f01c3711`.

`QXcbConnection::glIntegration()` initializes the candidate list as:

```text
xcb_glx
xcb_egl
```

It then reads `QT_XCB_GL_INTEGRATION`. For value `none`, Qt clears the candidate list. For another non-empty value, Qt restricts loading to that named integration. Without the variable, Qt retains its normal candidate order and attempts to load the available integrations.

Therefore `QT_XCB_GL_INTEGRATION=none` is not merely a hint: it deterministically prevents Qt's XCB platform plugin from selecting either built-in candidate name.

### `src/plugins/platforms/xcb/qxcbintegration.cpp`

Git blob: `5066a079614efd00730ced3bdd206b7c1f815464`.

`QXcbIntegration::createPlatformOpenGLContext()` obtains `m_connection->glIntegration()`. If it is null, Qt emits:

```text
Cannot create platform OpenGL context, neither GLX nor EGL are enabled
```

`QXcbIntegration::createPlatformOffscreenSurface()` follows the same pattern and emits:

```text
Cannot create platform offscreen surface, neither GLX nor EGL are enabled
```

Those are the same warning classes observed in the exact physical client log.

## Claim boundary

### PROVEN / exact trusted-worker behavior

- the trusted canonical worker explicitly forced `QT_XCB_GL_INTEGRATION=none` before this repair;
- official Qt 6.9.3 source clears the `xcb_glx`/`xcb_egl` candidate list for that value;
- the physical client emitted the exact Qt warning classes used when `glIntegration()` is unavailable;
- the repair removes only the deterministic disabling override.

### SOURCE-CORRELATED

- after removal, Qt 6.9.3 is allowed to try its normal XCB GL integration candidate selection instead of being forced to `none`.

### UNKNOWN UNTIL PHYSICAL VALIDATION

- whether `xcb_glx` or `xcb_egl` is present/loadable in the exact client/runtime environment;
- whether the runner/toolroot provides every dynamic dependency needed by the selected integration;
- whether enabling Qt's normal integration selection is sufficient to map a visible Tibia window;
- which integration, if any, is selected in the eventual canonical runtime.

## Safety and routing

This repair is `github_hosted`, `runtime_access:none`, no physical E2E. It does not change exact-client identity, lease/registration/Gate-B rules, WARP, process ownership, secret stripping, login authority or Track B. Physical proof belongs only to a fresh admitted RUNTIME attempt after promotion to trusted `main`.
