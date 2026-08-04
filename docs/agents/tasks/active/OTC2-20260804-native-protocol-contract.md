---
task_id: OTC2-20260804-native-protocol-contract
status: validating
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

- [x] Canonical Platform contract, Otheryn correspondence and coordination ID are linked.
- [x] Offer, Gateway selection, opaque session binding and no-downgrade behavior map to protocol-neutral layers.
- [x] Canary and native adapters remain independent and one session binds one immutable adapter.
- [x] Snapshot/delta, action result, duplicate and replacement-session behavior is explicit.
- [x] Later implementation ownership and ordering are explicit.
- [x] Independent consistency review has no remaining material findings.
- [ ] Exact-head CI and Rust Client workflows pass after the final checkpoint commit.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-04T15:32:00Z
head: 9779bb7ac1cb864894ba7cb293b02ce6afcd851b
branch: docs/OTS-20260804-native-protocol-contract
pr: blakinio/otclient#265
status: validating
context_routes:
  - coordination:OTS-20260804-native-protocol-selection
  - canonical-pr:blakinio/Oteryn-Platform#519
  - producer-correspondence:blakinio/Otheryn#356
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-native-protocol-contract.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
proven:
  - protocol-canary remains the existing independent compatibility adapter.
  - protocol-oteryn does not exist and this task adds no code or dependency.
  - Gateway API version is distinct from Game Session, adapter, transport and schema versions.
  - Production Auto must submit only compiled exact candidates and consume the authoritative Gateway result.
  - Native state uses a complete snapshot, strict deltas and no reconnect replay.
  - This task changes documentation only.
derived:
  - The Rust client owns supported-candidate declaration and immutable adapter binding, not the production preference or gameplay authority.
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
  - command: CI run 30924210250
    result: PASS
    evidence: content head 9779bb7ac1cb864894ba7cb293b02ce6afcd851b
  - command: Rust Client run 30924207588
    result: IN_PROGRESS
    evidence: content head 9779bb7ac1cb864894ba7cb293b02ce6afcd851b before final checkpoint
  - command: independent consumer consistency review
    result: PASS
    evidence: offer, endpoint, digest, command duplicate, strict delta and rollback rules align with canonical contract
blockers:
  - Platform and Otheryn PRs must merge first
  - exact-head CI and Rust Client workflows for the checkpoint commit
next_action: verify exact-head workflows, then refresh exact merged producer revisions and merge last
```
