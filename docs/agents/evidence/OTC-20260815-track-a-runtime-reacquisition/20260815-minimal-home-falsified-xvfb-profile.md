# Track A RUNTIME minimal-HOME falsification and Xvfb-profile discriminator

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`

## Run #22 — minimal launcher HOME is not sufficient

Run `31888683076` / job `95021585746`, head `67a134e0561d9fc6a4401159d43c6158b1f75e30`, executed the bounded HOME hypothesis from `20260815-x11-home-state-discriminator.md`.

The workflow successfully:

- validated the source `launchermetadata.json` as the expected 2485-byte public launcher structure with no credential-like keys;
- copied only that metadata into task-local generation HOME;
- created a fresh empty task-local `.running` marker;
- exposed only the task-owned copied package through `packages/Tibia`;
- preserved bundled Qt precedence, software Qt Quick backend, exact client SHA, WARP/relay/Xvfb isolation and no-secret process markers.

The artifact proves the task-local HOME actually contained the reconstructed launcher state plus runtime caches. Nevertheless the display-wide X11 census again reported:

```text
client_gen_1_pid=32158
visible_window_count=0
```

Protected login remained skipped and no gameplay/economic side effect occurred.

Sanitized artifact:

```text
artifact_id=9247964896
zip_sha256=e4d0a26dcd0b29bc9ae40168463822307abc28f3e50e09e002df3ee99cdbc814
```

### Classification

`DISPROVEN` as a sufficient explanation: the absence of the two known non-package launcher files in isolated HOME does not explain the missing window. The task must not copy additional persistent HOME state without new evidence.

## Verified successful historical reference

Historical run `31730884814`, attempt 14, job `94785048338`, is terminal `SUCCESS` and reached probable world view for the exact fenced client. It used the already-existing Track A display `:98` and successfully resolved a visible `^Tibia$` window before login.

The Track A launcher workflow that establishes that persistent display uses this Xvfb profile:

```text
-screen 0 1920x1080x24
-xkbdir <toolroot>/usr/share/X11/xkb
-nolisten tcp
-noreset
```

Current task-local Xvfb `:115` instead derives from the older helper profile:

```text
-screen 0 1280x800x24
-xkbdir <toolroot>/usr/share/X11/xkb
+extension GLX
+iglx
+render
-nolisten tcp
-noreset
```

Both remain native Linux and isolated. The screen/profile difference is now the next bounded environmental discriminator after loader, bundled Qt, renderer, PID/title and minimal-HOME hypotheses have been tested.

## Next hypothesis

Recreate the **known-good Xvfb command profile** on the task-owned display `:115` only. Do not attach to, stop or reuse persistent display `:98`. Keep the exact client, task-local HOME, WARP/SOCKS, no-secret, structural baseline and cleanup gates unchanged.

If the exact Xvfb profile still yields zero visible windows, classify this hypothesis as disproven and move to a fresh bounded X-server/runtime discriminator rather than repeating HOME/renderer changes.
