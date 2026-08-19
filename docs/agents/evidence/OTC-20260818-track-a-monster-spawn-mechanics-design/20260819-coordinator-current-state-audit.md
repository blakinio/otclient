# Monster spawn/mechanics design — coordinator current-state audit

Date: 2026-08-19  
Source PR: #540  
Source head: `3fea6bb6c674b36fb66e3b07de9f85f50b3fa562`  
Coordinator review: `4971768519`  
Decision: **ACCEPT_WITH_EDITS**

## Design acceptance

The source design is accepted as a fail-closed research contract. `MONSTER_OBSERVATION_V1` correctly separates client observation from empirical external behavior and from unproven server internals. It requires explicit epochs, coverage continuity, loss/gap provenance, local observation-instance identity, death/disappearance context, censoring, negative controls and exact client fencing.

The exact source-head schema promoted by this package is:

```text
docs/agents/contracts/MONSTER_OBSERVATION_V1.schema.json
blob ac7df1cef80c417af6b74d79102c8da074032bed
```

Independent coordinator re-read of that exact final schema confirms the important fail-closed invariants:

- `CONTINUOUS_CONFIRMED` requires a non-null monotonic continuity start and `last_gap_reason=NONE`;
- `CONTINUOUS_COVERAGE_CREATE` requires `coverage.mode=CONTINUOUS_CONFIRMED`, `tile_observed=true`, a monotonic continuity start and no gap;
- creature lifecycle records require a creature object;
- create records require appearance context;
- delete records require disappearance and death-evidence context;
- derived/inference records require source record IDs;
- creature semantic names are conditionally constrained by creature-class semantics;
- schema rejects unknown top-level fields and malformed exact-client SHA shape.

The design never treats `CreateOnMap`/creature-add alone as respawn, never turns coverage loss into an exact interval, and never equates an empirical leash/spawn-region model with a proven server algorithm.

## Source validation provenance correction

The source task narrative names an earlier validated privacy-hardened schema blob `2b54ceb...`, while the exact final source head actually contains later blob `ac7df1ce...`. The earlier blob identifier is therefore historical validation provenance, not the final schema identity.

Canonical promotion identifies `ac7df1ce...` as the promoted schema and does **not** claim that the old automated fixture run targeted that final blob. Final source-head repository gates were nevertheless green:

```text
Track A governance 32151427300 = SUCCESS
CI                 32151427685 = SUCCESS
```

The coordinator independently re-read the final schema invariants above before acceptance.

## Current-state correction

Several source `current` paragraphs were true at the 2026-08-18 design checkpoint but are stale on promotion. They must be read as historical checkpoint context, not present runtime authority.

Current trusted repository facts at promotion start include:

```text
current official client version token = 15.32
current client size                  = 52109920
current client SHA256                = ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current ELF Build ID                 = d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

Programme dependencies have also advanced:

- native-login #528 is terminal/released; it proved causal login-to-world on the current exact build, while later process-handoff session retention failed separately;
- S10 #539 is terminal; its action-specific connect/member edge remains blocked by missing retained code window and must not be inferred;
- coverage #536 is terminal; the current 169-row registry is canonical on main;
- current-build creature/combat static G0 from #558 is promoted and may be consumed only at its accepted PARTIAL/static boundary;
- direct-player-position #302 remains non-promotion-ready because authoritative current XYZ still lacks the required legal causal runtime proof.

No historical PID, address, vtable, helper, session or old client layout becomes current authority for this monster programme.

## Runtime boundary after promotion

This package remains **DESIGN ONLY**:

```text
live native-client recorder      NOT IMPLEMENTED
physical spawn sampling          NOT IMPLEMENTED
server spawn table extraction    NOT PROVEN
server AI implementation         UNKNOWN
current authoritative player XYZ NOT PROVEN
```

Future physical collection must start from then-current trusted `main`, create/claim its own separately valid Track A runtime task, satisfy the current admission contract, prove the exact current client/runtime target and structural `IN_GAME` state, and use at most the one legal canonical logged-in Track A Global session by default.

This design PR itself grants no login, credential, GUI, gameplay, process-control or transaction authority.

## Safe sweep integration

The source adds exactly 15 lines to `OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md`. The parent sweep blob on current main remained byte-identical to the source base (`24c41a2b5285292bdf2220e08d4c3fb86031709c`) at audit time, so carrying the source integrated sweep blob does not overwrite intervening sweep work.

## Source ancestry

At audit time source #540 was:

```text
merge base  ebbb36f50076ff4072c7218e302614c1dfea00b1
ahead_by    13
behind_by   35
```

Direct source merge is inappropriate. Clean current-main promotion carries only the nine design/contract/prompt/sweep deliverables plus this coordinator overlay and an archive checkpoint. The source active task record is not promoted.

## Safety

```yaml
runtime_access: none
client_executed: false
credential_use: false
login: false
gui_input: false
gameplay: false
transaction: false
process_memory_access: false
runtime_mutation: false
```
