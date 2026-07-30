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
| `OTS-20260721-oteryn-identity-auth` | Platform/Gateway protocol v1 and Canary Game Session contract | maintained legacy OTClient PR #17 | OAuth+PKCE -> ticket -> `/v1/login` -> GameSessionKey | bounded legacy consumer path; no Rust proof | legacy consumer `bb87346f6c516a19d19497d82bb01fb389334ff5` |
| `OTS-20260730-rust-technical-login` | Platform/Gateway `8e613c00503c0874e69e2085c740f87f4a87e002`; Canary `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f` | planned Rust wave `OTERYN-W7-TECHNICAL-LOGIN` | one exact issuer/world, one selected character, one-shot Current-profile admission through `0x0F` | plan accepted only after plan/archive merge; real Identity callback blocked | 2026-07-30 source cut |

## `OTS-20260730-rust-technical-login` exact evidence

### Platform native OAuth

At `blakinio/Oteryn-Platform@8e613c00503c0874e69e2085c740f87f4a87e002`:

- public Authorization Code client; no embedded client secret;
- PKCE `S256` is required;
- native redirect is required to be exactly `http://127.0.0.1/callback` and any explicit port/query/fragment/user/pass is rejected;
- access token must include `game:ticket`;
- after one Game Login Ticket is issued, the access token and associated refresh token are revoked;
- no reusable account-session/channel-switch claim follows from this producer behavior.

Conflict `W7-BLOCK-IDENTITY-REDIRECT`: `oteryn-client/docs/architecture/SECURITY_MODEL.md` requires an OS-assigned loopback port. The Rust consumer must not bind fixed port 80, weaken the invariant or invent dynamic redirect registration. Real callback integration remains blocked until exact producer or accepted architecture evidence reconciles this.

### Gateway protocol v1

At the same Platform revision:

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
- routing uses only server-authoritative world host/port;
- there is no server directory revision, gameplay-channel ID, general issuer directory or multi-world issuer selection contract;
- Platform `game_worlds.id` is not Canary channel ID.

### Gateway -> Canary Game Session

The authoritative contract is `Oteryn-Platform/docs/contracts/GAME_SESSION_CANARY_CONTRACT.md`:

- one configured Platform world maps to one exact Canary issuer process;
- Current profile only;
- opaque short-lived one-shot credential, process-local store, current TTL 60 seconds;
- wrong character/profile consumption burns according to manager semantics;
- duplicate issuance for one login-attempt ID is rejected within the bounded TTL;
- no process replicas/shared store/multi-world routing/security-generation immediate revocation claim;
- repository tests do not prove deployed TLS, firewall, secret manager or exact runtime revisions.

### Canary Current admission

At `blakinio/canary@4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`:

- release `3.6.1`, Current client protocol `1525`;
- OpenTibia RSA; server challenge before login;
- modern block-count framing/padding, sequence checksum after login and official compression signaling;
- login layout includes OS/protocol/client version, version string, asset hash, preview state, XTEA/session/character/challenge fields;
- one-shot session token is consumed against selected character and Current profile;
- successful world placement writes login `0x17`, pending-state `0x0A` and enter-world `0x0F` before map description;
- the W7 technical milestone may emit `SessionEntered` after validating the ordered prefix through `0x0F` and must stop before map decoding.

### Proof boundary

Canary PR #815 records a hardened physical E2E for the maintained legacy OTClient at exact older revisions. It is reference evidence that the architecture can work; it is not Rust compatibility evidence. W7 must provide its own named exact real admission or retain `W7-BLOCK-REAL-RUST-E2E`.

## Failure/rollout rules

- affected real adapters remain blocked while unaffected deterministic/fake lanes may proceed;
- no speculative production API, password fallback, credential replay or security downgrade;
- no credentials, private captures or proprietary assets in Git;
- one-sided unsupported combinations fail closed;
- rollout values remain `server-first-safe`, `client-first-safe`, `backward-compatible`, `atomic-required`, `breaking-migration` or `unverified`.
