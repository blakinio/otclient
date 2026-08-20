# TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT

```yaml
prompt_contract:
  version: 2.1.0
  prompting_standard_version: 2.1
  alias: TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT
  track_id: official-client-re
  task_kind: independent_architecture_security_audit
  risk: high
  run_scope: single_task
  continuation_policy: stop_at_task_boundary
  task_completion_policy: checkpoint_only
  user_communication: low_noise
  implementation_authorized: false
  objective: Falsify Control Center architecture and Package A readiness on one exact immutable head without modifying repositories or touching the official-client runtime.
  baseline_version: pre-repair audit prompt at PR #605 head 5e63a0ec988cf4fa7789274f13c9d654254e8e44
  eval_suite: docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
  rollback_version: restore the pre-repair audit prompt blob 4ae856ecf7369c1f8183d74f030eb88f0f1273d3
  feature_scope:
    type: documentation
    user_facing: false
    backend_required: false
    frontend_required: false
    integration_required: false
    e2e_required: false
    completion_claim: internal_only
```

Recommended reasoning effort: high / maximum.

Act as a **fresh independent read-only architecture, security, concurrency, durability, privacy and implementation-readiness auditor**.

Repository:

```text
https://github.com/blakinio/otclient
```

Use live connected GitHub state as source of truth. Do not trust conclusions from authors, implementers, prior reviews or this prompt's historical anchors.

## 1. Absolute execution boundary

This audit is `runtime_access:none`.

Do not:

- modify files;
- commit, push, merge or resolve findings;
- create replacement architecture;
- perform Track A runtime actions;
- launch/control Tibia;
- access credentials/secrets;
- log in or perform gameplay;
- write to `blakinio/Oteryn-v2`.

## 2. Freshness/discovery

Historical discovery anchors only:

```text
original design PR       #600
original design merge    ada65af85a872e2df43469f5687418fc5647811a
original closeout PR     #601
original closeout merge  5817f1ad699c2d68dfb1a03886dc8c20dace67e7
audit prompt PR          #602
hardening PR             #605 or successor/current state
```

Before relying on any:

1. fetch exact current `main`;
2. verify merge/open state and exact SHAs for relevant PRs;
3. identify later Control Center work;
4. verify exact audited blobs;
5. inspect open PRs/tasks for overlapping Control Center, Surveyor, runtime bridge, Track A authority, persistence/API/E2E work;
6. if auditing an open #605, require its exact head to be based on/reconciled with current main and report any drift;
7. use live state, not stale PR prose.

If the hardening is still open and the owner asks for that PR/head, audit that exact unchanged head against current main. Head movement after review invalidates readiness evidence.

## 3. Mandatory Control Center files

Read all in full:

```text
docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
```

Also read current hardening task/checkpoint and this audit prompt.

## 4. Mandatory repository governance/dependencies

Read/inspect current:

```text
AGENTS.md
docs/agents/README.md
docs/agents/AGENTS.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
current canonical lease/registration/Gate A/rebind/Gate B/bootstrap/whole-lifetime-supervisor contracts
current GUI input-lock/activity-heartbeat contracts/helpers
docs/agents/MODULE_CATALOG.md
docs/agents/REPOSITORY_MAP.md
docs/agents/KNOWN_RISKS.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CROSS_REPO_CONTRACTS.md
```

Inspect current:

- PR #592 / current Surveyor producer state;
- `tools/tibia_re_surveyor/**` if accepted/present;
- `tools/tibia_runtime_bridge/**`;
- canonical Track A authority/input helpers;
- existing scenario/recorder/persistence/API/CLI/fake/idempotency infrastructure.

For `blakinio/Oteryn-v2`, read-only inspect current main, applicable `AGENTS.md`, accepted ADR-0007, relevant security/architecture docs, client/test interfaces and production/test-build restrictions.

Do not treat historical `otclient/oteryn-client/**` as canonical.

## 5. Evidence labels

Use explicitly:

```text
FACT       directly verified
INFERENCE  derived from verified facts
UNKNOWN    evidence unavailable/missing
```

A prose intention is not a sufficient implementation contract unless two competent independent implementers can produce materially compatible safety behavior without inventing core semantics.

A test list does not cure ambiguous normative semantics.

## 6. Primary objective

Determine whether the design is:

