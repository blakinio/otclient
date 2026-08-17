# Track A semantic denominator normalization — fresh audit

Task: `OTC-20260817-track-a-semantic-denominator-normalization`  
PR: #460  
Validator role: fresh proportionate COVERAGE-AUDIT validator  
Trusted base: `main@1eb4a8edecba3966aa1e6155e241b404eb4d30cb`

## Scope

Attempt to falsify the claim that finite denominators can be promoted without converting inventory, lexical grouping, structural QMeta records, implementation fields or historical runtime evidence into semantic completion.

No client/runtime/Synology/login/gameplay/process-memory access was used by this task.

## Primary evidence

- canonical exact #304 source-fenced registry;
- hosted generation run `32017799293`, job `95350885329`, artifact `9284175545`, digest `sha256:cf2fb874e39af2465de76445347a118077893d9bbf213b69809b793ed4d7f577`;
- independent artifact ZIP digest/file/count/uniqueness inspection;
- full retained QMeta census run `31790507112`, job `94736106350`, source head `c04ff82918f954af019ab533bf6af0792dc730bf`;
- integrated canonical validator run `32018548728`, job `95353113344`;
- current trusted-main physical XRes identity and helper-fix lineage #457/#459/#461.

## Falsification checks

| ID | Check | Result |
|---|---|---|
| SD-A01 | immutable baseline | PASS — canonical validator reports `SOURCE_BASELINE_BLOBS_EXACT=true` |
| SD-A02 | E51 membership | PASS — exactly 349 unique IDs, exact set equality with canonical protocol inventory, 189 inbound + 160 outbound |
| SD-A03 | E51 semantic boundary | PASS — all 349 semantic states remain `UNKNOWN`; family is explicitly `LEXICAL_NORMALIZATION`/`UNCLASSIFIED`, never semantic proof |
| SD-A04 | E51 structural links | PASS — exactly the canonical 27 direct QMeta cases are marked |
| SD-A05 | E52 membership | PASS — 642 unique `tibia::` type names and 642 unique QMeta record VAs from exact retained full census |
| SD-A06 | E52 scope | PASS — 708 structural records = 642 Tibia-owned + 66 non-Tibia; denominator contains only the 642 retained Tibia-owned records |
| SD-A07 | E52 semantic boundary | PASS — all 642 semantic states remain `UNKNOWN`; historical 47 handler set is represented as a bounded subset, not the full denominator |
| SD-A08 | E52 kind partition | PASS — 303 OTHER_QMETA + 187 CONTROLLER + 77 STORAGE + 47 HANDLER + 28 ACTION_HANDLER = 642 |
| SD-A09 | P0 normalization | PASS — 180 unique item requirements across all groups 0..15; 16 headings remain grouping only; all live semantics remain UNKNOWN |
| SD-A10 | P1 normalization | PASS — 28 unique requirements; seven discovery targets remain a subset; `session_status.in_game_candidate` remains DERIVED and restart semantic reacquisition UNKNOWN |
| SD-A11 | finding accounting | PASS — resolves `AUD-COV-002` only as denominator completeness; `AUD-COV-003`, `004`, `007` remain open = 3 findings, 1 HIGH + 2 MEDIUM |
| SD-A12 | RUNTIME boundary | PASS — historical physical resource→PID proof is recorded as `PROVEN_AT_RUN`; current PID/session remain NOT_REGISTERED and Gate B/IN_GAME remain NOT_PROVEN |
| SD-A13 | P2/worldmap boundary | PASS — P2 transport semantics stay UNKNOWN; worldmap safe mutation/physical authorization stay false |
| SD-A14 | validator | PASS — integrated canonical validator prints `CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS` on run `32018548728` |

## Repair history

Two generator failures were bounded tooling defects, not denominator evidence failures:

1. retained Actions-log redirect authorization plus missing output directory;
2. historical log echoed source text containing `{len(records)}` before the actual numeric marker.

Both were repaired with narrower deterministic parsing. The first successful package was independently downloaded and inspected before canonical materialization. No failing attempt was re-labelled as evidence.

## Disposition

```yaml
audit_result: PASS
material_findings_open_for_this_task: 0
AUD-COV-002: RESOLVED_AS_DENOMINATOR_COMPLETENESS
protocol_denominator: 349
protocol_semantic_support: UNKNOWN/349
full_tibia_qmeta_denominator: 642
full_tibia_qmeta_semantic_support: UNKNOWN/642
P0_item_denominator: 180
P0_live_semantics: UNKNOWN/180
P1_item_denominator: 28
P1_live_semantics: UNKNOWN/28
remaining_programme_findings:
  - AUD-COV-003 MEDIUM
  - AUD-COV-004 HIGH
  - AUD-COV-007 MEDIUM
programme_complete: false
runtime_access: none
physical_e2e: NOT_APPLICABLE
```

The temporary generator/workflow is validation machinery for this task and must not survive the terminal tree without an active Track A admission record. The reusable canonical deliverable is the materialized JSONL data plus `validate_registry.py`.
