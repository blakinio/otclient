# 2026-08-28 loginservice `operatingsystem` contract

Task: `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE`
PR: #284
Track: Track B only

## Fresh authority

- trusted `main`: `470d5bd285e29f9d3f24f70ff3fc5370e2990e2a`
- starting PR head: `5a0b0879c43acbbf2d6e5d83b78ee4ceab62a044`
- promoted current loginservice contract: PR #734 / #735 on trusted main
- exact current Linux cut: `15.32.75d4a0`

## TDD RED

Test-only head: `b5e458043c5181f50a15e1f00e9ae690c03fe494`
Workflow run: `33145320209`
Job: `98764948909`

Hosted Ubuntu contract failed exactly at:

```text
AssertionError: encrypted handoff emitter: missing mandatory operatingsystem
```

`Prepare encrypted handoff runtime`, `Emit encrypted one-shot game handoff`, and artifact upload were skipped. No secret-bearing HTTP request occurred in the RED run.

## Minimal repair and local GREEN

All three Track B loginservice producers now add only the newly required `operatingsystem` field. They derive it from the Linux runtime using the same observable strategy as current Qt `QSysInfo::prettyProductName()`: use `PRETTY_NAME` from freedesktop `os-release`; if unavailable, fall back to `uname` system name plus release.

No conditional token/code fields are synthesized.

Local no-secret validation on Molehill WSL Ubuntu:

```text
TRACK_B_ENCRYPTED_HANDOFF_CONTRACT=PASS
TRACK_B_QSYSINFO_LINUX_DERIVATION=PASS
bash -n emit.sh/http-login-preflight.sh/world-entry-probe.sh = PASS
git diff --check = PASS
```

The one-shot current typed game E2E marker is absent. The next pushed material head is authorized for exactly one encrypted-handoff HTTP-only validation; game E2E remains disarmed until valid session/playdata is proven.
