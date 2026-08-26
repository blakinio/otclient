# Player-state semantic promotion E2E retry 2 — terminal runtime evidence

## Result

`AMBIGUOUS_POST_COMMIT_NO_VALID_RESULT`.

The single owner-authorized causal attempt crossed the irreversible `COMMIT` boundary after all required gates passed, but the one-shot causal worker did not return a valid result before the canonical guarded-dispatch worker timeout. The attempt is therefore conservatively classified as possibly dispatched and consumed. No retry is permitted, and no player-state semantic promotion is justified.

## Trusted source of truth

- trusted `main`: `8085b40698d409bbacba3460001e8ddca4f6c84f`
- terminal prior PRs revalidated before admission: `#694`, `#696`, `#697`
- Draft PR: `#698`
- controlled workflow head: `56f60bbf5d84eb43d5722349e445e99c5cb3839d`
- workflow run: `32944297164`
- self-hosted job: `98101615158`
- runner: `synology-otclient-01`
- job conclusion: `success` (the workflow records terminal fail-closed/ambiguous semantic outcomes without converting them into an Actions infrastructure failure)

## Deterministic pre-runtime verification

On exact workflow head `56f60bbf5d84eb43d5722349e445e99c5cb3839d`:

- Track A agent runtime governance: `PASS`
- canonical live transition suite: `42/42 PASS`
- Kasm existing-runtime probe suite: `10/10 PASS`
- one-shot causal worker suite: `11/11 PASS`
- player-state resolver suite: `7/7 PASS`
- `git diff --check`: `PASS`
- exact trusted-main fence: `PASS`

## Fresh authority and semantic gates

The final controlled attempt acquired canonical lease generation `33`.

Required sequence:

1. Gate A: `PASS`.
2. Fresh exact-target Kasm probe: `PASS`.
3. Authority transition decision: `REBIND` because the authoritative registration was already on the current boot epoch and its exact PID/start identity matched while its lease generation trailed the newly acquired controller generation.
4. Canonical generation rebind: `PASS`.
5. Gate B: `PASS`.
6. Target uniqueness: `PROVEN`.
7. Semantic preconditions: `PASS`.
8. Stable typed player-position baseline across two read-only reads 0.5 s apart: `(32546,32504,7)`.

Earlier in this same task, fresh attempt 1 encountered the prior-boot authoritative registration. It selected only the reviewed trusted-main `BOOT_EPOCH_RECOVERY` path from PR #696, passed that metadata-only recovery, then passed Gate B and target uniqueness before failing semantic preconditions pre-COMMIT with zero physical action. This confirms that ordinary rebind was not substituted across the boot-epoch discontinuity.

## Irreversible boundary and terminal ambiguity

The controlled request was exactly one eastward tile.

Guarded dispatch produced a valid READY envelope with the expected action hash and a 64-hex fence digest. The controller then atomically reserved the persistent one-shot budget marker and sent `COMMIT` exactly once:

- `PLAYER_STATE_RETRY2_READY=true`
- `PLAYER_STATE_RETRY2_BUDGET_RESERVATION=PASS`
- `PLAYER_STATE_RETRY2_COMMIT=true`

A fresh Kasm exact-target probe still passed after COMMIT. The worker then exceeded the 30-second guarded-dispatch worker timeout:

- `TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout`
- `PLAYER_STATE_RETRY2_NO_RETRY=true`
- `PLAYER_STATE_RETRY2_RESULT=AMBIGUOUS_POST_COMMIT_NO_VALID_RESULT`
- `PLAYER_STATE_RETRY2_POSSIBLY_DISPATCHED=true`
- `PLAYER_STATE_RETRY2_PHYSICAL_ACTION_COUNT=1`

`PHYSICAL_ACTION_COUNT=1` is the conservative consumed-attempt accounting required after COMMIT; the logs do **not** prove that the character actually changed tile. Because no valid causal worker result exists, there is no exact before/after one-tile differential and therefore no causal semantic proof.

Canonical lease generation `33` was released successfully after the terminal classification.

## Prohibited actions and promotion decision

No login, credentials, relog, restart, character selection, process-memory write, injection, or additional gameplay action was performed by this task.

The single movement authorization is terminally consumed. There will be no automatic or manual movement retry under this task after COMMIT.

Semantic promotion decision: **NOT PERFORMED**. `tools/tibia_re_surveyor/player_state.py` and the Control Center Surveyor provider remain on the existing candidate-only player-position semantic contract.

## Closeout requirement

The task-specific dispatch workflow must remain removed. The task-specific causal worker/test are ephemeral and are removed from the final evidence-only candidate. Closeout requires an independent audit of this exact terminal classification, exact-final-head CI, merge of the evidence-only PR, archive, and ownership release.