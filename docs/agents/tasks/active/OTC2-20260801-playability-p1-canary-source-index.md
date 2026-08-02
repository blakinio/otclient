---
task_id: OTC2-20260801-playability-p1-canary-source-index
status: validating
agent: "P1 Canary source-index worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-canary-source-index
phase: exact-head-validation
branch: tools/OTC2-20260801-playability-p1-canary-source-index
base_branch: main
created: 2026-08-01T22:25:00+02:00
updated: 2026-08-02T22:28:00+02:00
last_verified_commit: "724994eeebbcec3ac6c76287bbdabe495fd80284"
required_base_commit: "3887a0b7369e99ad200990d42a5314f1d5531e97"
risk: high
related_pr: 154
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
  - oteryn-client/tools/canary-protocol-index/**
  - oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
  - oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
shared_path_lease: []
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: github-only
context_pressure: high
decomposition_decision: single
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - bounded runtime Canary parsers and encoders
  - controlled packet fixtures and approved staging identity
  - proof that the inspected producer cut equals deployment
---

# Goal

Implement the deterministic exact-source Canary Current index and privacy-safe fixture-feasibility evidence defined by `P1_CANARY_SOURCE_INDEX_AGENT.md`.

# Source boundary

Accepted and mechanically inspected producer cut:

```text
blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3
Canary 3.6.1
client version 1525
ProtocolProfileId::Current
```

The result is source evidence, not a deployment-equality or runtime-compatibility claim.

# Acceptance

- [x] deterministic standard-library generator and unit corpus exist under the owned tool path;
- [x] two clean exact-source generations are byte-identical;
- [x] normalized direction, dispatch phase, opcode, handler/send, source, gate, state and proposed package fields are generated;
- [x] `livestream-viewer`, `gameplay-session` and `server-send` phases prevent false opcode conflicts;
- [x] literal, inline, no-op, indirect/orchestrator and unknown-local-opcode cases are explicit;
- [x] zero inbound dispatches and zero declarations remain unresolved;
- [x] representative bootstrap/map/entity/movement/player/items/containers/chat/combat/modern paths are present with exact source anchors;
- [x] fixture feasibility and provenance rules forbid credentials, session keys, private captures, proprietary assets and copied producer bodies;
- [x] no workspace member, root manifest, lockfile, architecture, runtime or producer-repository mutation;
- [ ] retained repository CI and clean review gate pass;
- [ ] PR is merged and the task is separately archived.

## Result summary

```yaml
producer:
  repository: blakinio/canary
  revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
  release: 3.6.1
  client_version: 1525
  profile: Current
index:
  total_entries: 347
  client_to_server: 159
  server_to_client: 188
  literal_inbound: 122
  inline_inbound: 31
  explicit_noop_inbound: 6
  unresolved_inbound: 0
  literal_outbound: 174
  outbound_without_local_literal: 14
  defined_indirect_orchestrators: 4
  declarations_without_definition: 0
fixture_families: 15
unclassified_review_entries: 59
```

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T22:28:00+02:00
head: 724994eeebbcec3ac6c76287bbdabe495fd80284
branch: tools/OTC2-20260801-playability-p1-canary-source-index
pr: 154
status: validating
phase: exact-head-validation
context_routes:
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
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
  - Exact main 3887a0b7 is in branch history and this lane requires no shared integration lease.
  - Seven changed paths are exactly the task, tool, generated JSON and two evidence reports.
  - The generator reads seven pinned producer source files and records their SHA-256 hashes.
  - Dispatch opcodes are scoped by livestream-viewer/gameplay-session phase; outbound methods use server-send phase.
  - Current profile exposes sixteen mechanically extracted ProtocolFeature values.
  - Representative source anchors cover bootstrap/ping/logout, map/teleport, entity, movement/autowalk, player, items, containers, chat, combat and modern-feature methods.
  - Methods not safely assigned to a bounded family remain in protocol-canary-unclassified-review rather than being guessed.
  - Temporary generation PR 179 is closed without merge with zero final changed files.
derived:
  - The index can seed later bounded protocol packages but cannot itself prove deployed ordering, configuration or wire equality.
  - The fourteen outbound methods without a local literal require direct source review by their consuming package before wire implementation.
unknown:
  - Exact deployed Canary revision/configuration/build and approved controlled fixture environment remain owner/operations inputs.
conflicts: []
first_failure:
  marker: dispatch extraction audit
  evidence: initial output conflated duplicate opcodes across two switches and classified grouped no-op/helper declarations imprecisely.
  causal_hypothesis: dispatch phase and indirect-helper semantics were absent from the first model.
  repair: phase-aware switch extraction, explicit no-op boundaries, source-defined indirect classification and send/resend recognition; final unresolved counts are zero.
rejected_hypotheses:
  - Infer deployment equality from the inspected source cut: rejected.
  - Copy producer method bodies or packet captures: rejected by security/privacy boundary.
  - Assign unclassified methods from neighboring opcode/family names: rejected; manual review remains explicit.
  - Treat sends without a local literal opcode as numeric evidence: rejected; opcode remains UNKNOWN.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
  - oteryn-client/tools/canary-protocol-index/README.md
  - oteryn-client/tools/canary-protocol-index/generate.py
  - oteryn-client/tools/canary-protocol-index/test_generate.py
  - oteryn-client/tools/canary-protocol-index/generated/current-index.json
  - oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
  - oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
validation:
  - command: initial exact-source generation run 30764947711 / job 91541870308
    result: PASS_WITH_AUDIT_FINDINGS
    evidence: three unit tests, two byte-identical generations and 347 entries; later audit required phase/helper refinement.
  - command: phase/helper refinement run 30765251078 / job 91542723692
    result: PASS_WITH_ONE_EXTRACTOR_FINDING
    evidence: phase separation and zero missing definitions; one resend and grouped-last-case vocabulary gap remained.
  - command: final exact-source run 30765540499 / job 91543471615
    result: PASS
    evidence: four unit tests, two byte-identical generations, 347 entries, six no-op inbound cases, zero unresolved inbound and zero missing definitions.
  - command: exact changed-path, source-anchor, claim-boundary and fixture-provenance audit
    result: PASS
    evidence: seven exclusive paths; no runtime/workspace/producer changes, captures, credentials, assets or copied method bodies.
blockers: []
next_action: Inspect retained repository CI on this checkpoint head, then mark ready, auto-merge and archive separately when the review gate remains clean.
```
