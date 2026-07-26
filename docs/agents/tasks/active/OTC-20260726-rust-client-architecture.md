---
task_id: OTC-20260726-rust-client-architecture
coordination_id: ""
status: awaiting_ci
agent: "GPT-5.6 Thinking"
branch: docs/OTC-20260726-rust-client-architecture
base_branch: main
created: 2026-07-26T23:30:22+02:00
updated: 2026-07-27T00:06:00+02:00
last_verified_commit: "d38cea5246a6c024948d9de8940129bcf4b82c68"
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
  - docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md
  - docs/agents/README.md
  - docs/agents/OTERYN_WORKSTREAM_MAP.md
  - docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md
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
- [x] Repository layout and crate dependency direction support non-overlapping workstreams.
- [x] Canary and future Oteryn protocols are isolated behind one domain adapter boundary.
- [x] Account session, character/world/gameplay-channel selection, game session and relog lifecycles are explicit.
- [x] Gameplay channels are parallel world instances selected at login/relog, not network streams.
- [x] Renderer, world storage, UI, assets, audio, input, launcher/updater, diagnostics and extension boundaries are defined.
- [x] Security model covers Identity, one-shot tickets, untrusted input, updater/assets and WASM extensions.
- [x] Performance budgets are documented as targets requiring reproducible measurement.
- [x] A standalone foundation-audit plan and copy-ready first-agent prompt are present.
- [x] Five durable ADRs record core product decisions.
- [x] Root routing points to the new architecture without editing active legacy implementation paths.
- [x] Detailed legacy architecture/workstream knowledge remains available for active C++/Lua work.
- [x] Complete changed-file/full-patch consistency review was performed and resulting issues were repaired.
- [ ] Required documentation/fast CI passes on the final head.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- The previous target architecture required evolving the C++/Lua client and conflicted with the confirmed greenfield direction.
- The new product selects architecture for performance, safety and maintainability rather than OTClient-internal compatibility.
- Canary is the initial server compatibility target; Oteryn is the long-term target.
- Gameplay-channel changes happen through relog. Seamless live channel transfer is not required.
- Open PRs inspected before ownership: #37 assets, #36 options Phase 0 and #23 legacy login-shell prototype.
- None owns the architecture/program paths changed here.
- Draft PR #45 was opened from `main` at `24452895ca44c4e9a98853d69fcc863b62bc089f`.

# Architecture package

