# Current Parallel Agent Wave

Status: completed and closed  
Wave ID: `OTERYN-W5-RENDER-SURFACE`  
Closure evidence cut: `main` `1bbbf5828d46684a38d5360c63c2d970a64014e1`

Live Git, active tasks and open PRs remain authoritative. This is the durable W5 completion record. **No W1-W5 lane is launchable.** A future wave requires a separate accepted plan and separate plan archive after a fresh preflight.

## 1. Closure result

| Work | Delivery | Delivery merge | Archive | Archive merge | State |
|---|---:|---|---:|---|---|
| W5 plan | PR #84 | `af1de7c9df83b1c736cdfcf6bd1db408dbc9e9e8` | PR #85 | `e9dcf70e8d60bcb5ba3e82280482108d43306f5f` | archived |
| W5-RENDER | PR #86 | `247837ad405a79fe6d9a8d2bc18b86911a2dcefa` | PR #87 | `1bbbf5828d46684a38d5360c63c2d970a64014e1` | archived |

W1, W2, W3, W4 and W5 are completed and must not be relaunched.

## 2. Delivered contract

W5 added exactly one `oteryn-renderer` crate and narrowly composed it into the existing Windows application shell.

It provides:

- typed transactional surface lifecycle keyed by `ProcessGeneration`;
- explicit unconfigured, configured, suspended, lost and closing states;
- zero-size suspension, stale-generation rejection, checked counters, bounded recovery and idempotent close;
- Windows-only safe ownership of wgpu instance, surface, adapter, device and queue;
- one original constant DX12 clear/present path with event-driven redraw;
- exact `wgpu 30.0.0` with default features disabled and only `std` plus `dx12`;
- exact `pollster 1.0.1` for one synchronous main-thread bootstrap;
- fatal renderer failures routed through the existing shell close path;
- renderer resources released before the shell window.

It added no game/map/entity rendering, assets, textures, shader module or pipeline framework, render graph, UI, protocol, identity, networking, audio, persistence, updater or extension runtime.

## 3. Validation evidence

| Evidence | Result |
|---|---|
| PR #86 final head | `cb6042875f51a71cbbd84cd7e6a1af7acad5a4f0` |
| Rust Client run `30470014282` | PASS: locked metadata, formatting, Clippy with warnings denied, all workspace tests, architecture policy and cargo-deny |
| repository run `30470017491` | PASS: all emitted required checks and `CI / Required` job `90638159006` |
| implementation diff | PASS: exactly 15 authorized paths, no final workflow change |
| PR #87 archive run `30474596520` | PASS: `CI / Required` job `90653302895`; Windows build correctly skipped for docs-only scope |
| comments, reviews and unresolved threads | none |

## 4. Compatibility boundaries

Hosted Windows compilation and deterministic tests do not prove:

- visible interactive launch or presentation;
- real resize, minimize, suspend or resume behavior;
- actual surface or device-loss recovery;
- GPU, driver or hardware compatibility;
- minimum supported Windows release;
- frame time, memory, power or other performance targets.

Production asset compatibility and redistribution are also not established. Proprietary or unlicensed game bytes remain forbidden, and production Canary-compatible asset inputs remain blocked on exact source-format and rights evidence.

## 5. Lease and ownership closure

| Path or contract group | Closure state |
|---|---|
| Cargo workspace, lockfile and dependency policy | released by archived W5-RENDER |
| renderer package and public surface contract | merged producer; no active producer task |
| application-shell composition paths | released after renderer merge/archive |
| shared catalogue, matrix, changelog, layout and workspace docs | released |
| architecture checker, rules and fixtures | unchanged; no lease |
| Rust CI and toolchain | unchanged; no lease |
| W5 coordination paths | closure task only until its archive merges |

Open PR #23 owns legacy OTUI/Lua presentation only. PR #48 is isolated operational non-merge work. Neither owns a greenfield Rust package, W5 contract or shared-path lease.

## 6. Exactly one next bounded recommendation

The next package should be planned as a **small normalized synthetic asset schema/compiler slice** under WS-R09.

A future accepted plan must require:

- synthetic or original fixtures only, with no proprietary or unlicensed game bytes;
- typed stable asset identifiers and a bounded metadata/pack schema;
- explicit compiler schema version, provenance/license reference and content hashes;
- deterministic, byte-identical compiler output for identical inputs;
- bounded counts, lengths and offsets, checked arithmetic, deterministic ordering and clear failures;
- path traversal and symlink rejection plus decompression size/ratio limits where applicable;
- exact architecture, workspace, supply-chain and repository CI through one unique future shared-path lease.

That first slice must not include:

- runtime mounting, streaming or cache policy;
- GPU upload, atlas/texture-array strategy or renderer integration;
- a real Tibia/Canary importer or proprietary fixtures;
- downloads, updater, activation or rollback;
- protocol, UI, audio or production-pack compatibility;
- an invented signature/authenticated-manifest design without a separate security decision.

This recommendation is not an accepted wave and is not pre-claimed. A future coordinator must create and merge a separate planning task and its archive before creating a worker task, branch, dependency change or lease.

## 7. Prohibited relaunches

Do not relaunch:

- W1 foundation primitives;
- any W2 implementation or evidence lane;
- W3 deterministic test support;
- W4 planning or Windows application shell;
- W5 planning or renderer surface ownership.

Extend merged contracts only through a new bounded owning task after live authorization.
