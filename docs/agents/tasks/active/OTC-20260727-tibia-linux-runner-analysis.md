# OTC-20260727 — Tibia Linux runner analysis

## Status

`blocked_on_execution_environment` — the no-OCR login path is implemented and test credentials are available in `blakinio/otclient`, but the repository currently has no verified execution path that can both obtain/run the official Linux client and use the required trusted/tunneled egress.

This is an operational research task. Do not merge temporary workflows as product code. Do not commit/upload proprietary CipSoft bytes, credentials, account/character data, cookies, session material, authenticated screenshots, or recovery material.

## Objective

Attempt a real official-client login/world entry **without OCR/Tesseract/image-to-text**, with credentials injected only from GitHub Actions secrets, a changed WARP egress proven before secret use, actual Tibia TCP confined to that tunnel, and success accepted only from non-image runtime/protocol evidence.

## Ownership

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` (draft operational PR)
- Session: `chatgpt-20260812-1802-no-ocr-login`
- Separate active runtime `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811` is read-only evidence for this task. Its `oteryn-tibia-client-analysis` container/state must not be mutated or reused.
- Canonical `oteryn-staging` Compose services remain strictly out of scope.

Owned task paths:

- `.github/workflows/tibia-linux-runner-analysis.yml`
- `.github/workflows/tibia-no-ocr-secret-gate.yml`
- `.github/workflows/tibia-hosted-no-ocr-login.yml`
- `.github/workflows/tibia-hosted-no-ocr-login-v2.yml`
- `.github/workflows/tibia-hosted-no-ocr-login-v3.yml`
- `docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md`

The three hosted-login workflows are temporary failed-probe scaffolding and must be removed before terminal closeout after their run IDs are retained here.

## PROVEN — no-OCR preparation

- `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` are both non-empty GitHub Actions secrets in `blakinio/otclient`: run `31616821899`, job `94181592919`, SUCCESS. The job emitted only boolean presence markers; values remained GitHub-masked and were not persisted.
- The dedicated `otclient` self-hosted workflow contains no Tesseract/OCR/image-to-text success path and fails closed unless the expected runner, owned-container labels, exact client identity, WARP egress, and actual TCP confinement all pass before credential entry.
- The researched official Linux executable evidence cut is client `15.32.df7b29`, size `51,965,216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Reusable decoded-world boundary from read-only Oteryn evidence: FullMap `0xcec8d0`, FieldData `0xcd3190`, Create `0xcecc70`, Change `0xcecf40`, Delete `0xcd4e20`, common ordered map routine `0x19a8a80`.

## PROVEN — hosted-runner attempts

All three hosted attempts stopped **before any credential entry**.

1. Run `31617222584`, job `94182946084`: secret gate passed and `OCR_BINARY_ABSENT=true`; failed because `xdpyinfo` was not installed.
2. Run `31617541307`, job `94184007303`: added X11 tooling; Xvfb worked; official Linux launcher archive request to `static.tibia.com/download/tibia.x64.tar.gz` returned HTTP 403 after retries.
3. Run `31617769586`, job `94184760079`: pinned `wgcf 2.2.32` and `wireproxy 1.1.3` hashes passed, Cloudflare trace showed `warp=on`, changed egress and `PROXYCHAINS_WARP_EGRESS_VERIFIED=true`; the same official launcher archive still returned HTTP 403 through the WARP SOCKS path.

Therefore GitHub-hosted `ubuntu-24.04` is not currently a viable bootstrap path for the official Linux launcher. Do not brute-force alternate public proxies or weaken the egress/secret boundary.

## PROVEN / INFERENCE — self-hosted runner availability

- Current `otclient` run `31616469972`, job `94180403029`, has remained `queued` with no job steps.
- Historical run `30223131080`, job `89848906511`, on the same `otclient` branch likewise completed `cancelled` with `steps=null` after remaining unable to execute.
- Direct repository runner enumeration through the available GitHub integration returns HTTP 403, so runner assignment cannot be inspected directly.

**INFERENCE (high confidence):** the live `oteryn-synology-staging` runner that executes `Oteryn-Platform` work is not registered/authorized for `blakinio/otclient`. Merely waiting for Oteryn jobs to finish is therefore not a reliable execution plan.

## Read-only cross-repository facts relevant to the blocker

From completed `Oteryn-Platform` runs on the actual Synology runtime:

- WARP userspace egress and real Tibia TCP confinement are proven there.
- Account credentials now succeed far enough to reach `Select Character`; prior row/OK and row-double-click attempts did not prove game-world entry and returned to the account-login state, with no proven decoded-map event.
- Renderer diagnostic run `31617864838`, job `94185070113`, proved Xvfb/GLX responds, direct rendering is available through software `llvmpipe`, OpenGL core 3+ is available, but Vulkan initialization fails and client logs contain a sanitized `failed vulkan instance` signature. This is a possible factor, not proof of the world-entry failure.
- Generic runtime/account warning evidence suggests a recovery/setup/create-character condition may exist, but it is not yet proven to be the reason existing-character world entry fails. Do not create, expose, or alter recovery/security material without an explicit authority path.

## Safety invariants

- Never use OCR/Tesseract/image-to-text for this task's login or success proof.
- Never expose secret values in command argv, logs, screenshots, repository files, artifacts, or chat.
- Never log in from the ordinary household/public egress; require verified changed tunnel egress first.
- Never touch canonical staging or the separately owned Oteryn analysis container/state.
- Do not accept a pixel/window change alone as successful world entry. Prefer a decoded Worldmap handler hit or an equivalently semantic runtime event.
- Leave the character idle if world entry is proven; no gameplay actions are authorized by this task.

## Validation record

```yaml
updated_at: 2026-08-12T18:40:00+02:00
branch_head_before_checkpoint: 877d1b3e9b4d2da14b01228e388989f724b46e29
pr: 48
status: blocked_on_execution_environment
secret_gate:
  run: 31616821899
  job: 94181592919
  result: PASS
hosted_attempts:
  - run: 31617222584
    job: 94182946084
    result: FAIL_PRE_CREDENTIAL
    blocker: missing_xdpyinfo
  - run: 31617541307
    job: 94184007303
    result: FAIL_PRE_CREDENTIAL
    blocker: official_launcher_http_403
  - run: 31617769586
    job: 94184760079
    result: FAIL_PRE_CREDENTIAL
    blocker: official_launcher_http_403_even_after_verified_warp
self_hosted_attempt:
  run: 31616469972
  job: 94180403029
  state_at_checkpoint: queued_no_steps
historical_self_hosted_evidence:
  run: 30223131080
  job: 89848906511
  result: cancelled_no_steps
safe_to_resume: true
```

`next_action`: make a trusted self-hosted runner with the `oteryn-staging` capability available to `blakinio/otclient` (or provide an equivalent trusted runner already authorized for this repository); then rerun the exact no-OCR workflow and accept success only from tunneled semantic/runtime world-entry evidence.
