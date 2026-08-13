---
task_id: OTC-20260813-tibia-global-login-lab
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: infrastructure
phase: live-world-entry
branch: feat/OTC-20260813-tibia-global-login-lab
base_branch: main
created: 2026-08-13T09:10:00+02:00
updated: 2026-08-13T12:55:00+02:00
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
- [ ] Make PR #48 intentionally terminal as superseded once all reusable evidence is ported.
- [ ] Run final exact-head audit/CI and closeout only when the runtime objective is terminal.

# Next action

Run the canonical E2E with the independent SOCKS5 game-port probe. If SOCKS TCP is granted but OTClient still times out, inspect proxychains integration; if both time out, persist the exact WARP/game-port reachability boundary and falsify it from another approved lab egress before terminal classification.
