# Track A historical login/session recovery — bounded accepted extract

Source PR: `#290` (`docs(tibia): persist Track A live-session login handover`)
Coordinator task: `OTC-20260815-track-a-promotion-coordination`
Classification: `ACCEPT_WITH_EDITS / REVALIDATION_REQUIRED`
Track: `official-client-re`
Runtime subject: official native Linux Tibia client only

## Promotion boundary

This file preserves only the historically successful, non-secret recovery procedure that remains useful for current Track A runtime revalidation. It does **not** prove that a current session is logged in, that the current upstream client has the same binary identity, or that old runtime addresses remain valid.

Current build-specific research fence remains:

```text
version mapping: 15.32.df7b29
size: 51965216
SHA-256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The version mapping is repository metadata for the digest/size pair. Every current live run must recheck the exact binary identity before using build-specific offsets.

## Historically successful sequence — REVALIDATION_REQUIRED

1. Use the official **native Linux** client only.
2. Use a task-owned isolated Linux GUI/runtime namespace and dedicated X display.
3. Verify the approved Track A SOCKS/WARP path before login; fail closed if confinement is not healthy.
4. Launch the client through the approved task-owned SOCKS/proxy path rather than treating an invasive debugger attach as the normal login mechanism.
5. Supply credentials only through protected runtime-secret inputs to the minimal login step. Never print, persist, artifact, screenshot, OCR, inspect or commit secret values.
6. Remove credential variables from the login helper environment immediately after the minimal credential-use step; persistent child/client/X/DBus/observer processes must not retain them.
7. GUI automation is permitted only for login/bootstrap where necessary. Historical recovery used OCR solely to locate character-selection row geometry; OCR was **not** semantic evidence for in-world state.
8. Activate the intended test character and verify progression structurally rather than inferring success from a click/key press.
9. Verify network confinement for the official client: expected task-local SOCKS path present, no direct client TCP, and no client UDP where the current approved login model requires those invariants.
10. Establish `IN_GAME` from decoded/structural world evidence. A running process, visible window, successful credential submission, socket existence or byte counters are insufficient by themselves.
11. After restart/relogin, reacquire a fresh PID, PIE base and runtime objects; never reuse transient process/session addresses.
12. Cleanup only task-owned processes, state, display/socket/port resources. Never delete pre-existing/shared X11 locks/sockets or touch Track B runtime state.

## Corrections retained from #290 and later review

- `Track A` is official-client reverse engineering; OTClient-to-Global compatibility is Track B.
- Historical character selection did use OCR as a bootstrap locator. Claims that the entire login flow was OCR-free are superseded.
- Socket existence or traffic deltas are not `IN_GAME` proof.
- A sent movement command is not proof of a coordinate change; movement/action evidence requires authoritative structural before/after state.
- `raw30` and similar decoded fields remain UNKNOWN until directly classified.
- Old string locations/message-path offsets are historical leads only and must not be promoted without exact-build rediscovery.
- Historical Oteryn repositories/runners/containers are not active Track A dependencies under the current repository isolation contract.

## Current consumer

Active Draft task `OTC-20260815-track-a-runtime-reacquisition` / PR `#303` may use this procedure only as revalidation input. Its own acceptance gate must independently prove fresh PID/PIE, structural world-state reacquisition, secret-free persistent child environments and task-owned namespace safety across restart/relogin.

## Remaining UNKNOWN

- current live login/session state;
- whether current protected login prerequisites are available to the active runtime task;
- restart/relogin reacquisition result;
- authoritative standalone player position;
- A3/A4 action parity.

No secret values, account identity, proprietary client bytes or authenticated screenshots are retained here.
