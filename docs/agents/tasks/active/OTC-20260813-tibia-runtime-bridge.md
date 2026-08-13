---
task_id: OTC-20260813-tibia-runtime-bridge
status: waiting
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-analysis
task_kind: implementation
phase: stable-bridge-v1
branch: feat/OTC-20260813-tibia-runtime-bridge
base_branch: main
created: 2026-08-13T02:20:00+02:00
updated: 2026-08-13T10:10:00+02:00
risk: medium
related_pr: "#283"
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-runtime-bridge.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
reuses:
  - PR #48 exact-client runtime evidence as read-only producer evidence
  - OTCLIENT-TIBIA-RE Phase 9 preload/Qt proof from run 31653375069 job 94302324521
  - relocation-aware exact-binary vptr proof from run 31654434331 job 94305639119
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
user_communication: terminal_only
context_pressure: medium
decomposition_decision: single
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
---

# Goal

Implement the smallest reusable non-GDB runtime bridge for the exact official Linux Tibia client: an `LD_PRELOAD` helper that executes work on the client's Qt event loop, exposes a local Unix-domain IPC endpoint, dynamically computes the executable PIE base, and discovers semantically profiled runtime objects without permanent modification of CipSoft files.

# Current implementation

The durable bridge is implemented in PR #283 and remains read-only/fail-closed:

- exact SHA-256/version profile fencing in `launcher.py`;
- `LD_PRELOAD` helper with runtime PIE-base discovery;
- owner-only Unix socket (`0600`);
- bounded JSON IPC client;
- `PING` and `DISCOVER <target>` operations;
- Qt-sensitive discovery marshalled to the real Qt event-loop thread;
- current-process readable/writable memory scan for exact profiled vptr values;
- Qt class-name validation for QObject-compatible hits;
- derived `session-status` candidate requiring `player_protocol_handler`, `gameserver_game_session`, and `worldmap_handler` simultaneously;
- relocation-aware ELF resolver (`resolver.py`) to recover primary vptrs for a new exact binary instead of copying old offsets forward.

No gameplay write/action command is part of this bridge slice. Write operations stay gated on a current OTClient-owned structural `IN_GAME` session and authoritative before/after state proof.

# Exact profile evidence — PROVEN

Relocation-aware run `31654434331`, job `94305639119`, passed and recovered primary vptrs for the exact SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`:

```text
TPlayerProtocolMessageHandler   0x308a008
TWorldmapProtocolMessageHandler 0x30871d8
TGameserverGameSession          0x3078ba0
TGameSessionBase                0x3084648
IGameSession                    0x30841c0
TPlayerData                     0x308ca70
TContainerStorage               0x308a1a0
TCreatureStorage                0x308d078
TGameClient                     0x3076908
```

The committed profile exposes seven resolver targets: player protocol handler, worldmap handler, gameserver game session, player data, container storage, creature storage, and game client. Every target is fenced to the exact client hash and cites run `31654434331` as evidence.

# Exact implementation validation — PROVEN

Run `31654823776`, job `94306874981`, completed successfully while explicitly checking out exact bridge code head:

```text
BRIDGE_HEAD=89e13819e6f53026b831b7e8e4c8fab228d1626c
EXACT_BRIDGE_HEAD_VERIFIED=true
12 focused tests: PASS
py_compile launcher/ipc_client/resolver: PASS
BRIDGE_STANDALONE_BUILD_PASS=true
COMPLETE_OFFICIAL_RUNTIME_LAYOUT_VERIFIED=true
EXACT_BRIDGE_VALIDATION_RUNTIME_READY=true
PROFILE_REDISCOVERY_MATCH=true
BRIDGE_SOCKET_MODE=600
EXACT_CLIENT_BRIDGE_E2E_PASS=true
```

The run reconstructed the researched exact official client through the task WARP path, independently reran `resolver.py`, and required each profile target to resolve uniquely to its committed primary-vptr offset. The exact client remained alive through the no-credential E2E.

Logged-out `session-status` correctly returned:

```yaml
in_game_candidate: false
evidence_level: DERIVED_UNTIL_LIVE_CORRELATION
player_protocol_handler.validated_hits: 0
gameserver_game_session.validated_hits: 0
worldmap_handler.validated_hits: 0
```

This is positive fail-closed behavior, not proof that the markers are authoritative in a live world session.

# Current PR head relationship

```yaml
pr: 283
branch: feat/OTC-20260813-tibia-runtime-bridge
current_head: b9a8b73b05d543c565090be7c70aa879c24c1c16
validated_code_head: 89e13819e6f53026b831b7e8e4c8fab228d1626c
compare:
  ahead_by: 1
  changed_files:
    - docs/agents/tasks/active/OTC-20260813-tibia-runtime-bridge.md
  product_code_delta: none
