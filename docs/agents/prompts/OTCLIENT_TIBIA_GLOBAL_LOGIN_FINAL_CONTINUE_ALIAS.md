# OTCLIENT-TIBIA-GLOBAL-LOGIN final continuation alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
track_id: otclient-global-login
role: final_implementation_and_e2e_closeout
canonical_pr: 284
canonical_branch: feat/OTC-20260813-tibia-global-login-lab
default_execution_class: github_hosted
default_runtime_access: track_b_only
run_scope: autonomous_until_terminal_or_real_external_stop
continuation_policy: continue_without_restart_and_without_identical_secret_retry
codex_spark_allowed: true
```

## Owner invocation

```text
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
```

## Resolution contract

This alias continues existing work. Do **not** restart the project, redo accepted Track A reverse engineering, or reopen already-promoted questions.

At startup resolve GitHub again and treat fresh repository state as authority. The checkpoint below is only a floor/reference and must not override newer state:

```text
trusted main after Track A lifecycle closeout:
  a670d4c8597a77b00c28b2c8a71d346329ad28b7

canonical Track B PR:
  #284
  branch feat/OTC-20260813-tibia-global-login-lab
  checkpoint head 5a0b0879c43acbbf2d6e5d83b78ee4ceab62a044

clean loginservice-request promotion:
  #734 merged as 4c0454af60a14321b363c3dc7d1f224a46e64153

Track A loginservice lifecycle closeout:
  #735 merged as a670d4c8597a77b00c28b2c8a71d346329ad28b7

source research:
  #733 closed UNMERGED as consumed/superseded
```

Mandatory startup reads from the fresh trusted base:

```text
AGENTS.md
docs/agents/README.md
docs/agents/evidence/OTC-20260828-current-loginservice-request-promotion/20260828-coordinator-promotion.md
docs/agents/evidence/OTC-20260828-current-loginservice-request-promotion/result.json
docs/agents/tasks/archive/OTC-20260828-current-loginservice-request-contract.md
docs/agents/tasks/archive/OTC-20260828-current-loginservice-request-promotion.md
```

Then read from the exact current head of PR #284:

```text
docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
tools/tibia-global-login-lab/evidence/official-1532-game-login-oracle.md
.github/workflows/tibia-global-login-lab.yml
.github/workflows/tibia-global-login-encrypted-handoff.yml
.github/track-b-encrypted-handoff/emit.sh
tools/tibia-global-login-lab/scripts/http-login-preflight.sh
tools/tibia-global-login-lab/scripts/world-entry-probe.sh
tools/tibia-global-login-lab/scripts/world-entry-probe-1532.sh
tools/tibia-global-login-lab/tests/ephemeral_runner_contract.py
tools/tibia-global-login-lab/tests/current_login_send_contract.py
tools/tibia-global-login-lab/tests/tibia_global_login_wire_contract.cpp
src/client/tibiagloballoginwire.h
src/client/protocolgame.cpp
src/framework/net/outputmessage.cpp
```

## Already completed — do not redo

The following work is accepted/promoted or already implemented on Track B and must be consumed rather than rediscovered:

1. The legacy official-game login body is stale. Current 15.32 uses typed protobuf `GameclientMessage -> field 1000 -> GameclientMessageLogin` with nested `LoginRSAEncryptedBlock`; Track B already contains the current typed encoder/transcoder work.
2. The current typed wire contract, XTEA key byte conversion, current sequence framing seam, client-first path, and integration source contract were developed RED -> GREEN in hosted checks.
3. The current Linux package layout is split: `tibiaclient-linux-current/package.json` contains the client package (`bin/...`) and no asset catalogue rows. Current game assets come from `https://static.tibia.com/launcher/assets-current/assets.json` and `.sha256` through the task-owned WARP SOCKS path.
4. Track B has the stronger terminal oracle. Success is not merely a callback; require both `GAME_START=true` and `IN_GAME=true`, where the latter requires online state, a local player and a numeric position without logging the position values.
5. The one-shot marker `.run-current-typed-e2e` was removed after the last blocked attempt. Keep it absent until the HTTP-only repair below is proven.
6. Source PRs/workflows/analyzers used for Track A research remain unmerged. Only their promoted facts on trusted `main` are authority.

