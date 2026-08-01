# Nonblocking technical-login shutdown

Status: accepted  
Date: 2026-08-01  
Finding: `OTC2-AUD-002`  
Task: `OTC2-20260801-nonblocking-shutdown-remediation`

## Context

The Windows shell owns the renderer, window and `winit` event loop. The technical-login runtime owns Identity and Canary admission threads through `JoinHandle`s. A close request previously reached a synchronous runtime shutdown path that could join an unfinished worker on the event-loop thread while an HTTP, connect, read or write operation was still inside a bounded blocking call.

The client must not detach, forget or forcibly terminate a worker. It must also remain responsive while cancellation is being observed.

## Decision

1. `TechnicalLoginRuntime::begin_shutdown` records one monotonic shutdown start, requests cancellation and returns typed progress.
2. `TechnicalLoginRuntime::poll_shutdown` retains every unfinished worker and calls `join` only after `JoinHandle::is_finished()` is true.
3. Progress is one of:
   - `Pending(WorkerKind)` while the worker is still inside the accepted bound;
   - `Overdue(WorkerKind)` after 31 seconds;
   - `Complete` after all workers have been joined exactly once and session state is logged out.
4. `Overdue` is diagnostic state. It does not permit worker detachment, renderer/window destruction or event-loop exit. Polling continues until `Complete` or a typed join failure.
5. The Windows shell begins shutdown from close/destroy/failure paths, then advances it from existing worker-completion user events and a 16 ms `ControlFlow::WaitUntil` fallback.
6. The shell releases the renderer and window and calls `event_loop.exit()` only after runtime shutdown reports `Complete` and the shell close state has been requested.
7. The runtime `Drop` implementation remains an ownership-invariant fallback for non-event-loop misuse. The normal Windows event-loop path reaches drop with no live worker.
8. Platform HTTP keeps its 30-second global maximum. Public TCP connect, read and write configuration rejects any timeout above 30 seconds. The loopback callback retains its 300-second user-wait maximum and at-most-250-millisecond read slices, so cancellation remains observable without shortening the user authorization window.

## Consequences

- Close handling remains responsive while a bounded worker finishes.
- A stalled worker stays visible and owned instead of being silently abandoned.
- Shutdown may remain pending beyond 31 seconds, but resource teardown order is deterministic.
- Starting new authentication or connection work after shutdown begins fails with `ShuttingDown`.
- Existing success, failure, cancellation and redaction contracts remain unchanged.

## Validation

The implementation includes a gate-controlled worker test proving `Pending -> Overdue -> Complete`, ownership retention while overdue, rejection of new work, and final joined/logged-out completion. The final branch is additionally required to pass locked metadata, rustfmt, strict Clippy, the complete workspace tests, architecture policy, Supply Chain and repository `CI / Required`.
