# Source and rights matrix

Evidence base: `blakinio/otclient@a6c8d1cfcac9364612c2ac56a9dc12618581adc9`.

This matrix records current evidence, not legal advice. An owner/legal review can strengthen or change a row through a later task; missing permission remains blocked.

## Required records for every distributable source

```yaml
source_id: <stable internal label>
asset_family: sprite | appearance_metadata | ui_image | font | sound | shader | localization | other
origin_owner: <person or organization>
origin_reference: <public project/release/contract reference; no private path>
source_version: <immutable version or commit>
license_id: <SPDX identifier or reviewed custom-license label>
license_text_reference: <repository path or approved public reference>
redistribution_scope: source | transformed | binary_pack | none
modification_permission: allowed | restricted | unknown
attribution_required: true | false | unknown
commercial_use: allowed | restricted | unknown
compatibility_scope: <product/protocol/asset-set scope>
input_sha256: <digest of reviewed input>
transform_tool: <tool name and version>
transform_recipe: <stable recipe identifier>
output_sha256: <digest of transformed output>
review_status: approved | blocked | prohibited
review_owner: <named role/task>
reviewed_at: <date>
notes: <non-secret bounded notes>
```

A URL, repository name, archive filename or presence inside an installed client is not a license record.

## Source classes

| Source class | Current disposition | Distribution/use rule | Evidence and blockers |
|---|---|---|---|
| original Oteryn-owned synthetic or production content | `SUPPORTED` | allowed only after ownership, contributor grant and explicit product license are recorded | accepted pipeline names this class; this task does not establish an Oteryn content license policy |
| original test fixtures created in this repository | `PROVEN` safe for planned synthetic slice | commit only purpose-built, non-derivative shapes/metadata/audio samples with documented generation recipe | repository MIT covers the authored software/docs; fixture provenance must still state original authorship and intended license |
| independently licensed third-party content | `SUPPORTED` case-by-case | require exact version, license text, redistribution/transformation scope, attribution and resulting hash | no blanket allowlist exists for fonts, sounds, images or shaders |
| permissively licensed code-generated primitives | `SUPPORTED` | acceptable when generation code and output license are compatible and no protected source material is embedded | example: simple geometric/color test images generated from numeric recipes |
| user-provided local compatibility assets | `BLOCKED` product policy | may be read locally only by a future approved importer; never uploaded, committed, repackaged or silently included in releases | legal/product decision, consent UX, safe path policy, source deletion/lifetime and non-redistribution proof missing |
| maintained legacy repository source code/docs | `PROVEN` software evidence | behavior and importer conventions may be reviewed; Rust runtime must not depend on legacy code | root MIT applies to named software/docs; separate embedded content still requires its own rights record |
| legacy `data/`, installed game files or downloaded release archives | `BLOCKED`/`PROHIBITED` as Rust distributable inputs | technical presence does not authorize copying into Rust fixtures, packs or releases | PR #37 and legacy installer preserve strict download hashes/paths but do not create redistribution rights |
| official Tibia/CipSoft client package or extracted files | `PROHIBITED` for repository/release absent explicit grant | no bytes, decoded images/audio, metadata dumps or derivative fixtures may be committed | PR #48 explicitly retains installed bytes only on isolated NAS and uploads no artifacts; no grant reviewed |
| packet captures containing appearance/content payloads | `BLOCKED` | require both protocol provenance and content/privacy review; prefer synthetic producer fixtures | may include identifiers, private data or proprietary content; no approved corpus exists |
| screenshots, marketing images or web-downloaded artwork | `PROHIBITED` by default | require explicit asset-specific license and provenance before use | public visibility is not redistribution permission |
| operating-system fonts/icons | `BLOCKED` for redistribution | may be referenced through platform APIs only when product design permits; do not bundle without license review | Windows installation availability does not imply redistributable font/icon files |
| open-source fonts | `SUPPORTED` case-by-case | pin exact font version and license; verify embedding/modification/attribution and font-file hashes | no specific font selected in this task |
| first-party reviewed shader source | `SUPPORTED` | source and generated binaries require provenance, toolchain version and deterministic recipe | server/extension-provided native shaders remain prohibited by architecture |
| localization strings authored for Oteryn | `SUPPORTED` | require ownership/contributor policy and stable locale/source version | no production localization corpus selected here |

## Asset-family status

| Asset family | Needed eventually | Current safe input | Current blocked input/fact | First evidence action |
|---|---|---|---|---|
| world sprites/textures | yes | original synthetic RGBA tiles and geometric patterns | official sprite pixels, exact atlas statistics and animation semantics | synthetic texture-grid slice only |
| appearance/type metadata | yes | original synthetic records with invented IDs/flags | official Current definitions, item/creature semantics and identifier mapping | use tiny invented schema local to synthetic tool task; do not call it Canary-compatible |
| UI images/icons | yes | generated geometric icons or separately licensed originals | existing third-party/official images without per-file rights | create four original test icons if UI/compiler testing needs them |
| fonts | yes | no bundled font required for first slice; synthetic metric fixtures may be metadata-only | exact production font choice and redistribution/embedding rights | separate font-selection/legal task |
| sounds | later | generated short waveforms/noise under original recipe | official sound files, voice/music and exact production formats | defer from first slice |
| shaders | yes | minimal first-party test shader in owning renderer task | downloaded/server-provided shader material | record compiler/tool version when selected |
| localization | yes | small original synthetic key/value fixture | legacy/official text corpus if rights/provenance are unclear | separate localization contract task |
| compatibility maps | yes for Canary adapter | metadata-only mapping against invented synthetic IDs | official ID tables or dumps without approved source | wait for exact legally usable producer evidence |

## Repository-license boundary

The root `LICENSE` states that **OTClient software and associated documentation** are available under MIT. Safe conclusions:

- repository-authored code and documentation covered by that notice can be reused under its terms;
- an independently authored synthetic fixture can be intentionally licensed and recorded;
- the notice does not automatically relicense every byte that may be downloaded, installed, referenced or historically stored by the application;
- every asset family still needs an asset-specific provenance record.

## Review outcomes

A future source review produces exactly one outcome:

- `approved`: exact source/version/license/rights/hash are sufficient for stated transformation and distribution;
- `blocked`: required evidence or decision is missing; no byte enters committed fixtures or release tooling inputs;
- `prohibited`: evidence shows the intended use is outside granted rights or repository policy.

“Probably allowed”, “available online”, “already used by OTClient” and “user owns the game” are not valid approval states.
