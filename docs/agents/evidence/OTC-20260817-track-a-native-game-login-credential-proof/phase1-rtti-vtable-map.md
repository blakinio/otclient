# Phase 1 — exact-client login protobuf RTTI/vtable map

Task: `OTC-20260817-track-a-native-game-login-credential-proof`  
PR: `#499`  
Track: `official-client-re`  
Execution: `github_hosted`, `runtime_access: none`

## Exact-client fence

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

## Validation

```text
workflow: .github/workflows/tibia-official-client-re-game-login-credential-proof.yml
commit: f217eb716edb0c0176659596ab758d9ace7fee6a
run: 32060290084
job: 95479800295
result: SUCCESS
marker: GAMELOGIN_RTTI_PROBE=PASS
```

Safety markers:

```text
GAMELOGIN_RTTI_EXACT_PACKED_SHA=PASS
GAMELOGIN_RTTI_EXACT_CLIENT_SHA=PASS
GAMELOGIN_RUNTIME_ACCESS=none
GAMELOGIN_LOGIN_PERFORMED=false
GAMELOGIN_SECRET_ACCESS=false
GAMELOGIN_PROCESS_X11_OBSERVATION=false
GAMELOGIN_RAW_CLIENT_UPLOADED=false
```

## FACT — recovered exact RTTI/vtables

### `GameclientMessageLogin`

```text
RTTI name VA: 0x1d573c0
typeinfo:     0x30c5ce8
vptr:         0x30c84a0

+0x00 0x17838c0
+0x08 0x17806a0
+0x10 0x1769270
+0x18 0x1763520
+0x20 0x1758790
+0x28 0x1709840
+0x30 0x1b0ffb0
+0x38 0x1783690
+0x40 0x175d710
+0x48 0x1712ff0
+0x50 0x1758df0
+0x58 0x765a60
+0x60 0x176dec0
```

### `LoginRSAEncryptedBlock`

```text
RTTI name VA: 0x1d57380
typeinfo:     0x30c5cd0
vptr:         0x30c8428

+0x00 0x1783450
+0x08 0x1780640
+0x10 0x1769210
+0x18 0x1763460
+0x20 0x17586d0
+0x28 0x1709840
+0x30 0x1b0ffb0
+0x38 0x17734f0
+0x40 0x175d5e0
+0x48 0x1712ff0
+0x50 0x1758de0
+0x58 0x765a60
+0x60 0x176db40
```

### `GameclientMessageSecondaryLogin`

```text
RTTI name VA: 0x1d56280
typeinfo:     0x30c56d0
vptr:         0x30c6628

+0x00 0x1783aa0
+0x08 0x17807c0
+0x10 0x1769340
+0x18 0x1763640
+0x20 0x17588a0
+0x28 0x1709840
+0x30 0x1b0ffb0
+0x38 0x17737a0
+0x40 0x175d8e0
+0x48 0x1712ff0
+0x50 0x1758e10
+0x58 0x765a60
+0x60 0x176b010
```

### `SecondaryLoginRSAEncryptedBlock`

```text
RTTI name VA: 0x1d56240
typeinfo:     0x30c56b8
vptr:         0x30c65b0

+0x00 0x1783a60
+0x08 0x1780770
+0x10 0x17692d0
+0x18 0x17635b0
+0x20 0x1758830
+0x28 0x1709840
+0x30 0x1b0ffb0
+0x38 0x17738d0
+0x40 0x175d860
+0x48 0x1712ff0
+0x50 0x1758e00
+0x58 0x765a60
+0x60 0x176e1e0
```

## FACT — vtable boundary correction

The actual generated-message vtable for these classes has executable slots through `+0x60`. The qword at `+0x68` is zero and `+0x70` is the next class typeinfo/header boundary; for `LoginRSAEncryptedBlock`, `+0x70` points to `GameclientMessageLogin` typeinfo and `+0x78` begins the next class vtable.

Therefore entries after `+0x60` from a naive fixed-count vtable dump MUST NOT be treated as methods of the preceding protobuf class.

## FACT — useful control comparison

A control generated message (`GameclientMessageEnterWorld`) has:

```text
typeinfo: 0x30b8138
vptr:     0x30b86d0
+0x20 0x1713690
+0x38 0x175fe90
+0x40 0x175d970
+0x48 0x1713000
+0x50 0x1758e20
+0x60 0x176b0f0
```

The corresponding login/RSA slots are different, giving a bounded set of generated functions whose disassembly can reveal field offsets/wire tags without scanning the whole executable.

## UNKNOWN

- semantic method name for each vtable slot;
- exact field offsets/types/wire tags;
- which field, if any, carries a session key or password-derived data;
- producer provenance of each protected login field;
- secondary-login field relationship.

## Next discriminator

Disassemble only the differing generated-message slots `+0x20`, `+0x38`, `+0x40`, `+0x48`, `+0x50`, and `+0x60` for:

- `GameclientMessageLogin`;
- `LoginRSAEncryptedBlock`;
- `GameclientMessageSecondaryLogin`;
- `SecondaryLoginRSAEncryptedBlock`;
- `GameclientMessageEnterWorld` as control.

Use field-relative memory offsets, protobuf wire constants and call patterns to identify `Clear` / size / serialization / merge functions before assigning semantics.
