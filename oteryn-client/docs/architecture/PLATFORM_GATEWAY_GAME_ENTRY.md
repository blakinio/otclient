# Oteryn Platform, Game Gateway and gameplay protocol selection

Coordination ID: `OTS-20260804-native-protocol-selection`  
Related decision: [ADR-001](decisions/ADR-001-dual-protocol-selection-and-async-transport.md)  
Execution plan: [Dual Protocol and Tokio Execution Plan](DUAL_PROTOCOL_EXECUTION_PLAN.md)

## Status

This document is an accepted responsibility and sequencing boundary.

The existing native-auth chain is already implemented and proven in bounded Platform/Gateway/Canary revisions, but native `protocol-oteryn` advertisement and selection are not implemented yet.

Do not interpret this document as proof that the current Gateway response contains native gameplay protocol candidates.

## The component is not a single login server

The Oteryn game-entry path is a chain of separately owned components:

```text
Rust client
  -> operating-system browser
  -> Oteryn Identity / OAuth Authorization Code + PKCE
  -> short-lived OAuth bootstrap credential with game:ticket scope
  -> one-time opaque Game Login Ticket
  -> Oteryn Game Gateway
  -> private atomic ticket redeem and authoritative login context
  -> World Registry route and Game Session issuance
  -> Otheryn game server
  -> selected gameplay protocol adapter
```

Future agents must use the established names:

- **Oteryn Identity** — the reusable credential and security-policy authority inside `blakinio/Oteryn-Platform`;
- **Game Login Ticket API** — the Platform public issue and private redeem boundary;
- **Oteryn Game Gateway** — the separately deployable Go login-orchestration runtime in `blakinio/Oteryn-Platform`;
- **World Registry** — the Platform-owned authoritative world routing source;
- **Game Session** — the short-lived world-entry authorization created through Gateway orchestration;
- **Otheryn game server** — the authoritative gameplay runtime in `blakinio/Otheryn`;
- **`protocol-canary` / `protocol-oteryn`** — Rust-client gameplay wire adapters, not login servers.

Do not introduce another client-owned login server, a second Identity authority or a parallel ticket system.

## Current delivered baseline

The already delivered Platform architecture establishes:

- system-browser sign-in;
- OAuth Authorization Code with PKCE S256 for a public native client;
- no confidential client secret in the game client;
- `game:ticket` bootstrap scope;
- one-time opaque Game Login Ticket issuance;
- private service-authenticated atomic ticket redeem;
- Platform-owned World Registry;
- separately deployable Go Game Gateway;
- Game Session issuance abstraction and a proven Canary-compatible producer path;
- server-authoritative character ownership and world routing.

The Rust client must reuse these contracts. It must not ask for, store or send the user's Oteryn password in the native Oteryn flow.

## Stable responsibility split

### Oteryn Identity and Platform

Own:

- reusable credentials;
- browser authentication, MFA, recovery and security policy;
- OAuth client registration and Authorization Code + PKCE behavior;
- Identity-to-game-account binding;
- Game Login Ticket issue, expiry, generation revocation and atomic consume state;
- World Registry data and account-authorized login context;
- public and private game-auth API versioning.

Do not own gameplay opcodes, combat state or client rendering.

### Oteryn Game Gateway

Own:

- accepting the one-time ticket from the client;
- redeeming it against the private Platform API;
- retrieving the minimum authoritative character/world login context;
- resolving World Registry routing;
- orchestrating Game Session creation;
- returning a bounded public login response;
- in the future, producing or relaying authoritative gameplay protocol candidates under the coordinated contract.

Gateway must never infer account or character ownership from client-supplied IDs.

### Otheryn game server

Own:

- validating and consuming the Game Session contract;
- accepting only an allowed gameplay adapter/profile for that session;
- all gameplay legality, state mutation, ordering and results;
- native Oteryn gameplay protocol production after its producer package exists;
- continued Canary compatibility where configured.

Otheryn retains asynchronous ASIO networking unless a separate profiling-backed ADR changes it.

### Rust client

Own:

- loopback callback and PKCE attempt lifecycle;
- transient OAuth bootstrap, ticket and Game Session credential handling;
- Gateway request and bounded response validation;
- character/world presentation and selection from authoritative data;
- local supported gameplay adapter/profile set;
- selection according to the accepted contract;
- exactly one adapter bound to one game-entry attempt/session;
- protocol-neutral Tokio transport, cancellation and backpressure;
- semantic player intent and non-authoritative presentation.

