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
parallel_lane_state: active
phase: implement
session_id: chat-github-20260731-w7-canary-entry-1
session_role: implementer
session_rotation_count: 0
execution_mode: chat-github
execution_reason: GitHub DNS and Cargo are unavailable in the sandbox; bounded repository changes use the GitHub connector and exact compilation uses repository CI
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one cohesive producer/consumer task with isolated implementation, workspace integration, exact-head validation and separate closure phases
validation_level: component
heavy_validation_runs: 1
heavy_validation_result: failed
first_relevant_error: cargo fmt --all --check reported formatting-only diffs in the three owned Rust crates
stale_takeover_count: 0
human_interruptions: 0
lease_expires_at: 2026-07-31T10:50:00+02:00
branch: feat/OTC2-20260731-w7-canary-entry
base_branch: main
created: 2026-07-31T09:12:00+02:00
updated: 2026-07-31T10:05:00+02:00
last_verified_commit: "a8e05a638a5b7730874e6c0c6e811255d50cbc9f"
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

# Durable implementation

- `oteryn-protocol-core`: bounded checked integer/string reader and writer; malformed, truncated, oversized, invalid UTF-8 and trailing-data rejection; closed stable errors; deterministic malformed-input tests.
- `oteryn-transport`: one already-resolved TCP endpoint; explicit connect/read/write timeouts; cancellation; checked directional frame limits; partial I/O; deterministic terminal state; no resolver, daemon, reconnect or socket exposure; timeout/close/redaction tests.
- `oteryn-protocol-canary`: exact Current metadata; shared W7 lifecycle/credential/result consumption; `connect`, `enter_session`, `cancel`, `close`; test-only original synthetic exchange; production mode blocked before network and credential handoff until exact fixture/E2E evidence exists.
- Exact contract: `oteryn-client/contracts/canary/current-entry/README.md`.
- PASS/OBSERVED/UNKNOWN/BLOCKED evidence: `oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md`.

# Evidence checkpoint

## PASS

- Producer merge and ownership are exact; no substitute identifiers, credential, lifecycle, failure or result type exists.
- Canary/Platform remained read-only.
- Workspace members and generated lockfile contain exactly the three new local packages; a guarded CI bootstrap verified no external package version/checksum change and was removed from the branch.
- `cargo metadata --locked` passed on Windows merge-head CI.
- `cargo deny check` passed.
- Exact `rustfmt` output was applied only to owned Rust sources; its temporary guarded workflow was removed.

## OBSERVED

- Selected Canary revision `95b276db311cf6e9acd58b847f1fb0ca6697b137`: release `3.6.1`, profile `current`, client/protocol `1525`.
- Current uses server-first challenge, OpenTibia RSA bootstrap, XTEA, sequence checksum, modern padding and official compression signaling.
- Source bounds: 65,500 network-message bytes, 4,096 input bytes, 30 character-name bytes.
- One-shot token is hash-stored, default 60-second TTL, account/character/profile bound and burned before field validation.
- Ordered technical success prefix is `0x17 -> 0x1A -> 0xEF -> 0x0A -> 0x0F`; map follows and is excluded.

## UNKNOWN

- Exact production client-version string, asset hash and approved RSA material/encoding provenance.
- Provenance-safe complete Current transcript bytes.
- Named deployment revisions/configuration and one controlled real Rust admission through `0x0F`.

## BLOCKED

- `W7-BLOCK-REAL-RUST-E2E`: production adapter remains fail-closed until exact configured Rust admission evidence exists.
- `W7-BLOCK-DEPLOYMENT-EVIDENCE`: no DNS/TLS/firewall/secret-manager/deployment claim.

# Validation checkpoint

```yaml
policy_version: 2
updated_at: 2026-07-31T10:05:00+02:00
head: a8e05a638a5b7730874e6c0c6e811255d50cbc9f
current_main: e891baac5f56d3706ade502645320bc33db5642f
branch: feat/OTC2-20260731-w7-canary-entry
pr: 113
status: in_progress
phase: implement
session_role: implementer
execution_mode: chat-github
context_pressure: high
context_growth: stable
context_score: 10
decomposition_decision: phased
validation_level: component
heavy_validation_runs: 1
heavy_validation_result: failed
first_relevant_error: formatting-only diff; exact rustfmt output now committed
last_completed_step: generated guarded Cargo.lock, passed locked metadata and cargo-deny, applied rustfmt, removed both temporary workflows, and adopted execution policy v2
proven:
  - exact merged W7 entry contracts are reused without substitutes
  - real admission fails closed before network and credential handoff
  - external dependency resolution did not change
unknown:
  - first Clippy/compiler/test result after formatting
blockers:
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
next_action: Observe the new merge-head CI against main e891baac, repair the first Clippy/compiler/test failure with focused changes, then restack the final branch on exact current main.
```
