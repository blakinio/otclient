# OTCLIENT-TIBIA-RE monster spawn and mechanics reconstruction

```yaml
programme: OTCLIENT-TIBIA-RE-MONSTER-SPAWN-MECHANICS
parent_programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
programme_version: 1.0.0
research_mode: semantic_non_ocr
observation_contract: MONSTER_OBSERVATION_V1
runtime_status: DESIGN_ONLY_ON_THIS_PR
implementation_status: NOT_STARTED
```

## Objective

Build an evidence-driven path from the official Linux Tibia client's native semantic state/protocol surface to reproducible models of:

1. monster appearances and lifecycle;
2. observed spawn locations/regions;
3. respawn interval distributions;
4. movement, wandering, chase, targeting, return/leash-like behavior, attack cadence and other observable monster mechanics;
5. behavioral fixtures suitable for later independent Oteryn implementation/testing without claiming that the inferred model is CipSoft's internal server algorithm.

The programme is intentionally not an OCR, screenshot, image-matching or coordinate-clicking project.

## Current evidence boundary

### FACT — promoted/repository evidence

The exact historical official-client census recovered semantic server-to-client world/map families including:

```text
FullMap
FieldData
CreateOnMap
ChangeOnMap
DeleteOnMap
MoveCreature
```

and creature families including:

```text
CreatureData
CreatureUpdate
CreatureHealth
CreatureLight
CreatureMarks
CreatureOutfit
CreatureParty
CreatureSkull
CreatureSpeed
CreatureType
CreatureUnpass
```

The exact historical binary also exposed `TCreatureStorage::creatureUpdated`, `creatureAppearanceUpdated`, battle-list and creature-HUD surfaces. The parent experiment sweep already treats creature registry/lifecycle and viewport/cache separation as first-class targets.

### FACT — current lifecycle constraint

The historical exact build `15.32.df7b29` is obsolete for login. Current physical owner PR #528 is reconciling the current official Linux package and still reports `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO` at this design checkpoint.

Therefore no historical address, object layout, ABI, message field layout, PID, display, VNC mapping or runtime helper is current-build authority for this subprogramme.

### UNKNOWN

No repository evidence currently proves that the official client contains a complete server-owned table of spawn coordinates, home positions/radii, population rules or respawn timers. No direct current-build creature/world resolver is yet promoted. Server AI implementation details remain unknown unless independently proven.

## Core distinction

The programme separates three questions that must never be collapsed:

```text
A. What did the client observe?
B. What external gameplay behavior is supported by repeated causal evidence?
C. What exact algorithm/data structure does the server implement internally?
```

`A` can often become FACT. `B` can become an empirically validated model. `C` remains `UNKNOWN` unless source-level or otherwise direct evidence exists.

## Architecture

```text
OFFICIAL LINUX CLIENT
       |
       | proven semantic messages/models
       v
NATIVE OBSERVER / RUNTIME BRIDGE ADAPTER
       |
       | append-only
       v
MONSTER_OBSERVATION_V1
       |
       +-------------------+
       |                   |
       v                   v
SPAWN NORMALIZER       MECHANICS NORMALIZER
       |                   |
       v                   v
SPAWN INFERENCE        MECHANICS INFERENCE
       |                   |
       +---------+---------+
                 |
                 v
       BEHAVIORAL MODEL / FIXTURE EXPORT
                 |
                 v
       LATER OTERYN CONSUMER TASK
```

The physical observer is a future producer. Offline normalization/inference should default to GitHub-hosted deterministic execution and consume sanitized evidence artifacts.

## Canonical raw evidence

All future producers emit `MONSTER_OBSERVATION_V1` records. See:

```text
docs/agents/contracts/MONSTER_OBSERVATION_V1.md
docs/agents/contracts/MONSTER_OBSERVATION_V1.schema.json
```

Raw evidence is append-only. Derived records preserve source record IDs. Event loss, sequence gaps, observer restart, disconnect, relog, floor/coverage loss or target ambiguity must create an explicit discontinuity rather than be smoothed over.

## Observation epochs and continuity

A spawn interval is meaningful only inside an observation epoch whose event/coverage continuity is proven for the relevant tile/region.

A new epoch is mandatory after process restart, client SHA change, unproven reconnect/relog continuity, observer/bridge restart with possible loss, or runtime-identity loss.

Coverage states are ordered by evidence strength, not by visual usefulness:

