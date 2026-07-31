---
task_id: OTC2-20260731-w7-canary-entry
project_lane: otclient-v2
status: in_progress
agent: "W7-CANARY-ENTRY worker"
track: greenfield-rust
workstream: transport-protocol-canary
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-CANARY-ENTRY
parallel_lane_state: active
phase: implement
session_id: chat-github-20260731-w7-canary-entry-1
execution_mode: chat-github
execution_reason: GitHub DNS and Cargo are unavailable in the sandbox; repository reads/writes use the connected GitHub API and exact validation will use repository CI
lease_expires_at: 2026-07-31T10:35:00+02:00
branch: feat/OTC2-20260731-w7-canary-entry
base_branch: main
created: 2026-07-31T09:12:00+02:00
updated: 2026-07-31T09:50:00+02:00
last_verified_commit: "2e6730b5ea9357e1aba9f3e25bce5391f8c5dc70"
required_base_commit: "9ecc43a4465f6565bc1c12ea61f170a96edcbe35"
risk: high
related_pr: "#113"
depends_on:
  - W7 plan PR #101 merged as f7ddc2849838df05a95e4d7260bfe7c3359b4c8d
  - W7 plan archive PR #102 merged as 11a14721e1f3ef81e6bbab54cdfbb631d7ec81e0
  - W7 entry producer PR #104 merged as 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - W7 entry lifecycle archive PR #105 merged as 8dcd353d5a9f19fabccf49508c27074f7749e3cf
  - current main 3c33f97fe2dca533d14a4284c3b13a7b6220a85d
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
  - GameEntryRequest and AdmissionCredential from producer merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - EntryLifecycle, EntryFailure and SessionEntered from producer merge 9ecc43a4465f6565bc1c12ea61f170a96edcbe35
  - Canary Current source at 95b276db311cf6e9acd58b847f1fb0ca6697b137, protocol paths unchanged since planning cut 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
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

Implement the smallest bounded Rust TCP transport and Canary Current-profile admission boundary that consumes one moved W7 credential and can return only shared entry lifecycle outcomes. No gameplay is implemented.

# Preflight

- Current OTClient base is `3c33f97fe2dca533d14a4284c3b13a7b6220a85d`.
- W7-ENTRY-CONTRACT is merged and archived; exact producer merge is `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`.
- Open PRs #23, #48 and #97 do not own Rust transport, protocol or W7 shared integration paths.
- W7-IDENTITY is merged and archived; its shared Cargo/document lease is released.
- Canary selected main is `95b276db311cf6e9acd58b847f1fb0ca6697b137`.
- Comparing Canary cut `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f` to selected main shows no network/protocol/login-session source change.
- Canary and Platform remain read-only.

# Implemented checkpoint

## Exclusive implementation

- `oteryn-protocol-core`:
  - bounded reader/writer;
  - checked little-endian integers and `u16` UTF-8 strings;
  - malformed, truncated, oversized, invalid UTF-8 and trailing-data rejection;
  - stable closed errors;
  - deterministic arbitrary bounded malformed-input test.
- `oteryn-transport`:
  - explicit connect/read/write timeouts;
  - caller-owned cancellation;
  - checked frame bounds before allocation/I/O;
  - partial read/write loops;
  - deterministic terminal state;
  - no DNS resolver, background task, reconnect or socket escape;
  - timeout, cancellation, abrupt close and error-redaction tests.
- `oteryn-protocol-canary`:
  - exact Current profile metadata for Canary `95b276db...`;
  - shared lifecycle/credential/result consumption only;
  - public `connect`, `enter_session`, `cancel`, `close` responsibilities;
  - real mode blocked before network and credential handoff;
  - original synthetic test-only exchange and transcript parser;
  - success creates `SessionEntered` only through `EntryLifecycle`;
  - server denial, credential, character, mismatch, cancellation and connection-loss classifications;
  - duplicate/expired rejection before the synthetic network-attempt counter.

## Evidence

- `oteryn-client/contracts/canary/current-entry/README.md` records exact profile, transport, request, one-shot token, success and denial source facts.
- `oteryn-client/docs/research/technical-login/W7_CANARY_ENTRY_EVIDENCE.md` separates PASS, OBSERVED, UNKNOWN and BLOCKED.
- Synthetic fixture tags and framing are explicitly original and unrelated to Canary bytes.

# Current evidence state

## PASS

- Producer contract and ownership are exact and merged.
- Current Canary protocol source is unchanged from the accepted planning cut.
- Exclusive paths and serialized shared-path lease were free at claim.
- No substitute shared identifier, credential, lifecycle or result type exists in the diff.
- No Canary or Platform write occurred.

## OBSERVED

- Current is release `3.6.1`, protocol `1525`, profile `current`.
- Current uses server-first challenge, OpenTibia RSA bootstrap, XTEA, sequence checksum, modern padding byte and official compression signaling.
- Source bounds are 65,500 network-message bytes, 4,096 input bytes and 30 character-name bytes.
- One-shot token is hash-stored, 60-second default TTL, bound to account/character set/profile and burned before field validation.
- Ordered success prefix is `0x17 -> 0x1A -> 0xEF -> 0x0A -> 0x0F`; map follows and remains out of scope.
- Denial packet `0x14` is followed by connection close; some malformed paths close without payload.

## UNKNOWN

- Exact production client-version string and asset hash.
- Approved exact RSA public-key material/encoding provenance for the Rust client.
- Provenance-safe complete Current transcript bytes.
- Named deployed Platform/Canary/endpoint/TLS/DNS/firewall/secret-manager revisions.
- One controlled real Rust admission through `0x0F`.

## BLOCKED

- `W7-BLOCK-REAL-RUST-E2E` until one exact configured Rust admission through `0x0F` is observed.
- `W7-BLOCK-DEPLOYMENT-EVIDENCE` for TLS, DNS, firewall, secret manager and deployed revision claims.

# Validation state

Not yet run on current head:

- workspace integration and generated lockfile;
- `cargo metadata --locked`;
- `cargo fmt --all --check`;
- full workspace Clippy with warnings denied;
- all workspace tests;
- architecture checks;
- `cargo deny check`;
- required GitHub CI;
- complete final diff/review-thread inspection.

The sandbox has neither Cargo nor GitHub DNS. This is an environment limitation, not a success claim. Exact validation will use repository CI after the minimal serialized workspace integration commit.

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-31T09:50:00+02:00
head: 2e6730b5ea9357e1aba9f3e25bce5391f8c5dc70
branch: feat/OTC2-20260731-w7-canary-entry
pr: 113
status: in_progress
phase: implement
execution_mode: chat-github
last_completed_step: implemented isolated transport, protocol-core, evidence-gated Canary adapter, synthetic tests, contract and evidence matrix
proven:
  - W7-CANARY-ENTRY consumes the exact merged producer API without substitutes.
  - Real admission fails closed before network and credential handoff.
  - Exact Canary source facts and missing evidence are separated.
unknown:
  - compilation, formatting, Clippy, tests, architecture and supply-chain results before workspace integration
blockers:
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
next_action: Integrate the three local crates into the serialized Cargo workspace, generate/reconcile Cargo.lock through an authorized executable environment, then inspect and repair exact CI failures.
```
