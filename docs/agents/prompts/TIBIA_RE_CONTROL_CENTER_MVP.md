# TIBIA-RE-CONTROL-CENTER-MVP

```yaml
prompt_contract:
  version: 2.0.0
  prompting_standard_version: 2.1
  alias: TIBIA-RE-CONTROL-CENTER-MVP
  track_id: official-client-re
  task_kind: control_center_implementation_program
  risk: high
  run_scope: autonomous_program
  continuation_policy: continue_until_real_stop
  task_completion_policy: finalize_archive_and_continue
  user_communication: low_noise
  objective: Implement the reusable Control Center through bounded package tasks while preserving deterministic scenario, durability, STOP, replay, privacy, Track A authority and Oteryn E2E boundaries.
  baseline_version: unversioned pre-repair prompt at PR #605 head 5e63a0ec988cf4fa7789274f13c9d654254e8e44
  eval_suite: docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
  rollback_version: restore the pre-repair prompt blob 4bae88b542effd26a431b5e90b5ed22d47f15c62
  feature_scope:
    type: infrastructure
    user_facing: true
    backend_required: true
    frontend_required: true
    integration_required: true
    e2e_required: true
    completion_claim: complete_feature
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

Implement the first reusable `TIBIA RE Control Center / E2E Lab` exactly from current repository contracts.

Do not reconstruct design from chat history. Git is authoritative.

Do not implement real official-client mutation in Package A or Package B.

## 2. Normative design package

Read **all** of these files in full before editing:

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

Artifact v1 is normative for Package A safety/control-state persistence and finalization. Comparison v1 is normative for any Package A comparator/profile types and pure comparator tests. Control API v1 becomes executable in Package B but its request/safety contracts must already be compatible with Package A persistence abstractions.

This prompt defines procedure only. It does not weaken current Track A or Oteryn governance.

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

Package A must be fully implementable/testable without KasmVNC, official-client processes, Track A runtime, credentials, login, GUI input, gameplay or network listener.

Package B may add the local Control API/browser/CLI but remains read-only for real official-client state. Mutation-capable Package B tests use only the explicit fake adapter.

Real official-client mutation is Package D under a separate fresh Track A task/admission.

## 4. Mandatory preflight

Before editing:

1. fetch exact current `main`;
2. read root `AGENTS.md`, `docs/agents/README.md` and applicable nested instructions;
3. inspect all open PRs and `docs/agents/tasks/active/**` for overlapping Control Center/scenario/recorder/persistence/API/adapter work;
4. read the complete normative design package above;
5. inspect current Track A admission/routing/contracts referenced by `docs/agents/README.md` even though Package A itself uses no runtime;
6. inspect current #592 Surveyor status and do not assume merge/interface stability;
7. inspect `tools/tibia_runtime_bridge/**` and existing test/runtime helpers for reuse;
8. inspect `MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, `BUILD_TEST_MATRIX.md`, `CROSS_REPO_CONTRACTS.md`;
9. search existing scenario, fake, recorder, persistence, HTTP, CLI, cancellation/idempotency and artifact infrastructure before creating abstractions;
10. create one dedicated task, branch/worktree and Draft PR;
11. persist the full `runtime_access:none` admission schema in the task;
12. declare owned paths and resolve live overlaps.

If current trusted-base state supersedes any example in this prompt, follow trusted base and record the discrepancy.

## 5. Non-negotiable architecture

```text
Browser UI ----\
                -> Control API/domain service -> Run Manager -> Scenario Engine
CLI -----------/                                      |
                                                     v
                                              MutationCoordinator
                                                     |
                                              Safety Controller
                                                     |
                                               Semantic Adapter
```

Recorder/Artifact Store observe the normal path; they never create authority.

Forbidden:

```text
CLI -> concrete adapter
Browser -> raw action/debug endpoint
Quick Action -> raw keyboard/mouse/bridge call
Scenario -> direct Track A lease/registration mutation
Recorder/Artifact Store -> evidence promotion
Passive capture -> hidden attach/injection/input mutation
STOP -> new gameplay/process-control action
```

## 6. Package split

Do not implement all phases in one PR.

```text
Package A  control-core + Scenario/Execution/Recorder/Artifact + fake adapter/durability tests
Package B  Control API v1 + browser + CLI + persistent global RequestLedger/safety store
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
```

## 7. Package A — control-core

Recommended path only after confirming repository conventions:

```text
tools/tibia_re_control_center/
```

### A1. Contract types/version negotiation

Implement typed models for:

- Scenario v1 including `SideEffectBudget`, `SemanticFieldPath`, `AbortCondition` and discriminated semantic references;
- Execution v1;
- Adapter v1;
- Artifact v1 including `ControlStateRecord`, Action/Budget/Recovery records and finalization models;
- Comparison v1 profile/result types where Package A implements pure comparator tests;
- adapter/execution/scenario major-version negotiation;
- generic capabilities;
- official-only evidence extension;
- runtime/freshness/snapshot state;
- events/artifacts/ledgers.

Unsupported required major semantics fail closed.

### A2. Bounded Scenario v1 parser

Implement the contract literally:

- JSON/YAML -> one typed AST;
- byte/depth/collection/string/step limits;
- reject duplicate keys;
- reject custom YAML tags/object constructors;
- aliases disabled or strictly bounded before expansion;
- reject non-finite/out-of-domain numbers;
- UTF-8 validation;
- exact `SemanticFieldPath` grammar plus normalized-schema membership validation;
- discriminated `EntityRef`, `ItemRef`, `DestinationRef` parsing with unknown variant fields rejected;
- action-specific parameter schemas;
- semantic selectors only;
- typed predicates with no implicit coercion;
- exact `SideEffectBudget` and `AbortCondition` semantics;
- deterministic privacy/capture policies.

### A3. Canonical hashes and step IDs

Implement JCS/RFC-8785 canonicalization exactly as Scenario v1 defines.

Verify known deterministic vectors for:

- scenario hash;
- action request hash;
- explicit local step IDs;
- generated ordinal step IDs.

Runtime fences/timestamps/current authority are not part of semantic action hash.

### A4. EffectBound and SideEffectBudget

Before reservation, obtain deterministic finite maximum plausible effect per action.

Fake adapter must support exact EffectBound fixtures.

The Scenario-v1 `SideEffectBudget` is the hard run ceiling and contains every required dimension. The action `EffectBound` is the conservative per-action maximum. If the bound cannot be produced or exceeds remaining budget, refuse before dispatch.

### A5. Backend epoch/control generation/control state

- create a fresh unique backend epoch for every simulated backend lifetime;
- control generation is monotonic only within that epoch;
- STOP and successful reset advance generation;
- no wrap/reuse on overflow;
- stale old-epoch callbacks cannot control new work;
- recover Artifact-v1 `ControlStateRecord` before mutation admission;
- a fresh backend epoch never implicitly clears `stop_latched`;
- missing/corrupt/contradictory prior control state fails closed.

### A6. MutationCoordinator

Exactly one coordinator per adapter instance.

It owns:

- one-at-a-time mutation commit;
- ActionLedger;
- BudgetLedger;
- durable local ControlState/STOP latch;
- `dispatch_gate`;
- STOP/reset;
- one-shot `commit_dispatch()`.

It does not own Track A authority.

### A7. Dispatch gate discipline

Never hold `dispatch_gate` while waiting for external/fake authority, GUI locks, capture, network or arbitrary I/O.

The only I/O permitted while holding it is one bounded local safety-store transaction of the exact kinds allowed by Execution v1:

```text
DISPATCH_COMMIT
STOP_TRANSITION
RESET_TRANSITION
```

Every such transaction has a deterministic finite timeout/failure path and no external network dependency.

Dispatch durability failure -> no effect. STOP durability failure -> coordinator remains fail-closed. Reset durability failure -> STOP remains latched.

### A8. Idempotent action ledger

Store:

```text
action_id
action_request_hash
lifecycle/dispatch state
backend/control/adapter/runtime/session fences
result/evidence refs
```

Rules:

- same ID/hash -> same logical action/result, no second dispatch;
- same ID/different hash -> conflict refusal;
- duplicate submission -> no second budget reservation;
- possible-dispatch -> no auto-retry;
- explicit retry -> new ID + fresh attempt/budget/fences/authority;
- `CONFIRMED` is the successful terminal action lifecycle state and cannot be rewritten by late callbacks.

### A9. Side-effect BudgetLedger

Per dimension:

```text
limit
reserved
at_risk
committed
uncertain
```

Use checked arithmetic.

Before dispatch reserve Scenario-v1 EffectBound against Scenario-v1 SideEffectBudget.

At durable dispatch commit, move reserved -> at-risk atomically with ActionLedger possible-dispatch transition.

Reconcile conservatively according to Execution v1.

### A10. Preparation

Outside dispatch gate:

- validate action;
- capability check;
- budget reservation;
- advisory preflight;
- await fake authority;
- before-state capture.

Every wait is deterministic/bounded/cancellable.

Preflight never grants standing dispatch permission.

### A11. One-shot `commit_dispatch()`

Immediately before fake irreversible effect:

1. enter dispatch gate;
2. verify exact action/hash not previously committed;
3. verify backend/control generation and recovered/unlatched ControlState;
4. verify STOP/cancellation;
5. verify adapter/runtime/session fences;
6. verify budget reservation;
7. verify capability;
8. verify current fake authority;
9. atomically make ActionLedger `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` and budget `AT_RISK` durable;
10. complete durability barrier;
11. leave dispatch gate;
12. only then allow exactly one fake physical effect.

Durability failure/timeout -> no effect.

### A12. STOP ALL

STOP races with commit on the same dispatch gate.

Required deterministic outcomes:

```text
STOP first -> STOP_TRANSITION durable -> stop_latched=true + generation advances -> stale commit refused -> no effect
commit first -> possible-dispatch/at-risk durable -> later STOP durably advances/latches without claiming rollback
```

STOP then cancels queued/waiting work and harness-owned passive captures, but grants no new external action.

If STOP persistence fails, mutation remains fail-closed and the safety store is treated as failed/recovery-required.

### A13. Reset

Reset is explicit and local only.

It requires valid recovered safety state, must preserve unresolved AMBIGUOUS overlapping side-effect domains, advances control generation, and durably writes `stop_latched=false` through Execution-v1 `RESET_TRANSITION` before mutation admission reopens.

Reset failure leaves STOP latched. Reset never restores cached Track A authority.

### A14. Restart/crash recovery

Deterministic store must simulate:

- first-ever durable ControlState initialization;
- restart with valid latched STOP;
- missing/corrupt/contradictory ControlState;
- STOP durability failure;
- reset durability failure;
- crash before dispatch commit;
- dispatch durability failure;
- crash after durable commit before effect;
- crash after effect before result;
- corrupt/missing/contradictory action/budget ledger.

Expected action classes:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED -> AMBIGUOUS unless reconciled
CONFIRMED
```

No automatic mutation resume/retry. Restart never implicitly resets STOP.

### A15. Pause/resume

Pause does not suspend external generations/deadlines.

Resume revalidates backend/control/adapter/runtime/session fences and declared predicates.

Changed runtime/session invalidates pending mutation by default.

### A16. Recorder core

Preserve:

- ingestion sequence/time;
- source timestamp/clock domain;
- source-local sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session fences;
- run/step/stimulus;
- late/sensitivity.

Track A causal metadata is retained when supplied.

Never turn ingestion order/timestamp proximity into causal proof.

### A17. Late-event/finalization model

```text
ACTIVE -> CLOSING -> FINALIZED
```

Late events enrich evidence only; they cannot rewrite terminal action/run results or restart execution.

Finalized result is immutable except explicit append-only supplements.

### A18. Construction-time privacy

Implement constructors/barriers such that secret-class data cannot enter normal Event/Error/Artifact objects.

Tests must cover:

- secret-shaped event fields;
- arbitrary exception/repr/debug text;
- environment-variable-shaped data;
- private-chat-shaped data;
- screenshot SAFE/QUARANTINED/REJECTED states;
- `SECRET_REJECTED` metadata only.

### A19. Passive capture boundary

Fake adapter distinguishes passive capture from invasive enablement.

Read-only `capture_start()` refuses any fixture classified as requiring attach/injection/input/process/network mutation.

### A20. Emergency-stop boundary

Fake `emergency_stop()` may only cancel/release harness-owned work.

A test must prove it cannot create a gameplay/process mutation path.

### A21. Artifact/safety model

Implement Artifact v1 literally for Package A-relevant types and deterministic stores:

- global `control/safety/` logical authority;
- durable ControlState;
- per-run Action/Budget/Recovery safety state;
- incomplete/staging run;
- safety-critical dispatch journal separate from report presentation;
- deterministic flush/finalization;
- manifest provenance/hashes;
- crash -> incomplete, never PASS;
- append-only supplement.

Define the persistence interface so Package B can add the global RequestLedger without changing Package A dispatch/control-state safety semantics.

### A22. Fake adapter

Use deterministic manual clock/state scheduler and fault injection for every required interleaving.

Fake success is never official-client evidence.

## 8. Package A mandatory tests

Package A is not complete until all applicable tests from Scenario/Execution/Artifact contracts pass with `runtime_access:none`, including at minimum:

1. safe bounded JSON scenario acceptance;
2. safe bounded YAML scenario acceptance;
3. duplicate-key rejection;
4. custom YAML tag/object-constructor rejection;
5. alias/depth/size/collection/string/step limits;
6. invalid/non-finite number rejection;
7. canonical scenario hash vector;
8. canonical action-request hash vector;
9. stable explicit/generated step IDs;
10. `SemanticFieldPath` grammar and unknown-schema path rejection;
11. complete `SideEffectBudget` validation/checked bounds;
12. `AbortCondition` discriminant/condition rules;
13. semantic reference union validation and unknown-field rejection;
14. typed predicate UNKNOWN/type mismatch behavior;
15. semantic action parameter validation for every v1 action family;
16. stale/ambiguous semantic selector refusal;
17. unsupported capability refusal;
18. EffectBound generation/refusal when unbounded;
19. read-only mutation refusal;
20. fresh backend epoch on restart;
21. stale backend callback refusal;
22. authority loss exactly before commit;
23. adapter/runtime/session change exactly before commit;
24. two mutation requests serialize;
25. same action ID/hash dispatches at most once;
26. same action ID/different hash conflict;
27. duplicate action creates no second reservation;
28. STOP wins dispatch gate -> durable latch/new generation/no effect;
29. commit wins dispatch gate -> possible-dispatch/at-risk before later STOP;
30. STOP can linearize while action waits for authority;
31. STOP durability failure leaves mutation fail-closed;
32. restart preserves STOP latch;
33. corrupt/missing ControlState refuses mutation;
34. successful reset advances generation and durably clears only STOP latch;
35. reset durability failure leaves STOP latched;
36. dispatch durability barrier failure -> no effect;
37. dispatch durability barrier timeout -> no effect;
38. crash after durable commit before effect -> AMBIGUOUS/no retry;
39. crash after effect before result -> AMBIGUOUS/no retry unless reconciled;
40. budget reservation/exhaustion;
41. budget arithmetic overflow refusal;
42. commit atomically moves reserved -> at-risk;
43. ambiguous consumable/item action consumes conservative budget;
44. explicit retry only after proven NOT_DISPATCHED and uses new action ID;
45. `max_attempts=0` is rejected and omitted retry means one total attempt;
46. pause/resume after session/runtime change refuses pending mutation;
47. wait timeout/cancellation;
48. before-commit versus after-commit cancellation classification;
49. `CONFIRMED` is terminal and cannot be rewritten by a late callback;
50. multi-clock source/ingest ordering stays distinct;
51. ingestion order cannot claim causal order;
52. late event cannot rewrite terminal result;
53. causal fields preserve supplied Track A metadata;
54. secret-shaped event rejected before object creation;
55. unsanitized exception text excluded from safe_message;
56. environment-shaped secret excluded;
57. screenshot unknown/auth-risk quarantined/rejected;
58. passive capture refuses invasive enablement;
59. emergency stop cannot create gameplay/process mutation;
60. artifact crash remains incomplete;
61. finalized result not silently rewritten;
62. fake one-step experiment success;
63. no operator-facing adapter bypass type/interface exists.

## 9. Package B — Control API v1 + browser + CLI

Consume merged Package A.

Before exposing mutation-capable fake operations, select one local persistent safety store that satisfies Artifact-v1 global RequestLedger + ControlState + Action/Budget dispatch-journal semantics.

Implement Control API v1 literally:

- exact loopback bind policy;
- fresh >=256-bit control nonce per backend epoch;
- nonce never in URL/log/artifact/command-line arg;
- all `/v1/*` requests require nonce;
- exact Host allowlist;
- exact same-origin browser Origin policy;
- mandatory CSP `frame-ancestors 'none'` anti-framing;
- no permissive CORS/cookie ambient auth;
- global durable request IDs/hashes;
- atomic `INTENT_DURABLE + minimum resource/control record` before scheduling/domain transition;
- duplicate POST resource/result/transition reuse;
- conservative reset recovery that never auto-unlatches STOP;
- request/page/event/subscriber bounds;
- slow-subscriber backpressure;
- stable safe error envelope;
- graceful shutdown;
- no wildcard/non-loopback mode;
- no raw/debug/adapter endpoint.

Browser and CLI are thin clients of the same backend/domain operations.

Mutating UI controls may execute only against explicit fake adapters in Package B. Real Track A remains read-only/refused.

### Package B mandatory tests

Run every mandatory Control API v1 security/replay test plus:

- browser/CLI semantic parity;
- authority/capability/evidence/freshness shown separately;
- `MUTATION_ALLOWED` is not locally grantable;
- browser reload/new tab cannot duplicate active work;
- UI UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN truthfulness;
- shutdown/restart preserves RequestLedger/ControlState/Action/Budget safety state;
- no real official-client mutation path exists.

## 10. Package C — Surveyor/read-only integration

Only after #592 has an accepted exact producer state.

Pin:

```yaml
surveyor_schema_version:
producer_commit:
producer_interface:
```

Consume outputs; never copy internal logic.

Expose read-only coverage/evidence/runtime/provenance/bundle status.

Schema mismatch -> explicit `UNAVAILABLE/INCOMPATIBLE`.

Control Center cannot promote/overwrite Surveyor-owned evidence state.

## 11. Package D — Official Track A mutation adapter

This prompt does **not** authorize Package D execution.

Package D is a separate runtime-sensitive task.

Before any real action:

1. read then-current trusted-base Track A contracts;
2. create/persist a current runtime admission task;
3. satisfy exact current lease/registration/Gate A/rebind/Gate B/uniqueness/whole-lifetime supervisor rules;
4. satisfy current GUI input lock when applicable;
5. prove action capability/evidence/reference-path parity;
6. produce safe Scenario-v1 EffectBound;
7. acquire Track A guard without holding local dispatch gate;
8. while Track A guard remains held, perform final current Track A checks;
9. immediately before physical effect invoke one-shot durable `commit_dispatch()`;
10. if COMMITTED, perform exactly one physical effect while Track A guard remains held;
11. reconcile action/budget/evidence conservatively.

Start with one smallest already-proven semantic action.

Never build a second Track A authority system.

## 12. Package E — Oteryn v2 adapter

Separate task/branch/PR in:

```text
blakinio/Oteryn-v2
```

Read current Oteryn governance and accepted ADR-0007.

Integrate with its shared E2E architecture or an explicitly versioned cross-repo semantic boundary.

Do not create:

- Tibia wire compatibility shortcut;
- second Oteryn E2E/scenario authority;
- hidden authoritative client mutation;
- unauthenticated production test-control surface.

Retain `protocol-oteryn`; client sends intent; server remains authoritative.

## 13. UI requirements

Always-visible:

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

Quick Actions are exactly one-step experiments through Scenario Engine.

No raw manual mutation shortcut.

## 14. Differential comparison

Use `TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md` literally for comparison profile/result semantics.

Never report Oteryn mismatch when official reference is UNKNOWN/unobservable. Report coverage gap.

Never require byte-level protocol, internal object or renderer equivalence.

## 15. Validation procedure for every package PR

1. inspect exact current main/open PR/task overlap;
2. inspect full final changed-file list and diff;
3. run focused deterministic tests;
4. select commands from current `BUILD_TEST_MATRIX.md`; never invent presets;
5. run required exact-head GitHub checks;
6. perform full self-review for architecture/security/failure paths/claims;
7. re-run race/idempotency/durability/privacy tests after related changes;
8. obtain independent review when current risk policy requires it;
9. record exact commands/outcomes/SHA in task/PR;
10. update `MODULE_CATALOG.md`/`CHANGELOG.md` when required and resolve live path ownership;
11. merge only through current repository policy.

## 16. Mandatory non-claims

Never claim:

- official-client action capability from fake tests;
- Track A authority from Control Center/API state;
- runtime compatibility from repository-only tests;
- causal proof from timing/ingest ordering alone;
- no external effect merely because result call timed out;
- safe retry after durable possible-dispatch without authoritative no-effect proof;
- passive capture when enablement actually attaches/injects/mutates;
- STOP reversal of already-committed effect;
- backend restart as implicit STOP reset;
- request replay safety unless request/resource intent is durably ordered before scheduling;
- remote/LAN security from loopback API design;
- safe secret handling from export-time redaction alone;
- Oteryn parity before separate adapter/evidence exists.

## 17. Package A terminal acceptance

```text
runtime_access=none
network_listener=none
official_client_access=none
Scenario v1 parser/hash/action/reference/budget/abort semantics=PASS
backend epoch/generation fencing=PASS
durable ControlState/STOP/reset recovery=PASS
MutationCoordinator serialization=PASS
STOP-vs-commit linearizability=PASS
bounded local durability-before-effect=PASS
ActionLedger idempotency=PASS
terminal CONFIRMED lifecycle=PASS
BudgetLedger at-risk/uncertain accounting=PASS
crash/restart ambiguity handling=PASS
multi-clock Recorder=PASS
construction-time secret exclusion=PASS
capture/emergency-stop bypass tests=PASS
artifact finalization=PASS
no adapter/operator bypass=PASS
all mandatory deterministic tests=PASS
self-review=no material findings
required independent review=PASS
exact-head CI=PASS
```

A fresh competent agent must be able to continue solely from Git/task/PR without this chat.

## 18. Desired first operator result

After Packages A-C the operator can:

- launch Control Center locally;
- use browser or CLI through the same secured loopback backend;
- inspect truthful read-only Track A/Surveyor status;
- see authority/capability/evidence/freshness separately;
- browse scenarios/runs/actions/events/artifacts;
- run deterministic fake one-step experiments;
- prove STOP/idempotency/durability/restart/privacy behavior;
- export privacy-safe `agent_bundle.json`;

while every real official-client mutation remains fail-closed until a separately admitted Package D exists.