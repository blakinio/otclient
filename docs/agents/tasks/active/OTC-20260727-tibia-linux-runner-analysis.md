# OTC-20260727 — Tibia Linux runner analysis

## Status

`active_local_login_dispatch_observation` — strict no-OCR hosted execution now reconstructs the complete current official Linux runtime, starts the exact game client in a stable `1020x650` X11 window through verified WARP, and arms decoded Worldmap breakpoints before credential use. Account login and deterministic first-character activation execute, but no `FullMap`/`FieldData` hit and no Internet-family game-server socket occur. Current evidence therefore places the remaining blocker locally between character activation and normal game-server connection setup.

This is an operational research task. Do not merge temporary workflows as product code. Do not commit/upload proprietary CipSoft bytes, credentials, account/character data, cookies, session material, authenticated screenshots, recovery material, or WARP account/profile material.

## Objective

Attempt a real official-client login/world entry **without OCR/Tesseract/image-to-text**, with credentials injected only from GitHub Actions secrets, changed WARP egress proven before secret use, Tibia TCP confined to that tunnel, and success accepted only from non-image runtime/protocol evidence.

## Ownership

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` (draft operational PR)
- Session: `chatgpt-20260812-no-ocr-world-entry`
- Separate `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811` runtime is read-only evidence. Its container/state must not be mutated or reused.
- Canonical `oteryn-staging` Compose services remain strictly out of scope.

Current owned operational paths include the task record plus temporary `.github/workflows/tibia-*` probes on this task branch. These workflows are evidence scaffolding and must be removed before terminal closeout after exact run/job IDs are retained here.

## PROVEN — strict no-OCR boundary and exact client

- `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` are non-empty Actions secrets in `blakinio/otclient`: run `31616821899`, job `94181592919`, SUCCESS. Only boolean presence was emitted; values were neither logged nor persisted.
- Strict execution explicitly fails if a Tesseract binary is present; current no-OCR runs emit `OCR_BINARY_ABSENT=true`.
- Exact official Linux client cut: version `15.32.df7b29`, executable size `51,965,216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Packed `bin/client.lzma` SHA-256: `496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b`.
- Reusable decoded Worldmap offsets from read-only evidence: FullMap `0xcec8d0`, FieldData `0xcd3190`, Create `0xcecc70`, Change `0xcecf40`, Delete `0xcd4e20`, common ordered map routine `0x19a8a80`.

## PROVEN — complete official runtime reconstruction

- Current package manifest contains exactly `1634` package entries.
- Official `assets-current/assets.json` contains exactly `7094` asset entries: run `31625032514`, job `94209116428`, SUCCESS.
- Package objects with `unpackedhash` are decoded and verified against both packed and unpacked SHA-256.
- Asset entries without `unpackedhash` must remain at their exact packed manifest path. This is required for runtime files such as `assets/subarea-*.bmp.lzma`; decoding/removing the `.lzma` suffix was a prior reconstruction bug.
- Run `31626946078`, job `94215664628`, reconstructed the corrected complete runtime with `209` packed minimap subarea objects and subsequently reported `FAILED_ASSET_LOAD_COUNT=0`.
- Earlier package-only SIGABRT was conclusively caused by missing separate runtime catalogs `assets/catalog-content.json` and `sounds/catalog-sound.json`, not by account credentials or Worldmap hooks.
- Do not reintroduce `QT_XCB_GL_INTEGRATION=none`; diagnostics proved that override disables required GLX/EGL behavior. Software Mesa/llvmpipe plus lavapipe is the valid hosted renderer path.

## PROVEN — best strict no-OCR world-entry attempt

Run `31626946078`, job `94215664628` (`tibia-hosted-complete-assets-no-ocr-login-v4.yml`):

- verified changed WARP egress before secret use;
- reconstructed all `1634 + 7094` official runtime entries with strict hashes;
- exact client started and remained alive in an exact `1020x650` window;
- direct TCP outside local WARP SOCKS and UDP were absent before login;
- `kernel.yama.ptrace_scope` was changed from `1` to `0` for observation only;
- exact FullMap and FieldData breakpoints were armed before credentials;
- account login was submitted and the previously established deterministic first-character target was activated without OCR;
- final result: `DECODED_WORLDMAP_HIT=false`, `FAILED_ASSET_LOAD_COUNT=0`, `POST_ACTIVATION_DIRECT_TCP_COUNT=0`, `POST_ACTIVATION_UDP_COUNT=0`;
- client remained alive during the bounded observation window.

**FACT:** the remaining failure occurs before normal Internet-family game-server connection setup. Repeating WARP, Vulkan, root/non-root, package-layout, asset-layout, or blind click changes without new evidence is not justified.

## PROVEN — official launcher is not currently a viable hosted execution path

- Earlier hosted launcher attempts failed to produce a usable X11 window.
- `tibia-hosted-official-launcher-window-inventory.yml`, run `31628168080`, job `94219884203`, proved there was no hidden alternate-title launcher window: after launch, the relevant process inventory was empty and the X11 root had zero children.
- `tibia-hosted-kernel-warp-official-launcher.yml`, run `31628361566`, job `94220527259`, repeated with native kernel WireGuard WARP and **without** proxychains/`LD_PRELOAD`. WARP and software GLX were valid, but the launcher still exited before any GUI child/process appeared; safe launcher log filtering produced no actionable error.
- Therefore `proxychains`/`LD_PRELOAD` is excluded as a sufficient explanation for hosted launcher non-start. Direct exact-client execution remains the only working hosted GUI path.

## PROVEN — local login dispatch names available in the exact client

Static no-secret inventory run `31627802861`, job `94218675614`, identified current exact-client types and method names needed for observational tracing:

- `tibia::authentication::TGameserverLoginProcessController`
- `tibia::gamewindow::TCharacterSelectionController`
- `tibia::client::TAntiCheatController`
- `tibia::game::TGameserverGameSession`
- `tibia::network::TGameserverNetworkPacketConnection`
- `tibia::network::TGameserverTCPConnection`
- `onCharacterSelectionConfirmed`
- `requestCharacterLogin`
- `onStartGameServerLoginStateEntered`
- `onConnectClientToGameserver`
- `onAbortConnectClientToGameserver`
- `connectClientToGameserverWithExistingCredentials`
- `connectToGameSession`
- `onGameSessionConnected`
- `onGameLoginSuccessful`
- `onLoginAbortedStateEntered`
- `onLoginFailedStateEntered`
- `onNetworkError`

Run `31628008127`, job `94219354880`, mapped the corresponding Qt method-name string VAs, including `onCharacterSelectionConfirmed=0x1ca3e65`, `requestCharacterLogin=0x1ca3d0d`, `onStartGameServerLoginStateEntered=0x1c8bd7a`, `onConnectClientToGameserver=0x1c8bdff`, and `onAbortConnectClientToGameserver=0x1c8bbc8`. These strings have no ordinary executable RIP-relative xrefs because they participate in Qt metadata rather than normal direct string use.

The first guessed function centers derived from nearby type-string xrefs were **not** proven Qt metaobject functions: relocation and raw-qword scans found no matching qmeta/vtable representation. Do not use those guesses as runtime breakpoints.

## Read-only cross-repository facts

The separate Synology investigation independently reaches authenticated `Select Character` and observes the same immediate return before AF_INET/AF_INET6 connection setup. It has already excluded wrong credentials, WARP failure, proxychains alone, root execution alone, missing Vulkan alone, and obvious row-selection geometry as sufficient explanations. This task may reuse those facts only as read-only evidence; no Oteryn runtime/state is shared.

## Safety invariants

- Never use OCR/Tesseract/image-to-text for this task's login or success proof.
- Never expose secret values in command argv, logs, screenshots, repository files, artifacts, or chat.
- Never log in from ordinary/direct egress; require verified changed WARP egress first.
- Never touch canonical staging or the separately owned Oteryn analysis runtime.
- Do not accept a pixel/window change alone as successful world entry; require a decoded Worldmap semantic runtime hit or equivalent game-world protocol state.
- Debugging/trace breakpoints are observational only. Do not patch return values, skip security checks, alter branch decisions, suppress anti-cheat, or otherwise bypass local security enforcement.
- If a security/anti-cheat requirement is proven as the blocker, stop at that supported-environment authority boundary instead of bypassing it.
- Leave the character idle if world entry is proven; no gameplay actions are authorized.

## Validation record

```yaml
updated_at: 2026-08-12T19:45:00+02:00
branch_head_before_checkpoint: e94ea3ee2aa79f32bc0ac9826afd820196d11b76
pr: 48
status: active_local_login_dispatch_observation
secret_gate:
  run: 31616821899
  job: 94181592919
  result: PASS
assets_manifest_probe:
  run: 31625032514
  job: 94209116428
  result: PASS
best_strict_no_ocr_world_entry:
  run: 31626946078
  job: 94215664628
  result: FAIL_BEFORE_GAME_SERVER_CONNECT
  decoded_worldmap_hit: false
  failed_asset_load_count: 0
  post_activation_direct_tcp_count: 0
  post_activation_udp_count: 0
hosted_launcher_window_inventory:
  run: 31628168080
  job: 94219884203
  result: NO_GUI_PROCESS_OR_WINDOW
hosted_launcher_kernel_warp:
  run: 31628361566
  job: 94220527259
  result: NO_GUI_PROCESS_OR_WINDOW
login_symbol_inventory:
  run: 31627802861
  job: 94218675614
  result: PASS
login_string_va_map:
  run: 31628008127
  job: 94219354880
  result: PASS
safe_to_resume: true
```

`next_action`: use the already-proven Worldmap Qt metaobject (`qmetaobject=0x3087800`, `stringdata=0x1cd8a54`, `metadata=0x1cd8820`, `static_metacall=0xdf2a60`) as a representation control to recover the exact Qt metadata/static dispatch for `TCharacterSelectionController` and `TGameserverLoginProcessController`; then run a strict no-OCR observational trace that records only which login callbacks fire after deterministic character activation while keeping FullMap/FieldData as the success gate. Do not modify any callback result or security decision.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: chatgpt-20260812-2259-otclient-global-probe
  session_started_at: 2026-08-12T22:59:00+02:00
  checkpointed_at: 2026-08-12T23:06:00+02:00
  last_progress_at: 2026-08-12T23:06:00+02:00
  phase: bounded_otclient_global_login_probe
  exact_head: 427f6c707a530f859e647eccf09401ff2cccde01
  pull_request: 48
  active_operation: prepare isolated OTClient Global login workflow
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: 2026-08-12T23:26:00+02:00
  check_generation: operational_probe
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: task branch remains exclusively owned and self-hosted oteryn-staging runner remains available
  next_action: create and execute an isolated OTClient 15.32 Global login probe using existing test secrets through verified WARP; stop at any anti-cheat/security rejection without bypass
```

Owner instruction on 2026-08-12 explicitly requests a real login attempt with this repository's OTClient. This bounded phase may use the task-owned self-hosted runner, task-owned isolated container/state, existing `TIBIA_TEST_EMAIL`/`TIBIA_TEST_PASSWORD` Actions secrets, and official runtime assets as transient test inputs. Secret values, session keys, character/account data, and proprietary assets remain forbidden from logs, artifacts, repository content, and chat.