1. architecturally sound;
2. implementable without material redesign/invention;
3. integrated with existing Track A without duplication;
4. fail-closed at irreversible mutation boundary;
5. linearizable under STOP/concurrent dispatch;
6. idempotent under duplicate HTTP/browser/CLI/action submission;
7. crash-safe against duplicate resources or side effects;
8. conservative/enforceable for runtime and value budgets;
9. deterministic/bounded at parser/semantic-registry layer;
10. privacy-safe before normal object creation;
11. truthful for multi-source causal evidence;
12. secure enough for local browser/CLI operation;
13. safe against cross-origin/DNS-rebinding/clickjacking;
14. incapable of hiding mutation in capture/cleanup;
15. compatible with Oteryn ADR-0007 without second E2E authority;
16. suitable for semantic differential E2E;
17. sufficiently specified for Package A with zero Track A runtime access.

## 7. Non-negotiable invariants

```text
scenario validity
!= semantic registry support
!= capability support
!= evidence maturity
!= freshness
!= mutation authority
```

```text
Browser ----\
             -> one Control API/domain service -> Run Manager -> Scenario Engine -> MutationCoordinator -> Adapter
CLI --------/
```

```text
backend restart -> fresh backend_epoch
fresh backend_epoch != implicit STOP reset
old callbacks cannot control new execution
```

```text
STOP wins dispatch_gate -> durable STOP/new generation -> no stale dispatch
commit wins dispatch_gate -> POSSIBLY_DISPATCHED + applicable non-time AT_RISK durable before later STOP
```

```text
physical mutation requires successful one-shot durable dispatch commit
```

```text
request_id -> transport/domain dedupe
resource_id -> stable durable run/experiment identity
action_id -> semantic attempt dedupe
RequestLedger + ResourceIdentityRecord durable before scheduling
```

```text
POSSIBLY_DISPATCHED without authoritative terminal proof -> AMBIGUOUS
AMBIGUOUS -> no automatic retry
```

```text
secret-class data never enters normal Event/Artifact/Error/Report/AgentBundle
```

```text
ingest order != source causal order
```

```text
passive capture != attach/inject/input/mutation authority
STOP != compensating gameplay/process authority
```

```text
loopback bind != browser trust
Host + Origin + current nonce required
UI framing forbidden
```

Any safety-relevant violation is at least P1 and P0 when it can cause unauthorized mutation, secret exposure or uncontrolled irreversible/value effect.

## 8. Audit A — repository fit/duplication

Classify each as `REUSE_EXISTING | EXTEND_EXISTING | NEW_COMPONENT_JUSTIFIED | DUPLICATE_OR_CONFLICTING | UNKNOWN`:

- Scenario Engine;
- SemanticFieldRegistry;
- MutationCoordinator;
- Safety Controller;
- Recorder;
- Artifact Store;
- global RequestLedger/ResourceIdentityLedger/ControlState;
- Action/Budget/Recovery persistence;
- Adapter API;
- Control API;
- fake adapter;
- Surveyor integration;
- runtime bridge integration;
- Track A lease/registration/Gates/supervisor/input lock;
- Oteryn adapter/E2E integration.

Verify no second Track A authority/evidence source and no second Oteryn E2E authority.

## 9. Audit B — Scenario/parser/semantic-registry determinism

Verify exact contract for:

- JSON/YAML -> same typed AST;
- document/depth/string/collection/step bounds;
- duplicate-key/custom-tag/object-constructor rejection;
- bounded/disabled aliases;
- UTF-8 and non-finite/out-of-domain rejection;
- RFC 8785 JCS + SHA-256 scenario/action hashes;
- deterministic step IDs;
- exact `SemanticFieldPath` grammar;
- immutable `SemanticFieldRegistry` schema, ID/version, descriptor type/cardinality/allowed-op semantics;
- deterministic built-in core registry;
- extension registry binding in scenario hash;
- adapter descriptor/registry JCS hash validation;
- unregistered path rejection vs registered runtime UNKNOWN distinction;
- typed predicates without coercion;
- exact `SideEffectBudget`;
- absolute runtime deadline;
- exact `AbortCondition`;
- retry total-attempt semantics with zero rejected;
- retry only after proven NOT_DISPATCHED;
- discriminated `EntityRef`, `ItemRef`, `DestinationRef`;
- `SNAPSHOT_PATH` includes explicit retained checkpoint and registry-compatible ENTITY_REF/ITEM_REF type;
- action-specific parameter schemas;
- finite EffectBound including bounded runtime fit;
- capture/privacy policy.

