# ADR-0003: Protocol Adapter Boundary

Status: accepted  
Date: 2026-07-26

## Context

The first playable client must connect to Canary, while the target ecosystem will later provide native Oteryn game services. Binding domain/UI logic to Canary opcodes would make that migration another rewrite.

## Decision

Define stable typed `GameEvent` and `GameCommand` domain contracts. Keep byte transport, framing and protocol translation outside the game domain.

Implement independent adapters:

- `protocol-canary` for exact selected Canary revisions;
- `protocol-oteryn` for the future native Oteryn contract.

Adapters may depend on domain contracts. Domain, features, UI and renderer may not depend on concrete adapters.

Exact wire facts require producer evidence, compatibility matrices, negative fixtures and cross-repository coordination.

## Consequences

- Canary enables initial gameplay without becoming the permanent client architecture;
- normalized replay and simulation tests can run without a live server;
- adapter-specific differences require deliberate mapping and may expose genuine domain-contract gaps;
- additional translation code is accepted in exchange for isolation.

## Rejected

- exposing raw packets to UI/features;
- placing Canary opcode checks in game-domain types;
- one adapter with conditional branches for unrelated protocols;
- designing the native Oteryn wire contract from client assumptions before server coordination.
