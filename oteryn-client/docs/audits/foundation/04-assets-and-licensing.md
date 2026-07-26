# Assets, Formats and Licensing Audit

Evidence cut: maintained client `main` at `5568cb6f5e2fd6162c78cde304deea5d32461e05`.

## Current runtime evidence

The maintained client uses versioned final roots:

```text
data/things/<version>/
data/sounds/<version>/
bin/* runtime extras when supplied
```

For modern versions (`>= 1281`), the documented installer supports:

- release/tag source ZIP as primary installation path;
- manifest fallback;
- `assets.json.sha256` integrity metadata;
- `catalog-content.json` and `catalog-sound.json`;
- packaged `.zip` / `.rar` assets;
- optional `.lzma` decompression;
- strict SHA-256 by default;
- missing-assets prompt, cancellation and progress.

Evidence: `docs/client-assets-auto-install.md`, `modules/client_assets/**`, `modules/game_things/**`, `init.lua`.

`PROVEN` these are legacy runtime/install contracts. They are not the new Rust asset-pack design.

## Required asset classes

| Class | Required by | Audit status |
|---|---|---|
| world/item/creature sprite imagery | MPS renderer and appearances | `PROVEN` required; legal distributable source `BLOCKED` |
| appearance/type metadata, IDs and animation frames | MPS domain/renderer | `PROVEN` required; exact importer schema needs evidence |
| map/tile metadata | MPS world | `PROVEN` required; runtime map arrives via protocol, static type data remains needed |
| effect/projectile imagery | MPS | `SUPPORTED`; exact first-slice set unresolved |
| UI images/icons | MPS/Beta | `PROVEN`; must be original Oteryn-owned or independently licensed |
| fonts and shaping data | MPS/Beta | `PROVEN`; font redistribution rights unresolved per selected family |
| game/UI audio | Beta | `SUPPORTED`; source and redistribution rights unresolved |
| shaders/material definitions | MPS renderer | `PROVEN`; should be first-party reviewed source |
| localization bundles | Beta | `SUPPORTED`; language set unresolved |
| benchmark/snapshot fixtures | engineering | `PROVEN`; must use synthetic/original content |

## Source/provenance classification

### Original Oteryn-owned material

- `PROVEN` permitted in principle when ownership and contributor provenance are recorded.
- Required record: source author/organization, license, version, hash and transformation.
- Preferred for UI, shaders, logos, controls and synthetic benchmark scenes.

### Independently licensed third-party material

- `SUPPORTED` permitted only when license terms allow repository distribution and intended modification/use.
- Required record: exact license text/reference, attribution obligations, source version and resulting hash.
- Copyleft/attribution implications must be reviewed before product adoption.

### User-supplied local compatibility assets

- `INFERRED` a production importer may allow users/operators to convert legally obtained local inputs without redistributing those inputs in this repository.
- This requires a product/legal decision and a safe importer.
- The repository may contain importer code and synthetic fixtures, not proprietary source bytes.

### Existing maintained-client/download source

`init.lua` currently names `dudantas/tibia-client` as a legacy asset repository and the legacy installer handles modern official-format packages.

- `PROVEN` the legacy client can download/use those assets under its current deployment model.
- `BLOCKED` this audit found no repository-owned legal approval proving that all game sprite/sound/package bytes may be copied into the new repository or redistributed in Oteryn releases.
- `REJECTED` treating technical downloadability as redistribution permission.

### Proprietary CipSoft/Tibia content

- `PROVEN` root governance forbids committing proprietary CipSoft assets without confirmed redistribution rights.
- `REJECTED` copying `.spr`, `.dat`, catalogs, sounds, fonts, icons, client binaries or extracted images into audit/test fixtures merely because the legacy client can load them.

## Prohibited material list

Do not commit without explicit reviewed rights:

