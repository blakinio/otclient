# OTCLIENT Track A — S10 action-to-protocol retained code-window harvest

Date: 2026-08-19  
Task: `OTC-20260818-track-a-s10-action-protocol-code-window-harvest`  
PR: `#539`  
Trusted S9 base: `main@ebbb36f50076ff4072c7218e302614c1dfea00b1`  
Live main observed during S10: `a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb`  
Execution: GitHub repository evidence only, `runtime_access: none`

## Result

```yaml
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
S10_RESULT: BLOCKED_MISSING_RETAINED_CODE_WINDOW
H1_MOVEOBJECT_SENDER: PROVEN_HISTORICAL_EXACT_BUILD
H2_ACTION_SPECIFIC_CONNECT_EDGE: UNKNOWN
H3_PROTOCOL_OWNER_AND_MOVEOBJECT_BUILDER: PROVEN_HISTORICAL_EXACT_BUILD
CURRENT_BUILD_OFFSETS: UNKNOWN
RUNTIME_EFFECT_BY_S10: NOT_OBSERVED
```

S10 recovered strong direct historical evidence on both sides of the requested boundary, but the retained exact-build corpus does not contain the action-specific connect/dataflow window required to join them without inference. Per the pre-declared fail-closed contract, the retained discriminator terminates as `BLOCKED_MISSING_RETAINED_CODE_WINDOW`.

This is not evidence that the action-to-protocol connection does not exist.

## Exact historical client fence

Every executable address in this report is fenced to the previously researched official native Linux client:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Historical addresses are not current-client offsets. S10 did not acquire or execute the current client; PR #528 owns that lane.

## H1 — `TContainerGameActionHandler::sendMoveObject`

**FACT — directly retained.**

Source:

`ci/OTC-20260814-track-a-single-item-drag:docs/agents/evidence/OTC-20260813-official-client-re/20260814-high-value-outbound-signal-disassembly.md`

Recovered exact-build mapping:

```text
TContainerGameActionHandler
static metaobject: 0x30850a0
qt_static_metacall: 0xd1dac0
sendMoveObject case: 0xd1df30
signal index: 1
behavior: load argument -> QMetaObject::activate -> return
```

The function is a Qt signal-emission wrapper, not a protocol serializer.

Provenance recorded by the retained evidence:

```text
run 31793188185
job 94744455372
head 1c4ef6b612220e24cb312dfa6fce032b5c13d484
```

## H2 — Qt receiver/route reconstruction

**FACT — one Container sender connection reaches `TInternalGameActionRouter`.**

Sources:

- `20260814-gameaction-connectimpl-arguments.md`
- `20260814-gameaction-slot-provenance.md`
- `experiments/EXP-20260814-gameaction-connectimpl-correlation.yaml`

At connect site `0x7ffb24` the sender static metaobject is exactly `0x30850a0` (`TContainerGameActionHandler`). Slot payload recovery gives direct target `0x8332d0`, adjustment `0`. Subsequent QMeta/disassembly identifies that target as `tibia::game::TInternalGameActionRouter`, an internal action router/re-emitter rather than a serializer.

Relevant historical provenance:

```text
connect correlation: run 31800490781 / job 94767068361
corrected connect arguments: run 31801334150 / job 94769784890
slot provenance: run 31801723690 / job 94771021150
slot payloads: run 31802254026 / job 94772727592
router receiver: run 31802346130
router QMeta decode: run 31802470787 / job 94773438804
```

**UNKNOWN — the retained window does not identify which Container signal/member this connection represents.**

The corrected connect reconstruction explicitly leaves pointer-to-member signal indices unproven for the proven sender-metaobject sites. Therefore the following promotion is not allowed:

```text
0x7ffb24 == TContainerGameActionHandler::sendMoveObject signal index 1
```

The other nearby Container site `0x7d7307` also fails to close the gap: within the bounded reconstruction the Container metaobject is on the receiver side while the pushed sender metaobject remains unresolved.

Classification:

```yaml
TContainerGameActionHandler_some_signal_to_TInternalGameActionRouter: PROVEN
TContainerGameActionHandler_sendMoveObject_signal_1_to_TInternalGameActionRouter: UNKNOWN
```

## H3 — exact protocol owner and MoveObject producer

**FACT — independently retained.**

Source:

`ci/OTC-20260814-track-a-single-item-drag:docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md`

Exact historical mapping:

