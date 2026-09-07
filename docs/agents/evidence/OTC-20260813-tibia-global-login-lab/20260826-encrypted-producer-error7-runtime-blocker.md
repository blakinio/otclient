# 2026-08-26 encrypted producer error-7 and Molehill runtime blocker

Task: `OTC-20260813-tibia-global-login-lab`
Track: `OTCLIENT-GLOBAL-LOGIN` / Track B only
Canonical PR: #284
Repository: `blakinio/otclient`

## Fresh source-of-truth snapshot

At this checkpoint:

- live `main`: `8085b40698d409bbacba3460001e8ddca4f6c84f`;
- PR #284 remains open/draft and mergeable;
- canonical branch: `feat/OTC-20260813-tibia-global-login-lab`;
- pre-checkpoint PR head: `599b951c7508e3a71a2842113cfdb3b52dc50a02`.

Do not trust these SHAs on a later invocation without resolving GitHub again.

## Producer harness repairs proven in this invocation

Commit `6e264798e3deb7c47123be71bd66048117af4a2f` fixed the encrypted emitter's stdin bug: the response-reduction heredoc now uses `docker exec -i`. A regression test was written RED first and then passed after the fix.

The same commit added two isolation guards:

1. the legacy `Tibia Global Login Lab` secret-bearing job is skipped for PR events from the canonical Track B branch while remaining manually dispatchable;
2. the encrypted producer has a latest-commit scope gate, so later docs-only checkpoints do not repeat the one-shot producer merely because the full PR diff still matches its path filter.

Fresh workflow evidence on that generation showed the legacy full-lab workflow skipped as intended. The encrypted producer passed WARP setup, current asset-identifier lookup, and HTTPS login HTTP 200, then reached a service-level login rejection instead of the prior heredoc failure.

Commit `599b951c7508e3a71a2842113cfdb3b52dc50a02` added redacted numeric rejection reporting. Its encrypted producer run `32942057475`, job `98094908992`, emitted only:

```text
LAB_ENCRYPTED_HANDOFF_WARP_READY=true
LAB_ENCRYPTED_HANDOFF_ASSET_IDENTIFIER_READY=true
LAB_ENCRYPTED_HANDOFF_HTTP_LOGIN_200=true
LAB_ENCRYPTED_HANDOFF_ERROR_CODE=7
```

No `handoff.cms` artifact was produced. No plaintext credential, session key, cookie/device cookie, play-session secret, or error-message text was logged or persisted to GitHub.

## Request-semantic regression discovered after errorCode=7

The encrypted handoff design explicitly says it must reuse the existing proven HTTPS login path. Current repository comparison shows one login-payload semantic delta:

- historically proven `tools/tibia-global-login-lab/scripts/http-login-preflight.sh`: `stayloggedin: True`;
- historically proven `tools/tibia-global-login-lab/scripts/world-entry-probe.sh`: `stayloggedin: True`;
- encrypted `.github/track-b-encrypted-handoff/emit.sh` at `599b951...`: `stayloggedin: False`.

All other login identity fields relevant to this comparison remain aligned (`email`, `password`, `type=login`, current `clientversion`, `clienttype=2`, current `assetversion`). Therefore a third secret-bearing attempt is justified only as a bounded A/B repair that restores the proven `stayloggedin: True` request semantic. It must not be an unchanged retry.

A public error-code search did not establish an authoritative CipSoft mapping for `errorCode=7`. Historical OpenTibia material associates `errorCode=6`, not 7, with the authenticator prompt. Do not label code 7 as credentials, 2FA, rate limiting, or account state without additional redacted evidence.

## Prepared redacted discriminator

A local WIP discriminator was being prepared to inspect `errorMessage` only inside the hosted Actions process and emit one closed category such as `temporary_block`, `authenticator`, `credentials`, `maintenance`, `rate_limit`, `account_state`, or `other`. It must never print the raw message. The contract test was first changed to RED for this discriminator; implementation validation was interrupted by the Molehill transport loss below.

Do not assume the uncommitted Molehill WIP survived or is correct. On resume, inspect the current worktree before reusing it and re-run the tests from scratch.

## Molehill consumer boundary

Before the disconnect, the task-owned key directory was freshly found under `%LOCALAPPDATA%\OTClientKasmVNC\trackb-handoff-key\`. Secret-free local verification proved:

```text
CERT_FINGERPRINT_MATCH=PASS
PRIVATE_KEY_PUBLIC_MATCH=PASS
```

against the committed public certificate and the expected fingerprint. The private key was never printed, copied, uploaded, or moved.

The existing Track B runtime containers were also freshly identified as:

```text
tibia-kasm     exited
otclient-kasm  exited
```

No Track A runtime/container/process was touched.

During classifier validation, Remote Desktop Commander first began timing out and then reported `Molehill-PC` offline. The final device discovery for this invocation showed Molehill offline and both Synology entries offline. That makes local ciphertext download/decrypt, current-asset re-verification/staging, and the one bounded OTClient game-login impossible in this invocation without violating the authority/safety boundary.

No producer attempt was launched after Molehill became unavailable, so there is no one-day ciphertext artifact stranded without its authorized consumer.

## Exact next action

1. Re-resolve live `main`, PR #284 head, current task record, and runtime. Do not reuse the SHAs/run IDs above without verification.
2. Require Molehill to be genuinely executable (`ping`/command succeeds), not merely stale `online` discovery metadata.
3. Inspect `C:\Users\barte\trackb-encrypted-handoff` for any uncommitted classifier WIP; keep only changes that belong to this Track B task.
4. TDD-lock the proven login request semantic: encrypted emitter must use `stayloggedin: True`, matching both historically successful login scripts, while still never promoting any device cookie into the encrypted handoff.
5. Keep/finish the redacted closed-category classifier for a nonzero login response; raw `errorMessage` must never be printed.
6. Run focused contract, embedded-Python syntax, shell syntax, diff-check, and current checkpoint validation. Revalidate the remote PR head immediately before writing.
7. Push one material repair commit to the existing branch/PR only. This is the third bounded producer hypothesis; do not perform another unchanged retry after it.
8. If the producer creates `handoff.cms`, consume only that exact ciphertext on Molehill: local certificate/private-key verification, local decrypt without plaintext output, structural handoff validation, current 15.32 asset hash re-verification/staging, then exactly one bounded OTClient game-login.
9. If that game-server result is structured `0x14`, do not resend the same packet or guess feature toggles. Require/consume promoted current-build wire-writer evidence first.
10. Success remains only real `GAME_START` plus semantic `IN_GAME`. Otherwise checkpoint the exact new blocker and evidence.

## Current outcome

`GAME_START=false` / `IN_GAME=false`.

Current hard blocker at checkpoint: authorized Molehill consumer/runtime is offline. Current upstream login fact: hosted encrypted producer reaches HTTPS 200 but the latest completed material attempt is rejected with redacted `errorCode=7`; a concrete proven-request semantic delta (`stayloggedin`) remains to be repaired before classifying that rejection as account/service state.
