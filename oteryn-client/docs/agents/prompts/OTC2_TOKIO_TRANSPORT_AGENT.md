# Prompt: protocol-neutral Tokio transport implementation

## Role and task

You are the sole implementation owner for the first executable package of the accepted Rust-client networking roadmap.

Repository:

`blakinio/otclient`

Product root:

`oteryn-client/`

Task mode:

`IMPLEMENTATION`

Package:

`Package A — protocol-neutral Tokio transport`

Coordination ID:

`OTS-20260804-native-protocol-selection`

Implement and deliver the protocol-neutral migration from the current blocking worker-owned TCP transport to an application-owned Tokio runtime without changing gameplay wire formats, login contracts or server behavior.

Continue autonomously through implementation, validation, review, merge and task archival. Do not stop after producing only an ADR, benchmark, abstraction or partial transport prototype.

## Mandatory startup

Before any mutation, read completely:

- repository root `AGENTS.md`;
- `AGENTS.override.md`, when present;
- `oteryn-client/AGENTS.md`;
- every nearer `AGENTS.md` governing touched paths;
- `docs/agents/AGENTS.md` and required root governance documents;
- `oteryn-client/docs/architecture/ARCHITECTURE.md`;
- `oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md`;
- `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md`;
- `oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md`;
- `oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md`;
- `docs/agents/CROSS_REPO_CONTRACTS.md`;
- current `Cargo.toml`, `Cargo.lock`, transport, runtime, session and application integration code;
- all active task records, open PRs, branches and shared-path leases affecting the Rust client.

Verify current live repository state. Do not rely on this prompt for current commit IDs or ownership.

## Ownership and concurrency

Create one dedicated task record, branch and early draft PR.

Declare exact:

- `owned_paths`;
- crates and public interfaces touched;
- `reuses`;
- `depends_on`;
- `blocks`;
- shared-path leases;
- validation scope.

Obtain exclusive lease before changing shared workspace files such as:

- `oteryn-client/Cargo.toml`;
- `oteryn-client/Cargo.lock`;
- application/runtime composition files;
- architecture catalogues or workflows.

The active P2 Canary producer may own `oteryn-client/crates/protocol-canary/**`. Do not take over, rewrite or broaden that task. Preserve its exact public behavior and coordinate any unavoidable interface change before editing an owned path.

## Existing game-entry boundary

The native Oteryn login chain already belongs to Oteryn Platform and Game Gateway:

```text
system browser
-> Oteryn Identity OAuth Authorization Code + PKCE
-> one-time Game Login Ticket
-> Oteryn Game Gateway
-> World Registry and Game Session
-> game server
```

This task must not:

- create another login server;
- implement OAuth, ticket issuance or Gateway behavior;
- request or store an Oteryn password;
- bypass Game Gateway;
- change the Gateway JSON contract;
- change Otheryn or Oteryn-Platform;
- create `protocol-oteryn`;
- implement automatic protocol selection.

The existing login/session consumers must continue to work through the new protocol-neutral transport boundary.

## Primary outcome

Deliver this architecture:

```text
application-owned runtime
  -> game-session supervisor
     -> bounded command/control queues
     -> selected existing framing/adapter
     -> Tokio TCP reader and writer ownership
```

Inbound:

```text
Tokio reader
-> bounded frame assembly
-> existing fail-closed codec/adapter
-> validated GameEvent
-> existing simulation/application boundary
```

Outbound:

```text
validated session-fenced GameCommand or bootstrap message
-> existing adapter/codec
-> bounded writer queue
-> Tokio writer
```

Tokio must remain below domain, simulation, renderer, UI and gameplay features.

## Required runtime design

Use the smallest justified Tokio feature set. Do not enable `full` by default without evidence.

The application owns runtime creation and shutdown. Do not introduce a hidden global runtime.

The implementation must provide:

