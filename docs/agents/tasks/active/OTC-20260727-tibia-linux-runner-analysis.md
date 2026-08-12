# OTC-20260727 — Tibia Linux runner analysis

## Status

`waiting_qmeta_dispatch_probe` — current HTTPS account login is structurally valid through verified WARP, and the old QMetaObject “recovery incomplete” conclusion has been disproven. A corrected path-scoped static recovery run is now executing on the exact official client. This invocation has consumed the repository's two ordinary observations for that exact run/head, so the task is checkpointed as waiting instead of polling.

This is an operational research task. Temporary `.github/workflows/tibia-*` files are evidence scaffolding, not product code. Do not commit/upload proprietary CipSoft bytes, credentials, account/character data, cookies, session material, authenticated screenshots, recovery material, or WARP profile/account material.

## Objective

Reach and prove official-client world entry **without OCR/Tesseract/image-to-text**, using only the existing authorized test-account Actions secrets through verified changed WARP egress, and accept success only from decoded runtime/protocol state such as Worldmap/GameState evidence.

## Ownership

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` draft operational PR
- Programme: `OTCLIENT-TIBIA-RE`
- Current session: `chatgpt-20260813-otclient-tibia-re`
- `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811`: read-only evidence only
- canonical `oteryn-staging`: out of scope

## PROVEN

### Exact current official Linux client

- Version: `15.32.df7b29`.
- Executable size: `51,965,216` bytes.
- Executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Packed `bin/client.lzma` SHA-256: `496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b`.
- Current package manifest: `1634` package entries.
- Current `assets-current/assets.json`: `7094` asset entries.
- Correct full runtime reconstruction retains packed manifest paths when no `unpackedhash` exists; run `31626946078`, job `94215664628` reconstructed the corrected runtime including `209` packed minimap subarea objects and reported `FAILED_ASSET_LOAD_COUNT=0`.

### Strict no-OCR/WARP boundary

- `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` are present as Actions secrets: run `31616821899`, job `94181592919`; only boolean presence was emitted.
- No-OCR executions fail if Tesseract exists and report `OCR_BINARY_ABSENT=true`.
- Login experiments verify changed WARP egress before secret use.
- The best complete-runtime attempt, run `31626946078`, job `94215664628`, had `DECODED_WORLDMAP_HIT=false`, `FAILED_ASSET_LOAD_COUNT=0`, `POST_ACTIVATION_DIRECT_TCP_COUNT=0`, `POST_ACTIVATION_UDP_COUNT=0`, with the client alive after deterministic first-character activation.
- Therefore that failure occurs before normal Internet-family game-server connection setup.

### Current HTTPS login identity bundle

Run `31647827166`, job `94285373954`, exact branch head `c951f148b883fffc39d105daf39cf9c7561da095`:

- request identity used `clientversion=15.32.df7b29`, `clienttype=2`, current 64-character `assets.json.sha256` as `assetversion`;
- endpoint returned HTTP `200`, JSON content;
- safe structural response keys: `devicecookie,loginemail,playdata,session,trusteddevice`;
- `HAS_ERROR_MESSAGE=false`;
- `HAS_SESSION=true`, `HAS_PLAYDATA=true`, `HAS_CHARACTERS=true`, `HAS_WORLDS=true`;
- `HTTPS_LOGIN_RESPONSE_VALID=true`.

No credential, session, cookie, character, or world values were logged. This proves current credentials and the login-service identity bundle are valid through WARP; it does not prove world entry.

### Worldmap structural starting points

Read-only/current-version evidence for this exact client cut includes:

- FullMap `0xcec8d0`;
- FieldData `0xcd3190`;
- Create `0xcecc70`;
- Change `0xcecf40`;
- Delete `0xcd4e20`;
- common ordered map routine `0x19a8a80`;
- Worldmap QMetaObject `0x3087800`;
- Worldmap string data `0x1cd8a54`;
- Worldmap metadata `0x1cd8820`;
- Worldmap static metacall `0xdf2a60`.

### Login/selection static inventory

Run `31627802861`, job `94218675614`, identified exact-client classes including:

- `tibia::authentication::TGameserverLoginProcessController`;
- `tibia::gamewindow::TCharacterSelectionController`;
- `tibia::client::TAntiCheatController`;
- `tibia::game::TGameserverGameSession`;
- `tibia::network::TGameserverNetworkPacketConnection`;
- `tibia::network::TGameserverTCPConnection`.

Run `31628008127`, job `94219354880`, mapped Qt method-name string VAs including:

- `onCharacterSelectionConfirmed=0x1ca3e65`;
- `requestCharacterLogin=0x1ca3d0d`;
- `onStartGameServerLoginStateEntered=0x1c8bd7a`;
- `onConnectClientToGameserver=0x1c8bdff`;
- `onAbortConnectClientToGameserver=0x1c8bbc8`.

The strings have no ordinary executable RIP-relative xrefs because they are Qt metadata. Earlier guessed code centers from nearby type strings are rejected as runtime breakpoint addresses.

### QMetaObject recovery

Run `31629211661`, job `94223374658`, was workflow `FAIL` but produced valid structural evidence:

- QMetaObject fields learned from Worldmap: `string=0x8`, `meta=0x10`, `static=0x18`.
- `tibia::worldmap::TWorldmapProtocolMessageHandler` decoded with map/event method inventory.
- `TCharacterSelectionController`: QMetaObject `0x2f656a0`, string data `0x1ca3b34`, metadata `0x1ca36e0`, static metacall `0xd46550`; method index `0=requestCharacterLogin`, index `11=onCharacterSelectionConfirmed`, 26 methods total.
- `TAntiCheatController`: QMetaObject `0x30768c0`, string data `0x1c92cc0`, metadata `0x1c92c20`, static metacall `0xcf39e0`.
- `TGameserverLoginProcessController` QMetaObject was structurally found at `0x30cdc60`; its actual Qt methods are `connected`, `disconnected`, `connectionError`, `onGameserverTCPConnectionConnected`, `onGameserverTCPConnectionSecondaryConnected`, `onGameserverTCPConnectionDisconnected`.
- `TGameserverGameSession` QMetaObject was structurally found; its actual Qt methods are `onCharacterConfigurationLoaded`, `onGameReadyForSecondaryConnection`, `onClientCheckTimerElapsed`.

**DISPROVEN:** `critical QMetaObject recovery incomplete`. The old workflow rejected valid class hits only because it incorrectly required non-metaobject methods on those QMetaObjects.

### Hosted launcher

Runs `31628168080`/job `94219884203` and `31628361566`/job `94220527259` proved the official launcher produces no usable hosted GUI/process even with native kernel WARP and without proxychains/`LD_PRELOAD`. Direct exact-client execution remains the working hosted GUI path.

## REJECTED / DO NOT REPEAT

- wrong credentials as the current login blocker — disproven by valid HTTPS login response;
- missing package/assets catalogs — corrected and `FAILED_ASSET_LOAD_COUNT=0`;
- WARP failure — changed egress is verified;
- proxychains alone, root alone, missing Vulkan alone, package-layout changes, blind click/row-geometry changes — no longer justified without new evidence;
- `QT_XCB_GL_INTEGRATION=none` — known bad; software Mesa/llvmpipe + lavapipe is the valid hosted renderer path;
- guessed Qt function centers from type-string xrefs — not structurally proven;
- rerunning QMetaObject recovery with the old required-method filter — hypothesis is invalidated.

## Safety invariants

- No OCR/Tesseract/image-to-text for login or success proof.
- Never expose secret values in argv, logs, screenshots, repository files, artifacts, or chat.
- Never log in from ordinary/direct egress; verify changed WARP egress first.
- Never mutate canonical staging or the separately owned Oteryn analysis runtime.
- Pixel/window changes are not world-entry evidence; require decoded Worldmap/GameState/protocol evidence.
- Breakpoints/tracing are observational only for this task: do not modify callback results, branch decisions, security decisions, or client/server state through the debugger.
- Leave the character idle if world entry is proven; gameplay actions are not authorized in this active task.

## Current experiment

```yaml
experiment_id: OTC48-QMETA-002
objective: recover exact current-version Qt dispatch metadata for the login/selection classes
hypothesis: the previous run recovered the classes but failed only because of invalid required-method assumptions
preconditions:
  client_version: 15.32.df7b29
  binary_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  secrets_required: false
  warp_required_for_client_fetch: true
