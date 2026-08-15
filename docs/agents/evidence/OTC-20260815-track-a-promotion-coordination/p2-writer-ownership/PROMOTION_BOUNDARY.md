# Track A P2 writer ownership — coordinator promotion boundary

Source Draft PR: #301 (`research/OTC-20260815-track-a-p2-writer-ownership`)
Source exact final head: `50e2d95c7dc8b0759eb6233a3751f73434958e88`
Coordinator disposition: `ACCEPT_WITH_EDITS`
Final source provenance run: `31883456870` — `SUCCESS`
Final source required PR CI: `31883459362` — required jobs `SUCCESS`
Exact client: official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## FACT promoted

For this exact build, the reviewed setup FDE creates a concrete canonical `TProtocolWriter` (`RTTI 0x3080728`, vtable address point `0x2f69dd0`). Its shared object/control pair is retained through an intermediate object whose exact class remains UNKNOWN. A wrapper retaining that intermediate pair is stored at outer `+0xa00/+0xa08`, independently identified by canonical #299 as `TProtocolClientMessageProcessor`.

The same setup FDE constructs/retains `TGameserverDualConnection` separately at outer `+0xc18/+0xc20`.

Therefore the bounded structural retention fact is:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (exact class UNKNOWN)
 -> retained shared TProtocolWriter
```

## INFERENCE promoted with label

Canonical #299 independently proves the processing graph:

```text
TProtocolClientMessageProcessor
 -> TGameserverNetworkPacketRawDataProcessor
 -> TGameserverDualConnection
```

Combining that graph with the retention fact supports the graph-relative inference:

```text
writer_location_relative_to_dualconnection = UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH
```

This is not a direct-member claim.

## NOT_PROVEN / UNKNOWN retained

- direct `TGameserverDualConnection -> TProtocolWriter` member/reference: NOT_PROVEN;
- exact class identity of intermediate vptr `0x2f69e30`: UNKNOWN;
- exact gameplay framing/serialization order: UNKNOWN;
- compression/encryption/sequence transformation boundary: UNKNOWN;
- final binary QIODevice/socket egress: UNKNOWN;
- causal controlled/local harness: UNKNOWN;
- historical `0x3084c70 -> +0xd0 -> 0xb40630` relationship to canonical `TProtocolWriter`: UNKNOWN.

## Negative evidence retained

- `0xb46bd0` remains disproven as binary gameplay-sink evidence;
- old `owner+0x88 -> ... -> 0xb5b880` gameplay-endpoint model remains superseded;
- generic/direct QIODevice coincidences do not satisfy the ownership gate.

## Provenance boundary

`source-snapshot/` contains exact Git blobs from reviewed source head #301: the durable evidence report, machine-readable result, reproducer and workflow. The source workflow verifies the historical reviewed artifact ID `9229609330` by ZIP SHA-256 `bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c` and fails closed against canonical #299 identity/negative-control anchors.

This promotion improves P2 ownership provenance only. P2 remains incomplete until transformation/framing order, final binary egress and a causal local/custom harness are proven.
