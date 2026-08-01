---
task_id: OTC2-20260801-playability-p1-canary-source-index
status: active
agent: "P1 Canary source-index worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-canary-source-index
phase: implementation
branch: tools/OTC2-20260801-playability-p1-canary-source-index
base_branch: main
created: 2026-08-01T22:25:00+02:00
updated: 2026-08-01T22:25:00+02:00
last_verified_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: high
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
  - oteryn-client/tools/canary-protocol-index/**
  - oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
  - oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
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

Implement the deterministic exact-source Canary Current index and privacy-safe fixture-feasibility evidence defined by `P1_CANARY_SOURCE_INDEX_AGENT.md`.

# Source boundary

Accepted producer cut:

```text
blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3
Canary 3.6.1
client version 1525
ProtocolProfileId::Current
```

No deployment-equality claim, capture, credential, proprietary asset byte, copied server implementation body or guessed opcode/layout is authorized.

# Acceptance

- [ ] deterministic tool/parser exists under the owned tool path;
- [ ] two clean generations are byte-identical;
- [ ] normalized direction/opcode/source/gate/state/package fields are produced or explicitly unresolved;
- [ ] representative bootstrap/map/entity/movement/player/item-container/chat/combat paths are reconciled;
- [ ] source and fixture reports are complete and bounded;
- [ ] no workspace member/root/shared-path edit;
- [ ] focused/component/repository CI and clean review pass;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:25:00+02:00
head: 55fec043758e1928fd5d39831322a0c21f47589b
branch: tools/OTC2-20260801-playability-p1-canary-source-index
pr: null
status: implementing
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_CANARY_SOURCE_INDEX_AGENT.md
  - oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
  - oteryn-client/tools/canary-protocol-index/**
  - oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
  - oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
proven:
  - P1 aggregation/archive are merged and authorize this bounded tool/evidence package.
  - Exact accepted source cut and Current profile are recorded.
  - This lane requires no shared integration lease or workspace member.
derived:
  - Generated exact-source metadata must replace handwritten opcode/layout assumptions.
unknown:
  - Unsupported source constructs and exact fixture feasibility until generator reconciliation.
conflicts:
  - Inspected source cut is not proven equal to deployment.
first_failure:
  marker: none
  evidence: lane creation preflight passed.
rejected_hypotheses:
  - Use packet captures: rejected by privacy/security boundary.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
validation:
  - command: launch ownership preflight
    result: PASS
    evidence: exclusive paths are absent and disjoint on main 55fec043.
blockers: []
next_action: Open the draft worker PR and implement the deterministic exact-source index within the exclusive paths.
```
