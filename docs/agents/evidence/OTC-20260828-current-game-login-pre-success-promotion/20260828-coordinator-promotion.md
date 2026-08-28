# Coordinator promotion — current game-login pre-success outbound

Decision: **PASS_BOUNDED_NO_IMPLEMENTABLE_VALUE_DELTA**.

This clean promotion is reconstructed from fresh trusted `main@e7f710b04da8c6f3adae43a019c44a6acb4a2866` and frozen source Draft PR #743. The source analyzer/workflow is not promoted.

## Exact evidence

```text
source PR             #743
source head           1342423c6fe4ef675f4b0b0cdc39ae012089f20e
source workflow       33159660190 = SUCCESS
source job            98810772742 = SUCCESS
source CI             33159660423 = SUCCESS
source governance     33159660171 = SUCCESS
artifact              9681208967
artifact sha256       c3fabb53fb82d1f466a82c508bfb1be9502061dc9e96737e0f33171a8415247c
result.json sha256    1c1748bbcd0cfe3410111ac3eb3f70563d6695d858cf007e8d07263adf1a472f
```

Exact public Linux client remains `15.32.75d4a0`, SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, size `52105824`. Analysis was static only; the official client was never executed and no login, secret, process-memory access, packet capture or raw-client upload occurred.

## Accepted producer facts

The exact primary `TLoginProtocolMessageHandler` producer remains slot `+0x60 -> 0xe25620`, FDE `0xe25620..0xe2656d`. The current `GameclientMessageLogin` object constructed on this path writes outer fields `1`, `2`, `3` and **`6`**. Field 6 is written at `0xe25ccc` from `r14d`; CFG-aware reaching-definition analysis binds `r14d` to producer input `edx` through `mov r14d, edx @ 0xe25624`.

This proves that outer field 6 is structurally present in the native producer, but it does **not** prove the runtime value passed in `edx` or a user-facing semantic name. The value therefore remains `UNKNOWN_CURRENT_EXACT`.

The same primary producer references retained AuthInfo sources for nested `LoginRSAEncryptedBlock` fields `1`, `2`, `5`, `6` and `7` through slots `+0x30`, `+0x40`, `+0x18`, `+0x50`, `+0x60`. Nested field 2 is conditionally omitted on one proved producer branch. Source-reference presence does not prove a non-empty runtime string or a semantic field name.

## Exhausted bounded callsite discriminators

The source task intentionally stopped rather than escalating heuristics:

```text
producer direct call refs                         0
producer RIP refs                                 0
bounded auth-start direct graph slot+0x60 calls  0
exact handler owner field                         +0x9c0
owner-field refs                                  41
owner-field -> slot+0x60 calls                    0
exact handler constructor FDE                     0x7d15c0..0x7d1a8a
Qt handler connections                            5
bounded connection-thunk -> slot+0x60 calls       0
```

The global `+0x60` census produced hundreds of unrelated virtual calls and is not a valid semantic discriminator. It is not used to manufacture an `edx` value.

## Track B consequence

PR #284's current typed encoder omits outer `GameclientMessageLogin.field6`, but the exact value needed for that field is still not proven. Adding a guessed constant, copying an unrelated platform-like value, or synthesizing nested fields `1/2/6/7` would violate the fail-closed contract.

Therefore this promotion **does not authorize a Track B payload mutation or another official-service game E2E**. The precise next blocker is:

```text
CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
```

A future task needs a stronger causal source for the actual `edx` value (or equivalent exact-current semantic producer evidence). Until then, #284 remains blocked before any additional secret-bearing game attempt.
