# Windows application-shell spike recommendation

## Decision

After a fresh preflight and shared Cargo-lease check, implement one small Windows-only application-shell package using exact-pinned `winit 0.30.13` as the sole new direct platform dependency unless current evidence changes.

The spike opens one blank window and proves lifecycle/input/diagnostics/shutdown contracts. It adds no renderer, GPU surface, async runtime, networking, protocol, assets, UI framework or game state.

## Proposed package

```text
apps/client/**            minimal executable and application handler
crates/platform/**        narrow normalized window/input/lifecycle contracts only when needed
```

Prefer one crate plus one binary over speculative platform abstractions. Reuse:

- `oteryn-foundation` generations, monotonic time, deadlines and cancellation;
- `oteryn-diagnostics` structured non-secret events;
- existing workspace architecture/lint/supply-chain policy.

## Observable behavior

- start one process and create one resizable Windows window after resume;
- show a reviewed static title;
- record structured, redacted lifecycle events;
- process resize, zero-size/minimize/restore, focus, keyboard, mouse, wheel, IME and scale-factor events;
- request redraw without renderer work;
- accept a bounded cross-thread synthetic user event through the event-loop proxy;
- close through one idempotent state machine and terminate with no hidden worker.

## Required dependency preflight

- exact winit version/source/release/license/advisory/MSRV review;
- exact Windows target dependency graph and cargo-deny result;
- no direct `raw-window-handle`, `windows-sys`, async runtime or `wgpu` unless split into a separately justified task;
- record every native/unsafe dependency boundary without introducing workspace-wide exceptions.

## Acceptance

### Automated

- unit tests for state transitions, duplicate close, bounded commands and stale-generation rejection;
- no arbitrary external text in platform errors/diagnostics;
- locked metadata, formatting, Clippy, workspace tests, architecture check and cargo-deny;
- exact-head Windows CI;
- repeated synthetic application-state construction/shutdown tests with no global mutable state.

### Named Windows runtime evidence

Record OS build, display topology/scales, keyboard layout/IME and input devices. Verify:

- create, resize, minimize, restore and close;
- move between two different monitor scale factors where available;
- IME enable, preedit, commit and cancel;
- keyboard/modifier/focus transitions without stuck state;
- mouse buttons/wheel/cursor plus device motion where winit exposes it;
- close during IME, focus loss and zero-size state;
- 100 sequential launch/close cycles with no observed surviving process/thread/resource symptom;
- manifest DPI-awareness behavior in the packaged executable.

Unavailable hardware/IME/multi-monitor cases remain explicit blockers, not inferred passes.

## Non-goals

- no accepted minimum Windows version;
- no GPU/swapchain/window-surface lifecycle;
- no raw Win32 registration or message hook;
- no production input bindings or settings persistence;
- no account/game session, renderer, UI, audio or asset loading;
- no cross-platform compatibility claim;
- no deployment/installer work.

## Follow-up decision

After the runtime matrix:

- keep winit-only when requirements pass;
- open a focused Windows-binding task only for a proven missing behavior;
- begin renderer surface work only after the window owner and shutdown contract merge;
- do not expand the spike into a general application framework.
