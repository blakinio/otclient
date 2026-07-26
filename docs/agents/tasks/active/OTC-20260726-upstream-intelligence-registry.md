---
task_id: OTC-20260726-upstream-intelligence-registry
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-upstream-intelligence-registry
base_branch: main
created: 2026-07-26
updated: 2026-07-26
last_verified_commit: "ca78b71397cd2196ab841144c27275d0462902d7"
risk: low
related_issue: ""
related_pr: ""
depends_on: []
blocks: []
owned_paths:
  - docs/agents/programs/OTCLIENT_UPSTREAM_INTELLIGENCE.md
  - artifacts/upstream/otclient/candidates.json
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260726-upstream-intelligence-registry.md
modules_touched:
  - OTClient upstream intelligence governance
reuses:
  - existing agent task and archival lifecycle
  - existing archived upstream synchronization evidence
  - existing GitHub code/PR/issue comparison process
public_interfaces:
  - canary-otclient-upstream-candidates-v1
cross_repo_tasks: []
---

# Goal

Create a durable human-readable and machine-readable OTClient upstream intelligence
registry so future audits update Git instead of relying on chat history.

# Acceptance criteria

- [ ] The 2026-07-17 baseline and current target/upstream/fork tips are recorded.
- [ ] All tracked candidates have explicit priority, status, disposition and local state.
- [ ] Deduplicated, watch and untriaged items remain explicit.
- [ ] Future audits have an update workflow and no implementation authority is implied.
- [ ] JSON parses deterministically and Markdown/path review succeeds.
- [ ] Open PR/path ownership has been checked and overlaps avoided.
- [ ] Applicable exact-head GitHub checks pass.
- [ ] Full diff is reviewed and the autonomous merge gate is satisfied.

# Confirmed context

- Current target `main` is `ca78b71397cd2196ab841144c27275d0462902d7`.
- Current upstream `main` is `e1a1ff150332b8879c91d46d8dc1402e78af9c3e`.
- The baseline common tip is `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`.
- Target and upstream are respectively 37 and 24 commits after that common tip.
- Local PR #26 already integrated selected reviewed upstream effects.
- Local PR #35 and archive PR #42 completed the Forge scheduled-event lifecycle fix.
- Local PR #34 and archive PR #41 completed Wheel conviction index repair.
- PR #37 owns `docs/agents/CHANGELOG.md`; this task deliberately leaves that path unchanged.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Agent governance | task/PR/merge lifecycle | `AGENTS.md`, `docs/agents/**` | Provides persistent discoverability and merge gates. |
| Upstream sync #26 | accepted/deferred decisions | `docs/agents/tasks/archive/OTC-20260725-upstream-sync-16.md` | Prevents re-importing excluded effects blindly. |
| Existing audit history | candidate baseline | 2026-07-17 audit context | Supplies the initial durable registry population. |

# Ownership and overlap check

- Open PRs inspected: #37 client assets, #36 options Phase 0, #23 login-shell prototype.
- Active task ownership inspected for PR #37; its `CHANGELOG.md` ownership is avoided.
- Overlaps: none in the programme, machine registry or README paths.
- Resolution: documentation-only branch with no runtime, protocol, asset or UI changes.

# Current state

The audit state exists in chat/project context and scattered task records but has no single
durable candidate ledger in the repository.

# Plan

1. Add the programme document and deterministic JSON registry.
2. Register the programme in `docs/agents/README.md`.
3. Parse JSON and review the exact branch diff.
4. Open a PR, observe applicable checks, archive this task and squash-merge.

# Work log

## 2026-07-26

- Completed repository, open-PR and active ownership preflight.
- Revalidated target/upstream tips and the latest watched-fork tips.
- Chose a docs/data-only registry rather than a new scanner or runtime component.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep Markdown and JSON together | Humans need rationale; agents need deterministic structured state. | none |
| Store exact tips but not infer cross-fork ahead/behind from squash history | Independent baseline counts cannot safely be subtracted. | none |
| Do not update `CHANGELOG.md` | Active PR #37 owns it; this task changes no runtime behavior. | none |
| Do not auto-implement candidates | Monitoring and implementation remain separate authorization boundaries. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `docs/agents/programs/OTCLIENT_UPSTREAM_INTELLIGENCE.md` | human programme and candidate summary | planned |
| `artifacts/upstream/otclient/candidates.json` | deterministic candidate registry v1 | planned |
| `docs/agents/README.md` | discovery route | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | JSON parse | not-run | |
| pending | Markdown/path/full-diff review | not-run | |
| pending | applicable GitHub checks | not-run | |

# Risks and compatibility

- Runtime: none; documentation/data only.
- Data/migration: schema version 1 is additive and contains no runtime input.
- Security: no secrets, binaries, assets or external writes.
- Backward compatibility: no client behavior changes.
- Cross-repo rollout: none.
- Rollback: normal squash revert.

# Remaining work

1. Create the three durable files, validate, open the PR and complete the merge gate.

# Handoff

## Start here

Open this task, the programme document and the JSON registry together.

## Do not repeat

Do not reconstruct the baseline from chat after this task merges; update the durable files.

## Required reads

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/MODULE_CATALOG.md`
- open target PRs and active tasks

## Open questions

None.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable; no reusable runtime module
- Changelog updated: not applicable; active PR ownership and no runtime behavior
- Archived at: pending
