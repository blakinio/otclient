# Canonical coverage registry — fresh independent audit

Date: 2026-08-17
Task: `OTC-20260817-track-a-canonical-coverage-registry`
PR: #454
Audited registry head: `7eb39676a235c6af07f3c891dfa9348a5ac43bb6`
Trusted main: `d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab`

## Scope

Falsify the claim that #454 closes only `AUD-COV-001` without converting the accepted #304 bounded inventory into global semantic truth. GitHub/repository evidence only; no runtime/client/Synology use.

## Independent checks

| ID | Check | Result |
|---|---|---|
| CCR-A01 | source authority | PASS — #304 exact `43a60bd...`, coordinator `ACCEPT_WITH_EDITS`, CI `31882010038` |
| CCR-A02 | exact source identity | PASS — promoted accepted baseline/provenance files are fenced by exact Git blob SHA-1 |
| CCR-A03 | protocol inventory | PASS — validator decompresses and hashes exactly 349 unique names = 189 inbound + 160 outbound |
| CCR-A04 | runtime/QMeta inventory | PASS — 47 unique bounded handler records, semantic default UNKNOWN |
| CCR-A05 | negative evidence | PASS — retained `DISPROVEN/SUPERSEDED` and scope `UNKNOWN` records |
| CCR-A06 | stale-source containment | PASS — historical README/blockers/summary/validator/output are `source-*`; current programme state is separate overlay |
| CCR-A07 | semantic non-overclaim | PASS — message semantics UNKNOWN/349, Qt semantics UNKNOWN/2184, P0/P1 item denominators UNKNOWN/UNKNOWN |
| CCR-A08 | P2 boundary | PASS — bounded chain promoted; framing/sequence/compression/encryption/final egress/socket ownership UNKNOWN |
| CCR-A09 | worldmap boundary | PASS — mutation design ready; safe mutation and physical execution authorization false |
| CCR-A10 | RUNTIME boundary | PASS — merged #448 consumed; exact XID→official-client PID, registered session and Gate-B semantics remain unproven |
| CCR-A11 | finding accounting | PASS — resolves only `AUD-COV-001`; remaining exactly `002,003,004,007` = 4 findings, 2 HIGH + 2 MEDIUM |
| CCR-A12 | safety | PASS — no raw client, runtime, credentials, login/gameplay, process memory or owner-funded AI |
| CCR-A13 | reusable validator | PASS — canonical `validate_registry.py` remains durable and directly runnable from the README |
| CCR-A14 | review hygiene | PASS — 0 reviews and 0 unresolved review threads at audit checkpoint |

## Resolved audit findings

### CCR-AUD-001 — MEDIUM — RESOLVED

After #448 merged, the first restacked validator still expected `raw_xres_promotion_merged == false`. The overlay was correctly `true`; the stale assertion was fixed to pin merge `d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab` while keeping physical XID→PID and Gate-B semantics unknown. Dedicated run `32013364473`, job `95337501296` then passed with `CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS` and `SOURCE_BASELINE_BLOBS_EXACT=true`.

### CCR-AUD-002 — MEDIUM — RESOLVED

The first terminal tree kept a new dedicated Track A workflow while removing the active admission task. Governance run `32013621176` correctly rejected that lifecycle shape because new Track A workflows are runtime-sensitive governance paths.

Resolution: the dedicated workflow is removed from the terminal tree. It served only as the GitHub-hosted validation vehicle for run `32013364473`. The reusable validator itself remains canonical, documented and executable; final exact-head repository/governance checks verify the terminal tree.

## Audit disposition

```yaml
audit_result: PASS
material_findings_open_for_this_task: 0
resolved_task_findings:
  - CCR-AUD-001
  - CCR-AUD-002
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

Terminal merge is allowed only after the exact final head passes Track A governance, repository required CI, review hygiene and final main-drift checks. The component validator evidence remains run `32013364473` on the unchanged registry/validator payload.
