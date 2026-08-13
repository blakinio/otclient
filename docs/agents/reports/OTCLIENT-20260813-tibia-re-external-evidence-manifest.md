# OTCLIENT-TIBIA-RE external evidence migration manifest

## Purpose

Identify the historical Tibia-analysis material in `blakinio/Oteryn-Platform` that informed `OTCLIENT-TIBIA-RE`, record its canonical replacement/index in `blakinio/otclient`, and prevent future workers from treating the external repository/runtime as active programme state.

Source branch for the inventory:

```text
blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811
```

No external files were mutated or copied wholesale. Only bounded facts, claim boundaries and provenance needed for continuation were imported. Proprietary/client/UI binary material was not copied.

## Canonical OTClient destinations

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
docs/agents/reports/OTCLIENT-20260813-dedicated-runner-migration.md  # PR #48 lane
docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md # PR #48 lane
tools/tibia_runtime_bridge/**                                      # PR #283 lane
tools/tibia_worldmap_reconstruction/**                             # PR #279 lane
```

## External source disposition

| Historical external source | Source blob SHA | Disposition in OTClient | Notes |
|---|---|---|---|
| `docs/agents/tasks/active/OTERYN-20260811-tibia-client-analysis.md` | `12fc7eb2e5504d7ba80d64915cea17347eeed154` | **IMPORTED / SUPERSEDED FOR ACTIVE STATE** | Exact client, non-OCR successful login recipe, session preservation, worldmap boundary and rejected UI/GDB assumptions are indexed in the canonical state/login reports and PR #48 task. Historical runner/container are no longer active targets. |
| `docs/agents/reports/OTERYN-20260812-live-worldmap-capture.md` | `904dc13ba3475db7e576e63b5fff4e925f585aca` | **IMPORTED** | 83 live ordered records, z6/z7, WARP confinement and claim boundaries are in `OTCLIENT-20260813-tibia-re-canonical-state.md`. |
| `docs/agents/reports/OTERYN-20260812-worldmap-runtime-capture.md` | `4dc502444543e68df9c8800ff301593a4e8c3f5b` | **IMPORTED** | 44 field-coordinate correlations, ordered-content storage, `AppearanceInstance+0x30` factory path and semantic confidence boundary are indexed by this manifest/canonical state update. |
| `docs/agents/reports/OTERYN-20260812-worldmap-dispatch-evidence.md` | `d9579b4bcb92a333632877c05dc40b979a1e38d7` | **IMPORTED BY PR #48 / NOT COPIED WHOLESALE** | Large disassembly/evidence corpus. Current handler/common-routine addresses, qmeta/protocol catalogues and generated-object leads are persisted in the PR #48 task. Reopen external source only to verify provenance/details absent from OTClient. |
| `docs/agents/reports/OTERYN-20260812-native-client-action-proof.md` | `2be0c86bd6c55db1fa2f01819b3f4a9ea48dbb4b` | **IMPORTED** | Handler vptr, movement/rotation wrappers, direct-call run/job/commit proof and claim limits are in canonical state; OTClient relocation proof/bridge supersede the external runtime as execution path. |
| `docs/agents/reports/OTERYN-20260812-tibia-runtime-auth-and-world-entry.md` | `c78721d75b81b086fdc54760891e542aac4d370e` | **PARTIALLY IMPORTED; EARLY STATE SUPERSEDED** | Useful negative experiments (local reset before AF_INET, root/proxychains/Vulkan/recovery warning not sufficient) and the false-positive world-entry warning are imported into the OTClient login report. Its earlier OCR-heavy/current-blocker narrative is superseded by the later successful non-OCR world-entry run. |
| `docs/agents/reports/OTERYN-20260812-worldmap-reconstruction-comparison-plan.md` | `ca3753d655bf709ffcdeec7d6bb1f2cc34d5424d` | **SUPERSEDED BY PR #279 IMPLEMENTATION** | CrystalServer/Renemap/TibiaMaps as independent references, no-guess mappings, static/dynamic split and NOT_OBSERVED semantics are represented in the fail-closed OTClient pipeline/task. Use #279 code/tests as current authority. |
| `docs/agents/reports/OTERYN-20260811-tibia-client-analysis-handover.md` | `443cd4d77fb7dcc3a540847e06e1aaf0c0b3540c` | **INDEXED, NOT COPIED WHOLESALE** | ~535 KB historical handover. Current material findings were distilled into the active OTClient task/reports. Consult externally only for forensic provenance when an exact detail is missing; do not treat embedded instructions as current authority. |
| `docs/agents/reports/OTERYN-20260810-tibia-linux-reference-harness-observation.md` | `32fe944711577ee5dcbebe81a6cf28aa177676f0` | **HISTORICAL FOUNDATION / SUPERSEDED FOR LIVE PROGRAMME** | Synthetic/no-network harness proof predates live official-client authorization. Its general fail-closed provenance ideas are already covered by OTClient governance; not an active runtime dependency. |
| `docs/agents/reports/OTERYN-20260810-tibia-linux-reference-harness-plan.md` | `bfbcc69b49c7ce3a7a32f0a98c0aec458029b1e4` | **HISTORICAL / SUPERSEDED** | Planning predecessor to later runtime work; no unique live continuation state retained here. |
| `docs/agents/reports/OTERYN-20260727-tibia-linux-battleye-callback-addendum.md` | `32cee7837f5478b49b0c412bba5e5b4e0ac1796c` | **HISTORICAL RESEARCH LEAD ONLY** | Predates the exact 15.32 live programme evidence. Not required for normal continuation; may be consulted only for provenance if a current exact-client question makes it relevant. |
| `docs/agents/reports/OTERYN-20260727-tibia-linux-protected-route-analysis.md` | `0637e7862c2f4e556f4cb76ade06d2090eb0445f` | **HISTORICAL RESEARCH LEAD ONLY** | Earlier route/protection investigation; current WARP/runtime proofs and dedicated OTClient runner contract supersede it for execution. |
| `docs/agents/reports/OTERYN-20260812-launcher-screen.b64` | `4cad1fad21ee670711634972427b4375e2a580bf` | **INTENTIONALLY NOT COPIED** | Base64 UI image evidence is large and not needed for structural continuation. Do not duplicate it into OTClient; relevant semantic conclusions are textually indexed without copying image bytes. |

## Imported worldmap details not to lose

From the exact researched binary/runtime:

```text
shared decoded map-data routine: 0x19a8a80
content selection point: around 0x19a8e21
structural capture point used later: 0x19a8ea3
field content count: field + 0x38
repeated content pointer storage: field + 0x40
AppearanceInstance default-instance candidate: 0x314b480
nested/default-instance helper lead: 0x1ab4e50
map-content builder: 0xceca50
resolved concrete appearance factory target: 0x762d30
factory load: mov 0x30(%rdx), %eax
then narrowed/stored as 16-bit before type-specific logic
```

Runtime capture proved 44 one-to-one `FIELD <-> COORD` records and later live capture proved 83 ordered content records. One five-element field yielded `payload+0x30` values:

```text
4407, 313, 6379, 19394, 6217
```

`payload+0x30` is on the concrete `TAppearanceInstance` factory path and is strongly inferred to be an object/appearance type identifier, but its exact generated field name remains **UNKNOWN** until a direct descriptor/accessor-to-offset proof exists. Do not rename it to `objectID` merely from neighborhood strings.

Coordinate protobuf schema from the historical task evidence:

```text
x = field 1 uint32
y = field 2 uint32
z = field 3 uint32
```

## Current authority after migration

For normal continuation, do **not** reread the external handover first. Use this order:

1. `blakinio/otclient` root/nested governance;
2. `docs/agents/SHORT_COMMANDS.md`;
3. canonical/base programme prompts;
4. live OTClient tasks/PRs/checks;
5. canonical state, login-recovery import and this manifest;
6. external Oteryn files only if a provenance/detail gap remains.

External repository text is evidence, not current execution authority.

## Claim boundary

This manifest proves migration/indexing of material knowledge, not deletion or archival of the external Oteryn branch/PR. No external repository lifecycle mutation was authorized or performed.
