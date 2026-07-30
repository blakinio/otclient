---
task_id: OTC-20260730-plan-w7-technical-login
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W7-TECHNICAL-LOGIN
parallel_lane: W7-C
parallel_lane_state: active
branch: docs/OTC-20260730-plan-w7-technical-login
base_branch: main
created: 2026-07-30T11:49:00+02:00
updated: 2026-07-30T11:49:00+02:00
last_verified_commit: ""
required_base_commit: "1922ef0201cd476cad2fabd42e6f9622e52891f6"
risk: high
related_pr: pending
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
  - current Oteryn Platform/Gateway native-auth contracts
  - current Canary Current-profile admission source
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

Prepare one accepted, bounded multi-agent plan for the first compilable Rust Oteryn technical-login slice. Do not implement or launch worker packages from this planning task.

# Required outcome

Publish one coordinator lane and at most four worker lanes:

- `W7-ENTRY-CONTRACT`
- `W7-IDENTITY`
- `W7-CANARY-ENTRY`
- `W7-LOGIN-E2E`

The plan must contain exact ownership, one public producer per contract, dependency/merge order, shared-path lease serialization, automated/interactive evidence, explicit external blockers, exact acceptance criteria and exact copy-ready prompts.

# Live preflight

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T11:49:00+02:00
head: pending
branch: docs/OTC-20260730-plan-w7-technical-login
pr: pending
status: active
required_main: 1922ef0201cd476cad2fabd42e6f9622e52891f6
proven:
  - PR #93 merged and its task archive merged through PR #95.
  - W6 implementation PR #92, archive #94, closure #98 and closure archive #100 are merged.
  - W1-W6 are closed, archived and not launchable.
  - PR #23 remains legacy OTUI/Lua presentation only.
  - PR #48 remains isolated operational non-merge work.
  - PR #97 owns only one legacy-client asset rehearsal workflow and its task; it owns no Rust login path or W7 shared path.
  - No active Rust task or open PR owns Identity, account-session, world-directory, game-session, transport, protocol-canary, technical-login composition or login E2E paths.
  - Every prior Rust Cargo, Cargo.lock, dependency-policy and shared-document lease is released.
  - Current Oteryn Platform/Gateway source evidence cut is 8e613c00503c0874e69e2085c740f87f4a87e002.
  - Current Canary source evidence cut is 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f.
derived:
  - W7 planning may proceed without pre-claiming worker paths or leases.
unknown:
  - exact dependency selections for HTTPS/OAuth browser integration and Current-profile crypto/compression remain worker evidence decisions under the serialized Cargo lease.
conflicts:
  - current Platform enforces redirect URI exactly http://127.0.0.1/callback with no port, while the normative Rust security model requires an OS-assigned loopback port.
first_failure:
  marker: plan-content-pending
  evidence: the planning task and branch exist, but the accepted wave record and exact prompts are not yet published.
changed_paths:
  - docs/agents/tasks/active/OTC-20260730-plan-w7-technical-login.md
validation: []
blockers:
  - Real browser callback integration is blocked until the fixed-redirect producer contract and OS-assigned-port security invariant are reconciled by exact evidence or an accepted architecture/producer change.
next_action: Open the early draft PR, publish the exact W7 plan and prompts, validate/merge it, then archive this planning task separately before any worker launch.
```
