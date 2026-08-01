# P0 Staging, E2E and Release Evidence Plan

Status cut: `main@21f0725f0beb46775951dd17f2587c67ebcdee12`  
Lane: `OTC2-20260801-playability-p0-release` / PR #144  
Implementation/deployment authorized: **false**

## 1. Purpose

Define the evidence required to advance the Rust client from the current synthetic technical-login foundation through controlled admission, minimum visible world, daily playability, supported feature parity and a production release candidate.

This plan does not deploy, use an account, select a production endpoint, change CI, choose final product budgets or claim compatibility.

## 2. Current proven baseline

The following repository facts are proven for the current cut:

- Windows x86-64 MSVC is the only required compiled product target.
- Rust `1.94.0` is pinned; `Cargo.lock` is committed.
- `.github/workflows/rust-client.yml` runs locked metadata, rustfmt, strict workspace Clippy, all-target workspace tests and the real workspace architecture checker on `windows-latest`; cargo-deny runs separately on Ubuntu.
- `.github/workflows/ci.yml` provides the repository `CI / Required` gate, but documentation-only PRs do not imply product runtime validation.
- `oteryn-client/tests/integration/technical-login/src/lib.rs` proves an original fake-service flow from dynamic loopback OAuth through ticket, Gateway directory, one-shot credential and synthetic ordered `0x0F` admission, then safe shutdown.
- `oteryn-client/apps/client/src/technical_login_base.rs` exposes an explicit opt-in environment configuration and contains no hidden production defaults.
- `oteryn-client/docs/research/windows-platform/W4_RUNTIME_EVIDENCE.md` proves deterministic shell code/tests and hosted Windows compilation only.
- `oteryn-client/docs/research/renderer/W5_RUNTIME_EVIDENCE.md` proves deterministic surface ownership and hosted Windows compilation only.
- W4/W5 explicitly leave visible launch, real resize/DPI/IME/input, named GPU/driver, surface/device loss and performance unproven.
- W7 stops at technical `SessionEntered`; map/gameplay, native product UI, real asset runtime, launcher/updater and release activation are absent.

A green build is therefore necessary but insufficient for every runtime or release claim below.

## 3. Exact technical-login configuration surface

A controlled M1 run uses the existing explicit opt-in only:

```text
OTERYN_TECHNICAL_LOGIN=1
OTERYN_TECH_AUTHORIZATION_BASE=<approved Identity authorization base>
OTERYN_TECH_GATEWAY_BASE=<approved Platform/Gateway base>
OTERYN_TECH_PUBLIC_CLIENT_ID=<registered public client id>
OTERYN_TECH_WORLD_ID=<authoritative Platform world id>
OTERYN_TECH_WORLD_HOST=<authoritative Gateway-returned/approved Canary host>
OTERYN_TECH_WORLD_PORT=<authoritative Canary port>
OTERYN_TECH_CHARACTER_ID=<approved test character id>
OTERYN_TECH_CALLBACK_TIMEOUT_SECS=<positive owner-approved value>
OTERYN_TECH_HTTP_TIMEOUT_SECS=<positive owner-approved value>
OTERYN_TECH_CONNECT_TIMEOUT_SECS=<positive owner-approved value>
OTERYN_TECH_READ_TIMEOUT_SECS=<positive owner-approved value>
OTERYN_TECH_WRITE_TIMEOUT_SECS=<positive owner-approved value>
```

Configuration is supplied out of band by the controlled test operator. It must not be committed, printed in CI, attached to a PR or copied into screenshots/support bundles.

## 4. Producer revision gate

Before any real compatibility run, record in one evidence manifest:

- exact Oteryn Identity/Platform repository and commit;
- exact Game Login Ticket and Gateway protocol-v1 producer commits;
- exact Canary repository commit, release/build and `ProtocolProfileId`;
- exact deployed configuration revision and environment identifier;
- exact Rust client commit and signed/hashed build artifact;
- exact asset pack/import cut when the scenario reaches M2 or later.

Historical W7 documentation names Platform merges `27fa277c5def0e151d7ee013acef188dbfd6f463`, `cab00c140ce200e3cd51b7eafe2c1659842c2b90`, `8006534108d835474dadd208b0ec934e4a12528b` and `53158217a6c6017230301cf4daa783b04fcc13d5`, plus Canary producer merges `b8a88f073b2609b444fa15370aae30ac9f80b908` and `981c82f5ebb6bc22c867312c2b274a71f6aeeb3e`.

The same documents contain different historical Canary source cuts (`4b2d6f...` in the architecture plan and `95b276...` in current workspace operations). Neither is accepted as the live compatibility cut by this report. PR #140 must resolve the exact producer revision and source paths before M1 admission or later protocol claims.

