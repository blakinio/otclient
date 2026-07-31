# Canary Current Entry Contract — W7 Evidence Cut

Status: source-verified, real-wire implementation blocked  
Consumer: `oteryn-protocol-canary`  
Shared entry producer: OTClient merge `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`

## Selected source

- read-only Canary revision: `95b276db311cf6e9acd58b847f1fb0ca6697b137`;
- accepted W7 source cut: `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`;
- comparison from the accepted cut to the selected revision contains no `src/server/network/**`, protocol-game or login-session source change;
- server release: `3.6.1`;
- client/protocol version: `1525`;
- profile registry identifier: `current`.

Every exact statement below is limited to those revisions and cites a read-only source path.

## Exact source-owned facts

### Profile and initial behavior

Sources:

- `src/core.hpp`;
- `src/server/network/protocol/protocol_profile.hpp`;
- `src/server/network/protocol/protocol_profile.cpp`.

`ProtocolProfileId::Current` is enabled for client version `1525`, uses the `CipsoftVanilla` wire family and the OpenTibia RSA key family. Its initial game behavior is `CurrentGameSequence` with `ServerChallengeBeforeLogin` and `CurrentLoginChallenge`.

The Current game transport is source-defined as:

- outer length: modern XTEA block count;
- encrypted payload layout: one modern padding-count byte;
- inbound/outbound checksum: sequence value;
- encryption: XTEA after the RSA bootstrap key exchange;
- compression: official compression layout;
- high sequence bit: compression signal;
- length includes the four-byte sequence/checksum field;
- decoded body size: `raw_length * 8 + 4`, checked into `u16`.

### Bounds

Sources:

- `src/utils/const.hpp`;
- `src/server/network/message/networkmessage.hpp`.

Exact source limits:

- network message buffer: `65,500` bytes;
- client input message: `4,096` bytes;
- player/character name: `30` bytes;
- message length storage: `u16`;
- outbound header staging space: eight bytes.

These are Canary source limits, not general application budgets.

### Current game-login field order

Source: `src/server/network/protocol/protocolgame.cpp`, `ProtocolGame::onRecvFirstMessage`.

Observed source order for Current:

1. operating-system `u16`;
2. protocol version `u16`;
3. client version `u32`;
4. length-prefixed client version string;
5. length-prefixed asset-hash identifier;
6. preview-state `u8`;
7. RSA-decrypted bootstrap block;
8. four `u32` XTEA key words;
9. game-master flag `u8`;
10. length-prefixed session key;
11. length-prefixed character name;
12. challenge timestamp `u32`;
13. challenge random byte `u8`.

The source enables XTEA immediately after reading the four key words. A challenge mismatch disconnects without admission.

### One-shot session-key semantics

Sources:

- `src/security/login_session_manager.hpp`;
- `src/security/login_session_manager.cpp`;
- `src/server/network/protocol/protocolgame.cpp`.

The server issues a 256-bit random token encoded as wire-safe text, stores only its SHA-256 hash, binds it to one account, the allowed character-name set and the exact protocol profile, and applies a default 60-second TTL. A matching token is removed before its fields are inspected, so wrong character/profile use also burns it and concurrent redemption cannot succeed twice.

When session authentication fails, the game protocol sends the stable user-facing session-expired denial and closes the connection. This is sufficient to classify the combined server result as `CredentialExpiredOrConsumed`; the wire response does not prove which cause occurred.

### Admission success boundary

Source: `src/server/network/protocol/protocolgame.cpp`.

For Current login, source order includes:

1. login/self packet `0x17`;
2. allow-bug-report packet `0x1A`;
3. Tibia-time packet `0xEF`;
4. pending-state-entered packet `0x0A`;
5. enter-world packet `0x0F`;
6. map description afterwards.

`0x0F` after the ordered preceding prefix is the selected W7 technical `SessionEntered` marker. No map-description byte is part of W7 admission.

### Denial and close behavior

`ProtocolGame::disconnectClient` writes packet `0x14`, writes one length-prefixed message and then disconnects. Some malformed/bootstrap failures disconnect without a denial payload. Arbitrary backend denial text must not cross the Rust adapter boundary; only closed stable outcome categories are permitted.

## Synthetic fixture contract

All committed synthetic fixtures are original Oteryn test data. Their framing and tag values are deliberately unrelated to Canary wire bytes. They exist only to prove:

- bounded parsing;
- ordered admission-state handling;
- one-shot credential ownership;
- outcome mapping;
- malformed/truncated/oversized input rejection;
- deterministic no-panic behavior.

Synthetic success is not Canary compatibility evidence.

## BLOCKED real path

The production adapter remains disabled before network I/O and before credential handoff because the repository does not currently contain provenance-safe exact Current transcript fixtures or a named controlled Rust admission run proving the complete RSA/XTEA/sequence/compression path through `0x0F`.

Exact missing evidence:

1. a repository-policy-approved source for complete Current challenge/login/denial/success transcript bytes;
2. exact client-version string and asset-hash values used by the controlled target;
3. exact OpenTibia RSA public-key material and encoding provenance for this client implementation;
4. one configured fresh credential issued for the named test character/profile;
5. one controlled Rust run at named client, Canary, Platform and deployment revisions;
6. observed ordered decoded prefix through `0x0F` and clean close, with no secret bytes retained.

No bytes or constants may be inferred to fill these gaps.
