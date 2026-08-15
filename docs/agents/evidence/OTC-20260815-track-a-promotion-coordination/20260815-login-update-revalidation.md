# Track A login/update revalidation correction — 2026-08-15

Coordinator task: `OTC-20260815-track-a-promotion-coordination`
Track: `official-client-re`
Classification: `ACCEPT_AS_BOUNDARY_CORRECTION / REVALIDATION_REQUIRED`

## Scope

This note resolves the stale assumption that the historical PR #290 login procedure first requires acquisition of a newer official Linux child binary. It does not claim a current logged-in session and does not promote any transient runtime address.

## FACT — failed launcher recovery was an install-state problem, not proof of a newer binary

Historical recovery run `31742909649`, job `94590422368`, preserved artifact `9198061945` (`track-a-current-child-recovery`). Its `launcher.log` shows:

- the official launcher started through the verified Track A WARP/proxy path;
- it loaded the persistent launcher `package.json.version`;
- local package state changed `Tibia: Unknown -> NotInstalled`;
- launcher metadata downloads proceeded, including `clientoptions.json` and `assets.json`;
- no replacement child appeared during the bounded wait, so the recovery job failed closed.

Therefore that run proves only that this launcher invocation treated the package as `NotInstalled` and did not automatically install it. It is not evidence that WARP was broken, and it is not evidence that a newer child SHA existed.

## FACT — independent official-manifest reconstruction produced the exact fenced build

Historical reconstruction run `31745572204`, job `94599228206`, head `ada844b07165fb4c932383d5b17941293c4e19a6`, completed successfully from the official current Linux package/asset manifests through the verified Track A WARP path into an isolated candidate directory.

Verified output:

```text
TRACK_A_PACKAGE_ENTRY_COUNT=1634
TRACK_A_ASSET_ENTRY_COUNT=7094
TRACK_A_RUNTIME_RECONSTRUCTION_COMPLETE=true
TRACK_A_CANDIDATE_FILE_COUNT=8728
TRACK_A_CANDIDATE_TOTAL_BYTES=683565384
TRACK_A_CANDIDATE_CLIENT_SIZE=51965216
TRACK_A_CANDIDATE_CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CURRENT_CANDIDATE_RECONSTRUCTED=true
```

The reconstructed client therefore matched the existing exact-build fence rather than producing a different child identity.

## FACT — the same exact build was subsequently live in world

Later run `31806312967`, job `94785974126`, head `ff8ebc6e2c3a1604d90c2b0439b60af2258b578a`, completed successfully on `synology-otclient-01` with:

```text
EXPECTED_CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_FORWARD_STEP_SENT=true
TRACK_A_INVERSE_STEP_SENT=true
TRACK_A_EVENT_COUNTS=2,2,2
TRACK_A_STRIP_COUNTS=0,33,88
TRACK_A_FORWARD_CHANGED_PIXELS=146599
TRACK_A_INVERSE_CHANGED_PIXELS=150668
```

The workflow verified the exact client SHA before acting, verified the owned client and persistent structural observer were alive, then captured Worldmap strip records after one step and its inverse. This is direct evidence that the exact fenced build was operating in a live world session on 2026-08-14.

## DISPROVEN / SUPERSEDED

The following prior working assumption is superseded:

> A `too old` / `NotInstalled` result from the earlier recovery means Track A must first replace `bin/client` with a newer SHA before login/session revalidation.

The evidence above does not support that conclusion. The same exact SHA was reconstructed from the official manifest channel and later observed live in world.

## Current promotion boundary

- Keep the exact client fence at SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, size `51965216`, until a future task independently proves a different current build identity.
- Do not reuse transient PID, PIE base, object addresses or debugger state from the historical runs.
- PR #303 / `OTC-20260815-track-a-runtime-reacquisition` remains responsible for a fresh task-owned restart/relogin proof using its own namespace and its own exact-build verification.
- The historical reconstruction utility is evidence that a fail-closed manifest reconstruction path exists; it is not automatically promoted into the current runtime task and must not be copied into another lane without ownership review.
- Current live login/session state remains UNKNOWN until the serialized self-hosted runtime lane executes the active revalidation work.

## Current scheduling blocker

At coordinator review time on 2026-08-15, P0 run `31880617510` for PR #302 remained `queued` in the shared serialized Track A runtime lane. PR #303 is intentionally waiting behind that lane and must not cancel, bypass or overlap it.

## Required next runtime action

When the serialized runtime lane is available, PR #303 should revalidate the existing exact fenced build directly: fresh task-owned launch/login, fresh PID/PIE, structural world-state reacquisition, secret-free persistent process environments, and safe task-owned cleanup. A new client acquisition step is not a prerequisite unless that run independently proves an exact-build mismatch or rejection.