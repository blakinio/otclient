---
task_id: OTC-20260730-plan-w7-technical-login
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-C
parallel_lane_state: ready
branch: docs/OTC-20260730-plan-w7-technical-login
base_branch: main
created: 2026-07-30T11:49:00+02:00
updated: 2026-07-30T12:00:00+02:00
last_verified_commit: ""
required_base_commit: "1922ef0201cd476cad2fabd42e6f9622e52891f6"
risk: high
related_pr: "#101"
depends_on:
  - W6 closure PR #98 and archive PR #100
owned_paths:
  - docs/agents/tasks/active/OTC-20260730-plan-w7-technical-login.md
  - docs/agents/README.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md
shared_path_lease: []
contract_role: coordination-only
contracts_produced:
  - accepted W7 lane/ownership/dependency/lease/evidence plan only
contracts_consumed:
  - current Rust architecture and lifecycle
  - Oteryn Platform/Gateway source 8e613c00503c0874e69e2085c740f87f4a87e002
  - Canary source 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
crates_touched: []
features_touched: []
contracts_touched:
  - planning metadata only; no production API or protocol implementation
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

Prepare one accepted, bounded multi-agent plan for the first compilable Rust Oteryn technical-login slice. This task implements no worker package and launches no worker.

# Planning acceptance

- [x] Reconciled exact current main `1922ef0201cd476cad2fabd42e6f9622e52891f6`.
- [x] Verified PR #93 merged and archived through #95.
- [x] Verified W6 implementation/archive/closure/closure-archive through PRs #92/#94/#98/#100.
- [x] Verified PR #23 remains legacy UI-only and PR #48 remains isolated operational non-merge work.
- [x] Verified PR #97 owns only one legacy-client asset-rehearsal workflow/task and no W7 path/lease.
- [x] Verified no active Rust task/open PR owns Identity, account-session, directory, game-session, transport, protocol-canary, login composition or E2E paths.
- [x] Verified every prior Cargo, lockfile, dependency-policy and shared-document lease is released.
- [x] Published one coordinator plus exactly four bounded worker lanes.
- [x] Published exact dependency graph, owned paths, sole producers/consumers, shared-path lease protocol and merge/archive order.
- [x] Published automated versus interactive evidence matrix.
- [x] Published exact milestone acceptance criteria and exclusions.
- [x] Published exact coordinator prompt and four exact worker prompts.
- [x] Recorded current Platform/Gateway/Canary source cuts and legacy-reference proof boundary.
- [x] Recorded fixed callback URI versus OS-assigned-port conflict without inventing an API or weakening security.
- [x] Recorded no multi-world/channel, reusable account-session, deployed TLS/secret-manager or production claim.
- [x] Detected and removed a concurrent unowned `TECHNICAL_LOGIN.md` draft that incorrectly claimed dynamic-port acceptance contrary to current Platform source.
- [ ] Pass exact-head CI, inspect complete nine-file diff and confirm no unresolved review threads.
- [ ] Merge through repository gates and archive this planning task separately before any worker launch.

# Plan outputs

| Output | Path |
|---|---|
| accepted wave/dependency/ownership/lease/evidence/acceptance plan | `oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md` |
| coordinator prompt | `oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md` |
| ENTRY prompt | `oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md` |
| IDENTITY prompt | `oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md` |
| CANARY prompt | `oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md` |
| LOGIN E2E prompt | `oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md` |
| current exact producer evidence and blockers | `docs/agents/CROSS_REPO_CONTRACTS.md` |
| routing/read order | `docs/agents/README.md` |

# Exact contract findings

## Platform/Gateway

- Native public Authorization Code + PKCE `S256` path exists.
- Current source requires redirect exactly `http://127.0.0.1/callback` and rejects an explicit port.
- Game Login Ticket issuance revokes the access token and associated refresh token, bounding W7 to one bootstrap attempt.
- Gateway protocol v1 accepts only `{protocol_version:1, game_login_ticket}` and returns one opaque session credential plus authoritative worlds/characters.
- `World.id` and `Character.id/world_id` are signed 64-bit JSON integers.
- Gateway exposes no directory revision, gameplay-channel ID, general issuer directory or multi-world issuer routing.

## Canary

- Current source cut is release `3.6.1`, protocol/client `1525`, Current profile.
- Current profile uses OpenTibia RSA, server challenge, modern block-count/padding, sequence checksum and official compression signaling.
- Source-derived minimal successful admission prefix reaches login `0x17`, pending-state `0x0A` and enter-world `0x0F` before map description.
- W7 may report `SessionEntered` after ordered validation through `0x0F`, then stop and disconnect before map decoding.
- Canary PR #815 physical E2E used legacy OTClient and older exact revisions; it is reference evidence only.

# Live checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T12:00:00+02:00
head: pending-current-commit
branch: docs/OTC-20260730-plan-w7-technical-login
pr: 101
status: ready
required_main: 1922ef0201cd476cad2fabd42e6f9622e52891f6
proven:
  - W1-W6 are closed/archived and not launchable.
  - Current plan owns exactly nine documentation paths and no Rust/dependency/workflow path.
  - W7-ENTRY-CONTRACT is the sole named entry/shared type producer.
  - W7-CANARY-ENTRY is the sole initial transport/protocol-admission interface producer.
  - W7-IDENTITY and W7-LOGIN-E2E are consumers and may not define substitutes.
  - Shared Cargo/document/apps-client integration is serialized and manual Cargo.lock conflict resolution is prohibited.
  - Current Platform/Gateway source cut is 8e613c00503c0874e69e2085c740f87f4a87e002.
  - Current Canary source cut is 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f.
derived:
  - After plan and separate archive merge, ENTRY is the first launchable worker.
  - IDENTITY real browser/listener adapter remains blocked; deterministic/fake work may proceed.
  - CANARY source-derived implementation may proceed, but real Rust compatibility needs named physical evidence.
unknown:
  - exact HTTPS/browser and crypto/compression dependencies; workers must select only under current evidence and serialized lease.
conflicts:
  - W7-BLOCK-IDENTITY-REDIRECT: fixed no-port Platform redirect versus OS-assigned-port Rust security invariant.
  - concurrent TECHNICAL_LOGIN.md claimed dynamic-port support without current source evidence and was removed from the branch.
first_failure:
  marker: exact-head-validation-pending
  evidence: the complete plan is published but current-head CI and final diff/review gate are pending.
changed_paths:
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-plan-w7-technical-login.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md
  - oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md
validation: []
blockers:
  - W7-BLOCK-IDENTITY-REDIRECT
  - W7-BLOCK-REAL-RUST-E2E
  - W7-BLOCK-DEPLOYMENT-EVIDENCE
  - W7-BLOCK-MULTIWORLD-CHANNEL
  - W7-BLOCK-ACCOUNT-SESSION-REUSE
next_action: Complete exact-head CI/diff/review gate for PR #101, merge it, then archive this planning task separately before launching W7-ENTRY-CONTRACT.
```
