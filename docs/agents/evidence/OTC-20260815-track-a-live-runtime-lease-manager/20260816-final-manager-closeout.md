# Final manager closeout — 2026-08-16

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Closeout source: live `main@e9df81f50dbb231bc4ac6cc3fc21f260fc358d34`  
Final implementation PR: #316  
Final implementation head: `d61d362c12125e3c70167f09729a0caa8b891e78`  
Fresh closeout PR: #319

## Result

```yaml
final_manager_closeout:
  result: PASS
  implementation_main: e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
  exact_head_validation: PASS
  material_findings_open: 0
  e2e: NOT_APPLICABLE
  stale_pr_314_evidence_reused: false
```

## Fresh live-state basis — FACT

This closeout was prepared only after re-reading live repository state after PR #316 merged. It does not reuse the superseded closeout prepared in PR #314.

- `main` resolved to `e9df81f50dbb231bc4ac6cc3fc21f260fc358d34`, the protected merge of PR #316.
- PR #316 exact head was `d61d362c12125e3c70167f09729a0caa8b891e78`, clean-restacked directly on PR #317 merge `b433290f48e18270279895ff4abb1a54b4475051`.
- The restack preserved PR #317's `LeaseManager.locked()` last-close behavior while adding the PR #316 external supervisor/wrapper/test changes.
- The two SC2016 expressions responsible for old repository CI failure `31910752406` were rewritten on the restacked head; final actionlint/shellcheck passed.
- PR #316's material test-cleanup review thread is resolved.
- PR #313's two surviving post-merge P1 review threads were resolved only after the final supervisor reached `main` and the E2E token was corrected to `NOT_APPLICABLE`.

## Exact-head validation — FACT

Final semantic validation on `d61d362c12125e3c70167f09729a0caa8b891e78`:

```text
run 31914257951
unit 95083728186 SUCCESS
isolated-selfhosted 95083728146 SUCCESS
fresh independent acceptance audit 95083728148 SUCCESS
```

Final repository validation on the same exact head:

```text
run 31914258080
Detect Build Scope 95083728609 SUCCESS
Lua Syntax / Check Lua Syntax 95083728698 SUCCESS
Fast Checks / Syntax and workflow validation 95083728736 SUCCESS
Fast Checks / Informational static analysis 95083728740 SUCCESS
CI / Required 95083836065 SUCCESS
```

The fresh acceptance audit re-ran the deterministic manager and supervisor suites and checked production routing, `PR_SET_CHILD_SUBREAPER`, `close_fds=True`, absence of a guarded `pass_fds=` flock path, and Python compilation. The isolated Synology job remained task-state-only and did not mutate production canonical state.

## Final semantics — FACT

The final manager stack on `main` provides these combined guarantees:

1. lease-sensitive time is sampled after coordination-lock acquisition;
2. generic manager lock release uses descriptor last-close rather than explicit `LOCK_UN`;
3. production `guard-run` acquires and validates before any detached process exists;
4. a dedicated Linux child-subreaper supervisor owns the flock out of band;
5. guarded commands receive no coordination-lock descriptor;
6. the supervisor waits for the primary command and all adopted/orphaned descendants before releasing serialization;
7. caller death after dispatch does not release the supervisor-held flock;
8. waiting-call cancellation before acquisition cannot leave a future detached mutation.

## Related lifecycle — FACT

- #312: merged initial manager (`3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`).
- #313: merged concurrency remediation (`f6fa2264904c6ffb3734d4a63e1edbb29260fcc1`); later P1 threads now resolved against final main.
- #314: closed superseded, not merged, and intentionally excluded as closeout evidence.
- #317: merged last-close remediation (`b433290f48e18270279895ff4abb1a54b4475051`).
- #316: clean-restacked, exact-head green, merged (`e9df81f50dbb231bc4ac6cc3fc21f260fc358d34`).
- #319: fresh lifecycle-only archive PR; task becomes archived/released when #319 reaches `main`.

## Safety boundary — FACT

- No live Tibia launch/login/input/attach/signal/runtime mutation was performed.
- No credentials were used and no canonical runtime registration was created.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` without direct evidence.
- Exact client fence remains `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- PR #303 runtime-owned paths/processes and Track B were untouched.
- No branch protection, lease gate, identity gate or host-security boundary was weakened.
- No owner-funded Codex/OpenAI API or paid AI quota was used.

## E2E classification

`NOT_APPLICABLE` — manager acceptance is fully exercised through the real public lease/guard entrypoint and isolated OS process/lock behavior. A live Tibia action would be outside this task's authorization.
