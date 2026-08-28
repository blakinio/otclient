# Coordinator promotion — current Gameserver dispatch envelope

Decision: **PASS_BOUNDED**.

This promotion was independently reconstructed from trusted `main@470d5bd285e29f9d3f24f70ff3fc5370e2990e2a` and the final exact-current source run for Draft PR #737. The source workflow/analyzer is not promoted.

## Primary evidence identity

```text
source PR             #737 (Draft, source-only)
source head           5273d52e0fdd3f0e2c212f633fb8e406409851ff
producer run          33152704802 = SUCCESS
producer job          98788182962 = SUCCESS
artifact              9678356574
artifact sha256        9bb4f18d2d684b4a7a0f5c9254367fdfc9786c633890b2beb5fe324c421aa918
re-downloaded ZIP      sha256:9bb4f18d2d684b4a7a0f5c9254367fdfc9786c633890b2beb5fe324c421aa918
result.json            sha256:eabcb9445cdafd699fb266ee94b4aca9a1b006170007cbefe682b7a6579d3764
```

The exact public Linux client fence remained:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Safety remained static-only: `runtime_access=none`, `login_performed=false`, `secret_access=false`, `process_memory_access=false`, `raw_client_uploaded=false`. The exact client was transient and deleted before artifact upload.

## Accepted dispatch controls

The exact-current parser FDE is `0xb84cd0..0xb8795e`; it reads a one-byte dispatch ID and uses a recovered table at `0x1d6f058`, indexed from base ID `3`.

Independent controls recover the expected exact-current login types:

```text
0x14 -> GameserverMessageLoginError
0x17 -> GameserverMessageLoginSuccess
0x1f -> GameserverMessageLoginChallenge
```

These controls establish that the resolver is reading the real current `GameserverMessage*` dispatch machinery rather than an unrelated byte switch.

## Accepted 0x34 boundary

For dispatch ID `0x34` (decimal 52), the exact-current table target is `0xb84ddf`. Unlike the concrete login cases, that target does not bind a concrete `GameserverMessage*` metadata type. The bounded classification is therefore:

```yaml
CURRENT_GAMESERVER_DISPATCH_0x34: UNKNOWN_FALLBACK
CURRENT_GAMESERVER_DISPATCH_0x34_CONCRETE_TYPE: NOT_PRESENT
```

This is materially different from Track B's legacy opcode interpretation, where decimal 52 is treated as a normal OTClient game opcode. The exact official client does **not** classify this first byte as `GameserverMessageLoginSuccess`, `GameserverMessageLoginError`, or `GameserverMessageLoginChallenge`.

## Track B consequence

Track B run `33150944475` / job `98782709382` proved the first decrypted application payload is exactly four bytes and begins with decimal `52` (`0x34`). The exact official-client result now proves that byte belongs to the current fallback dispatch path, not to Track B's legacy opcode meaning and not to a direct protobuf key.

The next Track B change may therefore prevent current 15.32 Global from feeding `0x34` into the legacy opcode handler. It must fail closed: consume only the current packet's already-bounded unread bytes as opaque fallback data and continue receiving; do not invent a `GameserverMessage*` semantic type or parse the remaining three bytes as legacy fields. A subsequent official-service E2E is allowed only after that material parser change and the existing one-shot gates.

## Still withheld

```yaml
CURRENT_GAMESERVER_DISPATCH_0x34_USER_FACING_MEANING: UNKNOWN
CURRENT_GAMESERVER_DISPATCH_0x34_PAYLOAD_FIELD_SCHEMA: UNKNOWN
CURRENT_GAMESERVER_DISPATCH_0x34_DOWNSTREAM_SEMANTIC_CALLBACK: UNKNOWN
CURRENT_GAMESERVER_DISPATCH_0x34_IS_LOGIN_SUCCESS: DISPROVEN
CURRENT_GAMESERVER_DISPATCH_0x34_IS_LOGIN_ERROR: DISPROVEN
CURRENT_GAMESERVER_DISPATCH_0x34_IS_LOGIN_CHALLENGE: DISPROVEN
```

No semantic label is invented for the fallback. Track B may only use the structural consequence: do not reinterpret this current fallback as the legacy opcode-52 payload.