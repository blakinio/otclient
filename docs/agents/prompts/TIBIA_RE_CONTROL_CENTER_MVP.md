# TIBIA-RE-CONTROL-CENTER-MVP

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

Do not prematurely implement an unrestricted gameplay bot. Preserve the stable future policy boundary while deterministic safety/authority remains outside any policy/model.

## 2. Normative design package

Read in full before editing:

```text
docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
```

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
6. inspect current Surveyor producer/prompt status and do not assume merge/interface stability from historical PR numbers;
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

Future policy/automation is a downstream consumer only:

```text
Normalized Observation -> Policy Decision -> bounded semantic proposal
                       -> ordinary Control Center domain/Scenario path
                       -> deterministic Safety/Authority -> Adapter -> Recorder -> Result
```

Forbidden:

```text
CLI -> concrete adapter
Browser -> raw action/debug endpoint
Quick Action -> raw keyboard/mouse/bridge call
Scenario -> direct Track A lease/registration mutation
Recorder/Artifact Store -> evidence promotion
Passive capture -> hidden attach/injection/input mutation
STOP -> new gameplay/process-control action
Policy/model -> credentials/shell/process/raw-memory/raw-input/concrete adapter
Policy/model -> direct Track A authority or safety bypass
```

## 6. Package split

Do not implement all phases in one PR.

```text
Package A  control-core + Scenario/Execution/Recorder + fake adapter/durability tests
Package B  Control API v1 + browser + CLI + persistent safety/request store
Package C  accepted Surveyor/read-only integration
Package D  separately admitted official Track A mutation adapter
Package E  separately governed Oteryn-v2 adapter
Future     policy/automation consumer only after stable research interfaces; never a safety authority
```

## 7. Package A — control-core

Recommended path only after confirming repository conventions:

```text
tools/tibia_re_control_center/
```

### A1. Contract types/version negotiation

Implement typed models for:

- Scenario v1;
- Execution v1;
- Adapter v1;
- Artifact v1 safety/result records required by Package A;
- adapter/execution/scenario/artifact major-version negotiation;
- generic capabilities;
- official-only evidence extension;
- runtime/freshness/snapshot state;
- events/artifacts/ledgers.

Preserve the Policy Boundary v1-compatible normalized observation/action/result interfaces without implementing an autonomous policy loop in Package A.

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
- typed `SideEffectBudget`, `AbortCondition`, `SemanticFieldPath` and closed semantic reference unions;
- action-specific parameter schemas;
- semantic selectors only;
- typed predicates with no implicit coercion;
- deterministic abort/privacy/capture policies.

### A3. Canonical hashes and step IDs

Implement JCS/RFC-8785 canonicalization exactly as Scenario v1 defines.

Verify known deterministic vectors for:

- scenario hash;
- action request hash;
- explicit local step IDs;
- generated ordinal step IDs.

Runtime fences/timestamps/current authority are not part of semantic action hash.

### A4. EffectBound

Before reservation, obtain deterministic finite maximum plausible effect per action.

Fake adapter must support exact EffectBound fixtures.

If any required hard effect cannot be bounded, refuse before dispatch.

### A5. Backend epoch/control generation and activation marker

- create a fresh unique backend epoch for every simulated backend lifetime;
- control generation is monotonic only within that epoch;
- STOP advances generation;
- no wrap/reuse on overflow;
- stale old-epoch callbacks cannot control new work;
- load global Artifact-v1 ControlState before mutation admission;
- durably mark `active_backend_epoch=<current>` before admitting mutation;
- prior non-null different active backend => unclean lifetime => `recovery_required=true` and mutation disabled until explicit recovery/reset;
- active-marker durability failure => mutation disabled.

### A6. MutationCoordinator

Exactly one coordinator per adapter instance.

It owns:

- one-at-a-time mutation commit;
- ActionLedger;
- BudgetLedger;
- backend-global STOP/reset/recovery ControlState;
- `dispatch_gate`;
- one-shot `commit_dispatch()`.

