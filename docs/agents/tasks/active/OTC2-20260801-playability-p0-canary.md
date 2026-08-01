---
task_id: OTC2-20260801-playability-p0-canary
status: active
agent: "P0 Canary capability worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-canary
phase: validation
branch: docs/OTC2-20260801-playability-p0-canary
base_branch: main
created: 2026-08-01T18:59:00+02:00
updated: 2026-08-01T19:56:00+02:00
last_verified_commit: "1e2e3292cf1aeefc80e0b8e5060a8de7a5b24eb5"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: high
related_pr: 140
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md
  - oteryn-client/docs/research/playability/p0/canary-capability-inventory.md
  - oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: work
context_pressure: high
decomposition_decision: single
validation_level: focused
---

# Goal

Produce an exact-revision, source-backed inventory of post-admission Canary Current-profile capabilities and a safe fixture-acquisition plan for bounded future protocol packages.

# Result

The lane produced:

- `canary-capability-inventory.md` — exact producer cut/profile/transport/feature facts and bounded capability families from bootstrap/map through common gameplay and optional modern systems;
- `canary-fixture-acquisition-plan.md` — generated source index, deterministic producer/synthetic fixtures, controlled project-owned runtime evidence, privacy rules, negative corpus, state harness and package ownership.

The report pins `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`, Canary release `3.6.1`, client version `1525`, modern-port `ProtocolProfileId::Current`, but does not claim that this is already the deployed staging/production cut. It does not hand-copy numeric opcodes; future implementation must mechanically index the exact dispatch/layout source and fixtures.

# Scope

Read-only investigation of exact Canary producer sources and current Rust protocol boundaries. No client/server code, protocol, capture, asset, manifest, workflow or external repository change occurred.

# Acceptance

- [x] exact producer repository, revision, profile and relevant source paths are named;
- [x] every major post-admission capability family is mapped to evidence, `UNKNOWN` or a named blocker;
- [x] ordering/state dependencies and future bounded package seams are explicit;
- [x] fixture provenance, privacy and sanitization rules are actionable;
- [ ] only the three owned paths change;
- [ ] checkpoint validator, independent document review and exact-head required CI pass.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:56:00+02:00
head: 1e2e3292cf1aeefc80e0b8e5060a8de7a5b24eb5
branch: docs/OTC2-20260801-playability-p0-canary
pr: 140
status: validating
context_routes:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/prompts/P0_CANARY_CAPABILITY_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md
  - oteryn-client/docs/research/playability/p0/canary-capability-inventory.md
  - oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
proven:
  - Exact inspected producer is blakinio/canary at bc0068ab80bbf003e128fce0589b4cc89d2682d3.
  - core.hpp identifies server release 3.6.1 and client version 1525.
  - The configured modern game port selects enabled ProtocolProfileId::Current.
  - Current uses server challenge, sequence checksums, official compression and explicit modern feature flags.
  - ProtocolGame declarations expose bootstrap, map, entity, movement, player, item/container, chat, combat, social, economy and modern feature families.
  - Session hints bind profile, account-session hash, character set, connection behavior and expiry through a claim/consume lease.
  - The reports require generated exact-source indexes and safe deterministic fixtures instead of hand-written opcode assumptions.
derived:
  - Shared game IDs/events/commands must merge before bounded Canary parser packages.
  - M2 likely begins with bootstrap, map, entity, movement, base player and minimum visual fixtures.
  - Build-specific Current layouts require exact supported build-string fixtures.
unknown:
  - Exact deployed Canary commit/configuration/build string.
  - Mechanically generated numeric opcode/layout index and exact bootstrap order.
  - Runtime-enabled/configured subset of optional systems and final release-required classification.
conflicts:
  - Historical client documents cited older differing Canary cuts; this inventory uses the current inspected exact source cut but does not claim deployment equality.
first_failure:
  marker: none
  evidence: exact producer source was accessible and discovery completed without ownership conflict.
rejected_hypotheses:
  - Infer opcodes/capabilities from the legacy client alone: rejected because exact producer source is authoritative.
  - Copy a numeric opcode table manually into this report: rejected because it would be stale/profile-mixed without mechanical generation and fixtures.
  - Treat every declared server method as a release requirement: rejected pending configuration and product classification.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-canary.md
  - oteryn-client/docs/research/playability/p0/canary-capability-inventory.md
  - oteryn-client/docs/research/playability/p0/canary-fixture-acquisition-plan.md
validation:
  - command: live ownership and launch-gate preflight
    result: PASS
    evidence: lane owns three disjoint documentation paths and no shared lease.
  - command: exact Canary producer source review
    result: PASS
    evidence: core, profile, profile registry, port routing, session hint and ProtocolGame declaration/implementation sources were reconciled at bc0068ab.
  - command: privacy, fixture and unsupported-claims review
    result: PASS
    evidence: official/private captures, credentials, session keys and proprietary bytes are prohibited; deployment and product scope remain explicit unknowns.
blockers:
  - Real compatibility requires owner/operations to name the deployed exact producer/configuration/build.
  - Implementation requires a generated dispatch/layout index and deterministic fixtures.
  - Product scope and production asset compatibility require P0 aggregation plus PR #141/#142 evidence.
next_action: Run exact-head validation and clean review for PR #140, then merge and archive the Canary discovery lane.
```
