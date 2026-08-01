# P0 Asset Source and Rights Matrix

Status cut: `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Lane: `OTC2-20260801-playability-p0-assets` / PR #142  
Production source selected: **no**  
Implementation authorized: **false**

## 1. Purpose

Separate technical availability from provenance, local-use permission and redistribution permission for every candidate source of sprites, appearances, UI resources, fonts and audio needed by M2-M6.

A technically readable format is not a legal source. A locally owned copy is not automatically redistributable. A server download path is not automatically trusted or licensed. No source becomes production-approved without an exact owner/legal decision and reproducible evidence.

## 2. Current Rust asset baseline

### Proven

`oteryn-asset-types` currently owns one original synthetic schema-v1 contract:

- non-zero `AssetId`;
- closed `Blob` and raw tightly packed `Rgba8 { width, height }` kinds;
- bounded logical name, license and provenance text;
- SHA-256 payload digest;
- deterministic canonical record order;
- strict decode with record/payload/pack/dimension limits;
- rejection of duplicate/non-canonical IDs, malformed/trailing/unsupported input and digest mismatch.

`oteryn-asset-compiler` currently owns one offline constrained JSON compiler:

- strict schema and exact key sets;
- bounded manifest and source sizes;
- normalized relative paths only;
- no backslash, drive prefix, absolute, empty, `.` or `..` components;
- each directory component and final source opened without following symlinks;
- source type, size and bytes obtained from the same accepted file handle;
- final output must not exist;
- same-directory temporary output and final commit only after complete validation;
- stable errors containing no source-machine path.

### Not proven/absent

- no runtime pack open/mount/index/lookup crate;
- no authenticated/signature manifest;
- no production importer;
- no Canary appearance/sprite/font/audio schema;
- no compression, atlas/array preparation or streaming format;
- no renderer/UI/audio logical resource handles;
- no cache/eviction/update/rollback integration;
- no approved production asset source or redistribution contract;
- no current performance or product limits beyond synthetic schema-v1 bounds.

Schema-v1 is a safe synthetic foundation, not a claim that production content fits `Blob`/raw `Rgba8` or may be redistributed.

## 3. Decision vocabulary

For each source category record independently:

- **Technical availability:** source can be obtained and parsed in an approved environment.
- **Provenance:** origin/version/hash/author/license evidence is sufficient and auditable.
- **Local import:** the project may permit a user/operator to transform a lawfully held local copy for that user/environment.
- **Redistribution:** the project may ship original or transformed bytes to other users.
- **Update binding:** exact producer/version/profile relationship is known.
- **Production approval:** product/legal/security owners accepted the source and process.

Allowed status values:

- `PROVEN` — exact evidence and decision exist;
- `CANDIDATE` — technically plausible; decision/evidence incomplete;
- `OWNER_DECISION` — cannot be resolved by engineering alone;
- `PROHIBITED` — may not enter the selected workflow;
- `UNKNOWN` — evidence unavailable;
- `NOT_APPLICABLE`.

## 4. Source and rights matrix

| Source category | Technical availability | Provenance | Local import | Redistribution | Update binding | Current decision |
|---|---|---|---|---|---|---|
| original project-created synthetic fixtures | PROVEN for current schema/compiler | PROVEN when generator/source/license is committed | PROVEN | PROVEN under project-selected license | fixture/schema revision | approved for tests and examples only |
| original project-created production artwork/audio/fonts | UNKNOWN/ABSENT | requires creator/license records | candidate after creation | candidate after explicit assignment/license | project pack/release | preferred production-safe path if funded/created |
| permissively licensed third-party content | CANDIDATE | exact upstream revision, license text and attribution required | depends on license | depends on license and transformation terms | exact upstream/version/hash | owner/legal review per asset family |
| reciprocal/copyleft content | CANDIDATE | exact license and source obligations required | depends on license | potentially incompatible with product distribution model | exact upstream/version/hash | OWNER_DECISION; no assumption |
| system fonts/icons/audio APIs | platform-dependent candidate | OS/vendor terms and supported-use evidence required | normally runtime reference only | bundling usually separate | Windows build/component | OWNER_DECISION; do not copy system files by assumption |
| user-owned local game-client import | technically plausible, importer absent | user attests/source identified; project does not gain rights | OWNER_DECISION by jurisdiction/product policy | normally PROHIBITED unless separate rights exist | exact source client/version/hash | possible local-only path, not accepted yet |
| project-owned Oteryn server-provided content | protocol/download contract absent | producer repository, release and rights record required | CANDIDATE | OWNER_DECISION | exact server/profile/pack revision | preferred when producer and rights are project-owned |
| approved CDN/release asset download | transport/integrity pattern exists only in legacy PR #97 | source/release/hash/license must be exact | depends on source | depends on source | release asset URL + digest + profile | no Rust contract; legacy evidence only |
| official/proprietary Tibia client assets | technically readable by legacy ecosystem | copyright/proprietary origin known; redistribution rights not established | OWNER_DECISION for user-owned local use only | PROHIBITED without explicit rights | exact official version/hash | must not be committed or redistributed by default |
| private captures/extracted runtime bytes | technically possible | provenance/privacy often insufficient | restricted evidence only | PROHIBITED | exact controlled source | artifact-only; reduce to sanitized facts/fixtures |
| community/fan packs of unclear origin | CANDIDATE/UNKNOWN | UNKNOWN or mixed | UNKNOWN | PROHIBITED until proven | often unstable | reject by default |
| runtime-generated caches/atlases | derived from approved source only | inherits source plus deterministic tool record | NOT_APPLICABLE | inherits source terms | compiler/pack/input hashes | never upgrades underlying rights |
| AI-generated or procedurally generated material | technically possible | generator/model/input/license and human rights review required | OWNER_DECISION | OWNER_DECISION | generation recipe/model/version | not accepted by assumption |

## 5. Required provenance record

Every committable or distributable asset family requires:

```text
logical asset family and owner
original creator/publisher/source URL or repository
exact source revision/release/version
original file/archive hashes
license identifier and complete license/notice location
attribution and source-offer obligations
territories/use/derivative/redistribution restrictions if applicable
approval decision, approver and date
importer/tool version and configuration
normalized output pack identity/hash
server/profile compatibility range
supersession/revocation procedure
```

A manifest string such as `license: "unknown"` or an unverified URL is not sufficient provenance.

## 6. Local import boundary

A future local-import option, if owner/legal approval permits it, must enforce:

- the user supplies or selects a lawfully held source locally;
- the project does not download proprietary source on the user's behalf unless separately authorized;
- input version/hash is recognized or fails closed;
- conversion is offline and deterministic;
- source paths and raw bytes never enter diagnostics/telemetry/Git;
- output is stored in a user-local bounded area;
- output cannot be silently uploaded or redistributed;
- importer clearly states that technical support does not grant rights;
- unsupported/mixed/tampered inputs fail with a safe action;
- generated pack metadata records only non-sensitive source identity/hash and tool revision;
- deletion/repair/re-import behavior is explicit.

Local import and redistribution are separate product/legal decisions.

## 7. Server-provided/downloaded boundary

A future approved server/CDN flow requires:

- authenticated/versioned manifest from an approved producer;
- exact profile/release/channel compatibility;
- immutable URL/object identity or authenticated content addressing;
- size/count/compression bounds before allocation/extraction;
- digest/signature verification before activation;
- TLS and redirect policy;
- staging download separated from active packs;
- atomic activation and rollback;
- license/provenance metadata bound to the exact pack;
- cache poisoning and downgrade protection;
- no arbitrary server-controlled filesystem path;
- no asset delivery before the rights/redistribution decision.

Legacy PR #97 demonstrates a useful integrity rule—bind a configured digest to the exact selected release asset and verify bytes before extraction—but it is an open legacy Lua workflow, uses a third-party release source, and is not a Rust runtime, launcher, rights or production-source contract.

## 8. Production resource requirements

The exact schema is pending PR #140/#141 and later producer decisions. M2-M5 likely require at least:

### Appearance/world visual

- stable logical appearance/type IDs separated from session entity IDs;
- sprite/texture page references;
- animation phases, durations and loop policy;
- object dimensions, layers/patterns and frame groups;
- origin/offset/elevation/displacement;
- transparency/mask/blend classification;
- outfit/addon/mount/palette or equivalent normalized variants;
- item/creature/effect/projectile classifications;
- optional lighting/emission metadata;
- exact profile/version/capability gates.

### UI/text

- logical UI image/icon/theme resources;
- scalable/nine-slice/vector candidates where owned;
- cursor resources;
- fonts with shaping/coverage/fallback/license metadata;
- glyph/rasterization parameters separated from source font bytes;
- localization resource identities;
- accessibility descriptions not encoded only in images.

### Audio

- logical sound/event IDs;
- category, priority and positional/UI classification;
- sample format/rate/channels or normalized decode metadata;
- streaming versus resident policy;
- loop/trim/gain metadata;
- source/license/provenance;
- exact feature/profile relationship.

### Pack/update

- schema/profile/build version;
- content and manifest hashes/signatures;
- dependencies between packs/resource families;
- size/resource-budget metadata;
- compatibility range and rollback identity;
- provenance/notice index;
- deterministic canonical index/lookup.

These are requirements for discovery/contract design, not authorization to encode official formats or content.

## 9. Threat and failure matrix

| Threat/failure | Required control |
|---|---|
| traversal/absolute/drive/alternate separator | normalized relative logical paths or no source paths at runtime |
| symlink/junction/reparse/hard-link substitution | capability/open-handle validation appropriate to platform and acquisition model |
| TOCTOU after validation | type/size/read from the same accepted handle; authenticated final pack identity |
| oversized counts/offsets/dimensions | checked arithmetic and pre-allocation limits |
| compression/image/decode bomb | compressed and decoded size/ratio/time/memory budgets |
| malformed/truncated/trailing/duplicate entries | strict canonical parser and negative corpus |
| digest/signature/version mismatch | fail closed before activation/use |
| cache poisoning/downgrade | authenticated manifest/channel/version and atomic activation |
| partial/interrupted output | staging temporary output plus atomic commit/rollback |
| source/output aliasing or overwrite | distinct validated outputs; no overwrite without explicit transactional policy |
| unsupported source version | stable incompatibility action; no heuristic permissive parse |
| license/provenance omission | build/release gate failure for distributable packs |
| proprietary/private bytes in logs/artifacts | redaction/classification; raw evidence restricted outside Git |
| GPU/CPU resource exhaustion | decoded/upload/cache budgets and bounded eviction/failure |
| hostile text/font/audio metadata | bounded validation, safe shaping/decoder isolation and fuzzing |
| server/client profile drift | exact compatibility manifest and capability negotiation |

## 10. Fixture policy

### Committable

- original tiny generated Blob/RGBA8 records;
- project-created images/audio/font-like metadata specifically licensed for tests;
- minimized malformed byte strings created from the original schema;
- metadata-only compatibility/provenance examples;
- hashes and sanitized facts from controlled sources where bytes are not needed.

### Restricted artifact-only

- approved private producer captures;
- licensed evaluation packages not redistributable in Git;
- decoder traces and minimized facts derived under approved process;
- installer/import rehearsals containing source-user paths or proprietary bytes.

### Prohibited

- credentials/private user data;
- proprietary official assets without explicit rights;
- copied community packs of unknown origin;
- anti-cheat or official-service automation material;
- fixtures whose origin/license cannot be explained.

## 11. Required owner decisions

| Decision | Required before |
|---|---|
| original production content budget/ownership model | production art/audio/font acquisition |
| local user-owned import policy and jurisdictions | local importer implementation |
| server-provided/downloaded pack rights and producer | remote acquisition implementation |
| redistribution and attribution policy per third-party family | packaging/release |
| approved profile/version source for appearances | M2 importer/runtime integration |
| telemetry/support handling of source identity and failures | M4 diagnostics/support |
| signing keys, pack/channel trust and revocation | M4/M6 update/release |

## 12. P0 result

The only currently approved content source is original/project-created synthetic test material under the existing bounded schema. All production source categories remain `UNKNOWN`, `CANDIDATE`, `OWNER_DECISION` or `PROHIBITED` as specified above.
