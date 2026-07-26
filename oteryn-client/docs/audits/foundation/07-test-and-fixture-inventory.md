# Test and Fixture Inventory

## Evidence scope

This document identifies reusable behavior evidence and gaps. Legacy C++/Lua test code is not linked into the Rust workspace.

## Maintained client test foundation

`PROVEN` `tests/CMakeLists.txt` establishes:

- GoogleTest-based C++ tests linked to `otclient_core`;
- C++20 tests;
- unit, map, stdext, OTML, integration and Lua subtrees;
- CTest labels and timeouts;
- Windows-specific build handling.

`PROVEN` the module catalogue records reusable legacy infrastructure:

| Existing support | Current role | Rust reuse policy |
|---|---|---|
| `InputMessageBuilder` | deterministic framed parser input | reuse semantics/expected bytes only after exact Canary proof; reimplement in Rust |
| `OutputMessageInspector` | inspect encoded output | reimplement Rust-native fixture inspector |
| Thing/Tile builders and assertions | synthetic map/object setup | audit behavior and create new typed Rust builders |
| `TestEnvironment` and fakes | isolate global legacy resources/game | do not port global seams; create dependency-injected Rust fakes |
| Lua runner/stubs | module lifecycle behavior | behavior evidence only; no Lua runtime in Rust product |
| protocol loopback | bounded local socket integration | model for Rust adapter integration, not shared code |
| OTML fixtures | legacy UI parse behavior | not reusable in native Rust UI |

## Maintained lifecycle regression evidence

`PROVEN` recent maintained-client work includes focused evidence for:

- exact source `ProtocolGame` callback validation;
- stale old-session callback protection;
- action-bar cooldown state across relog/rebuild;
- character-list recreation after relog;
- Forge scheduled callback cleanup;
- options event cancellation/migration;
- Oteryn Identity one-shot session handling.

Rust implication:

- preserve scenarios as normalized lifecycle tests;
- do not reproduce legacy globals, time-window guards or Lua lifecycle mechanics;
- every async result carries exact owner/session generation and cancellation.

## Oteryn Identity and Game Session evidence

`PROVEN` authoritative contract documents:

- positive Gateway -> Canary issue;
- idempotent duplicate issuance;
- conflicting duplicate rejection;
- credential rotation acceptance/rejection;
- single-use consumption;
- wrong-character/profile burn semantics;
- expiry rejection;
- rollback/kill-switch behavior;
- bounded login/logout/replay E2E.

Rust fixtures needed:

```text
identity_pkce_success
identity_state_mismatch
identity_stale_callback
identity_duplicate_callback
ticket_ttl_too_long
gateway_route_success
gateway_wrong_world_or_channel
game_credential_success
game_credential_replay
game_credential_expired
reconnect_does_not_replay_initial_credential
relog_channel_1_to_2_fresh_credentials
```

Current status: `SUPPORTED`; exact client-facing response fixtures and channel-aware contract do not yet exist.

## Canary protocol evidence

### Proven source-level structures

- protocol profile and feature registry;
- transport profiles;
- account and game login layouts;
- Current profile version `1525`;
- build-specific 15.25 payload gates;
- multi-channel login list and process context;
- game-session admission integration.

### Missing committed Rust-ready corpus

`BLOCKED` no complete, provenance-documented synthetic corpus exists for the new client's minimum-playable Current-profile message families.

The first adapter fixtures must include metadata:

```text
fixture_schema_version
source_repository
source_commit
producer_path
protocol_profile
client_version
client_build_string
feature_mask
direction
message_family
normalization_expectation
provenance
contains_personal_or_secret_data = false
```

### Fixture acquisition order

1. challenge/game-login envelope;
2. session-start/error/end;
3. map description and one tile update;
4. unknown/known creature and movement;
5. inventory/equipment and one container;
6. basic player data/stats;
7. move/turn/use/use-with/attack/follow commands;
8. local/system chat;
9. ping/logout;
10. later feature families.

Each family requires positive, minimal, maximal-bounded, truncated, malformed, wrong-gate and out-of-order cases.

## Canary multi-channel tests needed by client

Source architecture is `PROVEN`, but client-facing contract tests still need:

