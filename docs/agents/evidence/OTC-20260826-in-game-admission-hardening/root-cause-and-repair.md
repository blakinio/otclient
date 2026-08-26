# In-game admission hardening — root cause and repair

## Result

`ROOT_CAUSE_PROVEN_AND_REPAIRED`

This task is repository-only. It performed no official-client/runtime observation, login, relog, restart, character selection, GUI/gameplay input, process-memory write, client mutation, READY, COMMIT, or physical action.

## Source of truth

- source protected main: `8a9315e1cd621a5b868010deeec2578266547663`
- implementation PR: #715
- RETRY-4 source evidence: `docs/agents/evidence/OTC-20260826-player-state-semantic-promotion-e2e-retry-4/runtime-terminal.md`
- RETRY-4 run/job: `33012508829 / 98322159507`
- RETRY-4 prestate: `registration_state=UNKNOWN`, `registration_state_evidence=NO_STRUCTURAL_BRIDGE`
- RETRY-4 reached one READY and one COMMIT and ended `AMBIGUOUS / effect_count=1 / RECONCILIATION_DEADLINE_EXHAUSTED`

## Proven failure mechanism

The movement admission boundary combined three individually visible behaviors into an unsafe semantic composition:

1. `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` deliberately classifies adoption state as `UNKNOWN`. `NO_STRUCTURAL_BRIDGE` is UNKNOWN, and even bridge 3/3 remains `UNKNOWN/BRIDGE_3_OF_3_SEMANTICS_UNPROVEN` because bridge presence alone is not standalone proof that the client is in the game world.
2. `.github/scripts/tibia-official-client-re-canonical-live-transition.py::_guarded_dispatch()` fenced runtime identity repeatedly but had no movement-specific semantic-state requirement before emitting `TRACK_A_GUARDED_DISPATCH_READY` or before starting the worker effect.
3. `.github/scripts/tibia-official-client-re-player-state-causal-worker.py::validate_registration()` explicitly required `registration.state == "UNKNOWN"`, so direct/preflight worker validation treated the fail-closed state as the accepted state for movement.

Therefore a correctly fail-closed adoption result could pass identity/fence checks and still cross the irreversible movement COMMIT boundary without proven `IN_GAME` state.

## TDD proof

Test-only RED head:

- head: `9e9a4995c0785617d90967d0ad70cf75c885890e`
- hosted run: `33014845948`
- job: `98330275921`

The focused regression failed in both intended ways on the pre-repair code:

- canonical guarded dispatch emitted READY for `state=UNKNOWN` instead of raising `guarded_dispatch_move_requires_proven_ingame`;
- direct worker execution with `state=UNKNOWN` progressed to a post-dispatch `AMBIGUOUS` result instead of returning pre-dispatch `REFUSED/effect_count=0`.

This establishes the bug without live runtime access or gameplay.

## Repair

Minimal production repair commit:

- `54de1a00b234158a731a30708b3d11d808e0ef55`

Canonical defense:

- adds `_require_guarded_request_semantics(request, registration, manifest)`;
- for `kind != move`, behavior is unchanged;
- for `kind == move`, both current canonical registration and fresh probe manifest must be exactly `IN_GAME`;
- the semantic guard runs after the first probe, after the second probe immediately before READY, and after the third probe immediately before the worker effect;
- any non-IN_GAME state therefore fails closed before READY, or, if state drifts after READY, before the worker effect.

Worker defense in depth:

- `validate_registration()` now requires `state == "IN_GAME"` instead of `state == "UNKNOWN"`;
- exact PID, process-start, XRes window binding, client hash/size/version, display, runtime locator and proof-kind checks remain intact;
- direct/bypassed worker invocation with a non-IN_GAME registration returns semantic precondition refusal before tool/read/dispatch effect.

No new `IN_GAME` producer was introduced. The current `existing_runtime_adoption_v1` semantics remain deliberately unable to manufacture `IN_GAME`; an independently trustworthy proof source is still required before a movement can be admitted.

## Boundary regression coverage

Permanent regression:

- `.github/scripts/test_tibia_official_client_re_in_game_admission.py`
- wired into `.github/workflows/track-a-causal-worker-timing.yml`

Covered cases:

- `UNKNOWN` -> guarded move READY is blocked;
- `LOGIN` -> guarded move READY is blocked;
- `CHARACTER_SELECT` -> guarded move READY is blocked;
- `DISCONNECTED` -> guarded move READY is blocked;
- `IN_GAME` at first/second probe followed by drift to `UNKNOWN` after READY -> worker effect is blocked;
- synthetic explicit `IN_GAME` remains able to reach the mocked worker path, preventing accidental blanket disablement;
- direct worker invocation for all four non-IN_GAME states -> `REFUSED/effect_count=0` with zero dispatch.

Terminal safety statements:

- `NO_NEW_INGAME_PRODUCER=true`
- `UNKNOWN_TO_MOVE_READY=BLOCKED`
- `LOGIN_TO_MOVE_READY=BLOCKED`
- `CHARACTER_SELECT_TO_MOVE_READY=BLOCKED`
- `DISCONNECTED_TO_MOVE_READY=BLOCKED`
- `STATE_DRIFT_AFTER_READY_TO_WORKER_EFFECT=BLOCKED`
- `DIRECT_WORKER_NON_INGAME_TO_DISPATCH=BLOCKED`
- `SYNTHETIC_PROVEN_INGAME_POSITIVE_PATH=PRESERVED`

## Hosted verification before evidence binding

Green implementation/boundary head:

- `d2e52ff261805014399c856ce3a024f58fa6cace`

Hosted checks:

- Track A causal worker timing run `33016340057`: PASS
  - worker suite: PASS
  - timeout-contract suite: PASS
  - dispatch-boundary suite: PASS
  - strengthened in-game admission suite: PASS
  - canonical guarded-dispatch regressions: PASS
  - Kasm adoption-probe regressions: PASS
  - player-state resolver regressions: PASS
  - full PR whitespace: PASS
- Track A agent runtime governance `33016340032`: PASS
- Track A canonical live governance `33016340047`: PASS
- hosted XRes validation `33016340059`: PASS
- repository CI `33016340233`: PASS
- `CI / Required` job `98335600449`: PASS

Earlier `e209be54a02d5254790f8d17d0438ddf6c5352ed` and `ef6ffbf6123b4a6b57dcdb26cf20e1c5535c219b` failures were test-harness-only while strengthening the positive synthetic path: missing mocked `token_file/_lease`, then missing mocked `_cancel`. Production code was not changed in response; only the synthetic positive harness was completed. The negative and state-drift regressions already passed in those runs.

## Scope and remaining dependency

The admission bug is repaired, but this task does **not** establish that any current official client is logged in or `IN_GAME`. With the current adoption proof path, state remains `UNKNOWN`; consequently a future movement attempt must now stop before READY.

A future physical movement E2E can only be considered after a separate task establishes a trustworthy current `IN_GAME` proof source and the owner separately authorizes any physical action. This task itself authorizes none.
