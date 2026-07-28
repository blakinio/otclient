---
task_id: OTC-20260728-canary-current-evidence
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R06
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-CP
parallel_lane_state: active
coordinator_task: none
branch: docs/OTC-20260728-canary-current-evidence
base_branch: main
created: 2026-07-28T23:25:00+02:00
updated: 2026-07-28T23:25:00+02:00
last_verified_commit: "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
required_base_commit: "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
risk: low
related_issue: ""
related_pr: pending
depends_on:
  - merged foundation audit PR #47
  - merged current parallel-wave plan PR #59
integration_after:
  - "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
blocks:
  - accurate future WS-R06 protocol-adapter package selection
owned_paths:
  - oteryn-client/docs/research/canary-current/**
  - docs/agents/tasks/active/OTC-20260728-canary-current-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - current Canary protocol-profile source evidence
  - accepted Oteryn client architecture and foundation audit
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted contract modification
modules_touched: []
reuses:
  - foundation audit Canary compatibility report
  - accepted protocol-boundary and session architecture
  - current Canary profile registry and multi-channel source
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no credentials, private captures, packet bytes or proprietary content
---

# Goal

Revalidate the exact current Canary `ProtocolProfileId::Current` evidence needed for a future minimum-playable Rust adapter and produce a provenance-first fixture acquisition plan without adding protocol code, packet constants or external-repository changes.

# Acceptance criteria

- [ ] Exact current `blakinio/canary` revision and all cited source paths are recorded.
- [ ] Current client version, profile, transport/login layouts and relevant capability gates are separated from unsupported adapter claims.
- [ ] The minimum-playable message-family fixture plan includes positive, boundary, truncated, malformed, wrong-gate and out-of-order cases.
- [ ] Platform world IDs, Canary login-list world IDs, future product `WorldChannelId` and Canary process `channel_id` are distinguished.
- [ ] Current classic multi-channel behavior and native Gateway/session limitations are recorded without inventing routing.
- [ ] No protocol constants, packet bytes, product crates, Cargo files, architecture contracts, workflows or external repositories are modified.
- [ ] Changed files remain limited to the isolated research path and task lifecycle.
- [ ] Documentation and repository required checks pass on exact head.
- [ ] Task merges and archives independently.

# Confirmed context

- Current `blakinio/otclient` base is `9b5c86dff694aa65f4b264683f9c5ce3bf000035`.
- Current read-only Canary `main` is `87149c6b527f43025860c20cca0a440091ee8730`, 15 commits ahead of the foundation-audit cut `1408aaa886240034a90fc33873e9b9e0fa47cab6`.
- Canary current source still declares `CLIENT_VERSION = 1525` and `ProtocolProfileId::Current` as enabled.
- Current profile source defines explicit transport, challenge, account-login, game-login and feature metadata; source existence is not adapter compatibility proof.
- No open Canary PR matching protocol-profile/login/session/multichannel research terms was found during preflight.
- Open otclient PRs #23, #37 and #48 do not own `oteryn-client/docs/research/canary-current/**`.
- External repositories remain read-only.

# Evidence labels

- `PROVEN`: exact current source or accepted contract directly states the fact.
- `SUPPORTED`: several current sources agree but required fixture/runtime proof is missing.
- `INFERRED`: reasoned client-facing implication, not an authoritative producer contract.
- `UNKNOWN`: source does not resolve the fact.
- `BLOCKED`: a required producer contract, fixture or environment is absent.
- `REJECTED`: evidence contradicts the examined claim.

# Plan

1. Open an early draft PR.
2. Review current profile registry, transport/login code, MPS message producers and multi-channel/session sources.
3. Review the current Platform/Canary session contract only where needed for channel/routing gaps.
4. Write the four isolated evidence documents with exact revisions and paths.
5. Review the full docs-only diff, drive exact-head CI to green, merge and archive separately.

# Validation

| Revision | Check | Result | Evidence |
|---|---|---|---|
| `9b5c86dff694aa65f4b264683f9c5ce3bf000035` | otclient live preflight | PASS | W2-CP path unclaimed |
| `87149c6b527f43025860c20cca0a440091ee8730` | Canary revision/profile preflight | PASS | `CLIENT_VERSION=1525`; current profile enabled; external repo read-only |

# Boundaries

- no packet constants or bytes copied into Rust code;
- no claim that a future adapter supports current Canary;
- no edit to `CROSS_REPO_CONTRACTS.md` or accepted architecture;
- no creation of Canary/Oteryn Platform tasks or writes;
- no credentials, private captures, proprietary assets or personal data;
- no broad legacy-profile or advanced-feature implementation scope.

# Remaining work

1. Open the draft PR and complete source-focused evidence collection.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
