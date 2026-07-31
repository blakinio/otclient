---
task_id: OTC2-20260731-w7-canary-entry
project_lane: otclient-v2
policy_version: 2
task_kind: implementation
implementation_authorized: true
status: completed
agent: "W7-CANARY-ENTRY worker"
track: greenfield-rust
workstream: transport-protocol-canary
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-CANARY-ENTRY
parallel_lane_state: archived
phase: close
session_id: chat-github-20260731-w7-canary-entry-2
session_role: closer
session_rotation_count: 1
execution_mode: chat-github
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: phased
validation_level: full
heavy_validation_runs: 4
heavy_validation_result: passed
stale_takeover_count: 0
human_interruptions: 1
branch: feat/OTC2-20260731-w7-canary-entry
base_branch: main
created: 2026-07-31T09:12:00+02:00
updated: 2026-07-31T13:20:00+02:00
validated_feature_head: "7ce27154411f21571e96d74745d26ec73522d5e5"
merge_commit: "4a193bdf10ac32a8a2d8dc12f31706c7d668c8f9"
required_base_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
validated_main_commit: "e891baac5f56d3706ade502645320bc33db5642f"
canary_revision: "95b276db311cf6e9acd58b847f1fb0ca6697b137"
risk: high
related_pr: "#113"
owned_paths:
  - oteryn-client/crates/transport/**
  - oteryn-client/crates/protocol-core/**
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/contracts/canary/current-entry/**
  - oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md
  - docs/agents/tasks/archive/OTC2-20260731-w7-canary-entry.md
shared_path_lease: []
contract_role: consumer-and-sole-w7-transport-admission-producer
contracts_consumed:
  - merged W7 ENTRY contracts at 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - Canary Current source at 95b276db311cf6e9acd58b847f1fb0ca6697b137
contracts_produced:
  - bounded non-reconnecting W7 TCP transport interface
  - bounded protocol-core reader/writer and closed error categories
  - exact-evidence-gated Canary Current admission adapter
blockers:
  - exact production client-version string and asset hash remain external
  - approved exact RSA public-key material and encoding provenance remain unavailable
  - provenance-safe complete Current transcript bytes remain unavailable
  - one named configured Rust admission through ordered 0x0F remains unproven
  - deployment DNS, TLS, firewall and secret-manager state remain external
---

# Result

W7-CANARY-ENTRY implemented, validated and merged the bounded Rust transport and Canary Current admission foundation without claiming real Current wire compatibility.

Delivered:

- `oteryn-transport`: one already-resolved non-reconnecting TCP connection with explicit connect/read/write timeouts, directional frame bounds, caller-owned cancellation, partial-I/O handling and terminal closure after every started-I/O failure;
- `oteryn-protocol-core`: checked bounded little-endian integer, exact-byte and `u16` UTF-8 string helpers with closed malformed/truncated/oversized/invalid-text/trailing-data errors;
- `oteryn-protocol-canary`: exact Current metadata and typed shared ENTRY lifecycle outcomes consuming one moved credential without exposing raw sockets or credentials;
- original synthetic tests for success, denial mapping, wrong/expired/consumed/duplicate credential use, timeout, cancellation, abrupt close, malformed input, redaction and deterministic no-panic parsing;
- exact source contract and PASS / OBSERVED / UNKNOWN / BLOCKED evidence;
- workspace, lockfile, module catalogue, validation matrix, changelog, repository-layout and workspace-operation integration.

Production Current admission remains deliberately fail-closed before network I/O and before credential handoff. Gameplay, map, creature, item, chat, combat, reconnect and credential replay remain absent.

# Validation evidence

Exact feature head `7ce27154411f21571e96d74745d26ec73522d5e5` passed:

- Rust Client run `30626519026`;
- Windows job `91142950239`: locked metadata, formatting, strict Clippy, all workspace tests and architecture policy;
- supply-chain job `91142950178`: advisories, licenses, bans and sources;
- ready-state repository CI run `30626552977` with successful `CI / Required` job `91143333890`;
- complete 18-path diff review;
- zero commits behind validated `main` `e891baac5f56d3706ade502645320bc33db5642f`;
- no comments, submitted reviews or unresolved review threads;
- no temporary workflow/script, secret, private capture, proprietary fixture or external dependency version/checksum change in the merged diff.

PR #113 squash-merged as `4a193bdf10ac32a8a2d8dc12f31706c7d668c8f9`.

# Closure

The complete Cargo, lockfile and shared-document lease is released. Downstream W7-LOGIN-E2E may restack on exact merge `4a193bdf10ac32a8a2d8dc12f31706c7d668c8f9` after this archive PR merges.

The compatibility gates listed in frontmatter remain future work and do not invalidate the bounded fail-closed foundation delivered here.
