# TIBIA-RE-FEATURES static G0 — coordinator promotion audit

```yaml
date: 2026-08-19
source_task: OTC-20260819-track-a-features-static-g0
source_pr: 560
source_head: 2822de1bc916a581de5aa3eb0601c1708c468b39
coordinator_review: 4970396563
coordinator_decision: ACCEPT_WITH_EDITS
material_finding: FEATURE-AUD-001
open_material_findings_after_repair: 0
promotion_base: 08c0b6f89ffddd4c75b8f60060ce3b2a62195d95
runtime_access: none
mutation_authorized: false
physical_e2e_required: false
```

## Independent evidence verification

The coordinator did not rely on the researcher summary alone.

Producer artifact `9356800104` from run/job `32229656311 / 95996576897` was downloaded directly from GitHub Actions. Independent SHA-256 of the ZIP was:

```text
779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
```

This exactly matches GitHub's artifact digest metadata. The four extracted files independently reproduced the researcher-recorded hashes:

```text
features-qmeta.txt             fb153fed5966e1bebfa6910d9989f38655dd8469dc62d592c7bec0dc0fa11292
features-strings.txt           267a0e4c7e511276a95b1d9430e84131041b6ec8251a43e7d756ec72afb533dd
features-protocol-strings.txt  c05ed496bddd15f9857b820601daa88b0cf7f0484bc9cd4b048870d6472d628e
fence.txt                      e8f7da77eb41efbbb507103879014dc84c1d80b0efef3de530870361c76cbcbf
```

The producer workflow at `9ae46d14807e46e76c044c336e50033b11fa3a1e` was independently re-read. It fails closed on the exact current public package, parses Qt metaobjects structurally, and records QMeta/static-metacall ownership plus method/property/enum names. It does not derive per-method native code targets from jump-table heuristics and does not prove semantic dispatcher edges.

Exact current package reproduced by the artifact:

```text
packed SHA-256:   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked size:    52109920
unpacked SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
raw client retained: false
```

## Verified structural findings

Raw QMeta evidence independently confirms the material surfaces used by the four proposed rows, including:

- G01: `TCyclopediaProtocolMessageHandler` and `TCyclopediaDialogController`, explicit send/handle methods, tab/back navigation, subsystem-controller properties and `DialogTab` enum;
- G04: `TBestiaryTrackerProtocolMessageHandler`, `TMonsterRaceStorage`, `TCreatureTrackerWidgetController`, `TMonsterDialogController`, and `TQmlMonsterRace` kill/unlock/loot/progress fields;
- G05: charm view/remove/assign controller methods plus `majorCharm`, `minorCharm`, selected charm ID/slot, unassign-cost and affordability state;
- G06: `TMonsterBonusEffectStorage`, `TMonsterBonusEffectsDialogController`, `TQmlMonsterBonusEffect`, unlock/clear/assign surfaces, costs, assignment state and monster-race association.

The retained protocol-type strings independently include:

```text
GameclientMessageApplyClearingCharm
GameclientMessageMonsterBonusEffectAction
GameclientMessageTrackBestiaryRace
GameserverMessageBestiaryTracker
```

These are type-presence facts only. Generated message field schemas, concrete handler-to-storage mutation, server validation and causal live transitions remain unknown.

## FEATURE-AUD-001 — provenance correction

The source task metadata named `promoted public-package fingerprint from PR #551` as a dependency. That pointer is incorrect: #551 is the world/minimap promotion. The current canonical public-package/runtime fence was advanced by PR #555, squash merge:

```text
2e572789a2bc4b64c5e906c4515c15c625f6bc9e
```

and its lifecycle closeout #561 is present on trusted main through:

```text
34e41a04d62e642ef0ae67c79354f183473270a3
```

This is a provenance metadata defect only. The source producer independently fetched and fenced the exact package, and current trusted main now carries the same canonical fence. No evidence claim is weakened by the correction.

## Accepted coverage delta

Under PR #536's status vocabulary, this promotion accepts only the bounded task-local structural deltas:

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

No row is `DONE`. PR #536 shared matrix/checklist paths are intentionally untouched.

## Remaining UNKNOWN

- generated request/response field schemas;
- handler -> storage/controller causal writes;
- G01 cache ownership, lifetime and invalidation;
- Bestiary authoritative server/static field ownership and tracker limits/order;
- charm assignment/clearing validation, formulas, constraints and persistence;
- Monster Bonus Effect action variants, resource/cost formulas, validation and persistence;
- live success/error transitions, reconnect/character-switch behavior and runtime causality.

## Safety / E2E

This is static GitHub-hosted research only. No client execution, Synology/KasmVNC access, login, credentials, gameplay, resource spending, reroll, Forge/Imbuement commit or client-byte mutation occurred. Physical E2E is `NOT_APPLICABLE` for this bounded static evidence promotion.
