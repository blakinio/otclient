# Track A XCB GL integration plugin inventory — terminal evidence

## Scope

Read-only physical inventory on `synology-otclient-01`. No client launch, no canonical lease/registration/session access, no process mutation, credentials, login, gameplay or Track B access.

## Exact source fence

The installed package was resolved only after verifying the official exact client:

- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- source root: `/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia`
- trusted toolroot: `/work/_otclient_tibia_re_state/toolroot`

## First run — harness-only failure

Run `31961958668`, job `95201142094` reached the filesystem inventory but failed because `readelf` was absent on the runner. It also ran `ldd` without the canonical worker library path, so the initial package `libqxcb.so` missing-dependency list is not promoted as semantic evidence. No client was launched and no canonical state was accessed.

This was repaired by removing the unnecessary `readelf` dependency and running `ldd` with the exact canonical worker `LD_LIBRARY_PATH`:

`package/bin/lib : toolroot/usr/lib/x86_64-linux-gnu : toolroot/usr/lib/x86_64-linux-gnu/libproxy : toolroot/lib/x86_64-linux-gnu`

## Successful read-only inventory

- run: `31962017845`
- job: `95201280452`
- Track A governance: `31962018212 = SUCCESS`
- result: `PASS_READ_ONLY_INVENTORY`
- client launch: `false`
- canonical state access: `NONE`

Two `xcbglintegrations` directories are present:

- package: `bin/plugins/xcbglintegrations`
- toolroot: `usr/lib/x86_64-linux-gnu/qt6/plugins/xcbglintegrations`

Ten relevant plugin/platform shared objects were inspected under the canonical library path. **Total missing dynamic dependencies: 0.**

### Package plugins

1. `bin/plugins/platforms/libqxcb.so`
   - size `18712`
   - SHA-256 `f2fb869e9a358a78b3f6d574f9d54bd130adb57daf641d95688e3a7b86583e56`
   - `ldd` rc `0`, missing deps `0`

2. `bin/plugins/xcbglintegrations/libqxcb-glx-integration.so`
   - size `71960`
   - SHA-256 `6c9c91be781adb72f941f8a9f13971a4a0d9fd3a5242e2e09d2918b48781c9bc`
   - `ldd` rc `0`, missing deps `0`

No package-local `libqxcb-egl-integration.so` was found by the bounded inventory.

### Toolroot plugins

- `usr/lib/x86_64-linux-gnu/qt6/plugins/xcbglintegrations/libqxcb-egl-integration.so`
  - size `47728`
  - SHA-256 `adcdfdc73167767442f980c7ca8306e582af7edb3c633b32c3fe13bbfff0a23c`
  - missing deps `0`

- `usr/lib/x86_64-linux-gnu/qt6/plugins/xcbglintegrations/libqxcb-glx-integration.so`
  - size `72304`
  - SHA-256 `d7b61e1693e15e5167a6541f74d318d284933f927542c3151e28f769e0cf4ad5`
  - missing deps `0`

The toolroot also contains `libqxcb.so`, `libqeglfs.so`, and EGL device integration plugins; every inspected object reported `ldd` rc `0` and zero missing dependencies under the canonical library path.

## Plugin directory candidates

Package:
- `bin/plugins/platforms`
- `bin/plugins/xcbglintegrations`

Toolroot:
- `usr/lib/x86_64-linux-gnu/qt6/plugins/platforms`
- `usr/lib/x86_64-linux-gnu/qt6/plugins/xcbglintegrations`
- `usr/lib/x86_64-linux-gnu/cmake/Qt6/platforms` (directory-name inventory only; not promoted as a runtime plugin path)

## Classification

`PROVEN_XCB_GL_PLUGINS_PRESENT_AND_DEPS_RESOLVE_UNDER_CANONICAL_LD_PATH / DISCOVERY_OR_INITIALIZATION_REMAINS_UNKNOWN`

### PROVEN

- the exact package contains its own XCB platform plugin and a package-local GLX integration plugin;
- the trusted toolroot contains both Qt6 XCB EGL and GLX integration plugins;
- all inspected relevant shared objects resolve their dynamic dependencies under the exact canonical worker `LD_LIBRARY_PATH`;
- plugin/dependency file absence is therefore not a sufficient explanation for the runtime XCB message;
- no client launch or canonical-state access occurred.

### NARROWED / FALSIFIED

- blanket absence of XCB GL integration plugin files is falsified;
- missing ELF dependencies under the canonical library path are not observed for the inventoried plugin objects.

### UNKNOWN

- which XCB GL integration candidate the official client's Qt instance actually discovers;
- whether the package-local GLX plugin is rejected during metadata/load/initialization;
- whether toolroot Qt6 plugins are ABI-compatible with the official client's bundled Qt or are even in its plugin search path;
- whether GLX initialization fails because of the Xvfb/server capability rather than plugin loading;
- why Qt ultimately reports neither GLX nor EGL enabled.

## Next discriminator

Do not force a backend and do not retry canonical bootstrap. The next bounded, separately admitted `ephemeral_isolated` diagnostic should enable `QT_DEBUG_PLUGINS=1` together with existing `QSG_INFO=1` and capture only sanitized plugin discovery/load/initialization lines. It must use the same exact-client fence and task-owned isolated display, with no canonical state or credentials.
