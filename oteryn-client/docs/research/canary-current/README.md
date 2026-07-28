# Canary Current-profile evidence

Status: evidence package for future WS-R06 implementation; no adapter is implemented or authorized by this directory.

## Evidence cuts

| Repository | Revision | Role |
|---|---|---|
| `blakinio/otclient` | `9b5c86dff694aa65f4b264683f9c5ce3bf000035` | accepted Rust-client architecture, audit and wave plan |
| `blakinio/canary` | `87149c6b527f43025860c20cca0a440091ee8730` | current read-only protocol, login and multi-channel producer evidence |
| `blakinio/Oteryn-Platform` | `285eb5f89b8f83752fa4d5798bb242136b7b9ae6` | current read-only Game Gateway to Canary session-contract evidence |

The Canary evidence cut is 15 commits after the foundation-audit cut `1408aaa886240034a90fc33873e9b9e0fa47cab6`. Current source revalidation, rather than the older audit SHA, is used below.

## Evidence labels

- `PROVEN`: the exact cited revision and path directly state or implement the fact.
- `SUPPORTED`: current sources agree, but fixture or exact-pair runtime evidence is still missing.
- `INFERRED`: a client-facing consequence derived from proven sources; it is not a producer contract.
- `UNKNOWN`: the reviewed sources do not resolve the fact.
- `BLOCKED`: implementation compatibility needs missing fixtures, contracts or runtime evidence.
- `REJECTED`: current evidence contradicts the examined claim.

## Executive findings

1. `PROVEN` Canary Current remains client protocol `15.25` (`CLIENT_VERSION = 1525`) and is an enabled `CipsoftVanilla` profile. Sources: `blakinio/canary@87149c6b527f43025860c20cca0a440091ee8730:src/core.hpp` and `src/server/network/protocol/protocol_profile.{hpp,cpp}`.
2. `PROVEN` Current compatibility is not described by the numeric version alone. The profile selects transport/challenge behavior, account-login layout, game-login layout and an explicit feature mask; one Current payload branch additionally checks the login build-string prefix. Sources: `protocol_profile.{hpp,cpp}` and `protocolgame.cpp` at the same revision.
3. `PROVEN` the Current game transport uses modern block-count framing, XTEA padding, sequence checks and official compression semantics. The Current account-login response instead uses the Current login transport with Adler-32 and no compression. Sources: `protocol_profile.cpp` and `transport_codec.cpp`.
4. `SUPPORTED` the future minimum-playable adapter should target exactly one selected Canary Current revision and declared build/capability set. This package does not select a final producer/consumer pair because no Rust protocol adapter, fixture corpus or cross-repository task exists yet.
5. `PROVEN` classic Canary multi-channel login repeats each character for each available login-list channel. In the modern layout the encoded row carries the zero-based index of that response's world table, while the process `ChannelContext::channel_id` is a separate signed process identity resolved from CLI/environment/fallback. Sources: `protocollogin.cpp`, `channel_context.hpp` and `docs/multichannel/ARCHITECTURE.md`.
6. `REJECTED` treating Platform `game_worlds.id`, Canary response-local login-list `worldId`, Canary database channel row `channels.id`, Canary process `ChannelContext::channel_id` and product `WorldChannelId` as automatically identical. The current Platform contract explicitly states that Platform `game_worlds.id` is not Canary `ChannelContext::channel_id`; a client/domain mapping contract remains absent.
7. `BLOCKED` channel-aware native authentication. Gateway protocol v1 maps one configured Platform world to one exact Canary issuer and one process-local session store. It does not provide multi-world selection, replica routing or channel-aware issuer selection. Source: `blakinio/Oteryn-Platform@285eb5f89b8f83752fa4d5798bb242136b7b9ae6:docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`.

## Package contents

- [`CURRENT_PROFILE_MATRIX.md`](CURRENT_PROFILE_MATRIX.md) records the current profile, transport/login properties, feature gates and minimum-playable family ownership.
- [`FIXTURE_ACQUISITION_MANIFEST.md`](FIXTURE_ACQUISITION_MANIFEST.md) defines provenance metadata, safe fixture sources and required positive/negative coverage.
- [`CHANNEL_AND_SESSION_GAPS.md`](CHANNEL_AND_SESSION_GAPS.md) separates classic login-list channel selection from native Gateway/session routing and lists unresolved contracts.

## Implementation boundary

A later WS-R06 task must perform another fresh preflight, create shared `OTS-*`, `CAN-*` and `OTC-*` coordination, select an exact Canary producer revision and prove fixtures before writing adapter constants. It must not infer packet truth from this summary alone.

This evidence package claims no Rust build, parser correctness, successful connection, server compatibility, gameplay behavior, protocol coverage or production deployment.
