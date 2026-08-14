# OTCLIENT-TIBIA-RE experiment design review

```yaml
review_date: 2026-08-14
track: official-client-re
repository: blakinio/otclient
review_type: methodology_and_execution_architecture
result: HARDENING_REQUIRED_AND_APPLIED
```

## Scope

This review evaluates the capability sweep and evidence-derived extension as a research programme rather than as a feature checklist. It focuses on whether the design can produce causal, restart-stable, reusable evidence for a future Agent Game API without confusing static presence, temporal correlation, UI effects or successful function calls with semantic proof.

The functional coverage of the sweep is broad. The material weaknesses were execution lifecycle, evidence causality, read/action gate precision, machine-readable coverage and ordering of static versus live work.

## Findings

### F1 — design task lifecycle was ambiguous

The original active task objective could be read as "execute the whole sweep", while its acceptance primarily described persistence of the research design for later execution. That creates two bad outcomes: premature completion after documentation, or a permanently active design task that becomes a catch-all owner for the entire programme.

Resolution:

- the PR introducing the sweep is explicitly a **research-design deliverable**;
- after merge it is archived;
- the canonical `OTCLIENT-TIBIA-RE` coordinator executes the research through bounded hypotheses/phases and durable checkpoints;
- the design task is not the permanent owner of all future runtime experiments.

### F2 — task owned paths did not cover the real PR surface

The original task declared only the base sweep and task file while the PR also contained the census extension, capability census and handover.

Resolution:

- update the task to own every path in the research-design PR, including the execution model and this review report.

### F3 — static census should precede live login

The exhaustive generated-message and QMeta census does not require an authenticated world session. Performing it after login wastes scarce live-session time and unnecessarily couples account/runtime recovery to static analysis.

Resolution:

- use explicit S0/S1/S2 static phases before the live boundary;
- login begins at L0 only after static classification/probe planning is prepared.

### F4 — common-dispatch architecture must be falsified, not assumed

The sweep correctly seeks common inbound/outbound dispatchers, but a preferred common-bus interpretation could bias the research.

Resolution:

- test competing inbound hypotheses: central queue, queue-as-fanout, multiple lanes;
- test competing outbound hypotheses: one action spine, several family spines, independent feature paths;
- persist disproven architecture hypotheses.

### F5 — before/after state alone is vulnerable to noisy false correlations

The live world changes continuously through regeneration, timers, creature movement, chat and connection traffic.

Resolution:

- introduce a causal recorder with session epoch, monotonic time, stimulus ID, message identity/sequence, connection lane, thread, runtime object and normalized before/after state hashes;
- require a no-stimulus noise baseline for important new correlations.

### F6 — read and action maturity were conflated

A subsystem may be strongly readable while all mutating actions remain unsafe or unproven. One G0-G4 ladder is insufficiently expressive for this state.

Resolution:

- preserve G0-G4 as a summary;
- add independent R0-R4 read gates and A0-A4 action gates;
- record both in the capability matrix.

### F7 — action proof needs parity against normal client behaviour

Calling a plausible function or emitting a generated message does not prove that the programmatic path is semantically equivalent to the normal official-client action.

Resolution:

- trace a reference action through the normal client;
- normalize and compare its outbound message/result with the programmatic candidate;
- require semantic message/result parity before A3/A4 promotion.

### F8 — the sweep experiment schema omitted canonical safety/recovery fields

The canonical programme requires abort conditions and rollback/recovery. The first sweep schema did not preserve them.

Resolution:

- execution model makes `abort_conditions` and `rollback_or_recovery` mandatory;
- add explicit authorized effects, side-effect budget, allowed targets and privacy redactions.

### F9 — protocol census needs schema detail, not only names

The known exact binary exposed 349 generated message symbols. A name-only catalogue leaves substantial reverse-engineering value unused.

Resolution:

- extract field number/name/type/cardinality/oneof/enum/nested-message information where generated metadata permits;
- link messages to queue methods, handlers and first live observations.

### F10 — flat inventories are insufficient for architecture discovery

QMeta and generated-message lists should reveal dependencies and event/action topology, not just names.

Resolution:

- build a graph from message -> queue -> handler -> storage -> controller -> UI/model and the inverse outbound path;
- record QObject ownership/signal-slot relationships only when actually present and observable.

### F11 — high-cardinality state must be machine-readable

Hundreds of message types, runtime types and experiments cannot remain only in long Markdown reports without becoming difficult to query reliably.

Resolution:

- require logical machine-readable datasets for capabilities, protocol messages, runtime types and per-experiment records;
- reuse one canonical Track A evidence root rather than creating parallel registries;
- keep Markdown as human-facing synthesis.

### F12 — coverage needed quantitative completion gates

"Broad" or "material" classification is too subjective for a large census.

Resolution:

- track protocol-message classification %, QMeta/runtime classification %, P0 experiment coverage, terminal P0 read/action coverage, unknown inbound count and restart-validated capabilities;
- require every recovered item to be classified or explicitly `UNCLASSIFIED/ignored-with-reason`;
- require every P0 capability to have an experiment or explicit blocker/unsupported rationale.

### F13 — discovery and promotion validation need separation

An agent that finds a heap address or resolver can unconsciously overfit validation to that same process/session.

Resolution:

- important P0/G4 candidates receive a fresh PID/PIE/session validation pass;
- rediscover from semantic resolver strategy rather than old transient addresses;
- use a fresh validator context for stable bridge/API promotion when repository policy requires it.

### F14 — rare world/server events need non-waiting states

Some raids, maintenance messages and unusual disconnect reasons may not occur during a bounded worker session.

Resolution:

- use `STATIC_REACHABLE`, `LIVE_OBSERVED`, `REPLAY_CONFIRMED`, `NOT_OBSERVED` states;
- investigate sessiondump only as a safe deterministic-replay research lead;
- never keep a worker alive merely waiting for a rare event.

### F15 — social/chat evidence needs explicit privacy minimization

Private messages, VIP/friends and player identities can contain unrelated personal data.

Resolution:

- commit only minimal normalized/redacted evidence;
- hash/anonymize unrelated actor identity where identity correlation is needed;
- persist plain text only for owner/test/NPC generated evidence or after explicit redaction;
- never commit credentials/session secrets or secret-bearing captures.

## Revised execution architecture

```text
S0 exact binary identity
-> S1 exhaustive protocol/QMeta/runtime census
-> S2 graph + classification + probe planning

LIVE BOUNDARY

-> L0 login + structural IN_GAME
-> L1 inbound/outbound topology + causal recorder
-> L2 core reads
-> L3 core actions + reference-path parity
-> L4 interaction systems
-> L5 rich/read-preview systems
-> L6 restart/relogin/stable bridge/update resilience
```

The detailed normative contract is:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
```

## Overall assessment

```yaml
functional_coverage: strong
static_evidence_basis: strong
evidence_method_before_hardening: good_but_correlation_risk
execution_lifecycle_before_hardening: ambiguous
execution_model_after_hardening: suitable_for_bounded_autonomous_research
```

The highest-value expected result is not 75 independent reverse-engineering implementations. The research should first determine whether a small number of protocol queues, feature handlers, storages and action dispatchers form reusable spines that can expose many capability families through one normalized bridge.

That architecture remains a hypothesis until live evidence proves or disproves it.
