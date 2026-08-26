# Player-state causal worker post-COMMIT failure RCA

## Result

`ROOT_CAUSE_PROVEN_AND_REPAIRED`.

`RETRY_4_SAFE_TO_AUTHORIZE=true` **only as a future owner decision after this repair is merged to trusted main**. This RCA does not authorize retry-4: `retry_4_authorized=false`. Any future causal movement still requires fresh explicit owner authorization and fresh Track A Gate A / required recovery-or-rebind / Gate B / target uniqueness / semantic-precondition admission.

## Scope and source of truth

This investigation is strictly repository/hosted-test work with `runtime_access:none`, `physical_action_budget:0`, and no live-client observation or mutation.

Primary inputs:

- trusted main at claim: `64189859ae360205c0467b8fcd2ead1ff78df679`;
- terminal retry-3 evidence: `docs/agents/evidence/OTC-20260826-player-state-semantic-promotion-e2e-retry-3/runtime-terminal.md`;
- retry-3 controlled run/job: `32999512190 / 98277327059`;
- durable worker repair baseline: PR #701;
- retry-3 closeout/archive lifecycle: PRs #703/#704/#705;
- RCA implementation PR: #708.

No login, credentials, relog, restart, character selection, gameplay input, COMMIT, process-memory write, Synology/Kasm live observation, or physical action occurred during this RCA.

## Observed retry-3 failure boundary

Retry-3 crossed COMMIT exactly once only after all required live gates had passed. After COMMIT, the final fresh exact-target Kasm probe passed. The parent then emitted:

- `TRACK_A_CANONICAL_TRANSITION_ERROR=guarded_dispatch_worker_failed`;
- **not** `worker_timeout`;
- no valid `TRACK_A_GUARDED_DISPATCH_RESULT` envelope.

The wrapper therefore correctly classified the attempt as `AMBIGUOUS_POST_COMMIT_NO_VALID_RESULT` and forbade retry.

The distinction is material: the canonical parent did not hit its 30-second outer timeout. The worker itself terminated nonzero near the end of its internal 27-second budget, and the parent rejected any absent/unproven final result.

## Proven root cause

PR #701 reserved two seconds of the worker's absolute budget for durable final-result publication by subtracting that reserve from subprocess/read/reconciliation timeout calculations. That reserve was a scheduling calculation, not a hard wall around Python subprocess timeout cleanup.

Python `subprocess.run(..., timeout=...)` may spend additional time terminating and collecting a timed-out child after the requested timeout expires. A late post-dispatch player-state read could therefore consume the nominal result-write reserve during timeout cleanup.

The failure chain is:

1. one dispatch has already started and therefore the effect boundary is crossed;
2. reconciliation legitimately needs another read;
3. the read timeout is bounded using the remaining worker budget minus the nominal write reserve;
4. timeout cleanup overruns that requested timeout and consumes the nominal reserve;
5. `execute_once()` conservatively reaches an `AMBIGUOUS/effect_count=1` result;
6. `write_result()` sees insufficient deadline budget and raises `WorkerDeadlineExceeded` before durable publication;
7. worker `main()` returns nonzero;
8. the old parent treats nonzero as `guarded_dispatch_worker_failed` and never has a valid durable terminal envelope to return.

This explains the exact retry-3 parent marker without converting missing worker internals into an unsupported claim.

## Deterministic non-live reproduction

A fake monotonic clock and mocked candidate reader reproduced the boundary without the Tibia runtime:

- worker budget: 27 s;
- baseline read: 10 s;
- unchanged reconciliation read: 10 s;
- later read receives only the remaining bounded timeout;
- simulated timeout cleanup consumes the requested timeout plus 2.5 s;
- `execute_once()` reaches `AMBIGUOUS/effect_count=1` with `RECONCILIATION_DEADLINE_EXHAUSTED`;
- remaining write budget is zero;
- durable `write_result()` fails with `WorkerDeadlineExceeded`.

The pre-fix regression test also proved that the old worker started a third doomed reader: expected `reads=2`, observed `reads=3`.

## TDD history

### Measured late-read headroom

Commit `8671a462329205b4ca61264445aae905594f6714` introduced the first bounded fix after a RED test. It measures the actual fresh baseline-read cost and refuses to start a later reconciliation read when the current non-write window cannot cover that measured cost while preserving the durable-write reserve.

Hosted Linux run `33007910556` passed the inherited #701 timing stack on that slice.

