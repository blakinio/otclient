# Track A P2 first-transform boundary — Draft evidence root

Task: `OTC-20260815-track-a-p2-first-transform-boundary`  
Track: `official-client-re`  
Subject: official native Linux Tibia client only  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

This directory is **DRAFT / NOT PROMOTED** research evidence.

Objective: discriminate the first concrete serialization/data-transform edge on the coordinator-accepted `TProtocolClientMessageProcessor -> retained writer` branch without duplicating final-socket run `31825417040`.

Pinned coordinator evidence dependency: PR #300 head `5e6457b5afd717e3c92bb06a7219d8246c51f3b2`. Because PR #300 is unmerged, those accepted snapshots remain a pinned dependency and must be revalidated against the exact binary/current main before any researcher conclusion is promoted.

Forbidden as proof: generic QIODevice enumeration, vtable adjacency, superseded `0xb5b880`, disproven `0xb46bd0`, disproven `0xc33259`, stale writer RTTI `0x3080700`, or workflow colour alone.

No proprietary client bytes, credentials, account state, private chat or secret-bearing payloads may be committed here.