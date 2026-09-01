# OTC-VISION-P2-CONTROL-BRIDGE report

## Classification

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-CONTROL-BRIDGE
task_id: OTC-20260901-vision-p2-control-bridge
implementation_head: aa2bfaa8fc47c4c7abdb1ddd28a80e5178ed903e
pr: 830
worker_result: PRODUCER_COMPLETE
promotion_authority: coordinator_only
runtime_access_used: none
physical_action_count: 0
```

## Delivered slice

- Added `AgentEdgeBridge` as an authority-neutral read-only integration boundary over the existing Control Center session/event store.
- Bounded `read_only` task acceptance requires zero physical budget, no secret capability and `SCREENSHOT`-only action vocabulary.
- Edge observations bind session/run/edge instance, heartbeat, capture hash/ref and runtime evidence refs; secret-unsafe capture is rejected before persistence.
- Heartbeat loss, evidence staleness and disconnect degrade currentness without creating a physical effect.
- Restart preserves durable evidence but never restores a live edge connection; fresh observation is required before `current=true`.
- Replayed observations and competing edge instances are rejected fail-closed.
- Existing owner session API, MCP status and Agent UI expose edge availability/capture/runtime state without adding an edge-control endpoint or second store.
- Production executor remains `NULL`; mutation authority remains `NONE`; physical budget/count remain `0/0`.

## Validation

- RED: initial edge test failed with `RUNTIME_ACCESS_UNAVAILABLE` before implementation.
- RED: disconnect replay and live-instance replacement tests both failed before hardening, then passed after the bounded fix.
- `ruff 0.16.1` on all changed Python implementation/tests: PASS.
- `python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center`: PASS.
- Focused edge/session/API/MCP/persistence suite: 121 tests PASS under WSL/Linux-compatible Python.
- `audit_agent_foundation.py`: PASS for runtime surfaces, authority boundaries and MCP allowlist.
- `audit_package_b.py`: PASS on Windows.
- `e2e_package_b.py`: PASS on Molehill Windows including real Chrome browser, CLI and restart/idempotency; Official client access remained `NONE`.

## Known external/baseline evidence

The standalone `e2e_agent_foundation.py` currently fails on unchanged `origin/main`: its fixture submits `physical_action_budget: 1` through the existing Control API guard that requires budget `0`. Neither file is changed by this worker, so the conflict was recorded rather than repaired outside ownership.

A full `unittest discover` under WSL on the Windows-mounted worktree was terminated after 462 seconds in filesystem I/O (`D` state) without a test failure. Exact-head GitHub CI is therefore the authoritative full-suite result.

PRs #826-#829 still had bootstrap-only remote heads during the final worker review, so no sibling producer wire contract was available to integrate or override. The coordinator must revalidate those live contracts during classification.

## Runtime non-claim

No Synology/Kasm/Official Tibia runtime was observed, controlled or mutated. This worker stayed `runtime_access: none`; no credentials, login, GUI input, process control, process memory or network payload capture occurred.

## Coordinator handoff note - 2026-09-01 18:07 CEST

Live state at handoff:
- branch: `feat/OTC-20260901-vision-p2-control-bridge`
- published head inspected before this note: `30f12803f29ae38789959a5958e144b6f865c5e7`
- Draft PR: `#830`, base `main`; worker must not self-promote or self-merge.
- implementation commit: `aa2bfaa8fc47c4c7abdb1ddd28a80e5178ed903e`.

Exact-head CI evidence for `30f12803f29ae38789959a5958e144b6f865c5e7`:
- `Track A agent runtime governance` run `33529383606`: **SUCCESS**; both deterministic and fresh admission jobs passed.
- `TIBIA RE Control Center Package B` run `33529383647`: **SUCCESS**.
- `TIBIA RE Control Center Package A` run `33529383678`: **FAILURE**, but its deterministic core job passed; only `Fresh Package A falsification audit` failed because the historical Package A path allowlist rejects this worker's `docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md` and task record as unexpected paths. This is a CI/path-policy mismatch, not a demonstrated bridge test failure.
- main `CI` run `33529383982`: **FAILURE** because `Lua Syntax / Check Lua Syntax` failed during `sudo apt-get update && apt-get install luajit`; Microsoft Ubuntu/Azure CLI repositories returned HTTP 403 before checkout or Lua compilation. Fast Checks passed. `CI / Required` failed downstream from that setup failure.

Coordinator classification guidance:
- revalidate the live PR head and sibling PRs `#826-#829` before integration; their contracts may have advanced since the worker review;
- distinguish worker correctness from the two CI failures above: decide whether Package A's path-boundary allowlist needs coordinator-owned adjustment/waiver, and whether the Lua setup failure should simply be rerun after infrastructure recovery;
- preserve Phase 2 authority: this worker used `runtime_access:none`, performed no Synology/Kasm/Official Tibia observation or mutation, and physical action count stayed `0`;
- independently classify PR `#830` as `ACCEPT`, `ACCEPT_WITH_EDITS`, `RETURN_FOR_EVIDENCE`, or `REJECT/SUPERSEDE` only after the live CI/policy state and sibling contracts are reconciled.
