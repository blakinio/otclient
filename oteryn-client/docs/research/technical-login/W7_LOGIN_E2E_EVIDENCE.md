# W7 Technical Login Application Integration Evidence

Status: repository/fake technical flow complete; external real-path evidence blocked  
Lane: `W7-LOGIN-E2E`  
Branch: `feat/OTC2-20260731-w7-login-e2e-final`  
PR: #118

## Exact merged producers

- W7 entry contract: `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`;
- W7 Identity/Platform: `d66da47a33d6639876f3edda2b2c08709d1b7a5e`;
- W7 Canary entry: `4a193bdf10ac32a8a2d8dc12f31706c7d668c8f9`;
- Canary lifecycle archive and launch base: `065a37bcc1eab752f2a5504ba58882c4c9a6e6c9`;
- exact final restack main: `a43cf375dc25b95df790e515ca222bc80cae26e1`;
- restack merge commit: `4696faa961ef73ce361e8fd82351e2acea3f01f8`.

## Delivered composition

`oteryn-app-runtime` owns only top-level orchestration. It allocates one non-zero attempt generation, runs Identity and admission in separately owned cancellable threads, accepts only producer-owned account/directory/credential values, validates the explicit selection, moves the lifecycle into the admission worker, joins every worker and restores the producer-owned lifecycle before exposing typed state.

`apps/client` preserves the existing `winit` window, renderer ownership and close ordering. Technical login is disabled unless `OTERYN_TECHNICAL_LOGIN=1` and every required endpoint, public OAuth client ID, world ID/host/port, character ID and timeout is explicitly supplied. No endpoint, password, client secret or credential has a production default. Identity/admission completions enter the event loop as generation-tagged user events; bounded `about_to_wait` polling handles completion races without performing browser, listener, HTTP or TCP work on the event-loop thread.

Production `CanaryEntryAdapter` intentionally remains fail-closed before network and credential handoff because exact approved RSA/transcript/deployment evidence is absent. The application reports the resulting typed recoverable failure instead of claiming compatibility.

## Automated fake-service evidence

The workspace tests use only original synthetic values and exact merged producer APIs.

| Scenario | Evidence |
|---|---|
| dynamic callback | fake binder assigns port `49152`; authorization URL and token request use that exact redirect URI |
| strict Identity/Gateway bootstrap | merged `IdentityClient` executes authorization-code exchange, one Game Login Ticket request and one Gateway v1 request against bounded fake HTTP |
| authoritative selection | merged directory validates character `17` belongs to world `9`; focused runtime test rejects an unknown character with `ChooseAnotherCharacter` |
| one credential handoff | merged lifecycle exposes the synthetic credential once and rejects the second handoff as `CredentialAlreadyConsumed` |
| ordered admission | private original marker sequence reaches `0x17 -> 0x1A -> 0xEF -> 0x0A -> 0x0F` before producer-owned `SessionEntered` |
| fresh second attempt | runtime allocates attempt 2 only after attempt 1 is closed and accepts a distinct synthetic credential |
| stale/duplicate callback | merged `AuthorizationTransaction` rejects duplicate completion and mismatched account generation |
| cancellation/close | runtime cancels and joins an active worker, records `SafeCancellation`, then clears through `Closing -> LoggedOut` |
| production fail-closed | merged Canary adapter returns `RealAdmissionUnavailable` while lifecycle remains `CredentialReady`; no network or credential handoff occurs |
| redaction | runtime, worker event, HTTP request and adapter formatting contain no code, access token, ticket or session credential |

Merged Identity security tests additionally cover wrong path/peer/state, malformed or oversized callback, timeout, strict unknown/trailing/oversized Gateway responses, invalid identifiers/ports and world-character relationship failures. Merged Canary tests additionally cover bounded transport/parser errors, denial classifications, timeout, cancellation, abrupt close, expired/consumed/replayed credential and secret-free diagnostics. LOGIN-E2E consumes those exact contracts rather than duplicating public parsers or protocol types.

## Validation

Exact feature head before final evidence/restack: `87ac50efc97b569712276666a30c8d671cc099b1`.

- Rust Client run `30647012485`: success;
  - locked metadata: PASS;
  - `cargo fmt --all --check`: PASS;
  - strict workspace Clippy with `-D warnings`: PASS;
  - all workspace tests and doctests: PASS;
  - architecture policy: PASS;
  - cargo-deny supply chain: PASS.
- repository CI run `30647013322`: success.
- committed `Cargo.lock` retains the pre-existing external resolution, including `xcursor 0.3.10`; only local workspace package entries and dependency edges were generated.
- no temporary workflow remains in the intended final diff.

Final exact-head validation is repeated after the evidence and shared-document commits and before merge.

## Explicit external blockers

### `W7-BLOCK-REAL-RUST-E2E`

No deployed exact Identity, Gateway and Canary revisions, configured public client ID/issuer mapping or fresh controlled credential were available. No real browser return or Rust admission through `0x0F` was run, and no real compatibility claim is made.

### `W7-BLOCK-DEPLOYMENT-EVIDENCE`

Repository access does not prove deployed TLS, DNS, firewall, hostname, secret-manager or runtime revision state. No production-readiness claim is made.

### Interactive Windows observation

Required Windows compilation is proven by CI, and the existing event-loop/renderer ownership is preserved by source and tests. A named interactive desktop observation of the window remaining responsive during configured login was unavailable in the worker environment and is not claimed.

## Exclusions

No map-description decoding, gameplay state, inventory, chat, combat, reconnect/resume, channel switching, general native UI framework, credential persistence, production assets, updater/deployment code, password fallback, private capture or external-repository write is included.
