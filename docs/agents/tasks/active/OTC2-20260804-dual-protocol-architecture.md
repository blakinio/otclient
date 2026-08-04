---
task_id: OTC2-20260804-dual-protocol-architecture
coordination_id: OTS-20260804-native-protocol-selection
status: validating
agent: "dual protocol architecture documentation owner"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: WS-R05-WS-R07-architecture
branch: docs/OTC2-20260804-dual-protocol-architecture
base_branch: main
created: 2026-08-04T11:04:00+02:00
updated: 2026-08-04T12:04:00+02:00
last_verified_commit: "1ce81f206b19e17afdc82ef9c943e9caf0e7b0d3"
risk: medium
related_issue: ""
related_prs: [257, 259, 260]
depends_on: []
blocks:
  - future Tokio transport implementation package
  - future protocol-oteryn client/server contract programme
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-dual-protocol-architecture.md
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
  - .github/workflows/otc2-dual-protocol-docs.yml
modules_touched:
  - transport architecture
  - protocol adapter selection
  - protocol-canary
  - protocol-oteryn
reuses:
  - oteryn-client/crates/transport
  - oteryn-client/crates/protocol-core
  - oteryn-client/crates/protocol-canary
  - oteryn-client/crates/game-domain
public_interfaces:
  - ProtocolAdapter boundary
  - ProtocolSelectionPolicy
  - server-advertised protocol capabilities
cross_repo_tasks:
  - future Otheryn producer task under OTS-20260804-native-protocol-selection
shared_path_lease:
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/**
  - .github/workflows/otc2-dual-protocol-docs.yml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
complete_user_facing_feature: false
invocation_started_at: 2026-08-04T11:04:00+02:00
last_progress_at: 2026-08-04T12:04:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: clean-restack-validation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Make future agents follow one explicit direction: retain `protocol-canary` as exact compatibility, build an independent preferred `protocol-oteryn`, map both to neutral gameplay contracts, migrate client I/O separately to Tokio, and select the adapter from authoritative server capabilities without in-session or post-credential downgrade.

# Acceptance criteria

- [x] ADR-001 defines independent adapters, Tokio ownership, automatic selection and downgrade rules.
- [x] `PROTOCOL_BOUNDARY.md` defines adapter/transport/domain separation, bounded action lifecycle and server authority.
- [x] `DUAL_PROTOCOL_EXECUTION_PLAN.md` defines ordered client/server implementation packages and evidence gates.
- [x] `oteryn-client/AGENTS.md` makes the decision and plan mandatory for relevant future work.
- [x] Current code is described honestly: transport remains synchronous and `protocol-oteryn` is not implemented.
- [x] Temporary workflow is scheduled for deletion in the final product diff.
- [ ] Clean current-main diff receives a fresh documentation audit with zero material findings.
- [ ] Exact-head required CI passes, PR #257 merges, task archives and leases release.

# Decisions

| Decision | Boundary |
|---|---|
| Independent `protocol-canary` and `protocol-oteryn` adapters | Neither wraps the other; both map to neutral `GameCommand`/`GameEvent`. |
| Future client transport uses Tokio | Separate measured WS-R05 implementation; current synchronous transport stays valid until merged. |
| Production selection uses server-advertised `Auto` | Prefer mutually supported native Oteryn; Canary only when explicitly supported. |
| Force modes are development/test only | No unrestricted production player switch. |
| One session binds one adapter | No in-session switch or fallback after credential handoff, auth failure, ticket consumption or partial admission. |
| Otheryn keeps ASIO | Server networking changes require a separate profiling-backed ADR. |
| Client sends intent; server owns outcomes | Movement, combat, spells, resources, inventory, loot, economy, RNG and persistence remain authoritative on Otheryn. |

# Current state

- Canonical product PR: #257.
- Clean restack branch: `docs/OTC2-20260804-dual-protocol-architecture-restack`, created from current main `33da70afd159d9b9963e6e9d80398c298b26ff5d`.
- Final intended diff consists only of this task, three normative Rust-client documents, `oteryn-client/AGENTS.md`, and deletion of the temporary workflow.
- Temporary workflow registration PRs #259 and #260 merged after successful exact-head CI runs `30896012843` and `30896670824`; the final product PR removes their workflow.
- No Rust source, Cargo/lockfile, protocol bytes, server implementation, authentication, assets or production state are changed.

# Work log

## 2026-08-04T11:04:00+02:00

- Created task, branch and draft PR #257.
- Verified no ownership overlap with the Canary producer.

## 2026-08-04T11:24:00+02:00

- Registered temporary GitHub-only workflow through PR #259.

## 2026-08-04T11:33:00+02:00

- Repaired the temporary executor through PR #260 after the registration-only no-op.

## 2026-08-04T11:49:00+02:00

- Abandoned repeated workflow retries and applied the bounded documentation directly.
- Added ADR-001, the execution plan, the full protocol boundary and mandatory agent rules.

## 2026-08-04T12:04:00+02:00

- Rebuilt the intended product tree from exact current main to remove stale ancestry and intermediate workflow-only commits.
- Entered final diff audit and exact-head validation.

# Validation

| Head | Check | Result |
|---|---|---|
| `027e215fa25a36110c8056c2196c1e1cfa70046d` | registration scope/review/CI | PASS; one workflow path, 0 threads, run `30896012843` |
| `c66bd30ef6800fb10e11a6532a90d06968d864e4` | executor scope/review/CI | PASS; one workflow path, 0 threads, run `30896670824` |
| pending canonical restack head | changed-path, link, consistency and claim audit | not run |
| pending final head | required repository CI | not run |

# E2E

`NOT_APPLICABLE` — documentation and architecture only; no executable client/server behavior changes.

# Risks and compatibility

- Do not claim Tokio or `protocol-oteryn` is already implemented.
- Canary remains supported and independently versioned.
- Native Oteryn requires linked client/server tasks and exact compatibility evidence.
- No fallback after credential handoff, authentication failure, ticket consumption, protocol violation or partial admission.
- The final product tree must not retain the temporary workflow.

# Remaining work

1. Delete the temporary workflow on the clean restack, force-update the canonical PR branch, audit the exact final diff and run exact-head CI.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 6
  session_id: OTC2-20260804T1104+0200-dual-protocol-docs
  session_started_at: 2026-08-04T11:04:00+02:00
  checkpointed_at: 2026-08-04T12:04:00+02:00
  last_progress_at: 2026-08-04T12:04:00+02:00
  phase: clean-restack-validation
  exact_head: 1ce81f206b19e17afdc82ef9c943e9caf0e7b0d3
  pull_request: 257
  active_operation: clean current-main restack
  external_run_ids: []
  operation_started_at: 2026-08-04T11:56:00+02:00
  wait_deadline_at: null
  check_generation: clean-restack-validation
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: canonical PR branch points to the final clean restack head
  next_action: Delete the temporary workflow on the restack, force-update the canonical branch to the resulting head, then list and audit every PR #257 changed path.
```

# Completion

- Final status: pending
- Product PR: #257
- Temporary PRs: #259 and #260 merged
- Product merge commit: pending
- Archived at: pending
