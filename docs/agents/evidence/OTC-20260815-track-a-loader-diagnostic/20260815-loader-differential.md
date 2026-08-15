# Track A exact-client loader differential — 2026-08-15

Task: `OTC-20260815-track-a-loader-diagnostic`
Track: `official-client-re`
Consumer: PR #303 runtime reacquisition
Classification: `FACT / bounded negative discriminator`

## Exact fence

```text
client size: 51965216
client SHA-256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runner: synology-otclient-01
```

## Execution evidence

Workflow: `.github/workflows/tibia-official-client-re-loader-diagnostic.yml`
Run: `31893811826`
Job: `95033921299`
Head: `5e6df5fe39cdc2fdf0240eef8600483f727ec2d5`
Result: `SUCCESS`

The workflow did not launch the client, use credentials, signal processes, touch displays/ports or mutate Track A runtime state. It parsed the ELF directly with Python stdlib and used glibc `ld-linux-x86-64.so.2 --list` only for dependency resolution.

## ELF facts

Interpreter:

```text
/lib64/ld-linux-x86-64.so.2
```

The exact client has:

```text
RUNPATH $ORIGIN/lib
```

where `$ORIGIN` is the directory containing `bin/client`, so the bundled dependency directory is `bin/lib`.

The canonical package has no top-level `Tibia/lib` directory. The bundled Qt libraries are under `Tibia/bin/lib`. The current toolroot also contains Qt `6.4.2`, while the exact client/bundled library set is the client-owned build used for the `15.32.df7b29` fence.

## Loader cases

### Historical-style path expressed against today's mutable toolroot

```text
LD_LIBRARY_PATH=$runtime/lib:$tool_lib
TRACK_A_LOADER_CASE_RC=positive:127
```

It fails before a complete dependency graph can be produced:

```text
error while loading shared libraries: libpxbackend-1.0.so: cannot open shared object file
```

Therefore the old environment string cannot be replayed literally against today's toolroot and must not be treated as a current positive loader oracle.

### Current PR #303-style path

```text
LD_LIBRARY_PATH=$runtime/bin/lib:$toolroot/usr/lib/x86_64-linux-gnu/libproxy:$tool_lib
TRACK_A_LOADER_CASE_RC=current:0
```

It resolves the bundled Qt libraries from `Tibia/bin/lib`, including `libQt6Core.so.6`, `libQt6Gui.so.6`, `libQt6Qml.so.6`, `libQt6Quick.so.6`, `libQt6Widgets.so.6`, `libQt6WebEngineQuick.so.6` and related bundled libraries. It resolves `libEGL.so.1`, `libGLX.so.0`, `libOpenGL.so.0`, X11 and supporting system libraries from task toolroot, and the required libproxy backend directory is present.

The run emitted:

```text
TRACK_A_LOADER_CURRENT_STYLE_RC=0
TRACK_A_LOADER_DIFFERENTIAL_COMPLETE=true
```

## Disposition

**DISPROVEN as next launch fix:** removing the explicit `bin/lib` precedence or reverting blindly to the historical `runtime/lib:$tool_lib` environment.

The current loader environment is internally resolvable and correctly keeps the exact client's bundled Qt ahead of the toolroot Qt 6.4.2 set. The remaining `client_gen_1_window_missing` failure in PR #303 must be investigated above the base ELF dependency-resolution layer (for example Qt platform/plugin/runtime/X11 state), not by undoing the bundled-Qt loader fence.

This result does not prove GUI/window creation, login, structural world state or restart/relogin stability.
