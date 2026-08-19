# Track A native login operator

Permanent entrypoint: `.github/workflows/track-a-native-login.yml` (`Track A native login`).

This operator is the canonical repository path for a user-authorized one-shot native login on the current Track A KasmVNC runtime. It promotes the successful no-kill sequence proven by PR #599 and must not be reconstructed as an ad-hoc Remote Desktop credential command.

## Agent invocation

Use this user prompt:

> Uruchom kanoniczny Track A no-kill native login workflow z `main`. Zezwalam na jednorazowe użycie `TIBIA_TEST_EMAIL` i `TIBIA_TEST_PASSWORD` wyłącznie dla tego runu przez bounded native-auth ingress. Nie używaj bezpośredniego Remote Desktop secret-ingress ani GUI do wpisywania danych.

The agent must first read current Track A admission/governance, verify the workflow is present on live `main`, and establish fresh authority for the exact runtime. The user sentence above is credential-use authorization only; it does not manufacture runtime ownership, Gate A/Gate B, bootstrap or target uniqueness.

## Dispatch

Dispatch `Track A native login` from `main` with input:

`authorization=ONE_SHOT_NATIVE_LOGIN`

Do not dispatch from a feature branch or substitute a copied temporary workflow. The GitHub Actions run on the `synology-otclient-01` self-hosted runner is the secret boundary; do not invoke `secret-ingress` directly through Remote Desktop Commander.

## Invariants

The workflow must preserve all of these properties:

- exact official-client fence: size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- credentials are supplied only to the one bounded authentication step and are unset afterwards;
- no credential values are printed or persisted;
- no GUI credential entry, OCR, image matching, coordinate login or blind keyboard/mouse input;
- after native auth handoff, the replacement client is never killed or restarted by the workflow;
- `bridge.sock` and `character.sock` must resolve through `SO_PEERCRED` to the live replacement client PID;
- `character_count != 1` fails closed; only `CONFIRM_UNIQUE` is permitted;
- success requires `validated_hits == 1` for `player_protocol_handler`, `gameserver_game_session` and `worldmap_handler`.

## Listener prerequisite

The workflow intentionally fails before secret access if `auth.sock` is absent or stale. Recreating the one-shot listener is a separate pre-auth runtime mutation and must be performed only after current Track A admission proves that the target client is the authorized logged-out runtime. Never add a post-auth restart fallback to this operator.

If preflight fails, inspect the exact failed prerequisite. A preflight failure does not consume the one-shot credential authorization.

## Expected terminal markers

A successful run contains:

```text
AUTHORIZATION_GATE=PASS
EXACT_HELPER_RUNTIME=PASS
NATIVE_AUTH_INGRESS=PASS_WITH_PROCESS_HANDOFF
SECRET_VALUES_LOGGED=false
SECOND_SECRET_ATTEMPT=false
CLIENT_TERMINATED_BY_WORKFLOW=false
HANDOFF_HELPER_PROVENANCE=PASS
NATIVE_CHARACTER_COUNT=1
NATIVE_CHARACTER_CONFIRM=PASS
RESULT=SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME=PASS
```

`PASS_RESPONSE` is also a valid bounded authentication result when no process handoff causes the response channel to disappear.
