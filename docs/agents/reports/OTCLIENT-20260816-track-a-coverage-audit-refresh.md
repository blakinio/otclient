# OTCLIENT-TIBIA-RE coverage / contradiction / missing-proof audit — 2026-08-16

## Scope and result

```yaml
task_id: OTC-20260816-track-a-coverage-audit-refresh
track: official-client-re
lane: COVERAGE-AUDIT
execution_class: github_hosted
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
researcher_delivery: DRAFT_NOT_PROMOTED
snapshot_main: ddf7dd9408116fbeaca05bfeb69663f30f7cd34f
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 9
high_findings: 4
medium_findings: 5
owner_funded_ai_used: false
```

This audit attempts to falsify Track A campaign completeness from repository evidence only. It does not execute or observe the physical Tibia client, X11/VNC, login, process memory, network session or gameplay state. Current physical authority therefore remains:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Exact researched client fence used by the accepted static evidence:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## Point-in-time live repository snapshot

Live Git state has priority over stale task/checkpoint prose. The following exact heads were observed during this audit; active workers may advance them after this snapshot.

| Lane / concern | PR | Observed head | Snapshot disposition |
|---|---:|---|---|
| P0 direct player position | #302 | `d0b56ce562eb3ef6e59c1635687204917553dd32` | Draft; direct XYZ still not proven; new hosted exact-client retrieval hypothesis just landed |
| P1 bridge health/recovery | #357 | `fe37b80423d7cc8b269cd58edc19a2795e01e381` | Draft; semantic repair implementation validated, temporary validation workflow removed, integration/final-head gates remain |
| P2 downstream byte consumer | #310 | `a01281648c35dc04bf20437acc584b55b11ea727` | Draft; `BLOCKED_INPUT_STAGING` |
| canonical physical runtime | #358 | `d78e42b955c27ee07fba783f5496588f34d29461` | Draft; canonical registration absent; bootstrap required but not trusted/promoted |
| canonical bootstrap/rebind/Gate B implementation | #360 | `1d64fab66650b1fcd58388ff5cf6f9a77a392dc4` | Draft; four material coordinator findings remain open |
| hosted QLibrary source correlation | #356 | `f8e3733aa90bde0cd93c3bc6c3a364ac02b625dd` | Draft; load-bearing source validator failed |
| viewport continuation prompt | #363 | `b09e49cc950c091416c640dfd27f0fdfb7dd97fc` | open; continuation metadata still refers to superseded #325 lifecycle |
| this coverage audit | #369 | branch `research/OTC-20260816-track-a-coverage-audit-refresh` | Draft-only; coordinator promotion required |

Historical bounded coverage source:

```yaml
pr: 304
final_head: 43a60bd96cc644b656b200c9edbfb75578b330b6
state: CLOSED_UNMERGED
coordinator_disposition: ACCEPT_WITH_EDITS
exact_head_ci: 31882010038=SUCCESS
claim_boundary: bounded_inventory_baseline_not_global_semantic_coverage
```

The #304 registry was accepted as a bounded baseline and copied into superseded coordinator PR #300, but that coordinator branch was not merged. Current `main` evidence root does not contain an equivalent `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` registry. The accepted historical blobs remain useful evidence, but they are not a current-main canonical registry.

## Quantitative coverage ledger

Every percentage below keeps its original denominator and evidence class. `UNKNOWN` is not rewritten as zero.

