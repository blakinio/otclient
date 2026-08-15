# Track A RUNTIME X11 / isolated-HOME discriminator

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`  
Track: `official-client-re`

## Current exact-build failure

Diagnostic run `31888421091` / job `95020972569`, head `15b71212bf2d61b50dc138fb9e6092af7c9e37aa`, preserved the current exact-client fence and used the already-repaired bundled Qt precedence plus software Qt Quick backend.

The protected login step was skipped. No credentials, movement or gameplay/economic effects were used.

Sanitized artifact:

```text
artifact_id=9247897222
zip_sha256=15955783d74d7d868d899aee3036d50de85d969f0a1c0f4c89c455fa0d917163
```

### FACT — no visible X11 window exists in the isolated generation

The artifact's display-wide census on task-owned display `:115` recorded:

```text
client_gen_1_pid=31052
visible_window_count=0
```

Therefore the repeated `client_gen_1_window_missing` result is not explained by a different window title or a child-window PID mismatch. There was no visible X11 window to select.

### FACT — isolated generation HOME contains only runtime caches

The task-local `home-gen-1` tree contained Qt/Mesa cache state created by the running client, but no `.local/share/CipSoft GmbH/Tibia` launcher/package state.

The same artifact reported the source Track A HOME shape without reading source file contents:

```text
source_tibia_root_exists=true
source_config_root_exists=false
source_tibia_nonpackage_files=2
source_tibia_nonpackage_dirs=3
```

## Existing repository evidence identifies the two non-package files

Historical Track A launcher-state inventory run `31750725357` / job `94615626331` completed `SUCCESS` on the same runner and identified exactly these files under the source Track A `$HOME/.local/share/CipSoft GmbH/Tibia` outside `packages/`:

```text
launchermetadata.json  size=2485
.running               size=0
```

The inventory sanitized and printed the metadata structure. `launchermetadata.json` contains public launcher/package manifest URLs and launcher/package descriptors; `.running` is empty. No separate `$HOME/.config/CipSoft GmbH` tree exists in the current source-HOME shape.

This evidence does not authorize copying the persistent source HOME wholesale. It supports a smaller reconstruction of non-secret launcher state in each task-local generation HOME.

## Verified historical successful world-entry reference

Run `31730884814` had multiple attempts. The final attempt 15 failed and must not be used as success evidence. However attempt **14**, job `94785048338`, is independently terminal `SUCCESS` and proves the exact fenced client did produce a visible `^Tibia$` window and enter a probable world view on the same runner.

Attempt-14 markers include:

```text
TRACK_A_SOFTWARE_BACKEND_CLIENT_RUNNING=true
TRACK_A_KNOWN_GOOD_LOGIN_CLICK_SENT=true
TRACK_A_POST_LOGIN_CHANGED_PIXELS=466099
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=660094
TRACK_A_LOCAL_SOCKS_ESTABLISHED=7
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

Its launch used the persistent Track A HOME and `QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none`.

## Bounded next hypothesis

Reconstruct only the minimum non-secret launcher-state surface in each task-local generation HOME:

1. fail-closed validate the current source `launchermetadata.json` as a 2485-byte JSON document with only the expected public launcher/package top-level structure and no credential-like keys;
2. copy that one metadata file into the task-local HOME;
3. create a fresh empty task-local `.running` marker rather than copying the source marker;
4. expose the already task-local copied package through task-local `packages/Tibia`;
5. retain the existing exact-client, visible-window, no-secret, WARP/SOCKS, structural baseline and cleanup gates.

Persistent HOME, cookies, sessions, account state and any unknown files remain out of scope. If this minimal state still yields zero visible windows, the HOME hypothesis is disproven and the next discriminator should compare the isolated X server/runtime environment rather than copy broader state.
