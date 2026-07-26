# Greenfield Rust Client Foundation Audit

Status: in progress  
Audit task: `OTC-20260727-rust-client-foundation-audit`  
Evidence cut: 2026-07-27

## Purpose

This audit establishes the verified inputs required before creating the production Rust workspace for the Oteryn client. It treats the current C++/Lua/OTUI client as behavior and compatibility evidence, not as the architecture to port.

## Evidence repositories and cuts

| Repository | Evidence role | Reviewed main revision |
|---|---|---|
| `blakinio/otclient` | maintained client behavior, tests, assets and native-auth consumer evidence | `5568cb6f5e2fd6162c78cde304deea5d32461e05` |
| `blakinio/canary` | current game protocol, multi-channel and game-session producer evidence | `1408aaa886240034a90fc33873e9b9e0fa47cab6` |
| `blakinio/Oteryn-Platform` | Identity, ticket, Gateway and cross-repository contract evidence | `348f483938fc8358132128fc79d229e38b98045b` |

External repositories are read-only evidence sources for this task. A later implementation task must revalidate their current revisions.

## Evidence labels

| Label | Meaning |
|---|---|
| `PROVEN` | exact source, contract, test or runtime evidence supports the statement |
| `SUPPORTED` | consistent evidence exists but one required proof is missing |
| `INFERRED` | reasoned conclusion that is not authoritative |
| `UNKNOWN` | insufficient evidence |
| `BLOCKED` | required source, legal approval or runtime environment is unavailable |
| `REJECTED` | investigated hypothesis is contradicted by evidence |

## Audit documents

1. [`01-product-and-feature-inventory.md`](01-product-and-feature-inventory.md)
2. [`02-canary-compatibility.md`](02-canary-compatibility.md)
3. [`03-oteryn-identity-and-session.md`](03-oteryn-identity-and-session.md)
4. [`04-assets-and-licensing.md`](04-assets-and-licensing.md)
5. [`05-performance-baseline.md`](05-performance-baseline.md)
6. [`06-platform-and-hardware.md`](06-platform-and-hardware.md)
7. [`07-test-and-fixture-inventory.md`](07-test-and-fixture-inventory.md)
8. [`08-risk-register.md`](08-risk-register.md)
9. [`09-gap-and-decision-log.md`](09-gap-and-decision-log.md)
10. [`10-bootstrap-recommendation.md`](10-bootstrap-recommendation.md)

## Executive findings

### Proven foundations

- `PROVEN` Canary current protocol profile uses client version `1525` and a profile/feature registry rather than one undifferentiated parser. Evidence: `blakinio/canary/src/core.hpp`, `src/server/network/protocol/protocol_profile.hpp`.
- `PROVEN` Canary has a real multi-channel process and login-list architecture: one process per channel, a channel registry and repeated `(character, channel)` entries through the existing world list. Evidence: `blakinio/canary/docs/multichannel/ARCHITECTURE.md`, `src/game/multichannel/channel_context.hpp`.
- `PROVEN` Oteryn native authentication is implemented end to end through PKCE, a one-time Platform ticket, Gateway redeem and a one-time Canary Game Session credential carried in the existing `GameSessionKey` field. Evidence: `blakinio/Oteryn-Platform/docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`.
- `PROVEN` the maintained client and server already contain behavior surfaces for the minimum playable slice: map, creatures, items, movement, containers, stats, chat and game-session lifecycle.
- `PROVEN` the existing test foundation includes C++ unit/integration tests, Lua tests and protocol loopback support. It is evidence only; it will not be linked into the Rust workspace.

### Critical gap

- `BLOCKED` the current Gateway -> Canary protocol v1 is intentionally one Platform world mapped to one exact Canary issuer process. It explicitly does not claim multi-world issuer selection or horizontally replicated issuer routing. Platform `game_worlds.id` is also explicitly not Canary `ChannelContext::channel_id`.
- `PROVEN` classic Canary login can expose channels as world entries without a new game protocol.
- `INFERRED` the new Rust client can initially consume that classic world/channel list through the Canary adapter, but the desired Oteryn-native flow `character + world + gameplay channel -> one-shot ticket` requires a new explicit Platform/Gateway/Canary routing contract before it can be claimed.

### Asset and performance status

- `BLOCKED` repository evidence does not establish redistribution rights for all required game sprites, things, sounds, fonts or other proprietary content. The audit commits no such bytes.
- `BLOCKED` no reproducible Windows runtime measurements were available in this environment. The audit defines exact scenes and procedures rather than inventing FPS, memory or hardware results.

### Bootstrap decision

The first implementation package should be **WS-R01 workspace/toolchain and architecture-policy bootstrap only**. It must not implement a renderer, protocol, assets, UI or game domain. Details are in `10-bootstrap-recommendation.md`.

## Gate result

The audit does not authorize Canary gameplay implementation yet. It authorizes a narrow repository/toolchain bootstrap after this audit is accepted and merged.