| Metric | Current defensible value | Class | What it proves | What it does **not** prove |
|---|---:|---|---|---|
| generated protocol identifier inventory | `349/349` | FACT / inventory | exact known identifier set exists | semantic support or feature-family classification |
| protocol direction assignment | `349/349` | FACT / structural metadata | all 349 have direction; `189` inbound + `160` outbound | handler/field semantics |
| directly enumerated QMeta links in #304 registry | `27/349 = 7.736%` | FACT / bounded structural subset | 27 generated identifiers have accepted direct static links in that registry | global semantic protocol coverage |
| generated-message semantic support | `UNKNOWN/349` | UNKNOWN | denominator is known | no complete semantic numerator exists |
| protocol-handler QMeta inventory | `47/47` | FACT / bounded structural inventory | exact handler subset is represented | full Tibia-owned QMeta/runtime denominator or semantic coverage |
| raw direct Qt connection census | `2184/2184` | FACT / raw callsite inventory | known raw direct-connection callsites were inventoried | semantic classification of those 2184 edges |
| direct Qt semantic classification | `UNKNOWN/2184` | UNKNOWN | denominator is known | semantic numerator is absent |
| legacy QObject-connect selected subset | `40/41 = 97.561%` | FACT / selected subset | selected legacy edges were structurally resolved | all Qt/QMeta semantics |
| high-information GameAction sender metaobjects | `29/31 = 93.548%` | FACT / selected subset | selected high-information action sender set | global action-method coverage or action ABI proof |
| P0 top-level requirement registry | `16/16` | FACT / requirement registry | all 16 top-level P0 groups were represented in #304 | item-level P0 read/action coverage |
| P0 live-read coverage | `UNKNOWN/UNKNOWN` | UNKNOWN | no global percentage is defensible | terminal R1-R4 coverage |
| P1 bridge-v1 profile target inventory | `7/7` | FACT / implementation inventory | bounded bridge profile target set | overall P1 field/evidence coverage |
| P1 overall field/evidence coverage | `UNKNOWN/UNKNOWN` | UNKNOWN | item-level denominator was never normalized | global P1 completion |
| P2 chain closure | `UNKNOWN/5` | UNKNOWN | five closure questions were explicitly open in #304 | downstream framing/egress closure |
| restart/relogin stability | `UNKNOWN/1` | UNKNOWN | one required stability hypothesis is explicit | R3/R4/A4 restart stability |
| canonical physical runtime | registration `ABSENT`, lease generation `0` in #358 reconciliation | FACT / bounded physical reconciliation | current canonical registration was absent during run `31944216131` / job `95157691875` | current `IN_GAME`, display, VNC, PID, session, live bridge correlation |

### P0 historical group-level state

The accepted #304 `capabilities.jsonl` recorded the 16 top-level P0 groups as:

```yaml
stage_distribution:
  INVENTORIED: 7
  STRUCTURALLY_IDENTIFIED: 6
  SEMANTICALLY_SUPPORTED: 1
  UNKNOWN: 2
read_state_summary:
  R0_or_R1_groups: 10
  R1_groups: 1
  UNKNOWN_read_groups: 5
  NOT_APPLICABLE_read_groups: 1
restart_proven: 0
```

This is a group-level historical registry, not a valid item-level terminal-read percentage. In particular, the programme groups contain multiple independent fields/actions. The broad static capability census also contains more candidate surfaces than #304 normalized into these 16 rows, so the stage distribution must not be treated as exhaustive current static completeness.

## Material findings

### AUD-COV-001 — HIGH — accepted machine-readable coverage registry is not canonical on current `main`

**Classification:** FACT.

**Evidence:** closed Draft #304 at `43a60bd96cc644b656b200c9edbfb75578b330b6` contains the accepted task-scoped `capabilities.jsonl`, `protocol_messages.jsonl`, `runtime_types.jsonl`, validator and summary. Coordinator comment on #304 accepted it with provenance caveats and copied the blobs into coordinator PR #300. PR #300 was later superseded rather than merged. Current `docs/agents/evidence/` on `main@ddf7dd9408116fbeaca05bfeb69663f30f7cd34f` contains only the official-client RE, bootstrap-contract, lease-manager and viewport-feasibility evidence roots; repository search returns no current-main `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl`.

**Impact:** later agents cannot query a single canonical current-main item-level registry and are forced to reconstruct coverage from closed Draft evidence plus reports. This is a durability/coordination gap, not loss of the historical evidence itself.