```text
UNKNOWN
VISIBLE_RENDERED
DECODED_CACHE
DECODED_CURRENT
CONTINUOUS_CONFIRMED
```

Only `CONTINUOUS_CONFIRMED` may support an exact uncensored observed respawn interval.

## Spawn inference model

### Stage S0 — observed appearance

Any first locally observed `CREATURE_CREATE` is only:

```text
OBSERVED_APPEARANCE
```

It is never called a spawn merely because it arrived as `CreateOnMap` or a creature-storage add event.

The appearance context must be one of:

```text
INITIAL_SYNC
VISIBILITY_GAIN
AFTER_COVERAGE_GAP
CONTINUOUS_COVERAGE_CREATE
UNKNOWN
```

The first three explicitly block a direct respawn claim.

### Stage S1 — lifecycle anchor

Track one local `observation_instance_id` through create/move/update/delete. Do not use a client/network creature ID as a persistent monster-instance identity after deletion or epoch change.

A potential respawn interval needs a terminal anchor. Acceptable evidence strengths are recorded separately:

```text
EXPLICIT_SERVER_EVENT
ZERO_HP_CORRELATED
CORPSE_TRANSITION_CORRELATED
COMBAT_EVENT_CORRELATED
UNKNOWN
```

`CREATURE_DELETE` alone is not death.

### Stage S2 — continuous reappearance candidate

A `RESPAWN_CANDIDATE` requires all of:

1. one monster/race/type identity supported strongly enough for matching;
2. a prior terminal/death boundary;
3. a later `CONTINUOUS_COVERAGE_CREATE` of the matched monster/race/type;
4. same observation epoch;
5. same uninterrupted coverage token for the relevant region from terminal boundary through appearance;
6. no sequence/event-loss marker;
7. no floor change, viewport/coverage exit, cache-eviction ambiguity, disconnect, relog or observer restart;
8. world XYZ for the appearance or an explicit `UNKNOWN` position that prevents location promotion.

The result is still an empirical candidate, not a server-table extraction claim.

### Stage S3 — repeated observed respawn

Promote a region/type to `RESPAWN_OBSERVED` only after repeated uncensored candidates under equivalent semantic conditions plus at least one negative/no-stimulus control showing the candidate is not an observer artifact.

Default minimum proof target:

```yaml
uncensored_intervals: 3
independent_observation_epochs: 1_or_more
negative_control: required
contradictory_uncensored_intervals: 0_unresolved
```

Three intervals are a minimum causal-repeatability gate, not enough to claim a stable probability distribution.

### Stage S4 — respawn distribution

Retain every interval and its censoring class. Never discard long/short observations merely to fit an expected timer.

Represent intervals as:

```text
EXACT_UNCENSORED  death/terminal time and appearance time both continuously observed
LEFT_CENSORED     observation began after the prior terminal boundary
RIGHT_CENSORED    coverage/epoch ended before reappearance
INTERVAL_CENSORED terminal or appearance occurred inside a bounded but not exact observation window
INVALID           provenance/continuity insufficient
```

Report empirical sample count, min/max/median/quantiles only when supported by sufficient uncensored data. A parametric distribution name is `UNKNOWN` until goodness-of-fit and competing models are explicitly compared. Censored observations should remain available for survival/time-to-event methods rather than being converted into exact values.

### Stage S5 — spawn location/region

Keep three different outputs:

```text
observed_creation_tile     exact XYZ where client observed a qualifying create
inferred_spawn_region      cluster/envelope supported by repeated qualifying creation tiles
server_home_or_spawn_rule  UNKNOWN unless directly proven
```

A movement envelope or return point is not automatically the server's spawn centre. A group of nearby creation tiles may represent spawn variation, placement constraints, server correction, visibility semantics or another mechanism; alternative hypotheses stay recorded until falsified.

### Stage S6 — population/group behavior

Possible empirical targets include simultaneous population, reappearance ordering and correlations among several race/type instances in one continuously observed region.

Do not promote:

- a server spawn-group identifier;
- a shared timer;
- a maximum population rule;
- a radius/home coordinate;
- player-nearby suppression;

without experiments that specifically discriminate those hypotheses.

## Spawn result record

A normalized spawn result should include at least:

```yaml
model_id:
monster_identity:
world_region:
observed_creation_tiles:
uncensored_intervals_ns:
censored_intervals:
sample_count:
coverage_proof:
negative_controls:
contradictions:
alternative_hypotheses:
classification: OBSERVED_APPEARANCE | RESPAWN_CANDIDATE | RESPAWN_OBSERVED | SPAWN_REGION_INFERRED
server_rule: UNKNOWN | DIRECTLY_PROVEN
source_record_ids:
client_sha_set:
```

