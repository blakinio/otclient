---
task_id: OTC-20260730-plan-w7-technical-login
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-C
parallel_lane_state: validating
branch: docs/OTC-20260730-plan-w7-technical-login
base_branch: main
created: 2026-07-30T11:49:00+02:00
updated: 2026-07-30T12:12:00+02:00
last_verified_commit: "pending-current-head"
required_base_commit: "1922ef0201cd476cad2fabd42e6f9622e52891f6"
risk: high
related_pr: "#101"
depends_on:
  - W6 closure PR #98 and archive PR #100
owned_paths:
  - docs/agents/tasks/active/OTC-20260730-plan-w7-technical-login.md
  - docs/agents/README.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md
shared_path_lease: []
contract_role: coordination-only
contracts_produced:
  - accepted W7 architecture/lane/ownership/dependency/lease/evidence plan only
contracts_consumed:
  - current Rust architecture and lifecycle
  - Oteryn Platform/Gateway source 8e613c00503c0874e69e2085c740f87f4a87e002
  - Canary source 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
crates_touched: []
features_touched: []
contracts_touched:
  - planning metadata and cross-repository evidence only; no runtime API/protocol implementation
modules_touched: []
reuses:
  - existing Rust Windows shell and renderer
  - existing architecture categories and workspace policy
  - exact current external source evidence
public_interfaces:
  - no runtime interface in this task
cross_repo_tasks: []
performance_evidence:
  - no runtime, latency, throughput or compatibility claim
security_evidence:
  - no credentials, tokens, private captures, proprietary assets or external-repository writes
---

# Goal

Prepare one accepted, bounded multi-agent architecture and execution plan for the first compilable Rust Oteryn technical-login slice. This task implements no worker package and launches no worker.

# Planning acceptance

- [x] Reconciled exact current main `1922ef0201cd476cad2fabd42e6f9622e52891f6`.
- [x] Verified W1-W6 are merged, closed and separately archived through PR #100.
- [x] Verified PR #23 remains legacy UI-only, PR #48 remains operational non-merge work and PR #97 owns only legacy asset rehearsal.
- [x] Verified no active Rust task/open PR owns W7 login contracts, crates or final composition paths.
- [x] Verified every prior Cargo, lockfile, dependency-policy and shared-document lease is released.
- [x] Published a dedicated technical-login architecture document.
- [x] Published one coordinator plus exactly four bounded worker lanes.
- [x] Published exact dependency graph, exclusive paths, sole producers/consumers, shared-path lease protocol and merge/archive order.
- [x] Published automated versus interactive evidence matrix.
- [x] Published exact milestone acceptance criteria, exclusions and internal-only protocol-research boundary.
- [x] Published exact coordinator prompt and four exact worker prompts.
- [x] Recorded current Platform/Gateway/Canary producer cuts and legacy-reference proof boundary.
- [x] Revalidated Platform loopback behavior: no-port registered base plus explicitly tested dynamic loopback port; fixed port 80 remains prohibited.
- [x] Recorded no multi-world/channel, reusable account-session, deployed TLS/secret-manager or production claim.
- [ ] Pass exact-head CI, inspect complete ten-file diff and confirm no unresolved review threads.
- [ ] Merge through repository gates and archive this planning task separately before any worker launch.

# Plan outputs

| Output | Path |
|---|---|
| technical-login architecture | `oteryn-client/docs/architecture/TECHNICAL_LOGIN.md` |
| accepted wave/dependency/ownership/lease/evidence/acceptance plan | `oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md` |
| coordinator prompt | `oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md` |
| ENTRY prompt | `oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md` |
| IDENTITY prompt | `oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md` |
| CANARY prompt | `oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md` |
| LOGIN E2E prompt | `oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md` |
| exact producer evidence and blockers | `docs/agents/CROSS_REPO_CONTRACTS.md` |
| routing/read order | `docs/agents/README.md` |

# Exact contract findings

## Platform and Gateway

- Native public Authorization Code + PKCE `S256` exists.
- Platform registers `http://127.0.0.1/callback`; current tests explicitly prove an otherwise matching dynamic port for authorization and token exchange and reject wrong path/non-loopback redirects.
- Rust must bind `127.0.0.1:0`, use the actual assigned port and never bind fixed port 80.
- Game Login Ticket issuance revokes the associated access/refresh token family, bounding W7 to one bootstrap attempt.
- Gateway v1 accepts only `{protocol_version:1, game_login_ticket}` and returns one opaque session credential plus authoritative worlds/characters.
- `World.id` and `Character.id/world_id` are signed 64-bit JSON integers.
- Gateway exposes no directory revision, gameplay-channel ID, general issuer directory or multi-world issuer routing.

## Canary

- Planning cut is release `3.6.1`, protocol/client `1525`, Current profile; implementation must re-pin exact current evidence.
- Current profile uses OpenTibia RSA, server challenge, modern framing/padding, sequence checksum and bounded compression signaling.
- One-shot token is consumed against selected character and Current profile.
- Source-derived successful admission reaches self-login `0x17`, pending `0x0A` and enter-world `0x0F` before map description.
- W7 may report `SessionEntered` only after ordered validation through `0x0F`, then stops before map decoding.

# Live checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T12:12:00+02:00
head: pending-current-head
branch: docs/OTC-20260730-plan-w7-technical-login
pr: 101
status: validating
required_main: 1922ef0201cd476cad2fabd42e6f9622e52891f6
proven:
  - W1-W6 are closed/archived and not launchable.
  - The plan owns ten documentation paths and no Rust product/dependency/workflow path.
  - A dedicated W7 technical-login architecture is present.
  - W7-ENTRY-CONTRACT is the sole named entry/shared type producer.
  - W7-CANARY-ENTRY is the sole initial transport/protocol-admission interface producer.
  - W7-IDENTITY and W7-LOGIN-E2E are consumers and may not define substitutes.
  - Shared Cargo/document/apps-client integration is serialized and manual Cargo.lock conflict resolution is prohibited.
  - Platform current tests prove dynamic loopback-port authorization/token exchange for the registered no-port base.
  - Current Platform/Gateway source cut is 8e613c00503c0874e69e2085c740f87f4a87e002.
  - Current Canary source cut is 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f.
derived:
  - After plan and separate archive merge, ENTRY is the first launchable worker.
  - Identity may include the real loopback adapter after exact producer revalidation; deployment evidence remains separate.
  - Canary source-derived implementation may proceed, but real Rust compatibility needs named exact controlled evidence.
unknown:
  - exact HTTPS/browser and crypto/compression dependencies; workers select only under current primary evidence and serialized lease.
conflicts: []
first_failure:
  marker: exact-head-validation-pending
  evidence: complete corrected plan is published but current-head CI and final diff/review gate are pending.
changed_paths:
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-plan-w7-technical-login.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md
validation: []
blockers:
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
  - W7-BLOCK-MULTIWORLD-CHANNEL
  - W7-BLOCK-ACCOUNT-SESSION-REUSE
  - W7-BLOCK-EXACT-CANARY-CUT
next_action: Complete exact-head CI/diff/review gate for PR #101, merge it, then archive this planning task separately before launching W7-ENTRY-CONTRACT.
```
