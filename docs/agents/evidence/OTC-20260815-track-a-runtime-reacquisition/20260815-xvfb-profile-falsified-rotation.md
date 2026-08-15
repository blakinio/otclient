# Track A RUNTIME known-good Xvfb-profile falsification and rotation boundary

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`  
Track: `official-client-re`

## Run #24 — exact known-good Xvfb profile is not sufficient

Runtime run `31888992382` / job `95022321212`, exact head `3327b8731e7c9babb53e9cc9c0f27428ede8ee5c`, executed the task-owned runtime with the bounded fixes proven in prior generations:

- exact official native Linux client SHA/size fence;
- task-local WARP/SOCKS path and no-secret process markers;
- official bundled Qt `bin/lib` ahead of toolroot support libraries;
- existing toolroot `libproxy` path containing `libpxbackend-1.0.so`;
- `QT_QUICK_BACKEND=software` and `QT_XCB_GL_INTEGRATION=none`;
- bounded minimal task-local launcher HOME (`launchermetadata.json`, fresh empty `.running`, task-local package link);
- task-local display `:115` using the historical successful Track A Xvfb profile `1920x1080x24 -nolisten tcp -noreset` without the prior `+extension GLX +iglx +render` flags.

The runtime successfully reached exact-client generation-1 launch:

```text
TRACK_A_UPSTREAM_WARP_VERIFIED=true
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415
TRACK_A_TASK_XVFB_VERIFIED=true display=:115
TRACK_A_RUNTIME_MINIMAL_HOME_READY generation=1
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1
TRACK_A_RUNTIME_ROLE_DISCOVERED role=client-gen-1
```

It then failed closed before login at:

```text
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
```

Sanitized artifact:

```text
artifact_id=9248039977
zip_sha256=b0babd8bcce36cb0b8cab736723f071968914b97921f13c6b154b8f1c24bcc7a
```

The artifact records:

```text
visible_window_count=0
```

and zero structural map records. The client log shows asset loading and task-local proxied HTTP traffic, so the exact client remained alive through meaningful startup work; there was simply no visible X11 window on the isolated display.

## Classification

`DISPROVEN as sufficient explanations for the missing visible window`:

1. missing `libpxbackend-1.0.so` search path;
2. toolroot Qt shadowing the official Qt 6.9 runtime;
3. Vulkan/RHI launch profile instead of software Qt Quick;
4. hidden/different X11 title or child-window PID (display-wide census found zero visible windows);
5. absence of the two known non-package launcher-state files in isolated HOME;
6. the task-local Xvfb screen size / GLX flag profile relative to the verified historical attempt-14 profile.

These negative results must not be repeated without a materially new hypothesis.

## Verified historical positive control

Historical run `31730884814`, attempt 14, job `94785048338`, is independently terminal `SUCCESS` for the same exact fenced client and runner. It produced a visible `^Tibia$` window, submitted the bounded login bootstrap, entered a probable world view, and proved `7` task/proxy-local established sockets with `0` direct established sockets and `0` client UDP sockets.

The final attempt 15 of that historical run failed and must not be substituted for attempt-14 success evidence.

## Next bounded discriminator — not yet executed

The strongest remaining environment difference is the **launch path/cwd/argv surface**:

- verified historical attempt 14 executed the client directly from its canonical path under `$HOME/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client` and used that package path as runtime cwd;
- current isolated generations keep the physical copied package at the task run root and expose it into task-local HOME through a symlink before launching from the physical run-root path.

A fresh session should test only this distinction by launching the same task-owned copied package *through the task-local canonical HOME package path/cwd* while retaining the exact SHA, bundled Qt, software renderer, Xvfb, SOCKS, no-secret and visible-window gates. It must not copy broader persistent HOME or reuse display `:98`.

If canonical HOME package-path launch still produces zero visible windows, classify that hypothesis as disproven and move to a fresh bounded X11/process/runtime isolation analysis rather than another GUI-tuning retry.

## Exact-head repository validation state

Current exact-head CI run `31888994157` is `FAILURE` solely because `Fast Checks / Syntax and workflow validation` failed in actionlint/shellcheck after `yamllint` passed. The reported findings are deterministic shell-style issues in the compact current workflow (SC2016/SC2251/SC2015/SC2318), not semantic runtime failures.

Before another runtime mutation, a fresh session must normalize those shell snippets without weakening task ownership, credential, cleanup or semantic gates, then rerun exact-head repository CI.

## Anti-stall rotation

This session has exceeded the repository's maximum repair cycles for one runtime-visible-window gate. The bounded evidence above is therefore a mandatory rotation boundary. No further runtime retry is authorized in this session. The task remains resumable on the same branch/PR by a fresh defect-isolation session.
