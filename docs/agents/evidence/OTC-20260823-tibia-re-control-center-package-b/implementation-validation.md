# Package B implementation validation

Task: `OTC-20260823-tibia-re-control-center-package-b`

## Scope and authority

- Base branch snapshot at claim: `main@63100340f0dbe1aba16a20bc7febc8613291583d`.
- Package A dependency: PR `#628`, merge `13b3f02a07a176662d766352d9af39619775a73d`.
- Package C PR `#663` was inspected before implementation and owns only its Surveyor provider/test/task/evidence paths; Package B does not modify them.
- Official client access remained `NONE`; credentials, login, gameplay and official-client mutation were never authorized.
- Mutation-capable Package B execution is constrained to the explicit `FAKE_TEST` adapter.

## Candidate validation

The implementation candidate was exercised locally on Windows before the final implementation commit:

- `ruff check tools/tibia_re_control_center tests/tools/tibia_re_control_center/test_package_b.py tests/tools/tibia_re_control_center/audit_package_b.py tests/tools/tibia_re_control_center/e2e_package_b.py` -> PASS.
- `python -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center` -> PASS.
- `python -m unittest discover -s tests/tools/tibia_re_control_center -v` -> PASS, `Ran 160 tests`, `OK`.
- `python tests/tools/tibia_re_control_center/e2e_package_b.py` -> PASS:
  - `PACKAGE_B_BACKEND=PASS`
  - `PACKAGE_B_CLI=PASS`
  - `PACKAGE_B_BROWSER=PASS`
  - `PACKAGE_B_IDEMPOTENCY_RESTART=PASS`
  - `OFFICIAL_CLIENT_ACCESS=NONE`
  - `PACKAGE_B_E2E=PASS`
- `python tests/tools/tibia_re_control_center/audit_package_b.py` -> PASS:
  - boundary, transport, idempotency, restart and privacy all PASS;
  - `OFFICIAL_CLIENT_ACCESS=NONE`;
  - `PACKAGE_B_AUDIT=PASS`.
- `git diff --check` -> PASS.

## Additional falsification added during implementation

The first sequential design was not accepted as complete. Concurrency falsification exposed a theoretical duplicate-claim race, so RequestLedger acceptance was made atomic and same-request execution is serialized through bounded request-id lock stripes. Added live concurrent tests prove:

1. twelve simultaneous identical POSTs share one durable resource/result and one fake external effect;
2. two simultaneous bodies with the same request id produce one success, one `409`, and one fake effect;
3. STOP racing an action exactly before dispatch commit leaves zero fake effects;
4. concurrent STOP/reset resolves to the highest durable `control_generation` without contradictory state.

A real monotonic runtime clock replaced the deterministic zero-based test clock in the Package B backend so runtime deadlines advance in wall execution and remain comparable across backend process-object restarts on the same system boot.

## Compatibility edit rationale

Package A mandatory test 52 originally scanned every future Python file in the package and therefore classified the contract-authorized Package B listener/CLI as a Package A bypass. It is narrowed to the explicit Package A core file set. The Package A exported API and its runtime-access boundary are unchanged. The package docstring is updated to describe the now-present non-exported Package B loopback modules.

## Exact-head gate

This document records the pre-commit candidate validation. Exact-head validation is intentionally performed again after commit and by `.github/workflows/tibia-re-control-center-package-b.yml`; task criterion 30 remains open until PR merge, archive and ownership release.

## Continuation resync, fresh audit and remediation - 2026-08-23 17:45 +02:00

Current-main integration base for this continuation: `origin/main@36e277a0b7a33b862c838993e0ee2ff95d7516e0`; local merge commit before remediation: `eea357685b9561891a5a221cd9edefa44b035b21`. No Package C/D-owned path was edited by the Package B repair.

