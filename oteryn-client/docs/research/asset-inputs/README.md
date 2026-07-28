# Asset input and provenance evidence

Status: evidence package for future WS-R09 implementation. It defines no accepted pack format, importer API or runtime schema and contains no asset bytes.

Evidence base: `blakinio/otclient@a6c8d1cfcac9364612c2ac56a9dc12618581adc9`.

## Evidence labels

- `PROVEN`: accepted repository architecture, security policy, license text or source directly supports the statement.
- `SUPPORTED`: evidence supports a direction, but legal approval, samples or implementation proof are still missing.
- `INFERRED`: a proposed safe operating choice, not an accepted product contract.
- `UNKNOWN`: reviewed evidence does not determine the fact.
- `BLOCKED`: work cannot proceed safely without rights, sample, contract or environment evidence.
- `PROHIBITED`: the source/content must not enter the repository or release under current evidence.

## Executive findings

1. `PROVEN` runtime assets must pass provenance/license review, normalization, validation and cryptographic release verification; legacy formats are build-tool inputs only. Source: `docs/architecture/ASSET_PIPELINE.md`.
2. `PROVEN` the root MIT license grants rights to the named OTClient software and associated documentation. It does not establish ownership or redistribution permission for unrelated Tibia/CipSoft game content, third-party fonts, sounds or artwork.
3. `BLOCKED` complete redistribution rights for required game sprites, appearances/type metadata, sounds, fonts and other proprietary client content.
4. `BLOCKED` the exact official Current/15.25 source schema and complete size/count/dimension statistics because no legally approved representative sample is available in this task.
5. `SUPPORTED` user-supplied local compatibility assets may be a product option only after legal/product policy, safe importer design, private-path handling and non-redistribution behavior are approved.
6. `PROVEN` synthetic original assets and metadata are safe inputs for the first compiler/pack slice when their provenance and license are explicit.
7. `REJECTED` treating the maintained legacy client's downloaded/existing assets, PR #37 release archives or PR #48 locally installed official package as automatically reusable Rust release inputs. Those paths provide technical evidence only and no new redistribution grant.

## Package contents

- [`SOURCE_AND_RIGHTS_MATRIX.md`](SOURCE_AND_RIGHTS_MATRIX.md): source classes, required records and current legal disposition.
- [`NON_CONTENT_INVENTORY_SCHEMA.md`](NON_CONTENT_INVENTORY_SCHEMA.md): content-free schema for counts, dimensions, formats, hashes and compatibility metadata.
- [`IMPORTER_THREAT_CHECKLIST.md`](IMPORTER_THREAT_CHECKLIST.md): fail-closed controls for hostile files, archives, parsers and workers.
- [`SYNTHETIC_SLICE_RECOMMENDATION.md`](SYNTHETIC_SLICE_RECOMMENDATION.md): one small original-data package for the next WS-R09 implementation task.

## Durable rules

- Technical accessibility is not redistribution permission.
- Every distributable input records origin, version, license, transformation and resulting hash.
- User/private absolute paths are never durable inventory data; use source-local labels and stable digests.
- Unknown rights, format semantics or compatibility remain blocked, not inferred from filenames or legacy behavior.
- No importer copies source bytes into diagnostics, errors or support artifacts.
- No real game asset is required to prove deterministic compiler, pack-index, corruption or path-security behavior.

## Implementation boundary

A future asset implementation task must revalidate rights and exact samples before adding a real importer. This package authorizes only the synthetic slice described here; it does not authorize official asset extraction, user-directory scanning, format reverse engineering, runtime mounting or release distribution.
