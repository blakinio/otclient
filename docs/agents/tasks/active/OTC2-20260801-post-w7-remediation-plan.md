---
task_id: OTC2-20260801-post-w7-remediation-plan
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: coordination
phase: discovery-and-plan
branch: docs/OTC2-20260801-post-w7-remediation-plan
base_branch: main
created: 2026-08-01T00:30:20+02:00
updated: 2026-08-01T00:31:51+02:00
last_verified_commit: "10baa1e6eb6364e8975501aeb3eac88e2384e4bc"
required_base_commit: "d23edd0a8395deb586e2b93dd1954bb175243dc4"
risk: high
related_pr: "#122"
depends_on:
  - OTC2-20260731-rust-client-post-w7-audit
  - audit PR #120 merge 97c4f7a1ec581072940ae87697b80a4ec9c53921
  - audit archive PR #121 merge d23edd0a8395deb586e2b93dd1954bb175243dc4
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-post-w7-remediation-plan.md
  - oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md
  - oteryn-client/docs/agents/prompts/NEXT_POST_W7_SECRET_LIFECYCLE_AGENT.md
shared_path_lease: []
contract_role: coordination-only
contracts_produced:
  - post-W7 remediation decomposition, dependency graph, ownership, acceptance and validation plan
  - one first-worker prompt for secret-lifecycle remediation
contracts_consumed:
  - merged post-W7 audit report and validator packet
  - current Rust architecture, lifecycle and multi-agent ownership policy
  - current 19-member Cargo workspace and required CI
crates_touched: []
features_touched: []
contracts_touched:
  - planning metadata only; no Rust, manifest, workflow, architecture-rule or test implementation
implementation_authorized: false
policy_version: 2
task_kind: discovery
context_pressure: medium
decomposition_decision: discovery_first
execution_mode: chat
performance_evidence:
  - no runtime, latency, throughput or compatibility claim
security_evidence:
  - canonical audit evidence reconciled; no secret, credential, private capture or proprietary material added
---

# Goal

Convert the four independently confirmed post-W7 `MEDIUM` findings into the smallest safe remediation execution plan without implementing remediation.

# Verified durable state

- exact planning base/main: `d23edd0a8395deb586e2b93dd1954bb175243dc4`;
- audit PR #120 merged and validated;
- audit archive PR #121 merged and the audit task is archived;
- canonical report and validator both identify exactly `OTC2-AUD-001` through `OTC2-AUD-004` as `MEDIUM`;
- current workspace membership: 19;
- current required Rust checks: `Rust Client / Windows`, `Rust Client / Supply Chain`;
- repository required check: `CI / Required`;
- open PR #23 owns legacy login-shell paths plus shared `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`;
- open PRs #48 and #97 own isolated workflow/task paths;
- no open PR or active task owns the affected Rust production paths or public Rust contracts.

# Accepted decomposition

| Package | Finding | Decision |
|---|---|---|
| `R1-SECRET` | `OTC2-AUD-001` | separate phased security-remediation task; merge first |
| `R2-SHUTDOWN` | `OTC2-AUD-002` | separate phased lifecycle task; consume merged `R1-SECRET` API |
| `R3-ASSET-OPEN` | `OTC2-AUD-003` | separate phased discovery-first task; implementation blocked unless a safe opened-object primitive or mechanically enforced trusted-source contract is proven |
| `R4-ARCH-POLICY` | `OTC2-AUD-004` | separate bounded architecture-policy producer task |

`R1-SECRET` and `R2-SHUTDOWN` are serialized because they overlap Identity, Platform, technical-login evidence and integration tests, but their invariants and rollback boundaries differ.

`R3-ASSET-OPEN` and `R4-ARCH-POLICY` are production-path independent. Concurrent final integration is not authorized by this checkpoint because the asset dependency decision is unresolved, shared documentation remains leased by PR #23 and exact-head heavy CI must be serialized.

# Outputs

- `oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md`
  - live state and authority;
  - four-package decomposition;
  - dependency and merge-order graph;
  - exact production/test/documentation ownership;
  - public producers/consumers;
  - required invariants;
  - timeout and shutdown-state decision;
  - asset-open platform decision gate;
  - complete architecture category/dependency-kind policy requirements;
  - focused/component/heavy validation;
  - rollback boundaries and deferred decisions.
- `oteryn-client/docs/agents/prompts/NEXT_POST_W7_SECRET_LIFECYCLE_AGENT.md`
  - exactly one ready-to-paste Codex prompt for the first authorized package after plan/archive merge.

# Implementation authorization boundary

This task changes documentation only. It does not authorize a worker launch before:

1. this planning PR merges;
2. this planning task is moved to archive in a separate lifecycle PR and that PR merges;
3. a fresh main/open-PR/active-task/path/contract/shared-lease preflight passes.

The first launch is only `R1-SECRET`. No other remediation worker is pre-claimed.

# Validation performed

- required root and nested agent instructions read;
- prompting, execution, checkpoint and multi-agent rules reconciled;
- exact `main`, merged audit/archive PRs and archived audit task verified;
- all live open PRs and their changed/owned paths reconciled;
- canonical audit report and validator result cross-checked;
- current architecture, technical-login lifecycle and affected manifests/source paths reviewed;
- current required CI workflow commands verified;
- plan changed-path scope limited to exactly this task, one plan and one prompt;
- draft planning PR #122 opened from the exact base with three declared changed paths.

No heavy runtime gate is required by task scope. The planning PR still requires all checks emitted for its exact final head.

# Blockers and deferred decisions

- PR #23 retains the shared-document lease for `MODULE_CATALOG.md` and `CHANGELOG.md`; remediation source work may proceed later without those paths, but final integration must wait for lease release or transfer.
- `R3-ASSET-OPEN` must prove safe Windows opened-object semantics before code; another pathname metadata check is prohibited.
- a new zeroization dependency is not pre-approved for `R1-SECRET`.
- no detached/forced worker termination is permitted for `R2-SHUTDOWN`.
- no current member manifest migration is authorized for `R4-ARCH-POLICY`.

# Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T00:31:51+02:00
head: 10baa1e6eb6364e8975501aeb3eac88e2384e4bc
branch: docs/OTC2-20260801-post-w7-remediation-plan
pr: 122
status: validating
proven:
  - Exact main d23edd0a8395deb586e2b93dd1954bb175243dc4 contains merged audit and archive lifecycle state.
  - All four confirmed MEDIUM findings have one exact package disposition.
  - R1-SECRET and R2-SHUTDOWN remain separate and serialized.
  - R3-ASSET-OPEN fails closed at a mandatory platform primitive checkpoint.
  - R4-ARCH-POLICY must classify all 29 categories and normal/build/dev edges explicitly while preserving the current 19-member graph.
  - No remediation implementation, manifest, lockfile, workflow, rule or test path changed.
  - Exactly one first-worker prompt exists.
  - Draft PR #122 contains exactly the declared planning paths at the recorded head.
conflicts:
  - PR #23 owns docs/agents/MODULE_CATALOG.md and docs/agents/CHANGELOG.md; no planning diff overlaps them.
blockers:
  - exact-head planning PR CI and review gate not yet recorded
next_action: Complete the exact-head required CI and review gate for planning PR #122.
```
