# TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT

Recommended reasoning effort: high / maximum.

Act as a **fresh independent read-only architecture, security, concurrency, durability, privacy and implementation-readiness auditor**.

Repository:

```text
https://github.com/blakinio/otclient
```

Use live connected GitHub state as source of truth.

Do not trust conclusions from the design/hardening authors.

## 1. Absolute execution boundary

Do not implement fixes.

Do not:

- modify files;
- commit;
- push;
- merge;
- create replacement architecture;
- perform Track A runtime actions;
- launch/control the Tibia client;
- access credentials/secret values;
- log in;
- perform gameplay;
- write to `blakinio/Oteryn-v2`.

This audit is `runtime_access:none`.

## 2. Freshness/discovery

Historical anchors are discovery hints only:

```text
original design PR       #600
original design merge    ada65af85a872e2df43469f5687418fc5647811a
original closeout PR     #601
original closeout merge  5817f1ad699c2d68dfb1a03886dc8c20dace67e7
audit prompt PR          #602
first hardening PR       #605 (independently audited FAIL and superseded)
successor hardening      #613 or its merged/current successor state
```

Before relying on any:

1. fetch exact current `main`;
2. verify merge/open state and exact SHAs for relevant PRs;
3. identify later Control Center commits/PRs;
4. verify current blobs of all audited files;
5. inspect current open PRs/tasks for overlapping Control Center, Surveyor, runtime bridge, Track A authority, HTTP/CLI/E2E/persistence/policy work;
6. report discrepancies and use live state.

If the current hardening is an open PR and the owner explicitly asks to audit that exact PR/head, audit its exact unchanged head against current main; otherwise audit trusted current main.

## 3. Mandatory Control Center files

Read in full:

```text
docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
```

Also read relevant lifecycle task/archive records for #600/#605/#613 or their successors.

## 4. Mandatory repository governance/dependencies

Read/inspect current:

