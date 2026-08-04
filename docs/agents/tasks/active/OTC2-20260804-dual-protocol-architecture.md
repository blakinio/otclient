---
task_id: OTC2-20260804-dual-protocol-architecture
coordination_id: OTS-20260804-native-protocol-selection
status: ready-for-review
agent: "dual protocol architecture documentation owner"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: WS-R05-WS-R07-architecture
branch: docs/OTC2-20260804-dual-protocol-architecture
base_branch: main
created: 2026-08-04T11:04:00+02:00
updated: 2026-08-04T12:24:00+02:00
last_verified_commit: "a1d6a6b6cb56b9e8f362190ad6d7521130a27834"
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
last_progress_at: 2026-08-04T12:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: merge-ref-revalidation
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
- [x] Temporary workflow is deleted in the final product diff.
- [x] Clean current-main diff received a fresh documentation audit with zero material findings.
- [ ] Current merge-ref exact-head checks pass, PR #257 merges, task archives and leases release.

# Normative decisions

- `protocol-canary` and `protocol-oteryn` are independent adapters over common `GameCommand` / `GameEvent` contracts.
- Future client I/O uses a separately measured, application-owned Tokio runtime; the current synchronous transport remains valid until that package merges.
- Production uses authoritative server-advertised `Auto`; force modes are development/test only.
- One game-entry attempt and session bind exactly one adapter. No in-session switch or fallback after credential handoff, authentication failure, ticket consumption, protocol violation or partial admission.
- Otheryn keeps ASIO unless a separate profiling-backed ADR changes server networking.
- The client sends player intent; the server owns movement, combat, spells, resources, inventory, loot, economy, RNG and persistence outcomes.

# Final scope audit

Compared `main@33da70afd159d9b9963e6e9d80398c298b26ff5d` with product content head `4f1675d95d20650c25e5e1999285bc046440e405`.

Exact paths:

1. `.github/workflows/otc2-dual-protocol-docs.yml` — deleted;
2. this task — added;
3. `oteryn-client/AGENTS.md` — updated;
4. `oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md` — added;
5. `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md` — updated;
6. `oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md` — added.

Audit: `PASS`; material findings: `0`; review threads: `0`.

Verified no Rust, Cargo, lockfile, packet-byte, authentication, server, asset or production-state change; all relative links resolve; current-versus-future claims are explicit; authority and downgrade rules are consistent; temporary workflow is absent from the product tree.

# Validation

| Head | Check | Result |
|---|---|---|
| `027e215fa25a36110c8056c2196c1e1cfa70046d` | temporary registration scope/review/CI | PASS; run `30896012843` |
| `c66bd30ef6800fb10e11a6532a90d06968d864e4` | temporary executor scope/review/CI | PASS; run `30896670824` |
| `4f1675d95d20650c25e5e1999285bc046440e405` | documentation audit | PASS; 6 expected paths, 0 material findings |
| `a1d6a6b6cb56b9e8f362190ad6d7521130a27834` | repository CI | PASS; run `30898205092`, required job `91956427880` |
| `a1d6a6b6cb56b9e8f362190ad6d7521130a27834` | Rust Client | PASS; run `30898195226` |
| resulting checkpoint head | current merge-ref validation | pending |

The previous exact-head runs passed, but GitHub recalculated the synthetic PR merge ref before merge and the repository rule reported `CI / Required` as expected. This checkpoint creates one new synchronize generation; no PR metadata will change after its checks complete.

# E2E

`NOT_APPLICABLE` — documentation and architecture only.

# Remaining work

1. Observe the current synchronize generation; merge only when repository CI and Rust Client pass, the PR head remains unchanged, mergeability is true and review threads remain zero.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 8
  session_id: OTC2-20260804T1104+0200-dual-protocol-docs
  session_started_at: 2026-08-04T11:04:00+02:00
  checkpointed_at: 2026-08-04T12:24:00+02:00
  last_progress_at: 2026-08-04T12:24:00+02:00
  phase: merge-ref-revalidation
  exact_head: a1d6a6b6cb56b9e8f362190ad6d7521130a27834
  pull_request: 257
  active_operation: current synchronize generation required checks
  external_run_ids: []
  operation_started_at: 2026-08-04T12:24:00+02:00
  wait_deadline_at: 2026-08-04T13:09:00+02:00
  check_generation: merge-ref-revalidation
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: current head repository CI and Rust Client reach terminal results
  next_action: Fetch PR #257 current head and its workflow runs; merge without further PR metadata changes only if required checks are green and all gates remain satisfied.
```

# Completion

- Final status: pending
- Product PR: #257
- Temporary PRs: #259 and #260 merged
- Product merge commit: pending
- Archived at: pending
