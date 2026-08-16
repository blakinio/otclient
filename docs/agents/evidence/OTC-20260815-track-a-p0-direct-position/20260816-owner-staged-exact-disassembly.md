# P0 owner-staged exact-client disassembly evidence

Date: 2026-08-16
Consumer: PR #302 / `OTC-20260815-track-a-p0-direct-position`

## FACT — exact input fence

All source byte windows used below were read-only staged from the retained OTClient runner work volume and fenced as:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Successful source runs on `blakinio/Oteryn-Platform`, runner `oteryn-synology-staging`:

- `31952152531 / 95177178103`: exact bytes `0x836500..0x836a00`;
- `31952247901 / 95177409417`: exact bytes covering `0xd1cbd0`, `0xd2ac70`, `0xd2ef30`, `0x843e20`, `0x843f60`;
- `31952364373 / 95177697400`: exact bytes covering `0xeda3c0`, `0xeda3e0`, `0xee0010`, `0xee0100`.

Every source run declared `CLIENT_EXECUTED=false`, `PROCESS_MEMORY_ACCESSED=false`, `NETWORK_ACCESSED=false`, `CANONICAL_RUNTIME_SESSION_TOUCHED=false`.

The byte windows were deterministically decoded with GNU objdump 2.44. The complete derived text file is `p0-disasm.txt`, 76290 bytes, SHA-256:

`3e560917e407f8016d3a1fa31bf1b43403050cbcac4b94dd5972d78a72179b92`

No proprietary client binary is contained in this evidence.

## FACT — missing `playerPosition` instruction body recovered

Function boundary visible at `0x836580`:

```asm
836580: push   r15
836582: push   r14
836584: push   r13
836586: push   r12
836588: push   rbp
836589: push   rbx
83658a: mov    rbx,rsi
```

The recovered body constructs three successive decimal components from consecutive 32-bit members of the object retained in `rbx`:

```asm
836659: movsxd rdx,DWORD PTR [rbx+0x78]
83665d: mov    r9d,0x20
836663: xor    ecx,ecx
836665: mov    rsi,r12
836668: lea    rbp,[rsp+0xa0]
836670: mov    r8d,0xa
836676: mov    rdi,rbp
836679: call   0x4dfcd0

83667e: movsxd rdx,DWORD PTR [rbx+0x7c]
836682: mov    r9d,0x20
836688: xor    ecx,ecx
83668a: mov    rsi,rbp
83668d: lea    r13,[rsp+0x80]
836695: mov    r8d,0xa
83669b: mov    rdi,r13
83669e: call   0x4dfcd0

8366a3: lea    r15,[rsp+0x20]
8366a8: mov    r9d,0x20
8366ae: xor    ecx,ecx
8366b0: mov    rsi,r13
8366b3: movsxd rdx,DWORD PTR [rbx+0x80]
8366ba: mov    r8d,0xa
8366c0: mov    rdi,r15
8366c3: call   0x4dfcd0
```

Immediately before the exact primary literal:

```asm
8367b1: mov    rsi,r15
8367b4: mov    rdi,rbp
8367b7: call   0x4dfa80
8367bc: mov    esi,0xe
8367c1: lea    rdx,[rip+0x14a7677]  # 0x1cdde3f = "playerPosition"
8367c8: mov    rdi,r12
8367cb: call   0x4df210
8367d0: mov    rdx,rbp
8367d3: mov    rsi,r12
8367d6: mov    rdi,r13
8367d9: call   0x4dd4c0
```

Therefore the previous `DISASM_COMMAND_FAILED` gap at `0x8367c1` is closed.

## FACT — requested TPlayerData vtable target entry instructions

Exact target entries include:

```asm
d1cbd0: mov    rdi,QWORD PTR [rdi+0x8]
d2ac70: test   rsi,rsi
d2ef30: push   r12
843e20: lea    rax,[rip+0x2848c49]  # 0x308ca70
843f60: lea    rax,[rip+0x2848b09]  # 0x308ca70
eda3c0: mov    eax,DWORD PTR [rdi+0x18]
eda3e0: mov    eax,DWORD PTR [rdi+0x1c]
ee0010: push   r12
ee0100: cmp    DWORD PTR [rdi+0x1c],esi
```

The `0x843e20` and `0x843f60` entries independently reference the already-proven `TPlayerData` primary vptr `0x308ca70`.

## Classification

### FACT

- the missing static instruction body is recovered from the exact fenced client;
- the `playerPosition` property construction reads a consecutive signed 32-bit triple at offsets `+0x78`, `+0x7c`, `+0x80` from the object held in `rbx` (`rbx <- rsi` at function entry);
- those three values are converted/concatenated immediately upstream of the exact `playerPosition` property literal;
- all nine requested TPlayerData vtable target neighborhoods are now available as exact-client byte/disassembly evidence.

### INFERENCE

`+0x78/+0x7c/+0x80` is now a high-confidence direct XYZ-shaped backing candidate on the object passed as the function's second argument. This is materially stronger than the former string-only/xref evidence.

### UNKNOWN / NOT YET PROMOTED

Static evidence alone does not yet prove that the `rbx` owner at this call site is the authoritative live `TPlayerData` instance rather than a provider/render/status object or copy. Causal live-world correlation, negative controls, repeatability and relogin stability remain RUNTIME/P0 acceptance requirements. Do not promote `+0x78/+0x7c/+0x80` to authoritative player XYZ until that owner/type and live semantics are proven.
