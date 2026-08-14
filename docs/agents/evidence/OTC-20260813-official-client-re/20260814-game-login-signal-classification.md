# Official game-login Qt signal classification

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Correct the cross-track interpretation of `tibia::authentication::TLoginProtocolMessageHandler::sendLoginMessage` before Track B uses it as an oracle for the official 15.32 first game-login packet.

## Exact-client QMeta evidence — PROVEN

Exact-client workflow run `31652067802`, job `94298391194`, recovered this QMeta surface:

```text
class: tibia::authentication::TLoginProtocolMessageHandler
QMetaObject: 0x3084fa0
static metacall: 0xcf2aa0

sendLoginMessage:          0xcf2ca0   argc=1 flags=0x6
sendSecondaryLoginMessage: 0xcf2c50   argc=1 flags=0x6
```

The addresses and flags above are version-fenced to the exact executable hash named at the top of this report.

## Qt metadata interpretation — PROVEN FRAMEWORK SEMANTICS

Qt's QMetaObject method-flag definitions assign:

```text
AccessPublic = 0x02
MethodSignal = 0x04
```

Therefore QMeta flags `0x06` classify both `sendLoginMessage` and `sendSecondaryLoginMessage` as **public Qt signals**.

This interpretation is additionally consistent with earlier exact-client Track A evidence in `20260814-high-value-outbound-signal-disassembly.md`, where other high-value `send*` QMeta entries resolve to small signal-emission wrappers around `QMetaObject::activate` rather than their downstream protocol builders.

## Corrected claim boundary

### FACT

`TLoginProtocolMessageHandler::sendLoginMessage @ 0xcf2ca0` is an exact-version public Qt signal surface.

### DISPROVEN

The address `0xcf2ca0` by itself is **not** evidence that this function serializes or builds the official game-login packet.

### UNKNOWN

The following remain unknown until the signal connection is recovered and its receiver is analyzed:

- the concrete receiver/consumer of `sendLoginMessage`;
- the function that serializes the corresponding outbound login message;
- ordered public/pre-secret fields and widths;
- exact version representation on the game socket;
- asset identifier source/encoding/placement;
- preview-state presence/placement;
- RSA-block boundary;
- checksum/sequence/framing state for the first game-login message.

## Active recovery experiment

Track A commit `8ac9c72ee16427a8d79526184cb525f6a2114e8e` added:

`.github/workflows/tibia-official-client-re-login-signal-oracle.yml`

Push run `31816876078` is the bounded exact-SHA experiment for:

1. disassembling the two login signal wrappers;
2. checking for `QMetaObject::activate` behavior;
3. scanning direct/RIP/data references to the signal wrappers and login QMetaObject;
4. producing bounded neighborhoods that can identify where the login signal is wired to its consumer.

At the time this evidence was written, the `inspect` job was queued; no runtime or static result from that run is claimed yet.

## Cross-track promotion contract

Track B may consume the following immediately:

```yaml
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
login_message_qmeta: 0x3084fa0
send_login_message_signal: 0xcf2ca0
send_login_message_qmeta_flags: 0x06
classification: public_qt_signal
serializer_or_builder_address: UNKNOWN
```

Track B must not treat `0xcf2ca0` as the packet builder and must not infer a game-wire field layout from the signal name alone.

## Next action

Recover the exact signal-to-consumer connection for `sendLoginMessage`; then analyze the receiver function as the candidate outbound login serializer/builder. Promote only version-fenced, non-secret structural facts to Track B.
