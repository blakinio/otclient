# Track A canonical artifact correction — 2026-08-13

## Scope

Repository: `blakinio/otclient`
Track: `official-client-re` / Track A
Runner: `synology-otclient-01`

This checkpoint corrects a false-positive interpretation of canonical run `31730884814`, job `94550846782`. It contains no credentials, account identifiers, session tokens, cookies, or proprietary client bytes.

## PROVEN — artifact inspection

The GitHub Actions artifact from run `31730884814` was directly downloaded and inspected:

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

Visual inspection of the three XWD frames proves:

```text
pre-login.xwd: Account Login dialog
select.xwd: "Your client version is too old. Please download the current client from the website or use the Tibia launcher."
world.xwd: "Update failed. Please reinstall Tibia to update your client."
```

Therefore the run did **not** reach Select Character and did **not** enter the game world.

The following markers from that run are insufficient/false-positive as world-entry evidence:

```text
TRACK_A_POST_LOGIN_CHANGED_PIXELS=34047
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=43660
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

The network observations from the same run remain valid only for the login/update-error process state:

```text
TRACK_A_LOCAL_SOCKS_ESTABLISHED=4
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
```

They must not be described as world-session network evidence.

## PROVEN — official manifest/runtime consistency

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

## INFERENCE — launcher/update boundary

The canonical Track A workflows launch `packages/Tibia/bin/client` directly. CipSoft's Linux documentation distinguishes the Tibia launcher from the installed client directory and instructs Linux users to start the top-level `Tibia` launcher, which checks for and installs client updates.

The next recovery experiment should therefore use the latest official Linux launcher tarball in a fresh Track A-owned launcher root, through the same WARP/SOCKS confinement, and allow the launcher to establish the currently accepted child package before any credential submission.

This is an inference until reproduced on `synology-otclient-01`.

## Structural consequence

Structural run `31731046581`, job `94560023155`, attached while the supposed world session was actually an update-error UI. Its lack of Worldmap records therefore does not falsify the historical exact-version Worldmap decode path.

Do not repeat blind Right/Left movement loops. On the next valid login, arm the structural observer before character activation/world load and require literal records of the form:

```text
REC x=<x> y=<y> z=<z> order=<...> raw28=<...> raw30=<...>
```

before claiming structural `IN_GAME`.

## Current claim state

```yaml
LOGIN_STATE: ACCOUNT_LOGIN_REJECTED_CLIENT_TOO_OLD
STRUCTURAL_SESSION_STATE: UNKNOWN
SELECT_CHARACTER: NOT_PROVEN
WORLD_ENTRY: NOT_PROVEN
PLAYER_POSITION: UNKNOWN
CURRENT_WORLD_SCREENSHOT: NONE
CURRENT_WORLD_RECORDS: NONE
```

## Rejected hypotheses

- `TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true` proves a rendered world — false.
- the `world.xwd` frame from run `31730884814` depicts the world — false; it depicts an update-failure dialog.
- failure to hit `0x19a8ea3` in run `31731046581` proves the Worldmap decoder is invalid — false; that run was not in-world.
- manifest-consistent reconstructed files prove the child package is accepted by the login service — false for the observed run.

## Exactly one next action

Run a credential-free Track A launcher recovery on `synology-otclient-01`: download/extract the latest official Linux launcher tarball through owned WARP/SOCKS, launch the top-level official `Tibia` launcher from its extracted working directory, allow it to update/install the client, and record the resulting child `packages/Tibia/bin/client` SHA-256/version before login.
