# P0 Performance and Reliability Acceptance

Status cut: `main@21f0725f0beb46775951dd17f2587c67ebcdee12`  
Lane: `OTC2-20260801-playability-p0-release` / PR #144  
Final product budgets selected: **no**

## 1. Purpose

Define a repeatable evidence method for frame performance, startup/login/world-entry latency, memory/resource stability, network degradation, device loss, repeated lifecycle and multi-hour play without turning preliminary engineering targets into unsupported product claims.

This document extends `oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md`. That architecture remains normative.

## 2. Current evidence boundary

Current repository automation proves compilation, deterministic tests, dependency policy and architecture only:

- `Rust Client / Windows` uses hosted Windows, pinned Rust `1.94.0`, locked metadata, rustfmt, strict Clippy, all-target workspace tests and architecture validation.
- cargo-deny proves the reviewed dependency graph; it does not prove runtime performance.
- W4 shell evidence has no accepted visible interactive desktop observation.
- W5 renderer evidence has no accepted visible present, physical resize/DPI, named GPU/driver, device-loss or frame-time observation.
- no world scene, asset runtime, gameplay protocol stream, native product UI, audio runtime, replay harness or production package exists.

Therefore no current build has a valid gameplay FPS, memory, startup, soak or product reliability claim.

## 3. Measurement record

Every result must record:

```text
client commit and build profile
Rust/toolchain and relevant dependency versions
producer/profile/build revision or replay fixture revision
asset pack/import revision
Windows edition/build and session type
CPU, GPU, driver, RAM and storage class
monitor resolution, scale and refresh rate
power mode and foreground/background state
scene/scenario identifier and start state
warm-up policy, sample duration and repetition count
diagnostics/profiling configuration
raw artifact location and privacy classification
```

A result missing any material field is diagnostic evidence only, not an acceptance result.

## 4. Hardware/support tiers

Use three labels until the product owner selects exact machines:

- `minimum-candidate` — lowest desktop configuration being evaluated;
- `recommended-candidate` — mainstream target configuration;
- `high-refresh-candidate` — configuration evaluated for 144–240 Hz presentation.

Do not attach concrete CPU/GPU models to these labels without an owner-approved support-matrix task. Hosted Windows Server CI is not one of the tiers.

For each selected tier, record at least one integrated-GPU class and one discrete-GPU class where product scope requires both. VM and remote-session results are separate categories and cannot substitute for native desktop evidence.

## 5. Timing metrics

### Frame path

Capture distributions, not only averages:

- simulation/domain update;
- protocol event application;
- world extraction/culling/batching CPU;
- UI update/layout/extraction;
- main-thread orchestration excluding intentional wait;
- total CPU frame work;
- GPU frame time and present result;
- asset decode/upload work and resulting frame impact;
- queue depths/backlogs and saturation events.

Report median, p95, p99, worst relevant sample, sample count and stutter-event classification. Average FPS alone is invalid evidence.

### Lifecycle latency

Measure separately:

- cold process start to visible window;
- window to usable login presentation;
- authorization start to browser launch;
- callback to directory-ready;
- selection to TCP connect;
- connect to technical admission;
- admission to first stable world snapshot;
- first snapshot to first complete rendered frame;
- logout/disconnect to safe selection/logged-out state;
- clean shutdown to process exit;
- clean install/update/repair/rollback durations.

Do not merge network/server time and local client time into one unexplained number.

## 6. Preliminary architecture targets

`PERFORMANCE_AND_TESTING.md` contains initial recommended-tier engineering targets, including a 144 Hz total CPU frame-work target of `<= 5.5 ms p95` and GPU frame target of `<= 6.0 ms p95`, plus component targets.

These values are retained as design hypotheses only. They become release gates only after:

1. the minimum scenes and instrumentation exist;
2. measurements are stable on named candidate hardware;
3. product ownership accepts the target refresh/resolution;
4. noise and regression thresholds are characterized;
5. the accepted values are recorded in a focused budget decision/ADR.

Until then, reports show measured distributions and variance without declaring pass/fail against these numbers.

## 7. Reproducible scene catalogue

Each scene must be legally reproducible using project-owned synthetic, approved imported or normalized replay inputs.

