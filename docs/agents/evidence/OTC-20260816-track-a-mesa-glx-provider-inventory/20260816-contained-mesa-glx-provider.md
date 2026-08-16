# Track A contained Mesa/GLVND/DRI provider inventory — terminal evidence

## Exact execution

- PR: `#419`
- dispatch head: `c4d4d3b06e8944863b91667491f3e2cf303d71e1`
- governance run: `31965397320 = SUCCESS`
  - Fresh admission behavior audit: `SUCCESS`
  - Deterministic admission-policy audit: `SUCCESS`
- semantic run: `31965397353`
- semantic job: `95209684373`
- runner: `synology-otclient-01`
- runtime access: `read_only`
- parser: Python stdlib only
- X server/client started: `false`
- canonical state access: `NONE`

## Load-bearing provider stack

The fixed contained toolroot has a complete direct GLVND/Mesa surface for the inspected candidates.

### GLVND core

```text
libGL.so.1 -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGL.so.1.7.0
sha256=67f471213576d225d38347a0b6d2a08a231980685301ff6461bd74d3994e5027
missing direct deps=0

libGLX.so.0 -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGLX.so.0.0.0
sha256=16fc8a37eea9210dc83c57eeff5aedc10ab4c6673f2f97e8bb6ee103df657b40
missing direct deps=0

libGLdispatch.so.0 -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGLdispatch.so.0.0.0
sha256=ca01a91104c8887b3d8e59499b58cbb8f604cc285666b50d9ec888eb0c915182
missing direct deps=0
```

`libGLX.so.0` contains the vendor-loading shape `libGLX_%s.so.0`, `__GLX_VENDOR_LIBRARY_NAME` and `__GLX_FORCE_VENDOR_LIBRARY_%d`.

### Mesa GLX vendor

```text
libGLX_mesa.so.0 -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libGLX_mesa.so.0.0.0
sha256=409f932670504cc5829c7526db466eb69a6b7f9997fd5df8afc8dfb1588278c2
missing direct deps=0
```

Its direct dependencies all resolve inside the fixed contained roots, including X11/XCB, DRM and `libgallium-25.2.8-0ubuntu0.24.04.2.so`. Retained strings include `swrast`, `DRI_SWRastLoader` and Mesa GLX entry points.

### Xorg GLX server module

```text
/work/_otclient_tibia_re_state/toolroot/usr/lib/xorg/modules/extensions/libglx.so
sha256=373b75559ee9a17449dfb84871bb7e5e306da7bd3aecd3282c7f03831ccf961a
missing direct deps=0
```

Its bounded strings directly include:

```text
DRI_SWRast
swrast
DRISWRAST
DRI_SWRastLoader
LIBGL_DRIVERS_PATH
__driDriverGetExtensions
GLX: no usable GL providers found for screen %d
GLX: Initialized %s GL provider for screen %d
GLX: could not load software renderer
AIGLX error: dlopen of %s failed (%s)
AIGLX error: unable to load driver %s
AIGLX: Loaded and initialized %s
```

The literal `LIBGL_DRIVERS_PATH` is the key new causal input: it proves this GLX server code has an explicit DRI provider search-path override.

### Software DRI provider

The fixed DRI root exists:

`/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri`

`swrast_dri.so`, `kms_swrast_dri.so`, `zink_dri.so`, `radeonsi_dri.so`, `iris_dri.so` and `nouveau_dri.so` resolve to the same contained `libdril_dri.so` target in this Mesa package layout.

For the software path:

```text
swrast_dri.so -> /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri/libdril_dri.so
sha256=c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388
size=117064
missing direct deps=0
```

Retained strings include `__driDriverGetExtensions_swrast`, `__driDriverGetExtensions_kms_swrast` and `DRI_SWRast`.

### EGL/GBM support

`libEGL_mesa.so.0`, `libgbm.so.1`, `libdrm.so.2`, `libdrm_amdgpu.so.1` and the observed LLVM runtime are present with zero missing direct dependencies in the fixed roots. The GLVND vendor manifest also exists:

```text
/work/_otclient_tibia_re_state/toolroot/usr/share/glvnd/egl_vendor.d/50_mesa.json
library_path=libEGL_mesa.so.0
```

## Classification

`PROVEN_CONTAINED_MESA_GLVND_SWRAST_PROVIDER_STACK_PRESENT_DIRECT_DEPS_COMPLETE_LIBGL_DRIVERS_PATH_IS_SUPPORTED_OVERRIDE`

Directly proven:

- GLVND core libraries are present and directly dependency-complete in the contained roots;
- `libGLX_mesa.so.0` is present and directly dependency-complete;
- Xorg `libglx.so` is present and directly dependency-complete;
- software DRI provider `swrast_dri.so` is present in an exact contained DRI directory and directly dependency-complete;
- `libglx.so` explicitly contains `LIBGL_DRIVERS_PATH` and software-renderer/provider diagnostics;
- no missing direct ELF dependency was found among the load-bearing inspected components.

This materially weakens the hypothesis that GLX is absent because the software provider files themselves are missing. It instead makes **provider search-path resolution** the next bounded runtime discriminator.

## Next discriminator

Run one separately admitted Xvfb-only experiment using the same exact contained server environment as #417, with no client/VNC/WARP/canonical state, adding exactly:

```text
LIBGL_DRIVERS_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/dri
```

Keep `+extension GLX` as in the already-falsified #417 explicit-GLX case so the single new variable is the DRI provider search path. Capture:

- core-X11 GLX/RENDER presence;
- bounded Xvfb stderr for `GLX`, `AIGLX`, `swrast`, `renderer`, `dlopen`, `driver` and provider initialization diagnostics.

Do not set `LIBGL_ALWAYS_SOFTWARE`, `GALLIUM_DRIVER`, `MESA_LOADER_DRIVER_OVERRIDE` or other renderer/backend overrides in the same experiment; each would be a separate hypothesis.
