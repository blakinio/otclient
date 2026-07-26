# Gap and Decision Log

Evidence cut: 2026-07-27.

This document distinguishes accepted architecture decisions from implementation choices, cross-repository contracts and unresolved product/legal/runtime evidence. An `UNKNOWN` or `BLOCKED` item is not authorization to invent a value in code.

## Accepted architecture decisions

| ID | Decision | Status | Durable source | Implementation consequence |
|---|---|---|---|---|
| D-001 | Build a greenfield Rust client under `oteryn-client/` | `PROVEN` accepted | ADR-0001 | no linkage to legacy C++/Lua/OTUI runtime; legacy remains evidence/reference |
| D-002 | Use a data-oriented runtime with one logical simulation writer | `PROVEN` accepted | ADR-0002, `ARCHITECTURE.md` | no broad global `Mutex<GameState>`; bounded queues and extracted snapshots |
| D-003 | Use `wgpu` as the renderer abstraction | `PROVEN` accepted | ADR-0002 | exact crate version/backends/features remain implementation decisions |
| D-004 | Keep Canary and Oteryn wire formats behind independent adapters | `PROVEN` accepted | ADR-0003 | domain/features/UI cannot depend on concrete protocol crates |
| D-005 | Compile first-party modules as Rust crates | `PROVEN` accepted | ADR-0004 | no Lua/OTUI compatibility requirement |
| D-006 | Optional third-party extensions use capability-limited WebAssembly | `PROVEN` accepted | ADR-0004 | extension runtime is deferred until after playable core |
| D-007 | Gameplay channels are parallel world instances | `PROVEN` accepted | ADR-0005 | use typed `WorldChannelId`; never call them transport streams |
| D-008 | Channel changes occur through relog with a fresh game-entry transaction | `PROVEN` accepted | ADR-0005 | session-scoped state is destroyed; seamless transfer is out of scope |
| D-009 | Oteryn login uses system-browser Authorization Code + PKCE | `PROVEN` accepted | security/lifecycle architecture | main password is not collected or sent to game nodes |
| D-010 | Production assets and updates are signed/verified and atomically activated | `PROVEN` accepted | asset/security architecture | staging/cache is never runtime truth |
| D-011 | Windows is the first required production platform | `PROVEN` accepted | architecture and build policy | portability does not imply support for other platforms |
| D-012 | Foundation audit precedes product workspace/bootstrap implementation | `PROVEN` accepted | ADR-0001, audit plan | only the bounded WS-R01 package is authorized after audit acceptance |

## Decisions authorized by this audit

| ID | Decision | Evidence status | Scope |
|---|---|---|---|
| A-001 | The first implementation package is WS-R01 workspace/toolchain/architecture-policy bootstrap | `SUPPORTED` by all audit findings | repository/tooling only; no product runtime |
| A-002 | Initial Canary gameplay work should target one exact `ProtocolProfileId::Current` 15.25 revision | `SUPPORTED` | future WS-R06 task must select/revalidate exact commit/build/feature mask |
| A-003 | Legacy profiles are not part of the first Rust adapter | `PROVEN` non-goal | future independent packages only |
| A-004 | Synthetic assets, fixtures and replay scenes precede committed real game content | `PROVEN` safe sequence | no proprietary bytes while rights are unresolved |
| A-005 | Native channel-aware Oteryn admission is a separate cross-repository contract gate | `PROVEN` from current protocol-v1 limitation | it must not be inferred inside client code |
| A-006 | Initial reconnect behavior may return to selection unless an exact resume contract is selected | `INFERRED` safest MPS policy | final behavior requires WS-R06 evidence and product approval |
| A-007 | Product crates should be created only when their first observable slice starts | `PROVEN` governance requirement | no empty facade/module tree during WS-R01 |

## Cross-repository contract gaps

### G-001 — Stable identifier mapping

Required mapping:

```text
PlatformWorldId
ProductWorldChannelId
Canary login-list worldId
Canary ChannelContext channel_id
Canary issuer/process identity
```

