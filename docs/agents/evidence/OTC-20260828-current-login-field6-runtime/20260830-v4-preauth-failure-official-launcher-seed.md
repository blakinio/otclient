# 2026-08-30 V4 pre-auth failure and official-launcher seed checkpoint

## Authority and current scalar state

- trusted `main` at checkpoint discovery: `18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`;
- `FIELD6_VALUE=UNKNOWN`;
- `physical_action_count=0`;
- `login_submit_count=0`;
- no character selection, world entry or gameplay occurred;
- no Tibia credential was exposed to the V4 capture step.

## Terminal V4 execution

- owner trigger comment: `5467500633`;
- one-time label: `field6-v4-5467500633`;
- workflow run: `33300352335`, attempt `1`;
- live job: `99227195253`;
- runner: `molehill-otclient-v4-01`;
- clean guest: `OTClientV4Clean`;
- result: `failure` before authorization consumption;
- first failing step: `Materialize exact current package through task-owned WARP`;
- WARP proof: `TRACK_A_FIELD6_PACKAGE_WARP=PASS attempt=1`;
- materializer failure: `FETCH_FAILED:curl_22`;
- authorization, secret-bearing capture and scalar validation steps: `skipped`;
- ephemeral runner deregistered and `OTClientV4Clean` was destroyed after the terminal result.
## Root cause

The official client manifest remained current and valid:

- `package.json` HTTP status: `200`;
- manifest version: `15.32.75d4a0`;
- manifest file count: `1634`.

Direct binary-file requests made by the custom curl materializer returned Cloudflare managed challenge responses:

- HTTP `403`;
- `Cf-Mitigated: challenge`;
- therefore the custom curl downloader is no longer an admissible/reliable acquisition path.

This was not a client-fence movement and not a V4 runtime/credential failure.

## Existing official launcher discovery

Molehill-PC already contained two identical official Linux launcher archives:

- `C:\Users\barte\Downloads\tibia.x64 (1).tar.gz`;
- `C:\Users\barte\Downloads\tibia.x64 (2).tar.gz`;
- archive SHA256: `04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7`;
- archive size: `29477141` bytes;
- launcher ELF SHA256: `a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0`.

The archive itself is the launcher, not the full game package.
## Official-launcher package proof

A fresh throwaway WSL2 guest `OTClientInstallerProbe` was imported from the already-pinned Canonical rootfs. Host automount/interop was disabled before the useful launcher run. No credentials or login were used.

The official launcher was run under isolated X11 and its install button was activated once. It successfully downloaded the current package through its own updater and recorded:

```text
Package Tibia with version 15.32.75d4a0 is now fully installed
Installation of package "Tibia" finished.
```

The resulting official package proved the exact Track A fence:

- `bin/client` size: `52105824`;
- `bin/client` SHA256: `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`;
- package manifest version: `15.32.75d4a0`;
- package manifest rows: `1634`;
- asset manifest rows: `7094`;
- resulting package file count including four manifest/version files: `8732`.

The probe guest was destroyed after the package was frozen.
## Frozen local seed

The launcher-installed package was frozen locally on Molehill-PC as:

`C:\OTClientV4\tibia-15.32.75d4a0-official-launcher-seed.tar.gz`

Seed facts:

- size: `412272538` bytes;
- SHA256: `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`;
- proprietary package bytes are intentionally **not** committed to GitHub;
- repository evidence retains only public/sanitized hashes, sizes, manifest counts and provenance.

## Repository repair checkpoint

Fresh repair branch from trusted `main@18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`:

`fix/OTC-20260830-field6-official-launcher-seed`

New RED test:

`.github/scripts/test_track_a_current_client_package_seed.py`

Observed causal RED:

`FIELD6_SEED_RED: materialize_seed missing`

No production seed-import implementation exists yet. V5 must not be admitted or triggered until the repository-only seed path is implemented, audited, exact-head green and merged to trusted `main`.
