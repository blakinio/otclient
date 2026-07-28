# Dependency evaluation

Evidence date: 2026-07-28. Versions below are candidates, not workspace selections.

| Candidate | Current evidence | Role | Disposition |
|---|---|---|---|
| `winit 0.30.13` | Apache-2.0; Rust 1.70; current `ApplicationHandler` event-loop model; Windows target support | create window, receive normalized lifecycle/input/DPI/IME events, proxy user events | recommended dependency candidate for the bounded spike after a fresh advisory/license/source review |
| `raw-window-handle 0.6.2` | MIT OR Apache-2.0 OR Zlib; Rust 1.64; interoperability traits/handles | bridge window/display ownership to a later renderer/surface | do not add directly unless a public crate boundary needs it; use winit's 0.6 support first |
| direct `windows-sys`/Win32 binding | Windows API metadata/raw FFI; exact version not selected | fill a proven Windows-only gap such as explicit Raw Input or shutdown messages | deferred; requires a focused dependency/unsafe/FFI task and narrow platform module |
| async runtime | no candidate selected | background I/O/timers | out of scope; event loop must not be owned by an async executor |
| `wgpu` | architecture candidate only | renderer/surface/GPU | out of scope for the platform shell spike |

## Winit fit

The current API exposes required application callbacks for resume, window events, device events, user events, waiting and exit. Relevant `WindowEvent` variants include resize, close, destruction, focus, keyboard, modifiers, IME, mouse, scale change and redraw.

Constraints:

- `EventLoop` is not `Send` or `Sync`; main-thread ownership matches the architecture.
- graphics/window initialization should occur after the first resumed callback.
- redraw work belongs in `RedrawRequested`, not `about_to_wait`.
- IME events require explicit enablement on the active window.
- Windows does not expose every lifecycle concept through portable events; exact behavior needs runtime evidence.

## Feature/dependency policy

For a Windows-first package:

- pin an exact winit version after reviewing its current Cargo metadata, release notes, advisories and Windows dependency graph;
- do not enable unrelated serialization/mobile/web/Unix feature sets merely because they are defaults on other targets;
- let Cargo target resolution select Windows-only transitive dependencies; do not copy transitive versions into workspace dependencies;
- retain committed lockfile and cargo-deny policy;
- inspect native/unsafe code in the Windows dependency graph and document the boundary;
- avoid direct `raw-window-handle` unless renderer/platform public ownership requires it;
- avoid direct Win32 binding until a focused spike proves a missing portable behavior.

## Direct Win32 decision triggers

A dedicated Windows binding task is justified only when the winit spike proves one of these with exact evidence:

- high-precision device motion cannot satisfy the input requirement;
- required IME composition/candidate behavior is not exposed safely;
- DPI manifest/message handling cannot satisfy Per-Monitor V2 transitions;
- OS logoff/shutdown messages require an explicit non-blocking response path;
- another required Windows feature has no stable public winit surface.

The task then owns one narrow platform module, exact API calls, message-order tests, safety invariants and no arbitrary native surface exposed upward.

## Compatibility status

- Workspace Rust 1.94 exceeds both candidate MSRVs.
- License strings fit the current general allowlist only after the actual dependency task verifies every resolved package.
- Buildability on GitHub-hosted Windows is not proof of minimum Windows release, DPI/IME device behavior or end-user hardware support.
