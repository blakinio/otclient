---
task_id: OTC2-20260804-platform-gateway-protocol-plan
coordination_id: OTS-20260804-native-protocol-selection
status: completed
agent: "platform gateway protocol architecture owner"
project_lane: otclient-v2
track: greenfield-rust
created: 2026-08-04T16:01:00+02:00
completed: 2026-08-04T16:31:00+02:00
archived: 2026-08-04T16:31:00+02:00
product_pr: 263
product_head: "61d5e3db6d91e28e5391d3d78c0e7181540c7cdb"
product_merge: "90c1b44ca63ba96aae52b406883014c5cca48976"
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
---

# Terminal result

The Rust-client architecture and cross-repository registry now explicitly reuse the delivered Oteryn native game-entry chain:

```text
Rust client
-> system browser
-> Oteryn Identity OAuth Authorization Code + PKCE
-> one-time Game Login Ticket
-> Oteryn Game Gateway
-> private atomic redeem
-> World Registry and Game Session
-> Otheryn game server
-> selected gameplay adapter
```

The documentation prevents future agents from creating another login server, embedding Oteryn password authentication in the native client, bypassing Game Gateway, sending OAuth or Game Login Ticket credentials to the wrong component, or treating Gateway API `protocol_version: 1` as a gameplay protocol profile.

# Delivered paths

- `oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md`;
- `oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md`;
- `docs/agents/CROSS_REPO_CONTRACTS.md`;
- `oteryn-client/docs/agents/prompts/OTC2_TOKIO_TRANSPORT_AGENT.md`;
- `oteryn-client/docs/agents/prompts/OTS_NATIVE_PROTOCOL_CONTRACT_AGENT.md`.

# Accepted responsibility split

| Repository/component | Responsibility |
|---|---|
| `blakinio/Oteryn-Platform` / Identity | reusable credentials, browser OAuth/PKCE, MFA/security policy, account binding, ticket issue/redeem and World Registry |
| `blakinio/Oteryn-Platform` / Go Game Gateway | ticket acceptance/redeem, authoritative login context, world routing, Game Session orchestration and future protocol-candidate/session-binding producer |
| `blakinio/Otheryn` | Game Session consumer, allowed-profile validation and authoritative native/Canary gameplay production |
| `blakinio/otclient` | OAuth/Gateway consumer, protocol-neutral Tokio transport, selection policy and independent `protocol-canary` / `protocol-oteryn` adapters |

# Execution order

Only these packages are launchable immediately:

1. Package A — protocol-neutral Tokio transport in `blakinio/otclient`;
2. Package B — exact three-repository native protocol contract across Platform, Otheryn and the Rust client, with no runtime implementation.

Later packages remain dependency-gated:

1. Platform/Game Gateway protocol-candidate and Game Session binding producer;
2. Otheryn native gameplay producer and session enforcement;
3. Rust `protocol-oteryn` adapter;
4. automatic selection and downgrade-negative three-repository E2E;
5. full semantic gameplay-action lifecycle.

# Validation

| Head | Check | Result |
|---|---|---|
| `7a434338a00152e63393fa5167c83d854f41bcce` | first exact-head repository CI | PASS; run `30917797793`, required job `92020788439` |
| `7a434338a00152e63393fa5167c83d854f41bcce` | first exact-head Rust Client | PASS; run `30917797133` |
| `61d5e3db6d91e28e5391d3d78c0e7181540c7cdb` | final merge-ref revalidation repository CI | PASS; run `30918360500` |
| `61d5e3db6d91e28e5391d3d78c0e7181540c7cdb` | final merge-ref revalidation Rust Client | PASS; run `30918360161` |
| PR #263 | exact changed paths | PASS; six expected documentation/task/prompt files |
| PR #263 | full role/version/downgrade/current-versus-target audit | PASS; zero material findings |
| PR #263 | review threads | PASS; zero unresolved |
| PR #263 | protected merge | PASS; squash merge `90c1b44ca63ba96aae52b406883014c5cca48976` |

Windows formatting, strict Clippy, workspace tests, architecture policy and supply-chain validation passed.

# E2E

`NOT_APPLICABLE` — documentation, governance and reusable prompt delivery only. No Rust runtime, Cargo dependency, packet layout, authentication runtime, Platform/Gateway service, Otheryn server, workflow, asset or production state changed.

# Claim boundary

This completed task does not claim that Tokio, a native protocol candidate producer, `protocol-oteryn`, automatic adapter selection or the expanded action lifecycle is implemented.

It defines the authoritative dependencies and provides the two prompts safe to launch from the current state.

# Ownership release

All task ownership and shared-path leases are released.
