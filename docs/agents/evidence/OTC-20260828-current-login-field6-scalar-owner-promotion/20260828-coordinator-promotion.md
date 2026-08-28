# Coordinator promotion — current login field6 scalar-owner boundary

Decision: **PASS_BOUNDED_STATIC_VALUE_STILL_UNKNOWN**.

This promotion was reconstructed from trusted `main@7a7a7cc4d09dee08ea07f8c91144d8ac869111b7` and source-only Draft PR #751. The source analyzers/workflows are not promoted.

## Evidence identity

```text
source PR                    #751
source final head            a50a140cbdf4038921ed29e30cf0f53f8158bc27
independent scalar run       33171560068 / job 98849712747 = SUCCESS
scalar artifact              9686096894
scalar artifact sha256       b24572d2e232458826445bd8f405c89e36a313e90fc1134c0121783923b4e314
scalar result.json sha256    3b1344b06b280457e3ff4d42ee9d2bcd5b455e5862e36d53fec1deb496ac1715
focused final run            33174706577 / job 98860195057 = SUCCESS
focused artifact             9687275655
focused artifact sha256      136dc08adef86f742f44a5c71fdb6ff3ccf7f7a2e856336ba26ed051526e722c
focused result.json sha256   9c0537ee03d8afaf62bb78a7c567b54e712448a1411da7f7d6c8f29036078b0a
source CI                    33174706753 = SUCCESS
source Track A governance    33174706531 = SUCCESS
```

The exact public Linux client fence remains `15.32.75d4a0`, SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, size `52105824`. Both source runs were static-only; the official client was never executed and no credentials, session material, process memory, packet payloads or proprietary client bytes were retained.

## Scalar census conclusion

The independent clean successor source re-derived exactly three `call [vtable+0x60]` sites with a CFG-proven scalar value in `edx`:

```text
0xaa5132  edx=0  -> REJECTED_ABI_RECEIVER_MISMATCH
0xceddcb  edx=1  -> initially viable receiver=this+0x10
0x16da716 edx=0  -> REJECTED_PARENT_NOT_ENTRY_THIS
```

The focused final run then freshly re-asserted the exact current instructions around `0xceddcb`:

```text
0xcedd9f  mov r12, rdi
0xceddbb  mov rdi, qword ptr [r12 + 0x10]
0xceddc0  mov edx, 1
0xceddc8  mov rax, qword ptr [rdi]
0xceddcb  call qword ptr [rax + 0x60]
```

That candidate is **not** a current login-handler call. Exact-current QMeta ownership binds all four direct edges into FDE `0xcedd90..0xcee0ec` to `tibia::worldmap::TWorldmapProtocolMessageHandler`, specifically the left/right column and top/bottom row message handlers. The value `1` is therefore a worldmap-path scalar and must not be promoted into `GameclientMessageLogin.field6`.

This closes the bounded static scalar route: no statically scalar `+0x60` candidate is causally bound to trusted-main `TLoginProtocolMessageHandler::slot+0x60 -> 0xe25620`.

## Track B consequence

Trusted main already proves the native primary login producer writes outer `GameclientMessageLogin.field6` from its input `edx`. PR #284 still omits that outer field, but this source work **does not prove its runtime value**.

Therefore:

```yaml
CURRENT_GAME_LOGIN_FIELD6_VALUE: UNKNOWN_CURRENT_EXACT
TRACK_B_FIELD6_MUTATION_AUTHORIZED: false
TRACK_B_GAME_E2E_AUTHORIZED: false
NEXT_BLOCKER: CURRENT_GAME_LOGIN_FIELD6_RUNTIME_VALUE_OBSERVATION_REQUIRED
```

Do not infer `0`, `1`, a legacy preview byte, a platform value, or another semantic label from frequency or structural similarity. The next admissible evidence source is a separately governed, read-only runtime observation of only the producer input scalar `edx` at exact current `0xe25620`, under fresh Track A runtime admission. No credentials, session values or packet payload bytes are needed for that observation.
