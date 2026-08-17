# Track A QT_DEBUG_PLUGINS discriminator — terminal evidence

## Exact run

- PR: `#410`
- head at dispatch: `bd19c3e927c252b3a00f7a065bd0d9683ba89e3b`
- semantic workflow: `31962559445`
- job: `95202662909`
- governance: `31962559402 = SUCCESS`
- runner: `synology-otclient-01`
- base: `main@a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`

## Admission and isolation

The immutable accepted #398 startup harness blob `1616edcc982be50ef2c95b8077160ec8fe9291fe` was fenced and exactly three transformations were applied: nounset-safe snapshot declaration, current task ownership marker, and graphics environment replacement adding `QSG_INFO=1` plus `QT_DEBUG_PLUGINS=1` while removing `QT_XCB_GL_INTEGRATION=none` and preserving `QT_QUICK_BACKEND=software`.

Direct run markers:

```text
QTPLUG_DIAG_SOURCE_BLOB=PASS:1616edcc982be50ef2c95b8077160ec8fe9291fe
QTPLUG_DIAG_PATCH_COUNT=3
QTPLUG_DIAG_CANONICAL_STATE_ACCESS=NONE
QTPLUG_DIAG_ENV=QT_QUICK_BACKEND_software,QSG_INFO_1,QT_DEBUG_PLUGINS_1
WINDOW_DIAG_ADMISSION=EPHEMERAL_ISOLATED_MUTATION_AUTHORIZED
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
WINDOW_DIAG_WARP=PASS
WINDOW_DIAG_XVFB=PASS
WINDOW_DIAG_VNC=PASS
WINDOW_DIAG_CLIENT_START=PASS
WINDOW_DIAG_CLEANUP=COMPLETE
```

No account credentials, login, gameplay, canonical lease/registration/session state or Track B surface was used.

## Bounded runtime state

Exact client PID `25426` / PGID `25426` remained alive at t+5, t+15 and t+35. The isolated display `:231` had zero visible windows at all three snapshots.

```text
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0   # t05
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0   # t15
WINDOW_DIAG_VISIBLE_WINDOW_COUNT=0   # t35
WINDOW_DIAG_CLASSIFICATION=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
```

## QT_DEBUG_PLUGINS — directly proven

The bundled Qt plugin loader scans the copied official package's platform plugin directory:

```text
qt.core.plugin.factoryloader: checking directory path ".../Tibia/bin/plugins/platforms" ...
```

It directly inspects the package's `libqxcb.so`, extracts valid Qt platform plugin metadata and obtains key `xcb`:

```text
qt.core.plugin.factoryloader: looking at "libqxcb.so"
qt.core.plugin.loader: Found metadata in lib .../Tibia/bin/plugins/platforms/libqxcb.so
"IID": "org.qt-project.Qt.QPA.QPlatformIntegrationFactoryInterface.5.3"
"className": "QXcbIntegrationPlugin"
"Keys": [ "xcb" ]
qt.core.plugin.factoryloader: Got keys from plugin meta data QList("xcb")
```

The same bounded log proves Qt successfully loads other bundled plugins (for example TLS and QML plugins), so the general plugin loader is operating rather than globally disabled.

## What this run does NOT directly prove

The job log contains 426 sanitized client lines and the connector rendering elided a middle region. The available retained output does **not** directly show the `xcbglintegrations` directory scan, `libqxcb-glx-integration.so`/`libqxcb-egl-integration.so` load attempt, or their exact initialization result. Those remain `UNKNOWN` from this run and must not be inferred from the platform-plugin discovery alone.

## Classification

`PROVEN_BUNDLED_QXCB_PLATFORM_PLUGIN_DISCOVERED_METADATA_VALID / XCBGLINTEGRATION_DISCOVERY_LOAD_INIT_UNKNOWN`

Together with #408/#409 this narrows the frontier:

- package/toolroot XCB GL integration plugin files exist: PROVEN;
- their dependencies resolve under canonical `LD_LIBRARY_PATH`: PROVEN;
- bundled platform `libqxcb.so` is discovered and metadata-valid: PROVEN;
- exact xcbglintegration discovery/load/init sequence: UNKNOWN;
- visible window: still absent through 35 seconds.

## Next discriminator

Use one separately admitted ephemeral-isolated diagnostic that preserves the same exact startup surface but emits a **filtered plugin log only** for `xcbglintegrations`, `libqxcb-glx-integration`, `libqxcb-egl-integration`, `Cannot load library`, `loaded library`, `QXcbIntegration`, GLX/EGL and QRhi lines. Do not force a backend and do not retry canonical bootstrap.