```text
tibia::protocol::TProtocolMessageQueue
static metaobject: 0x3085b60
QMeta index 218: sendMoveObject
case entry: 0xdf6d58
concrete builder body: 0xbd3be0
internal GameclientMessage discriminator: 0x78
```

Builder disassembly proves message allocation/initialisation, typed payload preparation, argument copying and submission. `0x78` is an internal `GameclientMessage` discriminator only; it is not a proven final wire byte/opcode.

Provenance:

```text
QMeta decode: run 31802808290 / job 94774542787
action dispatch: run 31802935253 / job 94774953120
builder disassembly: run 31803012968 / job 94775199763
convergence: run 31803088165 / job 94775445667
```

## Fallback retained sources

S10 also inspected the bounded fallback branches declared before execution:

```text
ci/OTC-20260814-track-a-final-write-continuation
ci/OTC-20260814-official-client-re-receiver-recovery
ci/OTC-20260814-track-a-verified-merge-slice
```

### Later outbound model

The final-write/receiver-recovery continuation state contains a promoted historical high-level chain:

```text
semantic action
 -> TInternalGameActionRouter
 -> TProtocolMessageQueue builder
 -> clientMessageReadyToProcess
 -> Qt QSlotObject consumer
 -> protocol/network processing
```

It further proves/corrects downstream transport structure, including the real `clientMessageReadyToProcess` QSlotObject consumer at `0x7dd630` and later protocol/network owner classes.

This later corpus does **not** add a direct action-specific member reconstruction that binds `TContainerGameActionHandler::sendMoveObject` signal index `1` to connect site `0x7ffb24` or directly to `TProtocolMessageQueue::sendMoveObject`.

The later transport evidence also supersedes an older simple `queue -> containing owner virtual +0x90` interpretation. That stale transport model is not used by S10.

### Verified merge slice

`ci/OTC-20260814-track-a-verified-merge-slice` adds final-write/TCP and experiment-governance material but no new Container action-specific connect/member window. It therefore does not close H2.

## Causal-chain decision

Requested target:

```text
TContainerGameActionHandler::sendMoveObject
 -> exact receiver/route
 -> TProtocolMessageQueue::sendMoveObject
 -> concrete message producer
```

Directly retained portions:

```text
TContainerGameActionHandler::sendMoveObject
  signal index 1 / QMeta wrapper                           PROVEN

TContainerGameActionHandler::<some signal>
  -> TInternalGameActionRouter                            PROVEN

TProtocolMessageQueue::sendMoveObject
  -> builder 0xbd3be0 / internal discriminator 0x78      PROVEN
```

Missing direct edge:

```text
sendMoveObject signal index 1
 -> exact connect/receiver member preserving action identity
 -> exact queue dispatch to TProtocolMessageQueue::sendMoveObject
```

Because that edge is absent from the bounded retained evidence, joining the proven fragments would be an inference. The S10 proof standard explicitly forbids promoting that inference as `PROVEN`.

## Required next evidence

A future task can close this boundary only with an admissible exact code/connect/dataflow window proving at least one of:

```text
A. TContainerGameActionHandler::sendMoveObject signal index 1
   -> concrete receiver member
   -> router/queue action path

B. direct payload/dataflow from the sendMoveObject wrapper/source
   -> TProtocolMessageQueue::sendMoveObject / 0xbd3be0
   with action identity preserved across the edge.
```

For the legitimate current official client, all addresses must be rediscovered under a fresh exact-build provenance fence. Historical offsets in this report cannot be reused as current-build facts.

## Safety and isolation

```yaml
runtime_access: none
client_executed: false
new_client_bytes_obtained: false
credentials_accessed: false
login_performed: false
gameplay_performed: false
runtime_mutation: false
pr528_runtime_touched: false
pr475_runtime_touched: false
pr302_runtime_touched: false
E2E: NOT_APPLICABLE
```

The Remote Desktop/Synology connector became unavailable during the invocation. No result in this report relies on a current runtime observation, and S10 did not attempt login or gameplay.

## Validation / closeout boundary

Research result: terminal for this bounded retained discriminator.

Still required before promotion/merge:

1. fresh proportionate independent documentation audit;
2. exact-head path/Markdown/full-diff repository checks;
3. promotion/archive only if the audit accepts the bounded partial and preserves `BLOCKED_MISSING_RETAINED_CODE_WINDOW`.

No owner-funded direct Codex/OpenAI model invocation was used by S10.
