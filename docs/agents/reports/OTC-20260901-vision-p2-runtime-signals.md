# OTC-20260901 Vision P2 runtime-signals report

## Classification

This worker slice implements repository/static runtime-signal ingestion only. It performs no Official Tibia runtime observation and claims no real-runtime success.

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-RUNTIME-SIGNALS
runtime_access: none
mutation_authorized: false
process_memory_access_allowed: false
network_payload_capture_allowed: false
physical_action_count: 0
```

## Implemented contract

`tools/tibia_re_control_center/agent_runtime_signals.py` adds a Control-Center-owned `RuntimeSignalResolver` that:

- binds evidence to one exact `session_id` / `run_id` / `runtime_id` / `runtime_instance_id` plus the sibling admission producer's deterministic `runtime_binding_sha256`;
- accepts data only through resolver-owned reviewed producer/contract handles;
- maps producer `source_state` to semantic state and evidence class only from a reviewed contract, never from sample/model fields;
- requires one explicit trusted `clock_domain_id` plus a bounded monotonic freshness window;
- rejects future, stale, foreign-binding, foreign-clock, malformed, secret-shaped and ambiguous evidence;
- issues content-addressed `runtime-signal:<sha256>` evidence refs;
- supersedes older evidence from the same reviewed source and rejects out-of-order/equal-time conflicting replacements;
- fails closed when current reviewed-causal producers disagree between `IN_GAME` and `WORLD_EXIT`;
- permits semantic `IN_GAME` / `WORLD_EXIT` only for `REVIEWED_CAUSAL` contracts; `STRUCTURAL_ONLY` and `UNKNOWN` contracts may emit only semantic `UNKNOWN`;
- implements the existing `RuntimeEvidenceResolver` seam consumed by the already-merged deterministic reconciler.

`RuntimeSignalSample` deliberately contains no `runtime_state`, `evidence_class`, producer identity or contract identity fields. Visual/model output therefore cannot self-select runtime authority through this interface.

## Producer inventory and non-promotion ruling

Current trusted repository evidence does not justify hard-coding a production `REVIEWED_CAUSAL` producer in this worker:

- exact-current `gameWindowState` has reviewed static/reader work, but its live causal qualification remains a separate task and this Phase 2 worker forbids process-memory access;
- current Surveyor typed auth/player-state contracts explicitly retain `in_game_claimed=false` / no semantic promotion;
- the merged foundation intentionally left production runtime resolver composition unbound until this later Phase 2 work.

The concurrently implemented runtime-admission worker PR #826 now produces a deterministic `runtime_binding_sha256` over runtime namespace/owner, locator, exact process identity and X11 window identity. This worker consumes that value only as an opaque exact binding token and does not import the unmerged sibling module.

Therefore this PR provides the strict reviewed-source resolver/adapter and tests, but does **not** manufacture a causal producer from static QMeta/window/name evidence, Surveyor structural data, visual/model output or opaque refs. A later coordinator-accepted live read-only path must bind only a separately reviewed producer under fresh admission/provenance.

## TDD evidence

RED-to-GREEN was observed for the production behaviors added in this slice, including:

- missing module/API;
- binding/freshness/producer-contract enforcement;
- secret/malformed provenance rejection;
- clock failure classification and non-callable clock typing;
- supersession/out-of-order evidence handling;
- current causal conflict fail-closed behavior;
- bounded evidence-ref count;
- clock-domain binding;
- prohibition on structural semantic world-state assertion.

Focused final suite: `21` tests PASS.

## Regression and static validation

Final local evidence before publication:

- `python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_signals -q` -> 21 PASS;
- filtered full Control Center suite -> 476 PASS, 2 skipped, excluding exactly three clean-head baseline-failing test methods documented below;
- frozen vision benchmark -> 34 PASS;
- `python -m ruff check tools/tibia_re_control_center/agent_runtime_signals.py tests/tools/tibia_re_control_center/test_agent_runtime_signals.py` -> PASS;
- `python -m py_compile ...` -> PASS on the implemented module/test;
- refreshed `origin/main@ca1a71b5852f6e00ba144ed183af470555c51f56` changes none of this worker's owned paths.

## Clean-head baseline failures

The unfiltered Control Center discovery on the implementation worktree reported five errors across three pre-existing test methods. The same three methods were then reproduced on a clean stashed branch HEAD `11fc18820cc22303d6857361eb3404f5f1844ffa`, proving they are not introduced by the runtime-signals local changes:

1. `test_agent_api.AgentApiTests.test_all_six_routes_exist_and_nonce_is_checked_before_routing` ? Windows loopback `ConnectionResetError [WinError 10054]` in three POST subcases;
2. `test_agent_api.AgentApiTests.test_post_body_shapes_commands_and_transport_boundaries_are_preserved` ? the same loopback connection reset;
3. `test_agent_vision.AgentVisionSensorTests.test_capture_and_snapshot_os_errors_do_not_leak_paths_or_causes` ? existing `ModelSlotUnavailable("MODEL_INFERENCE_FAILED")` path.

No fix was attempted because those files are outside this worker's owned paths and clean-head reproduction isolates them from this slice.

## Current-main revalidation

After shared Package A repair #833 and coordinator checkpoint #836 merged, this worker was restacked conflict-free onto trusted `main@54a20bbd8721e92d069974af14d6ebd2f4f5a55d` without changing the accepted static producer contract. Fresh local validation:

- focused runtime-signals: `21/21 PASS`;
- Ruff and targeted `py_compile`: PASS;
- frozen vision benchmark: `34/34 PASS`;
- Track A runtime governance and checkpoint validator: PASS;
- `git diff --check`: PASS;
- exact changed paths remain the four worker-owned files.

No live runtime evidence is claimed or authorized. Exact head `9d751f340e0a9d1331d7f854795a7aa9d4b93425` passed CI `33534363910`, Package A `33534363711`, Package B `33534363817` and Track A governance `33534363709`. The Draft PR is returned to the coordinator for integration classification; the worker does not self-promote or merge.

## Remaining proof boundary

Real Official Tibia observation remains NOT RUN and unauthorized here. No exact current client PID/session/display/runtime claim, process-memory read, packet/payload capture, model inference, GUI input, credentials, login, process control or physical action occurred.

The coordinator has accepted this bounded static producer contract. Fresh current-main hosted revalidation is now the repository gate before promotion; consumer integration must still bind only to accepted current admission/runtime evidence before any serialized read-only observation or Phase 2 E2E can satisfy programme-level acceptance.

## Exact-head GitHub classification - 426a9aaf1

Exact worker head `426a9aaf15c440531fb9d0bc315f382bf5465ea0` was validated by GitHub Actions. All observed implementation/regression gates passed except one shared historical Package A changed-path audit:

- `CI` run `33529133602`: `CI / Required` PASS; syntax/workflow, Lua and informational static-analysis jobs PASS; build/startup jobs correctly skipped for this path class.
- `Track A agent runtime governance` run `33529133440`: deterministic admission-policy audit PASS and fresh admission behavior audit PASS.
- `TIBIA RE Control Center Package B` run `33529133331`: full regression PASS, fresh falsification audit PASS, real Chromium + CLI loopback E2E PASS.
- `TIBIA RE Control Center Package A` run `33529133500`: deterministic core PASS; `Fresh Package A falsification audit` FAIL only at job `99927496940`, step `Verify declared Package A path boundary`.

The failed job log reports exactly:

```text
Package A changed unexpected paths: [
  'docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md',
  'docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md',
  'docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md'
]
```

The workflow used historical `BASE_SHA=0fe1ecb3569f1d8372209c857ab57f3b626c29ae`; its code/test prefixes already admit this worker's implementation files, while its old exact documentation allowlist does not admit current Phase-2 durable task/report paths or the coordinator task added on `main`. This is therefore a shared CI-governance blocker outside this worker's exact `owned_paths`, not a runtime-signals implementation failure.

The coordinator has already opened non-draft PR `#833` (`ci(track-a): admit vision P2 durable docs`) at `c9c8fe0430d0a0ba2297a53db84d3f4840031d58`. That PR narrowly adds the bounded Phase-2 active-task/archive-task/report prefixes to the existing Package A audit. This worker does not duplicate or modify that shared repair.
