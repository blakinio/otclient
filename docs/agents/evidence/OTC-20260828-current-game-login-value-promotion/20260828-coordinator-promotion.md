# Coordinator promotion — current game-login envelope/value facts

Decision: **PASS_BOUNDED / ACCEPT_WITH_EDITS**.

This promotion was independently reconstructed from trusted `main@462320593ce3efc764af443c23c51ac725e1759a` and the final exact-head source run for PR #729. The source workflow/analyzer is not promoted.

## Primary evidence identity

```text
source PR             #729 (Draft, source-only)
source head           9876df611c8bf7f9c5cd07b3b28f5d12ee8c6e28
producer run          33121134592 = SUCCESS
producer job          98687978755 = SUCCESS
artifact              9666544571
GitHub artifact digest sha256:af5b57e8dbd5a5b0b597f71d4d367e7c9511aa98c56c10ba7cc8380db9050ebf
re-downloaded ZIP      sha256:af5b57e8dbd5a5b0b597f71d4d367e7c9511aa98c56c10ba7cc8380db9050ebf
trace.json             sha256:c1b37821925939295cde1bdcae657af338d7cfd370704e201bcb438d7d52180d
```

The exact public Linux client fence remained:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Safety markers remained static-only: `runtime_access=none`, `login_performed=false`, `secret_access=false`, `raw_client_uploaded=false`.

## Accepted top-level wire envelope

The exact build contains generated `tibia::protobuf::protocol::GameclientMessage` at RTTI `0x30ea9d8`, vtable address point `0x2f992e0`. Its current generated slots bind `ByteSizeLong` to `0x1781160` and `_InternalSerialize` to `0x1781050`.

`TProtocolMessageQueue::sendLogin` adapter `0xbd3050..0xbd34dd` constructs that message and writes scalar storage `message+0x30 = 10`. The generated serializer emits that scalar as protobuf field 1/tag `0x08`.

The same serializer invokes helper `0x1b55da0..0x1b55e4d` with `field_number=1000`; the helper writes `(1000 << 3) | 2`, the payload length, and dispatches the embedded message `_InternalSerialize`. Therefore the current primary login application payload is structurally:

```text
GameclientMessage {
  field 1   varint = 10
  field 1000 length-delimited = GameclientMessageLogin
}
```

This is **not** the historical raw one-byte `0x0A` body.

## Accepted current login scalar values

The current `GameclientMessageLogin` schema/field locations remain as promoted by #719. This task additionally closes the following current-value facts:

- field 2 is the producer literal `0x5fc` = **1532**;
- field 3 is built from current static text **`15.32`**, removes non-digits, and parses base-10, yielding **1532**;
- the platform selector compares `windows`, `macos`, `linux`; Linux resolves the constructor state used by the login producer to **7**;
- the exact state→wire map contains the identity pair **7→7**, so the normal Linux value for field 1 is **7**.

No semantic name beyond those directly supported by the exact dataflow is invented.

## Accepted XTEA / nested-block fact

Trusted #724 already maps `TAuthenticationAndEncryptionInfo` slot `+0x18` to `LoginRSAEncryptedBlock` field 5. The exact current build also identifies `shared::TXteaHelper` (`RTTI 0x30adc00`, vtable `0x2f82ea0`); slot `+0x10 -> 0xf71d70` requires an exact 16-byte input and copies it into the XTEA key material. `TAuthenticationAndEncryptionInfo` slot `+0x10 -> 0xe26570` passes the same underlying retained 16-byte value to that XTEA setter.

Therefore:

```yaml
LOGIN_RSA_ENCRYPTED_BLOCK_FIELD5: PROVEN_XTEA_KEY_BYTES_16
```

The class name `LoginRSAEncryptedBlock` is not evidence of an additional current RSA transform. In the proved primary path its generated protobuf serializer writes the nested message bytes directly into `GameclientMessageLogin`, after which the already-promoted generic transport performs the current XTEA/sequence/framing path. No separate login RSA transform was found in the exact producer→queue→processor chain.

## Track B consequences

The current Track B #284 body begins with legacy `ClientPendingGame`, writes a legacy OS/protocol/version/string/asset header, creates a fixed RSA block, RSA-encrypts it, and only then relies on generic transport. That application body is now disproven for `15.32.75d4a0`.

The next Track B change may replace only the application login body with the proved `GameclientMessage`/`GameclientMessageLogin` protobuf envelope while preserving the already-proven generic transport. A subsequent official-service E2E is allowed only after that material payload change.

## Still withheld / fail-closed

```yaml
GameclientMessageLogin_field4_user_facing_name: UNKNOWN_CURRENT_EXACT
GameclientMessageLogin_field5_user_facing_name: UNKNOWN_CURRENT_EXACT
GameclientMessageLogin_field6_semantic_name_and_value: UNKNOWN
LoginRSAEncryptedBlock_fields1_2_6_7_user_facing_names: UNKNOWN
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT_PROVEN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT_PROVEN
```

Historical/current-neighbor evidence may be used as a cross-check, but these names are not promoted unless current exact causality exists. Track B must not manufacture values for unknown required fields; it may use only values already present in its authorized handoff where a current structural destination has been proven, or stop at the first unknown boundary.