Flag any core field whose semantics remain materially free-form.

## 10. Audit C — final authority/dispatch

Expected sequence:

```text
prepare outside dispatch_gate
-> hold external authority guard where required
-> final checks + bounded local safety commit under dispatch_gate
-> physical effect while external guard remains continuously held
```

Do not accept advisory preflight as authority.

Verify gate not held waiting for Track A/external locks.

At final commit verify:

- action ID/hash;
- run ownership;
- backend/control generation;
- recovered/unlatched ControlState;
- cancellation;
- adapter/runtime/session fences;
- selected semantic registry still supported/matching;
- remaining runtime deadline/non-time budget;
- capability;
- current external authority;
- input lock;
- current Official Track A identity/authority requirements.

Official external guard remains held through local commit and physical effect.

## 11. Audit D — durability-before-effect / local safety store

Before physical effect require:

```text
DISPATCH_COMMITTED
POSSIBLY_DISPATCHED
applicable non-time budget AT_RISK
backend/control/action/hash/fence provenance
successful local durability barrier
```

Under `dispatch_gate` only:

```text
DISPATCH_COMMIT
STOP_TRANSITION
RESET_TRANSITION
```

Verify finite deadline, no external network dependency, dispatch timeout -> no effect, STOP write failure -> fail closed, reset write failure -> STOP remains latched, crash after commit -> AMBIGUOUS unless reconciled, presentation failure cannot erase safety state.

## 12. Audit E — STOP/concurrency/restart

Verify:

- one STOP-vs-commit linearization gate;
- durable ControlState;
- checked generation/overflow;
- queued old-generation cancellation;
- STOP while action waits for authority;
- active waits/captures;
- already-committed conservative classification;
- stale callback evidence-only handling;
- explicit durable reset;
- reset does not clear ambiguous Action/Budget state;
- restart with latched STOP remains STOPPED;
- explicit first-store initialization;
- missing/corrupt/contradictory ControlState -> fail closed;
- multiple tabs/browser+CLI/multiple runs;
- read-only concurrency only when proven safe.

Reject implicit restart reset or vague cancellation ordering.

## 13. Audit F — Action/Request/Resource idempotency

ActionLedger:

- globally unique action ID;
- canonical action hash;
- same-ID/same-hash existing result;
- same-ID/different-hash conflict;
- no duplicate non-time reservation;
- retry uses new ID;
- no retry after possible dispatch;
- `CONFIRMED` terminality.

Request/Resource safety:

- request ID distinct from action ID;
- canonical method/path/body request hash;
- global RequestLedger;
- global ResourceIdentityLedger;
- stable run/experiment/action IDs allocated before scheduling;
- atomic/equivalent `RequestLedger INTENT_DURABLE + ResourceIdentityRecord CREATED_NOT_SCHEDULED` before resource scheduling;
- same request/hash -> same resource;
- same request/different hash -> conflict;
- `POST /runs` replay -> same run ID;
- one-step replay -> same experiment/run/action IDs;
- crash after durable pair but before scheduling -> same identity, no auto-resume;
- corrupt/uncertain pair -> RECOVERY_REQUIRED, no replacement;
- STOP/reset transition IDs are stable;
- uncertain reset remains latched;
- safety records retained long enough to prevent duplicate side effects/resources.

## 14. Audit G — budgets/runtime

Verify Scenario hard dimensions include runtime/actions/movement/spells/consumables/items/gold/TC/irreversible.

Runtime:

- absolute monotonic deadline fixed at run start;
- pause/retry/ambiguity do not extend;
- action/wait must fit remaining runtime;
- no cross-backend monotonic continuation is invented because mutation runs do not auto-resume.

Non-time dimensions:

```text
limit
reserved
at_risk
committed
uncertain
```

Verify reserve-before-dispatch, atomic at-risk transition, conservative ambiguity, checked arithmetic, duplicate/retry behavior. Unbounded hard effect refuses.

## 15. Audit H — pause/restart/stale work

Verify pause does not freeze runtime deadline or external authority, resume revalidates all fences/registry/predicates, session/runtime/registry change invalidates pending mutation, fresh backend epoch, old-epoch callback refusal, no auto-resume, correct NOT_DISPATCHED/POSSIBLY_DISPATCHED/CONFIRMED recovery, corrupt safety state fail closed.

