# Windows platform foundation evidence

Status: evidence for a future WS-R02 spike. This directory accepts no dependency, platform API or supported Windows version.

Evidence cut: 2026-07-28; otclient base `048414f9457f6adaf6c3f94f8a8e6b92d624389d`.

## Findings

- `SUPPORTED` `winit 0.30.13` is the strongest current candidate for one-window/event-loop ownership. It is Apache-2.0, declares Rust 1.70 and exposes Windows-relevant close, destroy, focus, keyboard, mouse, IME, resize, DPI and redraw events.
- `SUPPORTED` the platform/application owner should keep `EventLoop`, window creation, DPI/IME policy and shutdown coordination on the main thread. Cross-thread work may send bounded commands through an event-loop proxy or application-owned channel.
- `SUPPORTED` `raw-window-handle 0.6.2` is an interop contract, not a windowing backend. Do not add it directly unless a renderer/surface boundary needs its public types; winit already supports the 0.6 contract.
- `BLOCKED` direct Win32 bindings in the first spike. Add a narrow Windows-only dependency only after a proven gap in winit for raw input, IME, DPI or shutdown behavior, with focused unsafe/FFI review.
- `PROVEN` Windows recommends process DPI awareness through the application manifest; Per-Monitor V2 and `WM_DPICHANGED` require logical/physical-size handling during monitor transitions.
- `PROVEN` Raw Input registration is process/window ownership: Microsoft warns only one window per raw-input device class should register, so registration must not occur in a reusable library.
- `PROVEN` IME composition is stateful; preedit/result/cancel behavior must not be collapsed into ordinary key events or duplicate committed text.
- `BLOCKED` exact minimum supported Windows release and hardware tier. A CI runner/build proves only that exact environment.

## Files

- `WINDOW_AND_EVENT_REQUIREMENTS.md`
- `DEPENDENCY_EVALUATION.md`
- `THREAD_AND_SHUTDOWN_MODEL.md`
- `SPIKE_RECOMMENDATION.md`

## Primary references

- https://docs.rs/winit/0.30.13/winit/application/trait.ApplicationHandler.html
- https://docs.rs/winit/0.30.13/winit/event/enum.WindowEvent.html
- https://docs.rs/winit/0.30.13/winit/event_loop/struct.EventLoop.html
- https://docs.rs/crate/winit/0.30.13/source/Cargo.toml
- https://docs.rs/crate/raw-window-handle/0.6.2/source/Cargo.toml
- https://learn.microsoft.com/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows
- https://learn.microsoft.com/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process
- https://learn.microsoft.com/windows/win32/hidpi/wm-dpichanged
- https://learn.microsoft.com/windows/win32/inputdev/about-raw-input
- https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-registerrawinputdevices
- https://learn.microsoft.com/windows/win32/intl/wm-ime-composition
- https://learn.microsoft.com/windows/win32/learnwin32/closing-the-window
- https://learn.microsoft.com/windows/win32/shutdown/wm-queryendsession
- https://learn.microsoft.com/windows/win32/shutdown/wm-endsession

## Boundary

No runtime, DPI, IME, raw-input, shutdown, renderer, performance or Windows-version compatibility is claimed until the recommended spike runs on named exact environments.
