# 2026-08-26 current-build encrypted handoff and game 0x14 checkpoint

Task: `OTC-20260813-tibia-global-login-lab`
Track: `OTCLIENT-GLOBAL-LOGIN` / Track B only
Canonical PR: #284
Repository: `blakinio/otclient`

## Fresh source-of-truth snapshot

At the start of this bounded continuation:

- live `main`: `8085b40698d409bbacba3460001e8ddca4f6c84f`;
- pre-repair PR #284 head: `be5c4499c4d4be41d988ed84689e24593576a76b`;
- PR #284 was open, Draft and mergeable;
- Molehill was online and command-executable;
- Synology remained offline;
- no Track A path/runtime/process was mutated.

Do not reuse these SHAs as later live state without resolving them again.

## Root cause of hosted login `errorCode=7`

A fresh secret-free WARP probe of the official current Linux package manifest proved that the producer's hard-coded HTTP `clientversion` was stale:

```text
stale producer clientversion: 15.32.bf29ac
current public clientversion: 15.32.75d4a0
```

This was a concrete request-identity drift, not an inferred account-state mapping for code 7.
The current official binary fence was then re-read through WARP without credentials:

```text
version:        15.32.75d4a0
packed_sha256:  075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked_sha256:d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked_size:  52105824
```

TDD first made the encrypted-handoff contract fail on the stale literal. Commit
`808e72e2410831ba12c2c844f9612795d1400237` (`fix(track-b): resolve current login build dynamically`) then changed the producer to fetch the current public package manifest through the same WARP session, require `15.32.<6 hex>`, and pass that value into the login request. Contract, shell syntax, diff-check and checkpoint validation passed before push.

## Encrypted producer — PROVEN

Exact-head workflow run `32969694447`, handoff job `98180313204`, completed successfully. Sanitized markers were:

```text
LAB_ENCRYPTED_HANDOFF_WARP_READY=true
LAB_ENCRYPTED_HANDOFF_CLIENT_VERSION_CURRENT=true
LAB_ENCRYPTED_HANDOFF_ASSET_IDENTIFIER_READY=true
LAB_ENCRYPTED_HANDOFF_HTTP_LOGIN_200=true
LAB_ENCRYPTED_HANDOFF_PLAINTEXT_VALID=true
LAB_ENCRYPTED_HANDOFF_CIPHERTEXT_READY=true
```

The legacy full login-lab workflow was skipped by its canonical-branch guard.
Exactly one ciphertext artifact was produced:

```text
artifact_id:     9607112832
artifact_name:   tibia-global-login-encrypted-handoff-808e72e2410831ba12c2c844f9612795d1400237
archive_sha256:  e0f3be3796dbc10ee012b47d58369b51f19cbf0edf6f3e4b06b0ad9f90d45aff
archive_size:    860
handoff.cms:     719 bytes
retention:       1 day
```

No account credential, session value, cookie/device cookie, character/world identity, or raw login error text was logged or uploaded outside the encrypted CMS payload.

## Molehill decrypt and current assets — PROVEN

Fresh local key/certificate checks passed without printing key material:

```text
CERT_FINGERPRINT_MATCH=PASS
CERT_REPO_LOCAL_MATCH=PASS
PRIVATE_KEY_PUBLIC_MATCH=PASS
```

The ciphertext decrypted locally. Structural validation emitted only booleans: the object had exactly `sessionKey`, `worldName`, `worldHost`, `worldPort`, `characterName`; required values/types were present; the protected port was valid; no device cookie was present.

The handoff was ultimately streamed directly from in-memory decryption into `/dev/shm/trackb-handoff.json` of the isolated one-shot Track B container, mode `0600`, without a plaintext host file or normal container-layer handoff file.
Fresh `assets-current` retrieval through WARP verified the current gameplay asset manifest and every downloaded packed/unpacked hash:

```text
assets_json_sha256: 686e88fdce30242faf6fcc83cfac63af79a7d0522782d0e64202799f5cb97414
manifest_rows:       7094
login_asset_files:   5
verification:        PASS
```

The five local-only files were `assets.json.sha256`, `catalog-content.json`, current appearances, current staticdata and current proficiencies. Current appearances changed to the `e8a12a...` content generation; staticdata remained the `62d3f5...` generation. These proprietary bytes stayed on Molehill and were never uploaded to GitHub.

A fresh isolated container, `otclient-trackb-e2e-808e72e2`, was created from the existing Track B OTClient image with task labels and no Track A/shared-home mount. The canonical repository `world-entry-probe-1532.sh` transformer was reused in transform-only mode. The only local wrapper changes were the `/dev/shm` handoff path and a passive post-`GAME_START` semantic marker requiring `g_game.isOnline()`, a local player and numeric player position before emitting `IN_GAME=true`.
## One bounded current-build OTClient game login

