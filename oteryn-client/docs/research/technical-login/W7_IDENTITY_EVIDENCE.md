# W7 Identity Evidence

Status: deterministic Rust implementation and synthetic fake-service evidence complete; real deployed compatibility remains blocked

## Exact revisions

- Oteryn client launch base: `626c7954e6e6999bb4b8c8d051500b543e3c09e0`
- W7-ENTRY-CONTRACT merge: `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`
- W7-ENTRY-CONTRACT archive: `8dcd353d5a9f19fabccf49508c27074f7749e3cf`
- workspace membership repair: `9e580a0fa615cc0e42f70c9d76395cf5a9fd0238`
- workspace repair archive / Identity base: `626c7954e6e6999bb4b8c8d051500b543e3c09e0`
- inspected Oteryn Platform head: `55ba8840a7de6556b6b173f587179f986a5a68e1`
- native OAuth producer merge: `27fa277c5def0e151d7ee013acef188dbfd6f463`
- Game Login Ticket producer merge: `cab00c140ce200e3cd51b7eafe2c1659842c2b90`
- Game Gateway protocol-v1 producer merge: `8006534108d835474dadd208b0ec934e4a12528b`
- native-auth hardening merge: `53158217a6c6017230301cf4daa783b04fcc13d5`

The Platform head advanced from the planning cut only in UX, portal and testing paths. No inspected OAuth, ticket or Gateway contract path changed.

## Delivered scope

### `oteryn-platform`

The crate terminates raw OAuth, ticket and Gateway DTOs and converts a successful Gateway result only into merged ENTRY contracts.

Implemented boundaries:

- explicit Identity and Gateway base URLs;
- HTTPS required outside loopback;
- no URL credentials, query, fragment or hidden non-root base path;
- blocking HTTPS adapter with platform-native certificate and hostname validation;
- no redirect following, environment proxy use or automatic request retry;
- bounded global timeout, response headers and response body;
- exact authorization-code token exchange form;
- exact Game Login Ticket request;
- exact Gateway protocol-v1 request;
- strict JSON with unknown-field and trailing-data rejection;
- required `application/json` and no-store/no-cache response policy;
- signed-64 identifier preservation, bounded strings and positive TCP ports;
- duplicate world/character identifier and character/world relationship rejection through the merged directory constructor;
- bounded future session expiry;
- conversion to `AccountDirectorySnapshot` and `GameEntryCredential` only.

### `oteryn-identity`

The crate owns one synchronous native authorization transaction suitable for execution on an application-owned worker thread.

Implemented behavior:

1. verify the active `AccountSessionId` generation and cancellation state;
2. bind IPv4 `127.0.0.1:0` before launching the browser;
3. generate independent CSPRNG state and verifier values;
4. derive PKCE `S256` using base64url without padding;
5. launch the system browser with one direct process argument and no shell interpolation;
6. receive one bounded HTTP callback request;
7. validate IPv4 loopback peer, exact `/callback`, state, required fields, uniqueness, active generation and duplicate-use state;
8. exchange the authorization code with the exact redirect and verifier;
9. discard the W7 refresh token and use the access token only for one ticket issuance;
10. perform one non-retried Gateway login and return the merged directory plus one fresh credential;
11. reject stale completions and clear secret-bearing values on every terminal drop path.

No Oteryn or Canary password is collected, stored or used. There is no legacy fallback, embedded browser, async runtime, global singleton, credential persistence or Canary protocol implementation.

## Exact producer surface consumed

- authorization endpoint: `/oauth/authorize`
- token endpoint: `/oauth/token`
- OAuth scope: `game:ticket`
- registered redirect base: `http://127.0.0.1/callback`
- dynamic redirect used by the client: `http://127.0.0.1:<OS-assigned-port>/callback`
- ticket endpoint: `POST /api/v1/game-auth/tickets`
- ticket body: `{"protocol_version":1}`
- Gateway endpoint: `POST /v1/login`
- Gateway body: `{"protocol_version":1,"game_login_ticket":"..."}`
- Gateway result: `protocol_version`, `session { credential, expires_at }`, `worlds[] { id, slug, name, region, host, port }`, `characters[] { id, name, level, vocation, world_id }`

