# Asset Input and Provenance Evidence Agent Prompt

Use after the common prefix in `WORKER_AGENT_BASE.md`.

```text
Lane: W1-AR
Workstream: WS-R09 evidence preparation only
Task type: documentation/research; no pack/importer implementation

Goal:

Prepare legally and technically safe evidence for the first synthetic asset package and future Canary-compatible import work without committing real/proprietary game content or freezing an unsupported binary pack schema.

Expected owned paths, subject to live overlap check:

- oteryn-client/docs/research/asset-inputs/README.md
- oteryn-client/docs/research/asset-inputs/SOURCE_AND_RIGHTS_MATRIX.md
- oteryn-client/docs/research/asset-inputs/NON_CONTENT_INVENTORY_SCHEMA.md
- oteryn-client/docs/research/asset-inputs/IMPORTER_THREAT_CHECKLIST.md
- oteryn-client/docs/research/asset-inputs/SYNTHETIC_SLICE_RECOMMENDATION.md
- one active task record

Forbidden paths:

- oteryn-client/assets/**
- oteryn-client/crates/asset-*/**
- oteryn-client/tools/asset-compiler/**
- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml
- .github/workflows/**
- data/things/**, data/sounds/** and other real legacy asset roots
- external repository writes

Required evidence sources:

- accepted `ASSET_PIPELINE.md` and foundation audit asset/licensing report;
- current maintained-client installer/runtime documentation and source, read-only evidence only;
- repository licensing/governance rules;
- current primary documentation for candidate source formats or compression only when needed to explain risks;
- no private archives, signed URLs, credentials or personal local asset paths.

Deliverables:

1. README.md
   - exact evidence revisions and date;
   - evidence labels;
   - clear distinction among original Oteryn assets, independently licensed inputs, user-local imports and prohibited content;
   - one bounded later WS-R09 recommendation.

2. SOURCE_AND_RIGHTS_MATRIX.md
   - asset classes: sprites/type metadata, UI, fonts, audio, shaders, localization and test fixtures;
   - possible source/delivery models;
   - rights/provenance evidence required before commit, redistribution, install-time download or local import;
   - explicit prohibited-material list;
   - no legal conclusion beyond available evidence.

3. NON_CONTENT_INVENTORY_SCHEMA.md
   - machine-readable metadata fields that can be collected without storing protected bytes;
   - counts, dimensions, frame groups, animation timing ranges, transparency/color-space properties, estimated decoded/compressed sizes, ID ranges and source version;
   - privacy/provenance fields;
   - bounded collection and validation requirements;
   - do not include actual protected identifiers or content when rights are unclear.

4. IMPORTER_THREAT_CHECKLIST.md
   - checked offsets/counts/arithmetic;
   - archive traversal/symlink handling;
   - decompression ratio/output limits;
   - image/audio dimension and memory limits;
   - deterministic ordering/output;
   - cancellation and error taxonomy;
   - no script execution;
   - fuzz entry points and synthetic corrupt corpus;
   - source path/secret redaction.

5. SYNTHETIC_SLICE_RECOMMENDATION.md
   - one smallest synthetic asset-types/compiler package;
   - original/generated fixture set only;
   - observable deterministic output and security negatives;
   - exact non-goals;
   - unresolved choices that must not be frozen yet, including atlas/texture-array layout, production compression, signing envelope and real compatibility mappings.

Rules:

- technical downloadability is not redistribution permission;
- do not download or inspect private/proprietary bytes unless an explicit approved environment and task authorizes it;
- do not commit hashes or URLs that reveal private distribution sources;
- do not select a final pack format, texture strategy or memory budget without measured statistics;
- do not add fonts/audio/images merely as convenient fixtures; use original generated metadata and record any open-license fixture separately;
- do not edit accepted architecture unless a separate ADR task is required;
- do not implement the later synthetic package in this research PR.

Acceptance:

- source/right categories and unknowns are explicit;
- prohibited inputs are unambiguous;
- non-content inventory can support later measured renderer/pack decisions;
- importer threat model is actionable and bounded;
- synthetic recommendation needs no proprietary bytes or production contract;
- changed files are limited to the isolated research path and task lifecycle;
- documentation and repository required checks pass on exact head;
- task merges and archives independently.

Final handoff:

Recommend exactly one future WS-R09 synthetic package with owned paths, acceptance tests and non-goals. Do not implement it in this PR.
```