Exactly one OTClient `loginWorld()` attempt was performed. The handoff was consumed once and deleted from tmpfs. Sanitized progress markers included:

```text
HANDOFF_CONSUMED=true
CLIENT_VERSION_ACCEPTED=true
APPEARANCES_LOAD_OK=true
THINGS_APPEARANCES_READY=true
SESSION_KEY_FEATURE=true
CHARACTER_LOGIN_ATTEMPT=true
CHARACTER_LOGIN_CALL_RETURNED=true
```

Staticdata still failed the existing parser and was explicitly marked `STATICDATA_LOAD_FAILED=true` / `STATICDATA_BYPASSED_FOR_LOGIN=true`; this was not represented as staticdata support.

Transport was real and bidirectional through the task-owned SOCKS forwarder:

```text
SOCKS_GRANTED=true
CLIENT_BYTES=true
SERVER_BYTES=true
CLIENT_LENGTH=230
SERVER_LENGTH=148
CLIENT_VERSION_VALUE=1532
PROTOCOL_VERSION_VALUE=1532
```
Server opcode order was observed without retaining packet payloads:

```text
GAME_SERVER_OPCODE_57=true
GAME_SERVER_OPCODE_20=true
GAME_LOGIN_ERROR=true
GAME_LOGIN_ERROR_RELATION_CLIENT_WORLD=true
GAME_LOGIN_ERROR_TEXT_LENGTH=117
```

Decimal opcode `20` is `0x14`. It was followed immediately by the structured game-login error callback. The raw server text was not printed. `GAME_START` and the passive semantic `IN_GAME` marker were never emitted.

Current result:

```text
GAME_START=false
IN_GAME=false
GAME_LOGIN_RESULT=STRUCTURED_0x14_REJECTION
IDENTICAL_RETRY_ALLOWED=false
```

This reproduces the historical structured `0x14` boundary on the newly current-fenced HTTP/session/assets path. The current run is therefore protocol evidence, not a login-service, stale-clientversion, asset-refresh, TCP, SOCKS, handoff, display, or process-start failure.

## Required wire-writer evidence — BLOCKED

Fresh repository/PR search after this result found no promoted final queue/TCP writer evidence for current build `15.32.75d4a0 / d1a16819...`.

The strongest promoted login-message evidence remains PR #589 / merged historical Track A material for `15.32.df7b29 / e6c244...`. It proves `GameclientMessageLogin`, nested `LoginRSAEncryptedBlock`, and the producer call into `TProtocolMessageQueue::sendLogin`, but explicitly does not prove the final TCP writer and is fenced to the older binary.
Per the canonical continuation rule, Track B must not resend this packet or guess feature toggles. A future protocol change requires promoted **current-build** evidence for the final `TProtocolMessageQueue` queue/TCP serialization path, then an explicit comparison against `ProtocolGame::sendLoginPacket()`.

## Cleanup and secret disposition

After the one-shot attempt:

- `/dev/shm/trackb-handoff.json` was absent after `HANDOFF_CONSUMED=true`;
- the isolated one-shot Track B container was stopped after evidence collection;
- local `handoff.cms` and its consume directory were deleted from Molehill;
- the GitHub artifact remains governed by the workflow's one-day retention;
- the Molehill private handoff key was not moved, copied to GitHub, or printed.
A Docker Desktop quirk discovered during an earlier failed staging attempt caused `docker cp` to a mounted `/dev/shm` path of the old `otclient-kasm` container to write a hidden rootfs-layer file. `docker diff` proved both hidden test and handoff paths existed. The old Track B container was stopped, both hidden paths were overwritten with zero-length files while stopped, and read-back proved:

```text
hidden handoff readback size: 0
hidden dummy readback size:   0
```

Thus no known local plaintext handoff remains persisted by this task.

## Exact next action

Do **not** run another OTClient game-login attempt from the current packet and do not mutate protocol features by guesswork.

Resume only after trusted repository evidence promotes the final current-build `15.32.75d4a0 / d1a16819...` game-login queue/TCP writer contract. Consume that evidence, compare it byte-contractually/structurally with Track B `ProtocolGame::sendLoginPacket()`, make only an evidence-derived delta if one exists, then authorize at most one new bounded E2E.

Until then the genuine blocker is:

`BLOCKED_REQUIRED_CURRENT_BUILD_GAME_LOGIN_WIRE_WRITER_EVIDENCE`.