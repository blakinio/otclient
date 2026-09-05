# Official 15.32 game-login oracle evidence for Track B

Track: `otclient-global-login` / `OTCLIENT-GLOBAL-LOGIN`
Repository: `blakinio/otclient`
Canonical PR: `#284`
Track B branch: `feat/OTC-20260813-tibia-global-login-lab`
Evidence date: 2026-08-14

## Scope and isolation

This report consumes only repository-owned, read-only, exact-version evidence promoted from Track A (`official-client-re` / `OTCLIENT-TIBIA-RE`) under `docs/agents/TIBIA_RESEARCH_TRACKS.md`.

No Track A mutable runtime, process, container, display, state directory, credential, session value or proprietary payload is shared with Track B. Static addresses are version-fenced to one exact executable and must not be reused against another SHA.

## Exact executable identity — PROVEN

Track A and Track B study compatibility against the same verified official Linux executable:

```text
package/client cut: 15.32.df7b29
executable sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed client sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

Canonical Track A provenance includes:

- `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`;
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-game-login-signal-classification.md`;
- exact-client hosted/static workflow evidence on Track A.

## Client-version identity boundary — PROVEN

Track A workflow `tibia-official-login-request-string-map.yml`, run `31647667024`, job `94284870421`, reverified the exact executable SHA and established two distinct version representations:

```text
binary literal: 15.32
package.json version: 15.32.df7b29
```

Track B independently proved successful HTTPS authentication using the full `15.32.df7b29` HTTP identity.

`15.32.df7b29` is therefore proven as package/HTTPS-login identity for this cut. It remains **UNKNOWN** whether the official game-server login serializes `15.32.df7b29`, `15.32`, numeric `1532`, more than one representation, or another derived value.

## Track B server-side boundary — PROVEN

Track B has crossed transport reachability and obtained a structured rejection from the official game endpoint.

Run `31702087216`, job `94453443371`, exact head `76d30527c718650dd50316140847f07154449342` established:

```text
CLIENT_VERSION_VALUE=1532
PROTOCOL_VERSION_VALUE=1532
SESSION_KEY_FEATURE=true
LAB_GAME_FORWARD_CLIENT_LENGTH=230
LAB_GAME_FORWARD_SERVER_LENGTH=148
GAME_LOGIN_ERROR=true
```

Run `31706716385`, job `94469029667`, exact head `0ee27024357913cfe4d0fca2214a609b86339b01`, structurally identified server opcode `20` (`0x14`, game-login error). The safe relationship classifier emitted `client+world=true`.

This proves the current OTClient packet reaches the official game server and is parsed far enough to produce a client/world compatibility rejection. It does not identify the incorrect field or framing rule.

## Current OTClient first-packet structure — DIRECT SOURCE INSPECTION

`src/client/protocolgamesend.cpp::ProtocolGame::sendLoginPacket()` currently builds the first login message from conditional field families including:

1. pending-game opcode/state;
2. OS identifier;
3. protocol version;
4. numeric client version when enabled;
5. post-1281 game-login version string;
6. asset identifier for modern versions;
7. preview-state byte when enabled;
8. RSA/XTEA login block containing protected session/character material and optional challenge fields;
9. checksum/XTEA/sequenced framing according to active features.

This is the implementation to compare with the official-client serializer once its structural contract is recovered. Legacy OTClient field presence/order is not evidence of the official 15.32 contract.

## Official login QMeta surface — CORRECTED PROVEN CLASSIFICATION

Exact-client Track A evidence resolves:

```text
class: tibia::authentication::TLoginProtocolMessageHandler
QMetaObject: 0x3084fa0
static metacall: 0xcf2aa0

sendLoginMessage:          InvokeMetaMethod case 0xcf2ca0, argc=1, flags=0x6
sendSecondaryLoginMessage: InvokeMetaMethod case 0xcf2c50, argc=1, flags=0x6
```

QMeta flags `0x06` classify both as public Qt signals (`AccessPublic | MethodSignal`). The `0xcf2cxx` locations are generated `qt_static_metacall` case entries, not packet serializers.

## Exact signal PMF and consumer map — PROVEN

Track A exact-SHA run `31820653663`, job `94832832975`, on `synology-otclient-01` disassembled both the signal functions and the `IndexOfMethod` path in `qt_static_metacall`.

```text
0xcf2950 -> signal index 0 = sendLoginMessage
0xcf2980 -> signal index 1 = sendSecondaryLoginMessage
```

The exact connection setup proves:

```text
sendLoginMessage
  signal PMF:       0xcf2950
  connectImpl call: 0x7d564f
  QSlotObject invoke trampoline: 0x7d4220
  captured slot PMF target: 0xbd36a0
  receiver source: enclosing object + 0x88

sendSecondaryLoginMessage
  signal PMF:       0xcf2980
  connectImpl call: 0x7d56e7
  QSlotObject invoke trampoline: 0x7d4190
  captured slot PMF target: 0xbf3990
```

The corrected SysV `QObject::connectImpl` mapping includes the hidden `QMetaObject::Connection` structure-return argument:

```text
rdi hidden return storage
rsi sender
rdx signal PMF storage
rcx receiver
r8 slot PMF storage
r9 QSlotObjectBase*
stack connection type / types / sender QMetaObject
```

