# Canary ↔ OTClient Contract Registry

Last reviewed: 2026-07-22

Copy durable contract changes to both repositories. Task-specific details belong in task records.

## Required fields

- shared `OTS-*` ID and linked `CAN-*`/`OTC-*` tasks;
- producer and consumer;
- opcode/message/protobuf/feature/config/identifier/path;
- old/new behavior;
- field order, widths, signedness, optional values;
- capability/version gate;
- supported/unsupported combinations;
- rollout order and one-sided failure behavior;
- tests on both sides;
- linked PRs and last verified commit pair.

## Durable areas

| Area | Canary source | OTClient source | Rule |
|---|---|---|---|
| Protocol/opcodes | server protocol handlers/definitions | `src/client` and affected modules | Never reuse opcode without checking both sides/versions. |
| Protobuf | `src/protobuf`/serialization | `src/protobuf`/deserialization | Schemas/generated expectations stay synchronized. |
| Feature flags | server capability/version behavior | `modules/game_features` and C++ checks | Gate new behavior while old combinations remain supported. |
| Assets/IDs/paths | datapack/distribution definitions | things/sounds/assets/loaders | Definitions/references differ; IDs/paths cannot be silently repurposed. |
| Login/auth | login service/config/protocol | enter-game/server-list/login modules | Defaults, TLS, fallback, failure behavior explicit. |
| Feature payloads | game logic/emission | matching `modules/game_*` consumer | Field order, optionals, gates match exactly. |
| Coupled defaults | server config/schema/migrations | client config/setup/module defaults | Defaults do not silently diverge. |

## Compatibility matrix

| Coordination ID | Canary PR/commit | OTClient PR/commit | Protocol | Rollout | Status | Last verified |
|---|---|---|---:|---|---|---|
| `OTS-20260714-protocol-session-lifecycle` | `blakinio/canary#245` physical two-session consumer proof | `blakinio/otclient#9` (supersedes merged #7) | unchanged | client-first-safe | OTClient implementation pending final CI/merge; Canary E2E must consume final squash SHA | OTClient PR #9 / Canary PR #245 |
| `OTS-20260721-oteryn-identity-auth` | production Game Session adapter pending separate Canary phase; current compatibility contract is `Oteryn-Platform/docs/contracts/GAME_SESSION_CANARY_CONTRACT.md` | `blakinio/otclient#17` | game-auth v1; existing `GameSessionKey` world-entry field | Platform/Gateway-first; client disabled by default; production cutover blocked on Canary adapter + cross-repo E2E | OTClient Phase 5 in progress; Platform OAuth/ticket/Gateway producers merged; no password fallback in Oteryn profile | Platform Gateway merge `8006534108d835474dadd208b0ec934e4a12528b`; OTClient PR #17 |

### `OTS-20260721-oteryn-identity-auth` contract notes

- Producer path: Oteryn Platform Identity Authorization Code + PKCE -> Platform Game Login Ticket -> standalone Game Gateway `/v1/login`.
- OTClient consumes Gateway protocol v1 and accepts only server-authoritative `world_id` -> host/port routing.
- Gateway Game Session credential is passed through OTClient's existing `GameSessionKey` game-login field with the selected character name; Oteryn account/password/authenticator fields are empty.
- Client clears the Game Session credential after the first normal world-login handoff and refuses automatic replay/reconnect.
- Exact production Canary acceptance/storage/revocation semantics are not claimed until a separate adapter task closes the Phase 6 contract and exact-version E2E is green.
- Unsupported one-sided combinations fail closed: native auth is disabled by default and an Oteryn profile never silently falls back to password auth.

Rollout values: `server-first-safe`, `client-first-safe`, `backward-compatible`, `atomic-required`, `breaking-migration`, `unverified`.