**Smallest next discriminator/action:** coordinator reviews #304 accepted blobs against current programme schema and either promotes a provenance-preserving current-main copy or regenerates the same logical datasets from current accepted evidence. Promotion must preserve `UNKNOWN` and `DISPROVEN/SUPERSEDED`, and must not relabel inventory completeness as semantic completeness.

### AUD-COV-002 — HIGH — required semantic denominators are still incomplete

**Classification:** FACT for missing normalized denominators; UNKNOWN for resulting semantic coverage.

The execution model requires at least:

```text
protocol_message_classification_pct
qmeta_type_classification_pct
p0_capabilities_with_experiment_pct
p0_reads_terminal_pct
p0_actions_terminal_pct
unknown_inbound_count
unclassified_runtime_type_count
restart_validated_capability_count
```

Current defensible evidence does not provide all required numerators/denominators:

- protocol identifier/direction inventory is complete, but accepted semantic support remains `UNKNOWN/349` and no current canonical per-message `feature_family | UNCLASSIFIED` registry exists;
- the 47 protocol handlers are a bounded subset, not the full Tibia-owned QMeta/controller/storage denominator required by E52;
- raw `2184/2184` direct Qt callsites have semantic classification `UNKNOWN/2184`;
- P0 and P1 lack an adopted item-level field/capability denominator, so group counts and bridge profile target counts cannot produce global read/action percentages;
- restart/relogin terminal coverage remains unproven.

**Impact:** any claim such as “protocol X% complete”, “QMeta X% complete”, “P0 X% complete” or “Track A mostly complete” would be unsupported.

**Smallest next discriminator/action:** build one current-main canonical registry with per-item provenance and deterministic validation. E51 must classify all 349 messages by feature family or explicit `UNCLASSIFIED`; E52 must define the complete recovered Tibia-owned runtime/QMeta set; P0/P1 must normalize individual read/action capabilities and attach experiment IDs or explicit `BLOCKED/UNSUPPORTED` rationale.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict (`612` vs historical `1004`)

**Classification:** CONFLICT / unresolved metric-definition mismatch.

`docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md` retains `HIGHLEVEL_ACTION_METHOD_COUNT=612` from the direct high-level action census while also preserving an older `1004` action summary. The report explicitly states that the two values must be treated as different definitions until the `1004` provenance/filter is reconstructed.

**Impact:** no global action-method percentage may use either number as a silent denominator. The accepted `29/31` GameAction sender result remains only a selected high-information subset.

**Smallest next discriminator/action:** reconstruct the exact query/filter/provenance that produced `1004`, normalize namespace/type/method inclusion rules against the retained `612` census, adopt one machine-verifiable denominator, and retain the other metric as historical/alternate scope if both are legitimate.

### AUD-COV-004 — HIGH — live semantic promotion is blocked by the canonical runtime/bootstrap chain

**Classification:** FACT.

RUNTIME #358 performed a valid read-only Synology reconciliation (`31944216131` / `95157691875`) and proved:

```yaml
canonical_lease_status: absent
canonical_lease_generation: 0
canonical_registration: ABSENT
bootstrap: REQUIRED_UNIMPLEMENTED_on_trusted_main
target_uniqueness: UNKNOWN
mutation_authorized: false
```

Bootstrap/rebind implementation #360 is not promotion-safe. Coordinator audit `5307269111` retains four material blockers:

1. `TACOORD-360-001` HIGH — failed post-write rebind probe may leave advanced registration authoritative;
2. `TACOORD-360-002` HIGH — transition/worker shell argv contract is incompatible;
3. `TACOORD-360-003` HIGH — login credentials are exposed in child argv through `xdotool`;
4. `TACOORD-360-004` material dependency — `wireproxy.pid` / SOCKS `25354` ownership is not proven current/non-#303/authorized.

**Impact:** no current physical mutation/login/bootstrap is authorized. Consequently current `IN_GAME`, live bridge correlation, direct player XYZ, causal P0 reads/actions, R3/R4/A4 restart stability and physical E2E cannot be promoted.

