# Independent contract audit — Track A canonical live bootstrap

Date: 2026-08-16
Validator role: fresh GitHub-only documentation validator
Task: `OTC-20260815-track-a-canonical-live-bootstrap-contract`
PR: #318
Implementation head inspected: `6b6bef68e1b6553660834fd53f0e2b9730c59974`
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

The validator re-read the trusted task boundary, the complete PR #318 diff, the final promoted manager closeout on `main`, and the production supervisor source at `.github/scripts/tibia-official-client-re-canonical-live-guard.py`. The audit did not rely on the implementer summary as evidence and did not inspect or mutate a live Tibia runtime.

Checks attempted to falsify the contract on these boundaries:

- final PR #316 supervisor semantics versus bootstrap wording;
- separation of Gate A controller authority, Gate B runtime identity/reuse, and initial creation;
- whole-lifetime anti-escape semantics during bootstrap mutation;
- safe-detach distinction from ordinary `guard-run`;
- exact client fence preservation;
- stale/historical runtime evidence being misrepresented as current;
- `:98`, `6082`, PID/session registration claims;
- PR #303/Track B ownership overlap;
- credential/login authority expansion;
- branch-protection/security weakening;
- unrelated changed paths and PR hygiene.

## Primary evidence

- Final manager task archive on trusted `main` records PR #316 exact implementation head `d61d362c12125e3c70167f09729a0caa8b891e78`, merge `e9df81f50dbb231bc4ac6cc3fc21f260fc358d34`, fresh closeout PR #319 and zero open manager review threads.
- Production guard source acquires and validates before fork, makes a Linux child subreaper, starts the guarded command with `close_fds=True`, keeps the coordination flock in the external supervisor, waits for the primary plus adopted/orphaned descendants, and releases by closing the supervisor descriptor.
- PR #318 contract explicitly treats ordinary `guard-run` as insufficient for a successful persistent bootstrap detach and requires a distinct reviewed bootstrap primitive/state machine.
- PR #318 keeps the exact fence `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` unchanged.
- Historical PR #315 observations are explicitly classified as historical only. Current `:98`/`6082` canonical status is `UNKNOWN`; PID/session remain `NOT_REGISTERED` until fresh direct preflight.
- The contract does not authorize implementation, launch, login, credential use, runtime mutation, PR #303 runtime access or Track B work.

## Findings

No critical, high, or material medium findings.

```yaml
findings:
  material_open: 0
  non_material_open: 0
```

## E2E

Result: `NOT_APPLICABLE`.

Reason: this PR defines a documentation-only bootstrap contract and explicitly does not implement or authorize the live bootstrap transition. A future implementation task must run deterministic non-live tests and a separately authorized real-client E2E before claiming bootstrap functionality.

## Audit result

`PASS`

The contract is internally consistent with the final promoted manager/supervisor, remains fail-closed, preserves runtime-identity uncertainty, and keeps bootstrap implementation/live execution outside this PR's authority. Final completion remains contingent on exact-head repository CI, zero unresolved review findings, protected merge, and fresh post-merge archival/ownership release.