No directory revision, gameplay-channel identifier, issuer directory or general multi-world routing field is inferred. `DirectoryRevision` remains client-local and `GameplayChannelId` remains unused/unserialized in W7.

## Secret and error properties

- state, verifier, authorization code, access token, refresh token, Game Login Ticket and Game Session credential have no ordinary clone or serialization surface;
- secret wrappers redact `Debug` and `Display` and overwrite owned bytes on drop as a best-effort safe-Rust cleanup barrier;
- request and response debug output redacts bearer and body material;
- stable errors contain no raw backend body, URL secret, OS text or producer credential;
- sensitive responses must be no-store/no-cache;
- a Game Login Ticket request is never automatically retried because issuance revokes the associated OAuth token family;
- a Gateway request is not replayed after uncertain completion;
- cancellation and generation checks occur before side effects and between each one-shot stage.

## Automated evidence

The workspace tests cover:

- RFC 7636 PKCE `S256` known vector;
- independent state and verifier/challenge material;
- listener bind before browser launch;
- actual dynamic loopback port propagation into authorization and token exchange;
- one synthetic browser/listener/HTTP success path with exactly three HTTP requests;
- callback state mismatch, wrong peer, wrong path, stale generation, duplicate callback, duplicate parameter and unknown parameter rejection;
- callback timeout and cancellation before further side effects;
- unknown and trailing JSON, uncontracted redirect and missing cache-policy rejection;
- oversized sensitive response rejection;
- unsupported Gateway protocol version;
- duplicate world IDs, invalid port and unknown character/world relation;
- stale generation without network work;
- access, ticket, code and credential redaction in debug output;
- conversion only into the merged ENTRY directory and credential types.

All fixtures are synthetic and contain no account, production endpoint, private capture, proprietary asset or reusable credential.

## Dependency and supply-chain review

New exact dependencies are minimal and pinned in `Cargo.lock`:

- `base64` for RFC-compatible base64url without padding;
- `getrandom` for operating-system CSPRNG bytes;
- `serde` and existing workspace `serde_json` for strict bounded DTO parsing;
- `time` for RFC 3339 session expiry parsing;
- `url` for exact URL construction and validation;
- `ureq` with `native-tls-no-default` for a bounded synchronous adapter.

The production HTTP adapter selects `NativeTls` and `PlatformVerifier`, preserving the operating system certificate store and hostname verification. Automatic redirects and proxy environment discovery are disabled.

`deny.toml` records one exact Windows-only generated-binding split: existing `winit` uses `windows-sys 0.52`, while reviewed SChannel/native-tls uses `windows-sys 0.61.2`. No wildcard, Git dependency, unknown registry, unreviewed license or advisory exception was introduced.

`Cargo.lock` was generated through Cargo `1.94.0`; it was not manually conflict-resolved.

## Validation

Final exact-head validation evidence is recorded in the active task and PR after the final documentation commit. Required gates are:

- `cargo metadata --locked --format-version 1`;
- `cargo fmt --all -- --check`;
- strict workspace Clippy with all targets and features;
- all workspace tests and doctests;
- architecture policy validation;
- cargo-deny advisories, licenses, bans and sources;
- repository `CI / Required`;
- complete diff and review-thread inspection.

## Blocked claims

The following remain explicitly blocked and are not represented as implementation proof:

- exact deployed public OAuth `client_id`;
- exact deployed Identity and Gateway URLs;
- deployed TLS certificate, DNS, firewall, reverse-proxy and secret-injection state;
- interactive Windows system-browser launch and return against a real configured producer;
- exact deployed Platform/Gateway revision reachability;
- real Rust Identity -> Gateway -> Canary end-to-end compatibility;
- reusable account-session, relog or channel-switch behavior after ticket issuance;
- general multi-world issuer or gameplay-channel routing;
- production rollout readiness.

These deployment gaps block only real-path compatibility claims. They do not weaken or invalidate the deterministic implementation and fake-service evidence above.