- `tokio::net::TcpStream` or an equivalently justified Tokio socket path;
- `TCP_NODELAY` preservation where currently applicable;
- independent safe read and write ownership;
- bounded inbound, outbound and control queues;
- explicit connect, read, write and idle deadlines consistent with existing contracts;
- explicit cancellation;
- deterministic joined shutdown;
- terminal close after errors that may desynchronize framing;
- bounded allocation and frame-size enforcement before allocation;
- typed queue-full, timeout, cancellation and protocol-terminal errors;
- stale-session generation fencing;
- no unbounded task spawning;
- no network work on the window/render thread;
- no blocking filesystem, asset, decompression, shader or GPU work on ordinary async tasks.

Use `spawn_blocking` only when unavoidable, bounded and documented.

## Compatibility

The migration is wire-compatible.

Do not change:

- Canary opcodes;
- field layouts;
- framing bytes;
- checksums;
- encryption;
- compression semantics;
- login API JSON;
- Game Login Ticket behavior;
- Game Session credentials;
- protocol selection policy;
- Otheryn server networking.

Where the current transport exposes stable errors, limits or shutdown behavior, preserve them or record and test an explicitly approved compatibility change.

Do not claim lower Internet ping. Measure only client-controlled latency, CPU, allocation and shutdown behavior.

## Queue and backpressure rules

All queues are bounded and have explicit capacities.

Prove:

- cancellation and shutdown cannot be starved;
- control messages cannot be starved by gameplay traffic;
- latency-sensitive movement cannot be starved by background traffic;
- spell, item, loot, trade and chat commands are not silently dropped or reordered;
- command coalescing occurs only when an existing semantic contract proves replacement safe;
- overflow produces a typed error and metric rather than unbounded memory growth;
- commands from an old session generation cannot reach a replacement session.

Do not broaden `GameCommand` merely to exercise transport tests. Use existing commands and synthetic protocol-neutral fixtures.

## Tests

Add deterministic focused coverage for at least:

- successful connect and shutdown;
- simultaneous full-duplex read/write;
- partial reads;
- partial writes or a controlled writer abstraction proving them;
- cancellation during connect;
- cancellation during read;
- cancellation during write/backpressure;
- connect/read/write timeout;
- connection reset and EOF;
- malformed and oversized frame length through the existing framing boundary;
- inbound and outbound queue saturation;
- control priority/no starvation;
- preserved strict ordering;
- stale-session rejection;
- replacement session isolation;
- shutdown with queued work;
- no leaked runtime tasks;
- no unbounded allocation under burst/slow-consumer scenarios;
- the window/render thread never performs blocking network I/O;
- existing Canary transport and technical-login tests remain green.

Use deterministic local loopback or in-memory test peers. Do not require production credentials, proprietary assets or public game services.

## Comparative evidence

Retain or create a bounded benchmark/replay harness comparing the current worker transport with the selected Tokio path where practical.

Measure at minimum:

- command queue wait median and p95/p99;
- representative small and burst message throughput;
- CPU time;
- allocation/high-water behavior;
- slow-consumer behavior;
- cancellation and shutdown latency.

Name the environment and workload. Do not generalize beyond measured evidence.

## Validation and delivery

Run all repository-required validation on the exact final head, including as applicable:

- pinned formatting;
- strict Clippy;
- workspace tests;
- focused transport tests;
- architecture policy;
- supply-chain checks;
- Windows Rust Client workflow;
- repository CI;
- benchmark/replay evidence;
- fresh independent architecture/security review;
- full changed-file and diff review;
- zero unresolved review threads.

Do not weaken, skip or delete checks to obtain green CI.

Update module catalogue, changelog, ADR notes and task evidence when public modules or interfaces change.

Merge only after all exact-head gates pass. Archive the task and release every lease after merge.

## Completion rule

Do not declare completion when Tokio is merely added as a dependency or when a prototype compiles.

Completion requires:

- the production client transport/session path uses the accepted Tokio runtime;
- the old path is removed, retained behind a clearly justified benchmark/test boundary, or explicitly deprecated without two production owners;
- bounded full-duplex operation, cancellation, deadlines and deterministic shutdown are proven;
- existing Canary and game-entry behavior remains compatible;
- no Platform, Gateway, Otheryn or gameplay-protocol behavior is invented;
- exact-head CI and independent review pass;
- PR merges;
- task archives and ownership releases.
