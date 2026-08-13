# OTC-20260813 — Direct OTClient → Tibia Global auth checkpoint

## Scope

This report persists the direct-protocol findings discussed during `OTCLIENT-TIBIA-RE` continuation. It is complementary to the newer runtime-bridge/current-client evidence in `docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md`; it does **not** roll that task back to an older head or replace later exact-client evidence.

```yaml
repository: blakinio/otclient
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
branch_head_observed_before_write: c08beb28a0acb89b039906aaff70de9470d9dfa5
recorded_at: 2026-08-13
lane: direct_otclient_to_tibia_global
success_state: NOT_PROVEN
```

## Verified facts

### Direct hosted protocol lane exists

`.github/workflows/otclient-global-login-hosted.yml` is a GitHub-hosted direct-auth probe for OTClient against the public Tibia login endpoint. The relevant path uses WARP and protocol/runtime diagnostics rather than OCR/image-to-text. Credentials remain workflow secrets and the workflow is designed to retain only aggregate diagnostics, not secret payload values or proprietary client bytes.

The probe implementation is `tools/otclient_global_login_probe.py`.

### Historical hosted run reached the protocol-aware auth step

Historical workflow run `31649027857`, job `94289067069`, on head `2ad242cd04540d034efbf38796ca0b52475e0ba3`, completed with `failure`.

Observed step boundary:

```text
Checkout                                                    PASS
Verify and materialize minimal official reference package   PASS
Start isolated WARP SOCKS5 tunnel                           PASS
Dry-run OTClient direct auth probe (no credentials sent)    PASS
Run protocol-aware OTClient GoRSA-compatible auth trace     FAIL
Upload aggregate auth diagnostics                           PASS
Upload raw OpenSSL oracle trace                             PASS
```

Therefore the run got past checkout, official-reference materialization, WARP setup and the dry-run boundary before failing in the protocol-aware direct-auth trace.

This run **predates the current PR #48 head** and is historical evidence only. It is not exact-head acceptance evidence.

### Exact auth-trace failure cause is still UNKNOWN in this checkpoint

The failed step is known, but the exact framing/RSA/protocol error has not been durably established in this report. Do not claim a specific root cause until the retained aggregate diagnostics/job output are inspected and matched to one concrete failure condition.

### Physical world entry remains unproven

No direct-OTClient run cited here proves an authenticated game session, physical character entry into the world, an authoritative player position, or decoded live world-map records. The programme must continue to report `NOT_PROVEN` until those semantic acceptance conditions are met.

## Derived direction

**INFERENCE:** because the historical run passed WARP, reference materialization and dry-run before failing inside the protocol-aware auth trace, the shortest candidate repair loop for this lane is to inspect and correct the direct protocol/auth implementation in `tools/otclient_global_login_probe.py` rather than making another blind GUI, OCR, renderer or WARP change.

This inference is conditional on the exact failure diagnostics. A code change must target one evidenced framing/RSA/auth mismatch, not a guessed one.

## Official-client semantic fallback

The official-client lane remains a fallback and a semantic reference source. The active task already proves the relevant Qt owners, including:

```text
TCharacterSelectionController
TAuthenticationProcessController
TLoginRequestUploader
TGameserverLoginProcessController
TGameClient
IGameSession
TGameserverGameSession
```

The active task also records that the earlier QMeta filter mixed methods owned by different QMetaObjects. Accordingly, a previous filter/gate miss must not be interpreted as proof that `TGameserverLoginProcessController` or the other critical controllers were absent.

## Next bounded actions for this lane

1. Inspect the exact failure output/aggregate diagnostics for run `31649027857`, job `94289067069`.
2. Form one concrete protocol-auth hypothesis from that evidence.
3. Make at most one bounded correction to framing/RSA/auth handling in `tools/otclient_global_login_probe.py` before rerunning the hosted probe.
4. If auth succeeds, advance the probe to the game-session transition rather than returning to visual/OCR automation.
5. Accept success only after semantic world-entry evidence is produced.

## Acceptance gates

A successful result requires all of the following, not merely a successful HTTP/login response:

- authenticated session reaches the game-session/world-entry transition;
- the intended character is physically in the world;
- the relevant client/probe process remains alive through the proof window;
- required transport remains WARP-constrained with no unintended direct egress;
- semantic decoded game evidence proves world state, preferably live map and/or authoritative player-position data;
- no OCR/image-to-text marker is used as semantic proof of `IN_GAME`.

## Safety invariants

- Never persist or print credentials, session tokens, cookies or character/account secrets.
- Never commit or upload proprietary CipSoft binaries/assets/payload bytes.
- Do not weaken anti-cheat or attempt to bypass it; this work is limited to compatibility/runtime observation and the owned OTClient implementation.
- Do not claim world entry from screenshots, pixel differences, window titles or OCR.
- Do not spend owner-funded Codex/API quota or owner tokens without separate explicit authorization.