**Smallest next discriminator/action:** repair exactly the four #360 findings with deterministic hosted tests, independently re-audit, then deliberately promote the corrected primitive to trusted `main`. Only then may #358 execute Gate A -> bootstrap/rebind -> Gate B -> bounded login/relogin/E2E. The first high-information physical proof should be structural `IN_GAME` plus bridge/session correlation, followed by direct player XYZ and fresh-PID/relogin repeatability.

### AUD-COV-005 — HIGH — compliant exact-client GitHub-hosted input is not yet proven reusable for static closure

**Classification:** FACT at the last persisted P2/P0 evidence boundary; new #302 retrieval change is IN_PROGRESS/UNVALIDATED at this snapshot.

P2 #310 has two accepted GitHub-hosted/no-runtime materialization attempts:

```yaml
run_31944074222: download.tibia.com DNS failure
run_31944119641: static.tibia.com HTTP 403
semantic_validator_executed: false
synology_static_fallback: forbidden
```

Therefore the current P2 first downstream consumer, framing/stage order, sequence/compression/encryption boundary and final binary egress remain `UNKNOWN`.

P0 #302 shares the same exact-client fence. Its newly observed head `d0b56ce562eb3ef6e59c1635687204917553dd32` replaces historical Synology static execution with a GitHub-hosted exact-client retrieval hypothesis using the official static endpoint plus a same-URL Referer. At this snapshot the durable P0 task/evidence still classifies hosted input as blocked and no new exact-SHA semantic artifact/result has yet been persisted. The new workflow commit itself is not proof that input staging succeeded.

**Impact:** both P2 exact-binary closure and the missing P0 instruction window around `0x8367c1` remain blocked until a hosted run proves exact size/SHA and produces sanitized evidence.

**Smallest next discriminator/action:** consume the first terminal exact-SHA-fenced result from the new hosted P0 retrieval hypothesis. If it legally and technically materializes the exact official binary, coordinator should evaluate that same compliant staging mechanism for P2 rather than inventing a second source. If it fails, establish one coordinator-approved GitHub-hosted-readable staging source; do not fall back to Synology for deterministic static RE.

### AUD-COV-006 — MEDIUM — P1 code findings are repaired, but P1 is not yet promotable and has no live semantic authority

**Classification:** FACT.

P1 #357 repaired the two earlier semantic code findings and validated the repaired implementation at `bf0fe057c5f320508dc7c9f0e5f2a55c2c3e1448` in run `31947365151=SUCCESS`. The current observed PR head `fe37b80423d7cc8b269cd58edc19a2795e01e381` removes the temporary validation workflow after that component validation.

Open gates remain:

- same-PR reusable integration records in `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` are blocked on serialization because open PR #23 owns those shared paths;
- current-main refresh and final exact-head normal governance/repository CI remain to be completed after integration;
- coordinator promotion remains required;
- `session-status` remains `DERIVED_UNTIL_LIVE_CORRELATION` and does not prove current canonical runtime, `IN_GAME`, restart/relogin stability or player position.

**Impact:** repaired hosted bridge code improves implementation coverage, but does not increase live semantic/R4 coverage yet.

**Smallest next discriminator/action:** serialize shared index ownership, add integration docs on #357, refresh from current main, run exact final-head governance/CI, coordinator-review the final branch. Physical bridge/session correlation remains a separate bounded RUNTIME proof.

### AUD-COV-007 — MEDIUM — durable coordinator checkpoint is stale relative to live Git state

**Classification:** FACT.

Current-main task `docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` is a waiting snapshot whose embedded `current_main` is `0d7b2607912552599ae501891491aab439cfde7b`. Live `main` is `ddf7dd9408116fbeaca05bfeb69663f30f7cd34f`.

The checkpoint also still lists #325 and #295 among relevant open PRs even though both are closed unmerged, and its P1 lane barrier records head `edcc3f85bbe084667cb89024b54cd3ab79185809` while live #357 has advanced through repaired heads to `fe37b80423d7cc8b269cd58edc19a2795e01e381`.