- Status: `BLOCKED`.
- Evidence: current Gateway v1 states Platform `game_worlds.id` is not Canary `channel_id`; classic Canary world-list IDs represent channel entries.
- Owner: Oteryn Platform + Canary + WS-R03/WS-R06.
- Required output: versioned schema, uniqueness/lifetime rules, supported conversions and failure behavior.
- Code prohibition: do not use one primitive alias or positional equality for these IDs.

### G-002 — Channel-aware game-session issuance

- Status: `BLOCKED`.
- Current contract: one Platform world maps to one exact Canary issuer process.
- Needed: selected-channel binding, issuer routing, ticket scope, idempotency, unavailable-channel behavior and rollout matrix.
- Required proof: Channel 1 login, logout, Channel 2 fresh issue/login, replay rejection and no overlapping character session.

### G-003 — Directory schema

- Status: `UNKNOWN`.
- Needed client-facing fields: typed character/world/channel IDs, status, compatibility, population/queue/recommendation when supported, directory revision and expiry.
- Current evidence: Canary classic login world list exists; no proven native Platform schema covers the desired explicit model.
- Owner: Oteryn Platform + WS-R03.

### G-004 — Logout commitment and relog fencing

- Status: `BLOCKED` for the native channel flow.
- Needed: authoritative indication that the old game session ended or exact lease/fencing semantics before new-channel admission.
- Client rule: a network timeout is not proof that persistent logout committed.

### G-005 — Session resume

- Status: `UNKNOWN`.
- Needed: exact Canary/native protocol support, resume credential type, expiry, sequence/snapshot semantics and replay restrictions.
- Initial-ticket reuse remains forbidden regardless of the decision.

### G-006 — Queue/full/maintenance semantics

- Status: `SUPPORTED` server concepts exist in Canary multi-channel runtime, but `UNKNOWN` client-facing Oteryn schema.
- Needed: status taxonomy, queue token/expiry, alternative-channel recommendation and race behavior.

### G-007 — Native Oteryn game protocol

- Status: `BLOCKED` until a cross-repository ADR/contract exists.
- Open choices include transport, schema technology, snapshots/deltas, prioritization and resume.
- Client audit does not authorize QUIC, Protobuf or another specific technology.

## Canary adapter gaps

### G-010 — Exact selected revision

- Status: `UNKNOWN` until WS-R06 starts.
- Audit candidate: Current profile 15.25.
- Required: re-read live Canary main/open PRs, select exact commit and record build string/feature mask.

### G-011 — Minimum-playable wire corpus

- Status: `BLOCKED`.
- Missing: complete synthetic/provenance-documented fixtures for login, map, creatures, items, stats, commands, chat, ping/logout.
- Required: positive, bounded, truncated, malformed, wrong-gate and state-order cases.

### G-012 — Build-string-specific payloads

- Status: `PROVEN` risk.
- Current evidence: 15.25 weapon-proficiency payload has known build-prefix branches.
- Needed: build identity in compatibility metadata and fixtures; no “1525 means all 15.25” assumption.

### G-013 — Normalized domain contract

- Status: `UNKNOWN` implementation details.
- Architecture fixes direction but not final enum/type shapes.
- Owner: WS-R04 before/with first WS-R06 family; one active owner for shared events/commands.

### G-014 — Legacy profile roadmap

- Status: `REJECTED` for MPS; `UNKNOWN` future product demand.
- No implementation work until Current-profile MPS is stable and a separate need is approved.

## Asset and legal gaps

### G-020 — Redistribution rights

- Status: `BLOCKED`.
- Affected: sprites, appearance/type packages, sounds, fonts, logos, maps and extracted official assets.
- Technical availability is not legal authorization.
- Owner: product/legal + WS-R09.

### G-021 — Approved source/delivery model

- Status: `UNKNOWN`.
- Options requiring review: committed approved assets, signed install-time download, or user-local import of legally obtained inputs.
- The final model may differ by asset class.

### G-022 — Real asset statistics

