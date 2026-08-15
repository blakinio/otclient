# Coordinator ownership audit — PR #295 vs merged PR #291

Date: 2026-08-15
Programme: `OTCLIENT-TIBIA-RE`
Coordinator PR: #300
Disposition: `RETURN_FOR_EVIDENCE / OWNERSHIP_LIFECYCLE_BLOCKED`

## Live facts

PR #295 (`docs(tibia): correct map observation programme to Track A`) is open and has four unresolved material review threads. They require:

1. resolving duplicate ownership of `docs/agents/contracts/MAP_OBSERVATION_V1.md` before the correction task claims it;
2. restoring explicit separate authorization before an external Atlas consumer may consume promoted artifacts;
3. preserving the unconditional ban on raw packet payload fields rather than limiting the ban to secret-bearing payloads;
4. restoring `producer.protocol_version` as a non-negative integer contract requirement.

PR #291 is already merged as `005158b5b9bf25fe77bd5fc10813a6388a072836`. Nevertheless its task record remains on `main` at:

`docs/agents/tasks/active/OTC-20260813-map-observation-export.md`

with `status: blocked` and still declares ownership of:

- `docs/agents/contracts/MAP_OBSERVATION_V1.md`;
- its fixture corpus;
- the fixture validator.

PR #295's active correction task also declares `MAP_OBSERVATION_V1.md`, so the reviewer's duplicate-ownership finding remains structurally true even though the old source PR merged.

## Coordinator decision

Do not mutate `MAP_OBSERVATION_V1.md` through PR #295 while both active task records claim the path. Do not resolve the review threads cosmetically without first repairing task lifecycle authority.

The required lifecycle repair is to archive/supersede the stale merged #291 task under an explicitly owned governance task, preserving its merged fixture/validator provenance, then assign the contract to the Track A correction task and address all four material review findings. The correction must remain producer-neutral in representation while making Track A the current authoritative producer and keeping Track B outside mutation authority.

This audit does not authorize mutation of Track B PR #284, external Oteryn repositories, or Atlas consumer code.

## Why this is a programme blocker

Until the lifecycle is repaired, a future worker could resume either active task and make conflicting edits to the same contract. That violates the repository one-owner/one-task path rule and makes any apparent PR #295 review resolution non-reproducible.

## Safe next action

Create/resolve a dedicated lifecycle-repair ownership record that explicitly owns the stale #291 task archival/supersession and the #295 task handoff. Only after that authority is durable should the contract be changed and the four review threads be resolved.
