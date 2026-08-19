# TIBIA-RE-CONTROL-CENTER-INDEPENDENT-AUDIT

Recommended reasoning effort: high / maximum.

Act as a **fresh independent read-only architecture, security, concurrency and implementation-readiness auditor**.

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
- launch/control/observe the Tibia client beyond repository evidence;
- access credentials or secret values;
- log in;
- perform gameplay actions;
- write to `blakinio/Oteryn-v2`.

Use `runtime_access:none` reasoning only.

# 2. Audit target

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

These are discovery hints only, not current truth.

Before relying on any historical value:

1. fetch current `main`;
2. verify #600/#601/#602 merge status and exact merge commits;
3. identify every later PR/commit touching the Control Center programme/contracts/prompts;
4. verify current blobs of every audited file;
5. inspect all current open PRs and active tasks for overlapping Control Center, Surveyor, runtime bridge, Track A authority, E2E, HTTP/CLI or Oteryn integration work;
6. report any discrepancy between historical hints and live state.

# 3. Mandatory files

Read in full from current trusted `main`:

- `AGENTS.md`
- `docs/agents/README.md`
- `docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md`
- `docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md`
- `docs/agents/tasks/archive/OTC-20260819-tibia-re-control-center-e2e-design.md`

Also inspect current relevant Track A governance/dependencies, including at minimum:

- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- current canonical lease/registration/Gate A/rebind/Gate B/bootstrap/whole-lifetime-supervisor contracts referenced by trusted instructions
- current GUI input lock/activity-heartbeat contracts/helpers
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
- existing scenario, recorder, artifact, HTTP, web, CLI, fake/test, cancellation and idempotency infrastructure that can overlap the design.

For `blakinio/Oteryn-v2`, read-only inspect:

- current `main` exact SHA;
- `AGENTS.md` and applicable nested instructions;
- `docs/architecture/ADR-0007-native-end-to-end-test-platform.md`;
- relevant current architecture/security documents;
- `apps/client`;
- existing E2E/test-support/control interfaces;
- production/test-build restrictions.

Do not assume historical `otclient/oteryn-client/**` is canonical.

# 4. Evidence discipline

Distinguish explicitly:

```text
FACT       directly verified from current repository/tool state
INFERENCE  derived from verified facts
UNKNOWN    missing/unavailable evidence
```

Do not convert prose intent into implementation-readiness automatically.

A contract passes only when two competent agents could implement the relevant behavior without inventing materially different safety semantics.

A test list does not repair an ambiguous contract unless the expected behavior is itself defined.

# 5. Primary objective

Determine whether the current Control Center design is:

1. architecturally sound;
2. implementable without major redesign;
3. integrated with existing Track A infrastructure instead of duplicating it;
4. safely fail-closed at the exact irreversible mutation boundary;
5. deterministic under concurrency, STOP, retries, transport loss and process restart;
6. privacy-safe before event/artifact creation;
7. truthful for multi-source causal evidence;
8. suitable for browser and direct-machine operation through one backend;
9. reusable as a research/E2E platform;
10. compatible with current Oteryn v2 ADR-0007 without becoming a second Oteryn E2E authority;
11. suitable for later semantic differential testing;
12. sufficiently specified for a fresh agent to implement Package A with zero Track A runtime access.

# 6. Non-negotiable invariants to falsify

