# Phase 2 — exact-client login protobuf wire schema discriminator

Task: `OTC-20260817-track-a-native-game-login-credential-proof`  
PR: `#499`  
Track: `official-client-re`  
Execution: `github_hosted`, `runtime_access: none`

## Exact-client fence and validation

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
workflow commit: 1fc634a19a0e08d988d1dbcfcc6977b0c671b54a
run: 32060478430
job: 95480403222
result: SUCCESS
marker: GAMELOGIN_METHOD_DISCRIMINATOR=PASS
```

Safety markers all passed:

```text
GAMELOGIN_METHOD_EXACT_PACKED_SHA=PASS
GAMELOGIN_METHOD_EXACT_CLIENT_SHA=PASS
GAMELOGIN_RUNTIME_ACCESS=none
GAMELOGIN_LOGIN_PERFORMED=false
GAMELOGIN_SECRET_ACCESS=false
GAMELOGIN_PROCESS_X11_OBSERVATION=false
GAMELOGIN_RAW_CLIENT_UPLOADED=false
```

## FACT — generated protobuf virtual-method semantics

Cross-comparison with the empty `GameclientMessageEnterWorld` control and direct behavior identifies the generated-message vtable slots as follows:

```text
+0x20  Clear
+0x38  Merge/copy from another message
+0x40  ByteSizeLong / compute serialized size and cache it
+0x48  cached-size accessor
+0x50  metadata/descriptor trampoline
+0x60  _InternalSerialize
```

This mapping is based on actual instruction behavior, not assumed ABI slot naming.

## FACT — `GameclientMessageLogin` has seven protobuf fields

Has-bits are stored in `[this+0x10]` and use bits:

```text
0x01  0x02  0x04  0x08  0x10  0x20  0x40
```

`Clear @ 0x1758790`, merge/copy `@ 0x1783690`, `ByteSizeLong @ 0x175d710`, and `_InternalSerialize @ 0x176dec0` together prove seven fields.

### Proven field storage and wire types so far

| field | has-bit | object storage | wire evidence | status |
|---:|---:|---|---|---|
| 1 | `0x08` | scalar `+0x30` | serializer writes tag `0x08` | **FACT: varint** |
| 2 | `0x10` | scalar `+0x34` | serializer writes tag `0x10` | **FACT: varint** |
| 3 | `0x20` | scalar `+0x38` | serializer writes tag `0x18` | **FACT: varint** |
| 4 | `0x01` | length-delimited-like `+0x18` | branch target `0x176e000` | field number/type branch tag not yet decoded |
| 5 | `0x02` | length-delimited-like `+0x20` | branch target `0x176dfb0` | field number/type branch tag not yet decoded |
| 6 | `0x40` | scalar `+0x3c` | serializer writes tag `0x30` | **FACT: varint** |
| 7 | `0x04` | non-scalar branch, candidate storage near `+0x28` | serializer branch `0x176e050`; ByteSize branch `0x175d820` | exact nested/length-delimited contract not yet decoded |

`ByteSizeLong` proves fields 4 and 5 are length-delimited-like because it reads the length from the protobuf string/message representation at `+0x18` and `+0x20`. Field 7 must be decoded from its branch before its precise type is promoted.

## FACT — `LoginRSAEncryptedBlock` has seven protobuf fields

Has-bits again use `0x01..0x40`.

`Clear @ 0x17586d0` proves five string/length-delimited storage fields and two scalar fields:

```text
bit 0x01 -> +0x18 length-delimited-like
bit 0x02 -> +0x20 length-delimited-like
bit 0x04 -> +0x28 length-delimited-like
bit 0x08 -> +0x30 length-delimited-like
bit 0x10 -> +0x38 length-delimited-like
bit 0x20 -> +0x40 scalar
bit 0x40 -> +0x44 scalar
```

`ByteSizeLong @ 0x175d5e0` independently confirms five length-delimited values at `+0x18,+0x20,+0x28,+0x30,+0x38` plus two varint-size calculations for `+0x40,+0x44`.

`_InternalSerialize @ 0x176db40` directly proves:

| has-bit | storage | proven tag | proven wire type |
|---:|---:|---:|---|
| `0x20` | `+0x40` | `0x18` | field 3, varint |
| `0x40` | `+0x44` | `0x20` | field 4, varint |

Remaining branch targets for exact tags:

```text
bit 0x01 -> 0x176dc40
bit 0x02 -> 0x176dbf0
bit 0x04 -> 0x176dd68
bit 0x08 -> 0x176dd18
bit 0x10 -> 0x176dc90
```

Until those branches are decoded, the likely field numbers of the five length-delimited values are an inference and are not promoted here.

## FACT — secondary-login structures are much smaller

### `GameclientMessageSecondaryLogin`

Has-bits: `0x01`, `0x02`.

```text
bit 0x02 -> scalar +0x20 -> serializer tag 0x08 -> field 1 varint
bit 0x01 -> branch 0x176b060 -> second field type/tag not yet decoded
```

### `SecondaryLoginRSAEncryptedBlock`

Has-bits: `0x01`, `0x02`.

```text
bit 0x01 -> length-delimited-like +0x18
bit 0x02 -> second branch-defined field
serializer branches: 0x176e220, 0x176e269
```

The exact tags/types must be decoded before assigning challenge/session semantics.

## FACT — current evidence is schema, not credential provenance

This phase proves message field count, storage families, several exact wire tags and the exact generated serializer locations. It does **not** identify which native producer populates any string field and therefore does not yet prove whether a password participates in game-server login.

## UNKNOWN

```text
semantic field names
full ordered tags for all length-delimited fields
which GameclientMessageLogin field embeds LoginRSAEncryptedBlock
which LoginRSAEncryptedBlock field is session/auth material
whether any field is populated from an account password
producer provenance from TPlaySessionData / selected character / challenge state
secondary-login challenge credential semantics
```

## Next discriminator

Bounded disassembly only of the serializer/size branch targets:

```text
GameclientMessageLogin:
  0x176dfb0
  0x176e000
  0x176e050
  0x175d820

LoginRSAEncryptedBlock:
  0x176dbf0
  0x176dc40
  0x176dc90
  0x176dd18
  0x176dd68

GameclientMessageSecondaryLogin:
  0x176b060

SecondaryLoginRSAEncryptedBlock:
  0x176e220
  0x176e269
```

No full-executable scan or runtime escalation is justified while this exact static discriminator remains productive.
