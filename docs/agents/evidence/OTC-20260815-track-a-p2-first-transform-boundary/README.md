# Track A P2 first-transform boundary — Draft evidence root

Task: `OTC-20260815-track-a-p2-first-transform-boundary`  
Track: `official-client-re`  
Subject: official native Linux Tibia client only  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

This directory is **DRAFT / NOT PROMOTED** research evidence.

## Result

`SERIALIZATION_ONLY_PROVEN`

Exact-build static reproduction proves a concrete serialization boundary on the coordinator-accepted branch:

```text
TProtocolClientMessageProcessor
  -> retained intermediate (AP 0x2f69e30, RTTI 0x3080748)
  -> retained TProtocolWriter (AP 0x2f69dd0, RTTI 0x3080728)
  -> QDataStream serialization
```

The first two intermediate slots are lifecycle-like. The first concrete non-lifecycle slot is `0xc10960` (`+0x10`), which uses the retained writer member at `+0x18`, consumes a message-derived value, and invokes `QDataStream::operator<<(signed char)`. The next slot `0xc20290` serializes structured argument fields through `QDataStream::operator<<(signed short)`.

Adjacent slot `0xc20c70` constructs `QBuffer`, but its temporal position relative to the proven serializer calls is `UNKNOWN`.

## Exact provenance

- workflow run `31893080162`
- job `95032159933`
- exact head `f471bfc0b67046bdd917ea6e10a2e22af7f8d00f`
- runner `synology-otclient-01`
- artifact `9249061176`
- digest `sha256:2604ddaddd7381de0797ccfdc1c027ac49f66175485012647a4804a98e100130`
- exact client SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- exact client size `51965216`

See:

- `RESULT.json` — machine-readable result and provenance;
- `STATUS.json` — compact current classification;
- `20260815-first-serialization-boundary.md` — evidence report and promotion boundary.

## Explicit UNKNOWN boundary

This result does **not** establish:

- temporal first operation in the entire outbound pipeline;
- framing/sequence/compression/encryption order;
- final binary egress or socket ownership;
- causal local harness;
- direct DualConnection writer ownership.

Pinned coordinator evidence is revalidated by the reproducer rather than inherited as an assumption. Exact-binary reproduction overrides pinned snapshots if they ever conflict.

## Forbidden proof shortcuts

Not used as proof:

- generic QIODevice enumeration;
- generic Qt/QMeta census;
- vtable adjacency alone;
- final-socket run `31825417040`;
- superseded `0xb5b880`, `0xb46bd0`, `0xc33259` sinks;
- stale writer RTTI `0x3080700`.

No proprietary client bytes, credentials, account state, private chat or secret-bearing payloads are committed here.
