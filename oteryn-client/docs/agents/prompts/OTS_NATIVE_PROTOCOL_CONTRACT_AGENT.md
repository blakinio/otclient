# Prompt: three-repository native gameplay protocol contract

## Role and task

You are the sole cross-repository contract coordinator for the future native Oteryn gameplay protocol and automatic adapter selection.

Authorized repositories for this task:

- `blakinio/Oteryn-Platform`;
- `blakinio/Otheryn`;
- `blakinio/otclient`.

Coordination ID:

`OTS-20260804-native-protocol-selection`

Task mode:

`CONTRACT / ARCHITECTURE ONLY`

Your responsibility is to produce an exact, implementable and security-reviewed producer/consumer contract spanning Oteryn Identity, Game Login Ticket, Game Gateway, World Registry, Game Session, Otheryn and the Rust client.

Do not implement runtime behavior, native packets or Tokio in this task. Continue autonomously through contract discovery, linked repository task/PR creation, consistency validation, review, merge and archival.

## Repository discipline

Use one dedicated task, branch and PR per repository. Do not share branches or task records across repositories.

Before every write, verify the repository is exactly one of the three authorized repositories.

Read and obey each repository's complete governing instructions before mutation, including root/nested `AGENTS.md`, overrides, task governance, cross-repository rules and active ownership.

Inspect live current heads, active tasks, open PRs, branches, contracts and shared-path leases. Do not rely on this prompt for current revisions.

No external or upstream repository is writable in this task.

## Mandatory source material

At minimum inspect the current exact versions of:

### Oteryn Platform

- ADR 0009 game authentication architecture;
- `OTCLIENT_GAME_AUTH_CONTRACT.md`;
- `GAME_GATEWAY_IDENTITY_CONTRACT.md`;
- `GAME_SESSION_CANARY_CONTRACT.md`;
- `WORLD_REGISTRY_CONTRACT.md`;
- Game Gateway public `/v1/login` request/response implementation;
- ticket issue/redeem implementation and tests;
- Gateway login-context and Game Session issuer implementation;
- staging/deployment contracts relevant to service identity and private ingress.

### Otheryn

- current Game Session issuer/consumer and login admission implementation;
- current Canary-compatible protocol profiles and session binding;
- ASIO connection/service architecture;
- player action handlers for movement, combat, spells, items and loot;
- current limits, framing, encryption/compression and authentication boundaries;
- active tasks and compatibility contracts.

### Rust client

- `oteryn-client/AGENTS.md`;
- ADR-001;
- `PROTOCOL_BOUNDARY.md`;
- `PLATFORM_GATEWAY_GAME_ENTRY.md`;
- `DUAL_PROTOCOL_EXECUTION_PLAN.md`;
- `docs/agents/CROSS_REPO_CONTRACTS.md`;
- current `game-domain`, `protocol-core`, `protocol-canary`, transport and game-session APIs;
- active P2 protocol work and exact public contracts.

## Proven baseline to preserve

The existing native game-entry flow is:

```text
Rust client
-> system browser
-> Oteryn Identity OAuth Authorization Code + PKCE
-> short-lived game:ticket bootstrap
-> one-time opaque Game Login Ticket
-> Oteryn Game Gateway
-> private atomic ticket redeem
-> authoritative character/world context and World Registry routing
-> Game Session issuance
-> Otheryn game server
```

The task must reuse this chain.

Do not create:

- another login server;
- another Identity authority;
- a second ticket system;
- client-side Oteryn password authentication;
- direct OAuth-token authentication to Otheryn;
- direct Game Login Ticket consumption by Otheryn;
- a bypass around Game Gateway.

## Critical naming distinction

The existing Gateway JSON `protocol_version: 1` is the Gateway login API version. It is not a gameplay protocol profile.

The contract must define distinct concepts and serialized fields for:

- Gateway API version;
- Game Session contract version;
- gameplay adapter family;
- gameplay profile/version;
- transport/framing requirements;
- gameplay capabilities;
- client build or compatibility metadata.

Do not overload one numeric version for multiple meanings.

## Required contract decisions

Resolve each item from exact source evidence and record decisions, alternatives and rejected options.

### 1. Candidate negotiation shape

Select exactly one initial mechanism:

- client sends a bounded supported-candidate offer and Gateway selects one;
- Gateway returns a bounded authoritative candidate set and client selects one;
- a dedicated bounded pre-game negotiation selects one.

The choice must account for ticket consumption, ambiguous failures, downgrade resistance, server-first rollout and current Gateway behavior.

### 2. Authoritative ownership

Define which component owns:

- configured adapter families/profiles per world/channel;
- capability metadata;
- supported transport/framing requirements;
- final selection decision;
- validation of the client's selected profile;
- binding of the selected profile to Game Session authorization;
- rollout enable/disable flags;
- compatibility matrix publication.

No ownership may be implied or duplicated.

### 3. Session binding

Define exact binding among:

- login attempt identifier;
- redeemed ticket;
- Identity/account binding;
- selected character;
- world/channel;
- Game Session credential;
- selected gameplay adapter family/profile;
- negotiated capabilities;
- expiry and revocation generation.

