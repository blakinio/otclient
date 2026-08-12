# OTC-20260727 — Tibia Linux runner analysis

## Status

`active_hosted_direct_package_login` — the previous hosted-runner launcher blocker has been narrowed: the official launcher archive can be fetched through verified WARP with the established request shape, but the launcher itself does not create a usable X11 window on GitHub-hosted Ubuntu. The current execution path therefore bypasses the launcher and reconstructs the exact official package directly from CipSoft package metadata before attempting a no-OCR login/world entry.

This is an operational research task. Do not merge temporary workflows as product code. Do not commit/upload proprietary CipSoft bytes, credentials, account/character data, cookies, session material, authenticated screenshots, or recovery material.

## Objective

Attempt a real official-client login/world entry **without OCR/Tesseract/image-to-text**, with credentials injected only from GitHub Actions secrets, a changed WARP egress proven before secret use, actual Tibia TCP confined to that tunnel, and success accepted only from non-image runtime/protocol evidence.

## Ownership

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` (draft operational PR)
- Session: `chatgpt-20260812-no-ocr-world-entry`
- Separate active runtime `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811` is read-only evidence for this task. Its `oteryn-tibia-client-analysis` container/state must not be mutated or reused.
- Canonical `oteryn-staging` Compose services remain strictly out of scope.

Owned task paths:

- `.github/workflows/tibia-linux-runner-analysis.yml`
- `.github/workflows/tibia-no-ocr-secret-gate.yml`
- `.github/workflows/tibia-hosted-no-ocr-login.yml`
- `.github/workflows/tibia-hosted-no-ocr-login-v2.yml`
- `.github/workflows/tibia-hosted-no-ocr-login-v3.yml`
- `.github/workflows/tibia-hosted-no-ocr-login-v4.yml`
- `.github/workflows/tibia-hosted-download-shape-probe.yml`
- `.github/workflows/tibia-hosted-launcher-runtime-probe.yml`
- `.github/workflows/tibia-hosted-direct-package-no-ocr-login.yml`
- `docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md`

Temporary hosted-login/probe workflows are operational scaffolding and must be removed before terminal closeout after their run/job IDs are retained here.

## PROVEN — no-OCR preparation

- `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` are both non-empty GitHub Actions secrets in `blakinio/otclient`: run `31616821899`, job `94181592919`, SUCCESS. The job emitted only boolean presence markers; values remained GitHub-masked and were not persisted.
- Tesseract/OCR is explicitly absent from the strict no-OCR execution path and success is not accepted from image text.
- The researched official Linux executable evidence cut is client `15.32.df7b29`, size `51,965,216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Packed `bin/client.lzma` identity from the signed package metadata is SHA-256 `496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b`; its CipSoft envelope carries an LZMA-alone header beginning at offset 32 and raw compressed data from offset 45.
- Reusable decoded-world boundary from read-only Oteryn evidence: FullMap `0xcec8d0`, FieldData `0xcd3190`, Create `0xcecc70`, Change `0xcecf40`, Delete `0xcd4e20`, common ordered map routine `0x19a8a80`.

## PROVEN — hosted runner network/download path

- Earlier direct requests to `https://static.tibia.com/download/tibia.x64.tar.gz` returned HTTP 403.
- Run `31619229063`, job `94189552673`, proved the established browser-compatible request shape through pinned userspace WARP can download the official launcher archive successfully: size `29,477,141`, SHA-256 `04a87c...60ea7`; direct remained blocked while WARP succeeded.
- The same WARP path proves `warp=on`, changed public egress, and can be consumed through `proxychains4`/SOCKS5 at `127.0.0.1:25344`.
- Do not brute-force public proxies or weaken the egress/secret boundary.

## PROVEN — hosted launcher failure is not the package-download blocker

- Run `31619497616`, job `94190454924`, advanced the full no-OCR workflow through secret availability, WARP setup, and official launcher download but failed before credential entry while waiting for a usable launcher X11 window/runtime materialization.
- Run `31619835423`, job `94191588183`, isolated launcher behavior: the downloaded official launcher did not yield a usable visible `Tibia` window on the GitHub-hosted Xvfb environment, both directly and through proxychains-localnet.
- Therefore the current hosted strategy bypasses launcher UI completely instead of adding OCR or more guessed launcher clicks.

## Read-only cross-repository bootstrap evidence

Completed `Oteryn-Platform` analysis established the package layout needed to reconstruct the exact official runtime without copying proprietary bytes between repositories/runners:

- package metadata endpoint: `https://static.tibia.com/launcher/tibiaclient-linux-current/package.json` with `package.json.version` as the version marker;
- package file entries carry `url`, `packedhash`, and `unpackedhash`;
- example packed object URL: `https://static.tibia.com/launcher/tibiaclient-linux-current/bin/client.lzma`;
- the exact current executable was reconstructed by verifying the packed hash, decoding the custom 32-byte-prefix + LZMA-alone envelope, and verifying the unpacked hash/size;
- this evidence is read-only input. No Oteryn container/state is reused or mutated by this task.

## Read-only cross-repository world-entry findings

The separate Synology investigation has authenticated the account and reached `Select Character`, but still has not proven world entry. Its latest durable evidence places that failure locally before an Internet-family game-session connect, and has excluded wrong credentials, obvious wrong-row selection, WARP failure, proxychains alone, root execution alone, and missing Vulkan alone as sufficient explanations. This task does not modify that runtime; the hosted environment is intentionally an independent execution path.

## Safety invariants

- Never use OCR/Tesseract/image-to-text for this task's login or success proof.
- Never expose secret values in command argv, logs, screenshots, repository files, artifacts, or chat.
- Never log in from ordinary/direct egress; require verified changed WARP egress first.
- Never touch canonical staging or the separately owned Oteryn analysis container/state.
- Do not accept a pixel/window change alone as successful world entry. Prefer a decoded Worldmap handler/common-routine hit or an equivalently semantic runtime event.
- Leave the character idle if world entry is proven; no gameplay actions are authorized by this task.

## Validation record

```yaml
updated_at: 2026-08-12T19:05:00+02:00
branch_head_before_checkpoint: de8833721f2bcf5f0b80837d7faca3b222e74e9f
pr: 48
status: active_hosted_direct_package_login
secret_gate:
  run: 31616821899
  job: 94181592919
  result: PASS
download_shape_probe:
  run: 31619229063
  job: 94189552673
  result: PASS_WARP
full_hosted_v4:
  run: 31619497616
  job: 94190454924
  result: FAIL_PRE_CREDENTIAL
  blocker: launcher_window_or_runtime_materialization
launcher_runtime_probe:
  run: 31619835423
  job: 94191588183
  result: FAIL
  blocker: no_usable_launcher_x11_window
safe_to_resume: true
```

`next_action`: reconstruct the complete `15.32.df7b29` package directly from the official package manifest on the GitHub-hosted runner through verified WARP; launch the exact client without OCR; inject the existing Actions secrets; activate the deterministic first-character target; accept success only on a decoded Worldmap runtime hit and keep all credential/account data out of logs/artifacts.