---
task_id: OTC2-20260801-playability-p1-input-actions
status: active
agent: "P1 input-actions worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-input-actions
phase: implementation
branch: feat/OTC2-20260801-playability-p1-input-actions
base_branch: main
created: 2026-08-01T22:28:00+02:00
updated: 2026-08-01T22:28:00+02:00
last_verified_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: medium
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/crates/input-actions/**
shared_path_lease: []
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
context_pressure: medium
decomposition_decision: single
validation_level: heavy
---

# Goal

Implement the framework-neutral normalized input and semantic action/context producer defined by `P1_INPUT_ACTIONS_AGENT.md`.

# Exclusive scope

```text
oteryn-client/crates/input-actions/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
```

No shared integration path is owned at launch. Integration must wait for game-domain and asset-runtime merge/archive plus a recorded lease.

# Acceptance

- [ ] normalized key/button/pointer/wheel/text/focus/capture contracts exist without winit/Win32 types;
- [ ] bounded semantic action/context/binding/chord/repeat APIs exist;
- [ ] context precedence, conflicts and focus/capture/device-loss cleanup are deterministic;
- [ ] no widgets, game commands, settings persistence, default product keymap or app composition;
- [ ] focused/property/component tests pass in exclusive paths;
- [ ] worker reaches `integration_ready` and waits without polling until the shared lease;
- [ ] exact-head heavy gates pass after serialized integration;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:28:00+02:00
head: 55fec043758e1928fd5d39831322a0c21f47589b
branch: feat/OTC2-20260801-playability-p1-input-actions
pr: null
status: implementing
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
  - oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
  - oteryn-client/crates/input-actions/**
proven:
  - P1 aggregation/archive authorize this bounded input contract producer.
  - Public contracts must remain independent of platform, UI and game-domain types.
  - Shared workspace and architecture paths are not leased at launch.
derived:
  - Exclusive crate implementation may proceed before root integration.
  - Shared integration follows asset-runtime archive.
unknown:
  - Exact minimum public API until existing foundation/error conventions are reconciled.
conflicts: []
first_failure:
  marker: none
  evidence: lane creation and ownership preflight passed.
rejected_hypotheses:
  - Add default bindings or settings persistence: rejected as later product scope.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
validation:
  - command: launch ownership preflight
    result: PASS
    evidence: exclusive crate/task paths are absent and disjoint on main 55fec043.
blockers: []
next_action: Open the draft worker PR and implement the exclusive input-actions crate without shared-path edits.
```
