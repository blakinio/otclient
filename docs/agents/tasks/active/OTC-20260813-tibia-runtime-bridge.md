---
task_id: OTC-20260813-tibia-runtime-bridge
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-analysis
task_kind: implementation
phase: stable-bridge-v1
branch: feat/OTC-20260813-tibia-runtime-bridge
base_branch: main
created: 2026-08-13T02:20:00+02:00
updated: 2026-08-13T02:20:00+02:00
risk: medium
related_pr: none
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-runtime-bridge.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
reuses:
  - PR #48 exact-client runtime evidence as read-only producer evidence
  - OTCLIENT-TIBIA-RE Phase 9 preload/Qt proof from run 31653375069 job 94302324521
  - same-hash TPlayerProtocolMessageHandler vptr lead 0x308a008 from read-only Oteryn evidence
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

# Scope

The first durable slice exposes only read/health operations:

- `PING` / health;
- exact executable identity fencing performed by the launcher;
- PIE-base discovery inside the client process;
- profile-driven vptr target resolution;
- current-process readable/writable memory scan;
- Qt metaobject class validation for discovered QObject-compatible targets;
- `DISCOVER player_protocol_handler` over local Unix-domain IPC.

No gameplay action is part of this first bridge slice. Live write/action operations are added only after a current OTClient-owned `IN_GAME` session and authoritative before/after state proof exist.

# Acceptance inventory

- [ ] Launcher refuses a client whose SHA-256 differs from the selected profile.
- [ ] Profile includes exact client version/hash and semantic target metadata; raw offsets are version-fenced rather than treated as permanent constants.
- [ ] Helper loads without permanently modifying the installed client.
- [ ] Helper discovers the main PIE base dynamically.
- [ ] IPC server binds only a local Unix socket with owner-only permissions.
- [ ] IPC `PING` works independently of game state.
- [ ] `DISCOVER player_protocol_handler` scans only readable/writable current-process mappings and validates an exact profiled vptr plus expected Qt class name when an object is present.
- [ ] Qt-sensitive discovery executes on the real client event-loop thread via queued/blocking invocation.
- [ ] Unsupported commands/targets fail closed.
- [ ] Unit tests cover profile parsing/hash fencing and IPC client framing.
- [ ] Exact-client integration proves helper load, local IPC and Qt-thread discovery path without credentials.
- [ ] No Codex, owner-funded AI/API quota, credentials or proprietary client bytes are committed.

# Evidence boundary

## PROVEN producer evidence

- exact client `15.32.df7b29`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- temporary preload proof run `31653375069`, job `94302324521`: constructor loaded, `QCoreApplication` found, `QMetaObject::invokeMethod(... Qt::QueuedConnection)` succeeded, eight real Qt-loop scans executed and the client remained alive;
- QCoreApplication child traversal found no target Tibia handler objects;
- same-hash read-only evidence identifies a live `TPlayerProtocolMessageHandler` primary vptr at `PIE + 0x308a008`.

## UNKNOWN until this task proves it

- whether profile-vptr memory scanning finds a target in logged-out state;
- whether a discovered vptr hit is QObject-compatible and reports the expected class;
- current in-game target object lifecycle/reacquisition after logout/restart;
- all write/action bridge semantics.

# Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T02:20:00+02:00
head: 05450748daca8344d9555638b638e98b6dc3abc7
branch: feat/OTC-20260813-tibia-runtime-bridge
pr: none
status: implementing
proven:
  - no overlapping open runtime-bridge PR was found before branch creation
  - branch was created from current main 05450748daca8344d9555638b638e98b6dc3abc7
  - temporary Phase 9 preload proof established real Qt event-loop execution
unknown:
  - implementation and validation result
blockers: []
next_action: implement profile-fenced launcher, preload helper, IPC client and focused tests, then validate with synthetic tests and exact-client no-credential integration
```
