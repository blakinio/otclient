# Track A P2 post-serialization buffer boundary — Draft evidence root

Task: `OTC-20260815-track-a-p2-post-serialization-buffer-boundary`  
Track: `official-client-re`  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

This is a **DRAFT / NOT PROMOTED** research namespace.

## Starting boundary

Coordinator PR #300 has promoted only the following bounded facts from closed-unmerged source #306:

- retained intermediate AP `0x2f69e30` / RTTI `0x3080748`;
- retained TProtocolWriter AP `0x2f69dd0` / RTTI `0x3080728`;
- `0xc10960` QDataStream signed-byte serialization through retained writer state;
- `0xc20290` structured signed-short serialization;
- `0xc20c70` QBuffer construction.

The temporal/data-flow relation between serializer state and QBuffer remains `UNKNOWN`.

## Research rule

The new researcher must prove shared/split state with exact member/call/data provenance. Vtable adjacency is explicitly insufficient.

No client bytes, credentials, account state or secret payloads belong in this directory.
