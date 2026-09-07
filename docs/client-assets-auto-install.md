# Client Assets Auto-Install

This document describes the automatic client assets installation flow introduced in OTClient.

## Goal

For modern Tibia client versions (>= 1281), OTClient must be able to:

1. Detect missing assets for the selected version.
2. Prompt the user to download required assets.
3. Download and install assets automatically.
4. Keep final installed files in the same paths already used by OTC runtime.

## Final Install Paths (Source of Truth)

Installed assets must end up in:

- `data/things/<version>/`
- `data/sounds/<version>/`
- runtime extras (when provided by upstream package), such as `bin/*`, in client runtime paths.

Do not introduce an alternative permanent assets root for runtime loading.

For a modern client version to be considered complete, the things directory must contain `catalog-content.json`, `assets.json.sha256`, and the catalog-referenced appearances/static-data files. The installer writes `.client-assets-complete` only after those runtime-path checks pass.

## Main Module

- Lua module: `modules/client_assets/client_assets.lua`
- Release preparation policy: `modules/client_assets/client_assets_release_selector.lua`
- Conditional GitHub releases adapter: `modules/client_assets/client_assets_release_adapter.lua`
- Enter-game integration: `modules/client_entergame/entergame.lua`
- Modern things/sounds loading: `modules/game_things/things.lua`

## Download / Install Strategy

The flow supports:

- archive installation from a matching release/tag archive as the default path
- codeload source ZIP fallback when a release contains no matching archive
- manifest-driven installation as a fallback path when the archive cannot be installed
- manifest hash identifier installation into `data/things/<version>/assets.json.sha256`
- packaged files list (including large binaries distributed as `.zip`/`.rar`)
- extraction of `.zip` and `.rar`
- optional `.lzma` decompression

### Release archive selection

GitHub release JSON is prepared before the existing resolver caches it:

1. Each release is evaluated from its own tag/name, so cache contents are stable across later client-version requests.
2. Only non-macOS ZIP/RAR assets that identify the release tag or version label are candidates.
3. A candidate containing `client` is preferred; `original` and `linux` variants receive a lower score.
4. `.app.zip`, `macos`, and standalone `mac` variants are excluded.
5. If no archive matches, every archive candidate is removed from the prepared release copy. The existing resolver therefore returns no release archive and uses its established codeload ZIP fallback.
6. Non-archive metadata assets remain present.

This policy prevents an unrelated legacy ZIP from being selected only because it appears first in a release.

### Configured release archive digest

When the configured GitHub Releases response supplies a selected asset `digest` using the `sha256:<hex>` form, the conditional release adapter binds that digest to the exact selected `browser_download_url`. The downloaded archive is read from the existing download cache and its SHA-256 is verified before the installer callback can begin extraction. A mismatch fails closed.

The adapter does not apply a digest from one URL to another, does not infer a digest for codeload fallback archives, and does not intercept unrelated HTTP downloads. Its `HTTP.getJSON` and `HTTP.download` wrappers are restored on module unload. A release asset without a valid SHA-256 digest retains the existing manifest/content integrity boundaries and cannot by itself satisfy the production archive-integrity rehearsal gate.

## Integrity and Security Defaults

Defaults are hardened:

- `strictManifestSha256 = true`
- `allowRawFallbackHashMismatch = false`
- `allowMissingPackedRawFallback = true`

`allowMissingPackedRawFallback` is a narrow compatibility fallback for repository releases that reference official `.lzma`/archive package files not stored in the assets repository. It is only used after the packed file is missing and the client falls back to the raw file from the same manifest/release source. It does not enable arbitrary hash mismatches for normal raw downloads.

Release cache is scoped per source (`releasesUrl` / repository key), avoiding stale cross-source reuse. Release archive preparation is idempotent and per-release, avoiding request-specific cache poisoning.

## Runtime/Platform Notes

- Desktop targets use `libarchive` for archive extraction when it is available.
- Builds without `libarchive` still extract `.zip` archives through the vendored minizip fallback. This keeps the GitHub source ZIP flow functional on clean desktop builds.
- `.rar` extraction requires `libarchive`. If a packaged `.rar` is optional and the build cannot extract it, installation should fail clearly or skip it according to the package configuration.
- The default flow is archive-first only when a matching release archive exists. The codeload ZIP and manifest paths remain compatibility fallbacks.
- Emscripten login fallback was aligned with native `httpLogin` semantics.

## UX Behavior

- Missing-assets dialog prompts before download.
- Download window supports cancellation.
- Progress supports indeterminate mode when remote does not provide reliable content length.
- Console logs show major phases and final install paths.

## Validation Evidence

Synthetic fixtures must cover:

- a matching tag/client archive among unrelated legacy, Linux, original and macOS archives;
- a release containing only unrelated/macOS archives, which must force codeload fallback;
- a generic tag whose version is present in the release name;
- idempotent preparation of cached releases;
- valid and invalid GitHub release SHA-256 digest normalization;
- exact selected-URL archive verification, mismatch rejection and unrelated-download passthrough;
- final things/sounds/extras paths;
- runtime completeness requiring catalog/hash/appearances/static-data files.

Before claiming production runtime archive compatibility, perform a networked rehearsal against the configured real release source on a clean writable directory:

1. record release/tag and selected URL;
2. verify archive hash/integrity behavior remains strict;
3. verify final paths and completion marker;
4. start the exact client version and prove appearances/static data load;
5. remove the rehearsal directory or retain it only as an external CI artifact, never in Git.

If the execution environment cannot download real release artifacts or start the client, record that as an explicit blocker. Synthetic fixtures and compiled CI do not replace this rehearsal.

## Troubleshooting

### 1) Assets appear downloaded but game still cannot load

Check:

- `data/things/<version>/catalog-content.json`
- `data/things/<version>/assets.json.sha256`
- catalog-referenced appearances/static-data files
- `data/sounds/<version>/catalog-sound.json` (when sounds are enabled)

### 2) Missing `.lzma` package file

If the console shows a 404 for `*.lzma`, the client is using the manifest fallback instead of a matching release archive/codeload source ZIP. First check why archive installation failed. The manifest fallback can install raw files through `allowMissingPackedRawFallback`, but this path is slower and should not be the normal flow for clean installs.

### 3) SHA-256 mismatch

By default, mismatches fail installation. Verify upstream files and hashes first before changing integrity flags. For a selected configured GitHub release asset, also confirm the release JSON contains a valid `sha256:<hex>` digest for the exact archive URL recorded by the installer.

### 4) Slow progress / “stuck”

If Content-Length is missing, UI may run in indeterminate mode during download and extraction. Use console logs to confirm active phase.

## Configuration (init.lua)

`Services.clientAssets` supports runtime behavior controls (repository, archive preference, sounds, packaged files, hash strictness, etc.). Keep secure defaults unless there is a specific compatibility reason to relax.

## Maintenance Checklist

When changing this system, validate:

1. Missing assets prompt appears for modern version.
2. A matching release archive is selected, or the resolver falls back to codeload when no match exists.
3. A configured selected release asset with a valid GitHub SHA-256 digest is verified before extraction.
4. Install completes into `data/things/<version>` and `data/sounds/<version>`.
5. Runtime loads modern assets from those paths.
6. Hash verification behavior matches configuration.
7. Windows required CI remains green; dormant platforms require their own acceptance before compatibility claims.
