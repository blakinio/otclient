---
task_id: OTC-20260815-track-a-coverage-registry-audit
status: validating
agent: chatgpt-coverage-auditor
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static-research-audit
phase: exact-head-ci-validation
branch: research/OTC-20260815-track-a-coverage-registry-audit
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-coverage-registry-audit
worktree_mode: isolated_branch_checkout_equivalent
risk: low
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-coverage-registry-audit.md
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/**
depends_on:
  - main canonical Track A evidence
  - coordinator PR #300 promotion ledger
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
---

# Objective

Build a reproducible item-level quantitative coverage baseline from existing exact-version Track A evidence without performing new runtime experiments and without presenting selected-subset census percentages as global semantic coverage.

# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-coverage-registry-audit
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-coverage-registry-audit.md
PROJECT_LANE: otclient
LANE: COVERAGE-AUDIT
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-coverage-registry-audit
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-coverage-registry-audit
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-coverage-registry-audit.md
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/**
DEPENDENCIES:
  - current-main canonical Track A evidence and registries, read-only
  - coordinator PR #300 classification ledger
```

Research output is DRAFT-ONLY. Promotion/canonical registry placement belongs to the coordinator after review.

# Exact client scope

Primary baseline is fenced to official Linux client:

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Evidence for any other build must be separately keyed and must not silently satisfy this denominator.

# Starting quantitative checkpoint

Existing exact-build baseline contains:

```yaml
protocol_identifier_inventory: 349/349
protocol_handler_qmeta_records: 47/47
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
direct_qt_connection_semantic_classification: UNKNOWN/2184
generated_message_semantic_classification: UNKNOWN/349
p0_live_read_coverage: UNKNOWN/UNKNOWN
```

The first two 100% values are inventory completeness for their stated scopes only. They do not prove semantic protocol/action/read coverage.

# Required registries

Create task-scoped draft registries under the owned evidence root, for example:

```text
docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/capabilities.jsonl
docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/protocol_messages.jsonl
docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_types.jsonl
docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/coverage-summary.json
```

Do not write canonical shared registry paths in this task.

# Classification rules

Every item must carry sufficient provenance to distinguish at least:

```text
FACT
INFERENCE
UNKNOWN
DISPROVEN/SUPERSEDED
NOT_APPLICABLE_WITH_REASON
```

Where applicable include exact client identity, evidence file/run/job/artifact, semantic family, read gate/action gate, and the exact reason an item is unresolved. Duplicated worker claims count once; contradictory evidence remains explicit.

# Acceptance gate

- [x] denominator definition is explicit for every percentage;
- [x] all 349 named generated messages are represented individually or an exact machine-verifiable source proves the item set;
- [x] all protocol-handler QMeta records used in the denominator are represented individually;
- [x] known 2184 direct Qt connection callsites are either itemized/classified or explicitly separated into a raw-census denominator with semantic numerator UNKNOWN;
- [x] P0 read families receive a canonical finite denominator derived from repository programme requirements, or remain UNKNOWN with the precise missing denominator decision recorded;
- [x] accepted negative evidence (`DISPROVEN/SUPERSEDED`) is retained, including the obsolete `0xb5b880` P2 model;
- [x] inventory completeness and semantic completeness are reported separately;
- [x] no selected subset percentage is labeled as global protocol/QMeta/P0 coverage;
- [x] each missing high-value item maps to one concrete follow-up hypothesis rather than a generic 'more RE needed';
- [x] deterministic validation checks duplicate IDs, invalid classifications, missing provenance, denominator mismatch and percentage arithmetic;
- [ ] exact-head repository CI is terminal before Draft handoff.

# Runtime boundary

No runtime execution, login, action, secret access or client mutation is authorized or required. This lane audits durable repository evidence only.

# Deliverable

Draft PR only with task-scoped machine-readable registries, validation evidence and a summary of exact remaining coverage gaps. The coordinator decides which registry slices become canonical.

# Execution checkpoint — 2026-08-15

Evidence root: `docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/`.

Static registry validation is terminal locally with `COVERAGE_AUDIT_VALIDATION=PASS`. The validator now enforces record-ID uniqueness, allowed classifications, provenance references, exact census/hash denominators, selected-subset arithmetic, percentage arithmetic and retained `0xb5b880` supersession evidence.

Verified bounded results:

```yaml
protocol_messages: 349
protocol_inbound: 189
protocol_outbound: 160
protocol_direct_qmeta_case_links: 27/349
protocol_handler_qmeta_records: 47/47
direct_qt_raw_census: 2184/2184
direct_qt_semantic_classification: UNKNOWN/2184
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
p0_top_level_requirement_groups: 16/16
p0_live_read_coverage: UNKNOWN/UNKNOWN
bridge_v1_profile_targets: 7/7
p1_overall_field_evidence_coverage: UNKNOWN/UNKNOWN
p2_chain_closure: UNKNOWN/5
restart_relogin_stability: UNKNOWN/1
```

No runtime/login/action experiment was performed. Next gate is exact-head repository CI; promotion remains coordinator-only under PR #300.
