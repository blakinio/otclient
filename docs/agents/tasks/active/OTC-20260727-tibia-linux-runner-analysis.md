# OTC-20260727 — Tibia Linux runner analysis

## Status

`active_structural_login_trace` — exact current-client Qt ownership/dispatch recovery is now proven. A bounded no-OCR live experiment is reconstructing the known-good full official runtime, dynamically reacquiring PID/PIE bias, tracing exact login/session dispatch points and retaining FullMap/FieldData as the structural `IN_GAME` gate.

This is an operational research task. Temporary `.github/workflows/tibia-*` files are evidence scaffolding, not product code. Do not commit/upload proprietary CipSoft bytes, credentials, account/character data, cookies, session material, authenticated screenshots, recovery material, or WARP account/profile material.

## Objective

Reach and prove official-client world entry without OCR/Tesseract/image-to-text, using the already-authorized test-account Actions secrets only through verified changed WARP egress. Success requires decoded runtime/protocol evidence, not UI state.

## Ownership

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` draft operational PR
- Programme: `OTCLIENT-TIBIA-RE`
- `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811`: read-only evidence only
- canonical `oteryn-staging`: out of scope

## PROVEN — exact client and runtime

- Official Linux client version: `15.32.df7b29`.
- Executable size: `51,965,216` bytes.
- Executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Packed `bin/client.lzma` SHA-256: `496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b`.
- Package manifest: `1634` entries; assets manifest: `7094` entries.
- Full-runtime reconstruction run `31626946078`, job `94215664628`, reached `FAILED_ASSET_LOAD_COUNT=0` and preserved `209` packed minimap subarea objects.
- Known-good hosted renderer path is software Mesa/llvmpipe + lavapipe. `QT_XCB_GL_INTEGRATION=none` is rejected.

## PROVEN — WARP/account/login service

- `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` exist as Actions secrets; only boolean presence has been emitted.
- No-OCR workflows fail if Tesseract is present.
- Changed WARP egress is verified before secret use.
- Run `31647827166`, job `94285373954`, proved the current login identity bundle through WARP: HTTP `200`, JSON, no error message, and structural presence of `session`, `playdata`, `characters`, and `worlds` using `clientversion=15.32.df7b29`, `clienttype=2`, and current 64-character asset version.
- No credential/session/cookie/character/world values were persisted.

## PROVEN — Worldmap structural boundary

For this exact client cut:

- FullMap `0xcec8d0`
- FieldData `0xcd3190`
- Create `0xcecc70`
- Change `0xcecf40`
- Delete `0xcd4e20`
- ordered map routine `0x19a8a80`
- Worldmap QMetaObject `0x3087800`
- Worldmap string data `0x1cd8a54`
- Worldmap metadata `0x1cd8820`
- Worldmap static metacall `0xdf2a60`

Cross-repository read-only evidence from the same binary hash additionally proves a live decoded map sample with real `(x,y,z)`, ordered contents and multiple floors, but this OTClient task still requires its own world-entry proof before consuming that as current live session state.

## PROVEN — QMetaObject and exact login dispatch

The Worldmap control proves QMetaObject field offsets `string=0x8`, `meta=0x10`, `static=0x18`.

Corrected recovery run `31649792368`, job `94291373444`, result `SUCCESS`, and owner-index run `31650684531`, job `94294137219`, result `SUCCESS`, prove:

### `tibia::gamewindow::TCharacterSelectionController`

- QMetaObject `0x2f656a0`
- static metacall `0xd46550`
- `requestCharacterLogin` index 0 -> direct target `0xd47300`
- `onCharacterSelectionConfirmed` index 11 -> direct target `0xd47130`

### `tibia::authentication::TAuthenticationProcessController`

- QMetaObject `0x3073920`
- static metacall `0xcfabb0`
- `onLoginFailedStateEntered` index 15 -> `0xcfb404`
- `onStartGameServerLoginStateEntered` index 27 -> `0xcfb122`
- `onLoginAbortedStateEntered` index 31 -> `0xcfaea7`

### `tibia::authentication::TGameserverLoginProcessController`

- QMetaObject `0x30cdc60`
- static metacall `0xcf9da0`
- `onGameserverTCPConnectionConnected` index 3 -> `0xcfa0e0`
- `onGameserverTCPConnectionSecondaryConnected` index 4 -> `0xcfa110`
- `onGameserverTCPConnectionDisconnected` index 5 -> `0xcfa150`

### `tibia::client::TGameClient`

- QMetaObject `0x2f61ea0`
- static metacall `0xd06260`
- `connectClientToGameserverWithExistingCredentials` index 11 -> `0xd06660`
- `onConnectClientToGameserver` index 20 -> `0xd06810`
- `onAbortConnectClientToGameserver` index 21 -> `0xd067b0`
- `onGameSessionConnected` index 28 -> `0xd066e0`
- metadata also places `onGameSessionLoginSuccessful` at index 29.

### Game-session structures

- `tibia::game::IGameSession` QMetaObject `0x30790a0`; metadata includes `worldEntered` index 6 and `gameLoginSuccessful` index 5.
- `tibia::game::TGameserverGameSession` QMetaObject `0x2f765a0`, static metacall `0xd215c0`.
- `tibia::game::TGameSessionBase` `onCharacterConfigurationLoaded` -> direct target `0xd26320`.

**DISPROVEN:** `critical QMetaObject recovery incomplete`. The earlier workflow failed because its required-method filter mixed methods owned by different QMetaObjects.

## PROVEN — previous best world-entry attempt

Run `31626946078`, job `94215664628`:

- exact client and complete assets loaded;
- exact `1020x650` window established;
- FullMap/FieldData breakpoints armed;
- deterministic account login and first-character activation executed without OCR;
- result: `DECODED_WORLDMAP_HIT=false`, `FAILED_ASSET_LOAD_COUNT=0`, `POST_ACTIVATION_DIRECT_TCP_COUNT=0`, `POST_ACTIVATION_UDP_COUNT=0`;
- client survived.

This places that failure before normal Internet-family game-server connection setup.

## REJECTED / DO NOT REPEAT

- wrong credentials/current HTTPS identity bundle;
- missing package/assets catalogs;
- WARP failure;
- proxychains alone, root alone, missing Vulkan alone, blind row geometry changes;
- official launcher as the hosted execution path;
- guessed function centers derived only from type-string xrefs;
- old QMetaObject required-method filter.

## Current experiment

```yaml
experiment_id: OTC48-LOGIN-TRACE-001
objective: identify the exact structural transition reached after deterministic first-character activation and prove IN_GAME if FullMap/FieldData arrives
hypothesis: exact Qt dispatch tracing will distinguish character-selection return, gameserver-login start/connect/abort/failure, session connection and world entry without pixels or OCR
preconditions:
  client_version: 15.32.df7b29
  binary_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  runtime_recipe: proven complete-assets v4 steps
  secret_path: Actions secrets only
  egress: verified changed WARP before secret use
