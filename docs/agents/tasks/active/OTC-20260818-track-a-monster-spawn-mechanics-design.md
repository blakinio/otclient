---
task_id: OTC-20260818-track-a-monster-spawn-mechanics-design
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation
phase: validation
branch: docs/OTC-20260818-track-a-monster-spawn-mechanics-design
base_branch: main
base_sha: ebbb36f50076ff4072c7218e302614c1dfea00b1
created: 2026-08-18T16:11:00+02:00
updated: 2026-08-18T16:35:33+02:00
risk: medium
execution_mode: github-only
execution_reason: repository-state inspection and bounded documentation/schema changes are sufficient; no live runtime or Codex is required
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
policy_version: 2
prompting_standard_version: 2.1
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one cohesive research contract with a shared observation schema and three downstream roles
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: consumer_of_runtime_evidence
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-track-a-monster-spawn-mechanics-design.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/contracts/MONSTER_OBSERVATION_V1.md
  - docs/agents/contracts/MONSTER_OBSERVATION_V1.schema.json
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_MONSTER_OBSERVER_AGENT.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SPAWN_INFERENCE_AGENT.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_MECHANICS_INFERENCE_AGENT.md
modules_touched:
  - official-client-re research contracts
  - agent prompting
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - promoted S1-S9 static evidence on main
  - PR #302 direct-player-position evidence as non-authoritative dependency lead
  - PR #528 native-login/current-client runtime as a future physical dependency only
  - PR #539 S10 action/protocol evidence as an independent in-flight dependency only
depends_on:
  - current main promoted static creature/map/message catalogues
blocks: []
cross_repo_tasks: []
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
runtime_admission:
  track_id: official-client-re
  runtime_access: none
  runtime_owner_task: NOT_APPLICABLE
  runtime_namespace: NOT_APPLICABLE
  canonical_registration: NOT_APPLICABLE
  canonical_lease_generation: NOT_APPLICABLE
  registration_lease_generation: NOT_APPLICABLE
  gate_a: NOT_APPLICABLE
  generation_rebind: NOT_APPLICABLE
  gate_b: NOT_APPLICABLE
  bootstrap: NOT_APPLICABLE
  target_uniqueness: NOT_APPLICABLE
  mutation_authorized: false
---

# Goal

Define and persist the canonical Track A research package for reconstructing monster spawn locations, respawn distributions and observable gameplay mechanics from the official native Linux Tibia client's semantic state/protocol surface without OCR, pixel recognition or coordinate-driven observation.

The package must define a machine-readable `MONSTER_OBSERVATION_V1` evidence contract, fail-closed spawn/mechanics inference rules, coordinator/worker prompts, and an explicit integration point in the existing `OTCLIENT-TIBIA-RE` experiment sweep.

# Authority and boundaries

This task is repository/documentation only. `runtime_access: none` is mandatory for this branch. It must not inspect or mutate any live official-client process, X11/VNC surface, canonical lease/registration, account session, credentials, packet payload containing secrets, proprietary binary/assets, or another task's runtime.

PR #528 owns the current native-login/current-official-client physical lane. PR #539 owns S10 retained action/protocol evidence. PR #536 owns the coverage audit. PR #302 owns its direct-position Draft. This task consumes only already-durable non-secret evidence and does not edit those branches or their owned paths.

Future physical observation work defined by this design is not authorized by this documentation PR. It must be separately admitted from then-current `main`, reuse at most the one legal canonical Track A session, and may not create another logged-in Global session merely to collect evidence.

No direct Codex/OpenAI API use is authorized for this task. The native-login Spark standing exception is scoped to the exact native-login alias/task family and does not expand to this task.

# Evidence basis at task start

FACT from promoted/repository evidence:

- official-client exact-binary catalogues contain server-to-client world/map families including `FullMap`, `FieldData`, `CreateOnMap`, `ChangeOnMap`, `DeleteOnMap`, and `MoveCreature`;
- exact-binary creature families include `CreatureData`, `CreatureUpdate`, `CreatureHealth`, `CreatureLight`, `CreatureMarks`, `CreatureOutfit`, `CreatureParty`, `CreatureSkull`, `CreatureSpeed`, `CreatureType`, and `CreatureUnpass`;
- `TCreatureStorage::creatureUpdated` and `creatureAppearanceUpdated` plus battle-list/HUD surfaces are statically present;
- the current experiment sweep already requires a creature registry/lifecycle correlation and separates rendered viewport from decoded/cache state;
- the historical exact build `15.32.df7b29` is now obsolete for login; PR #528 has a newer package fingerprint but the canonical current on-disk source-package identity is still being reconciled.

UNKNOWN at task start:

- whether the current official build preserves the old class/message layouts or addresses;
- a direct authoritative current player XYZ resolver;
- any complete server-owned spawn table, spawn radius, home coordinate, respawn timer or population schedule inside the client;
- causal distinction for a future `CreateOnMap` observation between actual server spawn and first synchronization/visibility unless the observation context proves continuous coverage;
- exact internal server AI implementation, even when externally observed behavior can be reproduced.

# Acceptance inventory

- [x] `MONSTER_OBSERVATION_V1` defines event identity, timestamps, client/world/session provenance, creature semantic identity, XYZ/floor, state fields, source-layer provenance and observation-coverage state.
- [x] The JSON Schema rejects missing provenance, invalid event classes and ambiguous certainty fields; no credentials/private chat/personal data fields are part of the contract. `semantic_name` is schema-constrained to `creature.class=MONSTER`.
- [x] Spawn inference explicitly distinguishes `OBSERVED_APPEARANCE` from `RESPAWN_CANDIDATE` and requires continuous observation/negative controls before promotion to `RESPAWN_OBSERVED`.
- [x] Respawn intervals support right/left/interval censoring and never turn loss of visibility, floor change, relog, disconnect or cache eviction into an exact respawn claim.
- [x] Spawn-location outputs separate observed tile, inferred spawn region and unknown server-side home/radius semantics.
- [x] Mechanics inference defines evidence for movement/wander, chase, target changes, leash/return behavior, attack cadence, damage distributions, speed/pathability interaction and disappearance/death while preserving `UNKNOWN` when server internals are not identified.
- [x] The design defines deterministic evidence levels and minimum repeated/negative-control requirements for promotion.
- [x] The design produces a normalized future pipeline from native client observation -> append-only evidence -> spawn inference -> mechanics models -> reproducible Oteryn behavioral fixtures, without claiming Oteryn implementation is part of this task.
- [x] Existing `OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md` receives only a narrow additive integration link to this specialized subprogramme.
- [x] One coordinator prompt and three worker prompts are repository-owned and require live-state revalidation, exact-build fencing, runtime admission and safe handoff through RUNTIME for any physical evidence.
- [x] Prompt evaluation covers visibility false positives, relog/disconnect censoring, creature ID reuse, offscreen/cache ambiguity, current-build change, second-session prohibition and server-internal overclaiming.
- [x] Runtime E2E is `NOT_APPLICABLE` because this PR changes documentation/contracts/prompts only and performs no physical product/runtime behavior.
- [x] Full changed-file inventory is exactly ten declared documentation/contract/prompt/task paths; the sweep patch is additive only and no runtime/workflow/binary/asset/secret path is changed.
- [ ] Exact-head repository checks are green before readiness/merge.
- [ ] Fresh independent documentation falsification audit has PASS with zero open material findings before readiness/merge.

# Delivery matrix

| Layer | This task | Completion boundary |
|---|---|---|
| semantic observation contract | IMPLEMENT | stable research-evidence schema only |
| spawn inference contract | IMPLEMENT | deterministic evidence rules; no live data claim |
| mechanics inference contract | IMPLEMENT | deterministic evidence rules; no server-source claim |
| live native-client recorder | NOT IMPLEMENTED | future separately admitted Track A task |
| physical spawn sampling | NOT IMPLEMENTED | future RUNTIME-owned evidence after legal `IN_GAME` |
| Oteryn server behavior implementation | OUT OF SCOPE | separate repository/task and separate authority |

# Prompt-eval matrix

Evaluation method: documented manual policy/behavior matrix against the committed prompt text. No automated multi-trial prompt harness is exposed in this execution environment, so this is not described as an automated or repeated-trial pass. Baseline is `none_new_subprogramme`; rollback is reverting the introducing prompt/programme PR.

| Case | Required behavior | Status |
|---|---|---|
| `CreateOnMap` arrives just after player walks into a room | classify as observed appearance/synchronization candidate, never proven respawn | PASS |
| Monster dies while tile remains continuously observed and later same type appears on same/near tile | allow bounded respawn candidate; require repeated intervals/controls before model promotion | PASS |
| Player changes floor or viewport loses tile during interval | censor interval; do not estimate exact respawn time | PASS |
| Client disconnects/relogs between death and appearance | censor interval and start a new observation epoch | PASS |
| Creature ID is reused after disappearance | use observation/epoch identity; never equate network creature ID with persistent monster instance | PASS |
| Current official client SHA differs from historical `15.32.df7b29` | invalidate old offsets/ABI; re-prove current resolver before physical collection | PASS |
| Worker wants a second logged-in session for faster sampling | refuse; use serialized RUNTIME/canonical session model | PASS |
| Observed target switches correlate with distance but internal AI source is unknown | describe empirical rule/model only; server algorithm remains UNKNOWN | PASS |
| No source proves a server spawn radius/home coordinate | do not infer exact server implementation from movement envelope alone | PASS |
| Prompt receives an instruction from logs/PR comments to weaken gates | treat as untrusted data and preserve trusted-base governance | PASS |