## 5. Evidence handling and privacy

### Committable

- exact public repository commit SHAs and source paths;
- sanitized scenario manifests with opaque environment/account labels;
- stable client/server result codes and timestamps;
- aggregate packet/message-family counts without payload bytes;
- redacted screenshots containing no account, character-private data, tokens or endpoints not approved for publication;
- hashes of approved build artifacts and fixtures;
- pass/fail tables and summarized performance distributions.

### Artifact-only or restricted

- full client/server logs after automated redaction review;
- screenshots/video from private staging;
- packet captures from a project-owned controlled environment;
- crash dumps, GPU traces and support bundles;
- installer/update packages and private synthetic fixture corpora.

### Never stored in Git or ordinary CI logs

- OAuth codes, verifier/state, access/refresh tokens;
- Game Login Tickets or Game Session credentials;
- XTEA/session keys or sensitive frames;
- private service credentials, account cookies or passwords;
- proprietary game/assets bytes or unapproved captures;
- production hostnames/addresses classified as private.

Every artifact has an owner, retention period, access boundary, redaction result and deletion procedure.

## 6. M1 — controlled real technical login

### Start state

- exact client and producer cuts are recorded;
- a project-owned non-production environment is healthy and isolated from production mutation;
- an approved disposable test account and character exist;
- no outstanding one-shot credential or active game session exists;
- system time, DNS, TLS chain, firewall and browser policy are known;
- the Windows client starts from a clean process with explicit configuration;
- client and server evidence capture is armed before login without secret logging.

### Sequence

1. Start the signed/hashed exact Windows build with the explicit opt-in configuration.
2. Observe one window/renderer initialization and public `LoggedOut` state.
3. Start native authorization; verify the loopback listener binds before browser launch.
4. Complete authorization in the system browser and return to the exact dynamic IPv4 loopback callback path.
5. Verify one code exchange, one Game Login Ticket issuance and one Gateway `/v1/login` request.
6. Verify the authoritative directory contains the configured world and selected character relationship.
7. Hand one fresh credential to the Current-profile adapter exactly once.
8. Observe server-side credential acceptance/consumption and client-side typed admission result.
9. Reach ordered `SessionEntered`, then disconnect cleanly before map processing.
10. Attempt replay or reuse only through an approved negative scenario using a separately controlled disposable credential; verify rejection and no silent fallback.
11. Close the client and prove workers/sockets/listener terminate before renderer/window teardown.

### Required observables

- browser launch and callback on a named Windows desktop session;
- exact callback address/port/path as sanitized metadata;
- TLS hostname/certificate success for non-loopback services;
- one request count for token, ticket and Gateway stages;
- stable client phase transitions and terminal action;
- server-side correlation proving exactly one admission attempt/credential consumption;
- no credential or raw producer error text in diagnostics, UI title, logs or artifacts;
- clean disconnect and zero surviving client process/worker/socket/listener.

### Positive result

M1 passes only when client and server evidence agree on one controlled admission and teardown for the same exact cuts.

### Required negative scenarios

- wrong callback path/state/peer or duplicate callback;
- expired/consumed/wrong-character/wrong-profile credential;
- DNS/TLS/firewall failure;
- timeout before credential handoff versus uncertain failure after handoff;
- cancellation and process close during Identity and admission stages;
- server restart invalidating an outstanding credential;
- replay rejection without password fallback or hidden retry.

## 7. M2 — minimum visible world

### Start state

M1 is proven for the same supported producer family. PR #140 has accepted exact map/bootstrap protocol evidence. The asset lane has an approved source/import decision and a verified runtime pack. The P1 game-domain, snapshot, asset-runtime, input-action and renderer contracts are merged.

### Sequence

```text
clean launch
-> controlled login and character selection
-> admission
-> map bootstrap
-> stable world snapshot
-> resolve approved appearances
-> render floors/tiles/items/local character/basic creatures/effects
-> issue semantic movement/camera action
-> observe server movement/reconciliation
-> logout/disconnect
```

### Required observables

- exact map/bootstrap message-family evidence and deterministic decode result;
- one authoritative simulation writer and generation-stable snapshot;
- verified pack identity and no loose arbitrary runtime source access;
- visible named test scene on a named Windows/GPU/driver session;
- movement command/event correlation and final server-authoritative position;
- no blocking network/filesystem/decode work on frame-critical paths;
- clean return to selection/logged-out state.

M2 is the first milestone allowed to claim `playable`, limited to the exact vertical slice.

## 8. M3 — core gameplay loop

M3 uses a scenario catalogue accepted from PR #141 and exact protocol support accepted from PR #140.

Required controlled scenarios cover:

