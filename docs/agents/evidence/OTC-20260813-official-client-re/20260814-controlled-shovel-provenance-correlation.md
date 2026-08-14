# Track A controlled shovel provenance correlation — 2026-08-14

## Scope

Repository: `blakinio/otclient`
Track: Track A / `official-client-re`
Runner: `synology-otclient-01`
Branch: `ci/OTC-20260813-official-client-re-continuation`
Official client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

This checkpoint persists the controlled manual item-movement experiment performed against the live official Linux Tibia client. It separates directly verified runtime evidence, owner-supplied identification, derived conclusions, and remaining unknowns. It contains no credentials, session tokens, cookies, or proprietary client bytes.

## PROVEN — persistent observer and controlled mutation capture

The post-login persistent world-map observer was active on the live Track A process before the owner performed the controlled item action.

Verified runtime identity during the experiment:

```text
TRACK_A_CLIENT_PID=13803
TRACK_A_OBSERVER_PID=16045
baseline mutation events=0
baseline strip records=0
```

After the owner manually moved one known item on the ground, the observer recorded a structural mutation sequence containing:

```text
CreateOnMap
DeleteOnMap
CreateOnMap
DeleteOnMap
CreateOnMap
DeleteOnMap
CreateOnMap
```

The observer remained attached and alive after the action.

## PROVEN — aware-range eviction/reload occurred through strip/snapshot delivery

After the mutation capture, the owner moved far enough away for the original area to leave the active aware region.

Observed counters:

```text
before leaving:
  mutation events = 7
  strip records   = 0

after leaving:
  mutation events = 7
  strip records   = 259

after returning to the original area:
  mutation events = 7
  strip records   = 714
```

Therefore the return to the original area was represented by strip/snapshot loading rather than a new `CreateOnMap` event for the already-existing world state.

## PROVEN — runtime object field at +0x30 behaves as a thing/type identifier

Read-only raw-dump analysis was executed by:

```text
workflow: .github/workflows/tibia-official-client-re-provenance-raw-analyze.yml
run: 31838027667
job: 94888605256
analysis commit: b081705dc8fa4442d41255337a82394bd809c9ff
conclusion: success
```

The analyzer decoded candidate object IDs from the runtime object field at offset `+0x30` and compared them with strip objects decoded using the same offset.

For the four relevant `CreateOnMap` objects, `+0x30` produced:

```text
3457
3457
3457
3457
```

The same value was later found in the strip/snapshot dataset:

```text
type_id=3457
position=(32546,32516,7)
stack=2
strip timestamp_ns=1786738897870226366
```

This is direct evidence that the same ABI field can correlate a dynamic mutation object with a later strip/snapshot object for this exact official-client binary.

## OWNER-CONFIRMED — type_id 3457 was the controlled shovel

The repository owner explicitly identified the controlled item used in the experiment as a shovel and stated that its in-game item ID is `3457`.

This identification is owner-supplied experiment metadata, not independently derived from sprite/OCR recognition by the observer.

For this controlled run, the correlation is therefore:

```text
controlled item: shovel
owner-confirmed item/type ID: 3457
observed mutation object +0x30: 3457
observed reloaded strip object +0x30: 3457
```

## PROVEN — observed mutation positions for type_id 3457

The raw runtime objects associated with the four `CreateOnMap` hits containing `type_id=3457` exposed the following position sequence during the controlled manipulation:

```text
(32547,32515,7)
(32547,32514,7)
(32547,32516,7)
(32546,32516,7)
```

The later strip/snapshot dataset contained the same `type_id=3457` at:

```text
(32546,32516,7), stack=2
```

This provides a concrete mutation-to-reload correlation for one known controlled item.

## CORRECTION — prior creature/NPC inference was wrong

A temporary analysis inference classified the repeated `3457` Create/Delete pattern as likely creature/NPC movement because the positions changed in a regular sequence.

That inference was falsified by the owner's identification of the manipulated object as the shovel with ID `3457`.

Durable correction:

```text
3457 in this controlled sequence = the owner-manipulated shovel.
Do not classify this event sequence as creature/NPC movement.
```

The runtime evidence itself was valid; only the semantic interpretation was wrong.

## DERIVED — mutation-to-snapshot identity survives at least as type_id + position state

For this exact binary and experiment, a dynamically manipulated object carrying `type_id=3457` was later present in a reloaded strip/snapshot with the same `type_id` and final observed position.

This proves that the client exposes enough structural state to correlate:

```text
runtime mutation
  -> thing/type ID
  -> x/y/z
  -> later strip/snapshot object
```

without OCR.

It does **not** yet prove that the reloaded strip object contains an explicit marker saying that the item was dynamically placed or moved by a player.

## OTBM consequence

The experiment strengthens the requirement that canonical OTBM reconstruction must maintain history/provenance outside a single static snapshot.

Safe current rule:

```text
If an object has been observed through CreateOnMap/ChangeOnMap/DeleteOnMap as dynamic,
retain that dynamic provenance in the reconstruction state even if the same type_id later
appears through a normal strip/snapshot reload.
```

A later strip entry containing `(x,y,z,stack,type_id)` must not automatically promote the object to canonical/static map content.

For this controlled shovel example:

```text
shovel 3457 observed through mutation history -> DYNAMIC_OBSERVED
same shovel 3457 seen after reload             -> remains DYNAMIC_OBSERVED
```

until stronger static-source evidence exists.

## Remaining UNKNOWN

The following questions remain unresolved:

1. Whether the official client's reloaded strip object itself contains an explicit provenance/origin flag beyond fields already decoded.
2. Whether any pointer-adjacent or nested object field distinguishes server-map/static content from a dynamically moved item with the same `type_id`.
3. Whether a permanent map item and a player-moved item with the same `type_id` become byte-for-byte indistinguishable after complete eviction/reload.
4. Exact semantics/layout of every CreateOnMap/DeleteOnMap argument and stack/index field.
5. Whether corpse, field, temporary effect, creature, NPC and player objects use the same object/type-ID ABI field or require class-specific decoding.

## Next action

Use the known controlled marker `type_id=3457` as the reference object for a byte-level comparison between:

```text
A. mutation-time object state for shovel 3457
B. post-eviction strip/snapshot object state for shovel 3457
```

Compare stable object bytes, nested pointers/objects, flags and class metadata to determine whether any provenance marker survives reload. Do not rely on OCR or sprite recognition; preserve the owner-confirmed `3457 = shovel` mapping only as experiment metadata.

## Current claim state

```yaml
CONTROLLED_ITEM: OWNER_CONFIRMED_SHOVEL
CONTROLLED_ITEM_TYPE_ID: OWNER_CONFIRMED_3457
TYPE_ID_FIELD_THIS_BINARY: PROVEN_RUNTIME_CORRELATION_AT_OBJECT_PLUS_0x30
MUTATION_TO_RELOAD_TYPE_ID_CORRELATION: PROVEN
MUTATION_TO_RELOAD_POSITION_CORRELATION: PROVEN_FINAL_POSITION_32546_32516_7
RELOAD_DELIVERY_PATH: PROVEN_STRIP_SNAPSHOT_WITHOUT_NEW_CREATEONMAP
EXPLICIT_PROVENANCE_FLAG_AFTER_RELOAD: UNKNOWN
SINGLE_SNAPSHOT_SAFE_FOR_CANONICAL_OTBM: NO
PROVENANCE_HISTORY_REQUIRED: YES
PRIOR_3457_CREATURE_NPC_INFERENCE: FALSIFIED
```