## 16. Audit I — Recorder/causal evidence

Verify distinction/preservation of:

- ingest sequence/time;
- source timestamp/clock domain;
- source sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session fences;
- late status;
- stimulus/BACKGROUND;
- direction/message sequence/type/lane;
- thread/handler/runtime object/object epoch;
- before/after hashes;
- semantic delta/evidence ref;
- negative/no-stimulus linkage.

Ingest order cannot be represented as universal causal order.

## 17. Audit J — privacy before object creation

Falsify against credentials/2FA, session/auth tokens, cookies/tickets, encryption material, private chat/identity, env values, raw packet payloads, trace strings, exception/repr/debug text, login screenshots and Control API nonce.

Required:

```text
classification/redaction/rejection BEFORE normal persistent-object construction
```

`SECRET_REJECTED` contains category/reason only. Export-only redaction is insufficient.

## 18. Audit K — capture/emergency bypass

Ordinary snapshot/semantic-field/wait/capture paths are observational only. If enablement needs attach/injection/input/process/network mutation, passive path must refuse and route to separately governed mutation action.

`emergency_stop()` cannot initiate gameplay stop/input, kill/signal/restart, attach/detach or network/client mutation.

## 19. Audit L — network capture

Default persistent path: direction, lane, source-local sequence when known, structurally known type only, size, correlation ID, `payload_capture=NONE`. No raw fallback. Future payload mode requires separately approved pre-persistence sanitization.

## 20. Audit M — Artifact/finalization

Verify:

- global Request/Resource/Control safety authority vs per-run Action/Budget/Recovery;
- semantic schema ID/version/hash provenance in manifest/bundle;
- ACTIVE -> CLOSING -> FINALIZED;
- bounded drain/watermarks;
- late evidence cannot rewrite terminal result;
- crash/incomplete state;
- immutable finalized result + append-only supplements;
- no synthetic PASS;
- presentation failure cannot alter safety state;
- retention cannot remove safety records still needed for replay/ambiguity/STOP.

## 21. Audit N — Control API security

Verify:

- default exact `127.0.0.1`;
- wildcard/non-loopback rejected;
- explicit-only `::1`;
- fresh >=256-bit nonce per backend epoch;
- nonce absent URL/query/fragment/log/artifact/CLI argv;
- all `/v1/*` nonce-authenticated;
- exact Host including port;
- arbitrary loopback-resolving DNS name rejected;
- exact same-origin browser Origin;
- no permissive/reflected CORS;
- no cookie ambient auth;
- CLI missing Origin still needs Host+nonce;
- CSP `frame-ancestors 'none'` mandatory and not ordinary-configurable away;
- bounded bodies/headers/pages/events/subscribers;
- deterministic slow-consumer handling;
- safe errors;
- no raw/debug/eval/adapter endpoint;
- remote/LAN unsupported;
- shutdown flushes safety state and invalidates nonce.

Determine whether hostile direct requests, DNS rebinding or clickjacking can control the backend.

## 22. Audit O — browser/CLI parity

Both use one domain implementation. CLI cannot call concrete adapters directly. Browser reload/new tab recovers backend-owned state instead of creating duplicate work.

## 23. Audit P — UI truthfulness

Required tabs:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Always distinguish `AUTHORITY`, `CAPABILITY`, `EVIDENCE`, `FRESHNESS` and semantic-schema support. `MUTATION_ALLOWED` is not locally grantable. UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN remain truthful. Quick Actions are one-step scenarios.

## 24. Audit Q — Official adapter

Generic support uses independent `read_supported`/`action_supported`; semantic registry support is separately negotiated. Official-only evidence uses R0-R4/A0-A4. Scenarios hide raw coordinates/keys/QMeta/addresses/vtables/opcodes/wire layouts. Official adapter extends existing Track A rather than duplicating authority.

## 25. Audit R — Surveyor

Package C pins exact `surveyor_schema_version`, `producer_commit`, `producer_interface`. Mismatch -> unavailable/incompatible. No copied fallback or Control Center promotion of Surveyor-owned evidence.

## 26. Audit S — Oteryn v2

Verify accepted ADR-0007 remains authority: `protocol-oteryn`, client intent/server authority, one E2E/scenario platform, no hidden authoritative client mutation, no unauthenticated production test control, test-only production exclusion, versioned cross-repo boundary, no Track A grades on generic Oteryn capability.

## 27. Audit T — differential E2E