## Last physical result — classify correctly

The latest qualified full workflow was:

```text
run 33126310912
probe job 98705374273
exact Track B head used by that run:
  156384207e764c572c8b5dd709ec35b27d8d51e7
```

It proved before the failure:

```text
current wire/package/harness contracts PASS
exact native Linux OTClient build PASS
current split package manifest PASS
current WARP asset manifest/hash PASS
bootstrap PASS
redacted HTTP request reached HTTP 200
```

But the login service returned no session/playdata and a redacted service rejection:

```text
LAB_HTTP_PREFLIGHT_HAS_SESSION=false
LAB_HTTP_PREFLIGHT_HAS_PLAYDATA=false
LAB_HTTP_PREFLIGHT_HAS_ERROR_CODE=true
LAB_HTTP_PREFLIGHT_ERROR_CODE=7
LAB_TRANSIENT_HTTP_LOGIN_STATUS_200=true
official login response rejected
```

Therefore **no current typed game-login packet was sent in that run**. It is incorrect to classify that run as a game-server failure or `0x14` retry. The blocker is upstream at the loginservice request contract.

After that failed attempt the marker was removed; current PR #284 checkpoint head became `5a0b0879c43acbbf2d6e5d83b78ee4ceab62a044`.

## Newly promoted exact-current loginservice request fact

Trusted main now contains an exact-current static proof for official Linux Tibia `15.32.75d4a0`:

```text
exact client packed sha256:
  075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
exact client unpacked sha256:
  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
exact client unpacked size:
  52105824
primary loginservice request builder FDE:
  0xe1e780..0xe1eb21
```

The primary builder has these unconditional keys:

```text
type
email
password
stayloggedin
devicecookie
clienttype
operatingsystem
clientversion
assetversion
```

Accepted values/provenance relevant to Track B:

```text
type = "login"
operatingsystem = QSysInfo::prettyProductName()
```

The current Track B request already provides the other eight unconditional keys but is missing exactly:

```text
operatingsystem
```

The following keys are conditional and must **not** be synthesized when the corresponding current state is absent:

```text
token
deviceverificationcode
trusteddevicetoken
emailcode
loginconfirmationcode
loginconfirmationtoken
```

The following belong to other JSON builders and must **not** be added to the primary login request:

```text
fromtimestamp
isreturner
showrewardnews
viewedid
```

Do not infer an authoritative meaning for `errorCode=7` unless new evidence proves it. Historical redacted classification was `other` and is not a credential/account/2FA diagnosis.

## Required next implementation — TDD first

### Task 1 — lock the current loginservice request contract

Use TDD before mutating the secret-bearing producer.

1. Extend the existing focused Track B contract test so it fails unless every Track B loginservice request producer contains the mandatory `operatingsystem` field and does not synthesize the conditional token/code fields.
2. Cover at minimum:

```text
.github/track-b-encrypted-handoff/emit.sh
tools/tibia-global-login-lab/scripts/http-login-preflight.sh
tools/tibia-global-login-lab/scripts/world-entry-probe.sh
```

3. Run the focused hosted/no-secret contract and record the real RED result.
4. Implement the smallest repair. On Linux, derive an equivalent current pretty OS product name from the runtime environment; do not hard-code a stale distro string. Verify the chosen Linux derivation against the `QSysInfo::prettyProductName()` semantic before using it.
5. Run the same focused contract and record GREEN.
6. Preserve secret redaction. Do not print email, password, device cookie, session key, raw response message, world identity or character identity.