A later audit found the first expression double-counted the two-second reserve. A new RED boundary test on the final repair line proved that exactly `baseline cost + write reserve` must still permit reconciliation (`reads=1` before correction). The final formula compares the measured baseline cost against `remaining(reserve=RESULT_WRITE_RESERVE_SECONDS)` without subtracting the reserve twice.

### Durable post-dispatch checkpoint

The stronger failure mode is the **first** reconciliation read itself overrunning the reserve during timeout cleanup. No finite arithmetic reserve alone can prove safety against arbitrary cleanup overrun.

The repair therefore adds a separate durable checkpoint immediately after one successful dispatch and before any reconciliation read:

```json
{
  "status": "AMBIGUOUS",
  "effect_count": 1,
  "action_hash": "<exact request hash>",
  "reason_code": "POST_DISPATCH_RECONCILIATION_INCOMPLETE"
}
```

The checkpoint is written atomically using the same fsync/replace/directory-fsync path as other worker results. The normal final result remains a separate file.

RED worker-contract head `0b2f070e78dc250abdf46fa1b3b807c4ef204237` failed because the checkpoint hook did not exist. Worker checkpoint implementation `fc1c3d5859f74fdb0dbcdd4ecb52da81e645c2aa` then made the worker suite 21/21 PASS on hosted Linux.

After correcting a test-fixture-only missing `json` import at `361f6a6d61ce7842a9f359a47cfcfdf7a574fa72`, the parent RED run `33009253427` proved the remaining old behavior exactly: nonzero still raised `guarded_dispatch_worker_failed`, while outer timeout still propagated `TimeoutExpired` despite the durable conservative checkpoint.

Parent implementation `ed1c35b69aea7d28977df5105c6f2c7f7cfdb0ed` added strict fallback recovery. Audit correction/final technical head is `2f816aa7b443152911001b07f7150dd5830ba99e`.

## Final repaired contract

The worker now:

- preserves the one-dispatch/no-retry rule;
- records a separate conservative post-dispatch checkpoint immediately after successful dispatch and before reconciliation;
- never writes `CONFIRMED` into that fallback checkpoint;
- measures the fresh baseline-read cost to avoid starting a clearly doomed late reconciliation read;
- keeps the ordinary final `REFUSED/AMBIGUOUS/CONFIRMED` result path unchanged for normal completion.

The parent now:

- deletes stale final-result and fallback-checkpoint files before worker start;
- on worker exit 0, accepts **only** the ordinary final result path;
- on worker nonzero or outer timeout, may inspect only the separate post-dispatch checkpoint;
- accepts that checkpoint only when it is exactly `AMBIGUOUS`, `effect_count=1`, has the exact request action hash, and reason `POST_DISPATCH_RECONCILIATION_INCOMPLETE`;
- rejects missing, malformed, mismatched, or `CONFIRMED` fallback checkpoints and preserves the previous failure/timeout classification;
- removes both paths in final cleanup.

A dedicated negative regression proves a dead worker cannot smuggle a `CONFIRMED` checkpoint into the parent result.

## Hosted validation on final technical head

Exact technical head: `2f816aa7b443152911001b07f7150dd5830ba99e`.

- Track A causal worker timing run `33010066853`: PASS;
- Track A agent runtime governance run `33010066998`: PASS;
- Track A canonical live governance run `33010066920`: PASS;
- Track A canonical XRes hosted validation run `33010066891`: PASS; its job is explicitly `Hosted canonical XRes window validation` and proves the hosted-only integration boundary;
- repository CI run `33010067149`: PASS;
- `CI / Required` job `98313912896`: PASS;
- fresh validator audit review `5034750238`: PASS, zero material findings.

No self-hosted/live-runtime job was used for this repair validation.

## Retry-4 decision

`RETRY_4_SAFE_TO_AUTHORIZE=true` for the specific post-COMMIT result-loss failure mode addressed here, because a successful dispatch now has a durable conservative terminal checkpoint before reconciliation can overrun its timeout budget, while the parent cannot upgrade that checkpoint beyond AMBIGUOUS.

This is **not** movement authorization and does not claim a future retry will confirm the semantic contract. It only establishes that the retry-3 `guarded_dispatch_worker_failed` / no-valid-result failure mechanism has a deterministic reproduction, a tested repair, and a fail-closed parent fallback.

A future retry-4, if the owner explicitly authorizes it in a separate task, must still start from then-current trusted main and pass fresh Track A admission. UNKNOWN/BLOCKED must still mean zero movement, READY/COMMIT must remain bounded by the new task's authorization, and any post-COMMIT result must remain terminal with no retry.