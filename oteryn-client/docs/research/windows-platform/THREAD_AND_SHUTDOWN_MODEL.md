# Thread and shutdown model

## Ownership

```text
main/event thread
  owns EventLoop, Window, focus/capture, DPI/IME policy and application lifecycle
  receives bounded user events from workers

simulation/application owners
  own mutable product/session state through explicit generations
  never call window APIs directly

renderer owner (later)
  owns GPU device/surface resources
  consumes current physical size/scale generations

I/O/worker tasks (later)
  perform bounded non-frame work
  report results through bounded channels/proxy and cancellation generations
```

The event loop is not placed behind a broad mutex and is not run inside an async executor. Window handles are not treated as freely transferable application state.

## Event-loop command boundary

Cross-thread requests use a small closed command enum, for example redraw, set title from reviewed static state, update cursor mode or request orderly shutdown. No closure, arbitrary callback, protocol packet, secret or unbounded string crosses this boundary.

Queue saturation has an explicit policy: coalesce redraw/state refresh, reject duplicate shutdown and never drop safety-critical close/device-loss state silently.

## Shutdown state machine

```text
Running
  -> CloseRequested
  -> Quiescing
  -> WindowDestroying
  -> EventLoopExiting
  -> Stopped
```

### CloseRequested

- accept only the first shutdown request;
- stop accepting new game/session work;
- cancel active task/session owners explicitly;
- release input capture and disable IME;
- request bounded application cleanup without blocking the event loop.

### Quiescing

- drain only explicitly selected bounded completion signals;
- discard stale results using process/session/task generations;
- flush no network/upload/support bundle by default;
- persist only already validated non-secret settings through a later owning service;
- escalate after a defined deadline instead of hanging indefinitely.

### WindowDestroying

- renderer/application drops surface references before final window destruction;
- no worker may retain a mutable window owner;
- destruction may occur after an OS close or independently, so it is idempotent.

### EventLoopExiting / Stopped

- no new platform command is accepted;
- remaining cancellation observers may finish/drop without implicit global work;
- process exit proves no hidden worker or global logger must remain alive.

## OS logoff/shutdown

Windows can ask whether a session may end and later announce the result. The application must respond promptly; it cannot depend on a long asynchronous save/network sequence. A later direct Win32 task may handle these messages only if the winit spike proves the portable exit callback insufficient.

Policy:

- maintain recoverable state continuously rather than relying on shutdown time;
- do not veto OS shutdown for optional work;
- no credential refresh, upload or network logout is required for process termination correctness;
- treat unexpected termination as possible at every point.

## Required tests for the implementation spike

- duplicate close request is idempotent;
- close during resize, focus loss and IME composition;
- worker result races with close and is rejected after generation change;
- bounded queue saturation while shutdown command still succeeds;
- zero-size window then close;
- window destruction before expected close callback;
- event-loop proxy send after exit fails safely;
- repeated process launch/close has no surviving background work;
- optional OS logoff/shutdown observation on a disposable Windows environment.

No test may claim renderer/session cleanup before those owners exist; the shell proves only its own lifecycle and command boundary.