| Scene | Required stress |
|---|---|
| `empty-light-map` | baseline map, camera and minimal UI |
| `dense-town` | players/outfits/labels, panels, mixed static/dynamic appearances |
| `heavy-combat` | creatures, movement, effects, projectiles, text and cooldown feedback |
| `inventory-containers` | many items, nested windows, drag/drop and battle list activity |
| `chat-ui-volume` | channel/private/NPC messages, virtualization and text shaping |
| `fast-map-stream` | rapid movement, floor changes, cache misses and bounded asset streaming |
| `relog-cycle` | repeated login/selection/session/logout with fresh credentials |
| `snapshot-recovery` | reconnect/full snapshot or approved recovery contract |
| `window-device` | resize, minimize/restore, DPI move, suspend/resume and device-loss paths |
| `long-soak` | representative normal play across protocol/UI/assets/audio |

Every scene has a versioned manifest, deterministic seed where applicable, expected entity/resource/message ranges and a hashable evidence identity.

## 8. Memory and resource evidence

Track at minimum:

- process working set/private bytes;
- committed virtual memory where available;
- CPU decoded asset cache;
- GPU textures/buffers and allocation failures;
- mutable game/domain state;
- transient frame arenas;
- UI tree, text/glyph and layout caches;
- protocol/replay/diagnostic buffers;
- worker/thread/socket/handle counts;
- queued async decode/upload work;
- settings, support and crash artifact growth.

### Required method

1. Record clean-start baseline.
2. Warm the exact scenario until expected caches stabilize.
3. Record steady-state samples.
4. Execute bounded stress/repetition.
5. Return to an equivalent idle/logged-out state.
6. Record post-cycle samples and retained owners.
7. Repeat enough cycles to distinguish one-time cache growth from sustained growth.

Acceptance requires bounded growth consistent with declared caches and release budgets. A monotonic leak slope, growing task/socket/handle count, unbounded queue or resources surviving terminal teardown is a failure even when the process remains responsive.

Exact byte budgets are owner decisions after asset and scene evidence from PR #142 and later implementation.

## 9. Network degradation matrix

The test harness must apply named profiles rather than informal Wi-Fi descriptions. Each profile records:

- baseline RTT and jitter distribution;
- added delay/jitter;
- loss, duplication and reordering policy compatible with the transport/protocol model;
- bandwidth/queue constraints where relevant;
- outage duration and restoration point;
- whether failure occurs before or after one-shot credential handoff.

Required scenarios:

- slow DNS resolution/failure before connect;
- TCP connect timeout/refusal;
- TLS/HTTP delay and timeout during Identity/Gateway;
- callback timeout/cancellation;
- partial reads/writes and abrupt close;
- latency/jitter during normal movement/combat/chat;
- temporary packet loss/outage;
- long outage requiring fresh session policy;
- disconnect during map bootstrap, asset load and ordinary play;
- uncertain post-write failure where credential replay is forbidden.

Product thresholds are not selected in P0. Later tasks choose profiles and acceptance based on measured user impact and server protocol semantics.

## 10. Lifecycle and soak scenarios

### Repeated lifecycle

Run controlled loops for:

```text
launch -> login -> admission -> logout -> close
launch -> login -> cancel before callback -> close
launch -> login -> cancel after directory -> close
launch -> admission failure -> fresh login -> successful entry -> logout
session -> disconnect -> approved recovery/relog -> logout
```

For every iteration prove:

- no stale-generation completion changes active state;
- no credential, listener, socket, thread or worker is reused incorrectly;
- terminal owners drop and resource counts return to their expected bounded baseline;
- settings/cache evolution is deterministic and migration-safe;
- server session/credential state matches client claims.

### Multi-hour soak

The soak uses a representative mix of movement, map changes, combat, containers, chat, panels, audio and periodic relog/recovery once those features exist.

Capture:

- frame distributions by interval;
- memory/cache/resource counts by interval;
- protocol and worker queue depth;
- error/recovery counts;
- GPU/driver reset or device-loss events;
- reconnect/relog/session counts;
- server-side drift or rejected commands;
- crash/hang/deadlock/watchdog outcomes.

A soak passes only when no material unbounded growth, deadlock, persistent backlog, protocol divergence or unrecoverable degradation occurs. Duration and quantitative limits require owner approval after baseline implementation.

## 11. Fault and recovery catalogue

