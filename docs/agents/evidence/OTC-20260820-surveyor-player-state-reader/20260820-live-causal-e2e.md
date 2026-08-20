# Surveyor player-state live causal E2E — 2026-08-20

## Result

PASS. The repaired exact-current-build read-only player-state reader changed causally after one owner-performed movement while the exact runtime fence remained stable.

## Runtime fence

- container: `otclient-track-a-kasmvnc`
- display: `:1`
- PID: `19590`
- process start ticks: `76611792`
- executable size: `52109920`
- SHA-256: `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
- target uniqueness: `PROVEN`
- process memory access: read-only
- agent-generated GUI/gameplay input: none

## Reader under test

PR #635 head before evidence commit: `accbf23dd6817d08ab0412c88dea5e66b61e2be7`.

The repaired reader resolves `tibia::cyclopedia::TCyclopediaMapStorage` and requires two mirrored world-coordinate copies to agree:

- primary: `+0x2f0/+0x2f4/+0x2f8`
- mirror: `+0x408/+0x40c/+0x410`

The exact-current ELF static resolver independently returned PASS for vptr `0x30c2738`, typeinfo `0x30c0aa0`, qt-metacast `0xd1eef0`, and position handler `0xd19ef0`.

## Baseline

Output directory: `/tmp/tibia-re-player-fixed-baseline-1787258201`

Reader state: `AVAILABLE`.

Position: `(32547, 32501, 7)`.

Mirror consistency: `true`.

## Owner action

The owner manually moved the player 3–5 tiles after the baseline and explicitly reported completion. The agent did not generate input.

## Post-movement snapshot

Output directory: `/tmp/tibia-re-player-fixed-postmove-1787258899`

Reader state: `AVAILABLE`.

Position: `(32547, 32496, 7)`.

Mirror consistency: `true`.

## Differential

- delta X: `0`
- delta Y: `-5`
- delta Z: `0`
- Manhattan tile delta: `5`

The observed five-tile change matches the owner-performed movement while PID, process start ticks, executable size/SHA, target uniqueness, and mirror agreement remained stable. This supplies the required causal live E2E for the repaired reader.

## Validation

Before this physical differential, the repaired PR head passed:

- 32 focused deterministic tests;
- Python compile validation;
- `git diff --check`;
- exact-current ELF static resolver;
- GitHub CI run `32414943288`: success;
- Track A agent runtime governance run `32414942936`: success.

The earlier `TPlayerData +0x78/+0x7c/+0x80` interpretation is rejected by this task: it produced invariant `(0,0,2520)` across owner movement and was replaced fail-closed by the mirrored `TCyclopediaMapStorage` path.
