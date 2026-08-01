---
task_id: OTC2-20260801-playability-p0-legacy
status: completed
agent: "P0 legacy parity worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-legacy
phase: archived
branch: docs/OTC2-20260801-playability-p0-legacy
base_branch: main
created: 2026-08-01T19:00:00+02:00
updated: 2026-08-01T20:23:00+02:00
last_verified_commit: "346d1bd8513fbe635873303b2818848ef3b2e489"
required_base_commit: "6007a5dfe2cfcf7429c7ef999b51f37244b21d0c"
result_merge: "8eb6d33f5ec8a22d3daf8b7a23cf5eca524875d3"
related_pr: 141
risk: medium
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: work
---

# Result

The P0 legacy workflow and functional parity scenario discovery lane is complete and merged through PR #141.

# Durable outputs

- `oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md`
- `oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md`
- merge `8eb6d33f5ec8a22d3daf8b7a23cf5eca524875d3`

The reports normalize user-visible launch/auth/selection, world/navigation, HUD/combat, items/containers, chat/NPC, settings/action bars, minimap/audio, relog/recovery and installation/update workflows into M1-M6 scenarios. They separate core playability, core gameplay, daily product and exact-profile feature families.

# Validation

Clean restacked head `346d1bd8513fbe635873303b2818848ef3b2e489`:

- Rust Client run `30712144007` — PASS;
- Windows job `91401340297` — PASS;
- Supply Chain job `91401340276` — PASS;
- repository CI run `30712144118` — PASS;
- required job `91401454738` — PASS;
- ready-for-review required job `91401875582` — PASS;
- exact changed-file review — three owned documentation paths;
- comments, reviews and unresolved threads — none.

# Boundaries and blockers

No legacy/Rust source, OTUI/Lua architecture, proprietary asset/binary, password fallback, automation or PR #23 path was made normative. Exact-profile scenario scope remains conditional on the Canary evidence and explicit product classification. Asset, UX and release acceptance consume their accepted P0 reports.

# Next action

Merge/archive the Canary P0 lane, then aggregate all accepted evidence into the capability matrix and smallest safe P1 contract-producer plan.
