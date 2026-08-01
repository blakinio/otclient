# P0 Asset Runtime and Import Roadmap

Status cut: `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Lane: `OTC2-20260801-playability-p0-assets` / PR #142  
Implementation authorized: **false**

## 1. Objective

Define the smallest dependency-ordered path from approved inputs to verified runtime-visible world, UI, text and audio resources while preserving provenance, security, deterministic builds and renderer/audio/UI ownership.

This roadmap builds on the existing synthetic schema/compiler. It does not declare schema-v1 production-ready, select an official/proprietary source or authorize an importer/runtime implementation.

## 2. Existing contracts to preserve

### `oteryn-asset-types`

Current sole owner of:

- non-zero synthetic `AssetId`;
- bounded metadata including license/provenance;
- Blob/RGBA8 validation;
- payload SHA-256;
- canonical schema-v1 pack encoding/strict decoding;
- closed stable errors.

### `oteryn-asset-compiler`

Current offline tool owner of:

- strict JSON manifest schema-v1;
- relative source path validation;
- capability-rooted no-follow component opening;
- same-handle type/size/read validation;
- output preservation and atomic temporary-file commit;
- deterministic synthetic pack generation.

These packages remain synthetic foundations. Later work extends or supersedes production contracts explicitly; it does not silently overload current types with unreviewed formats or rights assumptions.

## 3. Required architecture boundary

```text
approved source input
-> offline acquisition/provenance gate
-> source-family importer
-> normalized intermediate records
-> deterministic pack builder
-> signed/authenticated immutable pack
-> runtime open/verify/index
-> logical handles + generations
-> bounded decode/stream/cache
-> renderer/UI/text/audio resource realization
```

Offline importers never become frame-runtime dependencies. Runtime never opens arbitrary loose source trees or invokes an importer to make gameplay continue.

## 4. Phase A — production pack contract decision

### Sole producer

A focused asset-pack contract task owns the production schema/versioning decision. It may reuse compatible schema-v1 concepts but must not assume raw Blob/RGBA8 is sufficient.

### Required outputs

- logical resource/appearance identifiers and namespaces;
- pack/manifest schema and canonical encoding;
- exact limits for entries, strings, offsets, decoded sizes and dependencies;
- resource family metadata for world appearances, UI/text/fonts and audio;
- compatibility range: client schema, server/profile/build and asset source revision;
- payload/content hashes and authenticated manifest/signature design;
- provenance/license/notice index;
- deterministic build identity;
- pack dependency/overlay policy if needed;
- upgrade/migration/unsupported-version behavior;
- stable closed error/action model.

### Acceptance

- original synthetic positive/negative fixtures;
- deterministic byte-identical shuffled/repeated builds;
- malformed/truncated/trailing/duplicate/overflow/bomb negatives;
- capability and architecture review;
- rights decision for every fixture/input family.

No consumer publishes substitute pack/index/handle types while this producer is unresolved.

## 5. Phase B — runtime open, verify, index and lookup

### Candidate package

`asset-runtime` as the sole runtime pack owner.

### Responsibilities

- open only explicit approved pack locations/handles;
- validate regular-file/object identity appropriate to the platform;
- enforce pack-size and manifest/index bounds before allocation;
- verify schema/profile/version and authenticated manifest/signature;
- verify content hashes before exposing records;
- parse/index canonically with checked offsets/ranges;
- expose immutable logical lookup handles;
- bind handles to pack/resource generations;
- reject stale handles after replacement/rollback;
- publish safe diagnostics and recoverable actions;
- support transactional mount/replacement, not partial activation;
- expose notices/provenance metadata required by product UI/support.

### Must not

- decode/upload on frame-critical calls;
- read source manifests/loose importer files;
- own GPU/audio devices or widget state;
- infer server profile from filenames;
- silently fall back to unsigned/unsupported content;
- mutate active packs in place.

### Focused tests

- valid minimal/multiple pack lookup;
- wrong signature/hash/schema/profile/version;
- malformed counts/offsets/overlap/trailing data;
- source/path/symlink/reparse/special-file acquisition as relevant;
- pack replacement and stale generation;
- interrupted/corrupt/partial pack rejection;
- duplicate logical identifiers/dependencies;
- deterministic index order and error codes;
- no arbitrary source path in errors.

## 6. Phase C — logical resource and appearance contracts

### Sole producers

The P0 aggregation must decide whether these live in one asset contract or separate narrow producers:

- `AppearanceId`/world visual metadata;
- texture/image resource handles;
- UI/icon/cursor/theme handles;
- font/text source handles;
- audio resource handles.

### Required invariants

- logical/server appearance identifiers are distinct from pack offsets and GPU handles;
- runtime handles are generational and cannot escape the active pack lifetime;
- protocol adapters map exact producer IDs to stable domain/asset references without exposing wire fields to renderer/UI;
- renderer/audio/UI consume logical handles and prepared resources only;
- fallback/missing resource policy is explicit and does not hide incompatible required content;
- feature/profile capability gates are versioned.

## 7. Phase D — bounded decode and preparation

### Asset-runtime decode layer

Owns:

- bounded worker scheduling outside frame-critical work;
- compressed/encoded input validation;
- decoded dimension/sample/count limits;
- cancellation and session/pack generation;
- result cache and failure classification;
- decompression/image/audio bomb defenses;
- deterministic preparation where applicable;
- no direct GPU/audio callback mutation.

### Renderer resource layer

Consumes prepared image/appearance records and owns:

- texture/atlas/array realization;
- logical handle -> GPU resource generation mapping;
- bounded upload queues;
- cache budgets/eviction/pressure metrics;
- device-loss re-realization;
- placeholders only under an explicit product policy;
- no source/import/license parsing.

### Text/UI resource layer

Owns or consumes an accepted producer for:

- font selection/fallback metadata;
- shaping inputs and shaped run/glyph handles;
- glyph raster/cache/atlas realization;
- DPI/scale generation;
- UI image/theme/cursor realization;
- localization text remains separate from image assets.

### Audio resource layer

Consumes prepared audio records and owns:

- resident versus streaming preparation;
- sample/stream buffer budgets;
- logical handle -> prepared audio generation mapping;
- no file/decode work in the real-time callback;
- recovery after device replacement;
- category/voice policy remains in `audio-core`.

## 8. Phase E — source-family importers

Each source family is a separate offline tool package/task after the rights matrix accepts it.

### Common importer contract

Every importer:

- identifies exact input family/version/hash/profile;
- validates input before/during allocation;
- uses source-family-specific strict parsing;
- converts to the accepted normalized production contract;
- emits deterministic output plus provenance/license manifest;
- uses original/synthetic/approved fixtures only;
- never logs user paths/private/proprietary bytes;
- rejects unknown/ambiguous versions and trailing data;
- has fuzz/property/minimized-regression tests;
- has no renderer/UI/audio/network dependency;
- does not grant or infer rights.

### Candidate importer families

#### Project-original source importer

Preferred first production-capable path if project-created source becomes available. Defines a simple documented source format and can provide fully committable tests/evidence.

#### Canary/Oteryn producer asset importer

Only after an exact project-owned producer contract and rights decision. Maps exact producer appearance/resource metadata to the normalized pack while preserving profile/build compatibility.

#### User-owned local legacy/official client importer

Only after explicit owner/legal approval. It must be local-only, recognize exact source versions/hashes, avoid bundled/downloaded proprietary bytes and prevent generated output redistribution by default.

#### Permissively licensed third-party importers

One task per asset family/license/source format. Attribution/notice and transformation obligations are included in the generated manifest/release process.

#### Fonts/audio

Separate format/decoder/security/license decisions. A generic image importer does not establish safe font/audio handling.

## 9. Phase F — authenticated acquisition and update

This belongs to launcher/update ownership, consuming the merged asset contract.

Required sequence:

```text
select release/channel/profile
-> fetch authenticated manifest
-> validate compatibility and rollback policy
-> download to bounded staging
-> verify size/hash/signature
-> parse/validate pack before activation
-> atomic activation with health marker
-> retain known-good rollback
-> runtime opens explicit activated generation
```

Required controls:

- exact manifest/asset URL binding;
- redirect/TLS policy;
- downgrade/replay/rollback protection;
- disk-space and permission handling;
- interrupted download/resume policy;
- archive traversal/symlink/special-file defenses where archives are used;
- no activation before complete verification;
- no automatic deletion of the only known-good generation;
- key rotation/revocation and incident procedure;
- provenance/notices distributed with the exact content;
- privacy-safe diagnostics.

Legacy PR #97 may inform digest-to-selected-release binding and pre-extraction verification, but no legacy Lua path becomes a Rust runtime/launcher dependency.

## 10. Pack/cache lifecycle

Candidate lifecycle:

```text
Absent
Staged(untrusted)
Verified(candidate generation)
Activated(current generation)
Draining(previous handles)
RetainedRollback
Removed
Rejected(reason)
```

Rules:

- staged bytes are never runtime-visible;
- activation publishes one immutable generation atomically;
- old handles cannot resolve into replacement bytes;
- in-flight decode/upload results carry the original pack generation and are dropped when stale;
- renderer/audio caches use logical/generation identity;
- rollback activates a previously verified exact generation;
- cache cleanup is bounded and cannot remove active/required/rollback content;
- source/import caches and runtime packs are distinct.

## 11. Cache and resource budgets

P0 does not set byte budgets. Later tasks define configurable budgets from PR #144 performance scenes and approved production data:

- pack/index mapping/metadata;
- encoded source records;
- CPU decoded images/audio/text resources;
- GPU texture/buffer/glyph resources;
- streaming buffers;
- transient decode/upload arenas;
- staging/download/rollback disk generations.

Every budget has:

- owner and metric;
- soft pressure signal;
- eviction/prioritization policy;
- hard bound/failure action;
- observability;
- no frame-thread blocking cleanup;
- deterministic test and soak evidence.

## 12. Threat-model validation by phase

### Acquisition/import

- malicious path/archive/reparse/link;
- source substitution/TOCTOU;
- malformed counts/offsets/strings;
- decoder/decompression bomb;
- unsupported/mixed version;
- provenance/license omission;
- private/proprietary leakage;
- interrupted output.

### Pack/runtime

- signature/hash/schema/profile mismatch;
- malformed index/range/overlap/trailing data;
- cache poisoning/downgrade;
- stale generation and partial activation;
- memory/disk/resource exhaustion;
- arbitrary source path/error leakage;
- unsupported required resource.

### Renderer/UI/audio

- stale device/resource handles;
- upload/voice/glyph queue growth;
- oversized dimensions/sample counts;
- device loss during preparation/activation;
- frame/audio callback blocking;
- fallback hiding compatibility failure.

Every external parser receives fuzzing or an equivalent corpus strategy before M6.

## 13. Proposed bounded package sequence

Subject to P0 aggregation evidence:

1. `ASSET-PACK-CONTRACT` — production schema, logical IDs/handles, manifest/auth/versioning decision;
2. `ASSET-RUNTIME-OPEN` — immutable open/verify/index/lookup and generation lifecycle;
3. `ASSET-APPEARANCE-CONTRACT` — exact normalized visual metadata after PR #140;
4. `ASSET-DECODE` — bounded worker decode/cache contract;
5. `RENDERER-RESOURCE` — texture/resource handles/upload/cache/device-loss;
6. `TEXT-RESOURCE` — shaping/font/glyph contract after UI and rights decisions;
7. `AUDIO-RESOURCE` — decode/stream resource contract after audio/rights decisions;
8. first approved source-family importer;
9. launcher acquisition/signing/activation/rollback integration;
10. further exact-profile importers and streaming optimization.

Packages 3, 6 and 7 may be separate producers; aggregation must avoid one mega-crate.

## 14. Merge and lease order

Shared paths such as root Cargo/lockfile, architecture categories, `apps/client/**`, build matrix and programme capability matrix require one integration lease.

Preferred flow:

```text
producer design/contract
-> focused validator
-> producer implementation + synthetic tests
-> exact Windows/supply-chain gate
-> merge/archive
-> consumer restack
-> consumer component/runtime evidence
```

No worker manually merges lockfile fragments or creates a private public-contract substitute while waiting.

## 15. Evidence required before M2

M2 asset readiness requires:

- approved source/local-import/redistribution decision;
- exact profile/version appearance requirements from PR #140;
- release-required visual workflow set from PR #141;
- accepted production pack/logical handle contract;
- runtime open/verify/index/lookup implementation;
- one approved importer or project-original source path;
- deterministic verified pack for a legal minimum-world scene;
- bounded decode and renderer resource integration;
- named Windows/GPU visible-scene evidence;
- corrupt/missing/incompatible pack negative and recovery path;
- provenance/notices and no arbitrary loose runtime source access.

Until then, current synthetic schema/compiler remains test infrastructure only.

## 16. Decisions blocked on other P0 lanes

| Input | Needed from |
|---|---|
| exact appearance/item/effect/projectile metadata and profile gates | PR #140 Canary inventory |
| release-required user workflows/resources | PR #141 legacy parity inventory |
| UI/text/font/icon and audio resource requirements | PR #143 UX inventory |
| scene/load/cache/performance and packaging/update acceptance | PR #144 release reports |
| production source/local-import/redistribution approval | owner/legal decision using rights matrix |

## 17. P0 boundary

This roadmap authorizes no production schema change, crate, dependency, importer, asset byte, remote download, key/signature, pack activation or rights claim.
