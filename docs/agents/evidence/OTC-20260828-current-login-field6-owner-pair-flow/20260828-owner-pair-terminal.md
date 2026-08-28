# Current login field6 owner-pair terminal result

Terminal source classification: **FIELD6_VALUE_UNKNOWN / OWNER_PAIR_DIRECT_FLOW_UNKNOWN**.

## Exact evidence

```text
source PR             #757
source head           5391b62ce2a92b2b2a94dc09b30a9687758ab972
source workflow       33192191661 = SUCCESS
source job            98920197885 = SUCCESS
CI                     33192191992 = SUCCESS
Track A governance     33192191835 = SUCCESS
artifact               9694296429
artifact sha256        131c01a1482100ff32adee9bbfa8a33a6dfa8cf4e41ba6f4b5fae0afa4b5a23b
result.json sha256     2d4ced56143212832c570c57544c1ecf08637ed26df3f49e5c65eaa86deb9246
client version         15.32.75d4a0
client sha256          d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
client size            52105824
```

Safety remained `runtime_access:none`: no official-client execution, login, credentials/session access, process-memory access, packet capture, gameplay, or raw-client upload.

## Reasserted owner pair

The exact current constructor FDE `0x7d15c0..0x7d1a8a` reasserted:

```text
0x7d1677  mov dword ptr [rbp + 0x30], edx
0x7d167e  mov qword ptr [rbx + 0x9c0], r14   # login handler owner field
0x7d1685  mov qword ptr [rbx + 0x9c8], rbp   # adjacent config object
```

The handler vtable remains `0x30b6700`, with virtual slot `+0x60 -> 0xe25620`.

CFG-aware reaching-definition analysis for the `config+0x30` write found:

```text
0x7d1658  edx = 7
0x7d1662  edx = 5
0x7d1a39  non-scalar: edx = [edx + edx*2 + 6]
0x7d1a51  non-scalar: edx = [edx + edx*2 + 5]
```

The bounded result therefore does not reduce `config+0x30` to one current constant. `values=[5,7]` are only the directly constant branches; the two computed branches remain structurally distinct and are not guessed.

## Direct-flow result

The exact analyzer examined all `call [vtable+0x60]` sites and required, in the same FDE:

1. handler pointer loaded from the same entry-proven owner at `+0x9c0` into ABI `rdi`;
2. `edx` loaded from `config+0x30`, where that config pointer came from the same owner `+0x9c8`, or a same-owner immediate;
3. virtual call through `+0x60` on that exact handler.

Accepted flow count: **0**.

```yaml
OWNER_PAIR_DIRECT_FLOW: UNKNOWN
FIELD6_VALUE_PROVEN: false
FIELD6_VALUE: UNKNOWN
TRACK_B_PAYLOAD_MUTATION_AUTHORIZED: false
OFFICIAL_SERVICE_GAME_E2E_AUTHORIZED: false
```

## Next boundary

Do not broaden this source task. A successor must first identify the exact RTTI/vtable type of the object stored at `owner+0x9c8` in the same constructor, then inspect only that object's owned methods / causal helpers for a transfer of its `+0x30` field into `TLoginProtocolMessageHandler::slot+0x60` producer `edx`. Do not revisit the eliminated worldmap scalar `edx=1` candidate and do not rank global `slot+0x60` calls.