The client does not own reusable Oteryn credentials, account ownership, world routes or gameplay results.

## API version is not gameplay protocol selection

The existing Gateway JSON field:

```text
protocol_version: 1
```

identifies the **Gateway login API contract version**.

It does not by itself mean:

- Canary Current protocol;
- native Oteryn protocol v1;
- client version 1;
- a gameplay opcode family;
- a negotiated transport codec.

The current `client.version` presentation field also must not be treated as an authoritative gameplay adapter choice without a new accepted contract.

Use distinct names and types for:

```text
GatewayApiVersion
GameSessionContractVersion
GameplayAdapterFamily
GameplayProfileOrVersion
GameplayCapabilities
```

Never reuse one numeric field for more than one of these meanings.

## Future protocol-candidate production

Before automatic gameplay protocol selection can be implemented, the three-repository contract must define how the authoritative candidate set is produced and bound.

The contract must decide, with exact schema and tests, whether:

1. the client sends a bounded supported-candidate offer and Gateway selects one; or
2. Gateway returns a bounded authoritative candidate set and the client selects one; or
3. a dedicated bounded pre-game negotiation completes the selection.

Regardless of the selected mechanism, these invariants are mandatory:

- candidate data originates from authoritative Platform/Gateway/Otheryn configuration, never local user input alone;
- exact adapter family, profile/version, transport requirements and capability set are explicit;
- the selected profile is accepted and bound to the Game Session before gameplay messages are processed;
- the selected world/character/session cannot be reused for a different profile unless the contract explicitly authorizes it;
- no adapter switch occurs after ticket consumption, Game Session creation, credential handoff, partial admission or protocol failure;
- no error path falls back to Oteryn password authentication;
- unsupported or contradictory data fails closed before gameplay;
- reconnect/relog obtains fresh authoritative data and a fresh credential.

## Current implementation truth

At the current documented baseline:

- Platform native OAuth, ticket issue/redeem and Gateway login orchestration exist;
- Gateway protocol v1 returns Game Session material, worlds and characters;
- the current contract has a proven Canary Current game-entry path;
- `protocol-canary` is being implemented independently in the Rust client;
- the Rust transport is still the current synchronous worker implementation until Package A merges;
- Gateway does not yet have a source-proven native Oteryn gameplay candidate advertisement contract;
- `protocol-oteryn` does not yet exist;
- automatic adapter selection does not yet exist.

Agents must preserve this current-versus-target distinction.

## Required repository participation

Native gameplay protocol selection is a three-repository programme:

| Repository | Required role |
|---|---|
| `blakinio/Oteryn-Platform` | Identity, ticket, World Registry, Gateway login response and authoritative protocol-candidate/session-binding contract |
| `blakinio/Otheryn` | Game Session consumer and gameplay protocol producer/validator |
| `blakinio/otclient` | OAuth/Gateway consumer, selection policy, Tokio transport and independent protocol adapters |

A two-repository `otclient` + `Otheryn` design is incomplete because it omits the existing authoritative game-entry and routing layer.

## Rollout sequence

```text
A. protocol-neutral Tokio transport in otclient
B. exact three-repository native protocol and selection contract
C. Platform/Game Gateway capability and session-binding producer
D. Otheryn native gameplay producer and Game Session enforcement
E. Rust protocol-oteryn adapter
F. automatic selection integration and downgrade-negative E2E
G. semantic action lifecycle expansion
```

Package A and Package B may start now as separate non-overlapping tasks.

Packages C through G must not claim readiness before their named dependencies are accepted and merged.

## Explicit non-goals

This architecture does not authorize:

- another login server inside the Rust client;
- replacing Oteryn Identity with client password handling;
- bypassing Game Gateway for native Oteryn login;
- sending OAuth tokens to Otheryn;
- sending the Game Login Ticket directly to Otheryn;
- treating Gateway API v1 as gameplay protocol v1;
- inventing native Oteryn packets before producer evidence;
- replacing Otheryn ASIO with Tokio;
- removing Canary compatibility;
- production activation or legacy-path removal without exact cross-repository E2E and rollout authorization.

## Mandatory evidence for implementation

Every implementation package must record exact tested revisions for:

```text
Rust client
Oteryn Platform auth API
Oteryn Game Gateway
Otheryn game server
Game Session producer/consumer contract
selected gameplay adapter/profile
```

Repository tests do not prove production TLS, private ingress, service identity, secret rotation or deployed revision identity. Those remain separate production verification gates.
