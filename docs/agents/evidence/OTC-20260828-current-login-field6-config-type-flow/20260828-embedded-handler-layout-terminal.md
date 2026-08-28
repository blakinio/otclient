# Current login field6 embedded-handler layout

Terminal source result for PR #759: **STRUCTURAL PASS / FIELD6 VALUE STILL UNKNOWN**.

## Exact evidence

```text
source PR             #759
proving head          8bbb41dc1347b4271019cdbabdd5af6e13bbff1e
source workflow       33193729546 = SUCCESS
source job            98925452352 = SUCCESS
artifact               9694879860
artifact sha256        b7490480e88690bb05d301072056012a096d92a52089358b2e0a673416800709
result.json sha256     b7cb8472ca6bda802e2d0c428686ef9219bae2a772583eb38e44f7a7959df9aa
client version         15.32.75d4a0
client sha256          d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
client size            52105824
```

Safety remained `runtime_access:none`: no official-client execution, login, secret/process-memory access, packet capture, gameplay, or proprietary-client upload.

## Exact constructor layout

Constructor FDE `0x7d15c0..0x7d1a8a` reasserted:

```text
0x7d15df  mov edi, 0x38
0x7d15e7  call 0x4d8670
0x7d15f5  mov rbp, rax
0x7d15fc  lea rax, [rip + 0x27b8635]   -> vtable AP 0x2f89c38
0x7d1603  lea r14, [rbp + 0x10]
0x7d1607  mov [rbp], rax
0x7d1613  lea rax, [rip + 0x28e50e6]   -> TLoginProtocolMessageHandler vtable AP 0x30b6700
0x7d1622  mov [rbp + 0x10], rax
0x7d1677  mov dword ptr [rbp + 0x30], edx
0x7d167e  mov [owner + 0x9c0], r14
0x7d1685  mov [owner + 0x9c8], rbp
```

Raw RTTI for parent vtable AP `0x2f89c38` is:

```text
St23_Sp_counted_ptr_inplaceIN5tibia14authentication28TLoginProtocolMessageHandlerESaIvELN9__gnu_cxx12_Lock_policyE2EE
```

This is the libstdc++ `std::_Sp_counted_ptr_inplace< tibia::authentication::TLoginProtocolMessageHandler, ... >` control block. Therefore `owner+0x9c8` is not an independent semantic config object; it is the shared_ptr control block containing the actual handler at `rbp+0x10`.

## Field relation

The exact layout proves:

```text
control block base       rbp
embedded handler         rbp + 0x10
owner handler field      owner + 0x9c0 -> rbp + 0x10
owner control block      owner + 0x9c8 -> rbp
mode store               rbp + 0x30
handler-relative mode    (rbp + 0x30) - (rbp + 0x10) = +0x20
```

Hence the constructor's mode-like dword is **`TLoginProtocolMessageHandler + 0x20`**.

Independent exact-current producer evidence from the already-promoted `0xe25620..0xe2656d` producer shows that the producer itself reads/compares `[handler + 0x20]` (including a `== 4` branch) while outer `GameclientMessageLogin.field6` is populated from producer input `edx`. This establishes that the mode member is directly relevant to the native login producer, but does not yet prove what exact current path supplies as `edx`.

```yaml
CONFIG_CONTROL_BLOCK_IDENTITY: PROVEN
EMBEDDED_LOGIN_HANDLER_OFFSET: 0x10
LOGIN_HANDLER_MODE_MEMBER_OFFSET: 0x20
FIELD6_VALUE_PROVEN: false
FIELD6_VALUE: UNKNOWN
TRACK_B_MUTATION_AUTHORIZED: false
OFFICIAL_SERVICE_GAME_E2E_AUTHORIZED: false
```

## Next boundary

A successor must stay entirely within `TLoginProtocolMessageHandler`: re-derive its exact vtable and constructor mode member `+0x20`, enumerate only handler-owned virtual methods/direct helpers, and find a causal wrapper/path that supplies the handler to ABI `rdi`, supplies either `[handler+0x20]` or an exactly-proven transformation to ABI `edx`, and reaches virtual slot `+0x60 -> 0xe25620`.

Do not return to global `slot+0x60` ranking or the eliminated worldmap scalar candidate.