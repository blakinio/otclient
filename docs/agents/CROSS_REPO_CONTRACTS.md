# Canary ↔ OTClient Contract Registry

Last reviewed: 2026-07-30

Copy durable contract changes to producer and consumer repositories through separate authorized tasks. External repositories are read-only during OTClient coordination. Task-specific evidence belongs in task records/research documents.

## Required fields

- shared coordination ID and linked producer/consumer tasks;
- producer and consumer repository plus exact revisions;
- endpoint/opcode/message/config/identifier/path;
- field order, widths, signedness and optional values;
- capability/version gate;
- supported/unsupported combinations;
- rollout order and one-sided failure behavior;
- tests/evidence on both sides;
- linked PRs and last verified commit pair.

## Durable areas

| Area | Producer source | Consumer source | Rule |
|---|---|---|---|
| Protocol/opcodes | Canary protocol handlers/profiles | Rust `transport`/`protocol-*` or legacy client | Never reuse/infer an opcode without exact revision/layout evidence. |
| Identity/Gateway | Oteryn Platform OAuth/ticket/Gateway | Rust `platform`/`identity` or legacy enter-game | Redirect, PKCE, JSON, caching, routing and one-shot behavior remain exact and fail closed. |
| Identifiers | Platform/Gateway schemas | account-session/world-directory/game-session | Preserve widths/meaning; local generations are not producer IDs. |
| Assets/IDs/paths | datapack/distribution definitions | things/sounds/assets/loaders | Definitions/references differ; IDs/paths cannot be silently repurposed. |
| Feature payloads | Canary game logic/emission | matching consumer | Field order, optionals and gates match exactly. |
| Coupled defaults | producer config/schema/migrations | client config/setup | Defaults do not silently diverge or become production claims. |

## Compatibility matrix

