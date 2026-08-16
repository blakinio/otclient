# Track A Xvfb `LIBGL_DRIVERS_PATH` causal proof — terminal evidence

## Exact execution

- PR: `#420`
- dispatch head: `74650474e73f4418681a52c46bf524ba878a3080`
- governance run: `31965565693 = SUCCESS`
  - Fresh admission behavior audit: `SUCCESS`
  - Deterministic admission-policy audit: `SUCCESS`
- semantic run: `31965565953`
- semantic job: `95210097816`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- official client/VNC/WARP started: `false`
- cleanup: `COMPLETE`

## Exact support fence

```text
Xvfb=/work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
Xvfb SHA-256=2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
DRI root=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
swrast_dri.so -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
swrast SHA-256=c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388
xkbcomp=/usr/bin/xkbcomp
xkbcomp SHA-256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
```

## Single-variable experiment

The prior #417 explicit-GLX run used the same exact contained Xvfb environment and server arguments, including `+extension GLX`, but advertised 22 extensions with `GLX_PRESENT=false`.

This run explicitly unset other renderer/provider overrides:

```text
LIBGL_ALWAYS_SOFTWARE
GALLIUM_DRIVER
MESA_LOADER_DRIVER_OVERRIDE
```

and added exactly one provider variable:

```text
LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
```

## Direct result

The server started successfully and the same core-X11 query returned:

```text
XVFB_DRI_PATH_EXTENSION_COUNT=23
XVFB_DRI_PATH_EXTENSIONS=BIG-REQUESTS,Composite,DAMAGE,DOUBLE-BUFFER,GLX,Generic Event Extension,MIT-SCREEN-SAVER,MIT-SHM,Present,RANDR,RECORD,RENDER,SECURITY,SHAPE,SYNC,X-Resource,XC-MISC,XFIXES,XINERAMA,XInputExtension,XKEYBOARD,XTEST,XVideo
XVFB_DRI_PATH_GLX_PRESENT=true
XVFB_DRI_PATH_GLX_MAJOR_OPCODE=150
XVFB_DRI_PATH_RENDER_PRESENT=true
XVFB_DRI_PATH_RENDER_MAJOR_OPCODE=139
```

Compared with #417:

```text
#417 explicit +extension GLX, no LIBGL_DRIVERS_PATH:
extension_count=22
GLX_PRESENT=false

#420 explicit +extension GLX + contained LIBGL_DRIVERS_PATH:
extension_count=23
GLX_PRESENT=true
GLX opcode=150
```

The bounded Xvfb stderr had 19 total lines and no GLX/AIGLX error/provider line; the only filter match was the ordinary non-fatal `xkbcomp` warning.

## Classification

`PROVEN_CONTAINED_LIBGL_DRIVERS_PATH_CAUSALLY_ENABLES_GLX_ON_EXACT_XVFB`

Directly proven:

- the exact Xvfb/DRI provider fences pass;
- the contained DRI directory is a sufficient provider search path for this Xvfb to advertise GLX;
- adding only `LIBGL_DRIVERS_PATH` changes GLX from absent to present while RENDER remains present;
- the GLX major opcode becomes `150`;
- no official client, VNC, WARP or canonical runtime surface is involved;
- cleanup completed.

This is the first direct causal repair proof for the graphics prerequisite that blocked #415/#405. It does **not** yet prove that the official client will map a visible window, because that requires the separate hosted worker fix to reach trusted `main` followed by a fresh governance-compliant runtime validation.

## Next action

Implement a minimal **GitHub-hosted-only** trusted-worker repair that supplies the contained DRI root as `LIBGL_DRIVERS_PATH` to the canonical Xvfb process. The implementation must:

1. derive the DRI path only from the already validated selected contained toolroot;
2. require the directory and `swrast_dri.so` to remain contained below that root;
3. set `LIBGL_DRIVERS_PATH` only in the Xvfb environment unless existing worker architecture has a stricter shared support-environment abstraction;
4. add deterministic source/behavior contract tests proving the variable is present and bound to the selected toolroot DRI directory;
5. preserve all lease/bootstrap/Gate-B/credential/runtime fences;
6. perform no Synology/client/X11/VNC/network mutation in the implementation PR.

After coordinator promotion of the hosted repair, RUNTIME may be freshly redispatched from trusted `main`; do not reuse this ephemeral display or PID.
