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

- binds evidence to one exact `session_id` / `run_id` / `runtime_id` / `runtime_instance_id`;
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

Focused final suite: `20` tests PASS.

## Regression and static validation

Final local evidence before publication:

- `python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_signals -q` -> 20 PASS;
- filtered full Control Center suite -> 475 PASS, 2 skipped, excluding exactly three clean-head baseline-failing test methods documented below;
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

## Remaining proof boundary

Real Official Tibia observation remains NOT RUN and unauthorized here. No exact current client PID/session/display/runtime claim, process-memory read, packet/payload capture, model inference, GUI input, credentials, login, process control or physical action occurred.

The coordinator must classify this Draft PR and integrate it with the separately owned runtime-admission, capture, edge-transport and Control-Bridge slices before any serialized read-only observation or Phase 2 E2E can satisfy programme-level acceptance.