| Coordination ID | Producer evidence | Consumer evidence | Contract | Status | Last verified |
|---|---|---|---|---|---|
| `OTS-20260714-protocol-session-lifecycle` | `blakinio/canary#245` physical two-session consumer proof | `blakinio/otclient#9` (supersedes #7) | unchanged legacy session lifecycle | historical legacy record | PRs #9/#245 |
| `OTS-20260721-oteryn-identity-auth` | Platform OAuth/ticket/Gateway plus Canary Game Session producer | maintained legacy OTClient PR #17 | OAuth+PKCE -> ticket -> `/v1/login` -> `GameSessionKey` | bounded legacy consumer path; no Rust proof | legacy consumer merge `bb87346f6c516a19d19497d82bb01fb389334ff5` |
| `OTS-20260730-rust-technical-login` | Platform/Gateway `8e613c00503c0874e69e2085c740f87f4a87e002`; Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f` | planned Rust wave `OTERYN-W7-TECHNICAL-LOGIN` | one exact issuer/world, one selected character, one-shot Current-profile admission through `0x0F` | plan launchable only after plan/archive merge; real Rust path unproven | 2026-07-30 planning cut |

## `OTS-20260730-rust-technical-login` exact evidence

### Platform native OAuth

Producer chain:

- native OAuth PR #119, merge `27fa277c5def0e151d7ee013acef188dbfd6f463`;
- Game Login Ticket PR #121, merge `cab00c140ce200e3cd51b7eafe2c1659842c2b90`;
- Gateway PR #122, merge `8006534108d835474dadd208b0ec934e4a12528b`;
- current hardening evidence includes merge `53158217a6c6017230301cf4daa783b04fcc13d5`.

At the planning source cut:

- public Authorization Code client; no embedded client secret;
- PKCE `S256` is required;
- registered redirect base is exactly `http://127.0.0.1/callback` with no fixed port;
- current `NativeOAuthPkceTest::test_dynamic_loopback_port_authorization_and_pkce_s256_token_exchange_succeed_without_client_secret` proves authorization and token exchange with an otherwise matching dynamic loopback port such as `http://127.0.0.1:49152/callback`;
- wrong callback path and non-loopback redirects are rejected;
- Rust must bind `127.0.0.1:0`, use the actual assigned port in authorization and token exchange, validate exact state/path/peer and never bind fixed port 80;
- access token must include `game:ticket`;
- after one Game Login Ticket is issued, the access token and associated refresh token are revoked;
- no reusable account-session/channel-switch claim follows from this producer behavior.

The no-port registered base and dynamic request port are an intentional producer behavior proven by source tests, not a compatibility conflict. Every implementation worker must still revalidate it at the exact current producer revision.

### Gateway protocol v1

```text
POST /v1/login
request:  { protocol_version: 1, game_login_ticket: string }
response: {
  protocol_version: 1,
  session: { credential: opaque string, expires_at: timestamp },
  worlds: [{ id: i64, slug, name, region, host, port }],
  characters: [{ id: i64, name, level, vocation, world_id: i64 }]
}
```

Rules:

- bounded request body, no query, unknown fields/trailing JSON rejected;
- public failures are `invalid_request`, `invalid_login`, `login_unavailable`;
- sensitive responses are no-store/no-cache;
- routing uses only validated server-authoritative world host/port;
- duplicate/invalid IDs, invalid ports and character/world mismatches fail closed in the consumer;
- there is no server directory revision, gameplay-channel ID, general issuer directory or multi-world issuer selection contract;
- Platform `world_id` is not a Canary gameplay-channel ID.

### Gateway -> Canary Game Session

Authoritative producer evidence:

- Canary Game Session PR #722, merge `b8a88f073b2609b444fa15370aae30ac9f80b908`;
- rotation PR #807, merge `981c82f5ebb6bc22c867312c2b274a71f6aeeb3e`;
- Oteryn Platform `docs/contracts/GAME_SESSION_CANARY_CONTRACT.md` at the selected evidence cut.

Contract:

- one configured Platform world maps to one exact Canary issuer process;
- Current profile only for protocol v1;
- opaque short-lived one-shot credential, process-local hashed store, current TTL 60 seconds;
- wrong character/profile may consume/burn the matching credential;
- process restart invalidates outstanding credentials;
- duplicate issuance for one login-attempt ID is rejected within the bounded TTL;
- no process replicas/shared store/multi-world routing/security-generation immediate-revocation claim;
- repository tests do not prove deployed TLS, firewall, secret manager or exact runtime revisions.

### Canary Current admission

At `blakinio/canary@4b2d6f432d92628c42bde1d95daed6ae0d0eb88f` planning cut:

- release `3.6.1`, Current client protocol `1525`;
- OpenTibia RSA and server challenge before login;
- modern block-count framing/padding, sequence checksum after login and compression signaling;
- login layout includes OS/protocol/client version, version string, asset hash, preview state, XTEA/session/character/challenge fields;
- opaque session token is consumed against selected character and Current profile;
- successful world placement writes self-login `0x17`, pending-state `0x0A` and enter-world `0x0F` before map description;
- W7 may emit `SessionEntered` only after validating the ordered prefix through `0x0F`, then stop before map decoding and disconnect cleanly.

### Proof boundary

Legacy OTClient evidence proves only the maintained legacy consumer at its named revisions. It is reference evidence that the external architecture can work; it is not Rust compatibility evidence. W7 must provide its own named exact real admission or retain `W7-BLOCK-REAL-RUST-E2E`.

## Failure and rollout rules

- missing real/deployment evidence blocks only the affected claim while deterministic/fake work may proceed;
- no speculative production API, password fallback, credential replay or security downgrade;
- no credentials, private captures or proprietary assets in Git;
- protocol/capture work is internal Oteryn/Canary compatibility evidence and is not published as third-party gameplay manipulation or anti-cheat tooling;
- one-sided unsupported combinations fail closed;
- rollout values remain `server-first-safe`, `client-first-safe`, `backward-compatible`, `atomic-required`, `breaking-migration` or `unverified`.
