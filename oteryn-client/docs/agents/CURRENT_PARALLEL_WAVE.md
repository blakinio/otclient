# Current Parallel Agent Wave

Status: completed and closed  
Wave ID: `OTERYN-W2-DIAGNOSTICS-EVIDENCE`  
Closure evidence cut: `main` `140d83670face0fef1219c43d7d186783d0c57da`

Live Git, active task records and open PRs remain authoritative. This document is the durable completion record for W2. **No lane in this document is launchable.** A later parallel wave requires a new accepted plan after a fresh preflight.

## 1. Closure result

W2 completed one bounded Gate 1 implementation package and three isolated evidence packages. Every delivery received a separate lifecycle archive PR. No W2 task, public-contract claim or shared-path lease remains active.

| Lane | Delivery | Delivery merge | Archive | Archive merge | Final state |
|---|---:|---|---:|---|---|
| W2-DIAG | PR #61 | `6d0c5ce243e62ff1e5b548a626c3f5e228506717` | PR #62 | `9b5c86dff694aa65f4b264683f9c5ce3bf000035` | archived |
| W2-CP | PR #63 | `68567dbb118a3b3f2e420b62f5360979f461a725` | PR #64 | `a6c8d1cfcac9364612c2ac56a9dc12618581adc9` | archived |
| W2-AR | PR #65 | `39138bb6673be070878225b4f872121ae5d39a6c` | PR #66 | `048414f9457f6adaf6c3f94f8a8e6b92d624389d` | archived |
| W2-PR | PR #67 | `e7d9b5d5feb53debd79c4bdc82da16ca672217c5` | PR #68 | `140d83670face0fef1219c43d7d186783d0c57da` | archived |

W1-F remains archived and is also not launchable.

## 2. Delivered implementation contract

W2-DIAG added exactly one `oteryn-diagnostics` crate. Its merged contract provides:

- stable structured severity/category/code and technical correlation values;
- reviewed static safe text and lower-snake-case keys with fixed bounds;
- explicit sensitive classifications and redaction at value creation without retaining source text;
- deterministic technical context using merged foundation time/generation primitives;
- bounded events with at most 16 unique fields;
- compile-fail and synthetic secret-shaped redaction regression evidence.

It did not add a global logger/subscriber, sink, upload, crash reporting, support bundles, replay, async runtime, protocol, authentication, assets, renderer, UI or authoritative state.

## 3. Merged evidence

### Canary Current profile

`oteryn-client/docs/research/canary-current/**` records:

- Current compatibility as an exact producer revision/profile/transport/login/feature/build tuple, not only version 15.25;
- a provenance-first synthetic fixture acquisition manifest;
- response-local login-list world indexing as distinct from Canary process/channel, Platform world and product `WorldChannelId` concepts;
- the current native-auth v1 limitation to one configured Platform world and one exact process-local Canary issuer;
- protocol implementation remaining blocked until exact producer coordination and fixtures exist.

### Asset inputs and provenance

`oteryn-client/docs/research/asset-inputs/**` records:

- technical availability/local installation/download as insufficient redistribution permission;
- asset-specific rights/provenance requirements rather than extending the repository MIT license to unrelated content;
- a deterministic content-free inventory schema;
- a hostile-input importer threat checklist;
- one original synthetic 4×4 sprite-sheet/compiler slice without official/legacy assets or a production pack ABI.

### Windows platform foundation

`oteryn-client/docs/research/windows-platform/**` records:

- main-thread event-loop/window/DPI/IME/lifecycle ownership;
- `winit 0.30.13` as a future spike candidate, not an accepted production dependency;
- `raw-window-handle 0.6.2` as interop-only unless a later renderer boundary needs it;
- direct Win32 work deferred until a measured gap and focused unsafe/FFI review;
- exact Windows release, DPI, IME and device compatibility remaining blocked on named runtime evidence;
- one bounded blank-window application-shell recommendation.

## 4. Lease and ownership closure

| Path/contract group | W2 closure state |
|---|---|
| Cargo workspace/lockfile | released by archived W2-DIAG |
| diagnostics crate/public contract | merged producer; no active producer task |
| architecture checker/fixtures | unchanged; no lease |
| Rust CI/toolchain/deny policy | unchanged; no lease |
| Canary research path | merged and archived; unclaimed |
| asset research path | merged and archived; unclaimed |
| Windows research path | merged and archived; unclaimed |
| W2 coordination paths | closure task only until its archive merges |

Open PRs #23 and #37 own legacy UI/asset paths. PR #48 is an isolated non-merge operational workflow. They do not own a greenfield Rust package, W2 evidence path or Cargo integration lease.

## 5. Exactly one next bounded recommendation

The next package should be **deterministic Rust test support and fake-time helpers**.

Required envelope:

- one small test-support package only;
- consume `oteryn_foundation::ManualClock` and merged `oteryn-diagnostics` contracts;
- provide test-owned deterministic fixtures/builders and fake-time orchestration;
- do not create a second clock abstraction;
- no async runtime, executor, scheduler, product service, global test registry or runtime integration;
- obtain one unique Cargo/lockfile/shared-document lease after a fresh live preflight;
- pass exact Windows workspace, architecture, supply-chain and repository CI.

Rationale:

- this follows the accepted Gate 1 order after structured diagnostics;
- deterministic test support strengthens later application, asset and domain work without freezing product contracts;
- the Windows and asset evidence packages are ready for later bounded implementation waves;
- protocol implementation remains blocked on exact producer coordination and the reviewed fixture corpus.

This recommendation is not an accepted new wave and is not pre-claimed. A future coordinator must create a separate task/plan after checking current Git, tasks, PRs, contracts and shared-path leases.

## 6. Prohibited relaunches

Do not relaunch:

- W1-F foundation primitives;
- W2-DIAG diagnostics foundation;
- W2-CP Canary Current evidence;
- W2-AR asset input evidence;
- W2-PR Windows platform evidence.

Extend merged contracts/evidence through a new bounded owning task only when live state authorizes it.