```text
AGENTS.md
docs/agents/README.md
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

Inspect:

- current exact Surveyor implementation/prompt/successor state, including historical #592 only as a discovery anchor;
- `tools/tibia_re_surveyor/**` if present/accepted;
- `tools/tibia_runtime_bridge/**`;
- canonical Track A lease/transition/guard/input helpers;
- current Ollama/local-agent work only as a possible downstream policy/research consumer, never as Control Center authority;
- existing scenario/recorder/persistence/HTTP/CLI/fake/idempotency/policy infrastructure that could overlap.

For `blakinio/Oteryn-v2`, read-only inspect current:

- main SHA;
- `AGENTS.md` and applicable nested rules;
- `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`;
- relevant security/architecture docs;
- `apps/client`;
- current test/E2E/control interfaces;
- production/test-build restrictions.

Do not treat historical `otclient/oteryn-client/**` as canonical.

## 5. Evidence labels

Use explicitly:

```text
FACT       directly verified
INFERENCE  derived from verified facts
UNKNOWN    evidence unavailable/missing
```

A prose intention is not an implementation contract unless behavior is sufficiently specified for two competent independent implementers to produce materially compatible safety behavior.

A test list does not cure ambiguous normative semantics.

## 6. Primary objective

Determine whether the design is:

1. architecturally sound;
2. implementable without material redesign;
3. integrated with existing Track A infrastructure without duplication;
4. fail-closed at the irreversible mutation boundary;
5. linearizable under STOP/concurrent dispatch;
6. idempotent under duplicate browser/CLI/HTTP requests;
7. crash-safe against duplicate side effects/resources;
8. conservative/enforceable for budgets;
9. deterministic/bounded at the scenario-parser/semantic layer;
10. privacy-safe before normal object creation;
11. truthful for multi-source causal evidence;
12. secure enough for initial local browser/CLI operation;
13. safe against cross-origin/DNS-rebinding abuse of loopback HTTP;
14. incapable of hiding mutation inside capture/emergency cleanup;
15. compatible with Oteryn-v2 ADR-0007 without a second Oteryn E2E authority;
16. suitable for semantic differential E2E;
17. sufficiently specified for Package A implementation with zero Track A runtime access;
18. preserves a future policy/automation boundary without granting model/policy direct credentials, shell, process, raw-memory, unrestricted-input or Track A authority.

## 7. Non-negotiable invariants to falsify

```text
scenario validity
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
old-backend callbacks cannot control new execution
unclean prior backend -> recovery_required before mutation admission
```

```text
STOP wins dispatch_gate -> no dispatch commit -> no physical effect
commit_dispatch wins dispatch_gate -> possible-dispatch/at-risk is durable before STOP observes it
```

```text
physical mutation requires successful one-shot durable dispatch commit
```

```text
request_id dedupes transport/domain requests
action_id dedupes semantic action attempts
resource-creating request identity is durable before domain creation/scheduling
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
passive capture != permission to attach/inject/input/mutate
STOP != permission for compensating gameplay/process mutation
```

```text
loopback bind != browser trust
Host + Origin + nonce are required by Control API v1
```

```text
policy/model output = untrusted intent
policy/model output != safety authority != Track A authority
```

Any safety-relevant violation is at least P1 and P0 when it can cause unauthorized mutation, secret exposure or uncontrolled irreversible/value effects.

## 8. Audit A — repository fit/duplication

Classify each:

```text
REUSE_EXISTING
EXTEND_EXISTING
NEW_COMPONENT_JUSTIFIED
DUPLICATE_OR_CONFLICTING
UNKNOWN
```

Components:

- Scenario Engine;
- MutationCoordinator;
- Safety Controller;
- Recorder;
- Artifact Store;
- ControlState/Request/Action/Budget persistence;
- Adapter API;
- Control API;
- fake adapter;
- future policy boundary/consumer;
- Surveyor integration;
- runtime bridge integration;
- Track A lease/registration/Gates/supervisor/input lock;
- Oteryn adapter/E2E integration.

Verify no second source of truth for Track A authority/evidence, Control Center execution safety or Oteryn E2E authority.

## 9. Audit B — Scenario v1 parser/semantic determinism

Verify exact contract for:

- JSON/YAML -> same typed AST;
- document/depth/string/collection/step bounds;
- duplicate-key rejection;
- unsafe custom YAML tag/object-constructor rejection;
- bounded/disabled aliases;
- UTF-8;
- non-finite/out-of-domain number rejection;
- JCS/RFC-8785 canonicalization;
- SHA-256 scenario/action hashes;
- deterministic explicit/generated step IDs;
- typed `SideEffectBudget`;
- typed `AbortCondition`;
- bounded `SemanticFieldPath`;
- closed per-kind Entity/Item/Destination schemas;
- typed predicates without implicit coercion;
- UNKNOWN behavior;
- retry only after proven NOT_DISPATCHED;
- semantic selectors instead of raw client internals;
- action-specific parameter schemas;
- finite EffectBound;
- capture/privacy policies.

Flag any `object` field whose semantics remain materially free-form enough to produce incompatible engines for a core action.

## 10. Audit C — final authority/dispatch

Do not accept advisory preflight as authority.

Verify sequence:

```text
prepare outside local dispatch_gate
-> acquire/hold external authority guard where required
-> final checks + durable local commit under dispatch_gate
-> physical effect while external guard remains continuously held
```

Verify local dispatch gate is not held while waiting for Track A/external locks.

At final commit verify:

- action ID/hash;
- backend/control generation;
- durable + in-memory STOP/recovery-required/cancellation;
- adapter/runtime/session fences;
- budget reservation;
- capability;
- current external authority;
- current GUI input lock;
- all current Track A final identity/authority requirements for Official Tibia.

Verify official external guard remains continuously held through local commit and physical effect.

## 11. Audit D — durability-before-effect and dispatch-gate I/O

Verify persistent Package B+/future Package D requires before physical effect:

```text
DISPATCH_COMMITTED
POSSIBLY_DISPATCHED
budget AT_RISK
backend/control/action/hash/fence provenance
successful local durability barrier
```

Exactly two bounded local safety transaction classes may run under `dispatch_gate`:

1. dispatch ActionLedger/BudgetLedger possible-dispatch/at-risk write-ahead commit;
2. backend-global ControlState STOP/explicit-reset transition.

Verify for both:

- explicit finite durability deadline;
- no external network dependency;
- no arbitrary report/capture/general persistence under the gate;
- dispatch barrier timeout/error -> no physical effect;
- STOP/reset persistence failure remains fail closed;
- crash after dispatch commit but before effect -> AMBIGUOUS unless authoritatively reconciled;
- safety journal/control state cannot be lost merely because report/artifact presentation fails.

## 12. Audit E — STOP/concurrency/restart durability

Verify one dispatch-gate linearization point for STOP versus commit.

Audit:

- generation increment/latch;
- durable global STOP before successful transition acknowledgement;
- STOP remains latched across backend restart until explicit durable reset;
- STOP persistence failure leaves current process mutation-disabled;
- durable backend-active marker makes a later crash/unclean restart recovery-required instead of implicitly resetting failed STOP;
- reset persistence failure keeps STOP/recovery-required blocking mutation;
- overflow fail-closed;
- queued old-generation cancellation;
- action waiting on Track A/external authority while STOP occurs;
- active waits/captures;
- already-committed conservative classification;
- stale callback rejection;
- multiple browser tabs;
- browser + CLI concurrency;
- multiple runs;
- read-only concurrency safety.

Reject vague `cancel active action` without ordering semantics.

## 13. Audit F — idempotency/replay

Verify ActionLedger:

- action ID scope;
- canonical action hash;
- same-ID/same-hash behavior;
- same-ID/different-hash conflict;
- no duplicate budget reservation;
- `CONFIRMED` is terminal success;
- new retry ID/attempt;
- no auto-retry after possible dispatch.

Verify Control API/Artifact RequestLedger:

- request ID distinct from action ID;
- backend-global authoritative storage, including requests before run creation/global STOP-reset operations;
- canonical method/path/body request hash;
- same-ID/same-hash resource/result replay;
- same-ID/different-hash conflict;
- resource-creating request preallocates final resource ID;
- durable ACCEPTED mapping exists before domain creation/scheduling;
- crash after ACCEPTED before resource creation reuses the same reserved ID;
- crash after resource creation/scheduling before COMPLETED resolves the same resource without duplication;
- repeated POST /runs returns same run;
- repeated one-step request returns same logical resources;
- durable mapping survives backend restart regardless of new backend epoch;
- corrupt/missing contradictory safety-critical ledger fails closed.

## 14. Audit G — side-effect budgets

Verify Scenario v1 defines every input budget dimension and Execution uses per dimension:

```text
limit
reserved
at_risk
committed
uncertain
```

Audit reserve-before-dispatch, atomic at-risk transition, conservative ambiguity accounting, exact no-effect release requirements, checked arithmetic and duplicate/retry behavior.

At minimum:

- runtime;
- actions;
- movement;
- spells;
- consumables;
- moved items;
- gold;
- Tibia Coins;
- irreversible changes.

Hard unbounded effect must refuse before dispatch.

## 15. Audit H — pause/restart/stale work

Verify:

- pause does not freeze external authority/generations;
- resume revalidates required fences;
- session/runtime change invalidates pending mutation;
- fresh backend epoch after restart;
- old-epoch callback refusal;
- backend loads global ControlState before mutation admission;
- current backend-active marker is durable before mutation admission;
- prior uncleared active-backend marker => recovery-required;
- clean-shutdown marker may be cleared only after required safety flush;
- marker persistence failure is conservative/fail-closed;
- no automatic mutation resume;
- NOT_DISPATCHED/POSSIBLY_DISPATCHED/CONFIRMED recovery;
- corrupt/contradictory state fails closed.

## 16. Audit I — Recorder/causal evidence

Compare with normative Track A experiment model.

Verify distinction of:

- ingest sequence/time;
- source timestamp/clock domain;
- source sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session fences;
- late status.

Verify preservation when observable of:

- stimulus/BACKGROUND;
- direction;
- message sequence/type/lane;
- thread;
- handler/runtime object/object epoch;
- before/after hashes;
- semantic delta;
- evidence ref;
- negative/no-stimulus control linkage.

A total ingest sequence must not be presented as source causal order.

## 17. Audit J — privacy before object creation

Falsify against:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA material;
- private chat/player identity;
- environment variables;
- raw packet payloads;
- trace strings;
- exception/repr/debug text;
- login/auth screenshots;
- Control API nonce;
- raw policy/model prompt/debug/reasoning dumps when secret or unbounded.

Required:

```text
classification/redaction/rejection BEFORE normal persistent-object construction
```

`SECRET_REJECTED` contains category/reason only.

Export-time-only redaction is insufficient.

## 18. Audit K — capture/emergency-stop bypass

Verify ordinary snapshot/wait/capture paths are observational only.

If enabling capture requires attach/injection/input/process/network mutation, passive capture must refuse and require separately governed mutation action/contract.

Verify `emergency_stop()` cannot use STOP as authority to:

- send gameplay stop/movement/action;
- inject input;
- kill/signal/restart client;
- attach/detach instrumentation;
- mutate networking/client config.

Harness-owned passive-resource cleanup is allowed.

## 19. Audit L — network capture

Default persistent path metadata-only.

Verify:

- C2S/S2C;
- lane;
- source-local sequence when known;
- structurally known message type only;
- size;
- correlation ID;
- `payload_capture=NONE` default;
- no raw fallback.

Future payload capture must be separately approved and sanitize before persistence.

## 20. Audit M — artifact/global safety/finalization

Verify backend-global:

```text
control/control-state.json
control/request-ledger.jsonl
```

or transactionally equivalent authoritative storage exists distinctly from per-run presentation artifacts.

Verify ControlState covers STOP/recovery/active-backend lifecycle and RequestLedger covers pre-resource/global requests.

Verify per-run lifecycle:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Audit:

- safety-state precedence over report/UI;
- bounded drain/watermarks;
- late tagging;
- late event cannot rewrite terminal result;
- incomplete/crash state;
- staged finalization;
- immutable finalized result;
- append-only supplements;
- no synthesized PASS;
- safety ledgers durable independently enough from report presentation;
- retention cannot evict state needed to preserve STOP, dedupe or ambiguous recovery.

## 21. Audit N — Control API local security

Verify exact v1 rules:

- default bind `127.0.0.1`;
- wildcard/non-loopback rejected;
- optional `::1` only explicit;
- fresh >=256-bit nonce per backend epoch;
- nonce not in URL/query/log/artifact/CLI argv;
- all `/v1/*` requests require nonce;
- exact Host allowlist including port;
- arbitrary DNS name resolving to loopback not trusted;
- exact browser same-origin Origin;
- no permissive/reflected CORS;
- no cookie ambient auth;
- CLI without Origin still requires Host+nonce;
- bounded bodies/headers/pages/events/subscribers;
- deterministic slow-consumer/backpressure behavior;
- stable safe errors;
- no raw/debug/eval/adapter endpoint;
- remote/LAN unsupported in v1;
- graceful shutdown flushes required global/per-run safety state without falsely marking an unclean backend clean.

Determine whether DNS rebinding/cross-origin browser requests can still reach authenticated control operations.

## 22. Audit O — browser/CLI parity

Verify both surfaces call one domain implementation.

CLI must not import/call concrete adapters directly.

Browser reload/new tab must recover active backend-owned run/action state rather than create duplicate work.

## 23. Audit P — UI truthfulness

Required tabs:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Required distinct always-visible concepts:

```text
AUTHORITY
CAPABILITY
EVIDENCE
FRESHNESS
```

`MUTATION_ALLOWED` must not look locally grantable.

UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN remain truthful.

Quick Actions are one-step scenarios, not bypasses.

## 24. Audit Q — Official adapter

Verify semantic scenarios hide coordinates/raw keys/QMeta IDs/addresses/vtables/opcodes/wire layouts.

Generic support:

```text
read_supported
action_supported
```

Official-only evidence:

```text
R0-R4
A0-A4
```

Verify Official adapter extends current Track A infrastructure instead of duplicating authority.

## 25. Audit R — Surveyor

Verify Package C pins accepted exact producer state:

```text
surveyor_schema_version
producer_commit
producer_interface
```

Mismatch -> explicit unavailable/incompatible, not copied fallback/fabricated data.

No Control Center overwrite/promotion of Surveyor-owned evidence.

## 26. Audit S — Oteryn v2

Audit current Oteryn-v2 against accepted ADR-0007.

Verify:

- `protocol-oteryn` retained;
- client intent/server authority retained;
- no second Oteryn E2E/scenario authority;
- no hidden authoritative client mutation;
- no unauthenticated production test control;
- test-only production exclusion/lockdown;
- explicit cross-repo versioning;
- no Track A R/A pollution of generic Oteryn capabilities.

## 27. Audit T — differential E2E

Read Comparison v1 and verify versioned comparison classes:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

At minimum classify position, HP, mana, conditions, target, inventory, containers, equipment, cooldown state/timing, visual effects, pixels, latency, protocol bytes, internal layout and renderer implementation.

UNKNOWN/unobservable reference must be coverage gap, not mismatch.

## 28. Audit U — phasing/Package A zero-runtime readiness

Expected order:

```text
P0 contracts/falsification baseline
P1 Package A control-core + fake durability/Recorder/Scenario
P2 Package B local Control API/browser/CLI/persistent store
P3 Package C accepted Surveyor/read-only
P4 Package D separately admitted official action adapter
P5 runtime capture producers
P6 research suites
P7 future policy/automation consumer
P8 Oteryn adapter
P9 differential E2E
```

Package A must require:

```text
runtime_access=none
network_listener=none
official_client_access=none
```

If core semantics require real client access, report phasing defect.

## 29. Audit V — future policy/automation boundary

Read Policy Boundary v1 and verify future model/policy consumers remain downstream of Control Center deterministic safety.

Required shape:

```text
normalized State/Observation
-> untrusted Policy/Decision
-> bounded semantic proposal
-> ordinary domain/Scenario validation
-> Safety/Authority
-> Adapter
-> Recorder
-> Result
```

Verify policy/model receives no direct:

- credential/2FA/auth secrets;
- Control API nonce merely for reasoning;
- Track A writable lease/registration authority;
- shell/process-control authority;
- raw memory-write authority;
- unrestricted keyboard/mouse/input primitive;
- concrete adapter handle;
- raw network mutation path.

Verify deterministic code owns rate limits, budgets, idempotency, freshness validation, STOP/recovery, capability checks and final authority.

Ollama/model unavailability must not disable STOP/manual deterministic research/safety.

## 30. Mandatory falsification matrix

For each return:

```text
SAFE_DEFINED | UNSAFE | UNDERSPECIFIED
```

plus exact contract evidence.

1. Authority expires immediately before dispatch commit. Expected: commit refuses.
2. Client restarts between preflight and execute. Expected: stale fences refuse commit.
3. Two browser tabs start mutation scenarios simultaneously. Expected: per-adapter serialization.
4. CLI/browser submit same action ID/hash. Expected: at most one dispatch.
5. STOP races with commit. Expected: exactly one dispatch-gate order.
6. Network event arrives after run terminal. Expected: late evidence only.
7. Screenshot may contain login credentials. Expected: quarantine/refusal before normal artifact.
8. Adapter exception contains secret. Expected: raw text excluded.
9. Event sources use different clocks. Expected: no false total causal order.
10. Potion result is lost and caller retries same action ID. Expected: no second dispatch; conservative budget.
11. Oteryn reports field official client cannot observe. Expected: coverage gap.
12. Official action maturity A4/read maturity R1. Expected: independent truthfulness.
13. Surveyor schema changes. Expected: pinned incompatibility.
14. HTTP repeats same action POST after connection loss. Expected: same logical action/resource.
15. Runtime authority changes while paused. Expected: resume/final commit revalidation.
16. New session epoch while scenario paused. Expected: pending mutation invalidated.
17. Browser reload during active run. Expected: backend-owned state, no duplicate.
18. Backend restarts with possible in-flight action. Expected: fresh epoch; possible dispatch -> AMBIGUOUS/no auto-retry; unclean lifetime remains recovery-required.
19. Same action ID reused with different parameters. Expected: conflict refusal.
20. STOP finishes then stale old-generation callback reports PASS. Expected: evidence only, no run advance.
21. Ambiguous item/gold effect consumes remaining budget. Expected: overlapping new action refused if bound exceeded.
22. Recorder/report crashes before result flush. Expected: incomplete, never synthetic PASS.
23. Auth packet appears under metadata capture. Expected: no raw payload persistence.
24. Oteryn test adapter appears in production-default profile. Expected: current Oteryn policy prevents/flags readiness.
25. Dispatch-journal durability barrier fails. Expected: no physical effect.
26. Crash after durable commit before physical effect. Expected: AMBIGUOUS unless authoritative no-effect proof.
27. New backend starts same numeric control generation as old. Expected: backend epoch fences stale work.
28. Action waits for Track A guard while STOP occurs. Expected: STOP can linearize; later stale commit refuses.
29. Malicious YAML uses duplicate keys/custom tags/alias amplification. Expected: bounded parser rejection.
30. Two semantically identical scenario/action objects differ only in map key order. Expected: same JCS hash.
31. Mutation retry configured after `DISPATCH_COMMITTED`. Expected: validation/execution refuses retry path.
32. Passive capture request requires new debugger attach. Expected: passive capture refuses; no hidden attach.
33. `emergency_stop()` implementation tries to send stop-movement input/kill client. Expected: forbidden without separate action/authority.
34. Browser from hostile website sends request to loopback API. Expected: Origin+nonce prevent control.
35. DNS-rebinding Host points attacker domain at 127.0.0.1. Expected: exact Host allowlist rejects.
36. Valid nonce from previous backend epoch is replayed after restart. Expected: rejected.
37. `POST /v1/runs` response is lost; caller repeats same request ID after backend restart. Expected: same durable run resource, not duplicate.
38. Same request ID reused for different POST body. Expected: deterministic idempotency conflict.
39. Slow event subscriber fills queue. Expected: bounded backpressure/disconnect, no execution blockage.
40. Wildcard `0.0.0.0` bind requested. Expected: Control API v1 refuses.
41. Dispatch durability store stalls. Expected: finite commit timeout; no effect; STOP can still linearize independently of external waits.
42. Capture cleanup tries to introduce a new invasive detach/signal. Expected: refuse unless separately authorized action.
43. Durable STOP is latched, then backend restarts. Expected: fresh backend loads STOP and refuses mutation until explicit durable reset.
44. Reset ControlState durability fails. Expected: STOP/recovery-required remains blocking.
45. STOP persistence fails, then backend crashes. Expected: prior durable active-backend marker causes next backend recovery-required; restart cannot silently reopen mutation.
46. Prior backend crashes without clearing active-backend marker. Expected: next backend records/keeps recovery-required before mutation admission.
47. `POST /v1/runs` crashes after durable ACCEPTED/resource-ID reservation but before resource creation. Expected: retry uses same reserved run ID and creates at most that one resource.
48. `POST /v1/runs` creates/schedules resource then crashes before COMPLETED mapping. Expected: retry resolves same resource ID and does not duplicate domain work.
49. Policy/model proposes shell/process/raw-memory/unrestricted-input/concrete-adapter operation. Expected: Policy Boundary/domain schema refuses; no bypass path.
50. Policy/model uses stale observation, requests larger budget, or becomes unavailable. Expected: deterministic revalidation/caps/NO_OP-or-refusal; STOP/manual deterministic safety remains operational.

Any safety-critical `UNDERSPECIFIED` causes FAIL.

## 31. Package A readiness question

Answer exactly:

> Could a fresh competent implementation agent implement Package A solely from current repository documentation, without this chat and without inventing scenario types, parser safety, concurrency, dispatch, terminal-success, STOP, reset/recovery, backend activation, retry, durability, budget, privacy, event-ordering, artifact, capture or restart semantics?

If NO, list exact missing contract/type/lifecycle/test.

## 32. Severity

`P0` — can permit unauthorized mutation, secret exposure, uncontrolled irreversible/value effect, or invalidates the architecture.

`P1` — material ambiguity/flaw requiring redesign or making affected implementation unsafe/unreliable.

`P2` — meaningful correctness/testability/maintainability gap that should be fixed before/while implementing affected phase.

`P3` — non-blocking improvement.

Do not invent findings. Clean section must say exactly `NONE`.

## 33. Decision criteria

`PASS` only if:

- no P0/P1;
- Package A implementation ready=YES;
- every safety-critical falsification is SAFE_DEFINED.

`PASS_WITH_FINDINGS` only if:

- no P0/P1;
- Package A ready=YES;
- remaining findings only P2/P3.

`FAIL` if any P0/P1, Package A ready=NO, or safety-critical semantics remain underspecified.

## 34. Required output

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

POLICY_BOUNDARY_VERDICT:
...

PACKAGE_A_IMPLEMENTATION_READY=YES | NO

PACKAGE_A_MISSING_REQUIREMENTS:
- ...

DUPLICATION_OR_OVERLAP:
- ...

FALSIFICATION_RESULTS:
1. ...
2. ...
...
50. ...

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