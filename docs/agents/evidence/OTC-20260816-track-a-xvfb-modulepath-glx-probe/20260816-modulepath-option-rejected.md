# Track A Xvfb modulepath GLX discriminator — terminal evidence

## Exact execution

- PR: `#418`
- dispatch head: `201a2764ecc87faa53c2878402b69ac4cfe679c5`
- governance run: `31965191001 = SUCCESS`
  - Fresh admission behavior audit: `SUCCESS`
  - Deterministic admission-policy audit: `SUCCESS`
- semantic run: `31965191048`
- semantic job: `95209182706`
- runner: `synology-otclient-01`
- runtime access: `ephemeral_isolated`
- canonical state access: `NONE`
- official client/VNC/WARP started: `false`
- cleanup: `COMPLETE`

## Exact support fence

The task fenced the same contained server and support files used by the prior experiments:

```text
Xvfb=/work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb
Xvfb SHA-256=2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1
module root=/work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules
libglx=/work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
libglx SHA-256=373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
xkbcomp=/usr/bin/xkbcomp
xkbcomp SHA-256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
```

## Discriminator result

The isolated server was launched with the prior accepted environment plus:

```text
-modulepath /work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules
+extension GLX
```

It exited before creating an X11 socket. The bounded server output directly reported:

```text
Unrecognized option: -modulepath
Fatal server error:
(EE) Unrecognized option: -modulepath
```

The same built-in help output directly listed both:

```text
+iglx                  Allow creating indirect GLX contexts
-iglx                  Prohibit creating indirect GLX contexts (default)
+extension name        Enable extension
```

and included `GLX` among extensions that can be runtime enabled/disabled.

## Classification

`PROVEN_CONTAINED_XVFB_REJECTS_MODULEPATH_OPTION_GLX_MODULEPATH_CLI_HYPOTHESIS_DISPROVEN`

Directly proven:

- the exact contained Xvfb does not accept the Xorg-style `-modulepath` option;
- the failure occurs at argument parsing, before server/socket initialization;
- no conclusion about the loadability of the present `libglx.so` can be drawn from this failed CLI mechanism;
- `+extension GLX` and `+iglx/-iglx` are recognized by this Xvfb binary, consistent with prior static evidence;
- cleanup completed and no client/canonical runtime surface was touched.

This eliminates explicit modulepath injection as a valid correction for this Xvfb executable.

## Next discriminator

The next support-only step should identify the **actual GLX provider/software-renderer path** used by this statically GLX-aware Xvfb build. Perform a read-only fixed-root inventory for Mesa/GLVND/DRI components relevant to software GLX initialization, including exact locations and direct ELF dependencies for candidates such as:

- `libGL.so.1` / `libGLX.so.*` / `libGLX_mesa.so.*` / `libGLdispatch.so.*`;
- `swrast_dri.so` and its containing DRI directory;
- `libEGL_mesa.so.*`, `libgbm.so.*`, `libdrm.so.*` where present.

Do not start an X server or official client for that inventory. Only after exact paths are proven should a separately admitted Xvfb-only experiment alter one provider-search environment variable at a time.
