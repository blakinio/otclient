# ADR-0001: Greenfield Rust Oteryn Client

Status: accepted  
Date: 2026-07-26

## Context

The repository contains a mature C++ client with Lua/OTUI features. The product owner requires a new client designed from scratch for performance, safety and the future Oteryn ecosystem. Canary is needed during migration, but legacy implementation structure must not constrain the target.

## Decision

Create the new product under `oteryn-client/` as a Rust workspace.

The existing C++/Lua/OTUI client remains in place as legacy/reference evidence until a later retirement decision. The Rust client does not link, embed or execute legacy runtime code.

A mandatory foundation audit precedes production workspace bootstrap.

## Consequences

Positive:

- architecture can use modern ownership, concurrency, GPU and security models;
- legacy and greenfield CI/dependencies remain isolated;
- migration can be incremental at product level without contaminating runtime design.

Costs:

- feature and protocol behavior must be reimplemented;
- temporary dual-client maintenance is required;
- compatibility evidence and legal asset migration require dedicated audit work.

## Rejected

- line-by-line Rust port;
- progressive replacement inside the C++ engine;
- maintaining Lua/OTUI compatibility as a core requirement;
- moving all legacy files before the new client reaches parity.
