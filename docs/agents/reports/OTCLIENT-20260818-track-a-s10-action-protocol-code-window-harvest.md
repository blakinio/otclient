# OTCLIENT Track A — S10 action-to-protocol retained code-window harvest

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s10-action-protocol-code-window-harvest`  
PR: `#539`  
Trusted base: `main@ebbb36f50076ff4072c7218e302614c1dfea00b1`  
Execution: GitHub-hosted repository evidence only, `runtime_access: none`

## Purpose

S10 continues after the promoted S1-S9 static wave at the first still-open causal boundary:

```text
native game action
 -> exact protocol owner
 -> exact message producer
```

The first bounded discriminator is move-object because S9 exposes it on both `TGenericGameActionHandler` and `TContainerGameActionHandler`, while historical retained branches contain drag/move-object and protocol-queue investigations.

Target chain:

```text
TContainerGameActionHandler / TGenericGameActionHandler
  -> sendMoveObject
  -> exact protocol owner
  -> exact message producer
```

S10 is **not** a new broad action inventory and is **not** a new QMeta/name census.

## Starting point promoted by S9

Current `main` promoted the S9 action/control catalogue and formally ended the independent repo-only S1-S9 QMeta/static catalogue wave.

Principal S9 action surfaces include:

```text
TPlayerMovementIntentHandler
TPlayerMovementGameActionHandler
TPlayerProtocolMessageHandler
TCreaturesGameActionHandler
TUseWithGameActionHandler
TGenericGameActionHandler
TContainerGameActionHandler
TChatGameActionHandler
TPlayerGameActionHandler
TInternalGameActionRouter
```

The retained causal boundary remains:

```yaml
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
STATIC_ACTION_CONTROL_CATALOGUE: EXHAUSTED_FOR_RETAINED_QMETA
```

Therefore matching `send*` names or adjacent metaobjects are discovery leads only.

## S10 proof standard

A positive result requires direct retained exact-build evidence of a causal edge, for example:

```text
GameActionHandler sender/callsite
 -> QObject connection / slot trampoline / direct-call edge
 -> exact receiver or protocol handler
 -> concrete message producer/builder
```

Accepted evidence classes:

- bounded disassembly showing the call/dataflow;
- decoded Qt connect construction that identifies both sender/member and concrete receiver/member;
- a retained code window proving object/argument flow into a protocol producer;
- an equivalent exact-build causal artifact that is stronger than lexical proximity.

Insufficient by itself:

- identical or similar method names;
- QMeta presence;
- type/string proximity;
- neighboring symbols;
- historical workflow names;
- generic outbound transport proof that does not bind the particular action.

Classification remains:

```text
PROVEN
DERIVED
UNKNOWN
DISPROVEN
```

`DERIVED` must remain visibly weaker than direct `PROVEN` evidence.

## Retained historical sources verified for harvest

The following read-only branches exist in `blakinio/otclient` and are the bounded S10 evidence pool:

```text
ci/OTC-20260814-track-a-single-item-drag
ci/OTC-20260814-track-a-final-write-continuation
ci/OTC-20260814-official-client-re-receiver-recovery
ci/OTC-20260814-track-a-verified-merge-slice
```

### First source — `single-item-drag`

Its retained `.github/workflows` tree includes specifically relevant investigations such as:

```text
tibia-official-client-re-controlled-item-drag.yml
tibia-official-client-re-single-item-drag-only.yml
tibia-official-client-re-gameaction-connectimpl-arguments.yml
tibia-official-client-re-gameaction-connectimpl-correlation.yml
tibia-official-client-re-gameaction-dispatch-map.yml
tibia-official-client-re-gameaction-jumptable-map.yml
tibia-official-client-re-gameaction-receiver-callee-xrefs.yml
tibia-official-client-re-gameaction-receiver-targets.yml
tibia-official-client-re-gameaction-signal-xref.yml
tibia-official-client-re-gameaction-slot-invokers.yml
tibia-official-client-re-gameaction-slot-provenance.yml
tibia-official-client-re-high-value-send-disassembly.yml
tibia-official-client-re-player-gameprotocol-map.yml
tibia-official-client-re-protocol-queue-action-dispatch.yml
tibia-official-client-re-protocol-queue-sendmessage-connect.yml
tibia-official-client-re-protocol-queue-slot-provenance.yml
```

Their existence proves only that these historical investigations were retained. It does **not** yet prove the desired `sendMoveObject -> protocol` edge. S10 must inspect their contents and referenced immutable evidence before promoting any causal claim.