Do not merge evidence across client SHAs silently. Cross-version agreement is a stronger validation layer and remains explicit.

## Mechanics inference

Mechanics inference is empirical system identification over semantic events. Each model records input conditions, observed outputs, controls, counterexamples and alternative explanations.

### M1 — movement and step timing

Correlate consecutive monster XYZ, direction, client `CreatureSpeed` when available, player XYZ, tile/pathability evidence and monotonic time.

Targets:

- observed step intervals;
- diagonal/cardinal differences;
- acceleration/deceleration-like state if observed;
- relation between reported speed and actual tile transition timing;
- idle/wander movement distributions.

Do not confuse render interpolation with authoritative world-position transitions.

### M2 — chase response

With safe authorized stimuli, measure monster position response to bounded player movement while keeping attack/target relation observable where possible.

Use differential experiments:

```text
baseline stationary
-> one player step
-> monster response
-> inverse player step
-> response
-> no-stimulus control
```

Targets include response latency, chosen next tile, path deviation and distance dependence. A successful empirical predictor does not identify the server pathfinder implementation.

### M3 — targeting and target switching

When semantic target relations are available, correlate changes with distance, line/path state, damage events, disappearance and other controlled variables.

Record competing hypotheses rather than selecting by anecdote. Do not interact with unrelated players merely to obtain target-switch evidence.

### M4 — return/leash-like behavior

Measure trajectories after the controlled player/target condition changes. Candidate outputs:

- empirical return region;
- boundary at which behavior changes;
- time-to-return distribution;
- path chosen on return;
- despawn/disappearance correlation.

Name the model `return/leash-like` until direct evidence proves server terminology/data semantics. Never equate the observed boundary with an internal `deSpawnRange` or spawn radius by default.

### M5 — attack cadence

Correlate authoritative/correlated combat effects, player HP deltas when legally observable, creature action/effect events and monotonic time.

Separate:

- time between observed attack outcomes;
- animation/effect timing;
- server damage application;
- client rendering/cooldown representation.

A recurring interval does not by itself prove one internal cooldown constant.

### M6 — damage distribution and abilities

Collect observed output distributions under controlled defensive/state conditions when safe and already authorized. Preserve the distinction between raw monster output and player mitigation/resistance.

For projectiles/effects/area abilities, correlate semantic effect/projectile/map events where current-build evidence permits. Do not infer hidden damage formulas from final HP deltas without accounting for known/unknown mitigation variables.

### M7 — pathability interaction

Combine world/tile pathability evidence with creature movement. Repeated avoidance of a tile is only a candidate pathing rule until alternatives such as target choice, cooldown, occupancy or random movement are controlled.

### M8 — disappearance/despawn behavior

Classify deletions by coverage/disconnect/floor context. Only repeated `SERVER_DELETE_DURING_COVERAGE` with controls may support empirical despawn-like behavior. Loss of visibility or cache removal is not despawn.

## Mechanics model result

Every mechanics result contains:

```yaml
model_id:
mechanic:
inputs_observed:
outputs_observed:
controlled_variables:
negative_controls:
repetitions:
counterexamples:
alternative_hypotheses:
prediction_rule:
holdout_validation:
source_record_ids:
client_sha_set:
behavior_status: OBSERVED | CAUSAL_CORRELATED | REPEATED_MODEL | OUT_OF_SAMPLE_VALIDATED
server_algorithm: UNKNOWN | DIRECTLY_PROVEN
```

A future Oteryn implementation may intentionally reproduce the `prediction_rule` while `server_algorithm` remains `UNKNOWN`.

## Evidence promotion

Reuse the parent programme's G0-G4 capability gates. Monster-specific inference adds these semantic requirements:

```text
OBSERVED            source event/value structurally observed
CAUSAL_CORRELATED   bounded stimulus or world event correlates with expected semantic delta
REPEATED_MODEL      repeated/inverse/no-stimulus controls support one model with unresolved contradictions absent
OUT_OF_SAMPLE_VALIDATED
                    model predicts a separately collected holdout sequence/epoch within predeclared tolerance
```

Never convert static presence into a live mechanics claim.

## Experimental procedure

For each bounded hypothesis:

```text
1. pre-register objective and competing hypotheses
2. prove exact current client/runtime/IN_GAME identity through the owning runtime lane
3. prove observation coverage and sequence-loss detection
4. record no-stimulus baseline
5. apply exactly one harmless authorized stimulus when needed
6. capture semantic before/event/after records
7. perform inverse/control operation when applicable
8. repeat
9. collect counterexample/negative-control evidence
10. end/censor interval on any continuity loss
11. run offline inference deterministically
12. validate on a holdout observation when promoting a predictive model
13. persist evidence references and rejected hypotheses
```

Physical actions are never authorized by this programme document alone.

## Parallel execution model

The programme is designed for three roles with a serialized physical producer.

### Role A — Native Observer / Resolver

Default lane: P0-STATE + RUNTIME evidence provider.

Hosted work may recover/implement current-build resolvers, parsers and deterministic adapters. Any direct physical observation or stimulus must be performed by a separately admitted RUNTIME task or a separately proven non-conflicting read-only task under current governance.

There is at most one legal canonical logged-in Track A session by default. Do not create a second session for observer throughput.

### Role B — Spawn Inference

Default execution: GitHub-hosted, `runtime_access: none`.

May implement/validate pure normalization, censoring, lifecycle matching, region clustering and statistical summaries against synthetic and sanitized `MONSTER_OBSERVATION_V1` inputs before real samples exist.

Must not invent missing observations or relabel visibility gains as spawns.

### Role C — Mechanics Inference

Default execution: GitHub-hosted, `runtime_access: none`.

May implement empirical model extraction/validation over synthetic/sanitized records. It requests new physical stimuli as explicit experiment contracts; it does not take over the runtime itself.

### Coordinator

The coordinator chooses READY offline work independently of runtime availability, serializes physical experiment requests through current RUNTIME ownership, and never lets one waiting physical dependency stall offline inference/tooling work.

## Dependency graph

```text
current official client identity + structural IN_GAME
                  |
                  v
current-build creature/map/player resolvers
                  |
                  v
MONSTER_OBSERVATION_V1 physical producer
          /                       \
         v                         v
spawn inference              mechanics inference
         \                         /
          +-----------+-----------+
                      v
             behavioral fixtures
                      v
          separate Oteryn consumer task
```

Current design/contract work does not require the first dependency to be complete. Physical evidence collection does.

## Storage and evidence policy

Large observation streams should be workflow/runtime artifacts, not committed logs. Repository evidence indexes retain:

- contract version;
- exact client version/SHA/size;
- task/PR/run/job/artifact IDs;
- observation epoch metadata;
- sanitized record counts and loss/censoring summaries;
- deterministic inference digest/output summary;
- rejected hypotheses and contradictions;
- exact next action.

Never commit secrets, private chat, unrelated player names, raw proprietary client bytes or unbounded process/packet dumps.

## Future implementation path

The first implementation package after this design merges should be offline-first:

1. `MONSTER_OBSERVATION_V1` validator/normalizer with synthetic positive/negative fixtures;
2. spawn lifecycle/censoring inference with deterministic tests;
3. mechanics model skeleton with synthetic trajectories/controls;
4. only after the current official client reaches a legal structural `IN_GAME`, a separately admitted current-build observer producer;
5. bounded real observations and holdout validation;
6. behavioral fixture export;
7. separate Oteryn-side consumer/implementation task under that repository's own authority.

Do not block packages 1-3 merely because physical runtime work is waiting.

## Success criteria for the research programme

The programme can eventually be called research-complete for a specific monster/region/mechanic only when:

- source observations are exact-build/provenance fenced;
- required coverage continuity is proven;
- spawn claims survive visibility/relog/disconnect/cache negative controls;
- mechanics models have repeated controls and documented counterexamples;
- predictive claims pass a separately collected holdout;
- server internals not directly proven remain explicitly `UNKNOWN`;
- results are reproducible from sanitized evidence plus deterministic tooling;
- all material work is persisted in `blakinio/otclient` and related tasks/PRs are terminal.

It is not necessary to know CipSoft's internal algorithm to produce a behaviorally equivalent later implementation; equivalence claims must be limited to the validated observation domain.

## Real stop conditions

A future worker stops/rotates only for the repository's normal real stop conditions, including unresolved runtime ownership/authority, current-build identity unavailable for physical work, required protected credentials/live effects not authorized, missing evidence that cannot be recovered safely, or exhausted bounded execution budget.

A failed spawn/mechanics hypothesis is a research result, not a programme failure.
