# TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT

Recommended reasoning effort: high / maximum.

Act as a **fresh independent read-only architecture, security, concurrency, durability and implementation-readiness auditor**.

Repository:

```text
https://github.com/blakinio/otclient
```

Use connected live GitHub repository state as the source of truth.

This is an independent falsification task. Do not trust conclusions from the design/hardening authors.

# 1. Absolute execution boundary

Do not implement fixes.

Do not:

- modify files;
- commit;
- push;
- merge;
- create replacement architecture;
- perform Track A runtime actions;
- launch/control the Tibia client;
- access credentials or secret values;
- log in;
- perform gameplay actions;
- write to `blakinio/Oteryn-v2`.

Use `runtime_access:none` reasoning only.

# 2. Audit target and freshness

Audit the **current complete design** of:

```text
TIBIA RE Control Center / E2E Lab
```

Historical discovery anchors:

```text
design PR       blakinio/otclient#600
design merge    ada65af85a872e2df43469f5687418fc5647811a
closeout PR     blakinio/otclient#601
closeout merge  5817f1ad699c2d68dfb1a03886dc8c20dace67e7
audit prompt PR blakinio/otclient#602
```

These are hints only.

Before relying on them:

1. fetch current `main`;
2. verify #600/#601/#602 merge status/SHAs;
3. identify every later merged/open PR touching Control Center architecture/contracts/prompts;
4. verify current blobs of all audited files;
5. inspect current open PRs and active tasks for overlapping Control Center, Surveyor, runtime bridge, Track A authority, E2E, HTTP/CLI or Oteryn work;
6. use live state when historical hints differ and report the discrepancy.

# 3. Mandatory files

Read in full from current trusted `main`:

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
- `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md`
- `docs/agents/tasks/archive/OTC-20260819-tibia-re-control-center-e2e-design.md`

Also inspect current Track A governance/dependencies including:

- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- current canonical lease/registration/Gate A/rebind/Gate B/bootstrap/whole-lifetime-supervisor contracts referenced by trusted instructions
- current GUI input lock/activity heartbeat helpers/contracts
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/REPOSITORY_MAP.md`
- `docs/agents/KNOWN_RISKS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CROSS_REPO_CONTRACTS.md`

Inspect exact current state/content of:

- PR #592 Surveyor;
- `tools/tibia_re_surveyor/**` if present/accepted;
- `tools/tibia_runtime_bridge/**`;
- canonical lease/input-lock/runtime-control helpers;
- existing scenario, recorder, artifact, persistence, HTTP, web, CLI, cancellation, idempotency and fake/test infrastructure that could overlap.

For `blakinio/Oteryn-v2`, read-only inspect:

- current `main` SHA;
- `AGENTS.md` and applicable nested instructions;
- `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`;
- relevant current architecture/security documents;
- `apps/client`;
- existing E2E/test-support/control interfaces;
- production/test-build restrictions.

Do not assume historical `otclient/oteryn-client/**` is canonical.

# 4. Evidence discipline

Use:

```text
FACT       directly verified from repository/tool state
INFERENCE  derived from verified facts
UNKNOWN    missing/unavailable evidence
```

Do not convert design intent into readiness automatically.

A contract passes only when two competent independent implementers could derive materially compatible safety behavior without this chat.

A test list does not repair an ambiguous contract unless the expected behavior is normatively defined.

# 5. Primary objective

Determine whether the current design is:

1. architecturally sound;
2. implementable without material redesign;
3. integrated with existing Track A infrastructure rather than duplicating it;
4. fail-closed at the exact irreversible mutation boundary;
5. linearizable under STOP/concurrent dispatch;
6. idempotent under retries/repeated POST/browser reload;
7. crash-safe against duplicate side effects;
8. conservative/enforceable for side-effect budgets;
9. privacy-safe before normal object creation;
10. truthful for multi-source causal evidence;
11. suitable for one browser/CLI backend;
12. reusable as an E2E/research platform;
13. compatible with current Oteryn v2 ADR-0007 without a second Oteryn E2E authority;
14. suitable for semantic differential testing;
15. sufficiently specified for a fresh Package A implementation with zero Track A runtime access.

# 6. Non-negotiable invariants

Attempt to disprove each:

```text
scenario validity
!= capability support
!= evidence maturity
!= observation freshness
!= mutation authority
```

```text
Browser ----\
             -> one Control API/domain service -> Scenario Engine -> MutationCoordinator -> Adapter
CLI --------/
```

```text
backend restart -> fresh backend_epoch
control_generation is scoped to backend_epoch
old backend callbacks cannot control new execution
```

```text
STOP wins dispatch_gate -> no dispatch commit -> no physical mutation
commit_dispatch wins dispatch_gate -> action is durably possible-dispatched before STOP
```

```text
physical mutation requires successful one-shot durable dispatch commit
```

```text
same action_id + same request -> one logical dispatch maximum
same action_id + different request -> deterministic refusal
```

```text
possible dispatch + missing terminal proof -> AMBIGUOUS
AMBIGUOUS mutation -> no automatic retry
```

```text
secret-class data never enters normal Event/Artifact/Error/Report/AgentBundle objects
```

```text
ingest order != source causal order
```

Safety-relevant violation is at least P1 and P0 when it can permit unauthorized mutation, secret exposure or uncontrolled irreversible/value effects.

# 7. Repository fit and duplication

Classify every proposed component:

```text
REUSE_EXISTING
EXTEND_EXISTING
NEW_COMPONENT_JUSTIFIED
DUPLICATE_OR_CONFLICTING
UNKNOWN
```

Audit:

- Safety Controller;
- MutationCoordinator;
- Scenario Engine;
- Recorder;
- Artifact Store;
- action/run persistence;
- Adapter API;
- Control API;
- fake adapter;
- Surveyor integration;
- runtime bridge;
- Track A lease/registration/Gates/supervisor/input lock;
- Oteryn adapter/E2E integration.

Verify no component becomes a second source of truth for Track A authority/evidence or Oteryn E2E authority.

# 8. Final authority and dispatch path

Do not accept `preflight immediately before dispatch` by itself.

Verify a concrete two-stage path exists:

```text
prepare outside local dispatch_gate
-> acquire/hold external adapter authority guard where required
-> final revalidation + durable commit under local dispatch_gate
-> physical effect while external guard remains held
```

Verify local `dispatch_gate` is **not held while waiting for external/Track A locks or slow I/O**, so STOP can still linearize while an action waits.

At final commit verify:

- action ledger/request hash;
- backend epoch;
- control generation;
- STOP/cancellation state;
- adapter generation;
- runtime instance;
- session epoch;
- side-effect reservation;
- capability;
- current external authority;
- shared GUI/input lock if needed;
- all current official Track A identity/authority checks within the existing guarded mutation boundary.

For official adapter verify the Track A external guard remains continuously held from final Track A checks through local `commit_dispatch()` and physical effect.

Falsify against stale/expired lease, stale registration, generation mismatch, client restart, PID reuse, executable/boot/window/display/container/session changes and authority loss immediately before commit.

# 9. Durable write-ahead dispatch commit

Verify persistent Package B+ semantics require, before physical mutation:

- durable `DISPATCH_COMMITTED`;
- `POSSIBLY_DISPATCHED` state;
- action ID/request hash;
- backend/control generation;
- fence provenance;
- budget `AT_RISK` transition;
- successful storage durability barrier.

If the durability barrier fails, physical mutation must not begin.

Crash after durable commit but before physical external call must recover conservatively as AMBIGUOUS unless authoritative reconciliation proves no effect.

Flag any design that records `POSSIBLY_DISPATCHED` only after the external call.

# 10. STOP ALL and concurrency

Verify STOP linearizes using the same `dispatch_gate` used by final commit.

Audit:

- control-generation increment/latch;
- queued old-generation rejection;
- cancellation while waiting for external authority;
- active wait/capture cancellation;
- not-yet-committed mutation prevention;
- already-committed conservative classification;
- stale completion rejection;
- reset semantics;
- concurrent browser/CLI operators;
- concurrent scenarios;
- concurrent read-only work;
- resource cleanup.

Reject vague `cancel active action` language without a concrete ordering rule.

# 11. Idempotency, replay and crash recovery

Verify:

- globally unique logical `action_id` scope;
- canonical normalized-request hash;
- same-ID/same-request behavior;
- same-ID/different-request conflict;
- repeated HTTP POST;
- CLI retry;
- browser reload;
- duplicate tabs;
- duplicate budget reservation prevention;
- action/result retrieval;
- no auto-retry after dispatch commit/ambiguity;
- backend restart creates fresh backend epoch;
- stale old-backend callback rejection;
- no automatic mutation resume;
- `NOT_DISPATCHED` vs `POSSIBLY_DISPATCHED` recovery;
- missing/corrupt/contradictory ledger fails closed.

# 12. Scenario Engine determinism

Verify typed/versioned semantics for:

- schema version;
- deterministic step IDs;
- predicates/operators;
- UNKNOWN behavior;
- preconditions;
- assertions;
- waits;
- timeouts;
- pause/resume;
- abort conditions;
- explicit retries;
- failure propagation;
- partial completion;
- backend/control/adapter/runtime/session fencing;
- capabilities;
- reproducibility.

Ensure movement, turn, spell, potion, food, rune, target selection, attack/follow, inventory, containers, equipment, controlled chat, read-only observation and before/after checkpoints are representable semantically.

# 13. Side-effect budgets

Verify per-run dimensions use:

```text
limit
reserved
at_risk
committed
uncertain
```

Audit:

- reserve maximum plausible effect before dispatch;
- move reservation to at-risk atomically with durable dispatch commit;
- release only with proven no-effect;
- measured confirmed commit;
- conservative commit for dispatched-but-unmeasurable;
- timeout/fail/cancel/ambiguous -> uncertain maximum;
- uncertain counts against future admission;
- duplicate same action ID creates no second accounting;
- new retry creates new reservation;
- checked/overflow-safe arithmetic.

At minimum inspect runtime, actions, movement, spells, consumables, moved items, gold, Tibia Coins and irreversible changes.

A hard budget that cannot be safely bounded must refuse before dispatch.

# 14. Recorder and causal evidence

Compare with `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

Verify Event model distinguishes:

- ingestion sequence/time;
- source timestamp;
- source clock domain;
- source sequence/scope;
- ordering confidence;
- backend/control/adapter/runtime/session generations;
- late status.

Verify preservation when observable of:

- stimulus/BACKGROUND;
- direction;
- message sequence/type/lane;
- runtime thread;
- handler/runtime object/object-instance epoch;
- before/after hashes;
- semantic delta;
- evidence ref;
- negative/no-stimulus controls.

A single total ingest sequence must not be represented as source causal order.

# 15. Late events and artifact finalization

Verify:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Audit bounded drain/watermarks, late event tagging, inability to rewrite terminal results, crash/incomplete artifacts, staged finalization, immutable finalized result, append-only supplements and no synthesized PASS.

Also verify durable dispatch journal/action ledger is persisted independently enough that artifact-report failure cannot erase possible-dispatch safety state.

# 16. Security/privacy at construction time

Falsify against:

- email/password/2FA;
- auth/session tokens;
- cookies/tickets;
- encryption/RSA material;
- private chat/player identities;
- environment variables;
- raw packet payloads;
- trace strings;
- exception/repr/debug text;
- login/auth screenshots.

Required:

```text
classification/redaction/rejection BEFORE normal object construction
```

`SECRET_REJECTED` may store category/reason only, never value/hash/reversible derivative.

Screenshots need safe/quarantine/reject admission.

Export-time-only redaction is material weakness.

# 17. Network capture

Default persistent path must be metadata-only.

Verify C2S/S2C, lane, source-local sequence when known, size, structurally known message type, correlation ID and `payload_capture=NONE` default.

No raw-payload fallback.

Future sanitized payload mode needs separate explicit policy proving pre-persistence secret exclusion.

# 18. Control API/browser/CLI

Verify one backend/domain implementation.

Audit:

- versioning;
- loopback-only default;
- request/collection/history bounds;
- subscriber/backpressure bounds;
- idempotency keys;
- duplicate POST/result retrieval;
- malformed input;
- STOP/reset/pause/resume/abort;
- browser reload;
- backend shutdown/restart;
- absence of raw/debug action bypass.

Remote/LAN control must not be enabled through trivial unauthenticated bind configuration.

# 19. UI truthfulness

Required major surfaces:

```text
Main Runtime Movement Healing Spells Consumables Combat Targeting
Inventory Containers Equipment Chat Conditions Scenarios Recorder
Network Experiments Compare Logger
```

Verify explicit separation of:

```text
AUTHORITY
CAPABILITY
EVIDENCE
FRESHNESS
```

`MUTATION_ALLOWED` must not look locally grantable.

UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN remain truthful.

Quick Actions must be one-step Scenario Engine experiments.

# 20. Official Tibia adapter

Verify common scenarios hide coordinates, raw keys, QMeta IDs, addresses/vtables, opcodes and wire layouts.

Generic support is:

```text
read_supported
action_supported
```

Official-only maturity remains:

```text
R0-R4
A0-A4
```

Verify current Track A infrastructure is consumed/extended, not reimplemented.

Crucially verify the official adapter obtains Track A guard without holding local dispatch gate, then keeps Track A guard continuously held through final Track A checks, durable local commit and physical mutation.

# 21. Surveyor boundary

Verify integration pins:

```text
surveyor_schema_version
producer_commit
producer_interface
```

Schema mismatch -> explicit `UNAVAILABLE/INCOMPATIBLE`, not copied fallback logic.

Control Center cannot silently promote/overwrite Surveyor evidence/coverage state.

# 22. Oteryn v2 integration

Audit current `blakinio/Oteryn-v2`, especially accepted ADR-0007.

Verify:

- `protocol-oteryn` retained;
- semantic comparison sufficient;
- client intent/server authority retained;
- no second Oteryn E2E/scenario authority;
- no hidden authoritative mutation hook;
- production test-control exclusion/lockdown;
- explicit cross-repo versioning;
- no Track A R/A pollution of generic Oteryn capabilities.

# 23. Differential E2E

Verify versioned profiles support:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Classify position, HP, mana, conditions, target, inventory, containers, equipment, cooldown state/timing, visual effects, pixel output, latency, protocol bytes, object layout and renderer implementation.

UNKNOWN/unobservable reference is coverage gap, not candidate mismatch.

# 24. Package A zero-runtime testability

Package A must be implementable with:

```text
runtime_access=none
network_listener=none
official_client_access=none
```

Fake/manual-clock/store model must deterministically exercise all execution semantics including durability failure and crash after dispatch commit.

If a core semantic test needs the official client, report a phasing defect.

# 25. Implementation phasing

Expected:

```text
P0 contracts/falsification baseline
P1 Package A control-core + Recorder + fake durability model
P2 Package B loopback API + browser + CLI + persistent store
P3 Package C accepted Surveyor/read-only integration
P4 Package D separately admitted official Track A adapter
P5 runtime capture producers
P6 research suites
P7 Oteryn adapter
P8 differential E2E
```

Verify Scenario Engine/Recorder/fake adapter precede UI and real actions; Surveyor waits for accepted interface; Oteryn remains separate repo governance.

# 26. Mandatory falsification matrix

For every case return `SAFE_DEFINED`, `UNSAFE`, or `UNDERSPECIFIED` plus exact evidence.

1. Authority expires one nanosecond before final dispatch commit. Expected: commit refuses.
2. Client restarts between advisory preflight and execute. Expected: runtime/adapter/session fence refuses stale commit.
3. Two browser tabs start mutation scenarios simultaneously. Expected: one per-adapter MutationCoordinator serializes.
4. CLI and browser submit same logical Quick Action with same action ID. Expected: at most one dispatch commit/effect.
5. STOP races with commit_dispatch. Expected: exactly one dispatch-gate linearization order.
6. Network recorder reports after run terminal state. Expected: late evidence only; terminal result unchanged.
7. Screenshot may contain login credentials. Expected: quarantine/refuse before normal artifact construction.
8. Adapter throws exception containing secret material. Expected: stable safe reason; raw text excluded.
9. Sources use different clock domains. Expected: source/ingest clocks distinct; no false total order.
10. Potion result is lost then caller retries same action ID. Expected: existing possible-dispatch state/result, no second dispatch; conservative budget.
11. Oteryn reports field official Tibia cannot observe. Expected: coverage gap/not comparable.
12. Official action evidence A4 while read path R1. Expected: independent maturity truthful.
13. Surveyor output schema changes. Expected: pinned incompatibility/refusal.
14. HTTP client repeats POST after connection loss. Expected: same idempotency key returns existing logical state/result.
15. Runtime authority changes while scenario paused. Expected: resume/final dispatch revalidation.
16. Stale scenario resumes after new session epoch. Expected: pending mutation invalidated.
17. Browser reloads during active run. Expected: backend remains owner; no duplicate action/run dispatch.
18. Backend restarts with action possibly in flight. Expected: fresh backend epoch; possible dispatch -> AMBIGUOUS/no auto-retry.
19. Same action ID reused with different parameters. Expected: idempotency conflict refusal.
20. STOP completes then stale old-generation callback returns PASS. Expected: evidence may persist but cannot advance current run.
21. Ambiguous item/gold action consumes remaining conservative budget. Expected: overlapping retry/new action refused if it would exceed budget.
22. Recorder/report process crashes before final result flush. Expected: incomplete run, never synthesized PASS.
23. Auth packet appears with metadata recorder. Expected: metadata only, no raw fallback.
24. Oteryn test adapter appears in production-default profile. Expected: current Oteryn build/security policy flags/prevents readiness.
25. Persistent dispatch-journal durability barrier fails immediately before physical effect. Expected: no physical effect.
26. Backend crashes after durable `DISPATCH_COMMITTED` but before physical effect. Expected: restart classifies AMBIGUOUS unless authoritative no-effect reconciliation exists; no auto-retry.
27. New backend restarts `control_generation` numerically at the same value as old backend. Expected: distinct backend epoch prevents stale callback/action acceptance.
28. Action is waiting to acquire Track A guard and operator presses STOP. Expected: STOP can acquire local dispatch gate and linearize without waiting for Track A acquisition; when action later acquires Track A guard its stale generation causes commit refusal.

# 27. Package A readiness question

Answer exactly:

> Could a fresh competent implementation agent implement Package A solely from current repository documentation, without this chat and without inventing concurrency, dispatch, durability, STOP, retry, budget, privacy, event-ordering, artifact or restart semantics?

If NO, enumerate exact missing contract/types/lifecycles/tests.

# 28. Severity

`P0` — can permit unauthorized mutation, secret exposure, uncontrolled irreversible/value effects, or invalidates core architecture.

`P1` — material flaw/ambiguity making implementation unsafe/unreliable or requiring redesign before affected phase.

`P2` — meaningful correctness/testability/maintainability gap to fix before/while implementing affected phase.

`P3` — non-blocking improvement.

Do not invent findings. Clean section must be exactly `NONE`.

# 29. Decision criteria

`PASS` only if:

- no P0/P1;
- Package A readiness=YES;
- every safety-critical falsification case is `SAFE_DEFINED`.

`PASS_WITH_FINDINGS` only if:

- no P0/P1;
- Package A readiness=YES;
- remaining findings are P2/P3.

`FAIL` if:

- any P0/P1; or
- Package A readiness=NO; or
- required safety-critical behavior is underspecified.

# 30. Required output

Return exactly:

```text
REVIEW_TYPE=TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT

REPOSITORY=
CURRENT_MAIN=
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

TRACK_A_AUTHORITY_VERDICT:
...

DISPATCH_DURABILITY_VERDICT:
...

STOP_ALL_CONCURRENCY_VERDICT:
...

IDEMPOTENCY_REPLAY_VERDICT:
...

SCENARIO_ENGINE_VERDICT:
...

SIDE_EFFECT_BUDGET_VERDICT:
...

RECORDER_CAUSAL_EVIDENCE_VERDICT:
...

ARTIFACT_RECOVERY_VERDICT:
...

SECURITY_PRIVACY_VERDICT:
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
2. ...
...
28. ...

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