### Task 2 — one HTTP-only material validation

After Task 1 GREEN, perform **one** secret-bearing HTTP-only validation whose material delta is the newly promoted mandatory `operatingsystem` field.

Prefer the existing encrypted handoff producer because it stops at the loginservice/session handoff boundary and does not require a game-login packet. Its path gate may run automatically when its producer files change; account for that so only one material attempt occurs.

Required outcomes:

A. If loginservice succeeds:

```text
HTTP 200
valid session
valid playdata/worlds/characters
non-empty session key
ciphertext-only handoff may be produced
no plaintext secret artifact uploaded
```

Then the upstream blocker is removed and Task 3 is authorized.

B. If `errorCode=7` or another service rejection persists:

- do not repeat the same request;
- do not arm the game E2E marker;
- checkpoint the exact redacted result in the Track B task/evidence;
- continue only if there is a genuinely new evidence-derived request delta or a real external owner/account-state confirmation. Do not guess.

### Task 3 — one current typed game-login E2E only after HTTP success

Only after Task 2 proves valid session/playdata:

1. Re-resolve exact PR #284 head and current main.
2. Ensure focused wire, integration and ephemeral-runner contracts are GREEN.
3. Ensure the main lab workflow builds the exact native Linux OTClient before any secret-bearing game probe.
4. Add/arm the one-shot marker exactly once and record why this is not an identical retry. The material chain must include the current loginservice request repair and existing current typed game-login implementation.
5. Freeze the branch while the one-shot run is active; do not create unrelated commits that could schedule a second probe.
6. Require the real terminal oracle:

```text
TIBIA_GLOBAL_LAB_GAME_START_PROVEN=true
TIBIA_GLOBAL_LAB_IN_GAME_PROVEN=true
```

Only that is success.

If the game server returns a structured rejection such as legacy-observed `0x14`, do not repeat the same packet. Persist numeric/redacted evidence and require a new evidence-derived payload change before another secret-bearing attempt.

## Final closeout of PR #284

If and only if the runtime objective is terminally resolved:

1. Remove the one-shot marker before any final documentation/restack commit.
2. Update `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` and durable Track B evidence with exact runs/jobs/heads and the final outcome.
3. Re-resolve fresh trusted `main`.
4. Restack PR #284 on current `main` so its merge-base is current and historical Track A files do not produce false governance failures. Preserve Track B net changes; do not resurrect superseded Track A source workflows/analyzers.
5. Re-run focused contracts, full required CI and governance on the exact restacked head.
6. Inspect review threads/reviews and mergeability.
7. Merge #284 only when the exact-head diff is Track B-appropriate and required checks are genuinely green.
8. Archive/release the Track B task only after the merge and final current-main verification.

## Execution and safety rules

- Work autonomously; do not ask the owner to repeat already-known repository state.
- GitHub is source of truth. Re-resolve state immediately before every write/merge.
- Use GitHub-hosted runners for builds/static tests and secret-bearing lab jobs whenever the existing workflow supports them.
- Do not use the owner's desktop/Molehill for ordinary compilation, reverse engineering or repeated E2E. Use it only if current repository authority explicitly requires a task-owned consumer action unavailable on hosted runners.
- Keep Track A and Track B ownership isolated.
- No OCR/Tesseract.
- No raw official client upload.
- No credentials/session/cookies in commits, comments, logs or artifacts.
- No identical secret-bearing retry without a material evidence-derived change.
- Do not add speculative login fields.
- Do not rename UNKNOWN semantics into guessed user-facing meanings.
- User explicitly authorizes Codex Spark for this continuation; use it when useful, while still independently verifying all outputs and repository state.

## Terminal reporting

When finished, report only fresh verified state: current main SHA, #284 final head/merge SHA, exact successful/failing workflow run and job IDs, `GAME_START`/`IN_GAME` result, and any true remaining external blocker. Never claim completion from green static tests alone.
