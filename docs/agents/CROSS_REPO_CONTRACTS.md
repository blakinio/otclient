# Canary ↔ OTClient Contract Registry

Last reviewed: 2026-07-14

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

Rollout values: `server-first-safe`, `client-first-safe`, `backward-compatible`, `atomic-required`, `breaking-migration`, `unverified`.
