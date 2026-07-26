---
program_id: OTC-PROGRAM-UPSTREAM-INTELLIGENCE
name: OTClient Upstream Intelligence
status: active
owner: "GPT-5.6 Thinking"
created: 2026-07-26
updated: 2026-07-26
baseline_date: 2026-07-17
baseline_common_tip: "bdea0b23b4a738809d698cb7e4f88a299dd6bffc"
last_verified_target_commit: "ca78b71397cd2196ab841144c27275d0462902d7"
last_verified_upstream_commit: "e1a1ff150332b8879c91d46d8dc1402e78af9c3e"
machine_registry: artifacts/upstream/otclient/candidates.json
---

# OTClient Upstream Intelligence

## Mission

Maintain a durable, reviewable record of upstream and fork differences that may improve
`blakinio/otclient` without treating commit messages, hashes or feature count as proof.
The programme compares actual code, deduplicates equivalent work, evaluates Canary
compatibility and records integration risk before any implementation task is authorized.

This document is the human-readable source of truth. The machine-readable mirror is
`artifacts/upstream/otclient/candidates.json`. Update both in the same bounded PR.

## Safety and operating rules

- `blakinio/otclient` is the only writable repository.
- `opentibiabr/otclient` and watched forks are read-only evidence sources.
- Monitoring and classification do not authorize implementation.
- No candidate may be implemented, cherry-picked, pushed or merged without an explicit
  implementation task such as `IMPLEMENT <ID>`.
- Compare actual target and source code; never infer equivalence from SHA or title alone.
- Split bundled fixes by behavior and preserve local Oteryn, protocol-session and asset
  safety contracts.
- Report only new or materially changed P0/P1/P2 candidates and tracked-status changes.
- Record uncertainty as `TEST`, `PROFILE`, `WATCH` or `DEFERRED`, never as handled.
- Canary-coupled changes require exact field/version evidence and the existing cross-repo
  contract process.
- A future audit appends one dated history entry and refreshes repository/fork tips,
  candidate statuses and evidence references.

## Baseline

The durable comparison baseline is the audit from **2026-07-17**:

