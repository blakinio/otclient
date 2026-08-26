# Coordinator promotion — current game-login schema

Date: 2026-08-27  
Source task: `OTC-20260826-current-game-login-schema`  
Source Draft: PR #711  
Promotion task: `OTC-20260827-current-game-login-schema-promotion`

Decision: **ACCEPT_WITH_EDITS**

## Trust boundary

The coordinator did not use the researcher summary as proof. The exact final producer artifact was independently re-downloaded from GitHub Actions and re-hashed before review.

```text
source PR live head       39e1f7343d8c3932356a78db1eae00147e810d7d
source evidence head      d24b6e61d1086094112020db6e7d959c24bdb34a
producer run              33017207072 = SUCCESS
producer job              98338388458
artifact                  9625060590
GitHub artifact digest    sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
re-downloaded ZIP sha256  be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result.json sha256        1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
```

The artifact contains one sanitized `result.json` and no raw official-client binary.

Exact current package fence in the artifact:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Safety markers in primary evidence pass: `runtime_access:none`, `login_performed=false`, `secret_access=false`, `raw_client_uploaded=false`.

## Independent ABI and serializer audit

Current exact RTTI/vtable identities are unique in the sanitized artifact for the two target generated messages.

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

Behavioral slot comparison supports the current generated-message layout used by this evidence:

```text
+0x10 Clear-equivalent
+0x18 ByteSizeLong-equivalent
+0x28 _InternalSerialize-equivalent
+0x30 zero / end of current class vtable
```

Historical build addresses are not promoted.

## Accepted `GameclientMessageLogin` wire shape

The current serializer snapshot at `0x177a7e0` directly ties scalar/string storage to protobuf tags. The current `ByteSizeLong` snapshot at `0x17728a0` separately confirms the same storage and nested-message path.

```text
field 1: varint           storage +0x30  tag 0x08
field 2: varint           storage +0x34  tag 0x10
field 3: varint           storage +0x38  tag 0x18
field 4: length-delimited storage +0x18  tag 0x22
field 5: length-delimited storage +0x20  tag 0x2a
field 6: varint           storage +0x3c  tag 0x30
field 7: embedded message storage +0x28  field number 7
```

The nested type is independently accepted because `GameclientMessageLogin::ByteSizeLong @ 0x17728a0` loads `[this+0x28]` and calls current `LoginRSAEncryptedBlock::ByteSizeLong @ 0x1772740`.

The producer writes literal `0x5fc` into outer storage `+0x34`; this is promoted only as a structural value fact, not as an invented semantic field name.

## Accepted `LoginRSAEncryptedBlock` wire shape

The current serializer snapshot at `0x1770200` proves:

```text
field 1: length-delimited storage +0x18 tag 0x0a
field 2: length-delimited storage +0x20 tag 0x12
field 3: varint           storage +0x40 tag 0x18
field 4: varint           storage +0x44 tag 0x20
field 5: length-delimited storage +0x28 tag 0x2a
field 6: length-delimited storage +0x30 tag 0x32
field 7: length-delimited storage +0x38 tag 0x3a
```

The matching size-function snapshot reads the same five length-delimited regions and two scalar regions.

## Accepted producer provenance

Current primary evidence identifies:

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

The producer FDE references both current primary protobuf vtables and uses the retained `[handler+0x10]` owner object. Matching current virtual-target evidence binds that retained object to `TAuthenticationAndEncryptionInfo`.

Accepted structural value paths are limited to the address/offset relations directly visible in the artifact. User-facing semantic names of those retained fields are withheld.

## Track B implication

Trusted-main promotion #706 already proves the current generic outer padding/XTEA/sequence/framing/QTcpSocket writer shape and rejects another generic outer-framing guess.

This promotion establishes the earlier payload mismatch: the current official login producer constructs a generated `GameclientMessageLogin` containing nested `LoginRSAEncryptedBlock`, while Track B PR #284 still constructs its legacy byte-oriented pending-game/RSA login body.

```yaml
CURRENT_GAME_LOGIN_TYPED_PAYLOAD: PROVEN_GameclientMessageLogin
CURRENT_GAME_LOGIN_FIELD7_TYPE: PROVEN_LoginRSAEncryptedBlock
CURRENT_LOGIN_PRODUCER: PROVEN_TLoginProtocolMessageHandler_slot_0x60_0xe25620
CURRENT_LOGIN_RETAINED_SOURCE_TYPE: PROVEN_TAuthenticationAndEncryptionInfo
TRACK_B_LEGACY_LOGIN_BODY_MATCHES_CURRENT_NATIVE_TYPED_PAYLOAD: DISPROVEN_STRUCTURALLY
CURRENT_OUTER_TRANSPORT_CHANGE_NEXT: REJECTED
```

This rejects an identical Track B retry, but it does **not** authorize a guessed protobuf replacement. Before Track B mutation, every required current field value must be sourced from Track B's already-authorized inputs/current handoff without inventing password/session semantics.

## Withheld / unknown

```yaml
PASSWORD_OR_SESSION_SEMANTIC_FIELD_NAMES: UNKNOWN
PASSWORD_OR_SESSION_TO_RSA_FIELD_MAPPING: UNKNOWN
RETAINED_AUTHINFO_USER_FACING_FIELD_NAMES: UNKNOWN
CAUSAL_EXPLANATION_OF_TRACK_B_0x14: UNKNOWN
```

No secret inspection is used to close these semantics.

## Source PR audit

Live source PR #711 is Draft and changes exactly seven declared task-owned files: one hosted research workflow, one probe, two probe/workflow tests, source evidence, source task record and continuation alias. Review threads and submitted reviews are empty at audit time. No Track B path, proprietary binary or credential material is present in the changed-file inventory.

The source workflow/analyzer is intentionally **not promoted**. Only this independently reviewed docs/evidence result is intended for trusted `main`.

```yaml
audit:
  result: PASS_BOUNDED
  decision: ACCEPT_WITH_EDITS
  independent_validator_role: coordinator
  primary_artifact_rehashed: true
  researcher_summary_used_as_proof: false
  source_diff_scope_reviewed: true
  source_changed_files: 7
  source_review_threads: 0
  source_submitted_reviews: 0
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: docs-only static evidence promotion; no runtime behavior changes
```

After this promotion reaches trusted `main`, source PR #711 can be closed unmerged as consumed/superseded and its source task archived/released according to repository convention. Track B #284 may then consume only these promoted facts and must stop at the first unproven required field-value provenance boundary rather than guess.
