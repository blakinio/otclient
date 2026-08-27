# Coordinator promotion — current game-login field provenance

Decision: **PASS_BOUNDED / ACCEPT_WITH_EDITS**.

This promotion was independently rebuilt from protected `main@faf3018d520f58ad7841cf3819b16ef159f27148` after source PR #722 completed a fresh exact-client static run. The coordinator re-downloaded artifact `9635892718` from run `33046520991`, independently verified its GitHub digest and its only `result.json`, and inspected the producer/getter instruction snapshots directly.

## Independent hashes

```text
source PR head        36320a5e024f1ffab70592be52404da351b16b27
workflow run          33046520991 = SUCCESS
workflow job          98431684189 = SUCCESS
artifact              9635892718
artifact sha256        fca8de5f33c1c80f57b80a7575a9f9eabf2664d7355c25275e02c2a479b49e62
result.json sha256     d4926050670959c78d3dc59d1fd3dff32ea328fbde0603c538ab43e3ea2510a7
```

Exact public Linux client fence remained `15.32.75d4a0`, packed `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`, unpacked `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, size `52105824`.

## Accepted structural provenance

The exact artifact independently re-derives `TAuthenticationAndEncryptionInfo` (`RTTI 0x30adc40`, vtable AP `0x2f82f98`) and `TLoginProtocolMessageHandler` (`RTTI 0x30b4ed0`, vtable AP `0x30b6700`). Handler slot `+0x60` remains the login producer `0xe25620`, FDE `0xe25620..0xe2656d`.

Direct producer dataflow proves the following **wire-field destinations without assigning user-facing meanings**:

```text
AuthInfo slot +0x30 -> LoginRSAEncryptedBlock field 1
AuthInfo slot +0x40 -> LoginRSAEncryptedBlock field 2
producer input +0x18 dword -> LoginRSAEncryptedBlock field 3
producer input +0x1c dword -> LoginRSAEncryptedBlock field 4
AuthInfo slot +0x18 -> LoginRSAEncryptedBlock field 5
AuthInfo slot +0x50 -> LoginRSAEncryptedBlock field 6
AuthInfo slot +0x60 -> LoginRSAEncryptedBlock field 7
AuthInfo slot +0x70 -> GameclientMessageLogin field 4
AuthInfo slot +0x80 -> GameclientMessageLogin field 5
```

This complements the already-trusted schema promotion (#719): the current official client uses a typed `GameclientMessageLogin` with nested `LoginRSAEncryptedBlock`, while Track B #284 still builds a legacy raw `ClientPendingGame` body. The body mismatch is therefore material and proven; the generic outer transport alignment remains unchanged from #706.

## Explicitly withheld

The source experiment that attempted to identify a selected-character Qt metadata name failed closed with `CHARACTER_SELECTION_QMETA_AMBIGUOUS=0`. That experiment is not part of the task's required evidence and is not promoted. No heuristic replacement is accepted.

The following remain `UNKNOWN` and **must not** be inferred from field order, nearby literals, legacy packet order, or intuition:

```yaml
user_facing_authinfo_field_names: UNKNOWN
password_session_to_specific_rsa_field_mapping: UNKNOWN
selected_character_semantic_name_for_slot_0x18_path: UNKNOWN
track_b_safe_semantic_mapping: INSUFFICIENT
```

Therefore this promotion authorizes Track B to consume only the structural fact that its existing login body is stale and the exact source-slot-to-wire-field relationships above. It does **not** authorize a secret-bearing E2E or a guessed current native login body.

## Safety

The producer run was static only: no official-client execution, login, credentials/session values, process memory, network capture, gameplay, or proprietary binary upload. Source workflow/analyzer files from #722 remain source-only and are not promoted.