Verify comparison classes:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

At minimum position, HP, mana, conditions, target, inventory, containers, equipment, cooldown state/timing, visual effects, pixels, latency, protocol bytes, internal layout, renderer implementation. UNKNOWN/unobservable reference -> coverage gap, not mismatch.

## 28. Audit U — phasing/Package A readiness

Expected order:

```text
P0 repaired contracts/falsification
P1 Package A control-core + Scenario/Execution/Adapter/Artifact/Recorder/fake durability
P2 Package B local Control API/browser/CLI/global Request+Resource safety store
P3 Package C accepted Surveyor/read-only
P4 Package D separately admitted official adapter
P5 capture producers
P6 research suites
P7 Oteryn adapter
P8 differential E2E
```

Package A must remain:

```text
runtime_access=none
network_listener=none
official_client_access=none
```

## 29. Mandatory falsification matrix

For each return `SAFE_DEFINED | UNSAFE | UNDERSPECIFIED` plus exact contract evidence.

1. Authority expires immediately before dispatch commit -> refuse.
2. Client restarts between preflight and execute -> stale fences refuse.
3. Two browser tabs start mutation scenarios -> one adapter mutation-run owner.
4. CLI/browser submit same action ID/hash -> at most one dispatch.
5. STOP races with commit -> exactly one durable gate order.
6. Event arrives after terminal -> evidence only.
7. Screenshot may contain credentials -> quarantine/refusal before normal artifact.
8. Adapter exception contains secret -> raw text excluded.
9. Sources use different clocks -> no false total causal order.
10. Potion result lost and same action retried -> no second dispatch; conservative budget.
11. Oteryn field unobservable officially -> coverage gap.
12. Official A4/R1 -> independent truthfulness.
13. Surveyor schema changes -> pinned incompatibility.
14. HTTP repeats same action POST after connection loss -> same resource/action.
15. Authority changes while paused -> resume/final commit revalidate.
16. Session epoch changes while paused -> pending mutation invalidated.
17. Browser reload during active run -> backend-owned state, no duplicate.
18. Backend restarts with possible action -> fresh epoch; AMBIGUOUS/no retry.
19. Same action ID different parameters -> conflict.
20. STOP then stale callback PASS -> evidence only, no advance.
21. Ambiguous item/gold consumes remaining budget -> overlapping action refused when exceeded.
22. Recorder/report crashes before result flush -> incomplete, never synthetic PASS.
23. Auth packet under metadata capture -> no raw payload persistence.
24. Oteryn test adapter in production-default -> policy prevents/flags.
25. Dispatch durability barrier fails -> no effect.
26. Crash after durable commit before effect -> AMBIGUOUS unless authoritative no-effect proof.
27. New backend uses same numeric generation -> backend epoch fences stale work.
28. Action waits for Track A guard while STOP occurs -> STOP linearizes; later commit stale.
29. Malicious YAML duplicate keys/custom tags/alias amplification -> reject/bound.
30. Map-key-order-only difference -> same JCS hash.
31. Retry after DISPATCH_COMMITTED -> refuse.
32. Passive capture needs debugger attach -> refuse hidden attach.
33. emergency_stop tries gameplay input/kill -> forbidden.
34. Hostile website direct loopback request -> Origin+nonce reject.
35. DNS rebinding Host -> exact Host reject.
36. Prior-backend nonce replay -> reject.
37. POST /runs accepted then crash before scheduling/response -> durable RequestLedger+ResourceIdentityRecord already fix same run ID; replay returns same ID; no auto-resume.
38. Same request ID different body -> conflict.
39. Slow subscriber fills queue -> bounded disconnect/resync, no execution blockage.
40. `0.0.0.0` bind -> refuse.
41. Dispatch safety store stalls -> finite timeout, no effect, STOP not indefinitely blocked.
42. Capture cleanup introduces invasive detach/signal -> refuse absent separate authority.
43. STOP latched then backend restart -> new backend remains STOPPED until durable reset.
44. STOP durability write fails -> current/restarted system fail closed.
45. Reset durability write fails -> STOP remains latched.
46. Reset request uncertain after crash -> no auto-reset; RECOVERY_REQUIRED/latched.
47. `retry.max_attempts=0` -> validation reject.
48. `GROUND_POSITION` contains free-form/container fields -> discriminated-schema reject.
49. SemanticFieldPath wildcard/bracket/unregistered path -> validation reject.
50. Successful terminal action gets later stale failure callback -> `CONFIRMED` unchanged.
51. Hostile site frames UI -> `frame-ancestors 'none'` blocks.
52. Adapter advertises extension registry hash H but returns different JCS registry -> reject before scenario execution.
53. Same semantic registry ID/version changes descriptor across adapter restart -> incompatible/fail closed; no silent reinterpretation.
54. `SNAPSHOT_PATH` omits checkpoint or points to wrong registry value type -> validation/refusal.
55. Runtime budget expires while paused -> no extension; run cannot resume mutation past deadline.
56. Crash after durable one-step resource pair before scheduling -> same experiment/run/action IDs survive; no replacement/no auto-resume.
57. ResourceIdentityLedger contains duplicate run/resource identity contradiction -> fail closed.