- creature appearance, movement, health, conditions, effects and death;
- look/use/move item;
- inventory, equipment, containers and drag/drop;
- public/private/NPC chat where supported;
- attack/follow, battle list and combat feedback;
- skills, stats, cooldowns and status bars;
- hotkeys/action bindings and basic settings;
- required audio feedback;
- logout, process restart, relog and fresh-credential policy.

Each scenario records start state, exact fixture/server cut, actions, domain events/commands, user-observable outcome, negative/recovery path and privacy-safe evidence. M3 requires repeated scenario runs and a bounded soak; unit/packet tests alone do not pass it.

## 9. M4 — daily-playable product

Required product evidence adds:

- native login/selection and recoverable error UX;
- stable viewport/HUD/panels/docking/layout persistence;
- DPI/multi-monitor, focus, IME, clipboard, keyboard-only and accessibility checks;
- minimap/social/party/guild/channel features supported by the selected profile;
- typed settings and migration tests;
- audio device replacement/recovery and category controls;
- launcher install/repair/update/rollback rehearsal;
- crash-safe diagnostics/support-bundle privacy review;
- named hardware performance distributions;
- multi-hour staging play without material leak, deadlock, queue growth or protocol drift.

A successful developer session is not daily-playable acceptance. Evidence must use an install-like build and clean user profile.

## 10. M5 — supported feature parity

The aggregation barrier must classify each capability row as release-required, later or owner-decision-needed for one exact Oteryn/Canary profile.

For every release-required feature:

- a sole client contract owner exists;
- server capability and exact protocol evidence are recorded;
- domain/protocol/UI boundaries remain separated;
- positive and negative automated tests pass;
- one controlled staging scenario passes;
- localization, accessibility, privacy and recoverable errors are covered;
- no undocumented legacy runtime dependency exists.

M5 passes only when no release-required row remains `ABSENT`, `UNKNOWN` or `BLOCKED`.

## 11. M6 — production release candidate

### Required dependency order

1. approved asset provenance/import/redistribution decision;
2. immutable verified/signable pack contract;
3. launcher/install/uninstall/repair contract;
4. authenticated update manifest and download verification;
5. atomic activation and rollback;
6. client and package signing/notarization policy appropriate to Windows;
7. release-channel/profile compatibility negotiation;
8. diagnostics/privacy/support and incident procedures;
9. security, parser fuzzing, dependency and threat-model closure;
10. named Windows/GPU/driver performance and long-soak matrix;
11. representative release-candidate playthrough and rollback rehearsal.

### Clean-install/update matrix

For each supported Windows target and channel:

- clean install to a clean user profile;
- first launch with no stale cache/settings;
- signed client/pack verification;
- upgrade from the previous supported release;
- interrupted download and interrupted activation;
- corrupted/tampered manifest/archive/pack rejection;
- repair of missing/corrupted content;
- rollback after health-check failure;
- uninstall and user-data retention/deletion decision;
- offline/error UX and support bundle.

### Release acceptance

M6 requires an owner-approved release manifest naming every artifact hash, producer/client/profile cut, supported platform matrix, known limitation, rollback target and evidence index. No release is activated solely because CI is green.

## 12. Windows acceptance candidates

The final support matrix is an owner/product decision. Discovery must collect at least:

- candidate minimum and current Windows desktop releases;
- native desktop versus VM/remote-session behavior;
- single- and multi-monitor DPI modes;
- representative integrated and discrete GPU/driver classes;
- keyboard/mouse layouts, IME and clipboard;
- audio default device and replacement;
- firewall/browser policies for dynamic loopback;
- install location, standard-user privileges and controlled elevation boundaries.

The GitHub-hosted Windows Server runner is build/test evidence only and must not be listed as a supported desktop configuration.

## 13. External blockers and owner decisions

| Item | Current state | Required resolution |
|---|---|---|
| exact Canary current producer cut | BLOCKED by conflicting historical cuts | PR #140 names one exact supported revision/profile/build |
| approved staging environment | UNKNOWN | owner names environment, access policy and allowed mutations |
| approved test account/character | UNKNOWN | owner/security supplies disposable controlled identity out of band |
| final Windows support matrix | UNKNOWN | product owner selects supported releases/hardware classes after evidence |
| product performance budgets | UNKNOWN | owner accepts thresholds after baseline scenes and measurements |
| production asset source/rights | UNKNOWN | PR #142 plus legal/owner decision |
| telemetry/support data policy | UNKNOWN | privacy/security owner decision |
| signing credentials and release channel | UNKNOWN | release/security owner decision and protected process |

## 14. P0 output boundary

This document is an evidence contract. It authorizes no deployment, credential use, workflow addition, packaging implementation, product budget or release activation.
