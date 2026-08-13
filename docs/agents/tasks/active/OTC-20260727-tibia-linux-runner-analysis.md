# OTC-20260727 — Tibia Linux runner analysis

## Status

`active_decoded_world_entry_reproduction` — exact current-client runtime, login-service identity, Qt/protobuf capability surfaces and same-hash decoded Worldmap boundary are proven. Hosted account login now produces real tunneled TCP under GDB-from-start; the current experiment reproduces the successful same-hash Worldmap capture by using the decoded ordered-map routine itself as the `IN_GAME` truth signal instead of inferred Qt wrapper call sites.

This is an operational `OTCLIENT-TIBIA-RE` task. Temporary `.github/workflows/tibia-*` files are evidence scaffolding, not product code.

## Ownership and authority

- repository: `blakinio/otclient`
- branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` draft operational PR
- writable scope: this task record plus task-owned temporary Tibia analysis workflows
- `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811`: read-only same-hash evidence only
- canonical `oteryn-staging`: out of scope
- owner-funded Codex/API quota: forbidden unless separately authorized
- existing test-account Actions secrets: authorized only through the existing task workflow/runtime path; never expose values

## Exact client/runtime — PROVEN

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
package_entries: 1634
asset_entries: 7094
packed_minimap_subareas: 209
```

Run `31626946078`, job `94215664628`, proved complete runtime reconstruction with `FAILED_ASSET_LOAD_COUNT=0`. Software Mesa/llvmpipe + lavapipe is the known-good hosted renderer path. `QT_XCB_GL_INTEGRATION=none` is rejected.

## WARP/account login service — PROVEN

Run `31647827166`, job `94285373954`, proved current login identity through verified changed WARP egress:

```text
HTTPS_STATUS=200
HAS_SESSION=true
HAS_PLAYDATA=true
HAS_CHARACTERS=true
HAS_WORLDS=true
```

The accepted identity bundle uses `clientversion=15.32.df7b29`, `clienttype=2` and the current 64-character asset version. No credential/session/character/world values are retained.

## Worldmap structural boundary — PROVEN

For the exact current binary:

```text
FullMap        0xcec8d0
FieldData      0xcd3190
Create         0xcecc70
Change         0xcecf40
Delete         0xcd4e20
ordered map    0x19a8a80
capture point  0x19a8ea3
Worldmap qmeta 0x3087800
string data    0x1cd8a54
metadata       0x1cd8820
static call    0xdf2a60
```

QMetaObject layout is `string +0x8`, `metadata +0x10`, `static_metacall +0x18`.

Read-only same-hash Oteryn evidence proves a live decoded sample with 83 real ordered records across z6/z7. `raw28/raw30` semantics remain `UNKNOWN`.

## Exact login/session metadata — PROVEN static ownership

Runs:

- QMeta recovery `31649792368`, job `94291373444`: PASS
- method-owner index `31650684531`, job `94294137219`: PASS
- auth inventory `31652067802`, job `94298391194`: PASS

Important owners:

```text
TCharacterSelectionController qmeta=0x2f656a0 static=0xd46550
  requestCharacterLogin index 0 -> qmeta dispatch target 0xd47300
  onCharacterSelectionConfirmed index 11 -> 0xd47130

TAuthenticationProcessController qmeta=0x3073920 static=0xcfabb0
  onLoginStateMachineStarted -> 0xcfadd4
  onShowCharacterSelectionStateEntered -> 0xcfb374
  onStartGameServerLoginStateEntered -> 0xcfb122
  onLoginFailedStateEntered -> 0xcfb404
  onLoginFinishedSuccessfullyEntered -> 0xcfaeb4

TLoginRequestUploader qmeta=0x2f657e0 static=0xcfb5a0
  loginSuccessful -> 0xcfb7c0
  loginFailed -> 0xcfb790

TGameserverLoginProcessController qmeta=0x30cdc60 static=0xcf9da0
  TCP connected -> 0xcfa0e0
  secondary connected -> 0xcfa110
  disconnected -> 0xcfa150

TGameClient qmeta=0x2f61ea0 static=0xd06260
  connect existing -> 0xd06660
  onConnect -> 0xd06810
  onAbort -> 0xd067b0
  onGameSessionConnected -> 0xd066e0

IGameSession qmeta=0x30790a0 static=0xd26400
  gameLoginSuccessful index 5
  worldEntered index 6
```

