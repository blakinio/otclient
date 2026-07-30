---
task_id: OTC-20260730-w7-entry-postmerge-reconcile
status: ready
agent: "W7 entry post-merge reconciliation worker"
track: greenfield-rust
workstream: agent-governance
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-ENTRY-POSTMERGE-DOCS
branch: docs/OTC-20260730-w7-entry-postmerge-reconcile
base_branch: main
created: 2026-07-30T20:03:00+02:00
updated: 2026-07-30T20:19:00+02:00
last_verified_commit: "82c6c5e9b58d72fd821f909f3a0d9d4cdad2ad7f"
risk: low
related_pr: "#106"
depends_on:
  - W7 entry producer PR #104 merged as 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - W7 entry lifecycle archive PR #105 merged as 8dcd353d5a9f19fabccf49508c27074f7749e3cf
owned_paths:
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/README.md
  - docs/agents/tasks/archive/OTC-20260730-w7-entry-contract.md
  - docs/agents/tasks/active/OTC-20260730-w7-entry-postmerge-reconcile.md
shared_path_lease:
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/README.md
modules_touched: []
reuses:
  - merged producer and lifecycle evidence from PRs #104 and #105
  - accepted W7 dependency ordering in CURRENT_PARALLEL_WAVE.md
depends_on_tasks: []
blocks: []
cross_repo_tasks: []
---

# Objective

Remove the remaining pre-merge W7-ENTRY governance state after the producer and lifecycle archive merged.

# Scope

- mark the W7 entry contracts as merged and archived in the module catalogue;
- replace the obsolete blanket W7 authorization statement with the current producer/consumer state;
- finalize the archived producer task checkpoint with the archive merge commit and no remaining blocker;
- make no Rust, Cargo, workflow, protocol or compatibility change.

# Acceptance

- no document describes PR #104 as active;
- the exact producer commit `9ecc43a4465f6565bc1c12ea61f170a96edcbe35` and archive commit `8dcd353d5a9f19fabccf49508c27074f7749e3cf` are published consistently;
- W7 consumers are described as requiring a fresh overlap check and exact producer restack, not as globally unauthorized;
- the final changed-file list contains no workflow helper;
- changed-file review and required exact-head CI are green;
- the task is squash-merged and archived in a separate lifecycle PR.

# Current state

Preflight found no open PR owning these paths. Open PR #97 touches only its workflow and task record; PRs #23 and #48 do not own Rust governance documents.

Draft PR #106 is open from the dedicated task branch. The three governance documents are reconciled. A temporary workflow experiment did not run and was removed before any document update; it is absent from the final branch diff.

# Validation

- module catalogue records merged PR #104, archive PR #105 and exact producer merge `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`;
- coordination README records the completed producer and current consumer launch/restack gates;
- archived producer task records archive commit `8dcd353d5a9f19fabccf49508c27074f7749e3cf`, `status: archived`, `unknown: []`, `blockers: []` and a current next action;
- full changed-file review: PASS, exactly four authorized documentation paths and no workflow helper;
- repository CI run `30569670340` / CI #911 on head `82c6c5e9b58d72fd821f909f3a0d9d4cdad2ad7f`: PASS, including `CI / Required`; Windows correctly skipped for docs-only scope;
- reviews and unresolved threads: pending final check immediately before readiness.

# Next action

Require green exact-head CI for this checkpoint commit, verify current `main` and review threads, mark PR #106 ready and squash-merge, then archive this reconciliation task separately.
