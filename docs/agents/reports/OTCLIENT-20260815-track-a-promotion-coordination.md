# Track A promotion/integration coordination — 2026-08-15

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Coordinator PR: `#300`  
Repository: `blakinio/otclient`  
Canonical base for this campaign slice: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Scope and trust boundary

This is the campaign promotion ledger for Track A (`official-client-re`), official native Linux Tibia client only. Research worker prose, PR comments and workflow colour are evidence inputs, not semantic authority. Track B remains outside Track A mutation authority.

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Build-specific claims below apply only to this fence unless a later exact identity is independently proven.

## Canonical P2 boundary

### FACT

Merged PR #299 establishes for the exact build:

- `TGameserverTCPConnection` QMeta/type/RTTI ownership;
- concrete `QTcpSocket*` member construction at receiver `+0x10`;
- `TProtocolWriter : TIODeviceWriter` RTTI relationship;
- corrected outbound chain reaches `TGameserverDualConnection`.

### DISPROVEN / SUPERSEDED

Do not revive without direct contradictory proof:

- `clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880` as gameplay endpoint;
- `0xb46bd0` as binary gameplay-frame sink;
- `0xc33259` as network/gameplay binary sink.

### UNKNOWN

- concrete `TGameserverDualConnection -> actual writer` ownership/reference/dispatch edge;
- gameplay serialization/framing order;
- compression/encryption/sequence transformation boundary;
- final binary socket/QIODevice egress;
- causal controlled/local harness proof.

## Promotion dispositions

### ACCEPT

**PR #283 — bounded read-only runtime bridge implementation.**

Source PR is closed unmerged at `d93ccb34f66af7d3198a50a46e706b4f902ae637`. Coordinator independently verified:

- exact implementation runtime-validation head `89e13819e6f53026b831b7e8e4c8fab228d1626c`;
- run `31654823776`, job `94306874981`: 12 focused tests PASS, Python compile PASS, standalone bridge build PASS, exact runtime reconstruction/profile rediscovery PASS, owner-only IPC mode `0600`, exact-client no-credential E2E PASS;
- compare `89e13819... -> d93ccb34...` changes only the task Markdown, no product/tool/test file;
- source exact-head CI `31680615776` SUCCESS;
- zero unresolved review threads.

Accepted evidence is preserved at `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/accepted-read-only-runtime-bridge.md`. Exact accepted tool/test blobs are rebuilt on #300 under `tools/tibia_runtime_bridge/**` and `tests/tools/tibia_runtime_bridge/**`.

Promotion boundary:

```yaml
read_only_bridge_implementation: ACCEPT
exact_build_profile_rediscovery: FACT
logged_out_zero_marker_fail_closed: FACT
session_status_live_authority: DERIVED/UNKNOWN until structural live correlation
authoritative_player_position: UNKNOWN
restart_relogin_stability: UNKNOWN
write_action_api: NOT_IMPLEMENTED
P1_complete: false
```

**Bounded runtime/world-state evidence from rejected PR #289.**

Run `31806312967`, job `94785974126` remains accepted for the exact-build reversible structural world transition. It proves a structural transition and restoration under normal client input, not A3/A4 bridge action parity. Standalone absolute player position remains unproven; viewport-derived XYZ remains DERIVED.

### ACCEPT_WITH_EDITS

**PR #279 — fail-closed worldmap reconstruction tooling.**

Source PR is closed unmerged at `04356aa9c042ce19d9d8431b91f18567e410a5e5`. Verified source evidence: repaired 23/23 focused tests, Python syntax PASS, synthetic `reconstruct -> compare -> plan-otbm` PASS, both material audit findings repaired, source exact-head CI run `31681889560` SUCCESS, zero unresolved review threads.

Rather than merge the stale source branch, #300 rebuilt exact accepted source blobs on current main and reconciled report/catalogue/changelog state. Current integration includes `tools/tibia_worldmap_reconstruction/**`, its focused test and `docs/agents/reports/OTC-20260812-worldmap-reconstruction.md`.

Not promoted: real official-client capture coverage, complete appearance-role mapping, complete client-ID -> OTB mapping, spawn definitions or complete binary OTBM.

**PR #290 — historical login/session recovery procedure.**

Source PR is closed unmerged. Only the corrected historical native-Linux procedure is retained as `REVALIDATION_REQUIRED` at `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/accepted-historical-login-procedure.md`. OCR is explicitly limited to historical character-selection bootstrap; it is not world-semantic evidence. Current login/restart stability requires fresh runtime proof.

