# W7 Canary Current Admission Evidence

Task: `OTC2-20260731-w7-canary-entry`  
Wave: `OTERYN-W7-TECHNICAL-LOGIN`  
Draft PR: `#113`  
Evidence cut date: 2026-07-31

## Scope

This document covers only the smallest W7 transport, protocol-core and Canary Current technical-admission boundary. It does not claim gameplay, map decoding, creature/item support, channel relog, automatic reconnect or deployed compatibility.

## Exact revisions

- OTClient task base: `3c33f97fe2dca533d14a4284c3b13a7b6220a85d`;
- shared W7 entry producer merge: `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`;
- selected read-only Canary revision: `95b276db311cf6e9acd58b847f1fb0ca6697b137`;
- accepted Canary protocol source cut: `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`.

A compare from the accepted Canary cut to the selected revision contains no network, protocol-game or login-session source change. The selected revision is used for every compatibility statement.

## PASS

### Ownership and contract reuse

- W7 plan and lifecycle archive are merged.
- `W7-ENTRY-CONTRACT` is merged and archived.
- The implementation imports `GameEntryRequest`, `AdmissionCredential`, `EntryLifecycle`, `EntryFailure`, `SessionEntered`, `CharacterId`, `WorldId` and `GameplayChannelId` from their merged owners.
- No substitute entry credential, identifier or lifecycle type is introduced.
- W7-CANARY-ENTRY owns the three planned crates, exact contract path and evidence path.
- The shared Cargo/document lease was free when task `OTC2-20260731-w7-canary-entry` and draft PR `#113` were created.

### Bounded generic implementation

Implemented on the task branch:

- `oteryn-transport`:
  - one already-resolved `SocketAddr` per explicit connect attempt;
  - non-zero connect/read/write timeouts;
  - explicit cancellation observation before connect and between partial reads/writes;
  - checked zero/oversized frame rejection before allocation or I/O;
  - maximum inbound and outbound frame sizes;
  - `try_reserve_exact` before bounded input allocation;
  - deterministic `Disconnected -> Connecting -> Connected/Closed` state;
  - no resolver, background daemon, reconnect loop or raw-socket escape hatch;
  - stable error categories without operating-system/backend text.
- `oteryn-protocol-core`:
  - checked little-endian integer helpers;
  - bounded exact reads and writes;
  - checked `u16` length-prefixed UTF-8 strings;
  - malformed, truncated, oversized, invalid UTF-8 and trailing-data rejection;
  - closed stable protocol errors;
  - no Canary constants.
- `oteryn-protocol-canary`:
  - exact Current profile metadata only;
  - public `connect`, `enter_session`, `cancel` and `close` responsibility;
  - no application access to sockets or admission credentials;
  - production real admission blocked before network and before credential handoff;
  - original synthetic-only admission mode compiled only for tests;
  - synthetic success delegates `SessionEntered` construction to the shared `EntryLifecycle`;
  - local duplicate/expired credential rejection occurs before the synthetic network-attempt counter increments;
  - every terminal synthetic result closes the adapter.

Execution results remain pending workspace integration and exact-head CI. PASS above describes code invariants established by complete diff inspection, not yet executed checks.

## OBSERVED

### Selected Current profile

Read-only sources:

- `src/core.hpp`;
- `src/server/network/protocol/protocol_profile.hpp`;
- `src/server/network/protocol/protocol_profile.cpp`.

Observed exact facts:

- release `3.6.1`;
- client/protocol version `1525`;
- profile identifier `current`;
- wire family `CipsoftVanilla`;
- RSA family `OpenTibia`;
- support state enabled;
- server-first Current challenge;
- Current game sequence transport;
- modern XTEA block-count outer length;
- modern decrypted padding-count byte;
- sequence checksum in both directions;
- official compression layout;
- sequence high bit signals compression;
- decoded body length is checked from `raw_count * 8 + 4`.

### Packet and field bounds

Read-only sources:

- `src/utils/const.hpp`;
- `src/server/network/message/networkmessage.hpp`;
- `src/server/network/protocol/transport_codec.cpp`.

Observed exact facts:

- network-message buffer `65,500` bytes;
- client input-message maximum `4,096` bytes;
- character/player-name maximum `30` bytes;
- message length type `u16`;
- transport rejects zero decoded body size and values outside `u16`;
- encrypted frame payload length must be a multiple of eight;
- modern decrypted payload begins with a padding byte whose value cannot exceed decrypted message length.

### Current admission request structure

