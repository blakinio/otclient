# Track A gameWindowState trusted-main preflight blocker

Date: 2026-08-28
Task: `OTC-20260828-game-window-state-qualification`

## Terminal qualification state

`LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION_PASS` was **not** reached.

Terminal result for this execution:

`FAIL_CLOSED_BLOCKER_CANONICAL_REGISTRATION_CLIENT_VERSION_MISMATCH`

The bounded reader itself was not started. No process-memory observation was performed.

`IN_GAME_CLAIMED=false`

`semantic_promotion_performed=false`

## Trusted-main execution

Protected `main` was freshly verified at:

`356f49bfebab5f758dc1f95b1a74ef1d6e741b41`

That commit is the squash merge of PR #756, which added the memory-free readiness preflight and canonical read-only admission contract.

The repository-owner exact command was posted on merged PR #756:

`PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`

GitHub Actions evidence:

- workflow: `Track A game window state qualification`;
- run: `33193448068`;
- job: `98924502254` (`Continuous read-only gameWindowState qualification`);
- exact head: `356f49bfebab5f758dc1f95b1a74ef1d6e741b41`;
- conclusion: `failure`.

## Fail-closed point

The workflow successfully completed the repository/static trust gates before the failure:

- exact trusted-main checkout and remote-main equality proof;
- repository checkpoint remained `runtime_access: none`;
- mutation/login/character-selection/gameplay/GUI/process-control authority remained false;
- canonical Gate A / generation rebind / Gate B / bootstrap / target-uniqueness repository claims remained `NOT_APPLICABLE`;
- current repository exact-client fence validation passed;
- exact bounded preflight command validation passed.

The first runtime-identity step then failed in:

`Resolve canonical registration and current ownership`

with the exact fail-closed error:

`REGISTRATION_CLIENT_VERSION_MISMATCH`

No raw registration value is retained in this evidence. The only proven fact is that the authoritative `runtime-registration.json` `client_version` does not equal the trusted-main required exact build version `15.32.75d4a0`.

## What remains unknown

Because the workflow stopped at the registration-fence gate, this run did **not** authorize or establish:

- whether the registered PID/start identity is still live;
- whether the registered size/SHA matches the current exact build;
- whether exactly one current official-client candidate exists across running Docker containers;
- whether the current live client, if any, is the exact build `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- `target_uniqueness: PROVEN`;
- any `gameWindowState` value in any UI phase.

These facts must not be inferred from historical runs or the stale registration.

## Safety proof

All later steps were skipped, including:

- `Re-prove global unique exact target`;
- `Persist and validate fresh read-only admission`;
- `Revalidate admission immediately before any observation`;
- `Report memory-free logger readiness preflight`;
- `Build in-memory resolver bundle`;
- `Capture continuous bounded state log`;
- qualification artifact validation/upload.

Therefore this failed preflight performed no `/proc/<pid>/mem` access and no client/process/GUI mutation.

## Authority boundary

PR #754 advanced repository canonical fence constants from the superseded `15.32 / 52109920 / ed5469b9...` authority to the exact-current `15.32.75d4a0 / 52105824 / d1a168...` authority. The live authoritative registration was not silently rewritten by that repository change.

Current canonical-live governance explicitly rejects ad-hoc manual editing of `runtime-registration.json`. Existing reviewed transitions cover bootstrap, adoption, generation rebind and specific stale-registration recovery cases; this Track A gameWindowState qualification lane is not authorized to invent or perform an unreviewed canonical registration migration.

The next legal runtime step is therefore a **fresh canonical admission/reconciliation under the canonical-live governance lane**, after which this task may rerun `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. Only a successful preflight may make the continuous logger READY and justify owner manual phase traversal.

## Conclusion

`LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION=BLOCKED_FAIL_CLOSED`

`BLOCKER=CANONICAL_REGISTRATION_CLIENT_VERSION_MISMATCH`

`PROCESS_MEMORY_OBSERVATION_PERFORMED=false`

`IN_GAME_CLAIMED=false`

`semantic_promotion_performed=false`