Attempt to disprove every invariant below.

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
STOP linearizes before dispatch -> mutation does not begin
Dispatch linearizes before STOP -> action is classified already-dispatched
```

```text
same action_id + same request -> one logical dispatch maximum
same action_id + different request -> deterministic refusal
```

```text
possible dispatch + lost result -> AMBIGUOUS unless authoritatively reconciled
AMBIGUOUS mutation -> no automatic retry
```

```text
secret-class data never enters normal Event/Artifact/Error/Report/AgentBundle objects
```

```text
ingest order != source causal order
```

Any path that violates one of these in a safety-relevant way is at least P1, and P0 where it can create unauthorized mutation, secret exposure or irreversible/value effects.

# 7. Audit area A — repository fit and duplication

Classify each proposed component:

```text
REUSE_EXISTING
EXTEND_EXISTING
NEW_COMPONENT_JUSTIFIED
DUPLICATE_OR_CONFLICTING
UNKNOWN
```

Audit at least:

- Safety Controller;
- MutationCoordinator;
- Scenario Engine;
- Recorder;
- Artifact Store;
- Adapter API;
- Control API;
- fake adapter;
- Surveyor integration;
- runtime bridge integration;
- Track A lease/registration/Gates/supervisor/input lock;
- Oteryn adapter/E2E integration.

Verify no new component becomes a second source of truth for Track A authority/capability registries or Oteryn E2E authority.

# 8. Audit area B — final authority/dispatch linearization

Do not accept `preflight immediately before dispatch` as sufficient by itself.

Verify the design explicitly defines one final irreversible dispatch boundary and requires revalidation there of:

- idempotency state;
- current Control Center generation;
- cancellation state;
- adapter generation;
- runtime instance;
- session epoch;
- budget reservation;
- semantic capability;
- external current authority;
- shared GUI/input lock if applicable;
- all current official Track A identity/authority fences inside the existing canonical guarded mutation boundary.

Falsify against:

- stale/expired lease;
- stale registration;
- mismatched lease/registration generation;
- client process restart;
- PID reuse;
- changed executable/hash;
- changed boot ID;
- changed window/display/container;
- changed session epoch;
- changed adapter generation;
- authority loss one instruction/nanosecond before dispatch.

Any design where a prior cached PASS can authorize later mutation is a material finding.

# 9. Audit area C — STOP ALL and concurrency

Verify one explicit STOP linearization point exists under the same local coordinator synchronization domain used for dispatch admission.

Audit:

- increment/latch of control generation;
- queued work rejection;
- active wait cancellation;
- in-flight adapter cancellation request;
- not-yet-dispatched mutation prevention;
- already-dispatched conservative classification;
- stale completion rejection;
- reset semantics;
- concurrent browser/CLI operators;
- two scenarios;
- concurrent read-only operations;
- resource/lock cleanup.

Reject vague wording such as `cancel active action` without race-fencing semantics.

# 10. Audit area D — idempotency, replay and crash recovery

Verify:

- `action_id` uniqueness/idempotency scope;
- same-ID/same-body behavior;
- same-ID/different-body conflict;
- HTTP POST retry after response loss;
- CLI retry;
- browser reload;
- duplicate tabs;
- duplicate budget reservation;
- action result retrieval;
- no automatic retry after `AMBIGUOUS` or possible dispatch;
- backend restart with `NOT_DISPATCHED` versus `POSSIBLY_DISPATCHED` work;
- fresh control generation after restart;
- no automatic mutation resume after restart.

# 11. Audit area E — Scenario Engine determinism

Verify typed/versioned definitions for:

- schema version;
- deterministic stable step IDs;
- predicates/operators;
- UNKNOWN semantics;
- preconditions;
- assertions;
- waits;
- timeouts;
- pause/resume;
- abort conditions;
- retries;
- failure propagation;
- partial completion;
- runtime/session/adapter generation fencing;
- capability requirements;
- reproducibility.

Check representability of movement, turning, spells, potion, food, rune, target selection, attack/follow, inventory, containers, equipment, controlled chat, read-only observation and before/after checkpoints.

# 12. Audit area F — enforceable side-effect budgets

Audit per-run ledger semantics:

```text
limit
reserved
committed
uncertain
```

Verify reserve-before-dispatch and conservative accounting for:

- runtime;
- action attempts;
- movement tiles;
- spells;
- consumables;
- moved items/stack amount;
- gold;
- Tibia Coins;
- irreversible changes.

Determine exactly how PASS, proven no-dispatch, dispatched-but-unmeasured, TIMEOUT, FAIL, CANCELLED and AMBIGUOUS affect each ledger.

Hard budget that cannot be safely bounded must refuse before dispatch.

Flag any budget that is only decorative/reporting metadata.

# 13. Audit area G — Recorder and causal evidence

Compare against `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

Verify Event model distinguishes:

- ingestion sequence;
- ingestion monotonic time;
- source timestamp;
- source clock domain;
- source sequence;
- sequence scope;
- ordering confidence;
- late events.

Verify preservation when observable of:

- session epoch;
- stimulus ID/BACKGROUND;
- direction;
- message sequence/type/lane;
- runtime thread;
- handler/runtime object/object-instance epoch;
- before/after state hashes;
- semantic delta;
- evidence reference;
- negative/no-stimulus control linkage.

A single total `seq` must not be presented as source causal order across independent clocks.

Correlation must not auto-promote to causal proof.

# 14. Audit area H — late events and artifact finalization

Verify:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Audit:

- bounded drain/watermarks;
- late event tagging;
- late event inability to rewrite terminal result;
- crash/incomplete artifacts;
- atomic/staged finalization;
- immutable finalized result;
- append-only supplements;
- no synthesized PASS after restart/crash.

# 15. Audit area I — security/privacy at construction time

Falsify against:

- email;
- password;
- 2FA;
- auth/session tokens;
- cookies;
- tickets;
- encryption/RSA material;
- private chat;
- player identities;
- environment variables;
- packet payloads;
- trace strings;
- exception/repr/debug messages;
- screenshots showing login/auth UI.

Required invariant:

```text
classification/redaction/rejection BEFORE normal object creation
```

Export-time-only redaction is a material weakness.

Verify `SECRET_REJECTED` can record category/reason without value/hash/reversible derivative.

Verify screenshots have a safe/quarantine/reject admission path rather than automatic persistence.

# 16. Audit area J — network capture

Default persistent path must be metadata-only.

Verify support for:

- C2S/S2C;
- connection/session lane;
- source-local sequence when known;
- size;
- message type only when structurally known;
- correlation ID.

Verify no raw-payload fallback exists.

A future sanitized payload mode must require a separate explicit policy proving pre-persistence secret exclusion.

# 17. Audit area K — Control API / browser / CLI

Verify browser and CLI share one backend/domain implementation.

Audit:

- versioning;
- loopback-only default;
- body/collection/history bounds;
- event subscriber/backpressure bounds;
- idempotency key handling;
- duplicate POST/result retrieval;
- malformed requests;
- STOP/reset/pause/resume/abort;
- browser reload;
- backend shutdown;
- absence of raw/debug action bypass.

Remote/LAN control must not become available through a trivial unauthenticated bind flag.

# 18. Audit area L — UI truthfulness

Required major surfaces:

```text
Main
Runtime
Movement
Healing
Spells
Consumables
Combat
Targeting
Inventory
Containers
Equipment
Chat
Conditions
Scenarios
Recorder
Network
Experiments
Compare
Logger
```

Verify explicit separation of:

```text
AUTHORITY
CAPABILITY
EVIDENCE
FRESHNESS
```

`MUTATION_ALLOWED` must not appear to be locally grantable.

UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN must remain truthful states.

Quick Actions must be one-step experiments through Scenario Engine, never a raw bypass.

# 19. Audit area M — Official Tibia adapter

Verify common scenarios remain semantic and hide:

- GUI coordinates;
- raw key presses;
- QMeta IDs;
- addresses/vtables;
- opcodes;
- wire layouts.

Verify generic support is:

```text
read_supported
action_supported
```

and Track A-only evidence maturity remains in an official extension:

```text
R0-R4
A0-A4
```

Read support must never imply action support.

Verify the official adapter is an extension/consumer of current Track A infrastructure, not a parallel authority system.

# 20. Audit area N — Surveyor boundary

Verify integration is pinned to:

```text
surveyor_schema_version
producer_commit
producer_interface
```

A schema mismatch should degrade to explicit `UNAVAILABLE/INCOMPATIBLE`, not copied internals or fabricated data.

Control Center must not silently promote/overwrite Surveyor-owned evidence/coverage state.

# 21. Audit area O — Oteryn v2 integration

Audit against current `blakinio/Oteryn-v2`, especially accepted ADR-0007.

Verify:

- Oteryn retains `protocol-oteryn`;
- semantic comparison is sufficient;
- client sends intent and server remains authoritative;
- Control Center does not create a second Oteryn scenario/E2E authority;
- test hooks cannot mutate authoritative state outside supported paths;
- test hooks are excluded/locked down in production according to Oteryn governance;
- cross-repo contract/versioning is explicit;
- Track A R/A grades are not imposed on generic Oteryn capability semantics.

# 22. Audit area P — differential E2E

Verify versioned field profiles support:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

At minimum classify:

- position;
- HP;
- mana;
- conditions;
- target state;
- inventory;
- containers;
- equipment;
- cooldown state/timing;
- visual/game effects;
- pixel/frame output;
- latency;
- protocol bytes;
- internal object layout;
- renderer implementation.

An UNKNOWN/unobservable reference field must be coverage gap, not candidate mismatch.

# 23. Audit area Q — Package A zero-runtime testability

Package A must be implementable with:

```text
runtime_access=none
network_listener=none
official_client_access=none
```

Verify the fake adapter/manual clock can deterministically test every contract boundary without a real client.

If Package A requires current official runtime behavior to validate core semantics, report a material phasing defect.

# 24. Audit area R — implementation phasing

Expected dependency order:

```text
P0 contracts/falsification baseline
P1 Package A control-core + Recorder primitives + fake adapter
P2 Package B loopback API + browser + CLI
P3 Package C accepted Surveyor/read-only integration
P4 Package D separately admitted official Track A mutation adapter
P5 runtime capture-producer expansion
P6 research suites
P7 Oteryn adapter
P8 differential E2E
```