Read-only source: `src/server/network/protocol/protocolgame.cpp`, `ProtocolGame::onRecvFirstMessage`.

Observed Current field order:

1. operating-system `u16`;
2. protocol version `u16`;
3. client version `u32`;
4. length-prefixed client-version string;
5. length-prefixed asset-hash identifier;
6. preview-state byte;
7. RSA-decrypted bootstrap block;
8. four `u32` XTEA key words;
9. game-master flag;
10. length-prefixed session key;
11. length-prefixed character name;
12. challenge timestamp `u32`;
13. challenge random byte.

Current requires challenge response. A mismatch disconnects immediately.

### GameSessionKey semantics

Read-only sources:

- `src/security/login_session_manager.hpp`;
- `src/security/login_session_manager.cpp`;
- `src/server/network/protocol/protocolgame.cpp`.

Observed exact facts:

- raw token is 256 random bits encoded as wire-safe text;
- server stores only SHA-256 token hash;
- binding includes account, allowed character names and protocol profile;
- default TTL is 60 seconds;
- maximum active token count is 4,096;
- a matching token is removed before account/character/profile/expiry fields are inspected;
- wrong character or wrong profile therefore burns the token;
- concurrent successful redemption is impossible;
- the game protocol falls back to the existing session authentication path and returns the session-expired denial when authentication fails.

The denial is sufficient only for combined `CredentialExpiredOrConsumed`; it does not prove the exact sub-cause.

### Success and denial boundary

Read-only source: `src/server/network/protocol/protocolgame.cpp`.

Observed ordered Current success prefix:

1. `0x17` login/self packet;
2. `0x1A` bug-report permission packet;
3. `0xEF` Tibia-time packet;
4. `0x0A` pending-state-entered packet;
5. `0x0F` enter-world packet;
6. map description after the selected boundary.

`0x0F` after the ordered prefix is sufficient for the W7 `SessionEntered` technical marker. W7 does not parse the following map payload.

`disconnectClient` writes `0x14`, a length-prefixed message and then closes. Some malformed/bootstrap paths close without a denial packet.

## UNKNOWN

The following facts are not proven by a permissible committed fixture or controlled Rust run:

- exact production client-version string for the named deployment;
- exact production asset-hash identifier;
- exact complete client-to-server RSA block bytes;
- exact OpenTibia RSA public-key material and encoding provenance approved for this Rust client;
- exact complete encrypted frame bytes for Current challenge/login/success/denial;
- whether a particular deployment enables a different outer TLS layer, proxy or DNS route;
- deployed Platform revision and credential issuer configuration;
- deployed Canary revision, port, firewall and secret-manager wiring;
- a fresh configured credential for a named controlled test character;
- real Rust XTEA/sequence/compression interoperability;
- clean real close behavior after the first technical entry marker;
- any gameplay packet compatibility after `0x0F`.

## BLOCKED

### `W7-BLOCK-REAL-RUST-E2E`

Real admission is intentionally disabled before network I/O and before credential handoff. Required unblock evidence:

1. repository-policy-approved complete Current transcript fixture provenance, or a named controlled capture process whose committed output is permitted;
2. exact client-version string and asset-hash values;
3. exact RSA public-key material and encoding provenance;
4. one fresh one-shot credential bound to the exact character and Current profile;
5. one named controlled Rust run at exact OTClient, Canary, Platform and deployment revisions;
6. observed decoded order through `0x17 -> 0x1A -> 0xEF -> 0x0A -> 0x0F`;
7. confirmation that no secret bytes appear in logs, errors, fixtures or crash output;
8. clean close after the technical marker.

### `W7-BLOCK-DEPLOYMENT-EVIDENCE`

No claim is made about DNS, TLS, proxy, firewall, secret manager, production endpoint or deployed revision. Those require named environment evidence outside this source-only lane.

## Synthetic fixture provenance

All synthetic bytes and credentials are original Oteryn test material authored for this task. Synthetic tag values and framing are deliberately unrelated to Canary. They are safe to commit and may establish parser/lifecycle behavior only.

## Validation checkpoint

Not yet executed on the current head:

- `cargo metadata --locked`;
- `cargo fmt --all --check`;
- workspace Clippy with warnings denied;
- all workspace tests;
- architecture checks;
- `cargo deny check`;
- required GitHub CI;
- final full-diff and review-thread inspection.

The sandbox has no Cargo toolchain and cannot resolve GitHub for cloning. Exact validation will therefore be performed by repository CI after serialized workspace integration; unavailable local execution will remain explicitly recorded.
