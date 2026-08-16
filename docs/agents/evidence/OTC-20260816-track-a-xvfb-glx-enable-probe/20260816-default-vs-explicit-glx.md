# Track A Xvfb GLX enable differential — terminal evidence

## Exact execution

- PR: `#417`
- workflow run: `31965041300`
- job: `95208804449`
- dispatch head: `6ade6bf38131a325935686c9766f1545afd196d9`
- governance run: `31965041248 = SUCCESS`
  - Fresh admission behavior audit: `SUCCESS`
  - Deterministic admission-policy audit: `SUCCESS`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- official client started: `false`
- VNC started: `false`
- WARP started: `false`
- cleanup: `COMPLETE`

Support fence passed for:

```text
Xvfb=/work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
Xvfb SHA-256=2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
xkbcomp=/usr/bin/xkbcomp
xkbcomp SHA-256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
```

## Differential

Both subruns used the same exact contained Xvfb, screen geometry, XKB root, library path and server flags. The only intended server-argument difference was explicit `+extension GLX` in the second subrun.

### Default Xvfb

```text
server_started=true
extension_count=22
GLX_PRESENT=false
GLX_MAJOR_OPCODE=0
RENDER_PRESENT=true
RENDER_MAJOR_OPCODE=139
```

The extension list contained:

`BIG-REQUESTS, Composite, DAMAGE, DOUBLE-BUFFER, Generic Event Extension, MIT-SCREEN-SAVER, MIT-SHM, Present, RANDR, RECORD, RENDER, SECURITY, SHAPE, SYNC, X-Resource, XC-MISC, XFIXES, XINERAMA, XInputExtension, XKEYBOARD, XTEST, XVideo`.

The bounded server log had 19 total lines and only one allowlist match: the ordinary `xkbcomp` non-fatal warning. No GLX/AIGLX/provider diagnostic was emitted.

### Explicit `+extension GLX`

```text
server_started=true
extension_count=22
GLX_PRESENT=false
GLX_MAJOR_OPCODE=0
RENDER_PRESENT=true
RENDER_MAJOR_OPCODE=139
```

The extension list was identical to the default case. The bounded server log again had 19 total lines and no GLX/AIGLX/provider diagnostic; the only allowlist match was the same `xkbcomp` non-fatal warning.

## Classification

`PROVEN_EXPLICIT_GLX_FLAG_DOES_NOT_ENABLE_GLX_ON_CURRENT_CONTAINED_XVFB_ENVIRONMENT`

Directly proven:

- the default contained Xvfb starts and does not advertise GLX;
- the same contained Xvfb also starts successfully with explicit `+extension GLX`;
- explicit `+extension GLX` does not change the extension count or list;
- `GLX` remains absent while `RENDER` remains present;
- there is no server-side GLX provider/init diagnostic in either bounded stderr stream;
- both task-owned server instances were torn down and the ephemeral namespace was cleaned.

This disproves the hypothesis that the missing extension is explained solely by the absence of a `+extension GLX` command-line flag.

## New frontier

Read-only PR #416 already proved the contained support tree has `libglx.so`, `libglamoregl.so`, contained `libGL.so.1`, and GLX-related code/diagnostics in the exact Xvfb binary. The accepted runtime launch and this differential do **not** pass an explicit Xorg `-modulepath` pointing to that contained module tree.

Therefore the next high-information discriminator is a separately admitted Xvfb-only support experiment using the same exact server environment plus an explicit contained module path:

```text
-modulepath /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules
+extension GLX
```

Compare its extension list and bounded server log against this terminal result. Do not launch the official client, VNC or WARP, and do not touch canonical runtime state.