action: workflow tibia-hosted-login-structural-trace.yml
expected_structural_evidence:
  - dynamically reacquired PID and PIE load bias
  - named login/session dispatch events from exact current-version addresses
  - FullMap or FieldData hit for STRUCTURAL_IN_GAME=true
abort_conditions:
  - binary hash mismatch
  - runtime reconstruction failure
  - trace cannot attach/arm
  - direct TCP confinement violation
rollback_or_recovery: no persistent client mutation; preserve event trace and classify the last proven transition
external_run_id: 31650884938
workflow_head: e37f2208f9ce0fcce53e0b6cfae9212e75791161
result: INCONCLUSIVE
```

## Safety invariants for this task

- No OCR/Tesseract/image-to-text.
- Never expose secret values in argv/logs/screenshots/repository/artifacts/chat.
- Verify changed WARP egress before credential use and zero unintended direct TCP when relevant.
- Do not mutate canonical staging or the separately owned Oteryn runtime.
- Pixel/window changes are not world-entry evidence.
- Current #48 debugger instrumentation is observational only; no callback result, branch decision or client/server state modification through the debugger.
- Leave the character idle if world entry is proven. Gameplay/action proof belongs to the next programme phase/task after this login task is terminally checkpointed.

## Validation / live state

```yaml
updated_at: 2026-08-13T01:27:00+02:00
pr: 48
status: active
qmeta_recovery:
  run: 31649792368
  job: 94291373444
  result: PASS
method_owner_index:
  run: 31650684531
  job: 94294137219
  result: PASS
structural_login_trace:
  run: 31650884938
  head: e37f2208f9ce0fcce53e0b6cfae9212e75791161
  result: RUNNING
safe_to_resume: true
```

`next_action`: when run `31650884938` is terminal, inspect its structural event trace. If FullMap/FieldData hit, persist `IN_GAME` proof and close the #48 login phase cleanly before moving to the next `OTCLIENT-TIBIA-RE` phase. If it did not hit, use the exact last named transition as the sole next hypothesis and repair only that path.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 4
  session_id: chatgpt-20260813-otclient-tibia-re
  checkpointed_at: 2026-08-13T01:27:00+02:00
  last_progress_at: 2026-08-13T01:26:17+02:00
  phase: structural_login_trace
  exact_head_before_checkpoint: e37f2208f9ce0fcce53e0b6cfae9212e75791161
  pull_request: 48
  active_operation: GitHub Actions run 31650884938
  external_run_ids:
    - 31650884938
    - 31650684531
    - 31649792368
    - 31647827166
  status: active
  safe_to_resume: true
  resume_condition: PR #48 remains live owner and structural trace result can be reconciled
  next_action: inspect terminal run 31650884938 once and continue from its last structural event
```

Owner instruction invokes `OTCLIENT-TIBIA-RE` as an autonomous programme and requires continuation beyond world-entry until all authorized master-prompt objectives are either proven or reach a real evidenced stop condition. Owner-funded Codex/API quota remains forbidden without separate explicit authorization.