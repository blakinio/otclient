---
task_id: OTC2-20260804-dual-protocol-architecture
coordination_id: OTS-20260804-native-protocol-selection
status: completed
agent: "dual protocol architecture documentation owner"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: WS-R05-WS-R07-architecture
branch: docs/OTC2-20260804-dual-protocol-architecture
base_branch: main
created: 2026-08-04T11:04:00+02:00
completed: 2026-08-04T13:04:00+02:00
archived: 2026-08-04T13:04:00+02:00
product_pr: 257
product_head: "622bae7c4ffb5356d52b87d733c78ed16b6995b1"
product_merge: "dadfe0f7f89bc3cb5102da8714e03a326d6898ba"
temporary_prs: [259, 260]
risk: medium
owned_paths: []
shared_path_lease: []
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
execution_mode: github-only
complete_user_facing_feature: false
---

# Terminal result

The Rust-client architecture now defines and mandates the following direction for future agents:

- `protocol-canary` remains the independently supported exact compatibility adapter;
- `protocol-oteryn` is a future independent preferred native adapter and must not wrap or translate through Canary;
- both adapters map to protocol-neutral `GameCommand` and `GameEvent` contracts;
- client networking is migrated later through a separately measured, application-owned Tokio transport/session package;
- the current synchronous worker transport remains valid until that package merges;
- Otheryn keeps its asynchronous ASIO networking unless a separate profiling-backed ADR changes the server;
- production protocol selection uses bounded authoritative server-advertised `Auto` preference for native Oteryn, with force modes restricted to development/test;
- one game-entry attempt and gameplay session bind exactly one adapter;
- no in-session or post-credential/ticket/authentication/protocol-violation downgrade is allowed;
- the client sends semantic player intent while Otheryn remains authoritative for movement, combat, spells, resources, inventory, loot, economy, random outcomes and persistence.

# Delivered paths

- `oteryn-client/AGENTS.md`;
- `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md`;
- `oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md`;
- `oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md`.

The temporary workflow `.github/workflows/otc2-dual-protocol-docs.yml` was removed from the final product tree.

# Validation

| Head | Check | Result |
|---|---|---|
| `622bae7c4ffb5356d52b87d733c78ed16b6995b1` | complete path/link/claim/authority/downgrade audit | PASS; 0 material findings |
| `622bae7c4ffb5356d52b87d733c78ed16b6995b1` | repository CI | PASS; run `30899249211` |
| `622bae7c4ffb5356d52b87d733c78ed16b6995b1` | Rust Client | PASS; run `30899248948` |
| PR #257 | review threads | PASS; 0 unresolved |
| PR #257 | mergeability and protected merge | PASS; squash merge `dadfe0f7f89bc3cb5102da8714e03a326d6898ba` |

Earlier temporary-runner validation:

- PR #259 / run `30896012843`: PASS;
- PR #260 / run `30896670824`: PASS.

# E2E

`NOT_APPLICABLE` — the task changed architecture and governance documentation only. No executable client/server behavior, packet layout, authentication behavior, asset or production state changed.

# Claim boundary

This completed task does not claim that Tokio, automatic protocol negotiation or `protocol-oteryn` is implemented. Product implementation remains future work under coordinated, separately owned packages and exact producer/consumer evidence.

# Follow-up programme

Use coordination ID `OTS-20260804-native-protocol-selection` for the linked client/server programme unless superseded by a later accepted ADR.

Required order:

1. protocol-neutral Tokio transport and game-session supervisor migration in `blakinio/otclient`;
2. exact cross-repository native Oteryn framing, capability, sequencing, action-result, reconciliation and rollout contract;
3. Otheryn native server producer/service while preserving ASIO by default;
4. Rust `protocol-oteryn` consumer adapter;
5. automatic selection and downgrade-negative tests;
6. semantic player-action lifecycle and compatible-pair integration evidence.

# Ownership release

All documentation and workflow leases held by this task are released. Future tasks must claim their own exact paths and re-check live ownership before mutation.
