# Track A World Observation / Atlas Boundary

Shared programme: `OTS-20260813-world-reconstruction-navigation`.

## Scope

This document defines the producer-side architecture for delivering structured Real Tibia world evidence from Track A `official-client-re` to a separately authorized Otheryn Atlas consumer.

It is subordinate to current Track A governance, especially:

- `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
- `docs/agents/contracts/MAP_OBSERVATION_V1.md`;
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md`;
- current live task/PR/runtime ownership state.

## Authoritative producer

The current live producer is the **official native Linux Tibia client** under Track A `official-client-re`.

Track B / the native Linux `blakinio/otclient` Global-compatibility runtime is not the producer for this programme and must not be used as a shortcut to obtain Track A evidence.

The old open-source-OTClient recorder PR #292 is superseded and closed unmerged.

## Producer pipeline

The target producer flow is:

```text
exact official Linux Tibia client
  -> structurally verified player/world state
  -> coordinator-promoted Track A bridge/read surface
  -> local World Observation Index
  -> MAP_OBSERVATION_V1-compatible normalized facts
  -> deterministic sanitized dirty-chunk export
  -> separately authorized/promoted Atlas consumer
```

The producer never writes canonical OTBM.

## World Observation Index

Track A should maintain one durable local index of accepted world observations rather than treating each runtime sample as an isolated file.

The index must support at least:

- absolute `x/y/z`;
- `FULL`, `EMPTY`, `PARTIAL`, `UNKNOWN` knowledge semantics;
- ordered tile contents;
- factual categories and raw client identities;
- deterministic tile fingerprint;
- exact client/build/producer provenance;
- first-observed and last-observed metadata;
- observation count;
- material version/history when a tile's accepted fingerprint changes;
- acquisition method when proven;
- source/session evidence sufficient for later audit and bundle promotion.

Repeated observations with the same deterministic fingerprint may be deduplicated while updating observation metadata. A changed fingerprint must not silently erase prior accepted evidence.

SQLite is the preferred initial implementation candidate because the producer needs indexed lookup, deduplication, history and incremental dirty-chunk selection. The semantic contract does not require SQLite; another implementation may be accepted if it preserves the same invariants.

## Chunk alignment

The Otheryn Atlas already uses 128x128 world chunks. Producer export should align with the same chunk coordinates:

```text
chunkX = floor(x / 128)
chunkY = floor(y / 128)
floor = z
```

After initial population, only dirty/changed observation chunks should need export.

A deterministic export for the same accepted index state must be byte/semantically stable according to the chosen bundle contract.

## Identity boundary

Raw client/appearance identity is factual producer evidence. It is not automatically an OTBM/server item ID.

The producer must not guess the canonical mapping. It exports raw identities plus provenance; the consumer/integration layer resolves identity explicitly as `VERIFIED`, `AMBIGUOUS`, or `UNKNOWN`.

Updating Atlas assets to a newer client version is independent maintenance and does not weaken this identity rule.

## Accessibility and acquisition provenance

The producer should preserve the verified method by which an observation became available when that method is known. Suggested vocabulary:

- `NORMAL_TRAVERSAL`
- `CONDITIONAL_TRAVERSAL`
- `TRANSITION`
- `TELEPORT`
- `ADMIN_TELEPORT`
- `PASSIVE_WORLD_STREAM`
- `OTHER_VERIFIED_METHOD`

This metadata is evidence, not a route claim.

A tile being observed does not prove:

- an ordinary character can reach it;
- a normal WALK edge exists;
- the tile is reachable from the currently modeled world state.

Some locations may require quest/instance conditions, special access, or GM/admin teleport and may never be verifiable through ordinary-character traversal. Atlas models accessibility separately from verification.

## Runtime authority

The World Observation Index is not a new runtime owner.

Under current hybrid routing:

- deterministic index/schema/export implementation defaults to GitHub-hosted execution;
- P0-STATE/worldmap discovery defaults to hosted/static work where possible;
- physical login/display/input/gameplay/restart/relogin proof is supplied by RUNTIME on `synology-otclient-01` under current admission/lease/registration/bootstrap rules;
- non-RUNTIME implementation workers must fail closed rather than bootstrap/take over the canonical session as a shortcut.

No historical display, PID, VNC endpoint or session is current authority merely because prior evidence referenced it.

## Observation milestone

The first physical integration milestone is observation, not autonomous traversal:

```text
current exact official client in valid world state
-> structurally read absolute tile facts around current world state
-> normalize/index them
-> produce a sanitized changed-chunk bundle
```

The proof must not depend on OCR or guessed identities.

## Exploration mission boundary

Later, the Otheryn Atlas may publish a semantic exploration mission such as:

```text
target floor/chunk/bounds
reason
priority
estimated new coverage
access uncertainty
```

Track A owns execution against the current official-client state. It chooses local native actions/interactions and verifies material outcomes from resulting structural state.

Atlas does not own the canonical runtime, current PID/session, keyboard/mouse injection or blind action sequence.

## Viewport rule

Worldmap viewport enlargement is not a hard dependency of observation coverage.

If Track A can reliably expose absolute ordered tile facts for the currently available viewport, the observation index can accumulate larger coverage through repeated traversal. A larger viewport can reduce exploration cost and is therefore an accelerator rather than a prerequisite.

## Transfer boundary

The first cross-repository integration should use deterministic sanitized files/artifacts. A direct network API or event stream is not required.

External/Atlas consumption remains separately authorized and must not become an implicit runtime dependency of Track A. Track A should be able to persist/index observations even when the external consumer is unavailable.

## Safety/data boundary

Exports must not contain:

- account credentials;
- cookies/session keys/auth headers;
- login request/response material;
- raw packet payloads;
- proprietary client executable/assets;
- private transient runtime state not required by the normalized observation contract.

## Implementation decomposition

When current upstream evidence is sufficient, split implementation into bounded non-overlapping tasks:

1. **Observation index** — schema/store/dedup/history/fingerprints.
2. **Track A adapter** — convert coordinator-promoted structural reads to index facts.
3. **Chunk exporter** — deterministic 128x128 dirty-chunk promotion bundle.
4. **RUNTIME E2E** — physical observation/reacquisition/relogin evidence only where required.

Do not merge these responsibilities into Track B or into the Atlas repository.