Fresh contract falsification found four defects that the original tests encoded rather than caught: `PB-AUDIT-001` (`CONTROL_AUTH_REQUIRED`), `PB-AUDIT-002` (unknown-route 404 versus known-route method 405), `PB-AUDIT-003` (`CONTROL_IDEMPOTENCY_CONFLICT`), and `PB-AUDIT-004` (literal nonce in arbitrary URL data). All four were remediated in Package B-owned code and the tests/audit were changed to assert the normative v1 behavior. The audit/E2E scripts were also made directly executable without relying on `PYTHONPATH=.` because the canonical continuation alias requires direct script invocation.

Verified after remediation:

- focused Ruff across changed Package B code/tests/audit/E2E -> PASS;
- `python -m unittest tests.tools.tibia_re_control_center.test_package_b -v` -> `Ran 39 tests`, `OK`;
- `python tests/tools/tibia_re_control_center/audit_package_b.py` -> `PACKAGE_B_AUDIT=PASS`;
- `python tests/tools/tibia_re_control_center/e2e_package_b.py` -> `PACKAGE_B_BROWSER=PASS`, `PACKAGE_B_CLI=PASS`, `PACKAGE_B_IDEMPOTENCY_RESTART=PASS`, `PACKAGE_B_E2E=PASS`;
- official client access remained `NONE`.

The historical `Ran 160 tests` line above is preserved as pre-resync evidence only. It is not treated as final-head evidence after the new main merge/remediation; full regression and final exact-head CI must be rerun before closeout.

## Integrated mandatory gate run - 2026-08-23 17:52 +02:00

After merging current `origin/main@5ac05b2640e818a1efc3e065e2ed4e501eaed058`, code head `1c0814f931aff7a6ba5e12e6c2ecc6229be82a31` was validated with the continuation alias commands. Compileall PASS; full unittest discovery PASS with `Ran 193 tests`, `OK`; Package B audit PASS; real Chrome/CDP + CLI E2E PASS; and `git diff origin/main...HEAD --check` PASS.

The alias-wide Ruff command reports exactly 10 findings, all in `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py` (nine `RUF059`, one `B017`). This is verified as a current-main baseline rather than a Package B change: `git diff --exit-code origin/main -- tests/tools/tibia_re_control_center/test_package_d_official_adapter.py` returns 0 and both HEAD/current-main resolve that path to Git blob `3b2cdbddc03688f6f698a8b998e38fb6577429e2`. Package D paths are read-only for this task, so no cross-owner edit was made. Live PR CI/root merge-gate behavior must determine whether that baseline blocks Package B terminal closeout.

## Package A compatibility-audit repair

PR #666 CI exposed `PB-AUDIT-005`: Package A validation still treated future Package B modules/metadata as part of Package A's original `runtime_access:none` implementation boundary. No active Package A task or open Package A PR owned the two validator paths. The repair scopes `audit_package_a.py` to the explicit Package A core and admits only known Package B metadata in the Package A workflow path-boundary check.

Focused validation: Ruff PASS; `python -m unittest tests.tools.tibia_re_control_center.test_package_a -v` -> 76/76 PASS; `PYTHONPATH=. python tests/tools/tibia_re_control_center/audit_package_a.py` -> fresh audit PASS, zero material findings, runtime-access-none PASS, fake one-step E2E PASS. No Package A execution semantics or authority changed.

## Terminal implementation closeout

Implementation PR #666 merged exact final head `be8e5324cf8df0a62b3f37f43156723b859e7ed6` as squash merge `1e9f0245b2c7a249dfd0fdc9c6f8bdda2e9aa5e5`. Exact-head Package A workflow `32652125288`, Package B workflow `32652125330`, repository CI `32652125421` and required job `97225428316` all passed. Fresh Package A/Package B audits and real Chrome/CDP + CLI + backend E2E passed; PR #666 had no review/comment/thread blocker. `OFFICIAL_CLIENT_ACCESS=NONE` for the full task. The broad local Ruff command's 10 Package D findings are a verified main-baseline issue at identical blob `3b2cdbddc03688f6f698a8b998e38fb6577429e2`, not a Package B change.