## Entry and nested governance

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`

## Normative architecture

- `ARCHITECTURE.md`
- `REPOSITORY_LAYOUT.md`
- `CLIENT_LIFECYCLE.md`
- `MODULE_MODEL.md`
- `PROTOCOL_BOUNDARY.md`
- `SECURITY_MODEL.md`
- `PERFORMANCE_AND_TESTING.md`
- `ASSET_PIPELINE.md`

## Durable decisions

- ADR-0001 greenfield Rust client and isolated directory;
- ADR-0002 data-oriented runtime and `wgpu` renderer;
- ADR-0003 protocol adapter boundary;
- ADR-0004 static first-party modules and WASM extensions;
- ADR-0005 gameplay-channel login/relog semantics.

## Agent program

- `oteryn-client/docs/agents/PROGRAM.md`
- `WORKSTREAMS.md`
- `AUDIT_PLAN.md`
- `prompts/FIRST_AUDIT_AGENT.md`
- `templates/TASK.md`

## Legacy preservation

- `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md`
- `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md`

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Isolate new product under `oteryn-client/` | avoids dependency/CI/path conflicts while legacy stays buildable | 0001 |
| Require foundation audit before Cargo bootstrap | Canary/assets/hardware/dependency facts remain incomplete | 0001 / audit gate |
| Use data-oriented runtime and `wgpu` | frame-time/locality/control goals without OpenGL/legacy coupling | 0002 |
| Keep protocol adapters outside domain | Canary now and Oteryn later without another client rewrite | 0003 |
| Compile first-party modules; sandbox optional extensions in WASM | performance, reviewability and containment | 0004 |
| Change gameplay channels through relog | confirmed product behavior and simpler session ownership | 0005 |
| Preserve legacy maintenance knowledge separately | active legacy PRs still require exact owner/test/contract routing | legacy reference docs |

# Work log

## 2026-07-26T23:30:22+02:00

- Created the task branch and draft PR.
- Confirmed the old normative target conflicted with the requested product direction.

## 2026-07-26T23:52:03+02:00

- Added isolated architecture, nested instructions, workspace plan and five ADRs.
- Defined account/game lifecycle and Channel 1 -> Channel 2 relog behavior.
- Defined domain/protocol isolation, static modules, WASM boundary, signed asset pipeline and performance/test gates.
- Added mandatory ten-document foundation audit and standalone first-agent prompt.
- Updated root routing, discovery, risk, validation, catalogue and changelog documents.
- Added no production crates, legacy runtime code, external writes, assets or secrets.

## 2026-07-27T00:02:00+02:00

- Reviewed all changed filenames and the complete PR patch.
- Found that the first routing rewrite removed too much durable legacy maintenance knowledge.
- Restored that knowledge as explicit legacy architecture/workstream documents while retaining Rust as the only target architecture.
- Restored detailed legacy catalogue rows and preserved historical changelog wording.
- Restored legacy upstream-intelligence and new-agent discovery routes.
- Aligned the audit dependency section with ADR-0002: `wgpu` is selected at architecture level; exact version/backend details remain audit/bootstrap decisions.

## 2026-07-27T00:06:00+02:00

- Rechecked the final 31-file changed-path set: documentation/governance only, entirely within declared ownership.
- Rechecked architecture routing, relative paths, track separation and gameplay-channel terminology.
- Added the legacy-route pointer to the Rust entry README.
- No runtime, workflow, binary, asset, secret or external-repository file is present.
- Package is ready for exact-head documentation/fast CI.

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `7ee647f79bd2f4a61bf7d04831a3fbcb66ccd0fb` | complete changed-file and PR patch review | PASS | 31 documentation/governance files only; initial legacy-knowledge deletion identified and repaired |
| `d38cea5246a6c024948d9de8940129bcf4b82c68` | final changed-path and architecture consistency review | PASS | owned docs only; routes, terminology and legacy/Rust separation checked |
| final head pending | documentation/fast CI | pending | no C++ or Rust build required for docs-only package |

# Failed approaches and dead ends

- Keeping greenfield design as an optional section inside the old architecture was rejected because agents need one normative target.
- Moving legacy source into `legacy/` now was rejected because it would create a huge unrelated diff and conflict with active PRs.
- Treating gameplay channels as network streams was rejected; they are parallel world instances.
- Creating empty Cargo crates before the audit was rejected because placeholders would freeze unsupported assumptions.
- Deleting detailed legacy governance was rejected during full-diff review; it is preserved in explicitly scoped reference documents.

# Risks and compatibility

- Runtime: documentation only; no runtime behavior changed.
- Data/migration: legacy paths remain until a separate retirement task.
- Security: existing Identity/asset guarantees are preserved or strengthened in the target model.
- Backward compatibility: existing client remains buildable and active PR ownership is unchanged.
- Cross-repository rollout: exact Canary/Oteryn implementation requires separate coordinated tasks.
- Rollback: normal documentation PR revert.

# Remaining work

1. Inspect exact-head documentation/fast CI and fix any issue.
2. Mark ready and squash-merge only when the autonomous merge gate passes.
3. After merge, start the foundation audit from the copy-ready prompt; do not bootstrap Cargo first.

# Handoff

## Start here

- `oteryn-client/README.md`
- `oteryn-client/AGENTS.md`
- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/agents/AUDIT_PLAN.md`

## Do not repeat

Do not create another Rust architecture, move legacy source or create production crates before the audit gate.

## Open questions reserved for audit/cross-repository work

- exact initial Canary revision and fixture set;
- exact legally usable asset sources;
- concrete Windows hardware tiers;
- final Rust dependency package/versions;
- native Oteryn transport/schema/session-resume design.

# Completion

- Final status: awaiting CI
- PR: #45
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