repository_ci_current_head:
  run: 31673504822
  conclusion: success
```

GitHub compare proves the sole commit after the exact E2E code head changed only this task record. Therefore the current product/tool/test code is exactly the code validated by run `31654823776`; no second official-client execution is required merely for the documentation-only checkpoint delta.

# Acceptance inventory

- [x] Launcher rejects unprofiled/mismatched client identity by exact SHA-256.
- [x] Profile carries exact client version/hash and version-fenced semantic targets.
- [x] Helper loads without permanent CipSoft file modification.
- [x] Helper resolves main PIE base dynamically.
- [x] IPC binds an owner-only Unix socket (`0600`).
- [x] IPC `PING` works independently of game state.
- [x] `DISCOVER` scans only current-process readable/writable mappings and validates expected Qt class names when hits exist.
- [x] Qt-sensitive discovery runs on the real Qt event-loop thread.
- [x] Unsupported commands/targets fail closed.
- [x] Focused tests cover profile/hash fencing, IPC framing, session-status logic and resolver names.
- [x] Relocation-aware primary-vptr recovery is implemented and backed by exact-binary evidence.
- [x] Focused/build/relocation/exact-client no-credential E2E passed on exact implementation head `89e13819...`.
- [x] Current PR head differs from the validated implementation only by this task documentation and has green repository CI.
- [ ] Correlate `session-status` markers with a current OTClient-owned structural live world session.
- [ ] Prove authoritative player position and one reversible before/after action before adding write APIs.

# Evidence boundary

## PROVEN

- exact researched client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- temporary preload proof run `31653375069`, job `94302324521` established real Qt event-loop execution without credentials;
- QCoreApplication child traversal is insufficient for handler discovery;
- relocation-aware resolver recovered nine exact-binary primary vptrs;
- exact bridge implementation head `89e13819...` passed 12 tests, standalone Qt build, complete runtime reconstruction, profile rediscovery and exact-client no-credential E2E;
- logged-out session markers resolve to zero hits and fail closed;
- current head `b9a8b73...` has no code/test/tool delta from validated implementation and repository CI is green.

## DERIVED

- `session-status` is a structural candidate only; it becomes authoritative `IN_GAME` evidence only after live correlation with independently proven decoded world state.

## UNKNOWN

- current upstream `tibiaclient-linux-current` SHA after the later failed identity-download probe;
- live-session marker lifecycle and reacquisition after login/logout/restart;
- authoritative player position through the bridge;
- all gameplay write/action semantics.

# Waiting boundary

The remaining acceptance items require a current OTClient-owned structural live world session. New live execution is migrating to the dedicated `synology-otclient-01` runner through PR #280/#48. Do not fall back to the historical Oteryn runner. While the canonical runner job remains unaccepted, this task is accurately `waiting`, not technically failed.

# Durable checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-13T10:10:00+02:00
branch: feat/OTC-20260813-tibia-runtime-bridge
pr: 283
head_before_checkpoint: b9a8b73b05d543c565090be7c70aa879c24c1c16
status: waiting
proven:
  - durable read-only LD_PRELOAD/Qt/Unix-IPC bridge implemented
  - exact-hash fencing and dynamic PIE-base discovery implemented
  - relocation-aware vptr resolver proven on exact researched binary
  - seven exact-profile discovery targets persisted
  - exact implementation head 89e13819 passed 12 tests, standalone Qt build, complete runtime reconstruction, profile rediscovery and exact-client no-credential E2E
  - current PR head has only task-doc delta from validated code and green repository CI
  - logged-out session-status fails closed with zero marker hits
unknown:
  - current upstream official-client hash
  - live structural session marker correlation
  - authoritative position and before/after actions
blockers:
  - current OTClient-owned live structural IN_GAME session is unavailable until dedicated runner/runtime recovery resumes
next_action: after synology-otclient-01 accepts the canonical PR #48 runtime, recover structural IN_GAME, correlate bridge session-status, read authoritative position, and prove one reversible movement transition before any write API is added
```

No Codex or owner-funded AI/API quota was used. All material task state is persisted in `blakinio/otclient`.