It does not own Track A authority.

### A7. Dispatch gate discipline

Never hold `dispatch_gate` while waiting for external/fake authority, GUI locks, capture, network or arbitrary I/O.

The only I/O permitted while holding it is one of two bounded local safety transactions defined by Execution v1:

1. ActionLedger/BudgetLedger possible-dispatch/at-risk write-ahead commit;
2. backend-global ControlState STOP or explicit reset transition.

Both have deterministic finite timeout/failure paths and no external network dependency. No report/capture/general persistence work is permitted under the gate.

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
- `CONFIRMED` is terminal successful lifecycle state and cannot be rewritten by late callbacks.

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

Before dispatch reserve Scenario-v1 EffectBound against the explicit SideEffectBudget.

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
3. verify backend/control generation;
4. verify durable + in-memory STOP/recovery-required/cancellation state;
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
STOP first -> in-memory STOP -> durable global STOP/control generation -> stale commit refused -> no effect
commit first -> possible-dispatch/at-risk durable -> STOP sees already committed work
```

STOP remains durably latched across backend restart until explicit durable reset.

STOP persistence failure leaves the current process mutation-disabled. Because the backend-active marker was already durable before mutation admission, a later crash/restart must detect an unclean prior lifetime and remain recovery-required/mutation-disabled rather than reopening work.

STOP then cancels queued/waiting work and harness-owned passive captures, but grants no new external action.

### A13. Reset/recovery

Reset is local only and runs its ControlState transition under the dispatch gate.

It does not restore cached authority and must respect unresolved AMBIGUOUS overlapping side-effect domains.

It may clear STOP/recovery-required only after relevant Action/Budget/Request safety state is consistent and the clear transition is durable. Durability failure leaves mutation blocked.

### A14. Restart/crash recovery

Deterministic store must simulate:

- crash before dispatch commit;
- dispatch durability failure;
- crash after durable commit before effect;
- crash after effect before result;
- STOP persistence failure followed by crash;
- backend-active marker durability failure;
- unclean backend restart with prior active marker;
- reset persistence failure;
- corrupt/missing/contradictory ControlState/ledger.

Expected classes:

```text
NOT_DISPATCHED
POSSIBLY_DISPATCHED -> AMBIGUOUS unless reconciled
CONFIRMED
```

On every restart use a fresh backend epoch, load/validate global control state, classify an uncleared prior active backend as recovery-required, durably install the current active marker, then recover per-run safety state before any mutation admission.

No automatic mutation resume/retry.

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

Late events enrich evidence only; they cannot rewrite terminal results or restart execution.

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

### A21. Artifact model

Support Artifact v1 literally for Package A scope:

- backend-global durable ControlState including STOP/recovery/active-backend marker;
- incomplete/staging run;
- per-run safety-critical dispatch journal separate from report presentation;
- deterministic flush/finalization;
- manifest provenance/hashes;
- crash -> incomplete, never PASS;
- append-only supplement.

RequestLedger storage/types may be introduced in A if the persistence abstraction benefits from one shared global store, but Package B is the first package required to expose/consume transport request IDs.

### A22. Fake adapter

Use deterministic manual clock/state scheduler and fault injection for every required interleaving.

Fake success is never official-client evidence.

## 8. Package A mandatory tests

Package A is not complete until all pass with `runtime_access:none`:

1. safe bounded JSON scenario acceptance;
2. safe bounded YAML scenario acceptance;
3. duplicate-key rejection;
4. custom YAML tag/object-constructor rejection;
5. alias/depth/size/collection/string/step limits;
6. invalid/non-finite number rejection;
7. canonical scenario hash vector;
8. canonical action-request hash vector;
9. stable explicit/generated step IDs;
10. typed predicate UNKNOWN/type mismatch behavior;
11. semantic action parameter validation for every v1 action family;
12. stale/ambiguous semantic selector refusal;
13. unsupported capability refusal;
14. EffectBound generation/refusal when unbounded;
15. read-only mutation refusal;
16. fresh backend epoch on restart;
17. stale backend callback refusal;
18. authority loss exactly before commit;
19. adapter/runtime/session change exactly before commit;
20. two mutation requests serialize;
21. same action ID/hash dispatches at most once;
22. same action ID/different hash conflict;
23. duplicate action creates no second reservation;
24. STOP wins dispatch gate -> no effect;
25. commit wins dispatch gate -> possible-dispatch/at-risk before STOP;
26. STOP can linearize while action waits for authority;
27. durability barrier failure -> no effect;
28. durability barrier timeout -> no effect;
29. crash after durable commit before effect -> AMBIGUOUS/no retry;
30. crash after effect before result -> AMBIGUOUS/no retry unless reconciled;
31. budget reservation/exhaustion;
32. budget arithmetic overflow refusal;
33. commit atomically moves reserved -> at-risk;
34. ambiguous consumable/item action consumes conservative budget;
35. explicit retry only after proven NOT_DISPATCHED and uses new action ID;
36. pause/resume after session/runtime change refuses pending mutation;
37. wait timeout/cancellation;
38. before-commit versus after-commit cancellation classification;
39. multi-clock source/ingest ordering stays distinct;
40. ingestion order cannot claim causal order;
41. late event cannot rewrite terminal result;
42. causal fields preserve supplied Track A metadata;
43. secret-shaped event rejected before object creation;
44. unsanitized exception text excluded from safe_message;
45. environment-shaped secret excluded;
46. screenshot unknown/auth-risk quarantined/rejected;
47. passive capture refuses invasive enablement;
48. emergency stop cannot create gameplay/process mutation;
49. artifact crash remains incomplete;
50. finalized result not silently rewritten;
51. fake one-step experiment success;
52. no operator-facing adapter bypass type/interface exists;
53. typed SideEffectBudget/AbortCondition/SemanticFieldPath/closed destination schemas reject invalid/free-form inputs;
54. `CONFIRMED` is terminal successful state and stale/duplicate callbacks cannot rewrite/redispatch it;
55. durable STOP ControlState survives clean backend restart and refuses mutation until reset;
56. reset durability failure leaves STOP/recovery-required blocking mutation;
57. backend-active marker must be durable before mutation admission;
58. prior uncleared active-backend marker forces recovery-required on the next backend;
59. STOP persistence failure followed by crash cannot reopen mutation after restart;
60. clean-shutdown marker failure causes conservative recovery-required next start;
61. missing/corrupt initialized ControlState is fail-closed.

## 9. Package B — Control API v1 + browser + CLI

Consume merged Package A.

Before exposing mutation-capable fake operations, select/extend the local persistent store so it satisfies:

- backend-global ControlState;
- backend-global RequestLedger;
- per-run Action/Budget dispatch-journal semantics;
- Artifact-v1 safety-state precedence.

Implement Control API v1 literally:

- exact loopback bind policy;
- fresh >=256-bit control nonce per backend epoch;
- nonce never in URL/log/artifact/command-line arg;
- all `/v1/*` requests require nonce;
- exact Host allowlist;
- exact same-origin browser Origin policy;
- no permissive CORS/cookie ambient auth;
- durable request IDs/hashes;
- preallocate final logical resource ID and durably persist RequestLedger ACCEPTED **before** resource-creating domain execution;
- crash after ACCEPTED-before-create and crash after create-before-COMPLETED both replay to the same resource ID;
- duplicate POST resource/result reuse;
- request/page/event/subscriber bounds;
- slow-subscriber backpressure;
- stable safe error envelope;
- graceful shutdown preserving global/per-run safety state;
- no wildcard/non-loopback mode;
- no raw/debug/adapter endpoint.

Browser and CLI are thin clients of the same backend/domain operations.

Mutating UI controls may execute only against explicit fake adapters in Package B. Real Track A remains read-only/refused.

### Package B mandatory tests

Run every mandatory test defined by current Control API v1 plus:

- browser/CLI semantic parity;
- authority/capability/evidence/freshness shown separately;
- `MUTATION_ALLOWED` is not locally grantable;
- browser reload/new tab cannot duplicate active work;
- UI UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN truthfulness;
- shutdown/restart preserves ControlState/RequestLedger/Action/Budget safety state;
- no real official-client mutation path exists.

## 10. Package C — Surveyor/read-only integration

Only after the current Surveyor work has an accepted exact producer state.

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

Use `TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md` and the programme's versioned semantic comparison profile.

Never report Oteryn mismatch when official reference is UNKNOWN/unobservable. Report coverage gap.

Never require byte-level protocol, internal object or renderer equivalence.

## 15. Future policy/automation preparation

Do not implement an unrestricted policy loop as a convenience feature of Package A/B/C.

Preserve `TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md`:

```text
ObservationPort -> normalized non-secret state
PolicyIngress   -> untrusted bounded semantic proposal
ResultPort      -> canonical accepted/refused/result/evidence projection
```

A future policy/Ollama engine must re-enter the ordinary Scenario/ActionRequest/domain path. It never receives credentials, Control API nonce, direct adapter handles, shell/process/raw-memory/unrestricted-input authority or Track A writable authority.

Deterministic code, outside the policy/model, owns schema validation, rate limits, budgets, idempotency, STOP, recovery, capability/freshness checks and final external authority.

Model failure/unavailability must not disable manual research, STOP or deterministic safety.

## 16. Validation procedure for every package PR

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

## 17. Mandatory non-claims

Never claim:

- official-client action capability from fake tests;
- Track A authority from Control Center/API state;
- runtime compatibility from repository-only tests;
- causal proof from timing/ingest ordering alone;
- no external effect merely because result call timed out;
- safe retry after durable possible-dispatch without authoritative no-effect proof;
- passive capture when enablement actually attaches/injects/mutates;
- STOP reversal of already-committed effect;
- restart as an implicit STOP/recovery reset;
- remote/LAN security from loopback API design;
- safe secret handling from export-time redaction alone;
- policy/model output as authority/capability/evidence;
- Oteryn parity before separate adapter/evidence exists.

## 18. Package A terminal acceptance

```text
runtime_access=none
network_listener=none
official_client_access=none
Scenario v1 parser/hash/action semantics=PASS
backend epoch/generation fencing=PASS
backend activation/unclean-restart recovery=PASS
MutationCoordinator serialization=PASS
STOP-vs-commit linearizability=PASS
durable STOP/reset/recovery state=PASS
bounded local durability-before-effect=PASS
ActionLedger idempotency=PASS
BudgetLedger at-risk/uncertain accounting=PASS
crash/restart ambiguity handling=PASS
multi-clock Recorder=PASS
construction-time secret exclusion=PASS
capture/emergency-stop bypass tests=PASS
artifact finalization=PASS
future Policy Boundary remains downstream/no-bypass=PASS
no adapter/operator bypass=PASS
all mandatory deterministic tests=PASS
self-review=no material findings
required independent review=PASS
exact-head CI=PASS
```

A fresh competent agent must be able to continue solely from Git/task/PR without this chat.

## 19. Desired first operator result

After Packages A-C the operator can:

- launch Control Center locally;
- use browser or CLI through the same secured loopback backend;
- inspect truthful read-only Track A/Surveyor status;
- see authority/capability/evidence/freshness separately;
- browse scenarios/runs/actions/events/artifacts;
- run deterministic fake one-step experiments;
- prove STOP/idempotency/durability/restart/privacy behavior;
- export privacy-safe `agent_bundle.json`;

while every real official-client mutation remains fail-closed until a separately admitted Package D exists and every future policy/automation consumer remains downstream of the deterministic Control Center boundary.