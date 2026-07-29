# W6 Synthetic Asset Format and Security Evidence

Evidence cut: implementation branch after Rust Client run `30479573355` on 2026-07-29; final synchronized validation pending after full-diff hardening.

## Scope

W6 adds one bounded offline synthetic asset contract and compiler:

- `oteryn-asset-types`, category `asset-types`;
- `oteryn-asset-compiler`, category `tool`;
- original synthetic blob and raw RGBA8 fixtures only;
- no asset runtime, renderer/GPU integration, game importer, network input, updater, signing or production pack.

## Manifest schema version 1

The compiler accepts one UTF-8 JSON object no larger than 1 MiB with exactly:

```json
{
  "schema_version": 1,
  "assets": []
}
```

Each asset is a strict object. Unknown root or record fields are rejected.

Common record fields:

- non-zero unsigned 32-bit `id`;
- `kind`, exactly `blob` or `rgba8`;
- bounded non-empty `name`, `license` and `provenance` strings without control characters;
- relative normalized `source` under the manifest directory.

RGBA8 records additionally require unsigned 32-bit `width` and `height`.

## Pack schema version 1

The original pack is deterministic and little-endian:

1. 8-byte magic `OTASSET1`;
2. `u16` schema version, currently 1;
3. `u32` record count;
4. records sorted by ascending `AssetId` regardless of manifest order.

Each record contains:

1. `u32` non-zero ID;
2. `u8` kind code: 1 for blob, 2 for RGBA8;
3. `u32` width and `u32` height, both zero for blobs;
4. three `u16` length-prefixed UTF-8 strings: logical name, license and provenance;
5. 32-byte SHA-256 payload digest;
6. `u32` payload length;
7. exact payload bytes.

The decoder rejects bad magic, unsupported versions, unknown kinds, non-canonical order, duplicates, invalid UTF-8, malformed/truncated input, trailing bytes, invalid RGBA8 shape, digest mismatch and every configured bound violation.

## Synthetic schema-v1 limits

| Limit | Value |
|---|---:|
| records | 4,096 |
| payload per record | 16 MiB |
| encoded pack | 64 MiB |
| RGBA8 width or height | 16,384 |
| logical name | 128 UTF-8 bytes |
| license identifier | 64 UTF-8 bytes |
| provenance | 512 UTF-8 bytes |
| manifest JSON | 1 MiB |

All count, length, pixel and allocation calculations use checked conversions/arithmetic. RGBA8 requires non-zero dimensions and an exact checked `width * height * 4` payload length.

These values are synthetic engineering limits, not production budgets or compatibility claims.

## Filesystem boundary

The compiler:

- accepts only relative normalized source paths;
- rejects empty, absolute, rooted, prefixed, current-directory, parent-directory, colon-containing and backslash-containing paths;
- checks every path component with `symlink_metadata` and rejects symbolic links;
- canonicalizes the final source and proves containment under the canonical manifest root;
- rejects directories and non-regular files;
- checks metadata length before allocation and caps the subsequent read;
- never stores source paths or source-machine absolute paths in pack bytes;
- exposes stable reviewed error text without arbitrary OS error strings;
- uses `symlink_metadata` to require that no filesystem entry, including a dangling symlink, already occupies the final output path;
- requires the same-directory temporary output path to be absent;
- writes with `create_new` to that temporary file, syncs it and renames it only after complete validation/encoding;
- removes a failed temporary output and preserves an existing final output or stale temporary entry.

W6 does not recursively discover directories, parse archives, decompress data, execute scripts, watch files or access a network.

## Dependency evidence

| Dependency | Resolution | Purpose | Evidence boundary |
|---|---|---|---|
| `serde_json` | exact workspace `1.0.145` | constrained manifest parsing and test JSON encoding | existing approved workspace dependency |
| `sha2` | exact direct `0.11.0`, defaults disabled | SHA-256 only | MIT OR Apache-2.0; declared Rust 1.85; resolved by generated lockfile |
| `digest` | transitive `0.11.3` | hash trait implementation | generated lockfile and cargo-deny authoritative |
| `block-buffer` | transitive `0.12.1` | SHA-256 implementation support | generated lockfile and cargo-deny authoritative |
| `crypto-common` | transitive `0.2.2` | digest implementation support | generated lockfile and cargo-deny authoritative |
| `hybrid-array` | transitive `0.4.13` | fixed-size digest storage | generated lockfile and cargo-deny authoritative |
| `typenum` | transitive `1.20.1` | compile-time digest dimensions | generated lockfile and cargo-deny authoritative |
| `cpufeatures` | transitive `0.3.0` | target CPU feature selection | generated lockfile and cargo-deny authoritative |

The new resolution also reuses the already-present `cfg-if` and `libc` packages. Generated `Cargo.lock` records SHA-256 crate checksum `446ba717509524cb3f22f17ecc096f10f4822d76ab5c0b9822c5f9c284e825f4`. No cargo-deny policy weakening was required.

## Original fixture provenance

All files under `oteryn-client/assets/test-fixtures/synthetic-v1/` were created specifically for this repository:

- `manifest.json`: original constrained schema-v1 manifest;
- `blob.txt`: original short synthetic text payload;
- `checker.rgba`: original 16-byte synthetic 2x2 RGBA8 payload.

They contain no Tibia, Canary or other third-party game assets.

## Automated evidence

Rust Client run `30479573355` used hosted Microsoft Windows Server 2025, OS build `10.0.26100`, runner image `windows-2025-vs2026`, Rust 1.94.

PASS on that implementation head:

- `cargo metadata --locked`;
- `cargo fmt --all -- --check`;
- workspace Clippy with warnings denied;
- all workspace tests then present;
- architecture policy;
- cargo-deny advisories, licenses, bans and sources.

Full-diff review then added tests for:

- zero IDs, empty/control/oversized metadata;
- unsupported pack version, unknown kind and non-canonical record order;
- oversized encoded record count and payload length before allocation/read;
- unsupported manifest version, unknown kind, duplicate IDs and record-count overflow;
- oversized manifest and sparse oversized source rejection;
- stale temporary output preservation;
- dangling final-output symlink rejection on platforms where symlink creation is permitted;
- Unix-gated non-regular socket rejection.

Final synchronized exact-head CI is required before merge and supersedes `30479573355` as merge evidence.

Previously validated and retained tests cover:

- known SHA-256 vector;
- byte-identical repeated compilation and manifest-order independence;
- encode/decode round trip;
- duplicate, malformed, truncated, trailing, digest and RGBA8 failures;
- portable absolute/parent/prefix/separator path rejection;
- Windows source-symlink rejection when the runner permits symlink creation;
- directory rejection;
- preservation of an existing final output;
- absence of the source-machine absolute path in compiled bytes.

## Explicitly unproven or blocked

The automated evidence does not prove:

- production asset format compatibility with Tibia or Canary;
- legal redistribution rights for any real game assets;
- import of official/proprietary sprites, appearances, sounds, maps or metadata;
- runtime mounting, streaming, caching, activation or rollback;
- renderer/GPU upload, visual correctness or texture strategy;
- authenticated manifests, signatures, update-channel trust or download security;
- production compiler throughput, pack size, memory, latency or hardware targets;
- behavior on every supported Windows filesystem/security-policy configuration.

W6 is an offline synthetic contract and compiler only.
