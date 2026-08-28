# Exact-current field6 package materializer repair plan

> Execution must follow RED -> GREEN -> REFACTOR. GitHub live state and hosted checks are authoritative.

**Goal:** Remove the proven cumulative serial-acquisition timeout without weakening any official-package integrity, ownership, privacy, or runtime fence.

**Design:** Parse and validate the complete manifest deterministically before downloads. Execute regular-file download/unpack work through a bounded `ThreadPoolExecutor`, retain submission-order result collection, and keep each output path private and atomic. Preserve every packed/unpacked size and SHA-256 check, exact `bin/client` fence, task-owned WARP/SOCKS routing, non-execution, and cancellation-safe cleanup. Keep the existing 18-minute live-job timeout unless measured post-repair evidence proves a change is necessary.

## Phase 1 — RED

1. Put the active runtime task into `runtime_access: none` repair state.
2. Add a hosted behavioral contract that requires:
   - worker count in `1..16`;
   - observable parallel execution with a bound;
   - deterministic manifest-order results;
   - a material speedup over the serial fixture.
3. Open a draft static-safe PR and record the expected failing hosted run against the unchanged serial materializer.

## Phase 2 — GREEN

1. Add `validate_file_workers()` and `run_bounded_downloads()`.
2. Pre-validate and freeze every manifest row before scheduling downloads.
3. Add a per-file worker that retains all packed and unpacked integrity checks and writes only under task-owned staging.
4. Pass an explicit bounded worker count from the task-owned acquisition wrapper.
5. Run the focused contract, Python compile, shell syntax, actionlint, yamllint, Track A governance, and `CI / Required` on the exact PR head.

## Phase 3 — REFACTOR AND CLOSEOUT

1. Verify changed filenames are limited to the task-owned repair/evidence surface.
2. Obtain an independent exact-head review and resolve all threads.
3. Restack on fresh protected `main` if it moved, rerun required checks, and squash merge.
4. Update the stale V3 checkpoint to terminal pre-action cancellation.
5. Create a separate docs-only V4 admission with a new trigger string; the repair PR itself never performs live login.
