---
task_id: OTC-20260727-rust-client-foundation-audit
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R00
branch: docs/OTC-20260727-rust-client-foundation-audit
base_branch: main
created: 2026-07-27T00:25:00+02:00
updated: 2026-07-27T01:05:00+02:00
last_verified_commit: "8103788a242497bb459a7e3dfe3d297e9d2bac63"
risk: high
related_pr: "#47"
depends_on:
  - merged PR #45
  - merged PR #46
blocks: []
owned_paths:
  - oteryn-client/docs/audits/foundation/**
  - docs/agents/tasks/archive/OTC-20260727-rust-client-foundation-audit.md
crates_touched: []
features_touched: []
contracts_touched: []
modules_touched: []
public_interfaces:
  - foundation audit evidence set
  - recommended WS-R01 bootstrap boundary
cross_repo_tasks: []
---

# Goal

Complete the mandatory foundation audit for the greenfield Rust Oteryn client and recommend one narrow first implementation package without adding product code.

# Completion summary

The audit delivered an index plus ten evidence-labelled reports under `oteryn-client/docs/audits/foundation/` covering:

- product and minimum-playable feature inventory;
- Canary Current-profile 15.25 candidate compatibility;
- Oteryn Identity, account/game-session and channel-relog contracts;
- assets, provenance, licensing and prohibited material;
- reproducible P0-P8 performance scenes;
- Windows platform, unresolved hardware tiers and dependency gates;
- reusable tests and required synthetic fixtures;
- risk register;
- decision/gap log;
- one bounded WS-R01 bootstrap recommendation.

# Principal findings

- Canary implements real gameplay channels as separate processes and can expose the same character once per channel in the classic world list.
- Current Oteryn Gateway -> Canary protocol v1 maps one Platform world to one exact Canary issuer/process and does not define arbitrary selected-channel issuer routing.
- Platform world ID, Canary login-list world ID and process `channel_id` require an explicit mapping contract.
- Oteryn-native `character + world + gameplay channel -> one-shot ticket` remains a cross-repository blocker.
- Real game asset redistribution rights remain blocked; no proprietary bytes were committed.
- Numeric Windows performance baselines and concrete hardware tiers remain blocked; reproducible measurement procedures are now defined.
- The only authorized next implementation package is WS-R01 workspace/toolchain/dependency-policy/architecture-check bootstrap.

# Evidence cuts

| Repository | Revision |
|---|---|
| `blakinio/otclient` | `5568cb6f5e2fd6162c78cde304deea5d32461e05` |
| `blakinio/canary` | `1408aaa886240034a90fc33873e9b9e0fa47cab6` |
| `blakinio/Oteryn-Platform` | `348f483938fc8358132128fc79d229e38b98045b` |

External repositories remained read-only.

# Validation

| Evidence | Result |
|---|---|
| complete 12-file changed-path/full-patch review on `049612370d05e77652c62b724597badc1ec3edce` | PASS |
| exact-head CI run `30223820037` on `8103788a242497bb459a7e3dfe3d297e9d2bac63` | PASS |
| ready-for-review exact-head CI run `30223983499` | PASS |
| Detect Build Scope, both Fast Checks, Lua Syntax and `CI / Required` | PASS |
| Windows build | correctly skipped for documentation-only scope |
| comments/requested changes | none |

# Merge

- PR: #47
- Method: squash
- Merge commit: `7d367f6eca857eb55ef44599e447966daf278f36`
- Merged: 2026-07-27

# Rejected approaches

- freezing exact packet constants in the foundation audit;
- equating Platform and Canary channel/world identifiers;
- claiming Gateway v1 supports arbitrary multi-channel routing;
- treating asset downloadability as redistribution permission;
- inventing performance/hardware results;
- creating Cargo/product crates inside the audit;
- selecting application dependencies before their owning spike.

# Next action

Start WS-R01 Rust workspace/toolchain/dependency-policy/architecture-check bootstrap after this archive lifecycle PR merges. The initial workspace must contain only a narrow tooling member and synthetic graph fixtures, with no product placeholder crates or application dependencies.

# Completion

- Final status: completed
- PR: #47
- Merge commit: `7d367f6eca857eb55ef44599e447966daf278f36`
- Catalogue updated: not required
- Changelog updated: not required
- Archived at: `docs/agents/tasks/archive/OTC-20260727-rust-client-foundation-audit.md`
