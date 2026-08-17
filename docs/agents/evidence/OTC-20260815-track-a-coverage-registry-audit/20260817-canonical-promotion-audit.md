# Canonical coverage registry — fresh independent audit

Date: 2026-08-17
Task: `OTC-20260817-track-a-canonical-coverage-registry`
PR: #454
Audited implementation head: `7eb39676a235c6af07f3c891dfa9348a5ac43bb6`
Trusted main: `d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab`
Audit role: fresh proportionate repository/data validator

## Scope

The audit attempts to falsify the claim that #454 closes only `AUD-COV-001` without silently upgrading historical inventory evidence into current semantic facts. It uses live GitHub state, accepted source #304, the exact PR diff, validator output and current-main lane state. It performs no runtime/client/Synology work.

## Checks

| ID | Check | Result |
|---|---|---|
| CCR-A01 | source authority | PASS — #304 exact head `43a60bd...` was coordinator `ACCEPT_WITH_EDITS` bounded inventory only; source CI `31882010038` SUCCESS |
| CCR-A02 | source identity | PASS — canonical manifest fences every promoted accepted baseline/provenance artifact by exact Git blob SHA-1 |
| CCR-A03 | protocol inventory | PASS — validator independently decompresses/hashes exact 349 identifiers and proves 189 inbound + 160 outbound |
| CCR-A04 | runtime/QMeta inventory | PASS — exact baseline carries 47 unique bounded handler records with semantic default UNKNOWN |
| CCR-A05 | negative evidence | PASS — `DISPROVEN/SUPERSEDED` records including the obsolete `0xb5b880` model remain present; UNKNOWN scope records remain present |
| CCR-A06 | stale-source containment | PASS — old README/blockers/summary/validator/output are retained with `source-` prefixes; current routing/state lives in overlay files |
| CCR-A07 | semantic non-overclaim | PASS — protocol semantics stay UNKNOWN/349; direct Qt semantics UNKNOWN/2184; P0/P1 item-level denominators UNKNOWN/UNKNOWN |
| CCR-A08 | P2 overlay | PASS — bounded chain is promoted but framing/sequence/compression/encryption/final egress/socket ownership remain UNKNOWN |
| CCR-A09 | worldmap overlay | PASS — mutation design is promoted/ready, while safe mutation and physical execution authorization remain false |
| CCR-A10 | RUNTIME overlay | PASS — #448 merge is consumed; exact XID→official-client PID, registered session and Gate-B semantics remain unproven |
| CCR-A11 | audit finding accounting | PASS — candidate tree resolves only `AUD-COV-001`; remaining set is exactly `002,003,004,007` = 4 findings, 2 HIGH + 2 MEDIUM |
| CCR-A12 | execution safety | PASS — GitHub-hosted deterministic data validation only; no raw client, runtime, credentials, login/gameplay, process memory or owner-funded AI |
| CCR-A13 | reusable validation | PASS — permanent path-scoped GitHub-hosted workflow executes the canonical validator on registry/report changes |
| CCR-A14 | review hygiene pre-closeout | PASS — 0 reviews and 0 unresolved review threads at implementation audit checkpoint |

## Finding discovered during audit

### CCR-AUD-001 — MEDIUM — RESOLVED

After #448 merged, the first restacked validator still asserted the prior overlay state `raw_xres_promotion_merged == false`. The overlay itself had been correctly refreshed to `true`, so this stale assertion would have produced a false validation failure.

Resolution:
- validator now requires `raw_xres_promotion_merged == true`;
- it pins the accepted merge `d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab`;
- it still requires `exact_resource_to_official_client_pid == UNKNOWN`, `current_exact_client_pid == NOT_REGISTERED`, and `canonical_gate_b == NOT_PROVEN`.

Dedicated run `32013364473`, job `95337501296` then passed with `CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS` and `SOURCE_BASELINE_BLOBS_EXACT=true`.

## Audit disposition

```yaml
audit_result: PASS
material_findings_open_for_this_task: 0
resolved_task_findings:
  - CCR-AUD-001
AUD-COV-001: RESOLVED_IN_CANDIDATE_TREE
programme_findings_remaining:
  - AUD-COV-002 HIGH
  - AUD-COV-003 MEDIUM
  - AUD-COV-004 HIGH
  - AUD-COV-007 MEDIUM
programme_complete: false
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

Terminal closeout may archive/release this task and merge only after the exact terminal head passes the dedicated registry workflow, Track A governance, repository required CI, review hygiene and final main-drift checks.
