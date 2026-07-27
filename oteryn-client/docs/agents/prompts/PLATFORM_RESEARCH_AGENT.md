# Windows Platform Evidence Agent Prompt

Use after the common prefix in `WORKER_AGENT_BASE.md`.

```text
Lane: W1-PR
Workstream: WS-R02 evidence preparation only
Task type: documentation/research; no platform/application implementation

Goal:

Evaluate current primary documentation and repository requirements for the smallest Windows platform/application-shell spike, then recommend one bounded implementation package without adding dependencies or creating platform/application crates.

Expected owned paths, subject to live overlap check:

- oteryn-client/docs/research/windows-platform/README.md
- oteryn-client/docs/research/windows-platform/WINDOW_AND_EVENT_REQUIREMENTS.md
- oteryn-client/docs/research/windows-platform/DEPENDENCY_EVALUATION.md
- oteryn-client/docs/research/windows-platform/THREAD_AND_SHUTDOWN_MODEL.md
- oteryn-client/docs/research/windows-platform/SPIKE_RECOMMENDATION.md
- one active task record

Forbidden paths:

- oteryn-client/apps/**
- oteryn-client/crates/platform/**
- oteryn-client/crates/app-runtime/**
- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml
- oteryn-client/tools/architecture-check/**
- .github/workflows/**
- legacy platform implementation paths except read-only evidence
- external repository writes

Required evidence sources:

- accepted architecture, repository layout, lifecycle, security and performance documents;
- foundation audit platform/hardware report;
- current `RUST_WORKSPACE.md` and dependency policy;
- current official/primary documentation for candidate Rust window/event integration libraries and Windows APIs;
- current release/version/license/maintenance information at task time;
- maintained legacy behavior only as an interaction/reproduction checklist, not target architecture.

Deliverables:

1. README.md
   - exact research date and source versions;
   - evidence labels;
   - one bounded later WS-R02 recommendation and explicit unknowns.

2. WINDOW_AND_EVENT_REQUIREMENTS.md
   - process/window lifecycle;
   - per-monitor DPI awareness and monitor transitions;
   - resize, minimize, restore and close ordering;
   - keyboard, text/IME and raw/high-precision mouse requirements;
   - focus, cursor, clipboard and drag/drop only where required by accepted architecture;
   - system-browser URL launch and loopback callback boundaries;
   - no renderer or Identity implementation.

3. DEPENDENCY_EVALUATION.md
   - compare only serious current candidates for window/event integration;
   - exact versions and primary-source links;
   - Windows support, maintenance, license, unsafe/FFI/native surface, binary/runtime implications and known lifecycle constraints;
   - compatibility with the selected Rust toolchain and future `wgpu` surface ownership;
   - clear recommendation or BLOCKED result;
   - no Cargo edit and no popularity-based choice.

4. THREAD_AND_SHUTDOWN_MODEL.md
   - main-thread ownership of the Windows event loop;
   - boundaries among application orchestration, future network workers, renderer and audio;
   - cancellation/shutdown ordering and stale callback prevention;
   - no broad global mutex, hidden threads, async runtime or global event bus selected here;
   - interaction with future foundation cancellation/time primitives without defining their API.

5. SPIKE_RECOMMENDATION.md
   - one smallest Windows-only application/platform spike;
   - expected owned paths and architecture category;
   - exact observable behavior, such as create/resize/minimize/close a window and deterministic shutdown;
   - dependency review and CI evidence required;
   - tests that can be headless versus manual/runtime evidence;
   - non-goals: no game state, renderer pass, network, Identity, updater, audio or UI framework.

Rules:

- use web/current primary sources for dependency/version claims;
- do not claim another platform is supported;
- do not choose the minimum Windows release without product and dependency evidence;
- do not add `winit`, raw-window-handle, Windows bindings, `wgpu`, async or any other dependency in this PR;
- do not write a code prototype outside an approved later implementation task;
- do not mirror the legacy platform abstraction merely because it exists;
- do not change accepted architecture without a separate ADR task.

Acceptance:

- Windows lifecycle/input/DPI requirements are implementation-ready and bounded;
- candidate evaluation uses current primary evidence and records unsafe/license/maintenance concerns;
- thread/shutdown model respects accepted ownership and cancellation boundaries;
- one small spike is recommended with tests and non-goals;
- no application dependency or crate is added;
- changed files are limited to the isolated research path and task lifecycle;
- documentation and repository required checks pass on exact head;
- task merges and archives independently.

Final handoff:

Recommend exactly one future WS-R02 package. Do not implement it in this PR.
```
