# OTCLIENT-TIBIA-RE — creature/combat current-package static G0

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-creature-combat-static-g0
pr: 558
alias: TIBIA-RE-CREATURE-COMBAT
alias_primary_coverage: D01-D08, C15-C17
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
producer_run: 32228647135
producer_job: 95993567735
producer_state_at_checkpoint: in_progress
```

## Scope

This is a bounded current-package static researcher package. It revalidates creature/battle/combat structural surfaces on the current public native-Linux package and targets the previously missing dedicated G0 evidence for `D06` and `D07`.

It does not claim runtime combat semantics, server acceptance, live target causality, authoritative live creature values, or attack/follow effects. Those remain gated by `LIVE-STATE` / `LIVE-ACTION` and a separately admitted physical-runtime task where required.

## Trusted baseline before this G0

The canonical coverage snapshot used by PR #536 classifies:

```text
D01 PARTIAL  creature-family inbound queue boundaries
D02 PARTIAL  queue -> non-QMeta creature handler dispatch
D03 PARTIAL  creature handler -> model/storage mutation
D04 PARTIAL  central creature registry/lifecycle
D05 PARTIAL  creature health/outfit/speed/skull/party/marks/light/type/unpass
D06 NOT_STARTED creature HUD names/icons/status effects
D07 NOT_STARTED battle-list filters/sorting/secondary lists
D08 PARTIAL  battle target / first-next target selection
C15 PARTIAL  attack
C16 PARTIAL  follow
C17 PARTIAL  cancel attack/follow target
```

No row is promoted by this checkpoint while the current-package producer is still running.

## Historical exact-build evidence consumed read-only

### S8 creature inbound

Historical exact-build S8 proved, for `15.32.df7b29` only:

```text
TProtocolMessageQueue
  13 creature-family receive signals

TCreatureProtocolMessageHandler
  QMeta object present, 0 QMeta methods / 0 signals

TCreature
  positionWasUpdated + mark/party/inspection signals

TCreatureStorage
  playerAdded / creatureUpdated / creatureAppearanceUpdated

TCreaturesGameActionHandler
  sendAttack / sendFollow / sendLookAtCreature / party actions
```

S8 also proved a negative QMeta result: no suffix-matched `handleXMessage` method closed the queue-to-handler edge. Therefore `D02`/`D03` remain structurally incomplete; absence from QMeta is not absence of a non-QMeta implementation.

### S9 action/control

Historical exact-build S9 catalogued:

```text
TCreaturesGameActionHandler
  -> attack, follow, look-at-creature, inspect, party actions

TInternalGameActionRouter
  -> internal and cross-router game-action publication/handling
```

S9 explicitly left these unproven:

```text
action QMeta signal -> exact receiver/protocol object = UNKNOWN unless separately proven
per-action protocol producer -> serialized message = UNKNOWN
per-action server acceptance/effect = NOT_OBSERVED
```

This G0 preserves those boundaries and does not overlap PR #539/S10 action-protocol ownership.

## Current-package producer contract

Run `32228647135` is intentionally GitHub-hosted and disposable. The workflow must:

1. fetch the public Linux package through the existing WARP pattern;
2. fail closed against the expected packed/unpacked package fingerprint;
3. enumerate creature/battle/combat QMeta class/method ownership without the disproven world/minimap per-method jump-target heuristic;
4. retain relevant protocol and neutral semantic strings only;
5. delete packed and unpacked proprietary client bytes before upload;
6. upload only compact text evidence.

At this checkpoint, the producer is still running. Current-package QMeta/protocol/string findings are therefore `UNKNOWN` until its artifact is available and independently inspected.

## Expected evidence questions

The final producer artifact is intended to answer, at a static-only boundary:

- which current-package creature model/storage/controller QMeta surfaces exist;
- whether current-package creature HUD name/icon/status-effect surfaces are directly enumerated;
- which current-package battle-list controller/model/filter/sort/secondary-list surfaces are directly enumerated;
- which target-selection, attack/follow/cancel structural surfaces exist;
- which neutral generated-message/protocol names corroborate creature-state and combat families.

It is not sufficient to answer:

- authoritative live creature identity/value storage;
- queue -> non-QMeta handler executable dataflow;
- handler -> model mutation dataflow;
- live battle-list membership/filter results;
- attack/follow/cancel runtime causality;
- server acceptance or side effects.

## Safety and isolation

```yaml
client_executed: false
runtime_observed: false
credentials_accessed: false
login_attempted: false
gameplay_performed: false
client_byte_mutation: false
raw_client_artifact_allowed: false
shared_runtime_mutation: false
```

PR #528/#550 physical runtime, PR #536 shared coverage paths, PR #539/S10 paths and PR #540 spawn/mechanics paths are read-only dependencies and are not modified by this researcher.

## Pending finalization

After producer completion, this report must be updated with exact run/artifact identity, current-package fence, sanitized class/method/message findings, FACT/INFERENCE/UNKNOWN classifications, row-by-row coverage consequence and exact remaining discriminators. The temporary producer workflow must then be deleted before final Draft-head validation.
