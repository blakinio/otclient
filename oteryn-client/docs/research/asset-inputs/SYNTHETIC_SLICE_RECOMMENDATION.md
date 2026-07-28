# Synthetic asset slice recommendation

## Decision

After a fresh WS-R09 implementation preflight, add one bounded synthetic asset-types/compiler slice that compiles an original 4×4 sprite sheet and a tiny invented metadata table into a deterministic **test-only normalized bundle**.

This slice must not be called Canary-compatible and must not freeze the production signed pack format.

## Exact package envelope

Suggested future task:

```text
Track: greenfield-rust
Workstream: WS-R09
Observable result: one synthetic source directory deterministically compiles into one validated normalized bundle and inventory report
Production crates/tools: at most one small asset-types crate plus one focused compiler tool when workspace/lease policy permits
Inputs: original generated fixtures only
External dependencies: standard library first; any image/serialization dependency requires fresh review
```

### Synthetic inputs

Generate from source code or committed human-readable recipes:

- one 128×128 RGBA image divided into sixteen 32×32 cells;
- cells use simple solid colors, lines, checkerboards and alpha gradients produced from numeric formulas;
- four invented logical sprite IDs;
- two invented animation records referencing those IDs;
- one invented material/category label set;
- no Tibia/Oteryn artwork, silhouettes, item names, creature names, appearance flags or legacy numeric IDs;
- no font or audio input;
- no archive input;
- no private filesystem paths.

Each fixture records original authorship, repository license intent, generation recipe and SHA-256.

### Output boundary

The tool may emit a test-only directory or file set containing:

- schema/tool version local to the prototype;
- normalized sprite records;
- validated dimensions/regions/animation durations;
- deterministic cell ordering;
- raw synthetic RGBA payload or a simple lossless representation selected by the task;
- per-record/input/output hashes;
- the content-free inventory defined by `NON_CONTENT_INVENTORY_SCHEMA.md`;
- a canonical manifest binding the prototype output.

The slice does **not** add:

- production signatures, release updater integration or runtime mount;
- official/legacy importer;
- atlas/texture-array strategy decision;
- GPU compression or renderer dependency;
- user-local source scanning;
- sprites/appearances/sounds/fonts from a game client;
- public compatibility IDs or a production pack ABI.

## Required contracts

The future task should define only what this synthetic result needs:

```text
SyntheticSpriteId        checked non-zero/in-range test ID
PixelSize                checked width/height
SourceRegion             checked x/y/width/height within image
FrameDuration            bounded non-zero duration
SyntheticAnimation       bounded ordered frame list
InputDigest/OutputDigest exact SHA-256 bytes
InventoryRecord          content-free metadata output
CompileError             closed, non-secret error categories
```

Do not introduce generic game `AppearanceId`, Canary IDs, runtime asset handles or renderer texture handles in this slice.

## Determinism acceptance

- identical inputs/config/tool revision produce byte-identical output and inventory hash;
- shuffled source enumeration produces identical output;
- changing one pixel or metadata value changes the relevant digest and aggregate output hash;
- timestamps, absolute source paths and machine/user names do not affect output;
- output ordering follows typed logical IDs and schema rules, not directory order;
- repeated runs after interrupted staging do not reuse partial output.

## Security negatives

- invalid dimensions, zero/oversized frames and out-of-range source regions;
- duplicate logical IDs and duplicate canonical labels;
- animation count/duration overflow and dangling sprite reference;
- truncated/malformed image header and decoded-size mismatch;
- oversized input and aggregate memory budget;
- source label with absolute path, `..`, drive/UNC prefix, NUL/control or excessive length;
- cancellation during parse/validation/output with staged cleanup;
- synthetic private-path/token markers absent from errors/inventory;
- deterministic output under randomized input order;
- no output promotion after any validation/hash failure.

## Validation

Required exact-head evidence:

- locked metadata, formatting, Clippy and workspace tests on Windows;
- architecture checker proving asset-types/tool dependency direction;
- cargo-deny supply-chain policy;
- deterministic golden output generated only from original synthetic fixtures;
- corrupt/bounds/path/cancellation negative tests;
- complete source/license/provenance review;
- no asset/runtime/server/GPU compatibility claim.

## Why this slice is first

It proves the highest-value independent properties before rights and official-format blockers are resolved:

- typed asset metadata;
- bounded validation;
- deterministic transformation;
- provenance/hash propagation;
- private-path-free inventory;
- cancellation and staged output cleanup;
- architecture separation between build tooling and later runtime.

It deliberately does not spend the first asset implementation task on reverse engineering, official content, renderer layout or a prematurely stable pack format.

## First action after merge

The next WS-R09 worker should recheck active Cargo/shared-path leases and whether deterministic test-support work has already merged. It then creates a bounded task for this synthetic slice only, records the exact tool/dependency choices and opens a draft PR before adding any crate or fixture.
