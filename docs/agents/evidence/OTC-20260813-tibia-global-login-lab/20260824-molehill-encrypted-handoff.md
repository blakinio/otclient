# 2026-08-24 Molehill current-assets and encrypted-handoff checkpoint

Task: `OTC-20260813-tibia-global-login-lab`
Track: `OTCLIENT-GLOBAL-LOGIN` / `otclient-global-login`
Canonical PR: #284
Repository: `blakinio/otclient`

## Purpose

Persist the material facts discovered after the 2026-08-23 restack so a replacement worker can continue without chat history. This checkpoint does **not** claim `GAME_START` or `IN_GAME`.

## GitHub-hosted CDN boundary â€” PROVEN

Fresh secret-free discriminators showed that `https://static.tibia.com/launcher/assets-current/assets.json` is blocked for GitHub-hosted egress:

- Ubuntu 24.04: HTTP 403;
- Windows 2025: HTTP 403;
- macOS 15: HTTP 403.

The same hosted environment also received HTTP 403 for the public Linux launcher archive `https://static.tibia.com/download/tibia.x64.tar.gz`.

The current Linux package manifest endpoint remains reachable. `tibiaclient-linux-current/package.json` reported version family 15.32, generation `second`, 1634 files, and only `bin/*` plus `3rdpartylicences/*`; it contains no gameplay `assets/*` records. Therefore the binary package manifest cannot replace the separate assets catalog.

## Molehill official current cache â€” PROVEN

On `Molehill-PC`, the existing `tibia-kasm` container exposes the previously installed official package under:

`/legacy-home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/`

Read-only verification produced:

```text
PACKAGE_VERSION=15.32.bf29ac
CLIENT_SIZE=52109920
CLIENT_SHA=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ASSET_EXPECTED=d1969b4ba69339fcea5ea52aa1bfe3eaf0b7800226a3635c1e71de87235837f9
ASSET_ACTUAL=d1969b4ba69339fcea5ea52aa1bfe3eaf0b7800226a3635c1e71de87235837f9
CATALOG_SHA=6156366d9489d20bf2ec330f2365f3b328e36cbd57cdcdeba01706259e83765b
```

Current login-relevant files are present:

```text
appearances-063e8d11a76a6f95bd986812808b52db4158a05601e7ea5cf0cb688fa9e36d57.dat  5017898 bytes
staticdata-62d3f5f761a4c8cab02c89bd1a351770aca3504a74f1b34f457f0a0451dcd128.dat   178944 bytes
catalog-content.json                                                        1042224 bytes
```

The official launcher was then started locally using the existing Kasm X11 authority and legacy package HOME. It classified the package as `InstalledAndUsable`, launched the exact `bin/client` above, and logged `Asset loading complete`. No account credentials were read or copied during this verification.

Existing local lab containers remain separate:

```text
tibia-kasm     official client / KasmVNC
otclient-kasm  OTClient / KasmVNC
```

This makes Molehill the preferred current-assets source for the next Track B experiment. Do not upload proprietary asset bytes to GitHub.

## Synology / secret boundary â€” CURRENT BLOCKER

GitHub currently reports only `synology-otclient-01` as the registered repository self-hosted runner and it is offline. Molehill can reach `synology.local` at `192.168.1.21`, but has no working BatchMode SSH key and no Docker context for the NAS.

Repository policy explicitly keeps `secret-ingress` on the trusted GitHub Actions boundary; do not invoke it through Remote Desktop Commander. The previously documented encrypted secret vault belongs to the Synology runner state and was not found on Molehill.

A local ephemeral Actions runner image was built successfully on Molehill and could see the Docker Desktop daemon plus both lab containers, but the current tool safety layer blocked passing a short-lived runner registration token into that container. Do not bypass that boundary.

## Encrypted one-shot handoff â€” IMPLEMENTED LOCALLY, NOT YET LIVE-PROVEN

To preserve the GitHub-Secret boundary while moving only the one-shot game handoff to Molehill, the current WIP introduces an isolated producer lane under `.github/track-b-encrypted-handoff/**`.

Intended flow:

```text
GitHub Actions Secrets
  -> existing proven HTTPS login through userspace WARP
  -> reduce response to sessionKey/worldName/worldHost/worldPort/characterName in tmpfs
  -> CMS AES-256-CBC encrypt with Molehill public recipient certificate
  -> delete plaintext request/response/handoff
  -> upload only handoff.cms with retention 1 day
  -> Molehill downloads ciphertext
  -> local private-key decrypt
  -> local OTClient uses current verified assets for game-login
```

The private key remains outside Git on Molehill in a task-owned directory under `%LOCALAPPDATA%\OTClientKasmVNC\trackb-handoff-key\`. It must never be committed, uploaded, printed, copied into Actions, or returned to a model.

The committed public certificate fingerprint is expected to be:

`D2:DF:1E:AB:61:1C:39:01:8F:9B:14:1A:7D:CD:C9:A3:F4:68:72:A8:73:2E:57:51:E8:B0:63:A5:CE:E5:F4:B5`

Current isolated WIP paths:

```text
.github/workflows/tibia-global-login-encrypted-handoff.yml
.github/track-b-encrypted-handoff/prepare.sh
.github/track-b-encrypted-handoff/emit.sh
.github/track-b-encrypted-handoff/recipient.pem
.github/scripts/test_track_b_encrypted_handoff.py
```

Focused local validation on 2026-08-24:

```text
TRACK_B_ENCRYPTED_HANDOFF_CONTRACT=PASS
BASH_SYNTAX=PASS
YAML_PARSE=PASS
CMS_ROUNDTRIP=PASS  # synthetic handoff only; no Tibia secret value
```

The new workflow path is intentionally outside `tools/tibia-global-login-lab/**`, so committing this checkpoint does not itself match the old full login-lab path filter. The encrypted producer has not yet been executed in GitHub Actions and no ciphertext has yet been consumed by Molehill.

## Current semantic state

PROVEN: HTTP auth/session/playdata path works historically; current Molehill package/assets are exact current 15.32; GitHub-hosted CDN access is insufficient; local official assets are usable; CMS transport works synthetically.

UNKNOWN: encrypted producer live result; local ciphertext decrypt result; next OTClient game-server response; `GAME_START`; authoritative local-player/world state.

No protocol mutation is justified by this checkpoint.

## Exact next action

1. Revalidate live PR #284 head and confirm no concurrent Track B writer.
2. Validate the isolated encrypted-handoff files on that exact head.
3. Publish the checkpoint to the canonical branch `feat/OTC-20260813-tibia-global-login-lab` without touching Track A paths.
4. Execute only the isolated encrypted-handoff producer workflow and inspect its fixed non-secret markers.
5. If `handoff.cms` is produced, download only that ciphertext to Molehill, verify the public-certificate fingerprint, decrypt locally with the task-owned private key, and never print plaintext values.
6. Stage the already verified Molehill current 15.32 assets into the local Track B OTClient runtime, consume the decrypted handoff once, and perform one bounded game-login attempt.
7. Classify the first game-server outcome (`GAME_START`, structured server opcode, or exact harness failure). Do not change protocol fields before that result.

Stop only for a real safety/authority blocker, unavailable required secret boundary, ownership conflict, or a newly proven protocol boundary that requires separate promoted evidence.
