---
task_id: OTC-20260814-map-observation-track-a-correction
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-re
task_kind: documentation
phase: ownership-correction
branch: docs/OTC-20260814-map-observation-track-a-correction
base_branch: main
created: 2026-08-14T10:14:00+02:00
risk: medium
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/tasks/active/OTC-20260814-map-observation-track-a-correction.md
reuses:
  - PR #279 / OTC-20260812-worldmap-reconstruction
  - PR #283 / OTC-20260813-tibia-runtime-bridge
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
execution_mode: chat-github
---

# Correct Map Observation producer ownership to Track A

## Decision

The previous P0 incorrectly described `blakinio/otclient` Track B decoded `Map`/`Tile` state as the current producer. The owner's intended source is the official native Linux Tibia client, therefore this programme belongs to Track A `official-client-re`.

`MAP_OBSERVATION_V1` remains useful as a producer-neutral normalized artifact contract. This correction changes ownership/source semantics, not its core FULL/EMPTY/UNKNOWN/PARTIAL, ordering, identity, transition-evidence or secret-exclusion invariants.

## Verified existing Track A foundations

- PR #279 already implements a fail-closed reconstruction pipeline specifically for official-client worldmap evidence, including provenance, repeated observation merge, static/dynamic separation, client-to-OTB mapping gates, comparisons and OTBM-ready plans.
- PR #283 already implements an exact-version official Linux client runtime bridge and records the remaining live-session requirements for authoritative player position and reversible movement proof.
- Track B PR #284 is explicitly independent and must not own this programme.

## Corrected programme flow

```text
official native Linux Tibia client
  -> Track A structural/runtime bridge and worldmap evidence
  -> MAP_OBSERVATION_V1 normalized sanitized artifacts
  -> Track A fail-closed reconstruction/evidence pipeline
  -> separately owned Otheryn Atlas ingest/diff/coverage/navigation model
```

## P1 next action

Create a separate Track A implementation task only after revalidating live ownership/overlap of PR #279, PR #283 and the current Track A runtime continuation. P1 must extend/reuse those foundations rather than instrument open-source OTClient `ProtocolGame::setTileDescription` or Track B.

P1 initial goal is observation production only: exact-version, read-only, local, bounded semantic tile/world observations from structurally verified official-client state. Autonomous movement and interaction remain later phases and require authoritative decoded before/after state.

## Acceptance

- [x] Current producer corrected to Track A official native Linux client.
- [x] Track B explicitly excluded from current producer implementation.
- [x] PR #279 worldmap reconstruction identified as mandatory reuse.
- [x] PR #283 runtime bridge identified as mandatory reuse.
- [x] Existing v1 safety/identity/completeness invariants preserved.
- [x] P1 instructed not to duplicate OTClient parser hooks or Track A foundations.

## Validation

Documentation correction only. Runtime E2E is NOT_APPLICABLE to this correction; future P1 runtime claims require native-Linux Track A evidence.
