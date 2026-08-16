# Independent contract audit — Track A canonical live bootstrap

Date: 2026-08-16
Validator role: fresh GitHub-only documentation validator phase after the replacement implementer phase
Task: `OTC-20260815-track-a-canonical-live-bootstrap-contract`
PR: #318
Contract head inspected: `c24a9ba2c3eaaabab5c43ff31c9c268380953ebb`
Trusted base inspected: `main@25700f08c3f5729e4ee38bf8c0a3ca04020379be`

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
```

## Audit method

The validator re-read the trusted task boundary, complete PR #318 changed-file set and contract diff, the final promoted manager wrapper/lease implementation, the production out-of-band supervisor, and all current review threads. The audit used primary repository state rather than the implementer summary and did not inspect, launch, log in to, or mutate a live Tibia runtime.

The audit attempted to falsify the contract on these boundaries:

- durable lease-record authority versus the separate canonical coordination flock critical section;
- final PR #316 child-subreaper supervisor semantics versus bootstrap wording;
- stale preflight/racing-bootstrap behavior;
- one authoritative registration namespace/path for all Gate B readers and writers;
- rejection of exact, mismatched and unverifiable official-client candidates/sessions;
- separation of Gate A controller authority, Gate B runtime identity/reuse, and initial creation;
- safe-detach distinction from ordinary `guard-run`;
- exact client fence preservation;
- stale/historical runtime evidence being misrepresented as current;
- `:98`, `6082`, PID/session registration claims;
- PR #303/Track B ownership overlap;
- credential/login authority expansion;
- branch-protection/security weakening;
- unrelated changed paths and PR hygiene.

## Primary evidence

- Trusted `main` wrapper `.github/scripts/tibia-official-client-re-canonical-live-lease` fixes `CANONICAL_STATE_DIR` to `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime` and forbids a caller-selected state override.
- Trusted `main` `LeaseManager` stores `coordination.lock` and `lease.json` under that directory. Its ordinary lease `acquire` critical section is transient; therefore lease acquisition alone is not continuous flock ownership.
- Trusted `main` production `guard-run` separately opens/acquires the canonical flock, validates the current lease while holding it, forks a Linux child-subreaper supervisor, starts the guarded command with `close_fds=True`, and keeps the flock only in that external supervisor until the primary plus adopted/orphaned descendants have exited.
- Current PR #318 contract now mirrors that separation for bootstrap: acquire/renew authoritative lease first, then the reviewed bootstrap supervisor acquires the canonical flock and revalidates the lease, then performs the decisive fresh absence inventory under the same continuously held flock immediately before launch.
- The contract fixes the one authoritative current registration path at `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`; candidates are same-directory mode-restricted temporary files atomically renamed to that exact path, and alternative roots/paths fail closed.
- The absence gate inventories all official native Linux client candidates/sessions, not only the exact fence. Exact, mismatched or unverifiable candidates, existing official-client session evidence, or incomplete inventory are blockers rather than absence.
- The contract keeps the exact fence `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` unchanged.
- Historical PR #315 observations remain historical only. Current `:98`/`6082` canonical status is `UNKNOWN`; PID/session remain `NOT_REGISTERED` until future direct evidence.
- The contract does not authorize implementation, launch, login, credential use, runtime mutation, PR #303 runtime access or Track B work.

## Findings and dispositions

```yaml
findings:
  - id: BR318-P1-01
    severity: P1
    subject: stale absence preflight before lease/coordination critical section
    disposition: RESOLVED
    verification: state machine now acquires/renews the lease, then supervisor acquires flock and validates it, then repeats authoritative absence inventory immediately before launch while flock remains held
  - id: BR318-P1-02
    severity: P1
    subject: registration namespace/path unspecified
    disposition: RESOLVED
    verification: exact authoritative runtime-registration.json path is fixed under manager state root for all readers/writers/atomic commit
  - id: BR318-P1-03
    severity: P1
    subject: mismatched or unverifiable official clients could be mistaken for absence
    disposition: RESOLVED
    verification: all official-client candidates/sessions and inventory completeness are now fail-closed blockers
  - id: AUD-BOOTSTRAP-01
    severity: material
    subject: lease acquisition was initially described as if it continuously held coordination.lock
    disposition: RESOLVED
    verification: contract head c24a9ba2 explicitly separates transient lease acquisition from supervisor-owned flock acquisition and under-lock lease validation
  material_open: 0
  non_material_open: 0
```

No critical, high, or material medium finding remains open in the contract content inspected at `c24a9ba2c3eaaabab5c43ff31c9c268380953ebb`.

## E2E

Result: `NOT_APPLICABLE`.

Reason: this PR defines a documentation-only bootstrap contract and explicitly does not implement or authorize the live bootstrap transition. A future implementation task must run deterministic non-live tests and a separately authorized real-client E2E before claiming bootstrap functionality.

## Audit result

`PASS`

The corrected contract is internally consistent with the final promoted manager/supervisor, closes the three review P1s plus the audit-detected lease/flock wording defect, remains fail-closed, preserves runtime-identity uncertainty, and keeps bootstrap implementation/live execution outside this PR's authority. Final completion remains contingent on zero unresolved review threads, a frozen exact final head with repository `CI / Required` PASS, protected merge, and fresh post-merge archival/ownership release.
