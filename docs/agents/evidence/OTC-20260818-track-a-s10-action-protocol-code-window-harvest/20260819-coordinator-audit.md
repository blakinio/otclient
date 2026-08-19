# Track A S10 — coordinator independent documentation audit

```yaml
task: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
source_pr: 539
source_head: ac34c2f906e834ace414f8c8d8fa75a150b4b65a
coordinator_review: 4970899448
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: 5ce628b7e565eb17876b76305af6a6086ed7f258
runtime_access: none
physical_e2e_required: false
```

## Audit method

The coordinator independently re-read the original retained historical exact-build evidence from branch `ci/OTC-20260814-track-a-single-item-drag` rather than accepting the source PR summary by authority.

Audited primary evidence:

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-high-value-outbound-signal-disassembly.md`, blob `3ff5db3a5a81e94e35492376d6b11b1e59f5ed70`;
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-connectimpl-arguments.md`, blob `5ae3752e056a9e2e4b997730fada5d4aa9a510e6`;
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-slot-provenance.md`, blob `95dd260c9fe0f94650cc2bd1dc25350973e1010b`;
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md`, blob `983752615ccecb9423f1201507616c2adcc82c28`.

All executable addresses in this S10 package remain fenced to the historical official Linux client only:

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

They are not current-build offsets. Current exact-client addresses must be rediscovered under the current `52109920 / ed5469...` fence.

## H1 — sender wrapper

Independent source evidence directly establishes:

```text
TContainerGameActionHandler
static metaobject       0x30850a0
qt_static_metacall      0xd1dac0
sendMoveObject case     0xd1df30
QMeta signal index      1
behavior                loads argument and calls QMetaObject::activate
```

Classification: `H1_MOVEOBJECT_SENDER=PROVEN_HISTORICAL_EXACT_BUILD`.

The wrapper is a Qt signal emitter, not a protocol serializer.

## H2 — exact action-specific connect edge

The corrected `QObject::connectImpl` evidence establishes a Container sender-metaobject site at `0x7ffb24` with exact sender static metaobject `0x30850a0`. Slot-object payload recovery establishes direct target `0x8332d0`, adjustment zero; later exact QMeta/disassembly identifies that target as `tibia::game::TInternalGameActionRouter`, a router/re-emitter rather than a serializer.

However, the original corrected connect reconstruction explicitly says source expressions do **not** establish pointer-to-member signal indices. Therefore it does not establish:

```text
0x7ffb24 == TContainerGameActionHandler::sendMoveObject signal index 1
```

The other nearby Container site `0x7d7307` is also insufficient: in the bounded window the Container metaobject is on the receiver side and the sender metaobject is unresolved.

Accepted classification:

```yaml
TContainerGameActionHandler_some_signal_to_TInternalGameActionRouter: PROVEN_HISTORICAL_EXACT_BUILD
TContainerGameActionHandler_sendMoveObject_signal_1_to_that_connect_site: UNKNOWN
H2_ACTION_SPECIFIC_CONNECT_EDGE: UNKNOWN
```

This is a genuine missing retained proof window, not negative evidence that the connection does not exist.

## H3 — protocol owner / move-object builder

Independent retained evidence directly establishes:

```text
tibia::protocol::TProtocolMessageQueue
static metaobject                0x3085b60
QMeta index 218                  sendMoveObject
case entry                       0xdf6d58
concrete builder body            0xbd3be0
internal Gameclient discriminator 0x78
```

The retained builder evidence proves allocation/initialisation, typed payload setup, action-parameter copying and submission. The `0x78` value is an internal `GameclientMessage` discriminator only; it is **not** a proven final wire opcode/byte.

Classification: `H3_PROTOCOL_OWNER_AND_MOVEOBJECT_BUILDER=PROVEN_HISTORICAL_EXACT_BUILD`.

## Causal boundary

Direct evidence therefore supports only:

```text
TContainerGameActionHandler::sendMoveObject signal index 1    PROVEN
TContainerGameActionHandler::<some signal>
  -> TInternalGameActionRouter                                PROVEN
TProtocolMessageQueue::sendMoveObject
  -> builder 0xbd3be0 / internal discriminator 0x78          PROVEN
```

The retained corpus does not directly prove the action-identity-preserving edge from the specific `sendMoveObject` signal to the router/queue `sendMoveObject` path. Joining those fragments would be an inference and is not promoted.

Correct fail-closed S10 result:

```yaml
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
S10_RESULT: BLOCKED_MISSING_RETAINED_CODE_WINDOW
CURRENT_BUILD_OFFSETS: UNKNOWN
RUNTIME_EFFECT_BY_S10: NOT_OBSERVED
```

## Validation / safety

Source exact head `ac34c2f906e834ace414f8c8d8fa75a150b4b65a` has green CI `32195602147`, green Track A governance `32195543092`, and zero review threads. It is 19 commits behind coordinator-start current main and therefore is not directly merged.

No official-client execution, credentials, login, gameplay, process-memory access, GUI input or runtime mutation occurred in this coordinator audit. E2E is `NOT_APPLICABLE` for this retained-evidence documentation slice.
