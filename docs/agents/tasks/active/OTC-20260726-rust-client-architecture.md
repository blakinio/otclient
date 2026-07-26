---
task_id: OTC-20260726-rust-client-architecture
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-rust-client-architecture
base_branch: main
created: 2026-07-26T23:30:22+02:00
updated: 2026-07-26T23:52:03+02:00
last_verified_commit: "637a364ac3f0ab804bfdb71bfae4018c04fb866c"
risk: high
related_issue: ""
related_pr: "#45"
depends_on: []
blocks:
  - greenfield Rust client foundation audit
  - Rust workspace bootstrap
  - renderer, protocol, UI and asset workstreams
owned_paths:
  - oteryn-client/README.md
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/**
  - oteryn-client/docs/agents/**
  - docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md
  - docs/agents/README.md
  - docs/agents/OTERYN_WORKSTREAM_MAP.md
  - docs/agents/REPOSITORY_MAP.md
  - docs/agents/KNOWN_RISKS.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-rust-client-architecture.md
modules_touched: []
reuses:
  - existing repository governance and task/PR workflow
  - current C++ client only as behavior/protocol/asset evidence during audit
  - existing Canary and Oteryn Identity contracts where independently verified
public_interfaces:
  - target Rust workspace boundaries
  - client state machine and gameplay-channel login/relog contract
  - protocol adapter boundary
  - agent workstream ownership model
cross_repo_tasks: []
---

# Goal

Define one complete, agent-ready greenfield Rust client architecture in an isolated `oteryn-client/` directory. Canary is the first compatibility adapter and Oteryn is the target ecosystem. Include repository layout, module and protocol boundaries, security, performance, assets, gameplay-channel login/relog behavior and an audit-first implementation program.

# Acceptance criteria

- [x] Normative architecture defines a new Rust client rather than a line-by-line OTClient rewrite.
- [x] Current C++/Lua/OTUI code is classified as legacy/reference evidence and is not a target runtime dependency.
- [x] All new-client architecture and agent documents are isolated under `oteryn-client/`.
- [x] Repository layout and crate dependency direction are complete enough for non-overlapping workstreams.
- [x] Canary and future Oteryn protocols are isolated behind one domain adapter boundary.
- [x] Account session, character/world/gameplay-channel selection, game session and relog lifecycles are explicit.
- [x] Gameplay channels are parallel world instances selected at login/relog, not network streams.
- [x] Renderer, world storage, UI, assets, audio, input, launcher/updater, diagnostics and extension boundaries are defined.
- [x] Security model covers Identity, one-shot tickets, untrusted input, updater/assets and WASM extensions.
- [x] Performance budgets are documented as targets requiring reproducible measurement.
- [x] A standalone foundation-audit plan and copy-ready first-agent prompt are present.
- [x] Five durable ADRs record the core product decisions.
- [x] Root discovery/routing documents point to the new architecture without editing active legacy PR paths.
- [ ] Complete changed-file/full-diff consistency review is recorded on the final head.
- [ ] Required documentation/fast CI passes on the final head.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- The previous architecture on `main` required evolving the C++/Lua client and conflicted with the newly confirmed greenfield direction.
- The new product must select architecture for performance, safety and maintainability rather than compatibility with OTClient internals.
- Canary is the initial server compatibility target; Oteryn is the long-term target.
- Gameplay-channel changes happen through relog. Seamless live channel transfer is not required.
- Open PRs inspected before claiming paths: #37 assets, #36 options Phase 0 and #23 legacy login-shell prototype.
- None owns the architecture/program paths in this task.
- Draft PR #45 was opened from `main` at `24452895ca44c4e9a98853d69fcc863b62bc089f`.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Repository governance | branch/task/PR lifecycle and safety | root `AGENTS.md`, `docs/agents/**` | one coordination system for both tracks |
| Existing client | audit evidence only | `src/**`, `modules/**`, `data/**`, tests | behavior/protocol/assets must be inventoried, not structurally ported |
| Oteryn Identity contracts | security and session requirements | shared contracts and verified implementation evidence | preserves PKCE and no-password game handoff |
| Existing test foundation | legacy behavior evidence | legacy `tests/**` | Rust gets native Cargo tests after audit |

# Ownership and overlap check

- Open PRs inspected: #37, #36, #23.
- Their task records and paths were inspected.
- No legacy runtime/module/asset implementation path was edited.
- `ACTIVE_WORK.md` remains unchanged under current coordination policy.

# Architecture package

## Entry and nested governance

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`

## Normative architecture

- `docs/architecture/ARCHITECTURE.md`
- `REPOSITORY_LAYOUT.md`
- `CLIENT_LIFECYCLE.md`
- `MODULE_MODEL.md`
- `PROTOCOL_BOUNDARY.md`
- `SECURITY_MODEL.md`
- `PERFORMANCE_AND_TESTING.md`
- `ASSET_PIPELINE.md`

## ADRs

- `0001-greenfield-rust-client.md`
- `0002-data-oriented-wgpu-renderer.md`
- `0003-protocol-adapter-boundary.md`
- `0004-static-modules-wasm-extensions.md`
- `0005-gameplay-channel-relog.md`

## Agent program

- `docs/agents/PROGRAM.md`
- `docs/agents/WORKSTREAMS.md`
- `docs/agents/AUDIT_PLAN.md`
- `docs/agents/prompts/FIRST_AUDIT_AGENT.md`
- `docs/agents/templates/TASK.md`

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Isolate new product under `oteryn-client/` | avoids dependency/CI/path conflicts while legacy stays buildable | 0001 |
| Require a foundation audit before Cargo bootstrap | exact Canary/assets/hardware/dependency facts remain incomplete | 0001 / audit gate |
| Use data-oriented runtime and `wgpu` | frame-time/locality/control goals without OpenGL/legacy coupling | 0002 |
| Keep protocol adapters outside domain | Canary now and Oteryn later without another client rewrite | 0003 |
| Compile first-party modules; sandbox optional extensions in WASM | performance, reviewability and containment | 0004 |
| Change gameplay channels through relog | confirmed product behavior and simpler session ownership | 0005 |

# Work log

## 2026-07-26T23:30:22+02:00

- Created the task branch and draft PR.
- Confirmed the old normative documents conflicted with the requested product direction.

## 2026-07-26T23:52:03+02:00

- Added the isolated `oteryn-client/` architecture, nested instructions, detailed workspace plan and five ADRs.
- Defined explicit account/game lifecycle and Channel 1 -> Channel 2 relog behavior.
- Defined domain/protocol isolation, static first-party modules, WASM extension boundary, signed asset pipeline and measurable performance/test gates.
- Added a mandatory ten-document foundation audit and standalone prompt for the first audit agent.
- Replaced root architecture/workstream routing and updated discovery, risk, validation, catalogue and changelog documents.
- No production crates, legacy runtime code, external repository changes, assets or secrets were added.

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `637a364ac3f0ab804bfdb71bfae4018c04fb866c` | architecture package creation | complete | documentation-only; no build claim |
| pending final head | changed-file and full patch review | not-run | inspect PR #45 after this checkpoint |
| pending final head | documentation/fast CI | not-run | inspect emitted checks |

# Failed approaches and dead ends

- Keeping the greenfield design as an optional section inside the old C++ architecture was rejected because agents need one normative target.
- Moving the legacy client into `legacy/` now was rejected because it would create a huge unrelated diff and conflict with active PRs.
- Treating gameplay channels as QUIC/network streams was rejected; they are world instances.
- Creating empty Cargo crates before the audit was rejected because placeholders would freeze unsupported assumptions.

# Risks and compatibility

- Runtime: documentation only; no runtime behavior changed.
- Data/migration: legacy paths remain in place until a separate retirement task.
- Security: existing Identity/asset guarantees are preserved or strengthened in the target model.
- Backward compatibility: current client remains buildable and existing PR ownership is unchanged.
- Cross-repository rollout: exact Canary and Oteryn implementation work requires separate coordinated tasks.
- Rollback: normal documentation PR revert.

# Remaining work

1. Review the complete PR #45 changed-file list and full patch for consistency, broken paths and unintended legacy claims.
2. Update PR body/task with final validation and inspect required CI.
3. Mark ready and squash-merge only when the autonomous merge gate passes.
4. After merge, start the foundation audit using the copy-ready prompt; do not bootstrap Cargo first.

# Handoff

## Start here

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`
- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/agents/AUDIT_PLAN.md`

## Do not repeat

Do not create another Rust architecture, move legacy source, or create production crates before the audit gate.

## Open questions reserved for audit/cross-repo work

- exact initial Canary revision and fixture set;
- exact legally usable asset sources;
- concrete Windows hardware tiers;
- final Rust dependency choices;
- native Oteryn transport/schema/session-resume design.

# Completion

- Final status: in progress
- PR: #45
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