Prove that a credential cannot be replayed for a different character, world or gameplay profile.

### 4. Framing and schema

Define:

- transport protocol;
- connection bootstrap;
- frame boundaries;
- integrity/checksum rules;
- encryption/TLS boundary;
- optional compression and decompression limits;
- schema/serialization technology;
- field compatibility rules;
- unknown-field/message behavior;
- maximum frame, message, string, collection and nesting sizes;
- exact failure classification.

Do not copy Canary framing merely for familiarity. Do not invent bytes without Otheryn producer agreement.

### 5. Versioning and capabilities

Define:

- adapter family identifier;
- initial native protocol version/profile identifier;
- capability vocabulary and stability rules;
- backward/forward compatibility behavior;
- supported and unsupported client/Platform/Gateway/Otheryn combinations;
- version deprecation and minimum-supported policy;
- contradictory advertisement handling.

### 6. Action sequencing and results

Define protocol-neutral mapping for at least:

- movement and stop;
- attack/follow target selection;
- spells;
- item use and use-with;
- item movement;
- quick loot/corpse loot;
- chat;
- logout.

Decide exact semantics for:

- client action identifier;
- client sequence;
- server authoritative ordering/tick where provided;
- accepted;
- rejected with stable reason;
- delayed;
- effect observed;
- completion;
- expiry/cancellation;
- reconnect/session replacement.

The client sends intent only. Otheryn owns legality and every result.

### 7. State synchronization

Define:

- initial snapshot boundaries;
- incremental delta/revision behavior;
- ordering and duplicate policy;
- lost baseline/recovery behavior;
- movement prediction reconciliation;
- inventory/container authority;
- combat/resource/cooldown authority;
- reconnect/resume policy.

No client-authoritative inventory, loot, damage or resource mutation is allowed.

### 8. Security and downgrade resistance

Define and test:

- no password fallback;
- no adapter switch after ticket consumption, Game Session issuance, credential handoff or partial admission;
- unsupported pair failure before gameplay;
- stale directory/candidate behavior;
- candidate tampering and contradiction;
- replay and cross-world/profile misuse;
- logs and telemetry redaction;
- rate/size/decompression abuse limits;
- service identity and private API boundaries;
- safe ambiguous-failure behavior.

### 9. Rollout and rollback

Define exact staged order across all three repositories.

Default direction should be evaluated against:

```text
contract first
-> Platform/Gateway producer extension disabled by default
-> Otheryn producer/validator disabled by default
-> Rust adapter and selection support
-> exact integrated staging proof
-> bounded enablement
-> legacy Canary compatibility retained
```

State whether every step is `server-first-safe`, `client-first-safe`, `backward-compatible`, `atomic-required`, `breaking-migration` or `unverified`.

Do not remove legacy paths or activate production.

## Required deliverables

Create linked durable records in all three repositories.

At minimum deliver:

- one canonical cross-repository contract with an explicit source-of-truth repository;
- correspondence documents or registry entries in the other two repositories;
- an ADR or accepted amendment where stable architecture changes;
- exact producer/consumer responsibility table;
- exact schemas or schema IDL for review, without runtime wiring;
- message and error vocabulary;
- compatibility matrix;
- rollout/rollback plan;
- threat model/downgrade analysis;
- deterministic contract-test plan and golden fixture ownership;
- dependency graph for later implementation packages;
- separate ready-to-run implementation prompts for:
  1. Platform/Game Gateway producer extension;
  2. Otheryn native producer/session enforcement;
  3. Rust `protocol-oteryn` adapter;
  4. automatic selection and integrated E2E.

Do not place all three repositories' task state in one file. Link them with the shared coordination ID and exact PRs/revisions.

## Validation

For every repository:

- validate document links and referenced paths;
- inspect full changed-file list and diff;
- run repository-required documentation/governance validation;
- run exact-head CI required for documentation changes;
- perform an independent security and consistency review;
- prove there are no conflicting active owners or unresolved review threads.

Cross-repository review must check that identical terms have identical meanings and that no repository claims another repository's unimplemented behavior.

## Non-goals

Do not:

- add Tokio or Rust dependencies;
- create the `protocol-oteryn` crate;
- modify Otheryn runtime/network handlers;
- modify Game Gateway endpoints at runtime;
- add database migrations;
- change ticket/session behavior;
- invent or commit production endpoints/secrets;
- deploy anything;
- remove Canary support;
- claim production compatibility.

## Completion rule

Completion requires:

- all required decisions are explicit and no material field remains ambiguous;
- the three repositories contain linked consistent durable contracts;
- exact current-versus-target implementation status is truthful;
- later package ownership and ordering are unambiguous;
- documentation/governance CI passes on exact heads;
- independent review has zero open material findings;
- all contract PRs merge in a safe documented order;
- tasks archive and shared leases release.

If exact source evidence makes a decision impossible, do not invent it. Record the bounded unresolved item, identify the specific producer experiment or measurement needed, and complete every other decision that is not blocked.