- official or extracted game sprite sheets;
- official item/creature/outfit/effect images;
- official sounds/music/voice assets;
- official fonts, logos, frames or icons;
- official DAT/SPR/PIC/catalog/binary packages;
- private server asset archives or signed URLs;
- proprietary map files/datapacks not already legally distributable;
- user credentials, private paths or download tokens embedded in manifests;
- raw private packet captures containing asset hashes or personal data when not sanitized.

## New normalized asset model

The accepted architecture requires build-time import into typed Oteryn-owned runtime packs.

Candidate logical IDs:

```text
SpriteId
AppearanceId
ItemTypeId
UiImageId
FontId
SoundId
ShaderId
MaterialId
LocalizationBundleId
```

Required normalized metadata for the first slice:

- image dimensions, format/color-space and alpha policy;
- frame groups, animation durations/loop/randomization;
- sprite origin/size/offset and layering;
- appearance composition and direction variants;
- item flags needed for rendering/interaction;
- effect/projectile frame metadata;
- source compatibility version and stable mapping;
- provenance/license reference;
- content hash and compiler schema version.

`UNKNOWN` the exact current official catalog/type schema required for 15.25 because no legally distributable input sample is committed for this audit.

## Runtime pack requirements

`PROVEN` architecture requirements:

- immutable versioned pack;
- bounded index/string/count/offset validation;
- content hashes and authenticated manifest/signature;
- client/protocol/asset compatibility metadata;
- deterministic build output;
- memory mapping/range reads where measured useful;
- worker-thread decompression/decoding;
- CPU/GPU budgets and eviction;
- atomic activation and rollback;
- no runtime use of download staging as source of truth.

Exact binary format is deliberately not selected by the foundation audit.

## Texture strategy evidence gap

- `PROVEN` architecture selects modern batching/instancing and allows atlas, texture array or hybrid storage.
- `BLOCKED` actual sprite counts, dimensions, animation density, transparency behavior and GPU format size statistics are not legally available in this audit branch.
- `REJECTED` freezing atlas page size, compression format or texture-array layer count before collecting those statistics and testing target hardware.

The asset audit for the first real importer must produce a machine-readable, non-content inventory of counts/dimensions/metadata where collection is legally permitted.

## Fonts and text

Required decisions:

- selected UI/body/monospace font families;
- redistribution and embedding permissions;
- shaping engine/script coverage;
- fallback strategy;
- glyph atlas budget;
- localization languages and expansion testing.

All remain `UNKNOWN` pending product/branding/localization selection. Synthetic tests may use a small known-open font only after its license is recorded.

## Audio

- `PROVEN` legacy runtime has versioned sounds and sound catalogs.
- `BLOCKED` redistribution permission for actual sound content.
- `INFERRED` new runtime should distinguish short decoded effects from streamed long audio and normalize category/loudness metadata in the compiler.
- Audio is outside the first render/domain vertical slice and must not block the initial workspace bootstrap.

## Importer security requirements

Every importer/parser must enforce:

- bounded file/archive size and collection counts;
- checked offsets/dimensions/arithmetic;
- path traversal and symlink rejection;
- decompression output/ratio limits;
- no embedded script execution;
- deterministic ordering/output;
- cancellation and clear failures;
- fuzzable entry points;
- no source path or secret leakage in release manifests.

## Legal evidence required before real game assets

1. identify each source repository/package and rights holder;
2. obtain explicit redistribution/modification determination for Oteryn use;
3. record license/authorization in a durable asset provenance registry;
4. define whether assets may be committed, downloaded at install time or only imported locally;
5. separate source rights from generated-pack distribution rights;
6. verify fonts/audio independently from sprites/type metadata;
7. review trademark/logo restrictions separately;
8. approve test-fixture extraction policy.

## Audit conclusion

- `PROVEN` a synthetic asset schema/pack and renderer can be developed without proprietary game content.
- `BLOCKED` a production Canary-compatible game asset pack cannot be committed or distributed until rights and source-format evidence are closed.
- `INFERRED` the safest initial sequence is synthetic pack/tooling first, followed by a separately reviewed local importer or approved distribution flow.
