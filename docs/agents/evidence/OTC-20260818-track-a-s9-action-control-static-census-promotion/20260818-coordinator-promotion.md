# Track A S9 action/control static census — coordinator promotion and static-wave closeout

Date: 2026-08-18  
Source Draft: PR #535  
Source final head: `c08c10d7615c2e68a820f3383f969e7e75956bb9`  
Trusted promotion base: `main@a10df477ce88183718ed855386ef96ba25b66320`  
Decision: **ACCEPT_STATIC_ACTION_CATALOGUE**

## Promoted denominator

The exact retained QMeta corpus contains **28** classes ending `GameActionHandler`. The full type list is preserved in S9 `result.json`; detailed promotion is limited to the principal gameplay-control surfaces.

## Promoted core boundaries

```text
movement intent:
  TPlayerMovementIntentHandler
  eight directions / path / rotate / stop / cancel / follow-zero

protocol-facing movement:
  TPlayerProtocolMessageHandler
  sendGo* / sendStop / sendCancel / sendGoPath / sendRotate* / sendSetTactics

creature actions:
  TCreaturesGameActionHandler
  sendAttack / sendFollow / sendLookAtCreature / inspect / party actions

use/object:
  TUseWithGameActionHandler
  startTargetSelection / sendUseTwoObjects / sendUseOnCreature
  TGenericGameActionHandler
  sendTurnObject / sendUseObject / sendLook / sendBrowseField / sendMoveObject

container/equipment:
  TContainerGameActionHandler
  sendMoveObject / sendEquipObject / stash/depot/container actions

chat/NPC:
  TChatGameActionHandler
  channel/private/guild/talk signals and NPC-talk handling slot

player:
  TPlayerGameActionHandler
  mount/outfit/tactics/inspect

router:
  TInternalGameActionRouter
  internal and cross-router publication/handling
```

## Retained causal boundary

```yaml
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
```

The generic P2 outbound transport/framing/encryption proof does not automatically prove each `send*` QMeta action end-to-end.

## Independent static-wave completion

The promoted non-runtime wave now comprises:

```text
S1 full protocol/QMeta denominator
S2 player inbound queue boundary
S3 bounded player receiver stop
S4 creature/container evidence prioritization
S5 container inbound boundaries
S6 chat inbound boundaries
S7 inventory/equipment boundaries and handler correction
S8 creature model/storage/action boundaries and non-QMeta stop
S9 native action/control catalogue
```

The static lane is now terminal under the currently retained evidence set:

```yaml
PRINCIPAL_STATE_SURFACES: CATALOGUED
PRINCIPAL_ACTION_SURFACES: CATALOGUED
REPEATED_QMETA_NAME_SCAN_VALUE: EXHAUSTED
NEXT_MEANINGFUL_PROOF: EXACT_CODE_WINDOW_OR_LEGAL_RUNTIME
```

## Provenance / validation

```text
S9 run 32140983838
artifact 9325847070
sha256:12ddebc9aa1ff73f96370091c50e33a6cf3bf7b37a4cf8bc7007175861c5491d
QMeta source 31790507112 / 94736106350
source CI 32141422196 = SUCCESS
source Track A governance 32141421851 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new client bytes or execution, physical runtime, Synology/X11/VNC, process memory, credentials, login or gameplay were used. PR #528 and #475 runtime surfaces remained untouched. Physical E2E is `NOT_APPLICABLE` for S9.
