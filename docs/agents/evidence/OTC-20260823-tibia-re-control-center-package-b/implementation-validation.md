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
