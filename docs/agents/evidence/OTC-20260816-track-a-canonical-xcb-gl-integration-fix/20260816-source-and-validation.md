# Track A canonical XCB GL integration repair — source correlation and hosted validation

## Physical selector

Terminal isolated RUNTIME discriminator PR #398, run `31958546334`, job `95192878995`, proved the exact client remained alive for 35 seconds while the task-owned X11 display had zero visible windows at t+5/t+15/t+35. Its sanitized startup log reported:

```text
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
```

Asset loading and HTTPS startup activity still proceeded. Canonical registration/Gate B were not reached and no credentials/login were used.

## Trusted-worker selector

Before this repair the production canonical client launch explicitly set:

```text
QT_QUICK_BACKEND=software
QT_XCB_GL_INTEGRATION=none
```

This repair removes only `QT_XCB_GL_INTEGRATION=none`. It preserves `QT_QUICK_BACKEND=software`, exact-client identity, WARP/proxychains, lease/registration/Gate-B, process ownership, rollback and secret stripping. It does not force another XCB GL integration, Qt RHI backend, OpenGL implementation or graphics package.

## Official Qt 6.9.3 source correlation

Primary source: official `qt/qtbase` tag `v6.9.3`.

### `src/plugins/platforms/xcb/qxcbconnection.cpp`

Git blob: `e6d232d0ef95023e8b1586b706743fc7f01c3711`.

`QXcbConnection::glIntegration()` normally appends `xcb_glx` and `xcb_egl` to its candidate list. It reads `QT_XCB_GL_INTEGRATION` through `QString::fromLocal8Bit(qgetenv(...))`; when the value is `"none"_L1`, Qt clears that candidate list. With the variable absent, Qt is free to use its normal candidate-selection path.

### `src/plugins/platforms/xcb/qxcbintegration.cpp`

Git blob: `5066a079614efd00730ced3bdd206b7c1f815464`.

When `m_connection->glIntegration()` is unavailable, Qt emits the same warning classes observed physically for platform OpenGL context and offscreen-surface creation.

## Hosted semantic validation

Validated source PR: `#401`.

Corrected dedicated validator head: `780fb47791109751570800f7af2e7d6342e37379`.

Dedicated workflow run: `31959622751` = `SUCCESS`.

The split validator proved independently:

- worker shell syntax: PASS;
- XCB GL regression tests: PASS;
- canonical session tests: PASS;
- canonical transition tests: PASS;
- canonical guard tests: PASS;
- canonical lease tests: PASS;
- exact Qt 6.9.3 `qxcbconnection.cpp` / `qxcbintegration.cpp` Git blob fences: PASS;
- exact Qt source invariants for default `xcb_glx` / `xcb_egl`, environment lookup and `none` candidate clearing: PASS;
- exact observed `neither GLX nor EGL are enabled` warning-source correlation: PASS;
- routing boundary: `runtime_access:none`, physical E2E false.

An earlier validator generation failed only because it encoded stale/overly literal source spellings (`QStringLiteral` statements and `qgetenv` assignment shape) that differ from the actual Qt 6.9.3 implementation. The production worker change and all local regression/canonical tests were already green in that generation. The validator was corrected to the exact tagged source spellings; no production behavior changed between the failed and successful validator runs.

## Claim boundary

### PROVEN

- trusted worker previously forced `QT_XCB_GL_INTEGRATION=none`;
- official Qt 6.9.3 clears XCB GL integration candidates for that value;
- exact physical client log emitted the same warning classes Qt uses when no GL integration is available;
- the repaired worker no longer sets any `QT_XCB_GL_INTEGRATION` value;
- all existing canonical safety/identity/transition tests remain green.

### SOURCE-CORRELATED

- after the repair Qt 6.9.3 may execute its normal `xcb_glx` then `xcb_egl` candidate selection instead of being deterministically disabled by the worker.

### UNKNOWN UNTIL PHYSICAL RUNTIME

- which XCB GL integration, if any, is loadable in the exact runner/client environment;
- whether every plugin/library dependency is available;
- whether normal integration selection is sufficient for a visible Tibia window;
- whether a fresh canonical bootstrap can publish authoritative registration and pass Gate B.

## Promotion replay

The clean promotion branch replays the exact one-line production change plus the same regression test/evidence from trusted `main`, **without** the temporary semantic validator workflow. Final exact-head normal governance/CI remains the promotion gate.