- common/upstream tip: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`;
- target tip: `2a1b93bcdf6d4317ceeb2254b1e89429453a8e7f`;
- target relation at that time: 9 commits ahead, 0 behind.

## Current snapshot — 2026-07-26

| Role | Repository | Ref | Verified SHA | Commits after baseline common tip |
|---|---|---|---|---:|
| Target | `blakinio/otclient` | `main` | `ca78b71397cd2196ab841144c27275d0462902d7` | 37 |
| Upstream | `opentibiabr/otclient` | `main` | `e1a1ff150332b8879c91d46d8dc1402e78af9c3e` | 24 |

These counts are measured independently from the common baseline. Because the target
contains squash merges and adapted upstream effects, subtracting the counts does not
produce a valid exact ahead/behind relation.

### Watched fork tips

| Repository | Tip | State |
|---|---|---|
| `OTAcademy/otclientv8` | `08d348b8b0c5d87ef5415be1950da1e324b5373b` | tip recorded |
| `tibia-devs/otclient-mehah` | `5c276fa02cf0f9ffec188832d223b93b82f5de00` | tip recorded |
| `zimbadev/otc` | `0236ecf0d36c6384ac7a7ddbc600af87da79a5db` | tip recorded |
| `solchanel/otclient-15` | `86f2c397863e3a3fb5413ca83c0436d72fb21a23` | tip recorded; code triage required |

A recorded tip is not an endorsement or a parity claim.

## Candidate registry

| Priority | ID | Source | Candidate | Status | Disposition | Target state |
|---|---|---|---|---|---|---|
| P0 | `OTC-INT-001` | opentibiabr/otclient#1758 | Lua/C++ callback heap corruption | PENDING | IMPLEMENT_OR_ADAPT | missing |
| P1 | `OTC-INT-002` | opentibiabr/otclient#1765 | NPC trade active-imbuement double subtraction | IMPLEMENTED | ADAPTED | present via local PR #26 |
| P2 | `OTC-INT-003` | opentibiabr/otclient#1763 | draw preLoad before foreground | DEFERRED | TEST_OR_ADAPT | excluded from local PR #26 |
| P2 | `OTC-INT-004` | opentibiabr/otclient#1761 | AnimateAlways respects Animator timings | IMPLEMENTED | IMPLEMENTED | present via local PR #26 |
| P1 | `OTC-INT-005` | OTAcademy/otclientv8@ece0ee8cd4049c57eed3a2550aef7c8e2e87bae3 | proxy-enabled exit crash | PENDING | MANUAL_REIMPLEMENTATION | missing |
| P1 | `OTC-ISSUE-001` | opentibiabr/otclient#1691 | Forge scheduled Lua callback lifecycle race | IMPLEMENTED | ADAPTED | merged local PR #35; archived by #42 |
| P1 | `OTC-ISSUE-002` | opentibiabr/otclient#1738 | protocol 15.24 compatibility bundle | PARTIAL | SPLIT_ADAPT | bundle unresolved |
| P1 | `OTC-ISSUE-003` | opentibiabr/otclient#1743 | Forge Convergence on Canary 15.11+ | BLOCKED | TEST_OR_ADAPT | not resolved |
| P2 | `OTC-ISSUE-004` | opentibiabr/otclient#1753 | Wheel conviction summary indices | IMPLEMENTED | IMPLEMENTED | merged local PR #34; archived by #41 |
| P2 | `OTC-ISSUE-005` | opentibiabr/otclient#946 and #1757 | missing lastManualWalk breaks bundled game_bot | IMPLEMENTED | IMPLEMENTED | present via local PR #26 |
| P2 | `OTC-ISSUE-006` | opentibiabr/otclient#1562 | container drop and hit-testing | PENDING | TEST_OR_ADAPT | nearest-child workaround remains incomplete |
| P2 | `OTC-ISSUE-007` | opentibiabr/otclient#1601 and #1764 | AutoStats CPU overhead | PARTIAL | ADAPT | pause/resume present via local PR #26 |
| P2 | `OTC-ISSUE-008` | opentibiabr/otclient#1731 | startup performance | PROFILE | PROFILE | not measured |
| P2 | `OTC-ISSUE-009` | opentibiabr/otclient#1447 | outfit window performance | PROFILE | PROFILE | not measured |
| P2 | `OTC-ISSUE-010` | opentibiabr/otclient#1041 | updater checksum blocks UI | PROFILE | PROFILE_THEN_ADAPT | not resolved |
| P1 | `OTC-NEW-001` | opentibiabr/otclient#1752 | unknown opcode busy-loop/OOM recovery | IMPLEMENTED | IMPLEMENTED | present via local PR #26 |
| P2 | `OTC-NEW-002` | opentibiabr/otclient#1766 | client asset archive selection by version | IN PROGRESS | ADAPT | local PR #37 open/draft |
| P1 | `OTC-NEW-003` | opentibiabr/otclient#1748 | Reward Wall shrine/panel source-byte semantics | DEFERRED | ADAPT | excluded from local PR #26 |
| P2 | `OTC-NEW-004` | opentibiabr/otclient#1767 | peekBytes truncates length to 8 bits | PENDING | IMPLEMENT | missing locally |
| P2 | `OTC-NEW-005` | opentibiabr/otclient#1768 | creature information flicker while walking | TEST | TEST_OR_ADAPT | missing locally |
| P2 | `OTC-NEW-006` | opentibiabr/otclient#1750 | ground-border use-with target fallback | IMPLEMENTED | IMPLEMENTED | present via local PR #26 |
| P1 | `OTC-NEW-007` | opentibiabr/otclient#1775 | Canary 15.25 Monk protocol/vocation/relog bundle | PARTIAL | SPLIT_TEST_OR_ADAPT | character-list relog fixed by local PR #31 |
| P1 | `OTC-NEW-008` | opentibiabr/otclient#1772 | Cyclopedia automap flag subtype byte not consumed | PENDING | ADAPT_OR_IMPLEMENT | missing locally |
| P1 | `OTC-NEW-009` | opentibiabr/otclient#1774 | Gem Atelier wrong gem lock/destroy and inverted state | PENDING | ADAPT_OR_IMPLEMENT | missing locally |
| P2 | `OTC-NEW-010` | opentibiabr/otclient#1773 | stale container loot-value frame | PENDING | TEST_OR_ADAPT | missing locally |
| P2 | `OTC-NEW-011` | opentibiabr/otclient#1771 | equipped expirestop countdown runs locally | PENDING | ADAPT_OR_IMPLEMENT | missing locally |

Detailed notes, dependencies, deduplication entries, watch items and untriaged upstream
commits are stored in the JSON registry.

## Priority and status model

- **P0:** corruption, security boundary, unrecoverable crash or severe protocol failure.
- **P1:** Canary compatibility, crash/lifecycle, protocol desync or material correctness.
- **P2:** bounded correctness, UI/rendering or measured performance/maintainability.
- **IMPLEMENTED:** verified present in target code through a local merged task.
- **PARTIAL:** one subcase or incomplete upstream concept is present.
- **PENDING:** evidence supports work, but no target implementation is complete.
- **TEST / PROFILE:** adoption is blocked on reproduction, benchmark or exact contract.
- **DEFERRED / BLOCKED:** a named dependency or safety contract prevents adoption.

## Deduplication baseline

The following remain closed unless fresh target evidence proves regression:

- issue #1650 / merged #1652;
- issue #1665 / merged #1675;
- issues #1644 and #1574 / merged #1684;
- issue #1733 / merged #1739;
- `tibia-devs/otclient-mehah@b967b440...` DrawPool null guard;
- already-present `GameTileAddThingWithStackpos` and `GameCharacterSkillStats` feature IDs.

## Audit workflow

1. Re-fetch target, upstream and watched-fork tips.
2. Inspect open target PRs and active task ownership.
3. Search new/changed upstream commits, PRs and issues.
4. Compare source code with current target code.
5. Deduplicate equivalent, partial and superseding implementations.
6. Evaluate Canary version/field compatibility, regression risk and integration cost.
7. Update the Markdown and JSON registry together.
8. Create implementation work only after explicit authorization for a candidate ID.

## Audit history

### 2026-07-17 — baseline

Established the original candidate set and target/upstream relation.

### 2026-07-26 — durable registry bootstrap

Imported the audited candidate state into Git. Recorded the current target/upstream/fork
tips, merged local Forge and Wheel work, the local upstream-sync result, active assets
work and the newest upstream 15.25 candidates. No runtime implementation was performed
by this registry task.
