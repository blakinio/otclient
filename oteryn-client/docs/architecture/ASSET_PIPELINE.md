# Asset Pipeline

## 1. Goal

Runtime assets are compiled, versioned and verified for the Oteryn client. The production runtime does not parse arbitrary legacy development formats on the frame path.

## 2. Pipeline

```text
source inputs
 -> provenance and license gate
 -> importer
 -> normalized asset model
 -> validation
 -> texture/audio/font/shader processing
 -> atlas or texture-array planning
 -> compression
 -> immutable pack index
 -> manifest + hashes + signature
 -> release artifact
```

Canary-compatible legacy formats may be imported by tools, but their layout does not define runtime memory structures.

## 3. Source classes

- original Oteryn-owned assets;
- independently licensed third-party assets;
- user-provided local assets where product policy permits;
- compatibility metadata/fixtures with documented provenance;
- prohibited proprietary content without redistribution rights.

Every distributable source records origin, version, license, transformation and resulting hash.

## 4. Logical identifiers

Runtime code uses typed logical identifiers:

```text
SpriteId
AppearanceId
UiImageId
FontId
SoundId
ShaderId
MaterialId
LocalizationBundleId
```

Filesystem paths and source file names are build-time concerns. IDs cannot be silently repurposed within a compatibility line.

## 5. Pack format requirements

A pack contains:

- format and schema version;
- product/asset-set version;
- compatibility metadata;
- bounded index and string tables;
- content chunks with offsets, lengths and compression methods;
- per-content hashes or authenticated aggregate structure;
- manifest hash/signature binding the complete pack;
- optional dependency graph;
- provenance reference for distributable releases.

The format supports memory mapping and range reads where useful. Every offset, length and count is validated before use.

## 6. Graphics processing

The compiler determines from measured asset constraints whether data uses atlases, texture arrays or a hybrid.

It may perform:

- color-space normalization;
- alpha/premultiplication policy;
- padding/bleed handling;
- mip generation where appropriate;
- block compression variants by quality tier;
- animation metadata packing;
- sprite trim/origin metadata;
- deterministic layout generation.

Atlas layout is reproducible from inputs and tool version. Runtime never relies on nondeterministic source directory order.

## 7. Text and fonts

Fonts require explicit redistribution rights. The build prepares font metadata and initial glyph/cache hints, while runtime text shaping remains capable of localization-specific glyph loading.

UI text is localization-key driven; rasterized text is not embedded into general UI images unless deliberately required.

## 8. Audio

Audio import normalizes sample format, loudness/category metadata and streaming policy. Short effects and long streams use separate runtime strategies.

Decoder work stays off the real-time audio callback. Pack metadata includes bounded decoded-size estimates.

## 9. Shaders

Shader sources are first-party reviewed inputs. Build tooling validates variants and records compiler/tool versions.

Runtime may create backend pipelines from controlled shader modules, but downloaded servers and extensions cannot inject arbitrary native shaders into the production renderer.

## 10. Runtime mounting

`asset-runtime`:

- verifies manifest/signature/hash before mount;
- verifies product/version compatibility;
- opens immutable packs read-only;
- exposes typed asset handles;
- streams/decompresses on workers;
- enforces CPU/GPU budgets;
- publishes readiness/failure without blocking the frame loop;
- rejects corrupt data and supports repair workflow.

A staging or download cache is never the authoritative runtime source.

## 11. Updates

Asset updates are staged separately and activated atomically. Client binary, protocol compatibility and required asset manifest are checked before game entry.

Rollback restores a complete previous compatible set. Partial mixed-version activation is forbidden.

## 12. Development mode

Developers may use loose source assets only under an explicit non-production mode with visible diagnostics. This mode:

- cannot be enabled by a game server;
- does not weaken release verification;
- never causes loose files to be included in release packages automatically;
- keeps deterministic rebuild tooling available.

## 13. Importer isolation

Legacy/Canary importers live in tools, not runtime engine crates. Malformed input is treated as hostile:

- bounded allocations;
- archive/path traversal prevention;
- decompression limits;
- checked image/audio dimensions;
- no execution of embedded scripts;
- fuzzable parser entry points.

## 14. Audit outputs required before implementation

- inventory of currently required asset types;
- exact legally usable source/provenance classification;
- size/count/dimension statistics;
- animation and transparency semantics;
- font/localization needs;
- audio format and streaming needs;
- candidate pack-size and GPU-memory estimates;
- compatibility mapping needed for the first Canary slice;
- list of content that must not enter the repository.

## 15. Acceptance tests

- deterministic pack output for identical inputs;
- invalid signature/hash rejection;
- corrupt index and out-of-bounds offset rejection;
- decompression bomb rejection;
- clean install, update, interruption and rollback;
- asset-set/client/protocol mismatch behavior;
- worker cancellation during relog/shutdown;
- GPU budget pressure and eviction;
- no proprietary fixture bytes in committed tests.