**DISPROVEN:** the earlier claim that critical QMetaObjects were missing. The failing filter mixed methods owned by different objects.

**IMPORTANT DERIVED CORRECTION:** QMeta static-dispatch targets are useful semantic ownership evidence but are not proven normal runtime call sites. Live runs produced real auth TCP without hitting those wrapper breakpoints. Do not use absence of those hits to claim the corresponding state did not occur.

## Live hosted experiments — current conclusions

### Old post-start attach path

Run `31650884938`, job `94294748731`, and corrected geometry run `31651611051`, job `94296954131`:

- exact client/runtime and trace armed;
- no decoded map hit;
- no direct TCP/UDP;
- client survived;
- Qt wrapper-event file remained empty.

This disproves the old marker `FIRST_CHARACTER_ACTIVATED` as proof of character activation.

### Auth structural trace

Run `31652180172`, job `94298739316`:

- exact bootstrap succeeded;
- no decoded map hit;
- no direct TCP/UDP;
- wrapper trace remained empty.

Because QMeta wrapper targets are not proven normal call sites, this run does **not** prove the authentication state machine itself was absent.

### GDB-from-start v1

Run `31652573423`, job `94299916593`:

- exact runtime reconstruction: PASS
- exact client started under GDB from `starti`: PASS
- breakpoint setup before UI: PASS
- account login produced real local SOCKS traffic: `AUTH_LOCAL_SOCKS_OBSERVED=1`
- Qt wrapper trace: empty
- run stopped before character activation because it incorrectly required the wrapper `CHARACTER_SELECTION_STATE_ENTERED`

**DISPROVEN:** absence of QMeta wrapper hits is a valid character-selection gate.

## Current live experiment

```yaml
experiment_id: OTC48-WORLD-ENTRY-002
workflow: .github/workflows/tibia-hosted-gdb-from-start-world-entry.yml
head: e581377cb990bec332ef4cbd67e3546aa01b3366
run: 31653056907
objective: reproduce same-hash decoded world entry using the ordered-map content routine as truth
preconditions:
  binary_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  egress: verified WARP
  runtime: complete 1634+7094 reconstruction
  debugger: attached from starti before UI
method:
  - arm base+0x19a8ea3 decoded content capture before client proceeds
  - submit login with proven coordinates
  - require observed local SOCKS auth traffic
  - use the same row/Return + bounded double-click fallback as the successful same-hash Oteryn capture
  - accept IN_GAME only after at least 8 structurally valid decoded map records
  - require zero direct TCP and UDP
result: RUNNING
```

The map capture writes only record counts to workflow state; proprietary content bytes are not persisted as artifacts.

## Exact static capability catalogue — PROVEN for this binary

Capability QMeta run `31651155741`, job `94295569820`: PASS (`494` relevant methods, `460` direct qmeta dispatch targets).

Generated protocol inventory `31651220862`, job `94295767215`: PASS (`240` GameclientMessage + `550` GameserverMessage symbols; `142` capability-related).

Signature inventory `31651501473`, job `94296624884`: PASS.

High-level action inventory `31651684700`, job `94297172395`: PASS (`1004` high-level action methods).

### Outbound/action families

```text
TPlayerProtocolMessageHandler qmeta=0x30852a0 static=0xd1a920
  N/E/S/W, diagonals, GoPath, Rotate N/E/S/W, Stop, Cancel

TCreaturesGameActionHandler qmeta=0x3085060 static=0xd16340
  sendAttack, sendFollow

TGenericGameActionHandler qmeta=0x3085020 static=0xdcb990
  sendUseObject, sendMoveObject

TUseWithGameActionHandler qmeta=0x3085120 static=0xdc4480
  sendUseTwoObjects, sendUseOnCreature

TChatGameActionHandler qmeta=0x30851a0 static=0xcff5b0
  sendTalkMessage

TContainerProtocolMessageHandler qmeta=0x3084fe0 static=0xd1e000
  close/up/seek/action plus inventory/container inbound handlers
```

