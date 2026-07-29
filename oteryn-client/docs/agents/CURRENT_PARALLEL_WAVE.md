# Current Parallel Agent Wave

Status: completed and closed  
Wave ID: `OTERYN-W4-WINDOWS-SHELL`  
Closure evidence cut: `main` `ab0ac39ca70ccea6d8f7517f4119395de6b17017`

Live Git, active tasks and open PRs remain authoritative. This is the durable W4 completion record. **No W4 lane is launchable.** A future wave requires a separate accepted plan after a fresh preflight.

## 1. Closure result

| Work | Delivery | Delivery merge | Archive | Archive merge | State |
|---|---:|---|---:|---|---|
| W4 plan | PR #77 | `7ff7a80df15dd22178c3a1920cc3714216c91ac6` | PR #78 | `b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3` | archived |
| W4-SHELL | PR #79 | `00ad2729aab3696ca4571fd718ef1b350747e3b5` | PR #80 | `ab0ac39ca70ccea6d8f7517f4119395de6b17017` | archived |

W1, W2, W3 and W4 are completed and must not be relaunched.

## 2. Delivered contract

W4 added exactly one `oteryn-client` application package with architecture category `app` and exact direct dependency `winit 0.30.13`.

It provides:

- deterministic `ShellState`, `ShellPhase`, `ShellCommand`, `ShellError` and `WindowSnapshot` contracts;
- typed process-generation ownership and transactional stale-generation rejection;
- bounded command batches and bounded structured lifecycle diagnostics;
- deterministic startup, running, closing and exited phases with idempotent close/exit;
- one main-thread `winit::ApplicationHandler` creating one resizable blank window and enabling IME;
- one named one-shot proxy-wake thread joined after the event loop returns;
- explicit runtime evidence separating automated `PASS` from interactive `BLOCKED` cases.

It added no renderer/GPU surface, shader/render loop, direct Win32/windows-sys/raw-window-handle dependency, unsafe code, async runtime, protocol, identity, networking, assets, audio, feature UI, settings, persistence or updater.

## 3. Validation evidence

| Evidence | Result |
|---|---|
| PR #79 final Rust Client run `30443538715` | PASS: Windows workspace and Supply Chain |
| PR #79 final repository run `30443539114` | PASS: all required jobs and `CI / Required` |
| PR #79 ready-for-review run `30443666077` | PASS: all emitted required jobs and `CI / Required` |
| PR #80 lifecycle run `30443960356` | PASS: `CI / Required` |
| PR #80 ready-for-review run `30444085019` | PASS: all emitted required jobs and `CI / Required` |

Named compile/test runner evidence:

```text
Microsoft Windows Server 2025 Datacenter
OS 10.0.26100
runner image windows-2025-vs2026
image version 20260714.173.1
```

## 4. Compatibility boundaries

The following remain unproven and must not be presented as compatible:

- visible interactive launch/close and real window-manager resize/minimize/restore;
- multi-monitor DPI transitions;
- physical keyboard/mouse/cursor/wheel input;
- real IME enable/composition/commit/disable behavior;
- logoff/shutdown session-ending order;
- minimum supported Windows release;
- GPU/driver/device-loss and renderer-surface behavior;
- frame time, memory, power or other performance targets.

Hosted Windows compilation and deterministic tests are not interactive runtime proof.

## 5. Lease and ownership closure

| Path/contract group | Closure state |
|---|---|
| Cargo workspace/lockfile/dependency policy | released by archived W4-SHELL |
| application package/public shell contract | merged producer; no active producer task |
| catalogue/matrix/changelog/layout/workspace docs | released after closure catalogue correction |
| architecture checker/rules/fixtures | unchanged; no lease |
| Rust CI/toolchain | unchanged; no lease |
| W4 coordination paths | closure task only until its archive merges |

Open PRs #23 and #37 own legacy paths. PR #48 is isolated operational non-merge work. They own no greenfield Rust package or W4 lease.

## 6. Exactly one next bounded recommendation

The next package should be a **renderer surface-ownership evidence/spike** consuming the merged application-shell contract.

Required envelope:

- preserve main-thread window ownership and deterministic shell shutdown;
- establish only renderer instance, adapter, device, queue and surface ownership plus clear/present lifecycle with original synthetic content;
- perform fresh primary-source dependency version, license, MSRV, advisory and source review before Cargo changes;
- no game/map/entity rendering, texture or asset pipeline, shader framework, UI, protocol, identity, networking, audio, persistence or extension runtime;
- no global renderer singleton, hidden background service or scheduler;
- deterministic CPU-side state tests for unconfigured/configured/suspended/lost/closing states, zero-size handling and device/surface loss policy;
- mark interactive GPU, driver, hardware and performance evidence `BLOCKED` unless genuinely observed on a named environment;
- use one unique Cargo/lockfile/dependency-policy/shared-document lease through a separate accepted wave.

This recommendation is not an accepted wave and is not pre-claimed. A future coordinator must create a separate plan task and merge its plan plus archive before creating a worker branch or lease.

## 7. Prohibited relaunches

Do not relaunch:

- W1 foundation primitives;
- any W2 implementation/evidence lane;
- W3 deterministic test support;
- W4 planning;
- W4-SHELL Windows application shell.

Extend merged contracts only through a new bounded owning task after live authorization.
