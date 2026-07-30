---
task_id: OTC-20260730-w7-entry-contract
status: completed
agent: "W7-ENTRY-CONTRACT worker"
track: greenfield-rust
workstream: account-session-world-directory-game-session
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-ENTRY-CONTRACT
parallel_lane_state: archived
coordinator_task: none
branch: feat/OTC-20260730-w7-entry-contract
base_branch: main
created: 2026-07-30T12:25:00+02:00
updated: 2026-07-30T18:02:39+02:00
last_verified_commit: "e2d4981ffdde493054b794214e7ad69881cf8a5d"
required_base_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
risk: high
related_pr: "#104"
depends_on:
  - W7 plan PR #101 merged as f7ddc2849838df05a95e4d7260bfe7c3359b4c8d
  - W7 plan archive PR #102 merged as 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
owned_paths:
  - oteryn-client/crates/account-session/**
  - oteryn-client/crates/world-directory/**
  - oteryn-client/crates/game-session/**
  - oteryn-client/docs/research/technical-login/W7_ENTRY_CONTRACT_EVIDENCE.md
  - docs/agents/tasks/archive/OTC-20260730-w7-entry-contract.md
shared_path_lease: []
contract_role: producer
contracts_produced:
  - AccountSessionId
  - CharacterId
  - WorldId
  - GameplayChannelId
  - DirectoryRevision
  - GameEntryRequest
  - GameEntryCredential
  - EntryFailure
  - SessionEntered
  - public deterministic entry lifecycle states
contracts_consumed:
  - merged W7 technical-login architecture and accepted wave plan
  - Gateway protocol-v1 signed 64-bit identifier widths as read-only evidence
  - oteryn-foundation monotonic time contracts
crates_touched:
  - account-session
  - world-directory
  - game-session
features_touched:
  - typed account-session generation
  - typed world/character directory identity
  - deterministic one-shot game-entry lifecycle
contracts_touched:
  - sole shared W7 entry contract producer
modules_touched: []
reuses:
  - existing foundation ManualClock, Moment, Deadline and MonotonicClock
  - existing architecture categories and workspace policy
  - exact accepted W7 type ownership
public_interfaces:
  - typed W7 entry/session/directory primitives and lifecycle
cross_repo_tasks: []
performance_evidence:
  - deterministic bounded state-transition tests only; no latency or compatibility claim
security_evidence:
  - credential non-Clone/redacted/move-once/terminal-drop overwrite properties
  - no credential persistence, logging, raw backend text, capture or external-repository write
---

# Result

PR #104 delivered the sole shared W7 entry-contract producer and squash-merged as `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`.

The merged contract contains exactly three Rust packages:

- `oteryn-account-session`, owning non-secret client-local `AccountSessionId`;
- `oteryn-world-directory`, owning bounded signed-64 directory identity, deterministic ordering and validated selection;
- `oteryn-game-session`, owning one-shot redacted credential handoff, typed lifecycle/failures/recovery actions and non-secret `SessionEntered`.

The consumer contract and exact first calls for W7-IDENTITY, W7-CANARY-ENTRY and W7-LOGIN-E2E are documented in `W7_ENTRY_CONTRACT_EVIDENCE.md`. Consumers must restack on the exact producer merge commit above before final compatibility validation.

# Validation

| Evidence | Result |
|---|---|
| final feature head | `e2d4981ffdde493054b794214e7ad69881cf8a5d` |
| Rust Client run `30559239345` | PASS: locked metadata, Rust 1.94 formatting, strict Clippy, all workspace tests, architecture policy and cargo-deny |
| repository CI run `30559239645` | PASS, including required `CI / Required` |
| complete changed-file review | PASS: exactly 13 authorized paths |
| comments, reviews and unresolved threads | none |
| temporary infrastructure residue | none: no workflow, build script or generator path in the final diff |
| squash merge | `9ecc43a4465f6565bc1c12ea61f170a96edcbe35` |

# Preserved boundaries

The completed producer does not establish live Identity, Gateway, transport, Canary packet, browser, native UI, gameplay or production compatibility. It introduces no HTTP, sockets, async runtime, global singleton, adapter-specific field, arbitrary backend control text or secret diagnostic surface.

Credential cleanup is a best-effort safe-Rust overwrite barrier and is not a claim that compiler or runtime copies can never exist.

# Completion

- Final status: completed
- Feature PR: #104
- Producer merge commit: `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`
- Shared-path lease: released by this lifecycle archive
- Lane relaunch: forbidden; future changes require a new accepted task
- Archived at: `docs/agents/tasks/archive/OTC-20260730-w7-entry-contract.md`

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T16:02:39Z
head: pending
branch: docs/archive-OTC-20260730-w7-entry-contract
pr: pending
status: archiving
context_routes:
  - agent-governance
  - rust-entry-contract
  - supply-chain
owned_paths:
  - docs/agents/tasks/archive/OTC-20260730-w7-entry-contract.md
proven:
  - PR #104 squash-merged as 9ecc43a4465f6565bc1c12ea61f170a96edcbe35.
  - Final feature head e2d4981ffdde493054b794214e7ad69881cf8a5d passed Rust Client run 30559239345 and repository CI run 30559239645.
  - The merged implementation contains exactly 13 authorized paths and no final workflow, build-script or generator residue.
  - No reviews, requested changes or unresolved review threads remained at merge.
  - The exact producer merge commit is published for all consumer restacks.
derived:
  - W7-ENTRY-CONTRACT is completed and no longer launchable.
  - The Cargo, lockfile and shared-document lease is released after this archive PR merges.
unknown:
  - archive PR number and archive squash-merge commit until created and merged.
conflicts: []
first_failure:
  marker: none
  evidence: none
changed_paths:
  - docs/agents/tasks/active/OTC-20260730-w7-entry-contract.md
  - docs/agents/tasks/archive/OTC-20260730-w7-entry-contract.md
validation:
  - command: Rust Client run 30559239345
    result: PASS
    evidence: final feature head e2d4981ffdde493054b794214e7ad69881cf8a5d
  - command: Repository CI run 30559239645
    result: PASS
    evidence: final feature head e2d4981ffdde493054b794214e7ad69881cf8a5d
  - command: Squash merge PR #104
    result: PASS
    evidence: producer merge commit 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
blockers:
  - merge this lifecycle archive PR
next_action: Validate the two-path lifecycle diff, merge the archive PR and publish its merge commit.
```
