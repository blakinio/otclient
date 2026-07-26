---
task_id: OTC-20260727-rust-client-foundation-audit
status: awaiting_final_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R00
branch: docs/OTC-20260727-rust-client-foundation-audit
base_branch: main
created: 2026-07-27T00:25:00+02:00
updated: 2026-07-27T00:55:00+02:00
last_verified_commit: "049612370d05e77652c62b724597badc1ec3edce"
risk: high
related_pr: "#47"
depends_on:
  - merged PR #45
  - merged PR #46
blocks:
  - Rust workspace bootstrap
  - Canary adapter implementation
  - production asset pipeline
  - measured hardware/performance acceptance
owned_paths:
  - oteryn-client/docs/audits/foundation/**
  - docs/agents/tasks/active/OTC-20260727-rust-client-foundation-audit.md
crates_touched: []
features_touched: []
contracts_touched: []
modules_touched: []
reuses:
  - merged Rust client architecture and audit plan
  - maintained C++/Lua client source/tests as behavior evidence only
  - Canary source and multi-channel documentation as read-only producer evidence
  - Oteryn Platform game-session contract as read-only identity/session evidence
public_interfaces:
  - foundation audit evidence set
  - recommended WS-R01 bootstrap boundary
cross_repo_tasks: []
---

# Goal

Complete the mandatory foundation audit for the greenfield Rust Oteryn client and recommend exactly one narrow first implementation package. Do not add Cargo workspace files, production crates or product implementation.

# Acceptance criteria

- [x] Audit index plus all ten numbered audit documents exist under `oteryn-client/docs/audits/foundation/`.
- [x] Product behavior is classified into minimum playable, Beta, Later and unresolved contract scope without mirroring legacy modules.
- [x] Canary Current profile 15.25 is identified as the candidate initial adapter family without freezing an unverified implementation commit or packet constants.
- [x] Canary multi-channel behavior and the current Oteryn Gateway -> Canary v1 limitation are documented separately.
- [x] Oteryn Identity, account session, directory, one-shot ticket, game session, reconnect and channel-relog evidence is classified.
- [x] Asset formats, provenance categories, prohibited material and redistribution blockers are documented without adding asset bytes.
- [x] Reproducible P0-P8 performance scenes and evidence rules are defined without inventing results or hardware tiers.
- [x] Windows-first platform and dependency decision gates are documented; exact package versions remain implementation decisions.
- [x] Reusable legal test evidence and required Rust protocol/domain/asset/UI/security fixtures are inventoried.
- [x] Risk register identifies likelihood, impact, owner/mitigation and earliest gate.
- [x] Accepted decisions are separated from blocked cross-repository, legal, runtime and product gaps.
- [x] Exactly one narrow first package is recommended: WS-R01 workspace/toolchain/dependency-policy/architecture-check bootstrap.
- [x] No Cargo workspace, production crate, legacy runtime dependency, protocol constant, private capture, secret or proprietary asset is added.
- [x] Complete 12-file changed-path/full-patch consistency review is recorded.
- [ ] Exact-head required CI passes.
- [ ] Autonomous merge gate is satisfied.

# Evidence cuts

| Repository | Reviewed revision | Role |
|---|---|---|
| `blakinio/otclient` | `5568cb6f5e2fd6162c78cde304deea5d32461e05` | maintained client behavior, tests, assets and native-auth consumer evidence |
| `blakinio/canary` | `1408aaa886240034a90fc33873e9b9e0fa47cab6` | protocol, multi-channel and game-session producer evidence |
| `blakinio/Oteryn-Platform` | `348f483938fc8358132128fc79d229e38b98045b` | Identity/Gateway/game-session contract evidence |

External repositories remained read-only. Every implementation task must revalidate live revisions and open PRs.

# Delivered audit set

1. `README.md` — evidence policy, cuts and executive gate result.
2. `01-product-and-feature-inventory.md` — behavior inventory and MPS.
3. `02-canary-compatibility.md` — Current 15.25 candidate, profiles, fixtures and multi-channel/native-auth gap.
4. `03-oteryn-identity-and-session.md` — credential taxonomy, account/game lifetimes, directory, relog and reconnect.
5. `04-assets-and-licensing.md` — formats, provenance, prohibited material and pack requirements.
6. `05-performance-baseline.md` — P0-P8 scenes, measurement metadata and blocked numeric baseline.
7. `06-platform-and-hardware.md` — Windows scope, unresolved tiers and dependency gates.
8. `07-test-and-fixture-inventory.md` — reusable evidence and required synthetic corpora.
9. `08-risk-register.md` — risks R-001 through R-075 and highest blockers.
10. `09-gap-and-decision-log.md` — accepted decisions versus contract/legal/runtime/product gaps.
11. `10-bootstrap-recommendation.md` — one bounded WS-R01 implementation package.

# Confirmed findings

## Canary

- `PROVEN` current protocol version is 1525 and Canary uses explicit protocol profiles/features/transport layouts.
- `PROVEN` one process per gameplay channel and classic login world-list repetition of the same character per channel are implemented.
- `SUPPORTED` the initial Rust adapter should target one exact Current-profile 15.25 Canary revision selected at implementation time.
- `REJECTED` supporting every legacy profile in the first adapter.

## Identity and channels

- `PROVEN` PKCE -> Platform ticket -> Gateway -> one-use Canary Game Session -> existing `GameSessionKey` admission works for one exact configured issuer/process.
- `PROVEN` Platform world ID is not automatically Canary `ChannelContext::channel_id`.
- `BLOCKED` current Gateway protocol v1 does not define arbitrary selected-channel issuer routing or shared issuer state.
- `BLOCKED` native Oteryn `character + world + gameplay channel -> ticket` requires a new shared mapping/routing/fencing contract.
- `SUPPORTED` classic Canary world-list channel selection can be consumed by a Canary adapter independently of that native contract.

## Assets and performance

- `BLOCKED` redistribution rights for required real game sprites, type packages, sounds, fonts and other proprietary content.
- `PROVEN` synthetic asset packs/scenes and importer/security tooling can be built without those bytes.
- `BLOCKED` numeric performance baseline and concrete hardware tiers because no runnable controlled Windows environment/assets were available.
- `PROVEN` the required benchmark scenes, metadata and percentile-based measurement procedure are now defined.

# Bootstrap recommendation

The audit authorizes one next package only:

```text
WS-R01 Rust workspace/toolchain/dependency-policy/architecture-check bootstrap
```

The initial workspace contains only a narrow architecture-policy tool and synthetic graph fixtures. It does not add product application, renderer, protocol, domain, UI, asset, audio or feature crates and does not add application dependencies such as `wgpu`, windowing, async, HTTP/TLS, text, audio or WASM libraries.

# Work log

## 2026-07-27T00:25:00+02:00

- Created audit-only branch from current `main` after PR #45 and #46 merged.
- Claimed only foundation-audit documents and this task record.
- Opened draft PR #47 early.

## 2026-07-27T00:48:00+02:00

- Inspected live open PR/task ownership and confirmed no path overlap.
- Audited maintained client source/tests/assets, Canary current protocol/multi-channel source and Oteryn Platform game-session contract at exact revisions.
- Produced the index and all ten numbered audit outputs with explicit evidence labels.
- Identified the channel-aware native issuer-routing contract as the principal cross-repository blocker.
- Preserved asset-rights and runtime-performance unknowns rather than inventing data.
- Recommended one non-product WS-R01 bootstrap package.

## 2026-07-27T00:55:00+02:00

- Reviewed all 12 changed files and the complete PR patch.
- Confirmed the diff contains only the active task record, audit index and ten numbered Markdown reports.
- Checked relative links, evidence-cut consistency, gameplay-channel terminology, Current-profile qualification and separation of accepted decisions from unknown/blocked facts.
- Confirmed there are no Cargo files, workflow changes, runtime code, copied legacy content, binary assets, secrets, credentials or private captures.
- Confirmed the bootstrap recommendation creates only one tooling member and explicitly defers product crates and application dependencies.
- No unsupported runtime, production, legal or performance claim was found.

# Validation and CI

| Commit | Check | Result | Evidence |
|---|---|---|---|
| `8bab327cb80acbb39a96f388b532abf793530251` | required output creation | PASS | audit index + ten numbered documents present; documentation/task paths only |
| `049612370d05e77652c62b724597badc1ec3edce` | complete changed-file/full-patch consistency review | PASS | 12 declared Markdown paths, 2354 additions, no deletions or out-of-scope content |
| final task-record head | required documentation/fast CI | pending | no C++ or Rust build is required for audit-only content |

# Rejected approaches

- Freezing exact packet opcodes/fields in the foundation audit rather than a selected-commit adapter task.
- Treating classic Canary `worldId`, Platform world ID and process channel ID as one identifier.
- Claiming Gateway protocol v1 supports arbitrary multi-channel native routing.
- Treating downloadability as asset redistribution permission.
- Inventing FPS, memory or supported hardware without a runnable benchmark environment.
- Creating Cargo/product crates inside the audit.
- Selecting application dependencies before their owning implementation spike.

# Risks and compatibility

- Runtime: no runtime behavior changes.
- Protocol: findings are evidence and package boundaries, not a frozen opcode implementation.
- Assets: no content bytes or uncertain-license material are included.
- Security: no credentials, tickets, private logs or packet captures are included.
- Cross-repository: external repositories remained read-only; blocked contracts require separately coordinated tasks.
- Rollback: normal documentation PR revert.

# Remaining work

1. Update PR #47 body with findings and final review state.
2. Pass exact-head required CI.
3. Mark ready, recheck reviews/mergeability/checks and squash-merge.
4. Archive this task through a separate lifecycle PR.
5. Start the recommended WS-R01 bootstrap task only after audit merge/archive.

# Handoff

## Start here

- `oteryn-client/docs/audits/foundation/README.md`
- `oteryn-client/docs/audits/foundation/09-gap-and-decision-log.md`
- `oteryn-client/docs/audits/foundation/10-bootstrap-recommendation.md`

## Do not repeat

Do not create another audit architecture, commit real game assets, freeze protocol constants, or start product crates before the audit is merged.

## First next action

Perform a fresh preflight for the WS-R01 workspace/toolchain/architecture-check bootstrap and inspect live CI ownership before claiming workflow paths.

# Completion

- Final status: awaiting final CI
- PR: #47
- Merge commit: pending
- Catalogue updated: not required; no reusable implementation interface added
- Changelog updated: not required; audit evidence only
- Archived at: pending