**Impact:** the coordinator document is useful historical state but must not be treated as the current lane barrier. Repository policy already resolves the conflict correctly: live Git/PR state has higher authority.

**Smallest next discriminator/action:** the next coordinator invocation should refresh its single owned checkpoint from exact live main/heads and current accepted evidence, removing closed PRs and incorporating the repaired P1 state. No other lane should mutate the coordinator checkpoint.

### AUD-COV-008 — MEDIUM — QLibrary load-bearing hosted validator is still failed

**Classification:** FACT.

#356 exact head `f8e3733aa90bde0cd93c3bc6c3a364ac02b625dd` has green repository governance/CI but load-bearing Qt source validation `31943243252` / job `95155325324` failed. Coordinator findings remain:

- `QLIB-COORD-001`: validator expects the wrong Qt 6.9.3 `.so` suffix source form;
- `QLIB-COORD-002`: generated candidate order must remain distinct from actual `dlopen` attempt order because an existing absolute-path candidate that fails to load can stop later retries.

**Impact:** green generic CI cannot be used as evidence for QLibrary semantic resolution, and actual successful runtime mapping remains `UNKNOWN`.

**Smallest next discriminator/action:** repair the structural source validator on #356 against exact official Qt 6.9.3 source, encode generated-vs-attempted ordering explicitly, rerun hosted validation, persist hashes/output, and retain successful runtime mapping as unknown absent RUNTIME evidence.

### AUD-COV-009 — MEDIUM — viewport continuation metadata is stale against the promoted current-main feasibility checkpoint

**Classification:** FACT for lifecycle staleness; governance consequence is RECOMMENDATION pending #363 owner refresh.

#363 task `docs/agents/tasks/active/OTC-20260816-track-a-viewport-continuation-prompt.md` still treats PR #325 as a current dependency/read-only source. Live #325 is closed unmerged; its accepted report/evidence was replayed and promoted to `main` through #366, and the feasibility task is archived on `main@ddf7dd...`.

The #363 task also predates the full post-#331 hybrid-routing front-matter shape used by current Track A tasks: it records `runtime_access: none` admission fields, but does not record `routing_contract`, `execution_class`, `persistent_session_role` and `physical_e2e_required` in the active task checkpoint.

The prompt's strict GUI rule itself remains safe: it says to reuse an existing logged-in session only when current ownership/admission permits and otherwise stop `WAITING/BLOCKED`. Because current canonical PID/session are `NOT_REGISTERED`, the prompt must not infer that such a reusable session exists.

**Impact:** a new viewport worker could start from stale lifecycle metadata even though the research conclusions themselves were preserved on current `main`.

**Smallest next discriminator/action:** #363 owner should replace #325 lifecycle dependency with the current-main feasibility report/evidence/archive, add the current hybrid-routing fields for a GitHub-hosted/no-runtime task, preserve the `NOT_REGISTERED` runtime nonclaim, then run exact-head governance/CI. No runtime bootstrap is justified by this documentation repair.

## Supersessions and negative evidence that must remain explicit

The audit retains the following non-positive evidence rather than allowing later workers to rediscover/re-promote it accidentally:

| Evidence / model | Required classification |
|---|---|
| historical `0xb5b880` P2 endpoint model | `DISPROVEN/SUPERSEDED` |
| `0xb46bd0` binary gameplay sink claim | `DISPROVEN/SUPERSEDED` |
| `0xc33259` network-sink claim | `DISPROVEN/SUPERSEDED` |
| stale `TProtocolWriter` RTTI `0x3080700` | `DISPROVEN/SUPERSEDED`; later exact evidence used corrected `0x3080728` |
| PR #303 physical runtime surfaces | `CLOSED_SUPERSEDED`, historical evidence only, never current runtime authority |
| PR #325 viewport task branch | `CLOSED_SUPERSEDED`; accepted report/evidence now on current `main` via #366 |
| PR #304 coverage branch | `CLOSED_UNMERGED`; accepted bounded evidence only, not current canonical registry |
| socket existence/byte deltas alone | insufficient for `IN_GAME` or server-accepted movement |
| green generic CI alone | execution evidence only, never semantic/capability proof |