- Status: `BLOCKED` by source/rights availability.
- Needed: counts, dimensions, frame/animation distributions, transparency, decoded/compressed sizes and mapping complexity.
- Blocks final texture layout/compression/cache budgets, not WS-R01.

### G-023 — Runtime pack format

- Status: `UNKNOWN` implementation decision.
- Requirements are fixed; exact binary format, compression and signing envelope are not.
- Owner: WS-R09 after a synthetic format spike and threat model.

### G-024 — Fonts/localization/audio

- Status: `UNKNOWN` product selection and `BLOCKED` rights for actual content.
- Owner: product/branding/localization + WS-R09/WS-R10/WS-R12.

## Performance and hardware gaps

### G-030 — Legacy numeric baseline

- Status: `BLOCKED`.
- Needed environment: runnable Windows build, legal assets, controlled Canary/replay, frame-time capture and named hardware.
- Existing design estimates are not data.

### G-031 — Minimum/recommended/high-refresh machines

- Status: `BLOCKED` until P1–P8 scenes and asset memory evidence exist.
- Product owner selects supported tiers from measured candidates.

### G-032 — GPU CI

- Status: `UNKNOWN`.
- Required: reliable runner policy, backend/driver visibility and separation from physical hardware acceptance.

### G-033 — Final frame/memory budgets

- Status: `SUPPORTED` provisional architecture budgets exist; final numbers `UNKNOWN`.
- Any change requires measured evidence and architecture review.

## Dependency and platform gaps

### G-040 — Rust toolchain version

- Status: `UNKNOWN`; WS-R01 selects current stable/pinned version from primary Rust documentation and CI availability.

### G-041 — Exact `wgpu` version/backend policy

- Status: `UNKNOWN`; `wgpu` abstraction is accepted, but package version, feature flags and D3D12/Vulkan policy require a Windows spike.

### G-042 — Window, async, HTTP/TLS, text, audio and WASM libraries

- Status: `UNKNOWN`.
- Each owning workstream selects only after current primary-source review, license/unsafe/maintenance analysis and narrow behavior spike.
- WS-R01 must not pre-add them.

### G-043 — Minimum Windows release

- Status: `UNKNOWN`.
- Inputs: dependency support, target users, driver/GPU baseline, installer policy and test-machine availability.

## Product/UI gaps

### G-050 — Branding and original visual system

- Status: `UNKNOWN` final assets, typography and accessibility acceptance.
- Architecture/UI primitives may proceed with synthetic/original placeholders.

### G-051 — Localization set

- Status: `UNKNOWN`.
- UI core must support expansion/shaping independently of selected launch languages.

### G-052 — Cross-channel social behavior

- Status: `UNKNOWN` for private chat, party presence, guild/VIP visibility and invites in the native Oteryn product.
- These are Beta/Later contracts and do not block MPS local gameplay.

### G-053 — Commercial/advanced features

- Status: `UNKNOWN` product priority and exact server contracts for store, market extensions, Taskboard, Wheel, Forge and other modern systems.
- Explicitly outside first vertical slice.

## Implementation sequencing constraints

1. Merge/accept this audit.
2. Complete WS-R01 bootstrap without product dependencies or empty product crates.
3. Establish deterministic foundation types/test support and synthetic asset/render/domain slices through separate packages.
4. Resolve exact Canary revision/corpus before protocol implementation.
5. Resolve real asset rights before any production compatibility pack.
6. Resolve channel-aware native admission before claiming Oteryn-native multi-channel login.
7. Measure P-scenes before selecting hardware tiers or making performance claims.

## Decisions explicitly rejected by the audit

- One-to-one port of legacy modules/classes/globals.
- One universal numeric world/channel identifier.
- Automatic fallback from Oteryn Identity to main-password game login.
- Reuse of the initial one-shot credential for reconnect or another channel.
- Full legacy protocol support in the first adapter.
- Committing technically obtainable game assets without rights evidence.
- Freezing texture/cache/hardware parameters without measurements.
- Selecting native Oteryn transport/schema in a client-only task.
- Adding broad application dependencies during the workspace bootstrap.
