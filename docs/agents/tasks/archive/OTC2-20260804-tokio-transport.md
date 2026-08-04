---
task_id: OTC2-20260804-tokio-transport
status: done
created: 2026-08-04
completed: 2026-08-04
coordination_id: OTS-20260804-native-protocol-selection
implementation_pr: blakinio/otclient#266
implementation_head: f3be954c3d3b6cd1dfc9d3368545e8e5a496b18f
implementation_merge_commit: 1f3d766124f2eb7fa7d329102f3a35f0a3197ed8
evidence_run: 30929681775
final_rust_client_run: 30938267863
final_repository_ci_run: 30938268215
released_paths:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/transport/**
  - oteryn-client/crates/app-runtime/**
  - oteryn-client/apps/client/**
  - oteryn-client/tests/integration/technical-login/**
  - oteryn-client/docs/research/transport/**
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
---

# OTC2-20260804-tokio-transport — archived

## Result

The protocol-neutral Rust game transport was migrated from the production blocking connection owner to an application-owned Tokio runtime and merged in PR #266.

The delivered boundary provides:

- exact Tokio `1.51.4` with the minimum justified I/O, networking, runtime, synchronization, macro and time features;
- a named application-owned two-thread network runtime with deterministic shutdown and no hidden global executor;
- bounded independent inbound, gameplay and background queues;
- full-duplex reader, writer and cancellation supervision;
- total-operation connect, read and write deadlines plus an idle deadline;
- cancellation during connect, read, saturated inbound delivery and backpressured write;
- gameplay FIFO and priority over background traffic without silent dropping or reordering;
- typed queue-full, timeout, cancellation, stale-session, connection and protocol-terminal failures;
- session-generation fencing, header-first bounded allocation, `TCP_NODELAY`, metrics and joined shutdown;
- the prior blocking implementation only behind `blocking-baseline` for tests and comparative evidence.

Identity, Game Gateway, Game Session, OAuth, ticket behavior, protocol-canary public/wire contracts, Platform and Otheryn were not changed. No `protocol-oteryn`, automatic protocol selection or physical-network latency claim was introduced.

## Validation

Exact final implementation head `f3be954c3d3b6cd1dfc9d3368545e8e5a496b18f`:

- repository CI `30938268215`: PASS, including `CI / Required`;
- Rust Client `30938267863`: PASS, including locked metadata, formatting, strict workspace Clippy, full workspace tests, architecture policy and supply-chain checks;
- independent architecture/security/diff audit: PASS with zero critical, high or material-medium findings;
- unresolved review threads and requested changes: none.

Windows comparative evidence run `30929681775` recorded only deterministic hosted-runner loopback and process behavior:

- latency p50/p95/p99: blocking `40/74/91 µs`, Tokio `42/70/99 µs`;
- synthetic pipelined throughput: `23,003.74` versus `87,961.58 frames/s` (`3.82×`);
- process CPU time: `62.500 ms` versus `46.875 ms` (`0.75×` for this exact workload);
- Tokio queue high-water `968`, queue-full loss `0`, saturated-consumer cancellation `15.788 ms`;
- joined shutdown `52 µs` blocking and `121 µs` Tokio.

These values are bounded evidence for the exact CI environment and do not predict Internet, Gateway or game-server RTT.

## Final state

```yaml
implementation_status: merged
runtime_enabled: true
production_transport_owner: tokio
blocking_production_owner: false
blocking_baseline_retained_for_tests: true
protocol_canary_wire_changed: false
gateway_or_game_session_changed: false
platform_changed: false
otheryn_changed: false
protocol_oteryn_exists: false
automatic_protocol_selection_enabled: false
open_material_findings: 0
unresolved_review_threads: 0
leases_released: true
blockers: []
next_authorized_work:
  - coordinated protocol-oteryn client/server implementation at the accepted native contract revisions
  - later automatic selection and exact cross-repository E2E rollout package
```
