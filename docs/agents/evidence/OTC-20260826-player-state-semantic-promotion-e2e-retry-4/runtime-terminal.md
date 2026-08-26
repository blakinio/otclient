# Player-state semantic promotion E2E retry 4 — terminal runtime evidence

## Terminal result

`AMBIGUOUS_POST_COMMIT` with a valid durable worker result.

- semantic promotion: **not eligible / not performed**
- no retry after COMMIT: **true**
- owner movement authorization: **consumed**
- physical action count: **1 under conservative effect semantics**
- exact one-tile causal delta: **not confirmed**
- possibly dispatched: **true**

A physical action count of 1 is conservative post-COMMIT effect accounting. It is not proof that the character moved exactly one tile.

## Source of truth

- trusted main: `d139481f894f0307e0fe58296acf615271bff0f1`
- task head that executed: `8e6ca5b6594425ee7d1d6679c5fda6f44714d1ee`
- PR: #712
- workflow run: `33012508829`
- job: `98322159507`
- runner: `synology-otclient-01`
- causal worker RCA/repair merged in PR #708; lifecycle archived/finalized in #709/#710

## Deterministic pre-runtime gate

All checks completed successfully before live admission:

- Track A runtime governance: PASS
- canonical live transition tests: 42/42 PASS
- Kasm existing-runtime probe tests: 10/10 PASS
- player-state causal worker tests: 22/22 PASS
- causal worker timeout-contract tests: 6/6 PASS
- causal worker dispatch-boundary tests: 2/2 PASS
- player-state resolver tests: 7/7 PASS
- `git diff --check`: PASS
- trusted-main fence: PASS

The separate repository CI run `33012509025` later failed only because the temporary task workflow lacked a final newline (`yamllint new-line-at-end-of-file`). This formatting failure occurred independently of, and before no part of, the already completed live causal result. The physical workflow itself completed successfully. The temporary physical workflow is removed during closeout rather than rerun.

## Fresh live admission

Controller prestate before claim:

- canonical registration: PRESENT
- lease generation before claim: 34
- registration generation: 7
- registration lease generation: 34
- PID: 646
- process start ticks: 1394843
- proof kind: `existing_runtime_adoption_v1`
- registration state: UNKNOWN
- state evidence: `NO_STRUCTURAL_BRIDGE`
- mutation authorized: false

Fresh authority sequence:

- lease acquired: generation 35
- Gate A: PASS
- fresh Kasm existing-runtime probe: PASS
- required authority transition decision: REBIND
- rebind: PASS
- Gate B: PASS
- target uniqueness: PROVEN
- typed baseline: PASS
- input carrier: PASS
- semantic preconditions: PASS

No login, credentials, relog, restart, character selection, process-memory write or unrelated gameplay action was used.

## One-shot causal action

Request:

- kind: `move`
- direction: `east`
- tiles: 1
- action hash: `ddcf3e9ee93118d61f9fa9462883ea08a6ff1b795efa89a0efac1feb077a85ad`

Guarded-dispatch READY:

- protocol: `track-a-guarded-dispatch-v1`
- status: READY
- fence digest: `fe29f7b96e0d6df3ba8e8e0a9ada462934303ca659329dc5a4006ca4b6907147`
- READY accepted exactly once
- budget reservation: PASS
- COMMIT accepted exactly once

Post-COMMIT worker result:

```text
TRACK_A_GUARDED_DISPATCH_RESULT={"action_hash":"ddcf3e9ee93118d61f9fa9462883ea08a6ff1b795efa89a0efac1feb077a85ad","effect_count":1,"reason_code":"RECONCILIATION_DEADLINE_EXHAUSTED","status":"AMBIGUOUS"}
PLAYER_STATE_E2E_NO_RETRY=true
PLAYER_STATE_E2E_WORKER_STATUS=AMBIGUOUS
PLAYER_STATE_E2E_WORKER_REASON=RECONCILIATION_DEADLINE_EXHAUSTED
PLAYER_STATE_E2E_PHYSICAL_ACTION_COUNT=1
PLAYER_STATE_E2E_POSSIBLY_DISPATCHED=true
PLAYER_STATE_E2E_RESULT=AMBIGUOUS_POST_COMMIT
PLAYER_STATE_E2E_SEMANTIC_PROMOTION_ELIGIBLE=false
```

This is materially better diagnostic behavior than retry 3: the repaired worker/parent path returned a valid durable terminal `AMBIGUOUS` envelope instead of `guarded_dispatch_worker_failed` / no valid result. It still does not prove the exact one-tile semantic delta.

## Release and terminal policy

- canonical lease generation 35: RELEASED
- controller task after release: none
- controller session after release: none
- `PLAYER_STATE_E2E_RELEASE=PASS`
- retry after COMMIT: forbidden and not performed
- semantic promotion: forbidden and not performed

Any future physical causal attempt requires a new, separate explicit owner authorization. This retry-4 authorization cannot be reused.