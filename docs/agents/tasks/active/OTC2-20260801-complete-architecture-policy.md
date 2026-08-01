---
task_id: OTC2-20260801-complete-architecture-policy
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: architecture
phase: implementation
branch: fix/OTC2-20260801-complete-architecture-policy
base_branch: main
created: 2026-08-01T11:50:00+02:00
updated: 2026-08-01T11:50:00+02:00
last_verified_commit: "f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63"
required_base_commit: "f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63"
risk: high
related_pr: null
depends_on:
  - OTC2-20260801-nonblocking-shutdown-remediation
  - R2 implementation merge 296a45437bc4e2c546e5cef23f0f1a0a01571fd8
  - R2 archive merge f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63
blocks:
  - OTC2-20260801-safe-asset-open-remediation
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-complete-architecture-policy.md
  - oteryn-client/tools/architecture-check/src/lib.rs
  - oteryn-client/tools/architecture-check/tests/policy_fixtures.rs
  - oteryn-client/tests/architecture-fixtures/
  - oteryn-client/docs/architecture/decisions/2026-08-01-complete-dependency-allow-policy.md
shared_path_lease: []
modules_touched:
  - Rust workspace architecture checker
crates_touched:
  - oteryn-architecture-check
features_touched:
  - dependency category allow policy
  - dependency kind parsing
reuses:
  - existing 29-category catalogue
  - existing cargo metadata and fixture parsers
  - existing stable violation code E005_FORBIDDEN_EDGE
contracts_produced:
  - complete normal/build/dev category policy
  - exhaustive category-pair policy tests
contracts_consumed:
  - current 19-member Rust workspace graph
contracts_touched:
  - fixture schema dependency representation
  - architecture edge validation
implementation_authorized: true
policy_version: 2
task_kind: implementation
context_pressure: medium
decomposition_decision: single-package
execution_mode: codex
performance_evidence:
  - no latency or throughput claim
security_evidence:
  - no private data or external artifact required
---

# Goal

Remediate `OTC2-AUD-004` by replacing the partial category denylist with one complete dependency policy covering all 29 known categories and normal, build and dev dependency kinds.

# Acceptance

- every category pair has an explicit allow/deny result for each dependency kind;
- cargo metadata and fixture parsing retain dependency kind;
- production crates cannot normally depend on `tool`;
- dev dependencies may target `tool`;
- build dependencies fail unless explicitly allowed by policy;
- `E005_FORBIDDEN_EDGE` remains the stable violation code;
- exhaustive positive/negative tests cover all category pairs and kinds;
- the unchanged current 19-member workspace graph passes;
- no manifest, lockfile or workspace dependency change.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T11:50:00+02:00
head: f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63
branch: fix/OTC2-20260801-complete-architecture-policy
pr: null
status: active
context_routes:
  - docs/agents/AGENTS.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md
  - oteryn-client/tools/architecture-check/src/lib.rs
  - oteryn-client/tools/architecture-check/tests/policy_fixtures.rs
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-complete-architecture-policy.md
  - oteryn-client/tools/architecture-check/src/lib.rs
  - oteryn-client/tools/architecture-check/tests/policy_fixtures.rs
  - oteryn-client/tests/architecture-fixtures/
  - oteryn-client/docs/architecture/decisions/2026-08-01-complete-dependency-allow-policy.md
proven:
  - Current checker recognizes 29 category names but uses a partial forbidden_edge denylist.
  - Dependency kind is absent from the internal graph and fixture schema.
  - Open PRs 23, 48 and 97 do not touch owned architecture-check paths.
derived:
  - One isolated implementation package can remediate AUD-004 without manifest edits.
unknown:
  - Exact allowed matrix required to preserve every edge in the current 19-member workspace graph.
conflicts: []
first_failure:
  marker: not-run
  evidence: Implementation has not started.
rejected_hypotheses:
  - Extending the existing denylist is sufficient.
  - Dependency kind can be ignored safely.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-complete-architecture-policy.md
validation:
  - command: fresh overlap and ownership preflight
    result: PASS
    evidence: main f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63; no open PR owns architecture-check paths.
blockers: []
next_action: Open the draft PR, reconstruct the current graph and implement the complete policy.
```