Exact generated argument types resolve to `GameclientMessageGo*`, `Attack`, `Follow`, `UseObject`, `UseTwoObjects`, `UseOnCreature`, `MoveObject`, `Talk`, and container message types.

High-level Qt surfaces include `attackCreature(qint64)`, `followCreature(qint64)`, `useOnCreature(qint64)`, `sendChannelMessage(QString)`, `sendPrivateMessage(QString,QString)`, `sendNpcMessage(QString)`, container open/close methods and character turning.

### Read/state families

State inventory run `31652393473`, job `94299386259`: PASS (`121` targeted read/update methods).

```text
TCreature                   positionWasUpdated
TCreatureStorage            creatureUpdated / appearanceUpdated
TCyclopediaMapStorage       playerPositionChanged / onPlayerPositionWasUpdated
TCooldownStorage            spell/group/multi-use/passive cooldown changes
TPlayerData                 playerDataChanged / level / vocation
TPlayerSkillStats           playerSkillStatsChanged
THitpointManabarController  current/max HP and mana
TPlayerInventoryAndStatus   capacity / states / inventory / soul
TStatusBarController        states / HP / mana / skills
TContainerStorage           containerUpdated / containerRemoved
TInventoryContainer         inventoryChanged
TMinimapController          onPlayerPositionChanged
TWorldmapProtocolHandler    FullMap / FieldData / Create / Change / Delete
TProtocolMessageQueue       world entered, map, creature, player, inventory, container families
```

## Same-hash native movement lead — read-only evidence

The Oteryn runtime independently proved a live `TPlayerProtocolMessageHandler` object using vptr offset `0x308a008` and invoked native movement/rotation bodies while the client stayed alive and socket counters changed. That is a **lead**, not OTClient proof of authoritative before/after position.

Current semantic-vptr raw-file scanner run `31652312282`, job `94299139890`, failed without useful output. **Rejected implementation:** blind raw-qword RTTI/vptr scan. A future stable resolver should use relocations/semantic calibration instead.

## Stable bridge direction — DERIVED, not yet implemented

Evidence supports a future non-GDB interface using a process helper/sidecar with:

- exact-hash semantic resolver (Qt metaobjects, protobuf names, RTTI/vtables/signatures);
- structured Unix-domain IPC;
- Qt-thread-safe action invocation using high-level object methods where possible;
- structural reads from player/map/creature/inventory/container state;
- disconnect/restart detection and dynamic PID/PIE/object reacquisition.

GDB remains research instrumentation only and is not the final Phase 9 interface.

## Safety invariants

- no OCR/Tesseract/image-to-text for login or semantic proof;
- no secret values in argv/logs/screenshots/repository/artifacts/chat;
- changed WARP egress before secret use;
- zero unintended direct TCP/UDP when required by experiment;
- no canonical staging mutation and no mutation of the separately owned Oteryn runtime;
- pixels/windows are bootstrap aids, never semantic world-state evidence;
- debugger instrumentation in this task is observational only;
- leave character idle when world entry is proven; action proofs belong to the next programme phase.

## Durable checkpoint

```yaml
checkpoint_version: 5
updated_at: 2026-08-13T02:07:00+02:00
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
status: investigating
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
proven:
  - exact full runtime and current login-service identity
  - same-hash Worldmap structural decode boundary
  - exact Qt/protobuf action and state catalogues
  - GDB-from-start login produces real local SOCKS auth traffic
rejected_hypotheses:
  - missing critical QMetaObjects
  - FIRST_CHARACTER_ACTIVATED marker proves activation
  - lack of QMeta wrapper breakpoints proves auth/character state absent
  - raw-qword semantic vptr scanner
unknown:
  - whether hosted GDB-from-start run can reproduce >=8 decoded map records
  - authoritative current player position in the OTClient-owned live session
  - live before/after action effects
active_operation:
  run: 31653056907
  head: e581377cb990bec332ef4cbd67e3546aa01b3366
  workflow: tibia-hosted-gdb-from-start-world-entry.yml
safe_to_resume: true
next_action: inspect terminal run 31653056907 once; if decoded records >=8, persist structural IN_GAME and close this login phase, otherwise use the decoded-map count/socket outcome as the sole next live hypothesis
```
