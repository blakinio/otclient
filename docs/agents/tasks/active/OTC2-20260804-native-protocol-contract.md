---
task_id: OTC2-20260804-native-protocol-contract
status: implementing
branch: docs/OTS-20260804-native-protocol-contract
base_branch: main
created: 2026-08-04
updated: 2026-08-04
related_pr: ""
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
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

Record the Rust client consumer and automatic-selection responsibilities for the canonical native gameplay protocol contract without adding dependencies, creating `protocol-oteryn`, changing transport/runtime or claiming compatibility.

## Acceptance criteria

- The document points to the exact canonical Platform contract and coordination ID.
- The client offer, Gateway-selected result, session binding and no-downgrade behavior map cleanly to protocol-neutral domain/session contracts.
- Canary and native adapters remain independent and one session binds exactly one adapter.
- Later implementation ownership and ordering are explicit.
- Required documentation/governance validation and exact-head CI pass.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-04T14:50:00Z
head: UNKNOWN
branch: docs/OTS-20260804-native-protocol-contract
pr: none
status: implementing
context_routes:
  - coordination:OTS-20260804-native-protocol-selection
  - canonical:blakinio/Oteryn-Platform/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CONTRACT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
proven:
  - protocol-canary is the existing exact compatibility adapter.
  - protocol-oteryn does not exist and is forbidden in this contract-only task.
  - Gateway API protocol_version is distinct from gameplay adapter/profile identifiers.
derived:
  - Rust production Auto selection must consume the authoritative Gateway result rather than infer a protocol from bytes or expose an unrestricted user chooser.
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
validation:
  - command: repository documentation/governance validation
    result: NOT_RUN
    evidence: correspondence documents not yet complete
blockers: []
next_action: add the Rust correspondence document and cross-repository registry entry
```
