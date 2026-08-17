# Canonical XRes window integration — evidence basis

## Trusted base

- main: `1eb4a8edecba3966aa1e6155e241b404eb4d30cb`
- physical identity producer: PR #457 / merge `16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc`
- producer archive: PR #459 / merge `c55e3523e6e9d50df511e65dce9145a8f951a5f5`
- persistent XRes client-base fix: PR #461 / merge `1eb4a8edecba3966aa1e6155e241b404eb4d30cb`

## Retained physical fact

Run `32015479835` retained one unique VIEWABLE `1920x1080` X11 resource `0x00c00011`. QueryClientIds returned owning client base `0x00c00000`, LocalClientPid value length `4`, and PID `13648`, equal to the exact fenced client PID. Cleanup completed. The accepted classification is `XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT`.

Raw retained reply:

```text
01000300040000000100000000000000000000000000000000000000000000000000c000020000000400000050350000
```

PR #461 corrected the pure promoted helper so `extract_local_client_pid` accepts the owning-client resource-base semantics while retaining one-spec fail-closed cardinality, exact mask and positive CARD32 PID checks.

## Remaining canonical mismatch

The trusted canonical session worker still locates the window with:

```text
xdotool search --onlyvisible --pid <pid> --name '^Tibia$'
```

That selector depends on X11 properties/name identity which the physical producer proved absent for the exact-client viewable resource. Re-running the same worker unchanged would repeat the known failure and is not useful evidence.

## Integration

The hosted-only integration adds:

- `tibia-official-client-re-xres-window-owner.py`: bounded X11 tree enumeration plus raw XRes 1.2 transport using the already-promoted wire helper; returns only one VIEWABLE `1920x1080` XID whose LocalClientPid equals the expected PID and fails closed otherwise.
- `tibia-official-client-re-canonical-xres-worker-adapter.py`: exact-anchor transformation of the canonical worker's legacy `window()` implementation; refuses drift/duplicate anchors and leaves the existing worker command and manifest shapes unchanged.
- deterministic unit tests plus a hosted workflow that generates the worker from the current canonical source, runs `bash -n`, rejects any remaining legacy PID/name selector, reruns the promoted raw-XRes helper tests, and reruns the canonical transition regression suite.

## Boundary

This branch does not access Synology, X11 runtime state, canonical registration/lease state, credentials, login/gameplay, process memory, input, or client bytes. The historical PID `13648` is only a regression fixture and never current authority.

After merge, the canonical task must perform a fresh Track A admission. Per the current checkpoint, P0 must stop fail-closed if no legal current `IN_GAME` lifecycle is available and must not bootstrap a session solely for P0.