### Fallback sources

If the direct edge is not recoverable from `single-item-drag`, inspect in this order:

```text
1. ci/OTC-20260814-track-a-final-write-continuation
2. ci/OTC-20260814-official-client-re-receiver-recovery
3. ci/OTC-20260814-track-a-verified-merge-slice
```

Do not broaden into another repository-wide census between these sources.

## Historical exact-build fence

The retained older evidence was produced around the official native Linux client fenced as:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

This remains an admissible provenance fence for **historical retained evidence only**.

PR #528 has separately recorded current runtime evidence that this old client is refused as too old. Therefore S10 must not claim that historical addresses, vtables, QMeta addresses, helpers or code offsets are valid for the legitimate current official client.

## Current-client and runtime isolation

PR #528 is the active owner of current official-client package/runtime/native-login continuation. S10 therefore performs none of the following:

```text
current-client acquisition
package update
client execution
Synology/X11/VNC observation
process-memory access
runtime attach/injection
credential access
login or character selection
gameplay stimulus
```

PR #475 worldmap runtime and PR #302 direct-position runtime are also untouched.

PR #536's full-client coverage-audit task/checklist/matrix paths are separate and are not edited by S10.

## Bounded harvest procedure

### H1 — identify the historical move-object action endpoint

Read the retained drag/game-action workflows and their referenced evidence to identify the exact historical sender/member/callsite used for `sendMoveObject`.

Required output:

```text
sender object/type
member/callsite identity
exact evidence reference
```

### H2 — recover receiver/connection ownership

Follow only the smallest retained connect/disassembly window needed to identify the concrete receiver or direct callee.

Required output:

```text
sender/member
connection or direct-call construction
receiver object/type
receiver member/callee
```

### H3 — bind receiver to protocol producer

Use the retained protocol-queue / high-value-send evidence to determine whether H2 reaches an exact protocol handler/message builder and, if so, which concrete producer is used.

Required output:

```text
exact protocol owner
exact message producer/builder
field/argument flow if retained evidence contains it
```

### H4 — classify without overclaiming

Possible terminal outcomes:

```text
PROVEN_ACTION_TO_PROTOCOL_EDGE
PARTIAL_ACTION_TO_PROTOCOL_EDGE
BLOCKED_MISSING_RETAINED_CODE_WINDOW
```

`PARTIAL` is allowed only when a direct portion of the chain is proven and the exact missing edge is stated.

## Fail-closed blocker

If the historical retained corpus lacks a direct code/dataflow/connect window sufficient to establish the chain, record:

```text
BLOCKED_MISSING_RETAINED_CODE_WINDOW
```

This means:

```text
retained historical discriminator exhausted
!= action/protocol edge disproven
```

Do not replace missing code evidence with name proximity.

The next meaningful proof would then require:

1. an admissible exact code window for the legitimate current official client after current-build identity/provenance is established; or
2. a separately legal, non-conflicting runtime evidence path admitted under current Track A governance and ownership.

## Current checkpoint result

At this checkpoint S10 has established the bounded evidence pool and proof contract but has **not yet promoted a causal action-to-protocol edge**.

```yaml
S1_TO_S9: COMPLETED_AND_PROMOTED
S10_SCOPE: ESTABLISHED
S10_HISTORICAL_SOURCE_BRANCHES: VERIFIED_PRESENT
REPEATED_QMETA_NAME_SCAN: NOT_PLANNED
CURRENT_CLIENT_ACQUISITION_BY_S10: FORBIDDEN_BY_NON_OVERLAP_WITH_PR_528
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
S10_RESULT: IN_PROGRESS
```

## Validation boundary

This checkpoint is documentation/read-only retained-repository research.

```yaml
runtime_access: none
client_executed: false
new_client_bytes_obtained: false
credentials_accessed: false
login_performed: false
gameplay_performed: false
pr528_runtime_touched: false
pr475_runtime_touched: false
pr302_runtime_touched: false
E2E: NOT_APPLICABLE
E2E_reason: no official-client runtime operation occurs in this retained-evidence phase
```

No owner-funded AI/model invocation was required to create this checkpoint.

## Next action

Exactly one continuation action:

```text
Inspect the retained `ci/OTC-20260814-track-a-single-item-drag` workflow/evidence chain and recover the smallest direct code/connect/dataflow window that can prove or bound `sendMoveObject -> exact protocol owner -> exact message producer`.
```
