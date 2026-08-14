# Track A — network-owner vtable census

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

This experiment is a static S2 continuation of the already proven queue-to-network-owner handoff. Prior evidence proves that `TProtocolMessageQueue::clientMessageReadyToProcess` reaches the containing owner's virtual slot `+0x90`, and that the same owner setup path constructs a `QTcpSocket`. The remaining objective is to resolve the concrete owner vtable/slot function without depending on a live ptrace attach.

## Exact experiment

```yaml
workflow: .github/workflows/tibia-official-client-re-network-owner-vtable-census.yml
workflow_commit: 5980df1a5c14f5c9c6e4299cbc1b8e9d62e33e4a
run: 31811853350
job: 94804121997
result: PASS
runner: synology-otclient-01
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The census applied `R_X86_64_RELATIVE` relocations to the exact PIE image and searched non-executable PT_LOAD regions for Itanium-style vtable address points whose known owner virtual-call signature is executable at offsets `+0x4a8`, `+0x4b0`, `+0x4b8`, `+0x4c0`, `+0x4c8`, `+0x4d8`, and whose downstream `+0x90` entry is executable. Candidates were ranked by direct RIP-relative LEA references and proximity to the proven owner setup function around `0x7e7fe0`.

## Result

```text
VTABLE_SHAPE_CANDIDATE_COUNT=338
NETWORK_OWNER_VTABLE_UNIQUE=unknown
NETWORK_OWNER_SLOT_90_UNIQUE=unknown
TRACK_A_NETWORK_OWNER_VTABLE_CENSUS_COMPLETE=true
```

Representative highest-ranked candidates include:

| Address point | `+0x90` target | Direct LEA references observed by this scanner |
|---:|---:|---|
| `0x2f69168` | `0xe70460` | `0x7e7e18`, `0xc41a80` |
| `0x2f61c20` | `0x727ed0` | `0x6d02c4`, `0x7e7b9f` |
| `0x2f69380` | `0xd09ef0` | `0x7e7916` |
| `0x2f69348` | `0x727f80` | `0x7e77a7` |
| `0x3083a50` | `0xed9ba0` | includes `0x7e7516` |
| `0x2f69310` | `0x8106e0` | `0x7e74fd` |
| `0x2f692d8` | `0x810720` | `0x7e74bc` |
| `0x3083968` | `0x1757930` | includes `0x7e73ca` |
| `0x2f692a0` | `0x810760` | includes `0x7e73a4` |

These rows are candidates only. None is promoted to the transport-owner vtable or concrete `+0x90` function by this experiment.

## Classification

- **FACT:** run `31811853350` / job `94804121997` completed successfully against the exact fenced official-client SHA.
- **FACT:** the stated broad vtable-shape predicate yields `338` candidates.
- **FACT:** this experiment does not uniquely resolve either the containing network-owner vtable address point or its concrete `+0x90` target.
- **DERIVED:** executable-slot shape alone is insufficient; constructor/vptr-store provenance is required to reduce the candidate set.
- **UNKNOWN:** which candidate, if any, is the exact primary vtable address point used by the containing owner instance on the proven queue-processing path.
- **UNKNOWN:** the exact concrete function behind the live owner's `+0x90` slot and the point where `GameclientMessage` becomes framed network bytes.

## Rejected interpretation

Do not select the first or nearest candidate merely because it has a LEA reference near `0x7e7fe0`. Proximity is only a ranking heuristic; it does not prove that the candidate is stored into the containing owner's `this` vptr.

## Next action

Recover constructor/vptr provenance around the exact owner setup chain, especially the `0x7e7db0` function called at the start of `0x7e7fe0`. Identify direct `lea candidate_vtable` -> store-to-`this` patterns and intersect those proven stores with the 338-candidate set. Only after a unique or structurally proven owner vtable is established should `+0x90` be promoted and disassembled as the concrete queue-processing receiver.
