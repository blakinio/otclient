---
task_id: OTC-20260728-asset-input-evidence
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R09
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-AR
parallel_lane_state: active
coordinator_task: none
branch: docs/OTC-20260728-asset-input-evidence
base_branch: main
created: 2026-07-28T23:43:00+02:00
updated: 2026-07-28T23:43:00+02:00
last_verified_commit: "a6c8d1cfcac9364612c2ac56a9dc12618581adc9"
required_base_commit: "a6c8d1cfcac9364612c2ac56a9dc12618581adc9"
risk: low
related_issue: ""
related_pr: pending
depends_on:
  - merged foundation audit PR #47
  - merged current parallel-wave plan PR #59
blocks:
  - safe selection of the first synthetic asset-types/compiler slice
owned_paths:
  - oteryn-client/docs/research/asset-inputs/**
  - docs/agents/tasks/active/OTC-20260728-asset-input-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - accepted asset security/provenance architecture
  - foundation asset and licensing audit
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted asset schema or pack contract
modules_touched: []
reuses:
  - foundation asset/licensing audit
  - accepted asset pipeline and security model
  - repository MIT source license only for code/documentation covered by it
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no importer or runtime performance claim
security_evidence:
  - no asset bytes, archives, captures, credentials or private paths
  - importer checklist fails closed on untrusted inputs
---

# Goal

Refine the legal/source/provenance boundary for future Rust asset work, define a content-free inventory schema, record importer threat controls and recommend one synthetic first slice without adding real asset bytes, pack schemas, compiler code or external-repository changes.

# Acceptance criteria

- [ ] Required asset families are classified by safe source and rights state without treating technical availability as permission.
- [ ] Repository MIT licensing is not incorrectly extended to third-party or proprietary content.
- [ ] A content-free inventory schema captures origin, license, hashes, dimensions/counts and compatibility without embedding bytes.
- [ ] Importer threat checklist covers bounds, arithmetic, decompression, archives/paths, cancellation, determinism and secret/private-path handling.
- [ ] One small synthetic asset-types/compiler recommendation is specific and implementable without freezing official Tibia/Canary formats.
- [ ] No real sprite, thing, sound, font, archive, manifest, protocol constant, Cargo, workflow, architecture or external-repository change.
- [ ] Exact changed files stay inside the isolated research path and task lifecycle.
- [ ] Exact-head required CI passes; PR merges and archives separately.

# Confirmed context

- Current `main` is `a6c8d1cfcac9364612c2ac56a9dc12618581adc9`.
- Foundation audit classifies complete distributable game-content rights and exact official 15.25 schema as blocked.
- Root MIT license covers the OTClient software/documentation grant it names; it does not by itself establish redistribution rights for unrelated third-party game assets.
- Open PR #37 concerns the maintained legacy auto-installer and remains blocked on a real-release rehearsal; it does not own Rust asset research paths or authorize Rust reuse of downloaded content.
- PR #48 keeps official Tibia Linux bytes on an isolated NAS and explicitly uploads no binaries/assets; it provides no redistribution authorization.
- No current task or PR owns `oteryn-client/docs/research/asset-inputs/**`.

# Plan

1. Open an early draft PR.
2. Review accepted asset architecture/security/audit evidence and repository licensing boundaries.
3. Write source/rights matrix, non-content inventory schema, importer threat checklist and one synthetic slice recommendation.
4. Review the complete docs-only diff and run exact-head CI.
5. Merge and archive independently.

# Validation

| Revision | Check | Result | Evidence |
|---|---|---|---|
| `a6c8d1cfcac9364612c2ac56a9dc12618581adc9` | live ownership/source preflight | PASS | W2-AR path unclaimed; no real bytes proposed |

# Boundaries

- no legal conclusion beyond recorded evidence; unresolved rights remain blocked;
- no scraping/extraction/downloading or inspection of private user asset directories;
- no content bytes, source paths identifying a user, archive manifests or proprietary metadata dumps;
- no schema/pack/compiler contract accepted by this research PR;
- no change to legacy installer behavior or security policy.

# Remaining work

1. Open the draft PR and complete the four isolated evidence documents.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
