# OTC-VISION-P2-CONTROL-BRIDGE report

## Classification

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-CONTROL-BRIDGE
task_id: OTC-20260901-vision-p2-control-bridge
implementation_head: 7ec06d4d9bdec9f10f76cb7b8b49d5f696e28ecd
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
## Coordinator RETURN_FOR_REPAIR response - 2026-09-01 22:12 CEST

Trusted integration base is `main@e883543403d5430d7b1d287f59043b23c98f37d6`. Runtime admission producer #838 and runtime-signals producer #839 are both merged on this base. The worker restacked conflict-free; neither promotion overlaps the bridge-owned implementation/test paths.

Repair commit: `7ec06d4d9bdec9f10f76cb7b8b49d5f696e28ecd`.

The coordinator finding is addressed as follows:
- `TaskEnvelope.runtime_access=read_only` remains only a requested class; it does not make the edge or Official client access current. `official_client_access` is `NONE` until a fresh canonical `ReadOnlyRuntimeAdmission` is bound.
- `bind_read_only_runtime()` accepts the exact merged `ReadOnlyRuntimeAdmission`, `RuntimeSignalResolver` and `RuntimeSignalBinding` types and revalidates admission freshness/canonicality, task ownership, run/runtime binding hash and exact task client identity.
- edge observations may no longer inject runtime semantic strings or opaque refs. Runtime semantics are accepted only through exact merged `RuntimeSignalEvidence` produced/recognized by the bound resolver.
- the bridge recomputes the #839 content-addressed runtime-signal digest, so producer/contract/source provenance cannot be altered while retaining a trusted signal ref.
- stale/forged/foreign/duck-typed admission or signal data, resolver swaps, replay, competing edge instances, disconnect and restart all fail closed. Restart/disconnect discard live authority and require a fresh bind.
- the existing AgentEvent/session store remains the only durable plane. Production executor is still `NULL`, mutation authority `NONE`, and physical action budget/count `0/0`.

Fresh local validation after merged #839:
- edge bridge focused suite: 17/17 PASS;
- full Linux-compatible `test_agent*.py`: 260 PASS, 1 skipped;
- Ruff 0.16.1: PASS; compileall: PASS; `git diff --check`: PASS;
- Agent Foundation audit: PASS;
- Package A and P1 audits: PASS with `MATERIAL_FINDINGS_OPEN=0` and `RUNTIME_ACCESS_NONE=PASS`;
- Package B audit: PASS; real Chrome/CLI/restart E2E: PASS with `OFFICIAL_CLIENT_ACCESS=NONE`.

Windows-only baseline remains the previously isolated loopback reset family (`WinError 10054`) plus the existing broader vision `MODEL_INFERENCE_FAILED` case; the same final tree is green under WSL/Linux and no bridge-specific failure signature was introduced.

No live Synology/Kasm/Official Tibia observation was performed or authorized. This worker invocation stayed `runtime_access:none` and physical action count remained `0`. Exact-head hosted CI and coordinator reclassification remain the next gates.
## Exact-head hosted validation - 274955658f08

The repaired implementation/checkpoint head `274955658f08c8631d24511be1646a9ec16fff6c` completed the required hosted validation successfully:
- Track A agent runtime governance `33554082006`: SUCCESS;
- TIBIA RE Control Center Package A `33554082232`: SUCCESS, including deterministic core and fresh falsification audit;
- TIBIA RE Control Center Package B `33554082117`: SUCCESS, including fresh falsification, full regression, and real Chromium + CLI E2E;
- repository CI `33554082565`: SUCCESS with `CI / Required` PASS, Lua syntax PASS, workflow/syntax checks PASS, and informational static analysis PASS.

PR hygiene at the handoff point: exactly 8 expected changed paths, 0 submitted reviews, 0 review threads. The worker repair is therefore repository/static producer-complete and returns to `OTC-VISION-P2-COORDINATOR` for independent classification. No live runtime observation or physical action was performed.

## Coordinator review 5500323278 remediation — pending exact-head validation

The prior completion classification is superseded by the coordinator's exact-head
`RETURN_FOR_REPAIR`. The bridge now consumes only a one-shot receipt issued by
its composition-owned runtime-authority registry. The receipt seals the current
admission, reviewed resolver contract/configuration, session/run/runtime binding,
and task client identity. Task/edge callers cannot bind caller-supplied admission
or resolver components, including before an edge is connected.

The runtime paths now also fail closed at `TaskEnvelope.deadline_epoch_ms`:
binding, runtime-signal ingestion, edge-observation ingestion and status/currentness
all refuse or report no read-only authority after expiry. The repair keeps the
production executor `NULL`, mutation `NONE`, and physical action budget/count
`0/0`; no runtime was accessed.

Focused RED-to-GREEN evidence on the working repair tree:

- `test_agent_edge_bridge`: 20 PASS, including caller-minted admission,
  unapproved exact-class causal resolver, pre-connect substitution and task-expiry
  negatives;
- Windows full relevant `test_agent*.py`: 263 executed with the established five
  unrelated baseline errors (four loopback `WinError 10054`, one vision
  `MODEL_INFERENCE_FAILED`);
- WSL/Linux-compatible full relevant `test_agent*.py`: 263 PASS, 1 skipped;
- `compileall`, focused Ruff and `git diff --check`: PASS.

Fresh exact-head audit, Package A/Package B/Track A and CI remain pending after
the repair commit is published. The Draft PR remains coordinator-owned for
classification; this worker will not merge or promote it.
