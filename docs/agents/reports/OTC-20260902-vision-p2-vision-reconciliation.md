# OTC-20260902 Vision P2 reconciliation report

## Baseline

- Trusted base `main`: `8441fc1cce1600033b505d68ebc5c0141b337394`.
- Wave 1 trusted composition is integrated through PR #854 and lifecycle closeout #855.
- Wave 2 alias: `OTC-VISION-P2-VISION-RECONCILIATION`.
- Runtime authority at task start: `runtime_access:none`; mutation/login/gameplay/process/input authority all false; physical action budget/count `0/0`.
- Codex usage for coordination/task setup: `0`.

## Verified integration gap

`tools/tibia_re_control_center/agent_reconcile.py` contains the deterministic reconciliation matrix and a resolver-bound trusted composition seam. The default public compatibility entry point deliberately has no resolver, so reviewed-causal runtime claims fail closed. `tools/tibia_re_control_center/vision_p2_trusted_composition.py` is the application-owned trusted Phase 2 composition for capture/runtime transport but does not yet compose or invoke the reconciliation seam. `ControlDomainService.observe_agent_vision()` returns the bounded visual observation, and the session edge path already persists accepted read-only edge/runtime evidence.

Therefore Wave 2 should connect these accepted producer/consumer interfaces and persist reconciliation provenance; it should not build replacement capture, transport, runtime-signal or state-storage implementations.

## Required evidence

Pending implementation and validation:

- focused RED/GREEN reconciliation tests;
- trusted-composition integration tests for current reviewed runtime evidence;
- stale/forged/mismatched runtime evidence fail-closed tests;
- restart/persistence evidence proving historical data does not regain current authority;
- exact-head GitHub Actions result;
- later coordinator-serialized physical read-only E2E (cannot be substituted by hosted/fake evidence).

## Current result

`IMPLEMENTING` — task claimed and branch opened; no runtime access used and no owner-funded Codex invocation performed.