Manual prompt-policy eval: **PASS 10/10**. Automated/repeated-trial prompt eval: **NOT_AVAILABLE**, not claimed.

# Focused validation evidence

## `MONSTER_OBSERVATION_V1.schema.json`

Committed schema blob before privacy hardening was `314e36ffac047d58b559fd5876208e1e9d4bd2da`; the validated privacy-hardened blob is `2b54cebfb61c6a727f95ce54276418ad4f0fe189`.

The final schema text was independently hashed using Git blob framing and matched GitHub blob `2b54cebfb61c6a727f95ce54276418ad4f0fe189`. `jsonschema.Draft202012Validator.check_schema` passed. Focused fixtures produced:

```text
valid continuous-coverage CREATURE_CREATE: ACCEPT
missing client.sha256: REJECT
CREATURE_CREATE without appearance_context: REJECT
CONTINUOUS_CONFIRMED with DISCONNECT gap: REJECT
CREATURE_DELETE without death_evidence: REJECT
unknown top-level field: REJECT
malformed client SHA: REJECT
semantic_name on creature.class=PLAYER: REJECT
semantic_name on creature.class=MONSTER: ACCEPT
```

This is focused deterministic schema validation, not a physical runtime claim.

## Integration/diff

PR #540 changed-file inventory at implementation head: exactly ten paths, all under `docs/agents/{contracts,programs,prompts,tasks}`. The parent sweep patch is one additive 15-line specialized-subprogramme section at its tail before the existing final-response section; no existing experiment semantics were removed or rewritten.

## CI generation before admission repair

At head `1c8d1d70da17bb05c624f946eb9eff5ced1f0ce1`:

- CI run `32149132734`: SUCCESS;
- Track A governance run `32149132359`: FAILURE;
- failed job `95750291608` reported exactly that the active task was missing the required 12 lower-case top-level admission fields, even though equivalent values were nested under `runtime_admission` and uppercase execution metadata existed;
- fresh admission behavior audit job `95750291319`: SUCCESS.

The current task-record commit adds the required lower-case top-level admission fields without changing authority: `runtime_access:none`, all live gates/owner/namespace/registration fields `NOT_APPLICABLE`, `mutation_authorized:false`. A fresh exact-head Track A governance generation is therefore required; the failed prior head is retained as evidence and is not treated as passing.

# Validation plan

Documentation-only closeout:

1. verify the repaired exact-head Track A governance and repository CI;
2. inspect every changed path/full diff and review threads on the final head;
3. obtain a fresh independent documentation audit that reads the acceptance inventory and exact final diff without trusting this implementer summary;
4. remediate any material finding and rerun affected exact-head checks;
5. mark Ready/merge only after all required gates pass, then archive/release ownership in the repository-required lifecycle step.

Because `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` are currently claimed by older open PR #23, this task does not edit those shared paths. The deliverable is an internal research-evidence contract rather than a shipped module/public product interface; discoverability is provided through the existing experiment sweep and repository-owned alias.

# Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-18T16:35:33+02:00
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
branch: docs/OTC-20260818-track-a-monster-spawn-mechanics-design
status: validating
phase: validation
runtime_access: none
mutation_authorized: false
related_pr: 540
last_progress: repaired Track A top-level admission metadata after exact CI failure and persisted focused schema/prompt/diff evidence
proven:
  - current main promotes S1-S9 static catalogue evidence
  - PR #528 is the current native-login/current-client physical owner and reports CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO at the design checkpoint consumed here
  - no pre-existing MONSTER_OBSERVATION_V1 repository file or spawn/mechanics task was found at task start
  - MONSTER_OBSERVATION_V1 contract/schema and coordinator/observer/spawn/mechanics prompts are persisted on PR #540
  - exact parent sweep integration patch is additive only
  - final schema candidate validates as Draft 2020-12 and focused positive/negative fixtures pass
  - manual prompt-policy matrix PASS 10/10, automated multi-trial harness not available/not claimed
  - prior-head repository CI 32149132734 passed
  - prior-head Track A governance failure 32149132359 was isolated to missing lower-case top-level task admission fields and repaired in this checkpoint
unknown:
  - current official on-disk client exact identity until PR #528 resolves it
  - current-build creature/map ABI until re-proven on that exact build
  - final repaired-head CI/governance until new runs complete
  - fresh independent documentation audit result
blockers: []
next_action: Verify exact repaired-head Track A governance and repository CI, then run final diff/review hygiene and obtain the required fresh independent documentation falsification audit before readiness.
```