### RETURN_FOR_EVIDENCE

**PR #295 — map-observation ownership correction.**

Still not promotable: four material unresolved review threads plus Track B ownership collision remain. Required corrections include restoring blanket raw-packet prohibition, explicit non-negative integer `producer.protocol_version`, separate authorization for external Atlas transfer, Track B ownership release and exact-head CI.

**PR #301 — P2 writer ownership.**

Current head `29ca506501efc716330a80ab2b96eaf9bbe3d4d5` contains only the approved dispatch/task contract. No evidence report, reproducer or executed hypothesis exists yet. It remains READY for an independent Draft-only researcher; coordinator will reconsider after concrete exact-client writer-ownership discrimination and terminal exact-head CI.

**PR #302 — direct player position.**

Current head `e45b126923495b209c08a77e9a3db96b44ad71a4` contains a bounded read-only typed `TPlayerData` probe, but material runtime run `31880617510` job `95002559098` remains queued. No direct-position semantic result exists. Required before promotion: actual runtime evidence, typed provenance, negative controls, at least two observations, independent structural-world comparison and terminal exact-head CI.

**PR #303 — restart/relogin reacquisition.**

Current head `0270b1f3b6e75c995649b405758f058bae026c88` contains an isolated namespace/credential-safe workflow design, but run `31881287155` has materialized only auxiliary static jobs; no self-hosted `reacquire` semantic job has executed. It is serialized behind #302 in the same `official-client-re-runtime` concurrency lane. Restart/relogin stability remains UNKNOWN.

**PR #304 — item-level coverage audit.**

Current head `7eec15079e54bc163785013025cdea47d30e57c7` contains only the approved dispatch/task contract. No registries/validator/summary exist yet. It remains READY for an independent Draft-only static researcher; selected inventory percentages cannot be upgraded to semantic coverage.

### REJECT / SUPERSEDE

- **PR #289** — broad stale continuation branch; superseded P2 model, failed exact-head CI and unresolved safety findings. Unique positive/negative evidence was preserved before closure.
- **PR #296** — stale lifecycle draft after its valid archive correction was integrated as a bounded current-main coordinator slice.
- **PR #277** — stale Oteryn-dependent Track A continuation handover. Unique negative runtime history is retained at `superseded-pr277-negative-runtime-history.md`; historical Oteryn continuation instructions are not authoritative.
- **PR #280 as an active Track A dependency only** — its broader infrastructure PR intentionally remains open under separate ownership. Track A does not wait on it; later evidence already proves `synology-otclient-01` executed Track A jobs, and current Track A isolation forbids historical `oteryn-staging` as an active dependency.

## Quantitative coverage checkpoint

These are scope-limited inventory checkpoints, not global semantic completion:

```yaml
protocol_identifier_inventory: 349/349
protocol_handler_qmeta_records: 47/47
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
direct_qt_connection_semantic_classification: UNKNOWN/2184
generated_message_semantic_classification: UNKNOWN/349
p0_live_read_coverage: UNKNOWN/UNKNOWN
```

Final programme requirements for item-level `capabilities`, `protocol_messages`, `runtime_types`, finite P0 denominators and terminal read/action gates remain unsatisfied.

## Current lane state

```yaml
P2_NETWORK:
  pr: 301
  task_status: ready
  agent: unassigned_draft_only_researcher
  disposition: RETURN_FOR_EVIDENCE / DISPATCH_READY
P0_STATE:
  pr: 302
  task_status: waiting
  blocker: self-hosted passive-probe job 95002559098 queued
  disposition: RETURN_FOR_EVIDENCE
P1_BRIDGE:
  source_pr: 283 closed unmerged after ACCEPT
  current_main_integration: present on PR 300
  completion: partial
RUNTIME:
  pr: 303
  task_status: waiting
  blocker: serialized behind queued P0 runtime lane; no reacquire semantic job executed
  disposition: RETURN_FOR_EVIDENCE
COVERAGE_AUDIT:
  pr: 304
  task_status: ready
  agent: unassigned_draft_only_researcher
  disposition: RETURN_FOR_EVIDENCE / DISPATCH_READY
```

## Completion state

Track A is **not COMPLETE/100%**.

Open programme gates include P2 writer/transform/final-egress proof, authoritative P0 direct reads, live bridge authority/reacquisition, A3/A4 action parity, item-level quantitative coverage and final closeout. The coordinator must not self-research every independent lane merely to remove those UNKNOWNs; the repository operating model requires isolated Draft-only research workers and coordinator promotion review.
