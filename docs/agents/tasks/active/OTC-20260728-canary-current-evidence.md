---
task_id: OTC-20260728-canary-current-evidence
coordination_id: ""
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R06
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-CP
parallel_lane_state: validating
coordinator_task: none
branch: docs/OTC-20260728-canary-current-evidence
base_branch: main
created: 2026-07-28T23:25:00+02:00
updated: 2026-07-28T23:32:00+02:00
last_verified_commit: "fcd52bc3b29b58bbc472ec1649ab1625c41632a7"
required_base_commit: "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
risk: low
related_issue: ""
related_pr: "#63"
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
  - current Canary profile registry, transport/login and multi-channel source
  - current Platform Game Session to Canary contract
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no credentials, private captures, packet bytes or proprietary content
  - fixture plan requires synthetic provenance and secret/private-data exclusion
---

# Goal

Revalidate the exact current Canary `ProtocolProfileId::Current` evidence needed for a future minimum-playable Rust adapter and produce a provenance-first fixture acquisition plan without adding protocol code, packet constants or external-repository changes.

# Acceptance criteria

- [x] Exact current `blakinio/canary` revision and all cited source paths are recorded.
- [x] Current client version, profile, transport/login layouts and relevant capability gates are separated from unsupported adapter claims.
- [x] The minimum-playable message-family fixture plan includes positive, boundary, truncated, malformed, wrong-gate and out-of-order cases.
- [x] Platform world IDs, Canary login-list world IDs, future product `WorldChannelId` and Canary process `channel_id` are distinguished.
- [x] Current classic multi-channel behavior and native Gateway/session limitations are recorded without inventing routing.
- [x] No protocol constants, packet bytes, product crates, Cargo files, architecture contracts, workflows or external repositories are modified.
- [x] Changed files remain limited to the isolated research path and task lifecycle.
- [ ] Documentation and repository required checks pass on this final task-record head.
- [ ] Task merges and archives independently.

# Confirmed context

- Required `blakinio/otclient` base is `9b5c86dff694aa65f4b264683f9c5ce3bf000035`.
- Current read-only Canary `main` is `87149c6b527f43025860c20cca0a440091ee8730`, 15 commits ahead of the foundation-audit cut `1408aaa886240034a90fc33873e9b9e0fa47cab6`.
- Current read-only Platform `main` is `285eb5f89b8f83752fa4d5798bb242136b7b9ae6`.
- Canary current source still declares `CLIENT_VERSION = 1525` and `ProtocolProfileId::Current` as enabled.
- Current profile source defines explicit transport, challenge, account-login, game-login and feature metadata; source existence is not adapter compatibility proof.
- No open Canary PR matching protocol-profile/login/session/multichannel research terms was found during preflight.
- Open otclient PRs #23, #37 and #48 do not own `oteryn-client/docs/research/canary-current/**`.
- External repositories remained read-only.

# Delivered evidence

- `README.md` records exact repository cuts, evidence labels, executive findings and the implementation boundary.
- `CURRENT_PROFILE_MATRIX.md` records Current protocol 15.25, transport/login properties, the exact feature mask, build-string-specific weapon-proficiency branch and MPS family ownership without copying packet constants.
- `FIXTURE_ACQUISITION_MANIFEST.md` defines mandatory metadata/provenance fields, safe synthetic acquisition, positive/boundary/truncated/malformed/wrong-gate/out-of-order coverage and the future harness gate.
- `CHANNEL_AND_SESSION_GAPS.md` distinguishes five identifier concepts, documents classic response-local world indexing, preserves relog semantics and lists the contracts/E2E required for channel-aware native auth.

# Material findings

1. Current compatibility is a tuple of exact Canary revision, `ProtocolProfileId::Current`, protocol 1525, transport/login layouts, feature mask and exact build string—not just `15.25`.
2. The modern multi-channel login response writes a response-local zero-based world-table index into world/character rows; this is not automatically a stable product channel ID.
3. Platform `game_worlds.id`, Canary database/process channel IDs, response-local world index and product `WorldChannelId` require an explicit mapping/stability contract.
4. Native-auth protocol v1 remains bounded to one configured Platform world and one exact process-local Canary issuer; arbitrary channel selection is blocked.
5. The first WS-R06 implementation should isolate Current transport/login fixtures before any channel-aware Gateway contract work.

# Source review

Current Canary source reviewed at `87149c6b527f43025860c20cca0a440091ee8730`:

- `src/core.hpp`;
- `src/server/network/protocol/protocol_profile.{hpp,cpp}`;
- `src/server/network/protocol/transport_codec.{hpp,cpp}`;
- `src/server/network/protocol/protocollogin.{hpp,cpp}`;
- `src/server/network/protocol/protocolgame.{hpp,cpp}`;
- `src/game/multichannel/channel_context.hpp`;
- `docs/multichannel/ARCHITECTURE.md`;
- session/admission ownership paths identified in the matrix/manifest.

Current Platform contract reviewed at `285eb5f89b8f83752fa4d5798bb242136b7b9ae6`:

- `docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`.

Accepted client evidence reviewed at `9b5c86dff694aa65f4b264683f9c5ce3bf000035`:

- foundation Canary audit;
- Rust architecture/security/protocol boundary;
- current parallel wave;
- cross-repository contract registry.

# Validation

| Revision | Check | Result | Evidence |
|---|---|---|---|
| `9b5c86dff694aa65f4b264683f9c5ce3bf000035` | otclient live preflight | PASS | W2-CP path unclaimed |
| `87149c6b527f43025860c20cca0a440091ee8730` | Canary source/profile preflight | PASS | exact Current profile, transport/login, build branch and channel serializer reviewed |
| `285eb5f89b8f83752fa4d5798bb242136b7b9ae6` | Platform contract preflight | PASS | exact current v1 capability boundary and identifier warning reviewed |
| `fcd52bc3b29b58bbc472ec1649ab1625c41632a7` | complete evidence/content review | PASS | four research docs plus task only; no byte fixture or product-contract change |
| final task-record head | repository CI | pending | exact-head docs validation required |

# Boundaries preserved

- no packet constants or bytes copied into Rust code;
- no claim that a future adapter supports current Canary;
- no edit to `CROSS_REPO_CONTRACTS.md` or accepted architecture;
- no creation of Canary/Oteryn Platform tasks or writes;
- no credentials, private captures, proprietary assets or personal data;
- no broad legacy-profile or advanced-feature implementation scope;
- no Rust build, parser, server, runtime or performance claim.

# Remaining work

1. Pass exact-head required CI.
2. Mark PR #63 ready, inspect files/diff/comments/reviews/threads/base and squash-merge.
3. Archive this task in a separate lifecycle PR.

# Completion

- Final status: awaiting exact-head CI
- PR: #63
- Merge commit: pending
- Archived at: pending