Verify:

- Scenario Engine precedes UI;
- fake adapter precedes official adapter;
- Recorder core precedes real actions;
- Surveyor integration waits for an accepted exact producer interface;
- official actions are separate from UI implementation;
- Oteryn work remains separate repository governance.

# 25. Mandatory falsification matrix

For each case return `SAFE_DEFINED`, `UNSAFE`, or `UNDERSPECIFIED` plus exact contract evidence.

1. Authority expires one nanosecond before irreversible action dispatch. Expected safe outcome: final dispatch refuses.
2. Client restarts between advisory preflight and execute. Expected: runtime/adapter/session fence refuses stale dispatch.
3. Two browser tabs start mutation scenarios simultaneously. Expected: one per-adapter mutation coordinator serializes admission.
4. CLI and browser submit same logical Quick Action simultaneously with same action ID. Expected: at most one dispatch.
5. STOP ALL races with dispatch. Expected: exactly one linearization order; no stale post-STOP dispatch.
6. Network recorder reports after run terminal state. Expected: late evidence only; terminal result unchanged.
7. Screenshot may contain login credentials. Expected: quarantine/refuse before normal artifact creation.
8. Adapter throws exception containing secret-shaped material. Expected: stable safe reason only; raw text excluded.
9. Sources emit timestamps from different clock domains. Expected: source/ingest clocks remain distinct; no false total order.
10. Potion dispatch result is lost, then caller retries. Expected: original becomes/retains possible-dispatch state; no automatic second dispatch; conservative budget consumed.
11. Oteryn reports a field official Tibia cannot observe. Expected: coverage gap/not comparable, not mismatch.
12. Official adapter action evidence is A4 while read path is R1. Expected: independent maturity remains truthful.
13. Surveyor changes output schema. Expected: pinned incompatibility/refusal, no copied fallback logic.
14. HTTP client repeats POST after connection loss. Expected: same idempotency key returns existing logical state/result.
15. Runtime authority changes while scenario paused. Expected: resume revalidation; subsequent mutation does not reuse stale authority.
16. Stale scenario resumes after new session epoch. Expected: pending mutation invalidated/refused.
17. Operator reloads browser during active run. Expected: backend remains owner; no duplicate run/action dispatch.
18. Backend restarts with action possibly in-flight. Expected: possible dispatch -> AMBIGUOUS unless authoritatively reconciled; no auto-resume/retry.
19. Same action ID is reused with different parameters. Expected: deterministic idempotency conflict refusal.
20. STOP ALL completes, then stale old-generation action callback returns PASS. Expected: evidence retained but cannot advance current run.
21. Ambiguous item/gold action would exceed remaining budget under maximum plausible effect. Expected: no retry/new action admission that breaches conservative budget.
22. Recorder process crashes before final manifest/result flush. Expected: run remains incomplete, never synthesized PASS.
23. Login/auth packet appears while metadata recorder is enabled. Expected: metadata only, no raw fallback.
24. Oteryn test adapter is accidentally compiled in a production-default profile. Expected: current Oteryn security/build policy must prevent/flag this before claiming readiness.

# 26. Package A implementation-readiness question

Answer exactly:

> Could a fresh competent implementation agent implement Package A solely from current repository documentation, without this chat and without inventing concurrency, dispatch, STOP, retry, budget, privacy, event-ordering, artifact or restart semantics?

If NO, enumerate the exact missing contract/types/lifecycles/tests.

# 27. Severity

`P0` — design can permit unauthorized mutation, secret exposure, uncontrolled irreversible/value effects, or invalidates the core architecture.

`P1` — material flaw/ambiguity that can make implementation unsafe/unreliable or requires redesign before Package A/affected phase.

`P2` — meaningful correctness/testability/maintainability gap that should be fixed before or while implementing the affected phase.

`P3` — non-blocking improvement.

Do not invent findings to populate sections. Clean section must be exactly `NONE`.

# 28. Decision criteria

Return `PASS` only if:

- no P0/P1 findings;
- Package A implementation-ready=YES;
- all safety-critical falsification cases are `SAFE_DEFINED` from current contracts.

Return `PASS_WITH_FINDINGS` only if:

- no P0/P1 findings;
- Package A implementation-ready=YES;
- remaining findings are P2/P3 only.

Return `FAIL` if:

- any P0/P1 exists; or
- Package A implementation-ready=NO; or
- a required safety-critical behavior remains underspecified.

# 29. Required output

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

ATOMIC_DISPATCH_VERDICT:
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
24. ...

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