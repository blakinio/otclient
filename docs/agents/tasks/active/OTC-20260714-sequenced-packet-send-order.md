---
task_id: OTC-20260714-sequenced-packet-send-order
coordination_id: OTS-20260714-sequenced-packet-send-order
status: in_progress
agent: ChatGPT
branch: fix/sequenced-packet-send-serialization
base_branch: main
created: 2026-07-14T15:00:00+02:00
updated: 2026-07-14T15:00:00+02:00
last_verified_commit: "2a1b93bcdf6d4317ceeb2254b1e89429453a8e7f"
risk: high
related_issue: "blakinio/canary#245"
related_pr: "pending"
depends_on:
  - blakinio/otclient#9
blocks:
  - blakinio/canary#245
owned_paths:
  - src/framework/net/protocol.cpp
  - src/framework/net/protocol.h
  - tests/unit/protocol/**
  - docs/agents/tasks/active/OTC-20260714-sequenced-packet-send-order.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
modules_touched:
  - Framework protocol outbound transport
reuses:
  - existing Protocol framing and Connection write queue
  - existing protocol GoogleTest target
public_interfaces:
  - Protocol::send
cross_repo_tasks:
  - CAN-20260713-universal-agent-e2e-platform
---

# Goal

Preserve strict client packet sequence ordering when multiple outbound game messages are emitted close together or concurrently, so the sequence assigned during framing is the same order appended to the socket write queue.

# Acceptance criteria

- [ ] `Protocol::send` serializes framing, sequence allocation and transport enqueue for one protocol instance.
- [ ] Current login, proxy, recording, playback, checksum, XTEA and non-sequenced behavior remain unchanged.
- [ ] Concurrent sends cannot emit duplicate, skipped or wire-reordered client sequence values.
- [ ] Focused deterministic regression coverage exercises concurrent sequenced sends or the extracted serialization primitive.
- [ ] Current-head OTClient CI passes.
- [ ] Canary PR #245 consumes the final squash SHA and passes one-process two-session physical E2E.
- [ ] No timer, retry window, relog delay increase, server-side sequence relaxation or packet suppression is introduced.

# Confirmed evidence

Canary Universal Agent E2E run #33 used exact OTClient squash SHA `2a1b93bcdf6d4317ceeb2254b1e89429453a8e7f`. Database bootstrap, Canary build, OTClient build, general CI and ownership passed. The physical run produced two server-observed logins, two packet records and persisted `lastlogin`/`lastlogout`, but failed before `online_stable_2`.

The packet capture and records establish a transport ordering defect rather than a lifecycle callback race:

- session one logical outbound messages were enter-game, fight-modes and safe logout;
- the first two framed game messages carried duplicate client sequence `1`; the next carried sequence `3`;
- Canary therefore rejected the safe logout and kept the first player session until ping-timeout cleanup;
- session two emitted two automatic channel-open messages close together; their framed sequence again duplicated, and Canary closed the connection immediately;
- Canary's current transport correctly increments the expected client sequence and rejects any mismatch;
- `Protocol::send` currently performs unsynchronized `m_packetNumber++`, framing and `Connection::write` enqueue.

OTClient PR #9 remains a valid lifecycle/source-identity fix. This task addresses a separate outbound transport serialization defect exposed by the physical consumer test.

# Decisions

| Decision | Reason |
|---|---|
| Fix the OTClient sender, not Canary validation | The server correctly enforces a monotonic sequence contract; accepting duplicate/gapped sequences would hide malformed client traffic. |
| Serialize sequence allocation through transport enqueue | Atomic allocation alone cannot guarantee that packet sequence order matches wire enqueue order. |
| Keep the lock per protocol instance | Independent login/game/proxy protocols should not share a global transport bottleneck. |
| Keep `relog_delay_ms` unchanged | Scenario pacing is not a correctness mechanism and did not cause the sequence mismatch. |

# Work log

## 2026-07-14T15:00:00+02:00

- Verified OTClient PR #9 merged at final squash SHA `2a1b93bcdf6d4317ceeb2254b1e89429453a8e7f`.
- Verified Canary scenario is pinned to that exact SHA.
- Downloaded and reviewed the complete Canary run #33 artifact, including events, client/server logs, SQL state, both packet records, pcap, runtime hashes and screenshot.
- Correlated the first missing marker with duplicate/gapped client sequence values and Canary's strict inbound sequence check.
- Created this isolated follow-up branch from the final PR #9 squash commit.

# Validation and CI

| Commit | Check | Result | Notes |
|---|---|---|---|
| `2a1b93bcdf6d4317ceeb2254b1e89429453a8e7f` | Canary physical E2E run #33 | failed with actionable evidence | Lifecycle identity fix present; outbound sequence ordering still malformed under close/concurrent sends. |
| implementation head | focused protocol tests | pending | Must be deterministic and timing-independent. |
| implementation head | GitHub CI | pending | Linux/Windows and protocol tests required. |
| final squash SHA | Canary physical E2E | pending | Must prove both stable sessions and both safe logouts in one process. |

# Risks and compatibility

- The send critical section must include sequence assignment and connection/proxy enqueue, not only the counter increment.
- A non-recursive lock could deadlock if an existing send hook re-enters `Protocol::send`; implementation review must preserve current callback behavior.
- No packet fields, opcodes, feature gates, authentication payloads or Canary source are changed.
- Rollback is a source revert with no migration or persisted state.

# Remaining work

1. Implement per-protocol outbound serialization and deterministic regression coverage.
2. Publish a draft PR and inspect all CI results.
3. Merge only after current-head OTClient checks pass.
4. Pin Canary scenario to the new final squash SHA and run the complete physical proof.

# Handoff

Start with Canary run #33 evidence. Do not repeat run #33 unchanged and do not add timing-based workarounds. The first unresolved contract is the client packet sequence order at the wire boundary.
