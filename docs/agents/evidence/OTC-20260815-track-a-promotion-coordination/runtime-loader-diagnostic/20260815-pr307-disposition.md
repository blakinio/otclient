# Coordinator disposition — PR #307 runtime loader diagnostic

Date: 2026-08-15
Programme: `OTCLIENT-TIBIA-RE`
Track: `official-client-re`
Source task: `OTC-20260815-track-a-loader-diagnostic`
Source Draft PR: #307
Source head: `229d4bdb4051ab707f436f3c1e1602712e76ecb5`
Disposition: `ACCEPT_WITH_EDITS`
Promotion authority: coordinator PR #300

## Exact client fence

```text
version mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux only
runner: synology-otclient-01
```

## Independently reviewed source evidence

- loader differential: run `31893811826`, job `95033921299`;
- Qt platform/plugin dependency check: run `31893939190`, job `95034223662`;
- support-state metadata only: run `31894272272`, job `95035023704`;
- source exact-head repository CI: run `31894342104`, `SUCCESS`;
- source review submissions: zero;
- source review threads: zero.

The coordinator inspected the workflow source and raw job logs rather than relying on the worker summary.

## Promoted FACT — current exact-client loader boundary

The exact client records ELF `RUNPATH $ORIGIN/lib`. Because the executable is `Tibia/bin/client`, the bundled client-owned dependency directory is `Tibia/bin/lib`. The package has no top-level `Tibia/lib` directory.

The historical literal environment replayed against the current mutable toolroot,

```text
LD_LIBRARY_PATH=$runtime/lib:$tool_lib
```

fails dependency resolution with `RC=127` because `libpxbackend-1.0.so` is unavailable on that path. It is therefore **DISPROVEN as a current launch fix** and must not be used as a positive oracle simply because an older run once used the same string.

The current PR #303-style loader path,

```text
$runtime/bin/lib
+ $toolroot/usr/lib/x86_64-linux-gnu/libproxy
+ $toolroot/usr/lib/x86_64-linux-gnu
+ $toolroot/lib/x86_64-linux-gnu
```

resolves the exact client dependency graph with `RC=0`, including the client-bundled Qt libraries and current toolroot GL/EGL/X11/libproxy dependencies.

**Coordinator classification:** base ELF dependency resolution is not the demonstrated cause of `client_gen_1_window_missing`. Removing bundled-Qt precedence or reverting blindly to the historical literal loader path is rejected.

## Promoted FACT — Qt platform/plugin bytes and dependency chains

The exact package contains:

```text
plugins/platforms/libqxcb.so
plugins/xcbglintegrations/libqxcb-glx-integration.so
```

Under the current loader fence, `ldd` returns `RC=0` for both plugin chains. The qxcb chain resolves client-bundled `libQt6XcbQpa.so.6`, `libQt6Gui.so.6`, `libQt6Core.so.6` plus required XCB/X11/EGL/GLX/OpenGL dependencies. The xcb GLX integration chain likewise resolves `RC=0`.

**Coordinator classification:** missing qxcb/GLX plugin files or unresolved base plugin dependencies are **DISPROVEN as the presently demonstrated isolated cause**. This does not prove that Qt successfully loads/initializes the plugins at runtime or creates a window.

## Accepted metadata-only candidate — NOT causal evidence

The sanitized metadata-only job verified the same exact-client fence and observed:

```text
.config: absent
.cache: present
.cache/CipSoft GmbH: directory, 4 files, 6937 aggregate bytes, mode 0755
```

The workflow did not read file contents or emit nested names. This state is a concrete persistent-HOME difference from the fresh task homes used by #303.

**Coordinator edit:** this is only an `UNKNOWN / metadata-only candidate`. It is not promoted as required state, safe-to-copy state, account-independent state, or a fix. Payload purpose and sensitivity remain unknown. Do not read/copy/import these payloads merely to make the experiment pass.

## Runtime consequence

After PR #303 run `31893122418` also falsified historical patched-Xvfb cwd as an isolated cause, the next high-information RUNTIME discriminator is:

1. launch only in the existing task-owned #303 namespace/display/ports and exact-client fence;
2. capture sanitized `QT_DEBUG_PLUGINS=1` runtime diagnostics;
3. inventory all X11 windows for the client, including mapped and unmapped windows, plus relevant X server extensions;
4. preserve zero credential leakage and existing cleanup/ownership fences;
5. do not read or copy canonical cache payloads unless a separate fail-closed sensitivity classification is authorized and the runtime diagnostics point to cache state as causal.

## Non-promoted / still UNKNOWN

This disposition does **not** prove:

- successful Qt platform initialization;
- visible or hidden Tibia window creation on isolated `:115`;
- login or IN_GAME state;
- restart/relogin stability;
- direct player XYZ;
- P1 live authority;
- any A3/A4 action path.

Source PR #307 is a Draft research source. Promotion copies only the bounded facts above into coordinator-owned evidence; no source workflow is required in canonical product/runtime code.
