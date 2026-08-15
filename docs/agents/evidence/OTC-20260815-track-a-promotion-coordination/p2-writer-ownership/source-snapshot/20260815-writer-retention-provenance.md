# Track A P2 writer retention provenance — exact-build Draft evidence

Task: `OTC-20260815-track-a-p2-writer-ownership`  
Draft PR: `#301`  
Research head executed: `e603691ac4458efb4132e485f36538fef6a277dd`  
Workflow: `Track A P2 writer ownership provenance`  
Successful run/job: `31883231486` / `95008610322`  
Sanitized result artifact: `9246558034`  
Sanitized artifact digest: `sha256:d6a08baa10ff6fd7edf7e6e6a21dcaaa0244e2b69a9adc26417bab00a831759a`

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

The successful run consumed the previously reviewed exact-build provenance artifact from run `31828102313`, artifact id `9229609330`, and independently verified its ZIP digest before analysis:

```text
sha256:bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c
```

The source artifact itself contains the same exact client SHA fence and selected setup FDE `0x196fee0..0x1972517`.

## Result

```text
P2_WRITER_OWNERSHIP_RESULT=PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR
P2_DIRECT_DUALCONNECTION_WRITER_MEMBER=NOT_PROVEN
P2_FRAMING_ORDER=UNKNOWN
P2_TRANSFORM_BOUNDARY=UNKNOWN
P2_FINAL_BINARY_EGRESS=UNKNOWN
P2_CAUSAL_LOCAL_HARNESS=UNKNOWN
```

The result name deliberately uses `UPSTREAM` for the relative position in the already accepted outbound ownership/processing graph. The direct retention facts and graph-relative inference are separated below.

## FACT — canonical identities and outer retained fields

The reproducer requires the current canonical #299 reconciliation to identify:

```text
TProtocolWriter
  RTTI 0x3080728
  vtable address point 0x2f69dd0
  base -> TIODeviceWriter RTTI 0x3080718

outer +0xa00/+0xa08 -> TProtocolClientMessageProcessor
outer +0xa10/+0xa18 -> TGameserverNetworkPacketRawDataProcessor
outer +0xc18/+0xc20 -> TGameserverDualConnection
```

The canonical dynamic processing chain remains:

```text
TProtocolClientMessageProcessor
 -> TGameserverNetworkPacketRawDataProcessor
 -> TGameserverDualConnection
```

## FACT — `TGameserverDualConnection` is retained separately at outer `+0xc18/+0xc20`

Inside the exact setup FDE the source artifact contains the bounded construction/retention sequence around `0x1970757..0x19707bc`. It allocates/initializes the DualConnection branch and stores the object/control pair into outer `+0xc18/+0xc20`.

Later in the same FDE, code reloads outer `+0xc18` and uses that object in a separate QObject connection setup. This is a negative structural discriminator against treating the writer object created later as the same retained branch.

## FACT — a concrete `TProtocolWriter` is constructed in the same setup FDE

The exact artifact contains the bounded sequence around `0x1970d26..0x1970d7e`:

- allocate `0x28` bytes for a shared/control allocation;
- install control vptr `0x304c380`;
- load canonical `TProtocolWriter` vtable address point `0x2f69dd0` at `0x1970d63`;
- store that writer vptr at allocation `+0x10`;
- initialize following writer fields at `+0x18/+0x20`.

This is stronger than a generic writer-vtable/callsite census: the exact canonical `TProtocolWriter` address point is installed into a concrete allocated object in the network/game-session setup function.

## FACT — the writer shared pair is retained by an intermediate object

The same FDE then allocates an object of size `0x250`, installs vptr `0x2f69e30`, and stores the just-created writer object/control pair into that retained object at its object-relative `+0x8/+0x10` positions (`allocation +0x18/+0x20`).

The exact semantic class name of this intermediate `0x2f69e30` object remains `UNKNOWN`; the pointer/control retention relation itself is structural FACT.

## FACT — that retained writer branch is installed as `TProtocolClientMessageProcessor`

A subsequent `0x38`-byte shared/control allocation receives vptr `0x2f6a208`, retains the intermediate-object pair, and is stored at:

```text
0x19710a7 -> outer +0xa00
0x19710ae -> outer +0xa08
```

Current canonical #299 independently identifies outer `+0xa00/+0xa08` as `TProtocolClientMessageProcessor`.

Therefore, for this exact build:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (exact class UNKNOWN)
 -> retained shared TProtocolWriter
```

is a structural retention fact.

## INFERENCE — writer location relative to `TGameserverDualConnection`

Because canonical #299 independently establishes the processing chain:

```text
TProtocolClientMessageProcessor
 -> TGameserverNetworkPacketRawDataProcessor
 -> TGameserverDualConnection
```

and the concrete writer is retained on the `TProtocolClientMessageProcessor` branch while DualConnection is separately retained at outer `+0xc18/+0xc20`, the best current graph-relative classification is:

```text
writer_location_relative_to_dualconnection = UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH
```

This is an inference from two independently proven structural facts. It is **not** a claim that `TGameserverDualConnection` directly contains or owns the `TProtocolWriter`.

## NOT_PROVEN

- a direct `TGameserverDualConnection -> TProtocolWriter` member/reference;
- the exact intermediate object class at vptr `0x2f69e30`;
- whether the same writer instance is ultimately invoked by every gameplay action path;
- exact framing/serialization order;
- compression/encryption/sequence transformation boundary;
- final binary QIODevice/socket egress;
- a controlled causal local/custom harness.

## Negative controls

The successful run requires and preserves current canonical negative evidence:

- `0xb46bd0` is a real `TGameserverTCPConnection::QTcpSocket*` writer for QString/local-8-bit + newline, but is **DISPROVEN as binary gameplay sink evidence**;
- the old `owner+0x88 -> ... -> 0xb5b880` gameplay endpoint model remains **DISPROVEN/SUPERSEDED** and must not satisfy this gate;
- the source artifact reports `WRITER_DIRECT_CALL_COUNT=0`, preventing a generic/direct-call coincidence from becoming writer-ownership proof.

Historical `0x3084c70 -> +0xd0 -> 0xb40630` writer-family evidence remains a separate unresolved type/provenance lead. It is not equated to canonical `TProtocolWriter` vptr `0x2f69dd0` by this result.

## Repair history

First workflow run `31883167971` / job `95008465831` failed closed at `canonical_tprotocolwriter_identity` after the source artifact download and SHA verification had succeeded. The parser expected Markdown backticks around values that are actually inside a fenced code block in the canonical report. Commit `e603691ac4458efb4132e485f36538fef6a277dd` corrected only that textual matcher; no address, client fence, provenance relation or semantic gate was relaxed. Run `31883231486` then passed every structural and negative-control marker.

## Researcher disposition proposal

`ACCEPT_WITH_EDITS` for the bounded writer-retention relation above.

Do **not** mark P2 complete. The next P2 closure work is still the transformation/framing order, final binary egress and causal harness, using this writer-retention fact without reviving the superseded sink models.
