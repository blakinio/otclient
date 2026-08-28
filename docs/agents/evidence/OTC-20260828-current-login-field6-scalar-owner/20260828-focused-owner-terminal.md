# Focused current login field6 scalar-owner result

Terminal source classification: **FIELD6_VALUE_UNKNOWN**.

This evidence is source-only and static. It does not authorize Track B mutation or another official-service E2E.

## Exact identity

```text
source PR             #751
source head           a50a140cbdf4038921ed29e30cf0f53f8158bc27
source workflow       33174706577 = SUCCESS
source job            98860195057 = SUCCESS
CI                     33174706753 = SUCCESS
Track A governance     33174706531 = SUCCESS
artifact               9687275655
artifact sha256        136dc08adef86f742f44a5c71fdb6ff3ccf7f7a2e856336ba26ed051526e722c
result.json sha256     9c0537ee03d8afaf62bb78a7c567b54e712448a1411da7f7d6c8f29036078b0a
client version         15.32.75d4a0
client sha256          d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
client size            52105824
```

Safety remained `runtime_access:none`; the official client was not executed, no login or secret access occurred, no process memory or packet payload was accessed, and no raw client was uploaded.

## Fresh exact reassertion

The focused pass independently reasserted on the exact current binary:

```text
TLoginProtocolMessageHandler vtable AP  0x30b6700
slot +0x60 target                       0xe25620
viable scalar caller FDE                0xcedd90..0xcee0ec
viable callsite                         0xceddcb
receiver                                [this + 0x10]
edx                                     1
```

The exact instructions are `mov r12,rdi`, `mov rdi,[r12+0x10]`, `mov edx,1`, `mov rax,[rdi]`, `call [rax+0x60]`.

## Focused owner result

Direct-edge/QMeta recovery proved that the viable `edx=1` FDE is reached by four QMeta cases of **`tibia::worldmap::TWorldmapProtocolMessageHandler`**:

- `handleLeftColumnMessage(GameserverMessageLeftColumn)`;
- `handleRightColumnMessage(GameserverMessageRightColumn)`;
- `handleTopRowMessage(GameserverMessageTopRow)`;
- `handleBottomRowMessage(GameserverMessageBottomRow)`.

Because the FDE belongs to worldmap handling rather than the authentication login handler ownership chain, this scalar `1` is **not** evidence for `GameclientMessageLogin.field6`.

The earlier independent scalar census had exactly three statically scalar `slot+0x60` sites:

```text
0xaa5132  edx=0  ABI receiver mismatch -> rejected
0xceddcb  edx=1  focused owner = TWorldmapProtocolMessageHandler -> rejected
0x16da716 edx=0  parent-this provenance not proven -> not accepted
```

No scalar callsite is deterministically bound to `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620`. Therefore:

```yaml
FIELD6_VALUE_PROVEN: false
FIELD6_VALUE: UNKNOWN
TRACK_B_PAYLOAD_MUTATION_AUTHORIZED: false
OFFICIAL_SERVICE_GAME_E2E_AUTHORIZED: false
```

## Next boundary

The remaining exact-current path must follow the already-promoted `TAuthenticationProcessController` login-handler owner field (`+0x9c0`) through its actual pointer handoff / helper / Qt path to `TLoginProtocolMessageHandler::slot+0x60`, then recover the real producer `edx` reaching value. Do not revisit the eliminated `edx=1` worldmap candidate or rank scalar constants.