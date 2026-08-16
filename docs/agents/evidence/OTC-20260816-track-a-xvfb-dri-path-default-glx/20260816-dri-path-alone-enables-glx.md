# Track A default-Xvfb `LIBGL_DRIVERS_PATH` minimality proof

## Exact execution

- PR: `#421`
- dispatch head: `082be738559dcb16ba342086cfc48fcc8c2d724d`
- governance run: `31965779562 = SUCCESS`
- semantic run: `31965779546`
- semantic job: `95210624747`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- official client/VNC/WARP started: `false`
- cleanup: `COMPLETE`

## Minimality question

PR #420 directly proved that the contained DRI path enables GLX when the Xvfb command line also contains `+extension GLX`. The current canonical worker uses neither setting. This run kept the current canonical worker's Xvfb arguments unchanged:

```text
-screen 0 1920x1080x24
-xkbdir <contained xkb root>
-nolisten tcp
-noreset
```

It did **not** pass `+extension GLX` and added only:

```text
LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
```

`LIBGL_ALWAYS_SOFTWARE`, `GALLIUM_DRIVER` and `MESA_LOADER_DRIVER_OVERRIDE` were explicitly unset.

## Direct result

```text
XVFB_DRI_DEFAULT_SERVER_STARTED=true
XVFB_DRI_DEFAULT_EXTENSION_COUNT=23
XVFB_DRI_DEFAULT_EXTENSIONS=BIG-REQUESTS,Composite,DAMAGE,DOUBLE-BUFFER,GLX,Generic Event Extension,MIT-SCREEN-SAVER,MIT-SHM,Present,RANDR,RECORD,RENDER,SECURITY,SHAPE,SYNC,X-Resource,XC-MISC,XFIXES,XINERAMA,XInputExtension,XKEYBOARD,XTEST,XVideo
XVFB_DRI_DEFAULT_GLX_PRESENT=true
XVFB_DRI_DEFAULT_GLX_MAJOR_OPCODE=150
XVFB_DRI_DEFAULT_RENDER_PRESENT=true
XVFB_DRI_DEFAULT_RENDER_MAJOR_OPCODE=139
```

The server log had 19 lines and no GLX/AIGLX/provider failure; the only allowlisted match was the ordinary non-fatal `xkbcomp` warning.

## Comparison

```text
accepted current-worker-shaped Xvfb without DRI path (#417 default):
  extension_count=22
  GLX=false

same current-worker-shaped Xvfb + contained LIBGL_DRIVERS_PATH (#421):
  extension_count=23
  GLX=true
  GLX opcode=150
```

Therefore explicit `+extension GLX` is **not required** for the causal repair.

## Classification

`PROVEN_LIBGL_DRIVERS_PATH_ALONE_ENABLES_GLX_UNDER_CURRENT_CANONICAL_XVFB_ARGUMENTS`

Directly proven:

- the current canonical Xvfb argument surface can expose GLX without adding a new server flag;
- the only required new graphics/provider input identified by these experiments is the contained `LIBGL_DRIVERS_PATH`;
- RENDER remains present;
- no official client or canonical runtime state was used;
- cleanup completed.

## Implementation consequence

The minimal hosted-only canonical-worker repair should **not** add `+extension GLX`. It should:

1. validate `$TOOL/usr/lib/x86_64-linux-gnu/dri` as a real contained directory;
2. validate `swrast_dri.so` exists and resolves below that directory/toolroot;
3. export `LIBGL_DRIVERS_PATH="$TOOL/usr/lib/x86_64-linux-gnu/dri"` only into the Xvfb environment;
4. preserve the existing Xvfb argument list exactly;
5. add deterministic tests for the fail-closed DRI/swrast contract and the Xvfb environment assignment;
6. perform no physical runtime work in the implementation PR.
