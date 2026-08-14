# Official game-login Qt signal classification

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Purpose

Recover the exact Qt signal-to-consumer path for the official 15.32 game-login message before Track B uses the official client as a protocol oracle.

## Exact-client QMeta evidence — PROVEN

Exact-client workflow run `31652067802`, job `94298391194`, recovered this QMeta surface:

```text
class: tibia::authentication::TLoginProtocolMessageHandler
QMetaObject: 0x3084fa0
static metacall: 0xcf2aa0

sendLoginMessage:          InvokeMetaMethod case entry 0xcf2ca0   argc=1 flags=0x6
sendSecondaryLoginMessage: InvokeMetaMethod case entry 0xcf2c50   argc=1 flags=0x6
```

Qt QMeta flags `0x06` are `AccessPublic (0x02) | MethodSignal (0x04)`, so both are public Qt signals. The `0xcf2cxx` addresses above are case entries inside the generated static metacall path; they are not packet serializers.

## Exact signal PMF identity — PROVEN

Exact-SHA workflow run `31820653663`, job `94832832975`, on `synology-otclient-01` disassembled `qt_static_metacall` and the signal functions themselves.

The `IndexOfMethod` path compares the supplied pointer-to-member against the exact signal functions and writes the corresponding QMeta method index:

```text
PMF 0xcf2950 -> method/signal index 0
PMF 0xcf2980 -> method/signal index 1
PMF 0xcf29b0 -> method/signal index 2
PMF 0xcf29d0 -> method/signal index 3
PMF 0xcf2a10 -> method/signal index 4
PMF 0xcf2a50 -> method/signal index 5
PMF 0xcf2a80 -> method/signal index 6
```

The functions also directly confirm their signal indices through `QMetaObject::activate`:

```text
0xcf2950 -> QMetaObject::activate(..., signal_index=0, ...)
0xcf2980 -> QMetaObject::activate(..., signal_index=1, ...)
```

Combining that result with the previously recovered QMeta method order proves:

```text
sendLoginMessage          -> signal PMF 0xcf2950
sendSecondaryLoginMessage -> signal PMF 0xcf2980
```

## QObject::connect ABI correction — PROVEN

The earlier register labels around `QObject::connectImpl` omitted the hidden structure-return argument for `QMetaObject::Connection`. With the SysV hidden `sret` accounted for, the exact call-site mapping is:

```text
rdi   hidden QMetaObject::Connection return storage
rsi   sender
rdx   signal PMF storage
rcx   receiver
r8    slot PMF storage
r9    QSlotObjectBase*
stack connection type / types / sender QMetaObject
```

This corrected interpretation supersedes older provisional register labels from the first consumer scan.

## Primary and secondary consumer paths — PROVEN

The focused connect provenance plus the PMF map now prove the following exact-version paths:

```text
sendLoginMessage
  QMeta index:      0
  signal PMF:       0xcf2950
  connectImpl call: 0x7d564f
  QSlotObject invoke trampoline: 0x7d4220
  slot PMF target:  0xbd36a0

sendSecondaryLoginMessage
  QMeta index:      1
  signal PMF:       0xcf2980
  connectImpl call: 0x7d56e7
  QSlotObject invoke trampoline: 0x7d4190
  slot PMF target:  0xbf3990
```

At the primary connect setup, the binary materializes `0xbd36a0` into the slot-PMF storage and `0xcf2950` into the signal-PMF storage before `QObject::connectImpl`. The secondary connect similarly materializes `0xbf3990` and `0xcf2980`.

The `0x7d42xx`/`0x7d41xx` functions are Qt slot-object management/invocation trampolines. The semantically relevant receiver candidate is therefore the captured slot PMF target, not the trampoline.

## Corrected claim boundary

### FACT

- `sendLoginMessage` is QMeta signal index 0.
- its actual signal PMF is `0xcf2950`.
- it is connected through `connectImpl @ 0x7d564f`.
- the connection captures real slot PMF target `0xbd36a0`.
- `0xcf2ca0` is an InvokeMetaMethod case entry for signal index 0, not a proven serializer.

### DISPROVEN

- `0xcf2ca0` is the official game-login packet builder.
- the `0x7d4220` QSlotObject trampoline itself is the semantic packet serializer.

### UNKNOWN

Until `0xbd36a0` and its downstream calls are structurally analyzed, these remain unknown:

- whether `0xbd36a0` directly serializes the packet or delegates to another function;
- ordered public/pre-secret fields and widths;
- exact game-socket version representation;
- asset identifier source/encoding/placement;
- preview-state presence/placement;
- RSA-block boundary;
- checksum/sequence/framing state for the first game-login message.

## Active receiver-target experiment

Track A commit `ba89cb8affc8106974ae1054cb8c3c648bbabf2b` adds:

`.github/workflows/tibia-official-client-re-login-slot-target.yml`

Run `31821003485` is the exact-SHA bounded analysis of:

- primary slot PMF target `0xbd36a0`;
- secondary control target `0xbf3990`;
- their direct call graph neighborhoods and non-secret static references.

No result from that run is promoted here until it completes successfully and is inspected.

## Cross-track promotion contract

Track B may consume this immediately:

```yaml
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
login_message_qmeta: 0x3084fa0
send_login_message_qmeta_index: 0
send_login_message_signal_pmf: 0xcf2950
send_login_message_static_metacall_case: 0xcf2ca0
send_login_message_connect_call: 0x7d564f
send_login_message_slot_invoker: 0x7d4220
send_login_message_slot_target: 0xbd36a0
serializer_or_builder_address: UNKNOWN
```

Track B must not infer field layout from names or offsets alone. The next promotable protocol contract must come from structural analysis of `0xbd36a0` and its downstream callees.

## Next action

Analyze `0xbd36a0` as the exact primary receiver candidate, follow its outbound serialization/send callees, derive only non-secret version-fenced structural fields, and then compare that contract field-by-field with Track B `ProtocolGame::sendLoginPacket()`.