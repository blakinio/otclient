# P0 consumption of merged Cyclopedia exact-client evidence — 2026-08-17

Task: `OTC-20260815-track-a-p0-direct-position`  
Consumer Draft: PR #302  
Trusted base observed: `main@8c9486e2c6109a7a39b564804c8acd707659b5e0`  
Producer: merged PR #435 / `OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle`

## Exact accepted producer evidence

The producer is no longer pending. PR #435 merged to trusted `main` as `8c9486e2c6109a7a39b564804c8acd707659b5e0` and archived its producer task.

Accepted final producer coordinates:

- source run: `32000921225`
- source head: `40b5efd2f6371b8f5c0a00036084960ab66eefd0`
- consumer artifact: `9278368790` / `track-a-p0-cyclopedia-sanitized-32000921225`
- durable artifact ZIP digest recorded by the accepted closeout: `sha256:49f48d4283e63dd613b32a99300dc86eb98d68d7d7f640ec621c72e854c30c87`
- client fence: `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- hosted validation: `PASS`
- runtime access: `none`
- raw client upload: `false`
- semantic player XYZ proven: `false`
- physical confirmation owner: `RUNTIME`

Canonical durable evidence lives at:

- `docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/p0-cyclopedia-sanitized-evidence.md`
- `docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/evidence-data.json`
- `docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/selected-code-windows.txt`

## FACT — exact structural graph now consumable by P0

The exact fenced client contains the requested Cyclopedia/player-position metadata neighborhood and a recovered `TCyclopediaMapStorage` RTTI/vtable graph:

- typeinfo candidate: `0x3089a50`
- vtable address point: `0x3089db0`
- typeinfo relocation slot: `0x3089da8`
- code xrefs: `0x812952`, `0x812e12`, `0xeb0ea2` -> `0x3089db0`
- metadata xref: `0xd299ed` -> `0x1d2a8d8`

Relevant exact strings include:

- `TCyclopediaMapStorage`
- `playerPositionChanged`
- `TWorldMapCoordinate`
- `onPlayerCreatureAddedToGameSession`
- `weak_ptr<TCreature>`
- `pPlayer`
- `onPlayerPositionWasUpdated`
- `onPlayerPositionChanged`

The `0xeb0ea2` window installs the `TCyclopediaMapStorage` vtable at `[rbx]` and initializes a large member graph. This is accepted structural object-initializer evidence, not semantic XYZ proof.

## FACT — old static-input blocker is closed

P0 no longer depends on another generic exact-client staging source merely to establish the Cyclopedia structural route. The former `producer pending / no sanitized bundle` blocker is obsolete.

The merged producer does **not** identify executable implementations for the specific position callbacks and does not identify an authoritative in-process XYZ storage member. Therefore static evidence has advanced the owner/type graph but has not completed the semantic acceptance gate.

## RUNTIME discriminator contract

The remaining load-bearing evidence is physical and remains RUNTIME-owned. Once the canonical runtime path has separately established exact-client process identity/uniqueness and permits a bounded read-only discriminator, P0 needs the smallest durable result containing:

1. exact client version/size/SHA fence;
2. fresh exact PID/start identity and uniqueness under current admission;
3. at least two observations of the direct-position candidate/read path correlated with an independent structural world coordinate;
4. negative-control discrimination against viewport/map-origin/camera/copy values;
5. if a stimulus is required, one bounded reversible adjacent step and inverse with before/after/restore structural evidence;
6. repeatability after a fresh PID/relogin when the RUNTIME lifecycle already performs that transition.

P0 must not bootstrap, log in, take X11/VNC/input ownership, mutate the physical session, or create a second logged-in session.

## Current RUNTIME frontier

At this checkpoint the canonical RUNTIME programme is still resolving exact X11 resource-to-client-PID identity. Hosted raw-XRes helper research PR #447 has passed deterministic validation; coordinator promotion PR #448 is open. A physical identity retry remains forbidden until that helper is promoted and a fresh separately admitted RUNTIME discriminator is created.

Therefore the current P0 terminal classification is:

```text
STATIC_INPUT_BLOCKER=CLOSED
STRUCTURAL_OWNER_GRAPH=PROVEN_PARTIAL
SEMANTIC_PLAYER_XYZ=UNKNOWN
PHYSICAL_CONFIRMATION=WAITING_ON_RUNTIME
P0_RUNTIME_AUTHORITY=NONE
```

No owner-funded Codex/OpenAI API quota was used for this continuation.