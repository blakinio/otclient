# ADR-0005: Gameplay Channels Are Selected Through Login or Relog

Status: accepted  
Date: 2026-07-26

## Context

One logical world may expose several parallel gameplay instances. The user selects a channel during initial entry and may switch later. Earlier discussion briefly confused these instances with transport multiplexing channels.

## Decision

Represent gameplay instances with a typed `WorldChannelId` supplied by the authoritative directory/gateway contract.

Normal entry is:

```text
account session -> character -> world -> gameplay channel -> one-shot ticket -> game session
```

Changing Channel 1 to Channel 2 closes the current game session and performs a relog with a fresh channel-scoped game-entry transaction. The valid account session may remain active.

Seamless in-game channel transfer is not part of the initial client architecture.

Transport streams/channels use separate terminology and types.

## Consequences

- client lifecycle and UI explicitly expose channel selection;
- session-scoped state is destroyed between channels;
- ticket reuse across channels is prohibited;
- no complex live world-state migration is required in the first client;
- server-side session exclusivity remains an external authoritative contract.

## Rejected

- treating world channels as QUIC/logical network streams;
- changing channels by only swapping an address while preserving mutable session state;
- silently redirecting the user to a different channel after confirmation;
- designing seamless transfer before it is a product requirement.
