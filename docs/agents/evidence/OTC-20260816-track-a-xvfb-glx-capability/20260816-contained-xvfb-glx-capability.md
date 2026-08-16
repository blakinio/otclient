# Track A contained Xvfb GLX capability — terminal evidence

## Scope

Read-only support-filesystem inventory on `synology-otclient-01`. No X server, official client, canonical lease/registration/session, X11/VNC state, credentials, network/game/login state, Track B or historical PR #303 surface was observed or mutated.

## Executions

### Attempt 1 — harness failure

- run: `31964825329`
- job: `95208270559`
- result: `FAILURE / HARNESS_FAILURE`
- cause: host `file` command absent; subsequent external binutils path exited `127`
- useful bounded metadata before failure: exact Xvfb path/hash/size/owner only
- X server started: `false`
- client started: `false`

This is not semantic evidence about GLX capability and did not authorize any conclusion.

### Attempt 2 — self-contained read-only inventory

- run: `31964879003`
- job: `95208403843`
- result: `SUCCESS`
- parser: Python stdlib only
- X server started: `false`
- client started: `false`
- canonical state access: `NONE`

## Exact contained Xvfb

```text
path=/work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
sha256=2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
size=2064864
mode=755
uid=0
gid=0
ELF64 little-endian=true
machine=62 (x86_64)
```

The parsed dynamic section directly includes `libGL.so.1`, resolved inside the same contained toolroot:

```text
libGL.so.1 -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGL.so.1.7.0
```

Other recorded dependencies (`libXau`, `libXdmcp`, `libXfont2`, `libaudit`, `libc`, `libgcrypt`, `libm`, `libpixman-1`, `libselinux`, `libsystemd`, `libunwind`) also resolve within the fixed contained search roots used by this inventory.

## Direct GLX strings in Xvfb

The Xvfb binary contains 11 bounded GLX-related printable strings, including:

```text
+iglx                  Allow creating indirect GLX contexts
-iglx                  Prohibit creating indirect GLX contexts (default)
GLX: Initialized %s GL provider for screen %d
GLX: could not load software renderer
GLX: no usable GL providers found for screen %d
../../../../glx/glxcmds.c
../../../../glx/vndservermapping.c
```

This is direct binary-presence evidence that the contained Xvfb build includes GLX-related server code/diagnostics. It does not by itself prove that GLX successfully initializes on the runner.

## Contained Xorg GLX/glamor modules

The fixed module root exists:

`/work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules`

Two bounded candidates were found.

### `extensions/libglx.so`

```text
sha256=373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
size=310664
ELF64 little-endian=true
NEEDED libGL.so.1 -> contained libGL.so.1.7.0
NEEDED libc.so.6 -> contained libc.so.6
```

Its retained GLX strings include:

```text
../../../../glx/glxcmds.c
../../../../glx/glxdri2.c
GLX: Initialized %s GL provider for screen %d
GLX: could not load software renderer
GLX: no usable GL providers found for screen %d
```

### `libglamoregl.so`

```text
sha256=431437fee72a299a4c8b38f84eeb36aedf6e78b53a603956843377d536355acd
size=221600
ELF64 little-endian=true
NEEDED libc.so.6 -> contained libc.so.6
NEEDED libepoxy.so.0 -> contained libepoxy.so.0.0.0
NEEDED libgbm.so.1 -> contained libgbm.so.1.0.0
NEEDED libm.so.6 -> contained libm.so.6
```

## Classification

`PROVEN_CONTAINED_XVFB_HAS_GLX_SERVER_CODE_LIBGLX_MODULE_AND_CONTAINED_LIBGL_DEPENDENCY_RUNTIME_GLX_INITIALIZATION_UNPROVEN`

Directly proven:

- the exact contained Xvfb binary depends on contained `libGL.so.1`;
- the Xvfb binary contains GLX server diagnostics/options;
- contained `libglx.so` exists and its direct dependencies resolve in the fixed toolroot;
- contained `libglamoregl.so` exists and its direct dependencies resolve in the fixed toolroot.

Still unknown:

- why the #415 task-owned Xvfb display advertised no GLX extension;
- whether explicit `+extension GLX` changes the advertised extension state;
- whether GLX provider initialization succeeds or logs `could not load software renderer` / `no usable GL providers`;
- whether any resulting GLX availability would be sufficient for the official client to map a window.

## Next discriminator

The evidence justifies exactly one separately admitted **Xvfb-only** task-owned execution using the same contained Xvfb environment but adding explicit `+extension GLX`. It should:

1. start only task-owned isolated Xvfb on a fresh display;
2. capture Xvfb stderr;
3. query the same display through the X11 core protocol for extension list and GLX presence;
4. compare default vs explicit-GLX behavior only if both are produced within the same isolated support task;
5. clean up immediately.

Do **not** launch the official client, VNC or WARP for this discriminator. Do not access canonical runtime state and do not retry canonical bootstrap.