- directory/world list with one character repeated across Channel 1/2/3;
- stable typed mapping from wire `worldId` to `WorldChannelId`;
- offline/maintenance channel omitted or marked according to exact producer behavior;
- user selection preserved through refresh only by typed ID;
- ticket/route scoped to selected channel when the future native contract exists;
- relog Channel 1 -> Channel 2 destroying old session state;
- delayed Channel 1 callback unable to affect Channel 2;
- no reuse of Channel 1 credential;
- channel unavailable after selection;
- classic Canary path versus Oteryn-native directory path producing the same application selection model.

## Asset fixtures

Permitted committed fixture classes:

- original tiny generated RGBA images;
- synthetic sprite/animation metadata;
- original short generated PCM/audio tone if audio tests need it;
- original/open-license test font with recorded license, or generated font-independent metrics fixtures;
- corrupt/truncated pack/index cases;
- path traversal/archive metadata without proprietary content;
- signed test manifests using test-only keys.

Forbidden without reviewed rights:

- official sprite/item/outfit/effect images;
- official sound/music/font/package bytes;
- extracted binary catalogs or maps;
- private download archives/URLs/tokens.

Required asset test corpus:

```text
valid_minimal_pack
valid_multichunk_pack
bad_signature
bad_content_hash
out_of_bounds_index
overflowing_count
truncated_chunk
compression_bomb
path_traversal_source
unsupported_schema
client_asset_protocol_mismatch
interrupted_update_and_rollback
```

## Domain/replay fixtures

The Rust client needs protocol-independent scenarios:

- initial world snapshot;
- tile/entity delta sequence;
- local movement and server correction;
- inventory/container mutations;
- combat target/health updates;
- chat insertion and ordering;
- normal logout;
- stale callback/event after session replacement;
- 100-cycle channel relog;
- reconnect rejected -> return to selection.

A normalized replay includes domain schema, initial snapshot, capability set, deterministic clock and ordered events/commands. It contains no auth secrets or private chat by default.

## UI fixtures

Original/synthetic datasets:

- character list with 1, 20 and 200 entries;
- one character across multiple gameplay channels;
- channel online/full/maintenance/offline/queue states;
- long localized names and missing optional metadata;
- thousands of chat rows;
- 500 battle-list rows;
- large market table;
- nested containers/inventory;
- DPI/resolution matrices;
- keyboard-only and screen-reader metadata.

Screenshots/reference images must be original and tolerate backend/platform rasterization differences appropriately.

## Renderer/benchmark fixtures

Required synthetic scenes P1–P8 are defined in `05-performance-baseline.md`.

Scene data records:

- schema version and hash;
- deterministic entity/tile/item counts;
- asset pack hash;
- camera/input script;
- frame/warm-up/sample counts;
- expected invariants rather than vendor-specific exact pixels where unsuitable.

## Security/fuzz corpus

First-class negative corpora:

- arbitrary/truncated protocol frames;
- length/count mutation;
- decompression bombs;
- stale/duplicate auth callbacks;
- ticket replay/expiry/wrong scope;
- corrupt settings/layout/replay files;
- asset offset/hash/signature mutation;
- extension resource exhaustion when extensions are implemented.

Fuzz findings must be minimized and committed only when they contain no protected/private content.

## Test architecture for Rust

After bootstrap:

- crate-local unit/property tests near source;
- top-level cross-crate integration tests;
- deterministic fake clock/random/ID providers;
- no live network requirement for normal CI;
- fake Identity/Gateway/Canary endpoints;
- exact wire fixtures isolated under versioned protocol paths;
- headless domain/replay tests on all required CI;
- Windows runtime/GPU tests in milestone-specific jobs;
- no test-only public API that weakens production ownership/security.

## Reuse decision table

| Existing artifact | Reuse directly? | Decision |
|---|---:|---|
| legacy C++ test binaries/helpers | no | `REJECTED` runtime/build dependency |
| legacy test scenario descriptions | yes | `PROVEN` useful after behavior verification |
| exact synthetic wire bytes | conditional | only with producer commit/provenance and no protected data |
| live packet captures | no by default | `BLOCKED` privacy/provenance; prefer synthetic |
| legacy OTUI snapshots | no | native Rust UI and asset rights |
| Oteryn contract/E2E identifiers | yes as evidence | revalidate exact current revisions in implementation task |
| Canary source profile definitions | yes as source of truth | select exact commit per adapter package |

## Audit conclusion

- `PROVEN` enough behavior/test infrastructure exists to define the Rust test architecture and minimum scenarios.
- `BLOCKED` a complete Rust-ready Canary Current-profile corpus.
- `PROVEN` the first bootstrap package can add deterministic repository/tooling tests without waiting for protocol or assets.
