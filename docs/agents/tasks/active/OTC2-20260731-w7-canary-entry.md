---
task_id: OTC2-20260731-w7-canary-entry
project_lane: otclient-v2
policy_version: 2
task_kind: implementation
implementation_authorized: true
status: in_progress
agent: "W7-CANARY-ENTRY worker"
track: greenfield-rust
workstream: transport-protocol-canary
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-CANARY-ENTRY
parallel_lane_state: validating
phase: validate
session_id: chat-github-20260731-w7-canary-entry-1
session_role: implementer
session_rotation_count: 0
execution_mode: chat-github
execution_reason: GitHub DNS and Cargo are unavailable in the sandbox; bounded repository changes use the GitHub connector and exact compilation uses repository CI
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive producer/consumer task with isolated implementation, workspace integration, exact-head validation and separate closure phases
validation_level: full
heavy_validation_runs: 3
heavy_validation_result: passed
first_relevant_error: none on code checkpoint 39bdf7c32cfb1a3e6a5986bedf40012f7e04f1e5; later generic failures were limited to temporary documentation workflow syntax and all temporary files are absent from the final diff
stale_takeover_count: 0
human_interruptions: 0
lease_expires_at: 2026-07-31T11:30:00+02:00
branch: feat/OTC2-20260731-w7-canary-entry
base_branch: main
created: 2026-07-31T09:12:00+02:00
updated: 2026-07-31T10:45:00+02:00
last_verified_commit: "7526e6ce295812ab6ac6cbb66a2da2aca4455fb1"
required_base_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
current_main_commit: "e891baac5f56d3706ade502645320bc33db5642f"
risk: high
related_pr: "#113"
depends_on:
  - W7 plan PR #101 merged as f7ddc2849838df05a95e4d7260bfe7c3359b4c8d
  - W7 plan archive PR #102 merged as 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
  - W7 entry producer PR #104 merged as 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - W7 entry archive PR #105 merged as 8dcd353d5a9f19fabccf49508c27074f7749e3cf
integration_after:
  - W7-ENTRY-CONTRACT
owned_paths:
  - oteryn-client/crates/transport/**
  - oteryn-client/crates/protocol-core/**
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/contracts/canary/current-entry/**
  - oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md
  - docs/agents/tasks/active/OTC2-20260731-w7-canary-entry.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/deny.toml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
contract_role: consumer-and-sole-w7-transport-admission-producer
contracts_consumed:
  - shared W7 entry types from merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - Canary Current source at 95b276db311cf6e9acd58b847f1fb0ca6697b137
contracts_produced:
  - bounded W7 transport interface
  - bounded protocol-core reader/writer and error categories
  - exact-evidence-gated Canary Current admission adapter
crates_touched:
  - transport
  - protocol-core
  - protocol-canary
cross_repo_tasks: []
---

# Goal

Implement the smallest bounded Rust TCP transport and Canary Current-profile admission boundary that consumes one moved shared W7 credential and returns only shared entry lifecycle outcomes. Gameplay is excluded.

# Delivered

- `oteryn-protocol-core`: bounded checked integer/string reader and writer; malformed, truncated, oversized, invalid UTF-8 and trailing-data rejection; closed stable errors; deterministic arbitrary bounded malformed-input tests.
- `oteryn-transport`: one already-resolved TCP endpoint; explicit connect/read/write timeouts; caller-owned cancellation; checked directional frame limits; partial I/O; deterministic terminal state; no resolver, daemon, reconnect or socket exposure; timeout, abrupt-close and redaction tests.
- `oteryn-protocol-canary`: exact Current metadata; shared W7 lifecycle/credential/result consumption; application-facing `connect`, `enter_session`, `cancel`, `close`; original test-only synthetic exchange; production mode blocked before network and credential handoff until exact fixture/E2E evidence exists.
- Exact contract: `oteryn-client/contracts/canary/current-entry/README.md`.
- PASS/OBSERVED/UNKNOWN/BLOCKED evidence: `oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md`.
- Workspace, lockfile, module catalogue, validation matrix, changelog, repository layout and workspace operations documentation are integrated.

# PASS

- Exact producer contracts are reused; no substitute identifier, credential, lifecycle, failure or result type exists.
- Canary and Platform remained read-only.
- Final PR diff contains exactly 18 intended code/test/task/contract/evidence/shared-integration paths and no temporary workflow or script.
- Guarded lock generation added only the three local packages and preserved every external package version and checksum.
- Windows merge-head Rust CI passed `cargo metadata --locked`, `cargo fmt --all --check`, full workspace Clippy with warnings denied, all workspace tests, architecture policy and cargo-deny on code checkpoint `39bdf7c32cfb1a3e6a5986bedf40012f7e04f1e5` against current `main` `e891baac5f56d3706ade502645320bc33db5642f`.
- Duplicate second use is rejected before a second synthetic network attempt.
- Production admission fails closed before network I/O and before credential handoff.

# OBSERVED

- Selected Canary revision `95b276db311cf6e9acd58b847f1fb0ca6697b137`: release `3.6.1`, profile `current`, client/protocol `1525`.
- Current uses server-first challenge, OpenTibia RSA bootstrap, XTEA, sequence checksum, modern padding and official compression signaling.
- Source bounds are 65,500 network-message bytes, 4,096 input bytes and 30 character-name bytes.
- One-shot token is hash-stored, default 60-second TTL, account/character/profile bound and burned before field validation.
- Ordered technical success prefix is `0x17 -> 0x1A -> 0xEF -> 0x0A -> 0x0F`; map follows and is excluded.

# UNKNOWN

- Exact production client-version string and asset hash.
- Approved exact RSA public-key material and encoding provenance for the Rust client.
- Provenance-safe complete Current transcript bytes.
- Named deployment revisions/configuration and one controlled real Rust admission through `0x0F`.

# BLOCKED

- `W7-BLOCK-REAL-RUST-E2E`: production adapter remains fail-closed until exact configured Rust admission evidence exists.
- `W7-BLOCK-DEPLOYMENT-EVIDENCE`: no DNS, TLS, firewall, secret-manager or deployment claim.

# Validation checkpoint

```yaml
policy_version: 2
updated_at: 2026-07-31T10:45:00+02:00
head: 7526e6ce295812ab6ac6cbb66a2da2aca4455fb1
current_main: e891baac5f56d3706ade502645320bc33db5642f
branch: feat/OTC2-20260731-w7-canary-entry
pr: 113
status: in_progress
phase: validate
session_role: implementer
execution_mode: chat-github
context_pressure: high
context_growth: stable
context_score: 10
decomposition_decision: phased
validation_level: full
heavy_validation_runs: 3
heavy_validation_result: passed
first_relevant_error: none in the intended code or final diff
last_completed_step: integrated all required shared documentation, removed every temporary helper and confirmed the exact 18-path final diff
proven:
  - exact merged W7 entry contracts are reused without substitutes
  - production admission fails closed before network and credential handoff
  - external dependency resolution did not change
  - full Windows workspace Rust validation passed on the current merge-head
unknown:
  - exact-head result after final restack commit
blockers:
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
next_action: Create a backup ref, restack the task branch on exact current main e891baac5f56d3706ade502645320bc33db5642f, then run final exact-head CI and complete diff/review inspection.
```
