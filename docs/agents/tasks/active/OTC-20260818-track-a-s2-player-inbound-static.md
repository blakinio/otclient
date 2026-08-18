---
task_id: OTC-20260818-track-a-s2-player-inbound-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: received-owner-discriminator
execution_mode: github_only
branch: research/OTC-20260818-track-a-s2-player-inbound-static
base_branch: main
base_main: a9e7ab21ed0962482e4381aadd50be92714785a6
related_pr: 512
created: 2026-08-18T10:06:00+02:00
updated: 2026-08-18T10:17:00+02:00
risk: medium
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
owned_paths:
  - .github/workflows/track-a-s2-player-inbound-static.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s2-player-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - tools/tibia_runtime_bridge/resolver.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json
  - exact QMeta reconstruction pattern from merged PR #505
  - PR #302 exact static TPlayerData evidence as a negative/control consumer only
depends_on:
  - OTC-20260818-track-a-s1-unfiltered-static-census
blocks: []
non_overlap:
  - PR #475 physical runtime/worldmap/native-login surfaces are not observed or mutated.
  - PR #302 direct-player-position Draft is not modified; its static TPlayerData evidence is read-only control material.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
decomposition_decision: single
validation_level: focused
repair_cycles_for_current_gate: 1
---

# Objective

Resolve the exact static inbound player-message dispatch surface far enough to prove or bound:

```text
GameserverMessagePlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
  -> exact received* method metadata and owner
  -> exact QMeta dispatch target where provable
  -> static downstream owner/call edges toward TPlayerData where provable
```

No runtime is needed or permitted.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

# Starting canonical facts from #511

```text
TPlayerProtocolMessageHandler primary vptr = 0x308a008
TPlayerData primary vptr = 0x308ca70
189 generated server messages
189 received*Message string names
```

# Phase 1 result — QMeta identity and negative control

Successful repaired producer:

```text
run      32115252111
job      95643199117
result   SUCCESS
head     74433287fa9549361eed3733c513b3f46fd2601c
artifact 9316455906
digest   sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
```

Exact QMeta objects recovered:

```yaml
TPlayerProtocolMessageHandler:
  static_metaobject: 0x30852a0
  static_metacall: 0xd1a920
  methods: 22
  signals: 22
  dispatch_table: 0x1d713d0
  full_range_guard: cmp edx,0x15

TPlayerData:
  static_metaobject: 0x307ea60
  static_metacall: 0xd19f40
  methods: 5
  signals: 5
  dispatch_table: 0x1d7139c
  full_range_guard: cmp edx,4

TGameserverGameSession:
  static_metaobject: 0x2f765a0
  static_metacall: 0xd215c0
  methods: 3
  signals: 0
  dispatch_table: 0x1d71764
  full_range dispatch: proven
```

`TPlayerProtocolMessageHandler` QMeta methods are the outbound/control signal surface:

```text
sendEnterWorld
sendGoNorth/East/South/West
sendStop / sendCancel
send diagonals / sendGoPath
sendRotate*
sendSetTactics
worldEntered
showSelectOutfitDialog
showConfigureCreaturePodiumDialog
showHirelingNameChangeConfiguration
publishGameAction
```

No `receivedPlayer*Message` method exists in its 22-method QMeta table.

`TPlayerData` QMeta contains only:

```text
playerDataChanged
publishGameAction
playerLevelUp
vocationSpecificPlayerDataChanged
vocationChanged
```

`TGameserverGameSession` QMeta contains only three unrelated controller methods.

Therefore the simplest hypothesis:

```text
receivedPlayer*Message are QMeta methods owned directly by TPlayerProtocolMessageHandler
```

is **DISPROVEN** on the exact client.

This does not disprove that the handler receives inbound data through non-QMeta calls, Qt connections from another owner, or an upstream protocol queue/router.

# Phase 1 static anchors / control

Fresh whole-file code xrefs reproduce the known `TPlayerData` vptr sites:

```text
0x843e20
0x843f60
0x8440b0
0x8441f2
0xefd13c
```

and `TPlayerProtocolMessageHandler` vptr sites:

```text
0x825681
0x825991
0x194e5c6
0x194e8e4
```

PR #302 independently retains the static XYZ-shaped `TPlayerData` candidate `+0x78/+0x7c/+0x80`, but this task does not promote that candidate as inbound storage or authoritative player state without a direct edge.

# Failure / repair history

## R1 — Capstone skipdata operand access

First producer run `32114891658 / 95642067206` passed both exact-client hashes but failed before QMeta result with:

```text
capstone.CsError: Information irrelevant for 'data' instruction in SKIPDATA mode (CS_ERR_SKIPDATA)
```

Repair separated bounded function decoding from whole-section skipdata scanning and guarded skipdata operand access. No semantic result from the failed run was promoted.

# Current discriminator

Because `receivedPlayer*Message` is not owned by the expected handler QMeta table, the task now performs one exact-file global QMeta ownership census for exactly five target methods:

```text
receivedPlayerDataBasicMessage
receivedPlayerDataCurrentMessage
receivedPlayerInventoryMessage
receivedPlayerSkillsMessage
receivedPlayerStateMessage
```

The census scans relocation-backed `staticMetaObject` candidates, parses method tables and recovers an exact dispatch table only for the target owner(s) where a unique full-range guard exists.

# Acceptance

- [x] exact client fence revalidated;
- [x] `TPlayerProtocolMessageHandler` exact metaobject/method table recovered;
- [x] full-range QMeta dispatch table for `TPlayerProtocolMessageHandler` recovered;
- [x] direct ownership of `receivedPlayer*Message` by `TPlayerProtocolMessageHandler` disproven;
- [ ] exact actual QMeta owner of target received methods found or bounded `UNKNOWN`;
- [ ] exact received-method QMeta signatures/indices persisted where recoverable;
- [ ] exact dispatch targets persisted where recoverable;
- [ ] downstream relation to `TPlayerData` classified per direct evidence;
- [x] no runtime/login/Synology/X11/process-memory/credential access;
- [x] no raw proprietary client committed/uploaded;
- [ ] temporary producer removed before promotion;
- [ ] exact-head CI/governance and review hygiene before terminal disposition.

# Checkpoint

```yaml
checkpoint_version: 3
status: investigating
phase: received-owner-discriminator
pr: 512
last_completed_step: recovered exact QMeta/dispatch tables for handler, player data and game session and disproved direct QMeta ownership of receivedPlayer*Message by TPlayerProtocolMessageHandler
proven:
  - TPlayerProtocolMessageHandler has 22 QMeta signals and one unique full-range static dispatch table.
  - None of its QMeta methods is receivedPlayer*Message.
  - TPlayerData and TGameserverGameSession QMeta tables also do not own the five target received methods.
disproven:
  - receivedPlayer*Message is directly a TPlayerProtocolMessageHandler QMeta method.
unknown:
  - actual QMeta owner of receivedPlayer*Message
  - exact connection/call path from actual owner into TPlayerProtocolMessageHandler
  - handler to TPlayerData mutation edge
blockers: []
next_action: run the exact-file global QMeta ownership census for the five player receive methods, then inspect only the identified owner/dispatch targets; do not broaden into runtime or worldmap.
```
