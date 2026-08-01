---
task_id: OTC2-20260801-playability-p1-asset-pack-runtime
status: active
agent: "P1 asset pack runtime worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-asset-pack-runtime
phase: implementation
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
base_branch: main
created: 2026-08-01T22:27:00+02:00
updated: 2026-08-01T22:27:00+02:00
last_verified_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: high
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/crates/asset-runtime/**
shared_path_lease: []
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
context_pressure: high
decomposition_decision: phased
validation_level: heavy
---

# Goal

Implement the immutable synthetic-v1 asset pack open/verify/index/lookup runtime defined by `P1_ASSET_PACK_RUNTIME_AGENT.md`.

# Exclusive scope

```text
oteryn-client/crates/asset-runtime/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
```

`asset-types` and `asset-compiler` are read-only producer inputs. No shared integration path is owned at launch; integration must wait for the game-domain merge/archive and a recorded lease.

# Acceptance

- [ ] capability-safe immutable pack open verifies schema/version/counts/ranges/hashes;
- [ ] malformed, duplicate, overlapping, trailing, oversized and stale-generation cases fail closed;
- [ ] immutable bounded index and generation-stable logical handles exist;
- [ ] only project-original synthetic-v1 fixtures are claimed;
- [ ] no decode/GPU/import/signing/rights/app activation work;
- [ ] focused/component tests pass in exclusive paths;
- [ ] worker reaches `integration_ready` and waits without polling until the shared lease;
- [ ] exact-head heavy gates pass after serialized integration;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:27:00+02:00
head: 55fec043758e1928fd5d39831322a0c21f47589b
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
pr: null
status: implementing
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
  - oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/crates/asset-runtime/**
proven:
  - P1 aggregation/archive authorize this bounded synthetic-v1 runtime package.
  - asset-types and asset-compiler remain read-only producers.
  - Shared workspace and architecture paths are not leased at launch.
derived:
  - Exclusive crate implementation may proceed before root integration.
  - Shared integration follows game-domain archive.
unknown:
  - Exact runtime API details until current pack/compiler invariants are reconciled.
conflicts: []
first_failure:
  marker: none
  evidence: lane creation and ownership preflight passed.
rejected_hypotheses:
  - Expand to production import/signing: rejected as owner/later scope.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
validation:
  - command: launch ownership preflight
    result: PASS
    evidence: exclusive crate/task paths are absent and disjoint on main 55fec043.
blockers: []
next_action: Open the draft worker PR and implement the exclusive asset-runtime crate without shared-path edits.
```
