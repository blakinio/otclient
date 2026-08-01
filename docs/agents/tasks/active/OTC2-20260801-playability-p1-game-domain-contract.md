---
task_id: OTC2-20260801-playability-p1-game-domain-contract
status: active
agent: "P1 game-domain contract worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-game-domain-contract
phase: implementation
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
base_branch: main
created: 2026-08-01T22:26:00+02:00
updated: 2026-08-01T22:26:00+02:00
last_verified_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: high
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/crates/game-domain/**
shared_path_lease: []
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
context_pressure: high
decomposition_decision: single
validation_level: heavy
---

# Goal

Implement the sole protocol-neutral game-domain public contract producer defined by `P1_GAME_DOMAIN_CONTRACT_AGENT.md`.

# Exclusive scope

```text
oteryn-client/crates/game-domain/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
```

No shared integration path is owned at launch. The first shared lease may be requested only after exclusive-path focused/component validation.

# Acceptance

- [ ] canonical generation-scoped gameplay IDs/handles exist;
- [ ] closed/versioned `GameEvent` and `GameCommand` envelopes cover only the minimum shared M2 spine;
- [ ] all external values are bounded and stale generations fail deterministically;
- [ ] no Canary, socket, simulation, renderer, UI, platform or app dependency leaks into the public API;
- [ ] focused/property/negative tests and public API review pass;
- [ ] worker reaches `integration_ready` before requesting the shared lease;
- [ ] exact-head heavy gates pass after serialized workspace integration;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:26:00+02:00
head: 55fec043758e1928fd5d39831322a0c21f47589b
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
pr: null
status: implementing
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/crates/game-domain/**
proven:
  - P1 aggregation/archive authorize this exclusive contract producer.
  - This package is the sole producer for canonical gameplay IDs, GameEvent and GameCommand.
  - Shared workspace and architecture paths are not leased at launch.
derived:
  - Exclusive crate implementation may proceed before root integration.
  - Game-domain is the first runtime public producer to receive the serialized shared lease.
unknown:
  - Final minimum variant set until existing foundation/error conventions are reconciled.
conflicts: []
first_failure:
  marker: none
  evidence: lane creation and exclusive-path ownership preflight passed.
rejected_hypotheses:
  - Publish Canary-specific wire types: rejected by protocol-neutral ownership.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
validation:
  - command: launch ownership preflight
    result: PASS
    evidence: exclusive crate/task paths are absent and disjoint on main 55fec043.
blockers: []
next_action: Open the draft worker PR and implement the exclusive game-domain crate without shared-path edits.
```
