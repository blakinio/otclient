---
task_id: OTC-20260813-tibia-global-login-lab
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: otclient-global-login
track_alias: OTCLIENT-GLOBAL-LOGIN
task_kind: e2e
phase: validate
branch: feat/OTC-20260813-tibia-global-login-lab
base_branch: main
created: 2026-08-13T09:10:00+02:00
updated: 2026-08-26T14:03:00+02:00
risk: medium
related_pr: 284
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - .github/workflows/tibia-global-login-encrypted-handoff.yml
  - .github/track-b-encrypted-handoff/**
  - .github/scripts/test_track_b_encrypted_handoff.py
  - docs/agents/prompts/OTCLIENT_GLOBAL_LOGIN_ENCRYPTED_HANDOFF_CONTINUE.md
  - docs/agents/evidence/OTC-20260813-tibia-global-login-lab/**
  - .gitattributes
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
modules_touched:
  - otclient-global-login
  - github-actions
reuses:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/SHORT_COMMANDS.md
  - PR #48 runtime evidence as migration input only
  - synology-otclient-01 self-hosted runner
cross_repo_tasks: []
execution_mode: github_actions_self_hosted
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
policy_version: 2
session_id: chatgpt-20260824-track-b-encrypted-handoff
session_role: implementer
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one shared-state HTTP-auth -> one-shot handoff -> world-entry E2E
validation_level: focused
invocation_started_at: 2026-08-23T16:45:00+02:00
last_progress_at: 2026-08-26T14:03:00+02:00
heavy_validation_runs: 0
repair_cycles_for_current_gate: 3
identical_failure_retries: 0
context_reconstruction_attempts: 1
execution_reason: restack canonical PR 284, refresh current public package identity/assets, then run one bounded owner-authorized world-entry E2E
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
---

# Goal

Make `blakinio/otclient` the single durable source of truth and execution home for the official-Tibia compatibility investigation, and prove whether this OTClient fork can authenticate to and enter the official Tibia game service using the repository-owned `synology-otclient-01` runner.

# Owner durable-state directive

All material work for this investigation is persisted in `blakinio/otclient`. Chat is not a source of durable continuation state. Runtime-only proprietary bytes, credentials, cookies, session keys, character/world values and other protected material remain outside Git and are referenced only by redacted/non-secret evidence markers.

The owner restored this task and PR #284 as the canonical active Track B
`otclient-global-login` / `OTCLIENT-GLOBAL-LOGIN` lane for the repository's
native Linux OTClient on 2026-08-13. PR #48 is historical evidence only and
must not replace this lane.

# Safety and isolation

- Repository writes remain in `blakinio/otclient` and task-owned paths.
- Execution is pinned to `synology-otclient-01` through labels `[otclient, synology]`.
- The lab owns separate Docker named volumes/container namespace and uses userspace WARP.
- No writable Oteryn runtime dependency is allowed.
- No proprietary Tibia binaries/assets or secret-bearing account/session material may be committed/uploaded/logged.
- Existing `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` Actions secrets are allowed only inside the bounded workflow and must not be printed or persisted.
- Owner-funded Codex/OpenAI/API quota remains forbidden without separate explicit authorization.
- No OCR/Tesseract is part of the semantic proof path.
- Until structural world entry is proven, experiments are limited to login/session/world-entry compatibility; after world entry the character remains idle in this task.

# Canonical lane

PR #284 is the single active live implementation lane. PR #48 is migration input/evidence only. The actual working runner is `synology-otclient-01`; stale queued #48/#280/#281 probes are not evidence that the Synology host is unavailable.

# Exact client cut

```yaml
client_version: 15.32.bf29ac
client_executable_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
packed_client_lzma_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client_executable_size: 52109920
login_clienttype: 2
assetversion: official_64_hex_assets_json_sha256
```

All static/runtime offsets from earlier work remain version-fenced to that exact executable hash.

The prior 15.32.df7b29 / 51965216 / e6c244bd... cut is historical evidence only. On 2026-08-23 the owner-hosted current package manifest independently bound 15.32.bf29ac to packed client 1fc26d66... and unpacked client ed5469b9..., matching the current Track A fence already on trusted main. Historical addresses/offsets are not promoted to the current binary.

# Current implementation

The canonical workflow is `.github/workflows/tibia-global-login-lab.yml` and currently executes `tools/tibia-global-login-lab/scripts/world-entry-probe-1532.sh`.

The login flow is now:

1. bootstrap/reuse verified official 15.32 asset material in lab-owned volumes;
2. establish pinned userspace-WARP and require changed egress;
3. authenticate to the official HTTPS login service;
4. keep request/response only in container tmpfs `/lab/secrets`;
5. validate the response without logging secret values;
6. reduce it to a one-shot tmpfs handoff containing only session/world/character fields needed by `g_game.loginWorld()`;
7. remove raw login request/response;
8. start OTClient through proxychains/WARP with no email/password in its process environment;
9. consume/delete the handoff from Lua;
10. require structural OTClient game callbacks (`GAME_LOGIN`, `GAME_PENDING`, `GAME_ENTER`, `GAME_START`) for semantic progress.

Product support still declares last supported client 1525. The lab patches only its
container-local copy of `modules/gamelib/game.lua` to admit 1532 before OTClient
starts; it does not call the unrelated `g_gameConfig.setLastSupportedVersion()`
binding or modify production `game.cpp`/`game.lua`.

# Live evidence

## HTTP authentication — PROVEN

Run `31687427903`, job `94406651806`, executed on `synology-otclient-01` and proved:

```text
WARP changed egress
HTTP status 200
valid JSON
session present
playdata present
device cookie present
no login error
```

No secret/account/character values were persisted.

## Tmpfs handoff plumbing

Run `31688401176`, job `94409882043`, exposed a deterministic shell bug: the second `docker exec python3 -` did not have `-i`, so the validator received no stdin and created no handoff file. This was fixed in the lab wrapper; it is DISPROVEN as a current login blocker.

## Handoff and 15.32 gate — PROVEN

Run `31689043707`, job `94411862473`, exact head `729391d03f9f1c48954d9adcba207daf2cb25ce9`, proved:

```text
bootstrap PASS
WARP PASS
HTTP login 200 PASS
login response validation PASS
tmpfs game handoff ready PASS
OTClient process started PASS
HANDOFF_CONSUMED=true
direct OTClient TCP count=0
```

The next boundary was `THINGS_NOT_LOADED=true`, not account authentication or session transfer.

## 15.32 parser isolation — PROVEN

Run `31689801981`, job `94414248356`, executed on `synology-otclient-01` and proved:

```text
LAB_HTTP_PREFLIGHT_STATUS=200
LAB_TRANSIENT_HTTP_LOGIN_STATUS_200=true
LAB_TRANSIENT_LOGIN_RESPONSE_VALID=true
LAB_TRANSIENT_GAME_HANDOFF_READY=true
LAB_OTCLIENT_PROCESS_STARTED=true
HANDOFF_CONSUMED=true
APPEARANCES_LOAD_OK=true
STATICDATA_LOAD_FAILED=true
THINGS_NOT_LOADED=true
LAB_OTCLIENT_DIRECT_TCP_COUNT=0
GAME_START=false
FAILURE_STAGE=things_not_loaded
```

Therefore official 15.32 `appearances` protobuf data is accepted by the current OTClient parser while current 15.32 `staticdata` is not. This is a concrete compatibility gap, but it is not yet proven necessary for the game-server login packet itself.

# Current bounded experiment

Commit `5cb44a4b3a83718766d57cc8d9231b0ef6f0eec8` adds a lab-only login experiment that:

- disconnects only the `game_things` client-version autoload listener so its staticdata failure cannot reset client version to zero;
- still runs the normal other client-version listeners/feature setup;
- explicitly parses `appearances` and `staticdata` separately;
- requires `appearances` for world login;
- records `STATICDATA_LOAD_FAILED=true` plus `STATICDATA_BYPASSED_FOR_LOGIN=true` rather than claiming staticdata support;
- attempts `g_game.loginWorld()` only if appearance data is ready;
- keeps all secret/session values in tmpfs and logs only boolean/failure-stage markers.

Exact workflow run:

```yaml
run: 31690398665
head: 5cb44a4b3a83718766d57cc8d9231b0ef6f0eec8
runner: synology-otclient-01
status_at_checkpoint: in_progress
```

Run `31690398665` was cancelled while a newer PR-head run superseded it. Run
`31690489689`, job `94416503465`, exact PR head
`887465e86c2bb465a3412c1d23830b0ad22c0904`, again proved HTTP 200 and a valid
tmpfs game handoff, but failed before OTClient process start because display
`:100` never became ready:

```text
LAB_TRANSIENT_GAME_HANDOFF_READY=true
xdpyinfo: unable to open display ":100"
```

The first failing layer is therefore stale/unready lab Xvfb state, not HTTP
authentication, handoff creation, asset parsing, or the game protocol. The lab
now terminates only its prior `Xvfb :100`, removes only that display's stale
lock/socket, starts a fresh server, and emits `LAB_XVFB_READY` plus
`FAILURE_STAGE=xvfb_not_ready` on bounded readiness failure.

Run `31690800069`, job `94417408594`, exact head
`f3b261e53540028783cd8fe8e3aca006897a16e0`, proved the Xvfb repair and OTClient
startup. The first downstream boundary was the missing `GameSessionKey` feature:

```text
LAB_XVFB_READY=true
LAB_OTCLIENT_PROCESS_STARTED=true
APPEARANCES_LOAD_OK=true
HANDOFF_CONSUMED=true
SESSION_KEY_FEATURE_MISSING=true
LAB_OTCLIENT_DIRECT_TCP_COUNT=0
FAILURE_STAGE=session_key_feature_missing
```

`modules/game_features/features.lua` declares `GameSessionKey` for every client
version at or above 1074, so the isolated 15.32 wrapper now restores that
version-derived feature when the normal initialization sequence leaves it
unset. The override is lab-only and emits
`SESSION_KEY_FEATURE_LAB_OVERRIDE=true`; production feature defaults remain
unchanged. Fast Checks also identified the repository validator's missing
knowledge of the already-working `otclient` and `synology` self-hosted runner
labels, now declared in `.github/actionlint.yaml`.

Run `31692159409`, job `94421655408`, exact head
`aff08a5b8d3b02436edd455f788eb0e2d52e2e2c`, proved the session-key feature
restoration and reached the first game connection callback:

```text
SESSION_KEY_FEATURE=true
CHARACTER_LOGIN_ATTEMPT=true
CHARACTER_LOGIN_CALL_RETURNED=true
GAME_CONNECTION_ERROR=true
LAB_OTCLIENT_DIRECT_TCP_COUNT=0
FAILURE_STAGE=game_connection_error
```

The current callback intentionally discarded both error arguments, so this run
does not yet distinguish a proxy/TCP failure from a post-connect transport
close. The probe now records only the numeric `std::error_code` value as a
non-secret marker and continues to discard its free-form message.

Run `31692607512`, job `94423060887`, exact head
`5598eae8141f3ec532a19a2f5937223298cd02ee`, reproduced the connection callback
with numeric code `110` (`ETIMEDOUT`) after the character login call. No
`GAME_LOGIN` callback occurred and direct OTClient TCP remained zero. The next
probe independently attempts a bounded SOCKS5 TCP connection through the same
userspace-WARP endpoint to the handoff world host/port, emits only a boolean
grant marker, discards all curl output, and does not log target values.

Run `31693018740`, job `94424378218`, exact head
`c8c425bb8ae4ad937f129478e31de8493c8c3f26`, proved that an independent SOCKS5
connection to the exact handoff game endpoint is granted through WARP while
OTClient's proxychains-wrapped asynchronous connection still times out with
code 110. The remaining transport defect is therefore the proxychains adapter,
not WARP or game-port reachability. The lab now uses a loopback-only TCP forward
that performs the SOCKS5 handshake itself; proxychains bypasses only loopback
and continues to cover any other OTClient socket. Target values remain only in
the tmpfs handoff and are never logged.

Run `31693536712`, job `94426014523`, exact head
`505bf6ab29546b67cad805b10a718dd26413f3fd`, proved the loopback forward was
selected and its SOCKS5 request was granted. OTClient no longer emitted a
connection error, but neither a game callback nor `GAME_START` occurred before
the watchdog. The forwarder now records only direction-presence booleans for
client-to-server and server-to-client bytes, without retaining counts or
payloads, to distinguish a challenge-first deadlock from a parser failure.

Run `31693969725`, job `94427365487`, exact head
`6718c89eee5276d70217b4d1f1a0360b44e79b1c`, proved client-to-server bytes were
sent while no server bytes arrived. Source inspection then identified that the
lab's `setClientVersion(1532)` can be a no-op when the persisted runtime already
holds 1532, leaving the feature set previously reset by failed normal things
loading. The lab now forces a feature rebuild through `0 -> 1532` after
disconnecting only the things autoloader and records the critical login packet,
challenge, checksum, authenticator, and pending-login flags.

Run `31694372776`, job `94428653933`, exact head
`0cdbcf127cecb0237bd329b69e5e7bbd09f689cf`, still sent client bytes and received
no server bytes; none of the critical normal feature markers appeared. The next
bounded falsification explicitly enables only `GameChallengeOnLogin`: server
bytes would prove challenge-first behavior, while no bytes in either direction
would reject that handshake variant for this endpoint.

The challenge-first run `31694806569` and its one exact-head manual retry
`31695124060` were both cancelled externally before producing the required
direction markers; the retry was cancelled during HTTP preflight. Neither run
is protocol evidence. The owner has explicitly authorized resuming the exact
challenge-first experiment and keeping PR #284 active until terminal condition
A or B is proven.

Run `31695992918`, job `94433781793`, exact head
`3d1467255e73584163b11f2c88750477643c40dc`, completed that challenge-first
experiment. SOCKS was granted, but both directional markers were false. This
disproves challenge-first behavior for the current official game endpoint. The
earlier non-challenge run sent client bytes while normal encryption, checksum,
client-version, login-pending, and sequenced-packet flags were absent. The next
experiment keeps challenge-first disabled, restores those existing
version-derived features, and records only aggregate directional byte lengths,
never payloads.

Run `31697097942`, job `94437261305`, exact head
`05ba7696579a82601034959430243eca12aeb4c2`, completed the restored
non-challenge framing experiment. The forward granted the SOCKS request and
OTClient sent a 143-byte first packet, but the endpoint returned zero bytes:

```text
FEATURE_CHALLENGE_FIRST_REJECTED=true
FEATURE_CLIENT_VERSION=true
FEATURE_LOGIN_PENDING=true
FEATURE_PROTOCOL_CHECKSUM=true
LOGIN_PACKET_FEATURES_LAB_RESTORED=true
SESSION_KEY_FEATURE=true
LAB_GAME_FORWARD_CLIENT_BYTES=true
LAB_GAME_FORWARD_CLIENT_LENGTH=143
LAB_GAME_FORWARD_SERVER_BYTES=false
LAB_GAME_FORWARD_SERVER_LENGTH=0
LAB_OTCLIENT_DIRECT_TCP_COUNT=0
```

This disproves the missing legacy feature set as the sole cause. Source review
then found that `g_game.chooseRsa()` advertises the Linux OS id because the lab
runs in a Linux container, although official Tibia 15.32 has no native Linux
client. The next bounded experiment keeps the proven non-challenge framing and
advertises the official Windows OS id after selecting the CipSoft RSA key.

Run `31698057223`, job `94440289781`, exact head
`7c49a4a3efa1de68f247b7c289bca31c76f3dff8`, disproved that OS identity
hypothesis. The Windows override was active, the forward granted the connection,
and the exchange remained exactly 143 client bytes to zero server bytes. The
restored feature subset was then compared again with `features.lua`; it omitted
`GamePreviewState`, which has been part of the login packet since version 980
and contributes one pre-RSA field. The next experiment restores that field and
removes the disproven OS override so only the packet layout changes.

Under the current `main` Linux-only Track B governance, the temporary Windows
OS-id spoof is historical/non-admissible compatibility evidence. It never ran a
Windows binary, was removed immediately, and is not used by the current Linux
protocol conclusion or next action.

Run `31698702409`, job `94442332169`, exact head
`7eefc0f5a93fe0be33e6ce433839e0f349a18fb1`, proved the preview field was
present and increased the first packet from 143 to 144 bytes, but the server
still returned zero bytes. Inspection then identified a concrete identifier
encoding defect: `loadAppearances()` assigns the complete raw contents of
`assets.json.sha256` to the game-login asset identifier, while the successful
HTTP flow extracts its 64-hex first field. The lab now normalizes only the
runtime copy consumed by Linux OTClient to exactly that already-validated
64-character identifier; the cached source asset remains unchanged.

Run `31699422432`, job `94444685453`, exact head
`4a830036f1d404bc8b3126cb042f1c1ffab85f3b`, proved the runtime identifier
normalization was active, but the exchange remained 144 client bytes to zero
server bytes. Because 144 bytes is structurally shorter than the expected
version-1532 packet with a 64-character pre-RSA asset identifier, the next run
records the public numeric client/protocol versions immediately before
`loginWorld()` to determine whether failed staticdata loading mutates them.

Run `31699999084`, job `94446584260`, exact head
`4251aa83e826e71991f47f03807a1f688c875a9d`, reproduced 144 client bytes to
zero server bytes. The numeric markers were emitted inside the container, but
the wrapper exported only `=true` markers. The harness now exports only the two
strictly named public numeric version markers; no payload/session field is
matched.

Run `31700524092`, job `94448283844`, exact head
`32df0e573aa91cc993cd30d65cb9f02dd72055c1`, proved the actual defect:

```text
CLIENT_VERSION_VALUE=0
PROTOCOL_VERSION_VALUE=1532
LAB_GAME_FORWARD_CLIENT_LENGTH=144
LAB_GAME_FORWARD_SERVER_LENGTH=0
```

The appearances/staticdata isolation path therefore left the effective client
version at zero before game-login construction. The lab now restores client
version 1532 after the staticdata probe and immediately before choosing the
official RSA/login path. Runtime remains the task-owned native Linux image
`sha256:3ec759b55702dd967a6ef601967b4cf71e71192d69e2493481630241959b9dc7`.

Run `31701038478`, job `94449979161`, exact head
`ffbc7e50644d57f75baa2a08041e62077368da61`, showed that restoring 1532
retriggered the still-connected `ThingsLoaderController`, which again reset
both values to zero and removed `GameSessionKey` before any client bytes were
sent. The earlier disconnect candidate referenced `modules.game_things.load`,
but the loader function is local and the real registration is controller-owned.
The lab now terminates only `ThingsLoaderController` before changing versions,
then performs its explicit appearances/staticdata probes itself.

Run `31701555318`, job `94451677203`, exact head
`2e6c604c095b54a42bc9ea10ab405bdab3da62bd`, proved the controller symbol is
not visible across the sandboxed module boundary; versions again became zero
and no client bytes were sent. The next lab-only runtime patch removes only the
fatal staticdata error-list addition from the container copy of
`game_things/things.lua`. The explicit parser probe remains and still reports
`STATICDATA_LOAD_FAILED`, while successful appearances can keep version 1532
alive for the game-login experiment.

Run `31702087216`, job `94453443371`, exact head
`76d30527c718650dd50316140847f07154449342`, crossed the previous boundary:

```text
CLIENT_VERSION_VALUE=1532
PROTOCOL_VERSION_VALUE=1532
SESSION_KEY_FEATURE=true
LAB_GAME_FORWARD_CLIENT_BYTES=true
LAB_GAME_FORWARD_CLIENT_LENGTH=230
LAB_GAME_FORWARD_SERVER_BYTES=true
LAB_GAME_FORWARD_SERVER_LENGTH=148
GAME_LOGIN_ERROR=true
```

The endpoint now parses enough of the native Linux OTClient login to return a
protocol login error. The callback still discards the free-form text. The next
run maps it only to fixed non-secret categories without printing the message.

Run `31702589243`, job `94455122542`, exact head
`1d8c3e900e42a48137e5209ee590bd6d7a315f5b`, stopped before OTClient launch:
the task-owned cached Linux runtime already contained the lab staticdata patch,
while its guard accepted only the original source form. This is a harness
failure and not protocol evidence. The runtime patch is now idempotent: it
accepts exactly the original single gate or the exact marked replacement.

Run `31704259145`, job `94460713960`, exact head
`cf5ab7b4383b25360743c5274d830d6db02a2b7e`, reproduced the 230/148-byte
exchange with effective versions 1532. The first classifier matched both
client/version and character/world because it used individual generic words,
including `world`. The classifier is now phrase-based, emits one or more
specific detail categories, and explicitly emits `UNCLASSIFIED` when none
matches; it still never prints the server text.

Run `31705239981`, job `94464032351`, exact head
`06b8ab5b6ff41ba68ddd2b82bbc138ec9c8574b6`, reproduced the 230/148-byte
exchange but none of the narrow phrases matched. The next classifier preserves
the already-proven word relationship without content by emitting only
client+world, client+connect and client+denied booleans plus total message
length. No text or hash is exported.

Run `31705787903`, job `94465887261`, exact head
`f827ecfd5a529a5656a4565eeebcaa40f12e8975`, again exchanged 230/148 bytes at
effective 1532/1532 but emitted no login callback at all. The next run records
only numeric server opcodes through the existing pre-dispatch `onOpcode` hook
and adds the missing boolean `onLoginAdvice` callback. Payload bytes remain
unread and unlogged.

Run `31706716385`, job `94469029667`, exact head
`0ee27024357913cfe4d0fca2214a609b86339b01`, reproduced the effective
1532/1532 and 230/148-byte exchange and structurally identified server opcode
`20` (`0x14`, game-login error). The fixed non-secret relationship markers
showed `client+world=true`, and the discarded message length was 117. This
proves a server-returned client/world compatibility rejection rather than a
timeout, harness, proxy, WARP, or challenge-first failure.

Source inspection found that the post-1281 login packet sends only the numeric
string `"1532"`, while the proven HTTP login cut identifies itself as exact
version `"15.32.df7b29"`. The next bounded experiment adds an optional full
client-version string to `g_gameConfig`, retaining the existing numeric fallback
when unset, and configures only the Track B Linux lab with the exact full string.
The canonical workflow now builds the exact branch head as a native Linux
artifact before the Synology probe and replaces only the task-owned cached
runtime binary. No official client binary or non-Linux runtime is involved.

Run `31707825958`, jobs `94472766713` and `94481506722`, exact head
`0a2b83e080f7f513a865229102028f947ba71c76`, proved the exact native Linux
build, artifact handoff, isolated bootstrap, WARP and HTTP login. It stopped
after consuming the tmpfs handoff but before the character-login call, with
zero bytes in both directions and no full-version marker. This is a local Lua
binding/harness failure, not protocol evidence. The string accessors now use
Lua-binder-safe value semantics and the setter is guarded by `pcall` with a
fixed boolean marker before any network attempt.

Run `31711058660`, jobs `94483865718` and `94485052635`, exact head
`313cd1b8d5c1a463154a9ea675b00b2d6da95e3d`, reproduced the same pre-network
stop with zero directional bytes and no full-version `pcall` marker. Therefore
execution stops earlier at the existing last-supported-version setter. The
next run emits a marker before that call and guards it independently, so the
exact failing Lua/C++ boundary is classified without exposing error text.

Run `31712081913`, jobs `94487351437` and `94487558014`, exact head
`2b184f882a0a873ce55bdff281c5be7e6dd1f6f0`, passed the exact native-Linux
build, artifact transfer, isolated Synology bootstrap, WARP path and HTTP
login. The controlled probe reached `HANDOFF_CONSUMED=true` and
`VERSION_CONFIG_BEGIN=true`, then produced zero client/server directional bytes
and no subsequent configuration outcome marker. The prior diagnostic emitted
its `pcall` outcome as `=false`, which the existing boolean-only exporter did
not surface. This run therefore establishes neither a full-version setter
failure nor a protocol result.

The recovery change rebases Track B on current `main` and makes the bounded
full-version diagnostic self-classifying: it removes the unrelated runtime
last-supported-version setter from this path, raises only the lab runtime's
supported-client cap before OTClient starts, emits exactly one full-version
outcome marker, and exports a numeric exit-or-signal category if the process
ends before an outcome. The production selection path now has focused tests for
configured full-string serialization and the empty numeric fallback.

Run `31717603954`, job `94507702845`, exact head
`281a9d47491f064138b29dbe8ce450411cbb88a0`, passed the exact native-Linux
build, isolated bootstrap, WARP transport and HTTP login, but did **not** start
OTClient. Its lab-only Python injector stopped with an unterminated string
literal while rendering the container-local supported-client patch. Therefore
no `FULL_CLIENT_VERSION_*`, directional-byte, callback, or opcode marker was
produced. This is a reproducible harness defect, not a setter or protocol
classification; the injector now has a render check that reproduces the exact
transformation locally before the one valid bounded E2E retry.

Run `31718980508`, job `94511106360`, exact head
`d112e8a642530f4ab8dba068cc7cd12584e0b2f7`, passed the exact native-Linux
build, isolated bootstrap, WARP transport and HTTP login, but again did **not**
start OTClient. The repaired injector reached its version-list guard, which
assumed that the `1520` sequence began the final list line; the verified source
has `1500` and `1520` entries on that same line. No full-version, directional,
callback, or opcode marker exists from this run. The guard now matches the one
terminal `1525` entry plus its closing brace, and its complete inner container
patch is executed against an offline copy of the verified module shape before
the next E2E.

Run `31719826179`, jobs `94513685119` and `94513846464`, exact head
`7b0265d52262f9fba68c6ca96fde76bed48bc3b7`, passed the exact native-Linux
build, isolated bootstrap, WARP transport, HTTP login, tmpfs handoff, SOCKS
reachability and OTClient process startup. It then classified the requested
boundary without exporting exception text or configured/session values:

```text
HANDOFF_CONSUMED=true
FULL_CLIENT_VERSION_CONFIG_BEGIN=true
FULL_CLIENT_VERSION_CALL_FAILED=true
LAB_GAME_FORWARD_CLIENT_BYTES=false
LAB_GAME_FORWARD_SERVER_BYTES=false
LAB_GAME_FORWARD_CLIENT_LENGTH=0
LAB_GAME_FORWARD_SERVER_LENGTH=0
```

The setter call failed inside the Lua/C++ binding before character login and
before network traffic. The full-version wire hypothesis is therefore still
`UNKNOWN`, not disproven; opcode `0x14` was not observed on this head. The
bounded heavy attempt is exhausted. The failure-stage classifier now maps this
outcome directly to `full_client_version_call_failed`, and the next action is a
network-free binding test/repair before another E2E is authorized.

Run `31722078520`, jobs `94521255896` and `94522602196`, exact head
`b196c5019a682ebdeb4a4dfba7cf762a5757e0a2`, was automatically selected by the
PR path filter after the focused binding test commit. The exact Linux build,
isolated bootstrap, WARP transport, HTTP login and tmpfs handoff passed. The
runtime again emitted `FULL_CLIENT_VERSION_CALL_FAILED=true` before character
login with zero bytes in either direction. This is a reproduction of the
binding defect, not new protocol evidence. CI run `31722078961` passed, but its
scope detector skipped the C++ test build; that run does not prove the new
binding test executed.

The focused test now invokes the actual `Client::registerLuaFunctions()`
registration and performs setter/getter readback without network access. The
repair replaces only the two full-version member-pointer bindings with explicit
static Lua functions using value-semantics `std::string`; the existing
`GameConfig` storage and login-packet selection contract are unchanged.

Run `31723213104`, jobs `94525071799` and `94527090954`, exact head
`8a3ea454747186a896ceb973dd55d20e7ba4946e`, proved that explicit static Lua
functions with value-semantics `std::string` did not repair the runtime call.
The exact Linux build and every pre-network gate passed, but the same
`FULL_CLIENT_VERSION_CALL_FAILED=true` marker occurred with zero directional
bytes. Artifact `9190396013`, digest
`sha256:624618e73a78216364efbd9e0b91fdfb3c132e255dda6b073c84c05c683fd16c`,
was inspected locally and contains both `getClientVersionString` and
`setClientVersionString` names and compiled symbols. A stale binary or absent
compiled binding is therefore disproven. The ineffective registration change
was reverted without another workflow run. The focused source test remains,
but CI scope detection did not execute it.

# Evidence classification

PROVEN:
- `synology-otclient-01` executes the canonical lab;
- official HTTPS authentication succeeds through verified changed WARP egress;
- the current response contains a usable session plus playdata without login error;
- the redacted tmpfs handoff is created and consumed successfully;
- credentials are not passed into the OTClient process environment;
- official 15.32 appearance protobuf parsing succeeds;
- official 15.32 staticdata parsing fails in current OTClient;
- OTClient runtime traffic remains behind proxychains/WARP in the observed runs.

DERIVED:
- the first remaining game-entry boundary is downstream of HTTP auth/session handoff and upstream of `GAME_START`;
- staticdata incompatibility can be tested independently from game-login protocol compatibility because the lab can preserve appearance data and attempt login without claiming staticdata support.

DISPROVEN:
- account authentication failure as the current blocker;
- missing/invalid HTTP playdata as the current blocker;
- tmpfs handoff creation/consumption as the current blocker;
- official 15.32 appearances parser incompatibility;
- unavailable `synology-otclient-01` runner as the current blocker.
- challenge-first behavior on the current official game endpoint: run `31695992918` produced neither client nor server bytes after the granted TCP connection.
- the missing encryption/checksum/client-version/login-pending/sequenced feature set as the sole no-response cause: run `31697097942` sent 143 client bytes and received zero server bytes after restoring them.
- the missing preview-state field as the sole no-response cause: run `31698702409` sent 144 client bytes and received zero server bytes.
- a raw/untrimmed runtime asset identifier as the sole no-response cause: run `31699422432` normalized it to 64 characters and still received zero server bytes.

UNKNOWN:
- whether the 1525-era OTClient game-login packet/features are accepted by official 15.32;
- the exact staticdata protobuf/schema delta that causes `loadStaticData()` to fail;
- whether `GAME_START` and authoritative local-player/map state can be achieved without additional protocol changes.

# Acceptance inventory

- [x] Canonical isolated lab exists in `blakinio/otclient`.
- [x] Canonical workflow executes on `synology-otclient-01`.
- [x] WARP changed-egress path is proven.
- [x] Current official 15.32 assets are materialized and reused without Git persistence.
- [x] Official HTTPS authentication succeeds.
- [x] Secret-bearing raw login data is kept in tmpfs and deleted.
- [x] One-shot game handoff is created and consumed.
- [x] 15.32 appearance data parses successfully.
- [x] 15.32 staticdata incompatibility is isolated.
- [x] First game-server connection/callback is proven; historical current-packet result is structured opcode `0x14`.
- [ ] Prove `GAME_START=true` or persist the exact post-login protocol incompatibility.
- [ ] After `GAME_START`, prove authoritative local-player/position/world state and leave character idle.
- [x] Keep PR #48 as historical evidence only; it is not the canonical implementation lane and does not supersede PR #284.
- [ ] Run final exact-head audit/CI and closeout only when the runtime objective is terminal.

# Next action

Finish exact current-main restack validation and push PR #284 only with force-with-lease against the verified historical remote head. Then run exactly one materially changed, owner-authorized Actions E2E using the current HTTP package identity, freshly verified current assets and exact-head OTClient binary handoff. If the game server still returns structured `0x14`, stop identical retries and require a promoted final official queue/wire serializer contract before another protocol mutation.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-23T15:15:00Z
track: otclient-global-login
track_alias: OTCLIENT-GLOBAL-LOGIN
head: ee27bb732617b6abf6891d347bbec25665a92f7d
source_pr_head: 69f9f0fa6dd390e57a11d828508753f7e45988ce
base_main: 5ac05b2640e818a1efc3e065e2ed4e501eaed058
branch: feat/OTC-20260813-tibia-global-login-lab
pr: 284
status: validating
context_routes:
  - official-Tibia game login via synology-otclient-01
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - .gitattributes
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
proven:
  - HTTP auth/session/playdata and one-shot tmpfs handoff already passed in prior physical runs
  - run 31702087216/job 94453443371 sent 230 game-login bytes, received 148 server bytes, and reached GAME_LOGIN_ERROR
  - run 31706716385/job 94469029667 decoded structured server opcode 0x14 with client+world relationship
  - current owner-hosted package metadata binds 15.32.bf29ac to packed 1fc26d66... and unpacked ed5469b9... size 52109920
  - merged Track A promotion 589 proves internal GameclientMessageLogin plus nested LoginRSAEncryptedBlock but not the final queue/TCP writer
  - credential-free bash syntax, 1532 injector rendering, Python syntax, diff-check and checkpoint validation pass on the restack worktree
  - workflow inspection found and repaired exact-head binary loss across container recreation
rejected_hypotheses:
  - challenge-first
  - missing restored legacy login features alone
  - missing preview-state field alone
  - raw runtime asset identifier alone
  - HTTP full build string as an assumed game-wire field
derived:
  - restack the existing PR net diff on exact current main instead of rebasing 79 stale incremental commits
  - drop experimental GameConfig/full-version product changes and related test/catalog/changelog entries
  - refresh current official assets through verified WARP before world entry
  - use current HTTP package identity 15.32.bf29ac
  - stage exact-head OTClient binary plus SHA in task-owned runtime volume and reverify it after container recreation
conflicts:
  - none
unknown:
  - current exact-head E2E outcome after the refreshed package/asset/binary inputs
  - final official TProtocolMessageQueue queue/wire serializer and exact first-packet wire contract
  - whether GAME_START can be reached without a further proven protocol delta
first_failure:
  marker: HISTORICAL_GAME_LOGIN_REJECTED_OPCODE_0x14
  evidence: run 31706716385/job 94469029667
changed_paths:
  - .gitattributes
  - .github/workflows/tibia-global-login-lab.yml
  - .gitattributes
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
  - tools/tibia-global-login-lab/README.md
  - tools/tibia-global-login-lab/evidence/official-1532-game-login-oracle.md
  - tools/tibia-global-login-lab/scripts/bootstrap.sh
  - tools/tibia-global-login-lab/scripts/game-socks-forward.py
  - tools/tibia-global-login-lab/scripts/http-login-preflight.sh
  - tools/tibia-global-login-lab/scripts/login-probe.sh
  - tools/tibia-global-login-lab/scripts/refresh-current-assets.sh
  - tools/tibia-global-login-lab/scripts/run-probe.sh
  - tools/tibia-global-login-lab/scripts/world-entry-probe-1532.sh
  - tools/tibia-global-login-lab/scripts/world-entry-probe.sh
validation:
  - command: wsl -d Ubuntu -- bash validate-lab.sh
    result: PASS
    evidence: bash syntax, 1532 injector render and embedded Python syntax all passed without Docker, secrets or Tibia traffic
  - command: python tools/agents/checkpoint.py task --require-checkpoint
    result: PASS
    evidence: current checkpoint contract validated locally
  - command: git diff --cached --check
    result: PASS
    evidence: staged current-main restack has no whitespace errors
  - command: Python yaml.safe_load workflow
    result: PASS
    evidence: workflow parsed with build-linux and probe jobs
blockers:
  - no static blocker to one fresh materially changed E2E; canonical secret use must remain inside the existing owner-authorized Actions workflow
next_action: finish exact restack validation, force-with-lease PR 284 only if remote head is still 69f9f0fa6, then run exactly one secret-bearing Track B workflow and classify the first current failure without identical retry
```
## 2026-08-23 current-main restack checkpoint

This checkpoint supersedes the stale 2026-08-13 `FULL_CLIENT_VERSION_CALL_FAILED` next action.

### Fresh repository state

```text
current main:        5ac05b2640e818a1efc3e065e2ed4e501eaed058
source PR #284 head: 69f9f0fa6dd390e57a11d828508753f7e45988ce
source divergence:  ahead 79 / behind 260
restack method:      current-main squash of the existing PR net diff
```

The restack deliberately drops the experimental `GameConfig` full-version product API, Lua binding, serializer substitution, focused test and catalogue/changelog entries. Those changes never reached the network in physical E2E and the later Track A oracle disproved treating the HTTP full build string as a proven game-wire requirement.

### Current official package identity

Owner-hosted current package metadata was re-read on 2026-08-23 and exactly binds:

```text
package version: 15.32.bf29ac
packed client:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked client: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size:   52109920
```

This matches the current trusted-main Track A executable fence. Active Track B HTTP login inputs therefore use `15.32.bf29ac`; the old `15.32.df7b29` remains historical only.

### Consumed later Track A evidence

Merged promotion #589 proves, for the historical `e6c244...` cut, that the native producer constructs `GameclientMessageLogin` with nested `LoginRSAEncryptedBlock` and sends the typed object through `TProtocolMessageQueue::sendLogin`. It does **not** prove that the protobuf object is emitted unchanged on TCP. Promoted auth/session evidence still leaves `TProtocolMessageQueue` final queue/wire serializer unknown.

Consequently Track B must not replace `ProtocolGame::sendLoginPacket()` with a guessed protobuf encoder. The next live attempt keeps the numeric 1532 game-wire behavior that already reached structured server opcode `0x14` and changes only newly proven stale lab inputs.

### New bounded lab delta

- refresh current `assets-current` catalog inputs through verified WARP before world entry;
- verify packed/unpacked hashes before persisting only required asset files in the task-owned runner volume;
- use current HTTP package identity `15.32.bf29ac`;
- emit `GAME_WIRE_FULL_VERSION_NOT_ASSUMED=true` and remove the failed full-version game-wire setter path;
- keep secrets only in the existing bounded tmpfs/Actions-secret handoff.

Credential/network use in this checkpoint: **none**. Local `bash -n` and credential-free 1532 injector rendering pass after repair.

### Next action

Finish exact restack diff/workflow/checkpoint validation, push PR #284 with force-with-lease only if clean, then run exactly one owner-authorized secret-bearing Track B workflow on the exact restacked head. Classify current HTTP auth and first game-server outcome; do not perform an identical retry if the result remains the structured `0x14` rejection.

### Restack correctness repair

Fresh workflow inspection found that the old multi-step probe could lose the freshly built exact-head OTClient binary: `bootstrap.sh` copied the artifact into one container, while the HTTP/world-entry steps later removed that container and recreated from the cached runtime image. The cache could therefore carry an older client binary.

The restack now stages the exact artifact plus its SHA-256 in the task-owned runtime volume during bootstrap. World entry requires both files, re-hashes the staged artifact, installs it into `/otclient/otclient`, and re-hashes the installed binary before launch. It emits only fixed non-secret markers and never logs binary contents.

This repair is part of the pre-E2E gate; it changes no OTClient product/protocol code.

## 2026-08-24 Molehill encrypted-handoff continuation checkpoint

This checkpoint supersedes the stale restack-only next action above.

Durable evidence:
`docs/agents/evidence/OTC-20260813-tibia-global-login-lab/20260824-molehill-encrypted-handoff.md`

Continuation prompt:
`docs/agents/prompts/OTCLIENT_GLOBAL_LOGIN_ENCRYPTED_HANDOFF_CONTINUE.md`

Current state:
- GitHub-hosted gameplay asset CDN access is proven insufficient (403 across Ubuntu/Windows/macOS; official launcher archive also 403);
- Molehill `tibia-kasm` has an exact, launcher-accepted current 15.32.bf29ac package/assets cache matching the trusted client SHA fence;
- `synology-otclient-01` is offline and Molehill has no approved unattended NAS control path;
- encrypted CMS one-shot handoff has passed local synthetic round-trip and contract validation but has not yet been physically proven with a real Tibia session handoff;
- no new protocol mutation is justified yet.

Exact next action: validate/publish the isolated encrypted-handoff producer lane, execute only that GitHub-Secret-bound producer, download only `handoff.cms` to Molehill, decrypt locally without logging plaintext, stage verified local current assets, and perform one bounded OTClient game-login. Success still requires real `GAME_START` plus authoritative in-game semantic evidence.

## 2026-08-26 encrypted producer stable-rejection checkpoint

This checkpoint supersedes the earlier Molehill-offline blocker. Durable evidence:
`docs/agents/evidence/OTC-20260813-tibia-global-login-lab/20260826-encrypted-producer-stayloggedin-error7-other.md`

Current state:
- Molehill returned online and was executable; the interrupted Track B WIP was reconciled without touching Track A.
- exact head `6c5a0baa24241dacb5ada6684715e3aad248d515` restores the historically proven `stayloggedin: True` login semantic and keeps raw rejection text secret.
- automatic encrypted producer run `32966019711` reached WARP, current asset identifier and HTTP 200, then returned stable redacted `errorCode=7` with category `other`.
- no plaintext-valid marker, ciphertext marker or artifact exists; the legacy full lab stayed skipped and CI passed.
- public research still provides no authoritative CipSoft mapping for numeric code 7.

Exact next action: do not perform a fourth unchanged or classifier-only login retry. Require genuinely new non-secret evidence that distinguishes or removes the hosted login rejection, such as owner-side successful official-client login/account-state confirmation or authoritative current login-service contract evidence. Once HTTP session/playdata is valid again, resume the existing encrypted handoff -> Molehill local decrypt -> fresh current-asset verification -> one bounded OTClient game-login flow.