## Primary slot-target adapter — PROVEN

Track A exact-SHA run `31821003485`, job `94833872467`, completed successfully and structurally analyzed `0xbd36a0`.

`0xbd36a0` is an adapter/delegator, not a proven final wire serializer. It allocates and initializes a `0x50`-byte intermediate object, structurally reads fields from the signal argument, then invokes a virtual function on the primary receiver:

```asm
0xbd37f3: mov rax,QWORD PTR [r12]
0xbd37f7: mov rax,QWORD PTR [rax+0x68]
...
0xbd381e: mov rdi,r12
0xbd3821: call rax
```

At entry the receiver is retained in `r12`, therefore the next exact target is:

```text
receiver_vptr = *(receiver)
next_target = *(receiver_vptr + 0x68)
```

Additional structural facts from the adapter:

```text
intermediate allocation size: 0x50
signal-argument flags tested at +0x10: 0x1, 0x2, 0x4
signal-argument offsets accessed: +0x18, +0x20, +0x28, +0x30
intermediate +0x38 OR=0x2
intermediate +0x48 = 0x0a
```

No protocol semantics are assigned to these offsets/flags yet.

### Claim boundary

**PROVEN:** `sendLoginMessage` reaches `0xbd36a0`, which delegates through primary `receiver->vtable[+0x68]`.

**DISPROVEN:** `0xcf2ca0`, `0x7d4220`, or `0xbd36a0` has been proven to be the final game-wire serializer.

**UNKNOWN:** exact receiver class/vptr, exact function address at `vtable+0x68`, and whether that next target serializes directly or delegates further.

## Useful surrounding login transitions — PROVEN

```text
TAuthenticationProcessController::requestCharacterGameserverLogin    0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered 0xcfb122
TCharacterSelectionController::requestCharacterLogin                 0xd47300
TGameClient::connectClientToGameserverWithExistingCredentials        0xd06660
TGameClient::onConnectClientToGameserver                              0xd06810
TGameClient::onGameSessionConnected                                   0xd066e0
TGameserverLoginProcessController::onGameserverTCPConnectionConnected 0xcfa0e0
```

## Cross-track conclusion

### FACT

- Track B HTTPS login/session handoff/WARP/game-endpoint reachability are proven.
- The official game endpoint returns `0x14` after receiving the current 230-byte Track B first packet.
- `15.32.df7b29` is proven for package/HTTPS identity; exact game-wire version representation remains unknown.
- exact official path is now `sendLoginMessage PMF 0xcf2950 -> connect 0x7d564f -> slot target 0xbd36a0 -> receiver virtual slot +0x68`.

### INFERENCE

The shortest path to the Track B `0x14` root cause is to resolve the exact primary receiver vptr and function stored at `vptr+0x68`, follow that target to the real outbound writer, and only then derive the public field contract.

### UNKNOWN

- exact primary receiver class/vptr;
- exact `vtable+0x68` function target;
- ordered public/pre-secret wire fields and widths;
- exact game-socket version representation;
- asset identifier placement;
- RSA boundary;
- checksum/sequence/framing state.

No credential, session key, character name, world host or secret-bearing packet payload needs to be persisted to answer these structural questions.

## Track B decision and next action

1. Preserve `FULL_CLIENT_VERSION_CALL_FAILED` as a local defect, but do not prioritize it as root cause while game-wire version representation is unknown.
2. Do not spend another official-service E2E solely on `15.32.df7b29`.
3. Resolve Track A primary receiver vptr and `*(vptr+0x68)` using an exact-SHA non-secret structural probe or statically proven vtable mapping.
4. Disassemble that target and follow it until the actual outbound serializer/writer boundary is proven.
5. Compare the resulting official public field contract with `ProtocolGame::sendLoginPacket()`.
6. Implement only the first proven semantic/layout delta, add a focused test, then perform one bounded Track B E2E looking for advancement beyond opcode `0x14`.

## Evidence quality

This report stops at the strongest verified boundary. It does not infer packet bytes or secret-bearing payload semantics from class names, static addresses, HTTP fields or server error text.
## 2026-08-23 current-build supplement

The historical oracle above remains exact for `15.32.df7b29 / e6c244...`; its addresses are not reused for the current client.

Fresh owner-hosted package metadata exactly binds current package `15.32.bf29ac` to packed client `1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354`, unpacked client `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, size `52109920`. Those hashes match the current Track A fence already promoted on trusted main.

Later merged Track A promotion #589 adds historical exact-build structural proof that:

```text
TLoginProtocolMessageHandler
  -> GameclientMessageLogin
  -> nested LoginRSAEncryptedBlock at field 7
  -> TProtocolMessageQueue::sendLogin(GameclientMessageLogin)
```

The protobuf tag/types and nested object shape are proven internally. The final `TProtocolMessageQueue` queue/wire serializer remains unproven, so this evidence does **not** authorize treating the internal protobuf encoding as the raw TCP first packet.

Track B consequence: drop the failed `g_gameConfig` full-build-string game-wire experiment, keep the already network-reaching numeric 1532 login packet as the baseline, refresh current public package identity/assets, and spend at most one fresh E2E attempt on that materially changed input generation. If the server still returns structured `0x14`, the next dependency is a promoted final writer/wire contract rather than another blind feature or version toggle.
