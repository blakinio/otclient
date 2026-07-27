---
task_id: OTC-20260727-parallel-wave-transition
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-C
parallel_lane_state: validating
coordinator_task: OTC-20260727-parallel-wave-transition
branch: docs/OTC-20260727-parallel-wave-transition
base_branch: main
created: 2026-07-27T12:45:00+02:00
updated: 2026-07-27T13:15:00+02:00
last_verified_commit: "f0568602f8ab2d806fb5daeb822bc3a9619ede0b"
required_base_commit: "acbc78c618e6998fe29d16833f5c907d8ae8d1e8"
risk: low
related_pr: "#59"
depends_on:
  - merged PR #54 foundation primitives
  - merged PR #58 foundation task archive
  - merged PR #55 multi-agent execution protocol
  - merged PR #57 orchestration task archive
integration_after:
  - "acbc78c618e6998fe29d16833f5c907d8ae8d1e8"
blocks:
  - accurate launch of the next Rust-client parallel wave
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/NEXT_DIAGNOSTICS_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260727-parallel-wave-transition.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged oteryn-foundation primitives from PR #54
crates_touched: []
features_touched: []
contracts_touched:
  - accepted parallel-wave launch plan
  - next bounded Gate 1 diagnostics/redaction package scope
modules_touched: []
reuses:
  - merged multi-agent execution protocol
  - merged foundation primitives and archive evidence
  - Gate 1 package order
  - WS-R14 diagnostics ownership
public_interfaces:
  - coordination and copy-ready agent prompts only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - plan preserves redaction-at-creation and no-secret diagnostics requirements
---

# Goal

Replace the stale launch routing with one current, repository-native parallel plan after foundation PR #54 and archive PR #58 merged. Authorize only the next bounded Gate 1 diagnostics/redaction contract package while retaining the three isolated evidence lanes.

# Confirmed live state

- Current preflight `main`: `acbc78c618e6998fe29d16833f5c907d8ae8d1e8`.
- W1-F foundation implementation merged as PR #54 at `7a68f6e7d92eb6b05078bb001e4881d78544a82b`.
- W1-F task lifecycle archived by PR #58 at the preflight `main`; its shared-path lease is released.
- No open PR owns a greenfield Rust product crate, Cargo/lockfile integration or the diagnostics contract.
- Open PR #48 is an isolated non-merge operational workflow.
- Open PRs #37 and #23 own legacy client asset/UI paths, not the Rust product workspace.
- No live task or PR was found for the Canary, asset-input or Windows-platform evidence lanes.

# Delivered update

- Added `CURRENT_PARALLEL_WAVE.md` as the accepted launch plan and retained `INITIAL_PARALLEL_WAVE.md` as historical evidence.
- Recorded W1-F as merged/archived and explicitly released its shared-path lease.
- Authorized exactly one implementation lane, W2-DIAG, for a bounded `oteryn-diagnostics` structured diagnostics and secret-redaction contract package.
- Carried the Canary, asset-input and Windows-platform work forward only as isolated docs/evidence lanes.
- Added `NEXT_DIAGNOSTICS_AGENT.md` with exact scope, security boundaries, ownership, dependency and validation requirements.
- Updated the coordinator prompt to use current live state and forbid relaunching foundation.
- Updated shared discovery routing to distinguish current and historical wave documents.

# Acceptance criteria

- [x] `CURRENT_PARALLEL_WAVE.md` records the exact post-foundation state and one safe next wave.
- [x] W1-F is marked merged/archived and cannot be relaunched.
- [x] The released Cargo/lockfile/shared-path lease is explicit.
- [x] Exactly one next implementation lane is authorized: a bounded `oteryn-diagnostics` structured diagnostics and secret-redaction contract package.
- [x] The diagnostics package remains separate from product tracing subscribers, global logging, files/network sinks, crash upload, replay implementation and runtime service integration.
- [x] W2-CP, W2-AR and W2-PR are authorized only as isolated docs/evidence lanes.
- [x] Coordinator and diagnostics worker prompts route to the current wave rather than treating PR #54 as active.
- [x] Shared discovery distinguishes the historical initial wave from the current accepted wave.
- [x] No Rust source, Cargo metadata, lockfile, CI, architecture policy, asset, protocol constant or external repository changes occur.
- [x] Complete five-file changed-path/content/link review passed on `f0568602f8ab2d806fb5daeb822bc3a9619ede0b`.
- [ ] Exact-head required documentation/repository CI passes on the final task-record head.
- [ ] Autonomous merge gate is satisfied.

# Design decisions

- A separate current-wave document avoids rewriting the historical first-wave evidence and gives future coordinators one explicit launch target.
- The next implementation package follows Gate 1 order and the merged foundation agent's recommendation: structured diagnostics and secret-redaction contracts before product integration.
- The package is owned by WS-R14 and may consume only merged foundation primitives.
- The `diagnostics` architecture category already exists, so architecture-check changes are not part of the default package.
- One implementation plus three research lanes preserves the initial conservative concurrency profile while the Rust workspace remains young.
- Redaction regression fixtures must use obviously synthetic marker values shaped like sensitive classes; real secrets, endpoints, captures and personal paths remain forbidden.

# Review findings

- Changed paths exactly match the five declared documentation/task owners.
- No edit touches Rust source, Cargo metadata, lockfile, architecture checker, workflow, protocol, assets or legacy runtime.
- Current-wave dependencies and merge SHAs match merged PR #54/#58 evidence.
- Current and historical wave routing is unambiguous.
- Diagnostics scope is bounded to contracts and tests; product logging/sinks/upload/replay/runtime integration are explicitly excluded.
- The diagnostics prompt was clarified so redaction tests use synthetic marker data rather than real secret-bearing fixtures.
- Open PR #48/#37/#23 ownership remains outside these paths and the planned Rust diagnostics lane.

# Non-goals

- no diagnostics crate implementation;
- no Cargo or lockfile edit;
- no tracing dependency selection;
- no global logger/subscriber, sink, uploader, support bundle or replay implementation;
- no launch of worker sessions from this PR;
- no external-repository write;
- no modification of legacy PR ownership.

# Validation

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `acbc78c618e6998fe29d16833f5c907d8ae8d1e8` | live-state preflight | PASS | PR #54/#58 merged and archived; no open Rust product owner; three evidence lanes unclaimed |
| `f0568602f8ab2d806fb5daeb822bc3a9619ede0b` | complete documentation/path/link review | PASS | five declared files; synthetic redaction-fixture wording clarified; no out-of-scope path |
| final task-record head | exact-head repository CI | pending | docs-only package; no runtime claim |

# Remaining work

1. Pass exact-head required checks on this final task-record commit.
2. Mark PR #59 ready, recheck reviews/threads/mergeability and squash-merge.
3. Archive this task separately.

# Handoff

## Start here

- `oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md`
- `oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md`
- `oteryn-client/docs/agents/prompts/NEXT_DIAGNOSTICS_AGENT.md`

## First next action

After this plan and its archive merge, start one coordinator session. It should launch W2-DIAG and only the still-unclaimed evidence lanes after its own fresh preflight.

# Completion

- Final status: awaiting CI
- PR: #59
- Merge commit: pending
- Archived at: pending
