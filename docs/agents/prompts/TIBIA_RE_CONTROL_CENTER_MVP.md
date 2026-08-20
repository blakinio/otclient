# TIBIA-RE-CONTROL-CENTER-MVP

```yaml
prompt_contract:
  version: 2.1.0
  prompting_standard_version: 2.1
  alias: TIBIA-RE-CONTROL-CENTER-MVP
  track_id: official-client-re
  task_kind: control_center_implementation_program
  risk: high
  run_scope: autonomous_program
  continuation_policy: continue_until_real_stop
  task_completion_policy: finalize_archive_and_continue
  user_communication: low_noise
  objective: Implement the reusable Control Center through bounded package tasks while preserving deterministic scenario/semantic-registry, resource identity, durability, STOP, replay, privacy, Track A authority and Oteryn E2E boundaries.
  baseline_version: unversioned pre-repair prompt at PR #605 head 5e63a0ec988cf4fa7789274f13c9d654254e8e44
  eval_suite: docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
  rollback_version: restore pre-repair prompt blob 4bae88b542effd26a431b5e90b5ed22d47f15c62
  feature_scope:
    type: infrastructure
    user_facing: true
    backend_required: true
    frontend_required: true
    integration_required: true
    e2e_required: true
    completion_claim: internal_only
```

Recommended reasoning effort: high / maximum.

Repository:

```text
https://github.com/blakinio/otclient
```

Execution mode:

```text
AUTONOMOUS BOUNDED IMPLEMENTATION
```

## 1. Mission

Implement `TIBIA RE Control Center / E2E Lab` from current repository contracts. Git/current trusted base is authoritative; do not reconstruct semantics from chat/history.

Do not implement real official-client mutation in Package A or B.

## 2. Normative design package

Read all in full before editing:

```text
docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
```

Also read current repository governance/routing/build matrix and applicable Track A contracts even when Package A itself has no runtime.

## 3. Package A hard safety boundary

```yaml
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
network_listener_allowed: false
official_client_access: false
```

Package A is fully implementable/testable with fake adapters/manual clocks/deterministic stores only.

Package B may expose local Control API/browser/CLI but still has no real official-client mutation path.

Real official mutation is Package D under a separate fresh Track A task/admission.

## 4. Mandatory preflight

Before editing:

1. fetch exact current `main`;
2. read root/nested `AGENTS.md`, `docs/agents/README.md`, prompting/governance/closeout policies;
3. inspect open PRs and active tasks for overlap;
4. read complete normative package above;
5. inspect current Track A admission/routing even though A has `runtime_access:none`;
6. inspect current Surveyor producer state; do not assume #592/current successor accepted;
7. inspect `tools/tibia_runtime_bridge/**` and reusable helpers;
8. inspect `MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, `BUILD_TEST_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`;
9. search existing parser/recorder/persistence/API/CLI/fake/cancellation/idempotency code before abstractions;
10. create one task/branch/worktree/Draft PR per package;
11. persist full runtime admission schema and owned paths;
12. resolve live overlaps before edits.

If trusted base supersedes an example, follow trusted base and record discrepancy.

## 5. Non-negotiable architecture

```text
Browser UI ----\
                -> Control API/domain service -> Run Manager -> Scenario Engine
CLI -----------/                                      |
                                      Semantic Field Registry
                                                     |
                                              MutationCoordinator
                                                     |
                                              Safety Controller
                                                     |
                                               Semantic Adapter
