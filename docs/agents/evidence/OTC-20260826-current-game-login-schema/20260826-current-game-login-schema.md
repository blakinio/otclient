# Current game-login protobuf schema — exact build

Date: 2026-08-27  
Task: `OTC-20260826-current-game-login-schema`  
Source Draft: PR #711  
Execution: GitHub-hosted static only; `runtime_access:none`.

## Exact client fence

Final producer run `33017207072`, job `98338388458`, source evidence head `d24b6e61d1086094112020db6e7d959c24bdb34a` completed `SUCCESS`.

```text
version           15.32.75d4a0
packed_sha256     075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked_sha256   d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked_size     52105824
artifact          9625060590
artifact_digest   sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result_json_sha   1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
```

No official-client execution, login, credentials, session capture, process-memory access or raw executable upload occurred.

## Current generated-message ABI

Exact current RTTI/vtable recovery is unique for the target classes. Behavioral comparison with control generated messages proves the current generated protobuf layout:

```text
+0x10 Clear-equivalent
+0x18 ByteSizeLong-equivalent
+0x28 _InternalSerialize-equivalent
+0x30 zero / end of current class vtable
```

This supersedes historical `15.32.df7b29` slot assumptions; historical addresses were never accepted as current evidence.

Current primary identities:

```text
GameclientMessageLogin
  RTTI      0x30ed530
  vtable AP 0x2f9ee90
  Clear     0x17785c0
  ByteSize  0x17728a0
  Serialize 0x177a7e0

LoginRSAEncryptedBlock
  RTTI      0x30ed518
  vtable AP 0x2f9ee50
  Clear     0x1778500
  ByteSize  0x1772740
  Serialize 0x1770200
```

## FACT — current `GameclientMessageLogin` wire shape

Current serializer `0x177a7e0` proves:

```text
field 1: varint           storage +0x30  tag 0x08
field 2: varint           storage +0x34  tag 0x10
field 3: varint           storage +0x38  tag 0x18
field 4: length-delimited storage +0x18  tag 0x22
field 5: length-delimited storage +0x20  tag 0x2a
field 6: varint           storage +0x3c  tag 0x30
field 7: embedded message storage +0x28  field number 7
```

Current `ByteSizeLong` at `0x17728a0` handles field 7 by loading `[this+0x28]` and calling current `LoginRSAEncryptedBlock::ByteSizeLong @ 0x1772740`. The nested class identity is therefore directly proven.

The current producer also writes literal `0x5fc` (`1532`) into outer storage `+0x34` and sets the corresponding presence bit. This is recorded only as a structural fact.

## FACT — current `LoginRSAEncryptedBlock` wire shape

Current serializer `0x1770200` proves:

```text
field 1: length-delimited storage +0x18 tag 0x0a
field 2: length-delimited storage +0x20 tag 0x12
field 3: varint           storage +0x40 tag 0x18
field 4: varint           storage +0x44 tag 0x20
field 5: length-delimited storage +0x28 tag 0x2a
field 6: length-delimited storage +0x30 tag 0x32
field 7: length-delimited storage +0x38 tag 0x3a
```

The matching current size function reads exactly the five length-delimited regions and two scalar regions above.

## FACT — current producer and retained source type

Current exact RTTI/vtable recovery gives:

```text
TLoginProtocolMessageHandler
  RTTI      0x30b4ed0
  vtable AP 0x30b6700
  slot +0x60 -> 0xe25620
  FDE          0xe25620..0xe2656d

TAuthenticationAndEncryptionInfo
  RTTI      0x30adc40
  vtable AP 0x2f82f98
```

The producer FDE references both current primary protobuf vtables. It loads `[handler+0x10]`; matching current virtual targets independently bind that retained object as `TAuthenticationAndEncryptionInfo`.

Instruction-proven structural value paths include:

```text
outer +0x34 <- literal 0x5fc
outer +0x3c <- producer third argument
nested +0x18 <- retained AuthInfo path rooted around +0xd0/+0xe0
nested +0x20 <- retained AuthInfo path rooted around +0xe8/+0xf8
nested +0x40/+0x44 <- producer input structure +0x18/+0x1c
nested +0x30 <- retained AuthInfo path rooted around +0x100/+0x110
nested +0x38 <- retained AuthInfo path rooted around +0x118/+0x128
```

A retained-value transform also feeds nested `+0x28`. Its user-facing semantic name is not proven.

Therefore semantic field names, password/session-token mapping and password participation remain `UNKNOWN`; no secret value was inspected to close those semantics.

## Track B structural discriminator

Trusted-main wire-writer evidence already proves current outer padding/XTEA/sequence/framing/QTcpSocket behavior and rejects changing generic outer transport as the next hypothesis.

The current payload handed to that layer is a generated `GameclientMessageLogin` with nested field 7 `LoginRSAEncryptedBlock`. Track B PR #284 still uses the legacy byte-oriented `ProtocolGame::sendLoginPacket()` pending-game/RSA body and does not currently replace `protocolgamesend.cpp` with this native typed representation.

Bounded source conclusion:

```yaml
CURRENT_GAME_LOGIN_TYPED_PAYLOAD: FACT:GameclientMessageLogin
CURRENT_GAME_LOGIN_FIELD7_TYPE: FACT:LoginRSAEncryptedBlock
CURRENT_LOGIN_PRODUCER: FACT:TLoginProtocolMessageHandler_slot_0x60_0xe25620
CURRENT_LOGIN_RETAINED_SOURCE_TYPE: FACT:TAuthenticationAndEncryptionInfo
CURRENT_OUTER_TRANSPORT_CHANGE_NEXT: REJECTED
TRACK_B_LEGACY_LOGIN_BODY_MATCHES_CURRENT_NATIVE_TYPED_PAYLOAD: DISPROVEN_STRUCTURALLY
PASSWORD_OR_SESSION_SEMANTIC_FIELD_NAMES: UNKNOWN
CAUSAL_EXPLANATION_OF_TRACK_B_0x14: UNKNOWN
```

This evidence rejects an identical Track B retry. It does **not** by itself authorize a protobuf replacement: every required current field value must first be sourced from Track B's authorized inputs/handoff without semantic guessing.

## Handoff

Continuation prompt:

`docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_CURRENT_SCHEMA_CONTINUE_ALIAS.md`

Alias:

`OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME-CURRENT-SCHEMA-CONTINUE`

Next legal action: a fresh independent coordinator must re-download/re-hash the exact artifact, audit PR #711 from primary evidence, promote only accepted sanitized facts from current protected `main`, complete source lifecycle/archive, and only then allow Track B #284 to consume the promoted result.
