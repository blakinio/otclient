---
task_id: OTC-20260813-tibia-global-login-lab
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: infrastructure
phase: live-world-entry
branch: feat/OTC-20260813-tibia-global-login-lab
base_branch: main
created: 2026-08-13T09:10:00+02:00
updated: 2026-08-13T13:51:00+02:00
risk: medium
related_pr: 284
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
modules_touched:
  - legacy-analysis
  - github-actions
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - PR #48 runtime evidence as migration input only
  - synology-otclient-01 self-hosted runner
cross_repo_tasks: []
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
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

The owner explicitly restored this task and PR #284 as the canonical active
OTCLIENT-TIBIA-RE implementation lane for the repository's own OTClient on
2026-08-13. PR #48 is historical evidence only and must not replace this lane.

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
client_version: 15.32.df7b29
client_executable_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
login_clienttype: 2
assetversion: official_64_hex_assets_json_sha256
```

All static/runtime offsets from earlier work remain version-fenced to that exact executable hash.

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

Product support still declares last supported client 1525. The lab uses the existing Lua binding `g_gameConfig.setLastSupportedVersion(1532)` rather than modifying production `game.cpp`/`game.lua`. Product files owned by other tasks are not mutated.

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
- whether `g_game.loginWorld()` with appearances-only state reaches a game-server TCP/session callback;
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
- [ ] Prove first game-server connection/callback after appearances-only login attempt.
- [ ] Prove `GAME_START=true` or persist the exact post-login protocol incompatibility.
- [ ] After `GAME_START`, prove authoritative local-player/position/world state and leave character idle.
- [x] Keep PR #48 as historical evidence only; it is not the canonical implementation lane and does not supersede PR #284.
- [ ] Run final exact-head audit/CI and closeout only when the runtime objective is terminal.

# Next action

Run the canonical E2E with fixed non-secret login-error category markers and continue from the exact returned category.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T13:10:00Z
head: 1d8c3e900e42a48137e5209ee590bd6d7a315f5b
branch: feat/OTC-20260813-tibia-global-login-lab
pr: 284
status: validating
context_routes:
  - official-Tibia game login via synology-otclient-01
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
proven:
  - run 31702087216/job 94453443371 preserved version 1532, sent 230 client bytes, received 148 server bytes, and reached GAME_LOGIN_ERROR
derived:
  - first remaining boundary is the server-returned game-login rejection category
unknown:
  - exact non-secret category of the server GAME_LOGIN_ERROR response
conflicts:
  - none
first_failure:
  marker: GAME_LOGIN_ERROR=true
  evidence: run 31702087216/job 94453443371 at 76d30527c718650dd50316140847f07154449342
rejected_hypotheses:
  - challenge-first: run 31695992918 produced zero bytes in both directions
  - missing restored legacy login features alone: run 31697097942 still received zero server bytes
  - missing preview-state field alone: run 31698702409 sent 144 client bytes and received zero server bytes
  - raw runtime asset identifier alone: run 31699422432 normalized it and still received zero server bytes
changed_paths:
  - tools/tibia-global-login-lab/scripts/world-entry-probe-1532.sh
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
validation:
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md --require-checkpoint
    result: PASS
    evidence: checkpoint schema validated locally before commit
blockers:
  - none
next_action: run the exact-head canonical E2E with fixed non-secret login-error category markers and continue from the returned category
```