| Fault | Required observable |
|---|---|
| malformed/truncated/oversized external input | bounded typed failure; no panic/unbounded allocation |
| disk full/read-only user area | recoverable settings/cache/support error; no corruption loop |
| corrupted asset pack/cache | fail closed, repair path and no arbitrary loose-file fallback |
| interrupted asset/update download | partial content never activates |
| invalid/tampered signature/hash | explicit rejection before extraction/activation |
| process crash during activation | previous known-good release remains recoverable |
| renderer surface outdated/lost | bounded recovery or safe terminal failure |
| GPU device loss | user-visible recovery/restart policy; no authoritative-state corruption |
| audio device removal/replacement | bounded silence/recovery and no event-loop stall |
| DPI/monitor move | stable layout/input mapping without repeated resource leak |
| server restart/session invalidation | safe disconnect and fresh-credential action |
| worker hang on shutdown | nonblocking close state and bounded escalation evidence |
| support/crash artifact failure | client remains safe; secrets/private bytes are not emitted |

Each fault test names the injection mechanism, expected stable code/action, state invariant and cleanup proof.

## 12. Renderer/UI interactive matrix

Once the relevant implementation exists, exercise:

- visible launch and present on each candidate GPU/driver class;
- resizable window, zero-size/minimize and restore;
- multi-monitor movement across scale factors;
- fullscreen/windowed transitions if supported;
- focus loss/gain, keyboard layout and physical mouse input;
- IME enable/composition/commit/cancel;
- clipboard and drag/drop boundaries;
- high-frequency input during frame or network pressure;
- accessibility tree, keyboard-only navigation and screen-reader candidate checks;
- audio default-device change and unplug/replug;
- surface/device loss and application close ordering.

Screenshots/video alone are insufficient; pair them with exact build/environment metadata and structured result capture.

## 13. Benchmark/regression integration

Recommended maturation:

1. local deterministic scene runner and machine-readable result schema;
2. checked-in original/synthetic scene manifests without proprietary bytes;
3. stable named reference machine(s);
4. non-blocking trend collection while noise is characterized;
5. owner-approved budgets and regression thresholds;
6. blocking gates only for stable low-noise metrics;
7. periodic full hardware/driver matrix and long soak outside ordinary PR latency.

A hot-path PR compares before/after using the same build mode, machine, driver and scene. Correctness/security cannot be weakened to meet a performance target.

## 14. Packaging/update reliability

Required tests before M6:

- clean standard-user install and first launch;
- exact signed manifest/artifact verification;
- interrupted and resumed download;
- hash/signature mismatch;
- archive traversal/symlink/special-file rejection;
- insufficient disk and permission errors;
- atomic activation health check;
- crash/power-loss simulation at each activation step;
- rollback to a named previous known-good release;
- repair of missing/corrupt client and pack files;
- update-channel/profile incompatibility;
- uninstall and user-data policy;
- offline startup and support instructions.

The operational legacy asset PR #97 is read-only evidence for download-integrity concerns; it is not a Rust launcher/update contract.

## 15. Evidence artifacts and retention

Store large traces, binaries, screenshots, videos, crash dumps and detailed logs as restricted workflow or controlled test artifacts, not in prompts/checkpoints.

For each artifact record:

- artifact identifier/hash;
- scenario/environment/build;
- owner and readers;
- secrets/proprietary/privacy classification;
- automated and manual redaction result;
- retention and deletion date;
- summarized committable result.

Raw credentials, private captures and proprietary assets are never ordinary artifacts.

## 16. Acceptance ownership

| Decision | Owner required |
|---|---|
| supported Windows editions/builds | product/release owner |
| exact minimum/recommended/high-refresh hardware | product/performance owner |
| final frame/startup/memory/network budgets | product/performance owner after baselines |
| soak duration and release blocking limits | reliability/release owner |
| staging account/environment access | security/operations owner |
| artifact retention/privacy | security/privacy owner |
| signing/update/rollback policy | release/security owner |
| approved asset source and cache budgets | asset/legal/product owners |

P0 may recommend measurement methods and candidate coverage. It may not silently make these product decisions.

## 17. P0 output boundary

This report authorizes no benchmark implementation, workflow, hardware purchase, staging run, credential use, deployment, package signing or product budget. It is the acceptance input for later bounded tasks.
