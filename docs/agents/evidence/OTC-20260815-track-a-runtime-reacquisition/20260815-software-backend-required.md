# Track A RUNTIME software-render backend recovery

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`  
Execution head: `5965f03ecbb5c888a1bc22a4242d24f604a8002b`  
Run: `31887917603`  
Job: `95019811182`  
Runner: `synology-otclient-01`  
Conclusion: `FAILURE`  
Artifact id: `9247780885`  
Artifact ZIP SHA-256: `b15c623453291d9f47447932b7ab4581cebea481a403d9eea403f67bd3e7ca7f`

## FACT — bundled Qt precedence repair passed

Run #19 passed exact request/dependency fencing, pinned helper materialization, exact residue recovery from run #18, bootstrap, WARP/relay/Xvfb checks and cross-step process persistence. The exact official client was launched and retained as a credential-free task-owned process.

The previous `Qt_6.9 not found` loader error is absent. The sanitized client log reaches asset loading and task-local proxied HTTP requests, proving that the bundled Qt precedence repair is effective.

## FACT — current Vulkan/RHI launch profile does not produce a usable X11 window

The exact client log reports:

```text
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
```

The client remains alive long enough to load assets and use the task-local SOCKS path, but `resolve_window` finds no visible `^Tibia$` window and fails closed with `TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing` before the protected login step.

## FACT — exact-build historical successful login used the software Qt Quick backend

Historical Track A workflow `.github/workflows/tibia-official-client-re-software-world-login.yml` at exact-build research head `c04ff82918f954af019ab533bf6af0792dc730bf` launched the same fenced official Linux client with:

```text
QT_QUICK_BACKEND=software
QT_XCB_GL_INTEGRATION=none
```

That workflow successfully reached a visible `^Tibia$` window and subsequently world entry; later exact-build run `31806312967` used the resulting live session for structural reversible movement proof.

This is a stronger discriminator than relaxing the window-title gate. The window lookup mechanism itself is historically proven; the changed rendering backend is the material difference.

## Side-effect boundary

- protected login step was skipped;
- no credential values were injected;
- no movement/gameplay/economic action occurred;
- structural map records remained empty;
- exact current-run cleanup completed successfully and removed client/Xvfb/relay state.

## Next repair

Preserve exact bundled Qt precedence and `libproxy` support, but replace the unproven current `QSG_RHI_BACKEND=vulkan` launch profile with the exact historical `QT_QUICK_BACKEND=software QT_XCB_GL_INTEGRATION=none` backend before retrying generation 1. Keep the `^Tibia$` visible-window gate unchanged.
