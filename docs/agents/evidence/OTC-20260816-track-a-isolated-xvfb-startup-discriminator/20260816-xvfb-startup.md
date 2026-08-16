# Track A isolated Xvfb startup discriminator — 2026-08-16

## Scope

One ephemeral-isolated Xvfb-only process on `synology-otclient-01`, using the exact contained binary/environment/arguments used by the trusted canonical worker. No official client, x11vnc, xdotool action, WARP, canonical lease/registration/session, game network/login or credentials were used.

## Exact execution

- run: `31954834760`
- job: `95183766554`
- runner: `synology-otclient-01`
- display: `:199`
- binary: `/work/_otclient_tibia_re_state/toolroot/usr/bin/Xvfb`
- binary SHA-256: `2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1`
- dynamic-library missing count: `0`
- result: `FAIL_EXACT_INVOCATION`

The Xvfb process exited with code `1` before creating `/tmp/.X11-unix/X199`.

## Exact stderr discriminator

```text
sh: 1: /usr/bin/xkbcomp: not found
sh: 1: /usr/bin/xkbcomp: not found
XKB: Failed to compile keymap
Keyboard initialization failed. This could be a missing or incorrect setup of xkeyboard-config.
(EE)
Fatal server error:
(EE) Failed to activate virtual core keyboard: 2(EE)
```

Classification:

`PROVEN_XVFB_START_FAILURE_XKBCOMP_ABSOLUTE_PATH_MISSING`

This falsifies missing shared-library hypotheses for this invocation (`ldd` missing count is zero) and localizes the failure to XKB keymap compilation before the X11 socket becomes usable.

## Upstream source correlation

Xorg server source uses two distinct XKB directories:

- `XkbBaseDirectory = XKB_BASE_DIRECTORY` for XKB data;
- `XkbBinDirectory = XKB_BIN_DIRECTORY` for helper executables.

The XKB loader constructs the helper command from `XkbBinDirectory + xkbcomp`; therefore `-xkbdir`/XKB data-path selection does not itself redirect the helper binary path. This source correlation matches the observed absolute `/usr/bin/xkbcomp` execution failure. The exact packaged build's compile-time value is established directly by the runtime error above, not inferred from source alone.

## Cleanup / safety

The diagnostic process was task-owned and isolated on a high display. It exited before socket creation. The one-shot workflow was removed immediately after evidence capture. No canonical runtime state was created or changed.

## Next discriminator

Read-only support inventory should check only:

- `/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp`;
- `/usr/bin/xkbcomp`;
- relevant package metadata if present.

If a package-verified contained `xkbcomp` already exists, the repair should satisfy the exact absolute helper path without weakening the canonical worker's data/tool containment. If it does not exist, the missing support package becomes an explicit runner-support dependency rather than a reason to retry canonical bootstrap.