## Missing-proof queue, ordered by information gain

| Priority | Missing proof | Owning lane / executor | Smallest falsifiable next step |
|---:|---|---|---|
| 1 | current canonical machine-readable coverage registries | COVERAGE-AUDIT + coordinator, GitHub-hosted | promote/regenerate provenance-preserving `capabilities`, `protocol_messages`, `runtime_types` and validator on current main |
| 2 | full 349-message semantic/family classification | protocol/COVERAGE-AUDIT, GitHub-hosted | E51: every identifier gets family or explicit `UNCLASSIFIED`, fields/handler provenance where known |
| 3 | full Tibia-owned QMeta/runtime denominator | QMeta/COVERAGE-AUDIT, GitHub-hosted | E52: enumerate types/controllers/storages, classify every entry or ignored-with-reason |
| 4 | exact-client hosted staging | coordinator + P0/P2, GitHub-hosted | prove one official exact-SHA staging mechanism and reuse it across static lanes |
| 5 | promotion-safe canonical bootstrap/rebind | RUNTIME-INFRA #360, GitHub-hosted tests first | repair TACOORD-360-001..004 and pass independent re-audit |
| 6 | structural current `IN_GAME` + bridge correlation | RUNTIME #358, Synology physical only after trusted gates | Gate A/bootstrap/Gate B then one bounded structural session proof; no historical display/PID reuse |
| 7 | direct authoritative player XYZ | P0 static + RUNTIME physical evidence | recover member/accessor candidate; two passive live observations + structural world comparison + camera/viewport negative controls |
| 8 | restart/relogin stability | RUNTIME with P0/P1 consumer | fresh PID/PIE/session, rediscover and reproduce same semantic read/bridge correlation |
| 9 | P2 downstream transform/framing/egress | P2 GitHub-hosted | once exact input exists, prove first consumer then one stage at a time; keep compression/encryption/sequence/final egress unknown until exact evidence |
| 10 | action/QMeta normalized denominator | COVERAGE-AUDIT/QMeta, GitHub-hosted | reconcile `612` vs `1004`, then classify selected action surfaces against one explicit denominator |
| 11 | viewport patch/dependency graph | viewport static RE, GitHub-hosted | consume current-main feasibility report and recover extent/storage/protocol/render/camera/picker field/reader/writer graph before mutation |

## Campaign completeness verdict

```yaml
protocol_identifier_inventory_complete: true
protocol_semantic_coverage_complete: false
qmeta_handler_subset_inventory_complete: true
full_qmeta_runtime_denominator_complete: false
p0_group_requirement_inventory_complete: true
p0_item_level_read_action_denominator_complete: false
p1_implementation_profile_inventory_complete: true
p1_global_semantic_coverage_complete: false
p2_chain_complete: false
canonical_physical_runtime_ready: false
restart_relogin_stability_proven: false
stable_live_bridge_semantics_proven: false
programme_complete: false
```

No evidence in this audit supports a Track A completion claim. The largest quantitative progress is inventory/structural coverage. The highest-information remaining work is to restore a canonical queryable registry, clear exact-client hosted staging, make the canonical bootstrap path promotion-safe, and then use RUNTIME only for the narrow physical discriminators that static GitHub-hosted work cannot prove.

## Audit and E2E classification

```yaml
audit:
  result: FAIL_MATERIAL_GAPS_OPEN
  findings:
    high: 4
    medium: 5
  false_completion_claim_found: false
  inventory_vs_semantic_boundary_preserved: true
  historical_runtime_promoted_to_current: false
  negative_evidence_preserved: true
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs exclusively to the admitted RUNTIME lane
```

The next gate for this Draft is exact-head repository/governance validation and coordinator review. This researcher does not merge or promote global coverage state.
