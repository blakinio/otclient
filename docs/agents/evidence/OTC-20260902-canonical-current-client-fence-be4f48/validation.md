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