Any safety-critical `UNDERSPECIFIED` causes FAIL.

## 30. Package A readiness question

Answer exactly:

> Could a fresh competent implementation agent implement Package A solely from current repository documentation, without this chat and without inventing scenario types, semantic field-registry semantics, parser safety, concurrency, dispatch, STOP, retry, durability, request/resource identity, budget, privacy, event-ordering, artifact, capture or restart semantics?

If NO, list exact missing contract/type/lifecycle/test.

## 31. Severity

`P0` — unauthorized mutation, secret exposure, uncontrolled irreversible/value effect, or architecture-invalidating flaw.

`P1` — material ambiguity/flaw requiring redesign or making affected implementation unsafe/unreliable.

`P2` — meaningful correctness/testability/maintainability gap to fix before/while implementing affected phase.

`P3` — non-blocking improvement.

Do not invent findings. Clean section must say exactly `NONE`.

## 32. Decision criteria

`PASS` only if no P0/P1, Package A ready=YES and every safety-critical falsification is SAFE_DEFINED.

`PASS_WITH_FINDINGS` only if no P0/P1, Package A ready=YES and remaining findings are P2/P3 only.

`FAIL` if any P0/P1, Package A ready=NO or safety-critical semantics remain underspecified.

## 33. Required output

Return exactly:

```text
REVIEW_TYPE=TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT

REPOSITORY=
CURRENT_MAIN=
AUDITED_HEAD=
DESIGN_PR=
DESIGN_MERGE=
LATEST_CONTROL_CENTER_HARDENING=
AUDITED_FILES=
SURVEYOR_STATE=
OTERYN_V2_HEAD=

RESULT=PASS | PASS_WITH_FINDINGS | FAIL

SUMMARY:
...

P0_FINDINGS:
- ...

P1_FINDINGS:
- ...

P2_FINDINGS:
- ...

P3_FINDINGS:
- ...

ARCHITECTURE_VERDICT:
...

SCENARIO_CONTRACT_VERDICT:
...

TRACK_A_AUTHORITY_VERDICT:
...

DISPATCH_DURABILITY_VERDICT:
...

STOP_ALL_CONCURRENCY_VERDICT:
...

IDEMPOTENCY_REPLAY_VERDICT:
...

SIDE_EFFECT_BUDGET_VERDICT:
...

RECORDER_CAUSAL_EVIDENCE_VERDICT:
...

ARTIFACT_RECOVERY_VERDICT:
...

SECURITY_PRIVACY_VERDICT:
...

CAPTURE_EMERGENCY_STOP_VERDICT:
...

CONTROL_API_SECURITY_VERDICT:
...

BROWSER_CLI_VERDICT:
...

OFFICIAL_ADAPTER_VERDICT:
...

SURVEYOR_INTEGRATION_VERDICT:
...

OTERYN_V2_ADAPTER_VERDICT:
...

DIFFERENTIAL_E2E_VERDICT:
...

PACKAGE_A_IMPLEMENTATION_READY=YES | NO

PACKAGE_A_MISSING_REQUIREMENTS:
- ...

DUPLICATION_OR_OVERLAP:
- ...

FALSIFICATION_RESULTS:
1. ...
...
57. ...

RECOMMENDED_CHANGES_BEFORE_IMPLEMENTATION:
1. ...

RECOMMENDED_IMPLEMENTATION_ORDER:
1. ...

EVIDENCE:
- exact repository paths
- exact PRs
- exact SHAs
- exact relevant workflow/check results

FINAL_DECISION:
...
```

This is an independent audit, not an implementation task.