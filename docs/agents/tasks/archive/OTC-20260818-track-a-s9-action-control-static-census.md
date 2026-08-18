---
task_id: OTC-20260818-track-a-s9-action-control-static-census
status: completed_static_lane_terminal
session_role: researcher_then_coordinator
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PHYSICAL_E2E_REQUIRED: false
source_pr: 535
source_final_head: c08c10d7615c2e68a820f3383f969e7e75956bb9
promotion_decision: ACCEPT_STATIC_ACTION_CATALOGUE
ownership_release_state: released
---

# Result

S9 completed the planned independent repo-only exact-QMeta wave after S1-S8.

## Exact action catalogue

The retained exact QMeta corpus contains **28 `*GameActionHandler` classes**. Core gameplay boundaries are now explicitly catalogued for:

```text
movement / path / rotate / stop / cancel
attack / follow / look-at-creature
use object / use-with / use-on-creature
move object / equip / container operations
chat / channel / private / guild / NPC talk
player outfit / mount / tactics / inspect
internal game-action routing
```

Key exact classes:

```text
TPlayerMovementIntentHandler          0x3085de0 / 0xdc9220
TPlayerMovementGameActionHandler      0x3085260 / 0xdc4060
TPlayerProtocolMessageHandler         0x30852a0 / 0xd1a920
TCreaturesGameActionHandler           0x3085060 / 0xd16340
TUseWithGameActionHandler             0x3085120 / 0xdc4480
TGenericGameActionHandler             0x3085020 / 0xdcb990
TContainerGameActionHandler           0x30850a0 / 0xd1dac0
TChatGameActionHandler                0x30851a0 / 0xcff5b0
TPlayerGameActionHandler              0x3085160 / 0xd1a230
TInternalGameActionRouter             0x3074b20 / 0xd20600
```

## Retained boundary

```yaml
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
STATIC_ACTION_CONTROL_CATALOGUE: EXHAUSTED_FOR_RETAINED_QMETA
```

The static wave now has enough breadth. Repeating QMeta/name scans will not resolve causal dataflow. Next meaningful proof requires approved exact-build code/disassembly windows or a legal non-conflicting runtime surface.

## Provenance / validation

```text
S9 producer run 32140983838
artifact 9325847070
sha256:12ddebc9aa1ff73f96370091c50e33a6cf3bf7b37a4cf8bc7007175861c5491d
historical QMeta source 31790507112 / 94736106350
source CI 32141422196 = SUCCESS
source Track A governance 32141421851 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new official-client bytes, client execution, runtime, credentials, login or gameplay. PR #528/#475 runtime remained untouched.
