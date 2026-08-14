# Track A canonical artifact correction — 2026-08-13

## Scope

Repository: `blakinio/otclient`
Track: `official-client-re` / Track A
Runner: `synology-otclient-01`

This checkpoint first corrected a false-positive interpretation of canonical run `31730884814`, job `94550846782`, then records the later verified recovery on the same workflow run, attempt 5, job `94617262508`. It contains no credentials, account identifiers, session tokens, cookies, or proprietary client bytes.

## PROVEN — original false-positive artifact inspection

The GitHub Actions artifact from the earlier attempt of run `31730884814` was directly downloaded and inspected:

```text
artifact: track-a-software-world-login
artifact_id: 9193205116
run: 31730884814
job: 94550846782
zip_digest: sha256:800399186a90600c4697b1c084ee7597bcb294032850b847dd45a82baa65f51c
files:
  pre-login.xwd
  select.xwd
  world.xwd
```

Visual inspection of the three XWD frames proved:

```text
pre-login.xwd: Account Login dialog
select.xwd: "Your client version is too old. Please download the current client from the website or use the Tibia launcher."
world.xwd: "Update failed. Please reinstall Tibia to update your client."
```

Therefore that earlier attempt did **not** reach Select Character and did **not** enter the game world.

The following markers from that earlier attempt were insufficient/false-positive as world-entry evidence:

```text
TRACK_A_POST_LOGIN_CHANGED_PIXELS=34047
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=43660
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

The network observations from the same earlier attempt remain valid only for the login/update-error process state:

```text
TRACK_A_LOCAL_SOCKS_ESTABLISHED=4
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
```

They must not be described as world-session network evidence.

## PROVEN — official manifest/runtime consistency before recovery

Run `31731327660`, job `94552288545`, fetched the then-current official package manifest through the Track A WARP path and reported:

```text
TRACK_A_CURRENT_PACKAGE_ENTRY_COUNT=1634
TRACK_A_CURRENT_CLIENT_URL=bin/client.lzma
TRACK_A_CURRENT_CLIENT_PACKED_SHA256=496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
TRACK_A_CURRENT_CLIENT_UNPACKED_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Run `31731640209`, job `94553277254`, compared the installed runtime against the then-current official package and asset manifests and reported:

```text
TRACK_A_INTEGRITY_CHECKED_FILES=8728
TRACK_A_INTEGRITY_MISSING_COUNT=0
TRACK_A_INTEGRITY_MISMATCH_COUNT=0
```

Thus local file corruption/missing reconstructed files was not established. The reconstructed child package matched the official manifests observed through the Track A WARP path while the login endpoint still rejected that child client as too old.

## PROVEN — launcher recovery and current package state

The stale launcher single-instance marker was identified as:

```text
/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/.running
```

Before removal, Track A verified that no owned Tibia/client process was alive and that the file was not held by an active `flock`. Removing only that stale marker allowed the official launcher to proceed.

The official launcher `--first-launch` recovery then completed package installation and reported:

```text
PackageVersion: 15.32.df7b29
Package Tibia with version 15.32.df7b29 is now fully installed
Changing local package status from "PartiallyInstalled" to "InstalledAndUsable"
Installation of package "Tibia" finished.
```

The installed child client remained:

```text
path: /work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
size: 51965216
```

This establishes that the recovery was a package/launcher installation-state correction rather than a change of the child `bin/client` bytes.

## PROVEN — verified real world entry after recovery

The historically credential-capable workflow was re-run only after the launcher recovery. The exact execution was:

```text
workflow run: 31730884814
run attempt: 5
job: 94617262508
job conclusion: success
artifact: track-a-software-world-login
artifact_id: 9201010176
artifact_size: 2693123
artifact_zip_digest: sha256:b2639a3c8ecfb901a0971b3846bc894262418e26e030855bb1826ef88e3d49e4
files:
  pre-login.xwd
  select.xwd
  world.xwd
```

The run produced the following runtime observations after credential submission and character activation:

