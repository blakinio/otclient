# Phase 3 — complete native game-login wire tags

Task: `OTC-20260817-track-a-native-game-login-credential-proof`  
PR: `#499`  
Execution: exact-SHA GitHub-hosted static analysis, `runtime_access: none`

## Validation

```text
workflow commit: 74718a251749c62242eafe3c699d2ebc17e2ce45
run: 32060850607
job: 95481565159
result: SUCCESS
marker: GAMELOGIN_BRANCH_TAG_PROBE=PASS
```

Exact client and safety markers all passed. No client process was started and no credential/session value was read.

## FACT — complete `GameclientMessageLogin` ordered wire structure

Previously proven scalar fields:

```text
field 1 -> storage +0x30 -> tag 0x08 -> varint
field 2 -> storage +0x34 -> tag 0x10 -> varint
field 3 -> storage +0x38 -> tag 0x18 -> varint
field 6 -> storage +0x3c -> tag 0x30 -> varint
```

Run #4 proves the remaining fields:

```text
field 4 -> storage +0x18 -> tag 0x22 -> length-delimited
field 5 -> storage +0x20 -> tag 0x2a -> length-delimited
field 7 -> storage +0x28 -> embedded message -> length-delimited message field #7
```

Most importantly, `GameclientMessageLogin::ByteSizeLong @ 0x175d710` branches at `0x175d820` for field 7 and executes:

```asm
mov rdi, qword ptr [r9 + 0x28]
call 0x175d5e0
```

`0x175d5e0` is the already-proven `LoginRSAEncryptedBlock::ByteSizeLong` slot. Therefore:

```text
GameclientMessageLogin.field7 @ +0x28
  = embedded LoginRSAEncryptedBlock
```

The field-7 serializer branch `0x176e050` loads `[this+0x28]`, loads its cached size from `+0x14`, sets `edi=7`, and calls the generated embedded-message serializer helper `0x1b4f660`. This independently confirms the nested field number.

### Exact message shape

```text
GameclientMessageLogin {
  field 1: varint          // +0x30
  field 2: varint          // +0x34
  field 3: varint          // +0x38
  field 4: bytes/string    // +0x18
  field 5: bytes/string    // +0x20
  field 6: varint          // +0x3c
  field 7: LoginRSAEncryptedBlock // +0x28
}
```

Declared semantic protobuf types/names for fields 1–6 are not yet assigned; `varint` and length-delimited are wire-level FACTs.

## FACT — complete `LoginRSAEncryptedBlock` ordered wire structure

Run #4 directly emits the five length-delimited tags:

```text
field 1 -> +0x18 -> tag 0x0a -> length-delimited
field 2 -> +0x20 -> tag 0x12 -> length-delimited
field 5 -> +0x28 -> tag 0x2a -> length-delimited
field 6 -> +0x30 -> tag 0x32 -> length-delimited
field 7 -> +0x38 -> tag 0x3a -> length-delimited
```

Combined with the already-proven scalar tags:

```text
field 3 -> +0x40 -> tag 0x18 -> varint
field 4 -> +0x44 -> tag 0x20 -> varint
```

The exact wire shape is therefore:

```text
LoginRSAEncryptedBlock {
  field 1: bytes/string // +0x18
  field 2: bytes/string // +0x20
  field 3: varint       // +0x40
  field 4: varint       // +0x44
  field 5: bytes/string // +0x28
  field 6: bytes/string // +0x30
  field 7: bytes/string // +0x38
}
```

No semantic name such as `password` or `session_key` is assigned merely from field type.

## FACT — secondary login structure

`GameclientMessageSecondaryLogin` has:

```text
field 1 -> scalar +0x20 -> tag 0x08 -> varint
field 2 -> embedded-message branch at +0x18, generated helper called with field number 2
```

`SecondaryLoginRSAEncryptedBlock` has exactly two length-delimited fields:

```text
field 1 -> +0x18 -> tag 0x0a
field 2 -> +0x20 -> tag 0x12
```

The exact class identity of `GameclientMessageSecondaryLogin.field2` still needs a direct nested ByteSize/copy identity check before being promoted as `SecondaryLoginRSAEncryptedBlock`, although the adjacent native type family makes it the leading hypothesis.

## FACT — schema alone still cannot answer password participation

The exact `LoginRSAEncryptedBlock` contains five opaque length-delimited values. Any one could be a session key, character/world string, device/client material, password-derived value, or other protocol datum. The field layout does not establish value provenance.

Therefore at this phase:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
```

## Next discriminator

Recover the exact `TProtocolMessageQueue` login-related QMeta method targets and disassemble only:

1. the proven `sendLoginMessage` adapter/delegator boundary;
2. the queue method that constructs `GameclientMessageLogin` / `LoginRSAEncryptedBlock`;
3. the corresponding secondary-login method.

Trace each write to `GameclientMessageLogin +0x18/+0x20/+0x28/+0x30/+0x34/+0x38/+0x3c` and nested `LoginRSAEncryptedBlock +0x18/+0x20/+0x28/+0x30/+0x38/+0x40/+0x44` back to its native source object. Promotion to `YES` or `NO` requires that producer provenance, not absence/presence of password strings elsewhere in the binary.
