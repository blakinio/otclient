# Window and event requirements

## Process/window lifecycle

- Create the event loop and all top-level windows on the process main thread.
- Create the first window only after the event loop reports the application resumed/ready state.
- Own exactly one initial top-level client window; multi-window support is outside the first slice.
- Treat `CloseRequested`, actual destruction and event-loop exit as distinct states.
- Stop rendering/work when the client area is zero-sized; resume only after a valid non-zero size.
- Resize, minimize, restore, focus loss/gain and monitor movement must not panic, block the event loop or leave stale platform state.
- Request drawing explicitly and render only in the redraw event; `about_to_wait` may schedule work but is not a rendering callback.

## DPI and coordinates

- Declare process DPI awareness in an application manifest; do not set it opportunistically after DPI-sensitive objects exist.
- Candidate policy is Per-Monitor V2, subject to exact packaged-runtime proof.
- Keep logical UI dimensions separate from physical window/surface pixels.
- Handle scale changes and the OS-suggested window size atomically enough that renderer/UI snapshots do not observe mismatched scale and physical size generations.
- Moving between monitors, changing display scale and changing resolution are required transition tests.
- Persist logical layout; do not persist raw physical pixels as universal UI geometry.
- Reject NaN/non-finite or impossible scale/coordinate values before they reach UI/domain types.

## Keyboard, text and IME

- Normalize physical key identity separately from logical/text meaning and modifiers.
- Track focus generation so synthetic/stale key releases cannot mutate a replacement window/session.
- Enable IME only for an active text-input target.
- Model IME enabled, preedit/composition, committed result and disabled/cancelled states separately.
- Never emit both ordinary text and IME commit for one committed string.
- Cancel composition on focus loss, text-target replacement and shutdown according to observed platform behavior.
- Preserve bounded UTF-8 text and selection/cursor ranges; no raw OS pointer or unbounded composition payload enters UI state.

## Mouse and device input

- Cursor position is presentation input; it is affected by desktop coordinates/acceleration and is not suitable as high-precision camera delta.
- Mouse button and wheel input must retain device, phase/delta kind and focus/capture context before normalization to semantic actions.
- Prefer winit device events for the first spike. Introduce direct Raw Input only if measured requirements are not met.
- If Raw Input is required later, one application-owned window registers device classes. Reusable libraries must not call `RegisterRawInputDevices`.
- Device enumeration/registration failures are explicit non-secret errors; no device path or personal identifier enters diagnostics.
- Capture/grab is released on focus loss, close request and shutdown.

## File drop and untrusted paths

Winit exposes file-drop paths. The first shell must ignore them. Any later import surface validates user intent and path policy before reading; absolute paths never enter diagnostics.

## Required event observations in the spike

- initial resume/window creation;
- resize including zero width/height and restore;
- scale-factor transition between monitors;
- focus gain/loss;
- keyboard press/release and modifier changes;
- IME preedit/commit/cancel with at least one installed Windows IME;
- cursor movement, buttons, wheel and device motion where available;
- close requested, destroyed and event-loop exiting;
- OS logoff/shutdown behavior when the environment permits safe testing.

The evidence task does not assert that every OS message maps one-to-one to one winit event; the spike records actual normalized event sequences on exact tested revisions.