```text
TRACK_A_SOFTWARE_BACKEND_CLIENT_RUNNING=true
TRACK_A_KNOWN_GOOD_LOGIN_CLICK_SENT=true
TRACK_A_POST_LOGIN_CHANGED_PIXELS=319236
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=660127
TRACK_A_LOCAL_SOCKS_ESTABLISHED=8
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

Unlike the original false-positive attempt, the new artifact `9201010176` was directly downloaded and its XWD frames were decoded and visually inspected.

The inspected frames establish:

```text
pre-login.xwd: Account Login state
select.xwd: actual Select Character screen; no "client too old" update-error dialog
world.xwd: actual in-game Tibia world viewport with the player character rendered on the map and normal in-game UI, including HP/mana UI, minimap, battle list and chat/server-log interface; no update-error dialog
```

Therefore the new evidence is not inferred from changed-pixel thresholds alone. The actual rendered frames prove that account login succeeded, Select Character was reached, a character was activated, and the official Linux client entered the real game world.

The network observation is also valid for this recovered world-entry execution:

```text
established SOCKS-path connections: 8
established direct TCP connections: 0
UDP sockets: 0
```

## PROVEN — reproducible successful login recipe

The successful execution used the existing workflow:

```text
.github/workflows/tibia-official-client-re-software-world-login.yml
workflow id: 333784548
successful run: 31730884814
successful attempt: 5
successful job: 94617262508
```

The procedure that actually succeeded was:

1. Use the persistent Track A state root `/work/_otclient_tibia_re_state` when available.
2. Require the exact official child client at `home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client` with SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
3. Require the existing Track A WARP/wireproxy process and verify `warp=on|plus` through SOCKS5 at `127.0.0.1:25354`.
4. Before login, ensure the official launcher/package state has already been recovered to `15.32.df7b29` / `InstalledAndUsable`. If launcher startup is incorrectly blocked while no Tibia process exists, inspect `home/.local/share/CipSoft GmbH/Tibia/.running`; remove it only after proving no owned Tibia/client process is alive and the file is not actively `flock`-locked, then complete official launcher `--first-launch` installation.
5. Clear only the Track A-owned `packages/Tibia/crashdump` contents before starting the child client.
6. Reuse the Track A X server on display `:98` and launch the exact child `bin/client` with persistent `HOME=$state/home`, software Qt rendering (`QT_QUICK_BACKEND=software`, `QT_XCB_GL_INTEGRATION=none`), the Track A toolroot/font paths, and the existing proxychains `LD_PRELOAD`/configuration so all network traffic remains on the owned SOCKS/WARP path.
7. Wait for the visible Tibia window and focus it.
8. On the 1020x650 Account Login UI used by the successful run, execute the exact observed input sequence:

```text
click email field:     (535,275)
Ctrl+A
enter TIBIA_TEST_EMAIL
click password field:  (535,304)
Ctrl+A
enter TIBIA_TEST_PASSWORD
click Login button:    (590,388)
```

9. Wait approximately 8 seconds for the Account Login screen to transition to Select Character. Do not treat changed-pixel count alone as proof; the successful artifact showed the actual Select Character screen.
10. On the successful Select Character screen, the workflow selected the first visible character row at `(285,193)`, then sent `Return`. In this exact successful attempt, that activated the selected character and entered the world. This records what actually succeeded; a future semantic/UI-controller implementation may replace the coordinate/Return mechanism with explicit character selection plus the dialog's `OK` action.
11. Wait approximately 15 seconds for world load.
12. Preserve and inspect `pre-login.xwd`, `select.xwd`, and `world.xwd`. A successful claim requires `select.xwd` to be the actual Select Character UI and `world.xwd` to show the actual in-game world, not an update/error dialog.
13. Verify the live client remains Track A-owned and network-confined. The successful run had `8` established SOCKS-path connections, `0` direct established TCP connections, and `0` UDP sockets.

Credentials are never stored in the repository. The workflow receives them only from the existing GitHub Actions secrets `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`, uses `set +x`, and unsets them after submission.

The historical rerun is important: creating/replacing other login workflows was not necessary for the final success. Re-running the already credential-capable workflow after repairing the launcher/package state was sufficient.

## Structural consequence

Structural run `31731046581`, job `94560023155`, attached during the earlier update-error state. Its lack of Worldmap records does not falsify the historical exact-version Worldmap decode path.

The verified visual world entry above is sufficient to establish `WORLD_ENTRY: PROVEN`, but it does **not** by itself prove the structural Worldmap callback/record decoder or exact player coordinates. A future structural validation should arm the observer against a verified in-world session and require literal records of the form:

```text
REC x=<x> y=<y> z=<z> order=<...> raw28=<...> raw30=<...>
```

before claiming structural position evidence.

Do not substitute blind movement loops, changed-pixel thresholds, socket counts, or UI heuristics for those structural records.

## Current claim state

```yaml
LOGIN_STATE: IN_GAME
ACCOUNT_LOGIN: PROVEN
SELECT_CHARACTER: PROVEN
CHARACTER_ACTIVATION: PROVEN
WORLD_ENTRY: PROVEN
CURRENT_WORLD_SCREENSHOT: PROVEN_BY_ARTIFACT_9201010176
WORLD_SESSION_TUNNELING: PROVEN_8_SOCKS_0_DIRECT_0_UDP
OFFICIAL_PACKAGE_VERSION: 15.32.df7b29
OFFICIAL_CLIENT_SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
STRUCTURAL_SESSION_STATE: UNKNOWN
CURRENT_WORLD_RECORDS: NONE
PLAYER_POSITION: UNKNOWN
```

## Rejected hypotheses and corrected conclusions

- `TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true` alone proves a rendered world — still false as a general rule; the current world-entry claim is based on direct inspection of artifact `9201010176` in addition to runtime markers.
- the `world.xwd` frame from the earlier artifact `9193205116` depicts the world — false; it depicts an update-failure dialog.
- artifact `9201010176` is the same false-positive state — false; direct inspection shows Select Character followed by the real in-game viewport.
- failure to hit `0x19a8ea3` in old structural run `31731046581` proves the Worldmap decoder is invalid — false; that run was not in-world.
- manifest-consistent reconstructed files alone prove the child package is accepted by the login service — false; launcher/package installation state also mattered in the observed recovery.
- exact player coordinates are known from the current visual proof — false; `PLAYER_POSITION` remains `UNKNOWN` until structural or otherwise authoritative position evidence is collected.

## Exactly one next action

Attach the structural Worldmap observer to a verified recovered in-world Track A session and require literal decoded `REC x=... y=... z=...` records before promoting `STRUCTURAL_SESSION_STATE` or `PLAYER_POSITION` from `UNKNOWN`.
