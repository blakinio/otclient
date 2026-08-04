---
task_id: OTC2-20260804-native-protocol-contract
status: ready
branch: docs/OTS-20260804-native-protocol-contract
base_branch: main
created: 2026-08-04
updated: 2026-08-04
related_pr: "blakinio/otclient#265"
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
required_reads:
  - AGENTS.md
  - AGENTS.override.md
  - docs/agents/AGENTS.md
  - oteryn-client/AGENTS.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
search_first:
  - OTS-20260804-native-protocol-selection
optional_reads:
  - oteryn-client/crates/game-domain/src/lib.rs
  - oteryn-client/crates/protocol-core/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/game-session/src/lib.rs
---

# Rust client native gameplay protocol contract correspondence

## Goal

Record the Rust consumer and automatic-selection responsibilities without adding dependencies, creating `protocol-oteryn`, changing transport/runtime or claiming compatibility.

## Acceptance criteria

- [x] Canonical Platform contract and Otheryn correspondence are pinned to exact merged revisions.
- [x] Offer, Gateway selection, opaque session binding and no-downgrade behavior map to protocol-neutral layers.
- [x] Canary and native adapters remain independent and one session binds one immutable adapter.
- [x] Snapshot/delta, action result, duplicate and replacement-session behavior is explicit.
- [x] Later implementation ownership and ordering are explicit.
- [x] Independent consistency review has no remaining material findings.
- [x] CI and Rust Client passed on content head `2ddc39ebdb4d3501de27e65fab6a43bcd05b6928`.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-04T15:42:00Z
head: 2ddc39ebdb4d3501de27e65fab6a43bcd05b6928
branch: docs/OTS-20260804-native-protocol-contract
pr: blakinio/otclient#265
status: ready
context_routes:
  - coordination:OTS-20260804-native-protocol-selection
  - canonical:blakinio/Oteryn-Platform@9035ae987db67c062a8778721a2c8e686ce76750
  - producer-correspondence:blakinio/Otheryn@1807b6210375f6a18afabc817a01ccdfee80ddce
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
proven:
  - protocol-canary remains the existing independent compatibility adapter.
  - protocol-oteryn does not exist and this task adds no code or dependency.
  - Gateway API version is distinct from Game Session, adapter, transport and schema versions.
  - Production Auto submits only exact compiled candidates and consumes the authoritative Gateway result.
  - Native state uses a complete snapshot, strict deltas and no reconnect replay.
  - Platform canonical contract and Otheryn correspondence are merged and pinned exactly.
  - This task changes documentation only.
derived:
  - Rust owns supported-candidate declaration and immutable adapter binding, not production preference or gameplay authority.
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - unrestricted player-selected production protocol
  - first-byte inference or post-selection fallback
  - native dependency on protocol-canary
changed_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
validation:
  - command: CI run 30925007904
    result: PASS
    evidence: exact content head 2ddc39ebdb4d3501de27e65fab6a43bcd05b6928
  - command: Rust Client run 30925007062
    result: PASS
    evidence: exact content head 2ddc39ebdb4d3501de27e65fab6a43bcd05b6928
  - command: independent consumer consistency review
    result: PASS
    evidence: exact offer, endpoint, digest, duplicate, state and rollback rules match merged producer contracts
blockers:
  - exact-head workflows for this final ready-state checkpoint
next_action: verify required checks on final ready-state head, merge PR #265, then archive all linked tasks
```