```

Global Safety Store owns Request/Resource/Control identity. Per-run safety owns Action/Budget/Recovery. Recorder/Artifact presentation never creates authority.

Forbidden:

```text
CLI -> concrete adapter
Browser -> raw action/debug endpoint
Quick Action -> raw keyboard/mouse/bridge call
Scenario -> Track A lease/registration edits
Predicate -> arbitrary free-form snapshot object traversal
Recorder/report -> authority/evidence promotion
Passive capture -> hidden attach/injection/input mutation
STOP -> new gameplay/process action
```

## 6. Package split

```text
Package A  control-core + Scenario/Execution/Adapter/Artifact/Recorder + fake durability tests
Package B  Control API v1 + browser + CLI + global Request/Resource safety store
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
```

Do not combine all phases into one PR.

## 7. Package A implementation

Recommended path only after checking conventions:

```text
tools/tibia_re_control_center/
```

### A1. Typed contract models

Implement:

- Scenario v1 including `SideEffectBudget`, `EffectBound`, `SemanticFieldPath`, `SemanticFieldRegistry`, `AbortCondition`, discriminated `EntityRef`/`ItemRef`/`DestinationRef`;
- Adapter v1 including `SemanticRegistryDescriptor`, registry hash verification and typed `SemanticFieldValue` projection;
- Execution v1 identities/lifecycles/fences/control state;
- Artifact v1 ControlState, ResourceIdentity, Action/Budget/Recovery and finalization models;
- Comparison v1 pure profile/result types where Package A owns comparator tests;
- contract major-version negotiation and explicit unsupported states.

No arbitrary object may become a predicate/action command type merely for convenience.

### A2. Bounded Scenario parser and semantic registry

Implement literally:

- JSON/YAML -> one typed AST;
- byte/depth/collection/string/step limits;
- duplicate key/custom tag/object-constructor rejection;
- aliases disabled or bounded before expansion;
- finite/domain number + UTF-8 validation;
- exact SemanticFieldPath grammar;
- built-in `control-center.core@1.0.0` registry;
- immutable extension registry ID/version/descriptor schema;
- descriptor JCS/SHA-256 verification from Adapter v1;
- unregistered path = validation error;
- registered-but-unobservable = runtime UNKNOWN/STALE, never fabricated value;
- exact descriptor value type/cardinality/allowed ops;
- discriminated semantic references, explicit checkpoint for `SNAPSHOT_PATH`;
- action-specific parameter schemas;
- exact abort/privacy/capture semantics.

### A3. Canonical hashes

Implement RFC 8785/JCS vectors for:

- scenario hash including semantic schema identity/version;
- action request hash;
- semantic registry hash;
- explicit/generated step IDs.

Runtime fences/timestamps/current authority are not semantic action hash inputs.

### A4. Runtime and side-effect budgets

Scenario `max_runtime_seconds` is fixed absolute monotonic run deadline. Pause/retry/ambiguity never extend it.

Action `EffectBound.max_runtime_seconds = ceil(timeout_ms/1000)` is an admission/fit bound; action total attempt deadline includes preparation, authority wait, capture, dispatch and confirmation.

Non-time hard dimensions use:

```text
limit
reserved
at_risk
committed
uncertain
```

Unbounded effect or action that cannot fit remaining runtime/non-time budget -> refuse before dispatch.

### A5. Backend epoch / ControlState

- fresh unique backend epoch per lifetime;
- control generation monotonic within epoch;
- STOP/reset advance generation;
- overflow fail closed;
- recover durable ControlState before mutation admission;
- restart never implicitly clears STOP;
- missing/corrupt/contradictory prior state -> recovery-required/fail closed;
- old-epoch callbacks never control current execution.

### A6. MutationCoordinator / run ownership

Exactly one coordinator per adapter instance and at most one mutation-capable run lease per adapter by default.

Coordinator owns local Action/Budget/ControlState/dispatch gate only; never Track A authority.

### A7. Dispatch gate

Never hold while waiting for external authority/input lock/capture/network/sleep/discovery.

Only bounded local safety transactions under the gate:

```text
DISPATCH_COMMIT
STOP_TRANSITION
RESET_TRANSITION
```

Finite deadline, no external network dependency.

- dispatch durability failure -> no effect;
- STOP durability failure -> remain fail-closed;
- reset durability failure -> remain STOPPED.

### A8. Action idempotency and terminality

- same action ID/hash -> existing action/result;
- same ID/different hash -> conflict;
- duplicate -> no duplicate non-time reservation;
- retry uses new ID and only after proven NOT_DISPATCHED;
- possible-dispatch/AMBIGUOUS never auto-retry;
- `CONFIRMED` is successful terminal state and late callbacks cannot rewrite it.

### A9. Preparation/final commit

Outside gate: validate schema/action, capability, budget/deadline, advisory preflight, await fake authority, capture before-state.

Immediately before fake physical effect:

1. hold required fake external authority;
2. enter gate;
3. verify action/hash/run ownership/backend/control/STOP/adapter/runtime/session;
4. verify semantic registry identity/version/hash still valid;
5. verify runtime deadline/non-time reservation/capability/current authority;
6. atomically durable `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` + applicable non-time `AT_RISK`;
7. durability barrier;
8. leave gate;
9. exactly one fake effect;
10. conservative reconciliation.

### A10. STOP/reset

STOP and commit race on same gate.

```text
STOP first -> durable latch/new generation -> stale commit refused -> no effect
commit first -> possible-dispatch/non-time at-risk durable -> later STOP latches newer generation without rollback claim
```

Reset is explicit/durable, advances generation, clears only STOP latch, never ambiguity or cached authority.

### A11. Restart/crash recovery

Simulate:

- first safety-store bootstrap;
- valid latched STOP restart;
- corrupt/missing control state;
- STOP/reset durability failure;
- crash before dispatch;
- dispatch barrier failure;
- crash after durable commit before effect;
- crash after effect before result;
- contradictory Action/Budget state.

Expected action classes: NOT_DISPATCHED / POSSIBLY_DISPATCHED→AMBIGUOUS / CONFIRMED. No auto-resume/retry.

### A12. Recorder/privacy/capture

Implement multi-clock/source ordering truthfully; retain causal fields when supplied, never promote timing to causal proof.

Secret classification/rejection occurs before normal Event/Error/Artifact object construction.

Passive semantic-field/snapshot/capture APIs cannot trigger attach/injection/input/process/network mutation.

Emergency STOP cannot create gameplay/process mutation.

### A13. Artifact/safety model

Package A implements interfaces/types for:

```text
Global: ControlState, ResourceIdentity abstraction
Per-run: ActionLedger, BudgetLedger, Recovery
Evidence: staging/finalization/supplements/hashes
```

RequestLedger execution is Package B, but Package A persistence interfaces must allow atomic Request+Resource pair without redesigning Action/Control safety.

Manifest/bundle record semantic registry ID/version/hash.

## 8. Package A mandatory deterministic tests

At minimum all applicable Scenario/Execution/Adapter/Artifact tests, including:

1. bounded JSON/YAML acceptance;
2. duplicate-key/custom-tag/alias/depth/size rejection;
3. non-finite/out-of-domain rejection;
4. JCS scenario/action/registry hash vectors;
5. stable step IDs;
6. built-in semantic registry determinism;
7. extension descriptor/hash mismatch refusal;
8. same registry ID/version descriptor drift refusal;
9. unregistered/wildcard/bracket field path rejection;
10. registered UNKNOWN distinct from unregistered path;
11. type/cardinality/operator mismatch refusal;
12. SideEffectBudget validation;
13. runtime deadline not extended by pause/retry/ambiguity;
14. AbortCondition validation;
15. discriminated semantic references and checkpoint/type rules;
16. all v1 action family schemas;
17. stale/ambiguous selector refusal;
18. unsupported capability/registry refusal;
19. EffectBound/unbounded refusal;
20. read-only mutation refusal;
21. fresh backend epoch/stale callback refusal;
22. authority/adapter/runtime/session/registry change before commit refusal;
23. second mutation run conflict;
24. same action ID/hash dispatch at most once;
25. same ID/different hash conflict;
26. duplicate action no second reservation;
27. STOP wins gate -> durable latch/no effect;
28. commit wins -> possible-dispatch before STOP;
29. STOP while authority wait;
30. STOP write failure fail-closed;
31. restart preserves STOP;
32. corrupt ControlState refuses mutation;
33. reset success/failure semantics;
34. dispatch durability failure/timeout -> no effect;
35. crash after durable commit/effect -> AMBIGUOUS unless reconciled;
36. non-time budget exhaustion/overflow/uncertain accounting;
37. retry only proven NOT_DISPATCHED, zero attempts rejected;
38. pause/resume stale identity/registry refusal;
39. terminal CONFIRMED late-callback immunity;
40. multi-clock ordering truthfulness;
41. secret construction barriers;
42. screenshot quarantine;
43. passive semantic-field/capture purity;
44. emergency stop cannot mutate;
45. artifact crash/finalization/immutability;
46. semantic registry provenance retained in manifest/bundle;
47. no operator-facing adapter bypass.

## 9. Package B — Control API/browser/CLI/global Request+Resource safety

Consume merged A.

Select one local persistent store satisfying Artifact-v1 global RequestLedger + ResourceIdentityLedger + ControlState and per-run Action/Budget semantics.

Implement Control API v1 literally:

- loopback-only bind;
- fresh >=256-bit nonce per backend epoch;
- nonce absent URL/log/artifact/argv;
- exact Host and browser Origin;
- mandatory `frame-ancestors 'none'`;
- no permissive CORS/cookie ambient auth;
- typed bounded bodies;
- RequestLedger request hashes;
- stable ResourceIdentityRecord before scheduling;
- atomic/equivalent `RequestLedger INTENT_DURABLE + ResourceIdentityRecord CREATED_NOT_SCHEDULED` for run/one-step creation;
- same-resource replay across crash/restart;
- no auto-resume mutation from surviving resource intent;
- stable STOP/reset transition IDs with uncertain reset staying latched;
- bounded pages/events/subscribers/backpressure;
- safe errors;
- graceful shutdown;
- no raw/debug/adapter endpoint;
- no remote/LAN mode.

Browser and CLI are thin clients of same domain service. Package B mutating controls target fake adapters only.

Mandatory tests include every Control API v1 security/replay test, browser/CLI parity, truthful AUTHORITY/CAPABILITY/EVIDENCE/FRESHNESS/schema-support views, reload/new-tab dedupe and shutdown/restart safety-state persistence.

## 10. Package C — accepted Surveyor/read-only

Only after an accepted exact producer exists. Pin:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Consume outputs, never copy/promote producer logic/evidence. Mismatch -> `UNAVAILABLE/INCOMPATIBLE`.

## 11. Package D — Official Track A mutation adapter

This prompt does **not** authorize Package D execution.

Separate runtime-sensitive task must:

1. read then-current Track A contracts;
2. persist fresh runtime admission;
3. satisfy current lease/registration/Gate A/rebind/Gate B/uniqueness/whole-lifetime supervisor;
4. satisfy shared input lock;
5. prove capability/evidence/reference-path parity;
6. use exact semantic registry/action schema + safe EffectBound;
7. acquire Track A guard without local dispatch gate;
8. final Track A checks while guard held;
9. one-shot durable `commit_dispatch()` immediately before effect;
10. exactly one physical effect under same guard;
11. conservative reconciliation.

Start with one smallest already-proven semantic action. Never build a second Track A authority.

## 12. Package E — Oteryn v2 adapter

Separate `blakinio/Oteryn-v2` task/branch/PR. Reuse accepted ADR-0007/versioned cross-repo boundary; retain `protocol-oteryn`, client intent/server authority, production exclusion of test hooks. No second E2E/scenario authority or hidden authoritative client mutation.

## 13. UI requirements

Always visible:

```text
RUNTIME | CLIENT | RECORDER | AUTHORITY | CAPABILITY | EVIDENCE | FRESHNESS | SESSION
STOP ALL | PAUSE
```

Required tabs:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Schema support must not be rendered as authority. Quick Actions are one-step scenarios only.

## 14. Differential comparison

Use Comparison v1 literally. Unknown/unobservable official reference -> coverage gap, never Oteryn mismatch. No byte/internal-layout/renderer parity requirement by default.

## 15. Validation procedure per package

1. re-fetch exact main/open PR/task overlap;
2. inspect exact final changed files/full diff;
3. run focused deterministic tests from actual BUILD_TEST_MATRIX/repository tooling;
4. run required exact-head GitHub checks;
5. full self-review for architecture/security/failure paths/claims;
6. rerun invalidated race/idempotency/durability/privacy tests after repair;
7. obtain independent review when policy requires;
8. record exact commands/outcomes/SHA;
9. update catalog/changelog/contracts as required;
10. merge only through current policy;
11. archive task/release ownership after terminal completion.

## 16. Mandatory non-claims

Never claim:

- official action capability from fake tests;
- Track A authority from Control Center/API/schema state;
- runtime compatibility from repository-only tests;
- causal proof from timing/ingest order;
- no effect merely because result timed out;
- safe retry after possible dispatch;
- passive capture if enablement mutates;
- STOP rollback of committed effect;
- restart as implicit STOP reset;
- request replay safety without durable Request+Resource pair before scheduling;
- remote security from loopback design;
- secret safety from export-only redaction;
- Oteryn parity before adapter/evidence exists.

## 17. Package A terminal acceptance

```text
runtime_access=none
network_listener=none
official_client_access=none
Scenario parser/hash/registry/action/reference/budget/abort=PASS
Adapter semantic registry/projection=PASS
backend epoch/generation/ControlState=PASS
MutationCoordinator serialization=PASS
STOP-vs-commit + durable reset=PASS
durability-before-effect=PASS
ActionLedger idempotency + terminal CONFIRMED=PASS
runtime deadline + non-time budget accounting=PASS
crash/restart ambiguity=PASS
multi-clock Recorder=PASS
construction-time privacy=PASS
capture/emergency bypass tests=PASS
Artifact finalization/provenance=PASS
no adapter/operator bypass=PASS
all mandatory deterministic tests=PASS
self-review=no material findings
required independent review=PASS
exact-head CI=PASS
```

A fresh agent must be able to continue solely from Git/task/PR without this chat.

## 18. Desired first operator result

After A-C: local browser+CLI through same secured backend, truthful read-only Track A/Surveyor status, schema/capability/evidence/freshness views, scenario/run/action/event/artifact browsing, deterministic fake experiments, STOP/idempotency/restart/privacy proof and privacy-safe agent bundle. Real official mutation remains NO until separately admitted Package D.