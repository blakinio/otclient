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