action: path-scoped push workflow tibia-hosted-login-qmetaobject-recovery.yml
expected_structural_evidence:
  - all four target QMetaObjects recovered by exact class identity
  - exact qmeta/string/meta/static_metacall values
  - actual method tables
  - static-metacall dispatch/jump-table candidates where structurally derivable
abort_conditions:
  - exact client hash mismatch
  - target class absent from current binary
  - analysis cannot validate Worldmap QMetaObject control
rollback_or_recovery: preserve prior proven evidence and update hypothesis; no runtime mutation
external_run_id: 31649792368
workflow_head: 691f4e865dcdd800f7bd3fb129d0929e63c33da7
observed_structural_evidence: pending
result: INCONCLUSIVE
```

## Validation / anti-stall state

```yaml
updated_at: 2026-08-13T01:10:00+02:00
pr: 48
branch_head: 691f4e865dcdd800f7bd3fb129d0929e63c33da7
status: waiting
invocation_started_at: 2026-08-13T01:02:00+02:00
last_progress_at: 2026-08-13T01:08:47+02:00
ordinary_ci_observations_for_qmeta_head: 2
qmeta_run:
  id: 31649792368
  first_observation: queued
  second_observation: in_progress
  conclusion: pending
safe_to_resume: true
```

`next_action`: after run `31649792368` reaches a terminal state, inspect it once in a fresh continuation session. If successful, persist the exact QMetaObject/static-metacall/method-target evidence and construct the smallest strict no-OCR **observational** login trace using those current-version dispatch points with FullMap/FieldData as the success gate. If it fails, inspect the failed job log, isolate the first actionable error, and repair only with a new evidence-based hypothesis.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 3
  session_id: chatgpt-20260813-0106-otclient-tibia-re
  session_started_at: 2026-08-13T01:02:00+02:00
  checkpointed_at: 2026-08-13T01:10:00+02:00
  last_progress_at: 2026-08-13T01:08:47+02:00
  phase: qmeta_dispatch_recovery
  exact_head: 691f4e865dcdd800f7bd3fb129d0929e63c33da7
  pull_request: 48
  active_operation: GitHub Actions run 31649792368
  external_run_ids:
    - 31649792368
    - 31647827166
    - 31629211661
  operation_started_at: 2026-08-13T01:08:47+02:00
  wait_deadline_at: null
  check_generation: qmeta-recovery-v2
  checks_used: 2
  status: waiting
  safe_to_resume: true
  resume_condition: run 31649792368 is terminal and PR #48 remains the live owner
  next_action: inspect terminal run 31649792368 once, classify structural evidence, and continue from the exact result
```

Owner instruction on 2026-08-13 invokes `OTCLIENT-TIBIA-RE` autonomously and resolves the alias through `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md`. Existing test-account secrets may be used only through the already-authorized workflow/runtime mechanisms after verified WARP; their values and all sensitive session/account data remain forbidden from durable evidence.