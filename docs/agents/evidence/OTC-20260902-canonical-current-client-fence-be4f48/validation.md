# Validation checkpoint

Exact GREEN implementation head: `22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba`.

## Local / deterministic

- focused current-client fence: PASS
- Phase 2 runtime admission: 14/14 PASS
- deterministic Track A agent runtime governance: PASS
- changed Python `py_compile`: PASS
- `git diff --check`: PASS

## Linux exact-head validation

A fresh clone in `otclient-synology-runner` was fenced to exact head `22977b3ab264bbfce986a5ff5b2ae7e9e1c457ba`. It passed:

- `bash -n` canonical live-session worker
- focused current-client fence test
- canonical live-session suite
- canonical live-transition suite
- Kasm existing-runtime probe suite
- Kasm bootstrap-worker suite
- Phase 2 runtime-admission suite

The first Linux governance invocation failed before governance assertions because `--single-branch` omitted the `origin/main` ref required by `git diff origin/main...HEAD`. Deterministic governance had already passed on Molehill-PC. Subsequent fresh runner clone attempts were blocked by GitHub credential/auth transport before tests started, so no further Linux governance result is claimed.

## Provenance limitation

Raw CDN refetch attempts were blocked by Cloudflare challenge/HTTP 403 and are not treated as authority. The promoted exact identity is based only on official-launcher manifest/install state plus fresh exact live-ELF hash/size agreement.

Direct Codex usage through this checkpoint: `0`.
## Exact-head CI repair cycle 1

First exact-head CI at `4c308ce11ba30f509894d87dffe9a1a4f9af936a` found two integration failures:

- Package A fresh falsification audit rejected the legal cross-cutting fence change at its declared path boundary before running the safety audit.
- Package B full regression ran 563 tests and reported 18 errors; every error was `observed client does not match the current exact official-client fence` from stale test fixtures still constructing the superseded current tuple.

Repair cycle 1 is intentionally narrow:

- current-build fixtures in `test_agent_edge_bridge.py` and `test_vision_p2_trusted_composition.py` use the new current tuple; the deliberate bad-SHA mismatch fixture remains bad;
- Package A boundary grants the cross-cutting exact-path set only when both the exact fence task is present and `github.head_ref` equals `fix/OTC-20260902-canonical-current-client-fence-be4f48`.

Pre-commit repair validation:

- affected suites: 28/28 PASS
- runtime admission: 14/14 PASS
- focused current-client fence: PASS
- deterministic Track A runtime governance: PASS
- affected Python compile: PASS
- `git diff --check`: PASS
- Package A boundary simulation across the complete 23-path PR+repair diff: `UNEXPECTED_COUNT=0` / PASS
## Fully terminal repair-head CI and post-CI scope audit

Exact head `fc29715dea57b1e8c05a9d8e7aae7f79d0f8cf69` reached fully terminal GitHub Actions with **11/11 associated workflows SUCCESS**, including Package A fresh falsification + deterministic core, Package B fresh falsification + real browser/CLI E2E + full regression, main CI, and all Track A fence/governance/Kasm/self-hosted checks.

A fresh post-CI GitHub diff audit confirmed the 23 changed files are limited to current exact-client authority, Phase 2 admission fixtures, task/evidence, and the Package A boundary integration required by the atomic fence update. Remaining `15.32.75d4a0` references were inspected: canonical fence reconciliation and Field6/QMeta/worldEntered/materializer surfaces are historical/build-specific and deliberately stay pinned to their source ELF.

The audit found one hardening issue: `github.head_ref` alone can be spoofed by a fork PR. TDD RED therefore required an explicit head-repository fence and one-time base SHA. GREEN now admits the special Package A exact-path set only when all of these are true:

- exact fence task is changed;
- `github.head_ref` is `fix/OTC-20260902-canonical-current-client-fence-be4f48`;
- head repository is `blakinio/otclient`;
- PR base SHA is exactly `8441fc1cce1600033b505d68ebc5c0141b337394`.

Extracted workflow-script controls: exact PR = PASS; same branch from `attacker/otclient` = FAIL; same repo/branch against base `4c308ce11...` = FAIL. This makes the exception generation-specific rather than reusable after merge.
