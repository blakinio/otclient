# Coordinator review — post-RHI / XRes evidence chain

## Promotion authority

Coordinator-only review under `OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md`.

Trusted integration base: `main@845adabba5f6d2bfecb6d54bc13834c47cc61c94`.

## Source Draft #438 — ACCEPT

Final source head: `171fbfa679c8c75dc9722fe39c19141962282f01`.

Exact-final checks recorded by the source and re-inspected by the coordinator:

- Track A governance `31972667061 = SUCCESS`;
- repository CI `31972667199 = SUCCESS`;
- `CI / Required` job `95227425189 = SUCCESS`;
- unresolved review threads: `0`.

The coordinator independently re-read physical job `95226396914` from run `31972261899`. The job directly proves:

- same-generation Track A admission and exact fences passed;
- canonical state access `NONE`;
- GLX present, opcode `150`; RENDER present, opcode `139`;
- exact client remained alive;
- raw X11 at t+15 and t+35 contained a non-root `VIEWABLE` `1920x1080` XID `0x00c00011` while the name-based xdotool search remained `0`;
- PID/name/class identity for that XID remained unavailable through the tested property path;
- OpenGL llvmpipe context, QRhi Vulkan and QtQuick.Window initialized;
- the QQmlEngine/QSGSoftwareRenderThread cross-thread warning is present but not proven causal;
- discriminator result and cleanup completed.

Accepted bounded classification:

`PROVEN_RAW_X11_TREE_HAS_VIEWABLE_1920X1080_NAMELESS_PIDLESS_WINDOW_FROM_T15_WHILE_XDOTOOL_NAMED_VISIBLE_SEARCH_RETURNS_ZERO_AND_EXACT_CLIENT_REMAINS_ALIVE_POST_GLX`

The coordinator rejects any stronger interpretation that the XID is already proven to belong to the official-client PID.

## Source Draft #442 — ACCEPT

Final source head: `80bd75a1352ef1ffe84c3dcc34bf51a0cf0a7c54`.

Exact-final checks:

- Track A governance `31973655155 = SUCCESS`;
- repository CI `31973655294 = SUCCESS`;
- `CI / Required` job `95229833967 = SUCCESS`;
- unresolved review threads: `0`.

The coordinator independently re-read physical job `95229260820` from run `31973388722`. Direct evidence shows:

- same-generation admission/base/source/support fences passed;
- exact isolated client launched once;
- the raw full-display viewable XID was reproduced;
- at t+05/t+15/t+35 the observer reported `libxcb=True`, `libxcb_res=False`, `libX11=True`;
- `QueryClientIds(LocalClientPid)` therefore did not execute;
- final XRes classification was `XRES_IDENTITY_UNRESOLVED`;
- the discriminator reached `PASS_DISCRIMINATOR_CAPTURED` and `CLEANUP=COMPLETE` before later post-job cancellation from the hardening generation.

Source #440's accidental physical scheduling was separately fenced out before generated-script/client execution and is not counted as a client launch.

Accepted bounded classification:

`PROVEN_XRES_IDENTITY_UNRESOLVED_BECAUSE_LIBXCB_RES_HELPER_UNAVAILABLE_ON_RUNNER_FIXED_ALLOWLIST`

Exact viewable-XID PID ownership remains `UNKNOWN`.

## Source Draft #443 — ACCEPT_WITH_EDITS

Final source head: `02c63797b0835ea745a08362c12874307129a9d1`.

Exact-final checks:

- Track A governance `31973955917 = SUCCESS`;
- repository CI `31973956038 = SUCCESS`;
- `CI / Required` job `95230545137 = SUCCESS`;
- unresolved review threads: `0`.

The coordinator independently re-read read-only support job `95230007324` from run `31973740033`. Direct evidence proves:

- Track A admission/base fence passed;
- no X server or official client started;
- canonical state access `NONE`;
- `libxcb-res.so*` and `libXRes.so*` are absent in all fixed contained/system roots tested;
- contained and system libxcb/libX11 copies are present;
- contained `XResproto.h` is present and emitted relevant v1.2 lines including QueryClientIds minor opcode `4`, LocalClientPID mask `0x02`, request fixed size `8` and reply fixed size `32`;
- checked generated XCB-RES/public XRes headers and pkgconfig files are absent;
- classification is `HEADERS_PROTOCOL_BASIS_PRESENT_NO_HELPER_LIBRARY`.

### Coordinator correction

The source Markdown contained two library SHA-256 values inconsistent with job `95230007324` and asserted a header digest that the job did not emit. Promotion corrects those claims to the raw-log values:

- libxcb observed SHA-256: `7958a0136b121bdc4c708968569ad152a9ed208ab026e2537b1005dde64ca440`;
- libX11 observed SHA-256: `c5b5d782bd9cab3420a62df88f5c991507edf3331a89f98464ddbc538c37b879`;
- no XResproto header SHA-256 is promoted.

The source also described system aliases as resolving to contained paths; raw logs instead show distinct system real paths with matching observed library hashes. Promotion corrects that wording.

These edits do not alter the support classification.

## Integrated consequence

Promoted facts establish a narrower causal frontier:

1. graphics initialization is no longer the known blocker;
2. a raw full-display X11 window exists, but exact PID ownership is not proven;
3. convenience XRes helper libraries are absent;
4. contained protocol definitions provide enough observed wire-layout basis to design a raw XRes helper without package installation.

Canonical bootstrap retry and canonical window-identity relaxation remain unauthorized.

## Next action

Build and validate a hosted/static raw-XRes encoder/parser from the contained `XResproto.h` layout without Xvfb or official-client execution. Only after host-side validation may a separately admitted physical identity run be considered.
