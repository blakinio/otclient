---
task_id: OTC2-20260801-playability-p0-release
status: active
agent: "P0 release E2E worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-release
phase: validation
branch: docs/OTC2-20260801-playability-p0-release
base_branch: main
created: 2026-08-01T19:03:00+02:00
updated: 2026-08-01T19:18:00+02:00
last_verified_commit: "e944a445ffd79eddba674816d734ada22151e449"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: high
related_pr: 144
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md
  - oteryn-client/docs/research/playability/p0/staging-e2e-and-release-plan.md
  - oteryn-client/docs/research/playability/p0/performance-reliability-acceptance.md
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

Define the controlled staging, Windows runtime, E2E, performance, reliability, packaging and release evidence required for M1-M6 without deploying, using credentials or inventing production claims.

# Result

The lane produced two evidence contracts:

- `staging-e2e-and-release-plan.md` defines exact M1-M6 start states, sequences, observables, negative scenarios, evidence classes, privacy boundaries and release dependency order;
- `performance-reliability-acceptance.md` defines named-environment measurement records, candidate hardware tiers, frame/lifecycle distributions, reproducible scenes, memory/resource methods, network degradation, fault/device-loss, repeated lifecycle, soak, packaging/update and artifact-retention acceptance.

The reports preserve the current boundary: repository tests prove a synthetic technical-login lifecycle and hosted Windows compilation, not interactive desktop, real staging, gameplay, GPU/hardware or production release compatibility. They identify the conflicting historical Canary cuts as a dependency for PR #140 rather than selecting one by assumption.

# Scope

Read-only investigation of current CI/runner/operations, W7 technical-login evidence, deployment contracts and relevant platform/renderer/asset/runtime boundaries. No deployment, account/credential use, infrastructure mutation, workflow, code, manifest or proprietary artifact change occurred.

# Acceptance

- [x] M1-M6 have named start state, fixtures, sequence, observables and evidence classes;
- [x] controlled technical-login prerequisites and secret-safe artifact rules are explicit;
- [x] Windows hardware/driver/input/IME/audio acceptance candidates are named;
- [x] performance, network-loss, device-loss, soak and rollback methodology is actionable without invented budgets;
- [x] delivery dependencies, privacy rules and owner decisions are separated;
- [ ] only the three owned paths change and exact-head required validation passes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:18:00+02:00
head: e944a445ffd79eddba674816d734ada22151e449
branch: docs/OTC2-20260801-playability-p0-release
pr: 144
status: validating
context_routes:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/prompts/P0_RELEASE_E2E_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md
  - oteryn-client/docs/research/playability/p0/staging-e2e-and-release-plan.md
  - oteryn-client/docs/research/playability/p0/performance-reliability-acceptance.md
proven:
  - Current launch base is 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2 and coordinator merge is 21f0725f0beb46775951dd17f2587c67ebcdee12.
  - Rust CI proves locked metadata, formatting, strict Clippy, all-target tests, architecture policy and supply-chain checks on hosted Windows/Ubuntu.
  - The technical-login integration is original synthetic fake-service evidence through ordered 0x0F and shutdown only.
  - W4 shell and W5 renderer reports explicitly leave interactive Windows, DPI, IME, physical input, named GPU/driver, device loss and performance unproven.
  - Existing client configuration is explicit opt-in with no hidden production endpoint or account default.
  - The reports define M1-M6 evidence, privacy and reliability methods without deployment or final budget claims.
derived:
  - Exact Canary compatibility must consume the producer cut accepted by PR #140.
  - M1 requires matching client and server evidence for one controlled admission and teardown.
  - Final platform, performance, soak, asset, privacy and signing decisions require named owners after baseline evidence.
unknown:
  - Exact live Canary producer revision/profile/build.
  - Approved staging environment and disposable test account/character path.
  - Final Windows support matrix and product performance/reliability budgets.
  - Approved production asset source, telemetry policy and signing/release process.
conflicts:
  - Historical architecture and workspace documents cite different Canary source cuts; no compatibility cut is selected here.
first_failure:
  marker: none
  evidence: discovery completed without an implementation or ownership conflict.
rejected_hypotheses:
  - Treat synthetic E2E or compile CI as production readiness: rejected because controlled runtime evidence is required.
  - Convert preliminary engineering frame targets into product gates: rejected until named scene/hardware baselines and owner approval exist.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md
  - oteryn-client/docs/research/playability/p0/staging-e2e-and-release-plan.md
  - oteryn-client/docs/research/playability/p0/performance-reliability-acceptance.md
validation:
  - command: live ownership and launch-gate preflight
    result: PASS
    evidence: PR #48/#97 paths are disjoint and read-only; no shared lease exists.
  - command: exact source and policy evidence review
    result: PASS
    evidence: W7 architecture, build matrix, performance strategy, CI workflows, workspace operations, W4/W5 runtime evidence, app configuration and synthetic integration tests were reconciled.
  - command: privacy and unsupported-claims review
    result: PASS
    evidence: reports prohibit credentials/private captures/proprietary bytes, separate synthetic from runtime proof and leave product decisions explicit.
blockers:
  - Real M1 execution requires the exact Canary cut accepted by PR #140.
  - Real staging/account access requires operations and security owner authorization outside this discovery task.
  - Final budgets, platform matrix, asset rights, privacy and signing remain owner decisions after later evidence.
next_action: Run exact-head validation and clean review for PR #144, then merge and archive the release discovery lane.
```
