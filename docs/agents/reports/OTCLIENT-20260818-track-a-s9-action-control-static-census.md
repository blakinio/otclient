# OTCLIENT Track A — S9 action/control static census and lane closeout

## Decision candidate

`ACCEPT_STATIC_ACTION_CATALOGUE`.

S9 is the terminal planned repo-only exact-QMeta stage of this independent research wave. Together with promoted S1–S8 it provides a durable map of the principal inbound state boundaries and native action/control entry surfaces while leaving unproven causal edges explicit.

## Core control boundaries now catalogued

```text
movement:
  TPlayerMovementIntentHandler
  -> eight directions, path, rotate, stop, cancel, follow-zero
  TPlayerProtocolMessageHandler
  -> matching protocol-facing movement/rotation/tactics signals

creature actions:
  TCreaturesGameActionHandler
  -> attack, follow, look-at-creature, inspect, party actions

object/use:
  TGenericGameActionHandler
  -> turn/use/look/browse/move object
  TUseWithGameActionHandler
  -> target selection, use-two-objects, use-on-creature

container/equipment:
  TContainerGameActionHandler
  -> move/equip/stash/depot/container actions

chat/NPC:
  TChatGameActionHandler
  -> channel/private/guild/talk actions and NPC talk slot

player:
  TPlayerGameActionHandler
  -> mount/outfit/tactics/inspect

routing:
  TInternalGameActionRouter
  -> internal and cross-router game-action publication/handling
```

## Denominator

```text
retained *GameActionHandler QMeta classes = 28
```

The complete list and exact QMeta addresses are preserved in the S9 producer and `result.json`.

## What this does NOT claim

```text
action QMeta signal -> exact receiver/protocol object = UNKNOWN unless separately proven
per-action protocol producer -> serialized message = UNKNOWN
per-action server acceptance/effect = NOT_OBSERVED
```

The generic outbound transport/framing/encryption proof does not automatically convert every `send*` method into a fully proven end-to-end action.

## Independent static-wave closeout

The completed non-runtime wave now covers:

```text
S1 full inbound/protocol/QMeta denominator
S2 player inbound queue boundary
S3 bounded player queue receiver stop
S4 creature/container evidence prioritization
S5 container inbound boundaries
S6 chat inbound boundaries
S7 inventory/equipment boundaries and handler-owner correction
S8 creature model/storage/action boundaries + non-QMeta stop
S9 native action/control catalogue
```

Further useful causal progress is no longer a repository-QMeta census problem. It needs:

1. approved exact-build executable/disassembly connection/dataflow windows; or
2. legal non-conflicting runtime after the current physical runtime owner releases/provides the relevant evidence surface.

Until then repeating type/name/QMeta scans would mostly duplicate known boundaries.

## Provenance

```text
S9 run 32140983838
artifact 9325847070
sha256:12ddebc9aa1ff73f96370091c50e33a6cf3bf7b37a4cf8bc7007175861c5491d
QMeta source 31790507112 / 94736106350
```

## Isolation

This entire S9 stage used no new official-client bytes, client execution, physical runtime, Synology/X11/VNC, process memory, credentials, login or gameplay. PR #528 and #475 were not observed or mutated.
